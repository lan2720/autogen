# from openai_functools import FunctionsOrchestrator
from autogen.retrieve_utils import (
    get_file_from_url, # 从url直接下载pdf文件
    extract_text_from_pdf # 从pdf中提取文字
)
from tools.file_parse import *



# orchestrator = FunctionsOrchestrator()
# # Register all methods of the class
# orchestrator.register_all([get_file_from_url, extract_text_from_pdf])
# orchestrator.register_instance(FileParser())

import os
import json
import autogen

current_dir = os.path.dirname(os.path.realpath(__file__))

functions = autogen.config_list_from_json(
    os.path.join(current_dir, "FUNCTIONS")
    )
# print(json.dumps(functions, indent=4))

function_map = {}
for func in functions:
    func_name = func["name"]
    func_op = eval(func_name)
    function_map[func_name] = func_op
# print(function_map)