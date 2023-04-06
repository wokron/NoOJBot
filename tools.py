import os

from langchain import PromptTemplate, LLMChain
from langchain.agents import tool, Tool

import prompts


class MetricsProject:
    def __init__(self, metrics_report_path):
        if metrics_report_path is None:
            self.project_metrics_report = ""
        else:
            with open(metrics_report_path, "r") as f:
                self.project_metrics_report = "\n".join(f.readlines())

    def __call__(self, inputs: str) -> str:
        return self.project_metrics_report


@tool("ReadFile")
def read_file(code_file_path):
    """
    useful when you want get the content of the file.
    because of token limitations, you can not use this tool for one file more than one time.
    the input is the path to the source code file. You must enter a real file path.
    the output is all the contents of the file.
    """
    try:
        with open(code_file_path, "r") as f:
            return f.readlines()
    except IOError:
        return (
            "source code file not found, "
            "you should use tool ProjectStructure to get the correct path before you use this one"
        )


class MetricsClass:
    def __init__(self, llm):
        prompt = PromptTemplate(
            input_variables=["code"],
            template=prompts.METRICS_CLASS_TEMPLATE
        )
        self.chain = LLMChain(llm=llm, prompt=prompt)

    def __call__(self, code_file_path):
        metrics_result = self.chain.run(read_file(code_file_path))
        return metrics_result


class Modify:
    def __init__(self, llm):
        prompt = PromptTemplate(
            input_variables=["code", "instruction"],
            template=prompts.MODIFY_CODE_TEMPLATE
        )
        self.chain = LLMChain(llm=llm, prompt=prompt)

    def __call__(self, inputs):
        split_inputs = inputs.split(',')
        if len(split_inputs) != 2:
            return "invalid input, The input to this tool should be a COMMA separated string of two"

        code_file_path, instruction = split_inputs

        modify_result = self.chain.run(
            code=read_file(code_file_path),
            instruction=instruction
        )

        return modify_result


def get_tools(llm, metrics_report_path):
    return [
        Tool("MetricsProject", MetricsProject(metrics_report_path), prompts.METRICS_PROJECT_DESC),
        Tool("ReadFile", read_file, prompts.READ_FILE_DESC),
        Tool("MetricsClass", MetricsClass(llm), prompts.METRICS_CLASS_DESC),
        Tool("Modify", Modify(llm), prompts.MODIFY_DESC),
    ]
