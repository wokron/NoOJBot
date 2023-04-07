import os.path

from langchain import PromptTemplate, LLMChain
from langchain.chains import SequentialChain

import prompts


class LLMMetrics:
    def __init__(self, llm, verbose=False):
        pick_related_report_prompt = PromptTemplate(
            input_variables=["class_name", "report_info"],
            template=prompts.LLM_METRICS_PICK,
        )
        pick_related_report_chain = LLMChain(
            llm=llm, prompt=pick_related_report_prompt, output_key="report", verbose=verbose
        )

        analyze_source_code_prompt = PromptTemplate(
            input_variables=["code", "report", "class_name"],
            template=prompts.LLM_METRICS_ANALYZE,
        )
        analyze_source_code_chain = LLMChain(
            llm=llm, prompt=analyze_source_code_prompt, output_key="analyze_output", verbose=verbose
        )

        code_modify_prompt = PromptTemplate(
            input_variables=["code", "analyze_output", "class_name"],
            template=prompts.LLM_METRICS_MODIFY,
        )
        code_modify_chain = LLMChain(
            llm=llm, prompt=code_modify_prompt, output_key="code_modify", verbose=verbose
        )

        self.metrics_chain = SequentialChain(
            chains=[pick_related_report_chain, analyze_source_code_chain, code_modify_chain],
            input_variables=["class_name", "code", "report_info"],
            output_variables=["analyze_output", "report", "code_modify"],
            verbose=verbose,
        )

        summarize_prompt = PromptTemplate(
            input_variables=["metrics_list"],
            template=prompts.LLM_METRICS_SUMMARY,
        )

        self.summarize_chain = LLMChain(llm=llm, prompt=summarize_prompt, verbose=verbose)

    def __call__(self, *args, **kwargs):
        return self.metrics(*args, **kwargs)

    def metrics(self, root_path, metrics_target_set: set = None, metrics_report_path=None, file_suffix=".java"):
        report_info = ""
        if os.path.exists(metrics_report_path):
            with open(metrics_report_path, "r") as f:
                report_info = "\n".join(f.readlines())

        metrics_result_list = {}
        for root, dirs, files in os.walk(root_path):
            for file in files:
                if not file.endswith(file_suffix):
                    continue

                class_name = file.split('.')[0]
                if metrics_target_set is not None and class_name not in metrics_target_set:
                    continue

                source_code_path = os.path.join(root, file)
                with open(source_code_path, "r") as f:
                    source_code = "\n".join(f.readlines())

                print(f"开始评价文件：{file}...")
                metrics_result = self.metrics_chain({
                    "class_name": class_name,
                    "code": source_code,
                    "report_info": report_info,
                })
                print(f"评价{file}完成")

                metrics_result_list[class_name] = (metrics_result["analyze_output"], metrics_result["code_modify"])

        print(f"开始进行总结")
        result_without_modify = {k: v[0] for k, v in metrics_result_list.items()}
        result = self.summarize_chain.run(str(result_without_modify))
        print(f"总结完成")

        return metrics_result_list, result
