import argparse
import atexit

import loguru
from kink import di

from finetune.parquet.fine_tuning.tools import finetune_tools


def parser_register():
    """
    Register the parsers
    :return:
    """
    parser = argparse.ArgumentParser(description='fine-tuning tools by stupidfish.')

    parser.add_argument(
        '--index_file',
        type=str,
        default='',
        help='Input a index txt,read line by line.'
    )

    parser.add_argument(
        '--index_folder',
        type=str,
        default='',
        help="Input a folder,i'll read all the .md files."
    )

    parser.add_argument(
        '--input_parquet_file',
        type=str,
        default='',
        help='Path to the input parquet file.'
    )
    parser.add_argument(
        '--encoding',
        type=str,
        default='',
        help='file encoding with markdowns.'
    )
    parser.add_argument(
        '--instruction',
        type=str,
        default='',
        help="Alpaca's instruction for the fine-tuning process."
    )
    parser.add_argument(
        '--system_prompt',
        type=str,
        default="请根据题目和原文作答，并给出准确的答案。",
        help="System prompt for the fine-tuning process."
    )
    parser.add_argument(
        '--response_prefix',
        type=str,
        default="<think>",
        help="Prefix to be added before the response."
    )
    parser.add_argument(
        '--response_suffix',
        type=str,
        default='',
        help="Suffix to be added after the response."
    )

    parser.add_argument(
        '--exams',
        action='store_true',
        help="Execute the exam method."
    )

    parser.add_argument(
        '--gen_questions',
        action='store_true',
        help="Generate questions for exam."
    )

    parser.add_argument(
        '--convert_json_tmp_to_alpaca_file_path',
        type=str,
        default='',
        help="Convert json.tmp's file to alpaca json dataset."
    )

    args = parser.parse_args()
    di['index_file'] = args.index_file
    di['index_folder'] = args.index_folder
    di['input_parquet_file'] = args.input_parquet_file
    di['encoding'] = args.encoding
    di['instruction'] = args.instruction
    di['system_prompt'] = args.system_prompt
    di['response_prefix'] = args.response_prefix
    di['response_suffix'] = args.response_suffix
    di['convert_json_tmp_to_alpaca_file_path'] = args.convert_json_tmp_to_alpaca_file_path

    return parser, args


def main():
    parser, args = parser_register()
    FT = finetune_tools()  # 核心逻辑类
    atexit.register(FT.save)  # 不用管
    if args.exams:
        FT.exam()
    elif args.gen_questions:
        FT.gen_questions()
    elif args.index_file:
        FT.gen_questions_by_index_file()
    elif args.index_folder:
        FT.gen_questions_by_index_folder()
    elif args.convert_json_tmp_to_alpaca_file_path:
        FT.convert_json_tmp_to_alpaca(args.convert_json_tmp_to_alpaca_file_path)
    else:
        loguru.logger.error("Please specify the method to execute.")
