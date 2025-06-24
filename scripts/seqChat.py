import os
import autogen
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
    "timeout": 120,
    "cache_seed": 41,
    #"cache_seed": None,
    "temperature":0
}

# Start logging to a SQLite database
logging_session_id = autogen.runtime_logging.start(config={"dbname": "logs.db"})
print("Logging session ID: " + str(logging_session_id))

financial_tasks = [
    """What are the current stock prices of NVDA and TESLA, and how is the performance over the past month in terms of percentage change?""",
    """Investigate possible reasons of the stock performance leveraging market news.""",
]

writing_tasks = ["""Develop an engaging blog post using any information provided."""]

financial_assistant = autogen.AssistantAgent(
    name="Financial_assistant",
    llm_config=llm_config,
)
research_assistant = autogen.AssistantAgent(
    name="Researcher",
    llm_config=llm_config,
)
writer = autogen.AssistantAgent(
    name="writer",
    llm_config=llm_config,
    system_message="""
        You are a professional writer, known for
        your insightful and engaging articles.
        You transform complex concepts into compelling narratives.
        Reply "TERMINATE" in the end when everything is done.
        """,
)
#run generated code without asking for human input: human-in-the-loop (HITL)
user_proxy_auto = autogen.UserProxyAgent(
    name="User_Proxy_Auto",
    human_input_mode="NEVER",
    is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={
        "last_n_messages": 1,
        "work_dir": "tasks",
        "use_docker": False,
    },  # Please set use_docker=True if docker is available to run the generated code. Using docker is safer than running the generated code directly.
)

user_proxy = autogen.UserProxyAgent(
    name="User_Proxy",
    human_input_mode="ALWAYS",  # ask human for input at each step
    is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={
        "last_n_messages": 1,
        "work_dir": "tasks",
        "use_docker": False,
    },  # Please set use_docker=True if docker is available to run the generated code. Using docker is safer than running the generated code directly.
)


chat_results = autogen.initiate_chats(
    [
        {
            "sender": user_proxy_auto,
            "recipient": financial_assistant,
            "message": financial_tasks[0],
            "clear_history": True,
            "silent": False,
            "summary_method": "last_msg",
        },
        {
            "sender": user_proxy_auto,
            "recipient": research_assistant,
            "message": financial_tasks[1],
            "max_turns": 2,  # max number of turns for the conversation (added for demo purposes, generally not necessarily needed)
            "summary_method": "reflection_with_llm",
        },
        {
            "sender": user_proxy,
            "recipient": writer,
            "message": writing_tasks[0],
            "carryover": "I want to include a figure or a table of data in the blogpost.",  # additional carryover to include to the conversation (added for demo purposes, generally not necessarily needed)
        },
    ]
)

# Stop logging
autogen.runtime_logging.stop()