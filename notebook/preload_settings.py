import os
import time
import autogen
current_dir = os.path.dirname(os.path.realpath(__file__))

config_list = autogen.config_list_from_json(
    os.path.join(current_dir, "OAI_CONFIG_LIST"),
    filter_dict={
        "model": ["gpt-4", "gpt-4-32k"],
    },
)


def get_llm_config(trail_id=None, model="gpt-4", functions=[]):
    if trail_id is None:
        trail_id = int(time.time())
    return {
            "request_timeout": 600,
            "seed": trail_id,
            "functions": functions,
            # Excluding azure openai endpoints from the config list.
            # Change to `exclude="openai"` to exclude openai endpoints, or remove the `exclude` argument to include both.
            "config_list": config_list,
            "model": "gpt-4",  # make sure the endpoint you use supports the model
            "temperature": 0
        }