import argparse
import atexit

import loguru
from kink import di


def parser_register():
    """
    Register the parsers
    :return:
    """
    parser = argparse.ArgumentParser(
        description='fine-tuning tools by stupidfish.',
        epilog='''
Example:
    %(prog)s --index_folder rss-picker --system_prompt "你是一名网络安全领域的出题专家，你需要根据给你的知识库来出题，确保后者可以通过做题来完全吸收知识库里的知识，如果提供的是广告等非纯技术类的干货，那么可以不返回问题" 
    %(prog)s --exams --input_parquet_file example.parquet
        ''',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

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

    parser.add_argument(
        '--openai_api_key',
        type=str,
        default='',
        help="OpenAI API key for accessing OpenAI services."
    )

    parser.add_argument(
        '--openai_api_endpoint',
        type=str,
        default='http://gpus.dev.cyberspike.top:8000/v1',
        help="OpenAI API endpoint for accessing OpenAI services."
    )
    parser.add_argument(
        '--default_model',
        type=str,
        default='QwQ-32B',
        help="Default model for OpenAI API."
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
    di['openai_api_key'] = args.openai_api_key
    di['openai_api_endpoint'] = args.openai_api_endpoint
    di['default_model'] = args.default_model

    return parser, args


def main():
    parser, args = parser_register()
    from finetune.parquet.fine_tuning.tools import finetune_tools  # 要在依赖注入的下面，否则会报错
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
