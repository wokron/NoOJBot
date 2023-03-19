import os

from langchain.llms import OpenAI
from langchain.memory import ConversationBufferWindowMemory
from langchain.agents import initialize_agent

import prompts
from tools import get_tools
from utils import get_source_file_paths


class NoOJBot:
    def __init__(self, root_path, metrics_report_path=None, verbose=False, max_memory=20):
        llm = OpenAI(
            temperature=0.2,
            model_name="gpt-3.5-turbo",
        )

        memory = ConversationBufferWindowMemory(
            memory_key="chat_history",
            output_key="output",
            k=max_memory,
        )

        tools = get_tools(llm, metrics_report_path)

        self.agent = initialize_agent(
            tools, llm,
            agent="conversational-react-description",
            verbose=verbose,
            memory=memory,
            return_intermediate_steps=True,
            agent_kwargs={
                'prefix': prompts.NOOJ_BOT_PREFIX,
                'format_instructions': prompts.NOOJ_BOT_FORMAT_INSTRUCTIONS,
                'suffix': prompts.NOOJ_BOT_SUFFIX.replace("{path_list}", get_source_file_paths(root_path)),
            },
        )

    def __call__(self, input_str):
        result = self.agent({"input": input_str})
        return result["output"]
