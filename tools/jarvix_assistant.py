

from notebook.preload_settings import *
from tools import functions, function_map
from langchain.prompts import (
    PromptTemplate,
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)

def combine_messages(messages):
    content = ""
    for msg in messages:
        content += "\n" + msg.content
    return content

def do_one_task(instruction_prompt, input_prompt, task_params, max_consecutive_auto_reply=5):

    assistant_for_jarvix = autogen.AssistantAgent(
        name="assistant_for_jarvix",
        # system_message="You are a helpful assistant. Reply TERMINATE when the task is done.",
        llm_config=get_llm_config(functions=functions)
    )

    # 我
    jarvix = autogen.UserProxyAgent(
        name="jarvix_proxy",
        human_input_mode="NEVER",#"TERMINATE",
        max_consecutive_auto_reply=max_consecutive_auto_reply,
        code_execution_config={"work_dir": "jarvix_proxy",
                               "use_docker": False},
        function_map=function_map,
    )
    # task3_prompt = """
    # Extract all text from the PDF file located in {pdf_filepath}. If it is in traditional chinese, transfer to simplified chinese string.
    # """
    instruction_template = SystemMessagePromptTemplate.from_template(instruction_prompt)
    input_template = HumanMessagePromptTemplate.from_template(input_prompt)
    chat_prompt = ChatPromptTemplate.from_messages([instruction_template, input_template])
    # task_template = PromptTemplate.from_template(task_prompt)
    # task = chat_prompt.format_prompt(**task_params)
    task = combine_messages(chat_prompt.format_prompt(**task_params).messages)
    print(f"given task: {task}")
    jarvix.initiate_chat(assistant_for_jarvix, message=task)
    jarvix.stop_reply_at_receive(assistant_for_jarvix)
    return jarvix.last_message()["content"]


if __name__ == '__main__':
    system_prompt = """Given a python function, read it overally and fully understand it, then write descriptions for the function and all input parameters, response in bullet items."""
    user_input_prompt = """The python function: {function_code}"""
    # TODO: 运行有bug
    do_one_task(instruction_prompt=system_prompt, 
                input_prompt=user_input_prompt,
                task_params={"function_code": """
def get_file_from_url(url: str, save_path: str = None):
    # Download a file from a URL.
    if save_path is None:
        save_path = os.path.join("/tmp/chromadb", os.path.basename(url))
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(save_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return save_path
                """})