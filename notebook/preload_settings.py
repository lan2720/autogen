import autogen

config_list = autogen.config_list_from_json(
    "OAI_CONFIG_LIST",
    filter_dict={
        "model": ["gpt-4", "gpt-4-32k"],
    },
)


def get_llm_config(trail_id, model="gpt-4"):
    return {
            "request_timeout": 600,
            "seed": trail_id,
            # Excluding azure openai endpoints from the config list.
            # Change to `exclude="openai"` to exclude openai endpoints, or remove the `exclude` argument to include both.
            "config_list": config_list,
            "model": "gpt-4",  # make sure the endpoint you use supports the model
            "temperature": 0
        }