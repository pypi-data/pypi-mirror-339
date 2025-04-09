import concurrent
import json
import os
import random
import re
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from threading import Thread
from typing import List

import loguru
import numpy as np
import pandas as pd
from kink import di, inject
from langchain_core.output_parsers import PydanticOutputParser, StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from tqdm import tqdm

from finetune.parquet.llm_init import global_llm
from finetune.parquet.read_parquet import ParquetReader
from finetune.parquet.schemas.schemas import SeedPropmts
from finetune.parquet.schemas.works.PydanticSafetyParser import ChatWithSafetyPydanticOutputParser
from finetune.tools.func.retry_decorator import retry


class finetune_tools:
    @inject
    def __init__(
            self,
            instruction: str = "",
            system_prompt: str = "",
            response_prefix: str = "",
            response_suffix: str = ""
    ):
        """
        :param instruction: alpaca 's instruction
        :param system_prompt: will not display in the final result,just for the agent to know what to do
        :param response_prefix: will display in the final result
        :param response_suffix: will display in the final result
        """
        loguru.logger.remove()
        loguru.logger.add(lambda msg: tqdm.write(msg, end=""))

        self.rows = []

        self.instruction = instruction
        self.system_prompt = system_prompt
        self.response_prefix = response_prefix
        self.response_suffix = response_suffix

        self.last_time = time.time()
        self.total_tokens = 0
        self.tps = 0

        self.alpaca_dict = []

        self.fine_tune_result_filename = f'fine_tune_datafile_{datetime.now().strftime("%Y%m%d%H%M%S")}.json.tmp'

    def log_tps(self):
        """
        Calculate the TPS(Token Per Second)
        :return:
        """
        while True:
            time.sleep(10)
            current_time = time.time()
            elapsed_time = current_time - self.last_time
            if elapsed_time > 0:
                self.tps = self.total_tokens / elapsed_time
            loguru.logger.info(f"TPS: {self.tps:.2f} tokens/sec")
            self.last_time = current_time
            self.total_tokens = 0

    def schedule_backup(self):
        """
        Schedule backup
        :return:
        """
        while True:
            time.sleep(3600)
            self.save()

    @inject
    def gen_questions(self, input_parquet_file):
        """
        Generate questions based on the knowledge base
        :return:
        """
        with global_llm():
            with ParquetReader(input_parquet_file) as pr:
                @loguru.logger.catch
                @retry(max_retries=3, delay=1)
                def invoke(i):
                    parser = PydanticOutputParser(pydantic_object=SeedPropmts)
                    promptTemplate = ChatPromptTemplate.from_messages([
                        ("system", "{system_prompt}"
                                   "{format_instructions};"),
                        ("user", "֪ʶ:{knowledgebase};")
                    ])
                    input_args = {
                        "format_instructions": parser.get_format_instructions(),
                        "knowledgebase": pr.get_line(i),
                        "system_prompt": self.system_prompt
                    }
                    res = ChatWithSafetyPydanticOutputParser(model=di['llm'], input_args=input_args,
                                                             promptTemplate=promptTemplate,
                                                             schemas_model=SeedPropmts)
                    loguru.logger.debug(np.array([res]))
                    return {"KnowledgeBase": pr.get_line(i), "questions": res}

                loguru.logger.info(f"Columns: {pr.num_columns}")
                loguru.logger.info(f"Rows: {pr.num_rows}")
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    results = list(tqdm(executor.map(invoke, range(pr.num_rows)), total=pr.num_rows))
                    self.rows.extend(results)
                df = pd.DataFrame(self.rows)
                df['questions'] = df['questions'].apply(lambda x: str(x))
                loguru.logger.debug(df.dtypes)
                datetime_format = '%Y%m%d%H%M%S'
                df.to_parquet(f'seed_prompts_{datetime.now().strftime(datetime_format)}.parquet')

    @loguru.logger.catch
    @retry(max_retries=3, delay=1)
    def _markdown_knowledgebase_invoke(self, knowledgebase_filepath: str):
        """
        处理每个markdown并生成一些问题
        :param knowledgebase_filepath: markdown文件路径
        :return:
        """
        knowledgebase_filepath = os.path.normpath(knowledgebase_filepath.strip())
        with open(knowledgebase_filepath, 'r', encoding=di['encoding']) as f:
            knowledgebase = f.read()
        parser = PydanticOutputParser(pydantic_object=SeedPropmts)
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", "{system_prompt}"
                       "{format_instructions};"),
            ("user", "{knowledgebase};")
        ])
        input_args = {
            "format_instructions": parser.get_format_instructions(),
            "knowledgebase": knowledgebase,
            "system_prompt": self.system_prompt
        }
        res = ChatWithSafetyPydanticOutputParser(model=di['llm'], input_args=input_args,
                                                 promptTemplate=prompt_template,
                                                 schemas_model=SeedPropmts)
        loguru.logger.debug(res)
        invoke_res = {"KnowledgeBase": knowledgebase, "questions": res}
        return invoke_res

    @inject
    def gen_questions_by_index_folder(self, index_folder: str):
        """
        根据目录里的所有md文件生成问题集
        :param index_folder:
        :return:
        """

        def get_all_md_files(folder_path):
            """
            获取目录下所有的md文件
            :param folder_path:
            :return:
            """
            md_files = []
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    if file.endswith('.md'):
                        md_files.append(os.path.join(root, file))
            return md_files

        markdown_files = get_all_md_files(index_folder)
        with global_llm():
            loguru.logger.info(f"Get {len(markdown_files)} markdown files.")
            self._convert_markdown_knowledge_to_parquet(markdown_files)

    @inject
    def gen_questions_by_index_file(self, index_file: str):
        """
        生成很多个问题集
        :param index_file:
        :return:
        """
        with open(index_file, 'r') as index_file:
            with global_llm():
                rows = index_file.readlines()
                loguru.logger.info(f"Rows: {len(rows)}")
                self._convert_markdown_knowledge_to_parquet(rows)

    def _convert_markdown_knowledge_to_parquet(self, knowledgebase_filepaths: List[str]):
        """
        Convert markdown knowledge base to parquet file
        :param knowledgebase_filepaths:
        :return:
        """
        rows = []
        rows = knowledgebase_filepaths
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = list(tqdm(executor.map(self._markdown_knowledgebase_invoke, rows), total=len(rows)))
            self.rows.extend(results)
        df = pd.DataFrame([row for row in self.rows if row is not None])
        df['questions'] = df['questions'].apply(lambda x: str(x))
        loguru.logger.debug(df.dtypes)
        datetime_format = '%Y%m%d%H%M%S'
        df.to_parquet(f'seed_prompts_{datetime.now().strftime(datetime_format)}.parquet')

    @inject
    @inject
    def exam(self, input_parquet_file):
        """
        Generate answer based on question and knowledge base
        :return:
        """
        fine_tune_datafile = []

        tps_thread = Thread(target=self.log_tps, daemon=True)
        tps_thread.start()

        with global_llm():
            file_lock = threading.Lock()
            data_lock = threading.Lock()

            data = []
            with ParquetReader(input_parquet_file) as pr:
                for i in tqdm(range(pr.num_rows), desc=f"Loading {input_parquet_file}"):
                    row = pr.get_raw_line(i)
                    knowledgebase = row['KnowledgeBase']
                    topics = re.findall(r"question='(.*?)'", row['questions'])
                    for topic in topics:
                        data.append({
                            'topic': topic,
                            'knowledgebase': knowledgebase
                        })
                random.shuffle(data)
                loguru.logger.debug("shuffled.")

            @loguru.logger.catch
            @retry(max_retries=3, delay=1)
            def process_item(item):
                promptTemplate = ChatPromptTemplate.from_messages([
                    ("system", "{system_prompt}"),
                    ("user", "请答题:{topic};相关知识:{knowledgebase};")
                ])

                input_args = {
                    "topic": item['topic'],
                    "knowledgebase": item['knowledgebase'],
                    "system_prompt": self.system_prompt
                }
                chain = promptTemplate | di['llm'] | StrOutputParser()
                res = chain.invoke(input_args)
                appended_data = {
                    "instruction": self.instruction,
                    "input": item['topic'],
                    "output": self.response_prefix + res + self.response_suffix
                }
                with data_lock:
                    self.alpaca_dict.append(appended_data)
                    if hasattr(self, 'fine_tune_datafile'):
                        self.fine_tune_datafile.append(appended_data)
                loguru.logger.debug(np.array([appended_data]))
                tokens_in_response = len(res)
                with data_lock:
                    self.total_tokens += tokens_in_response
                with file_lock:
                    with open(self.fine_tune_result_filename, 'a') as f:
                        f.write(json.dumps(appended_data, ensure_ascii=False) + '\n')

                return appended_data

            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                results = list(tqdm(
                    executor.map(process_item, data),
                    total=len(data),
                    desc="Processing items"
                ))

    @inject
    def convert_json_tmp_to_alpaca(self, convert_json_tmp_to_alpaca_file_path: str):
        """
        Convert .json.tmp file to .alpaca.json
        :param convert_json_tmp_to_alpaca_file_path: .json.tmp file path str
        :return:
        """

        def check_dict_alpacaify(data: dict):
            """
            Check data is alpaca format?
            :param data:
            :return:
            """
            need = ['instruction', 'input', 'response']
            for it in need:
                if it not in need:
                    return False
            return True

        alpaca_res = []
        with open(convert_json_tmp_to_alpaca_file_path, 'r') as f:
            loguru.logger.info(f"Loading {convert_json_tmp_to_alpaca_file_path}...")
            for it in tqdm(f.readlines(), desc=f"Loading {convert_json_tmp_to_alpaca_file_path}"):
                jit = json.loads(it)
                if check_dict_alpacaify(jit):
                    alpaca_res.append(jit)
                else:
                    loguru.logger.error(f"{it} require some parameters.")

        file_name_without_extension = os.path.splitext(os.path.basename(convert_json_tmp_to_alpaca_file_path))[0]
        output_file_path = f"{file_name_without_extension}.alpaca.json"
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            json.dump(alpaca_res, output_file, ensure_ascii=False)
        loguru.logger.success(f"Converted {convert_json_tmp_to_alpaca_file_path} to {output_file_path}.")

    def save(self):
        """
        Use pickle serialize class data to file
        :return:
        """
        import pickle
        with open('main.pkl', 'wb') as f:
            pickle.dump(self.rows, f)

        alpaca_dumps = json.dumps(self.alpaca_dict, ensure_ascii=False)
        dumps_filename = self.fine_tune_result_filename
        with open(dumps_filename, 'w') as f:
            f.write(alpaca_dumps)
        loguru.logger.info(f"At exit tmp save alpaca data to {dumps_filename}")

    def load(self):
        """
        If the file exists, load the data from the file
        :return:
        """
        ...
