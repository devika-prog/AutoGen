import os
from autogen import AssistantAgent, UserProxyAgent
from autogen.coding import DockerCommandLineCodeExecutor

config_list = [
    {
        "model": "llama3",
        "base_url": "http://localhost:11434/v1",
        "api_key" : "NULL",
        "price": [0, 0]
    }
]

#config_list = [{"model": "gpt-4", "api_key": os.environ["OPENAI_API_KEY"]}]

llm_config = {
    "config_list": config_list,
    "timeout": 240,
    "cache_seed": 41,
    #"cache_seed": None,
    "temperature":0
}


# create an AssistantAgent instance named "assistant" with the LLM configuration.
#writes code
assistant = AssistantAgent(name="assistant", llm_config={"config_list": config_list})

# create a UserProxyAgent instance named "user_proxy" with code execution on docker.
#code_executor = DockerCommandLineCodeExecutor()
user_proxy = UserProxyAgent(name="user_proxy",  code_execution_config={
        "work_dir": "coding",
        "use_docker": False,
    })
# the assistant receives a message from the user, which contains the task description
#executes code
user_proxy.initiate_chat(
    assistant,
    #message="""What date is today? Which big tech stock has the largest year-to-date gain this year? How much is the gain?""",
    message = "Write Python code to add two numbers. Save the Python code into a file."
)
