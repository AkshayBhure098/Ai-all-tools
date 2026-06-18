# import time
# import logging
# from typing import Dict, Any, List

# from deepeval.metrics import GEval
# from deepeval.test_case import LLMTestCase, LLMTestCaseParams
# from deepeval.models import GPTModel

# logger = logging.getLogger(__name__)

# # -------------------------------
# # Config
# # -------------------------------

# THRESHOLD = 0.5
# DEFAULT_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"
# DEFAULT_BASE_URL = "https://api.groq.com/openai/v1"
# api_key="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"


# # -------------------------------
# # Logging Wrapper
# # -------------------------------

# class LoggingGPTModel(GPTModel):
#     """Logs every prompt + response sent to judge LLM"""

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.call_count = 0

#     def generate(self, prompt, **kwargs):
#         self.call_count += 1
#         logger.info(f"\n{'='*80}")
#         logger.info(f"JUDGE CALL #{self.call_count}")
#         logger.info("PROMPT:")
#         logger.info(prompt)
#         logger.info(f"{'-'*80}")
#         response = super().generate(prompt, **kwargs)
#         logger.info("RESPONSE:")
#         logger.info(response)
#         logger.info(f"{'='*80}\n")
#         return response


# -------------------------------
# Translation Evaluator Class
# -------------------------------
# from deepeval.metrics import GEval, AnswerRelevancyMetric

# class TranslationEvaluator:
#     """
#     Production-ready evaluator using DeepEval GEval metrics.
#     Compatible with Streamlit UI.
#     """

#     def __init__(
#         self,
#         api_key: str = api_key,
#         model: str = DEFAULT_MODEL,
#         base_url: str = DEFAULT_BASE_URL,
#         threshold: float = THRESHOLD,
#         verbose: bool = False,
#     ):
#         self.threshold = threshold
#         self.verbose = verbose

#         self.judge = LoggingGPTModel(
#             model=model,
#             api_key=api_key,
#             base_url=base_url,
#             temperature=0,
#         )

#         self.metrics = self._initialize_metrics()

#     # -------------------------------
#     # Metric Initialization
#     # -------------------------------

#     def _initialize_metrics(self) -> List:
    
#         return [
    
#             GEval(
#                 name="Correctness",
#                 criteria="Is the translation factually accurate and semantically equivalent to the source?",
#                 evaluation_params=[
#                     LLMTestCaseParams.INPUT,
#                     LLMTestCaseParams.ACTUAL_OUTPUT,
#                 ],
#                 threshold=self.threshold,
#                 model=self.judge,
#                 verbose_mode=self.verbose,
#             ),
    
#             GEval(
#                 name="Completeness",
#                 criteria="Does the translation preserve all important information from the source?",
#                 evaluation_params=[
#                     LLMTestCaseParams.INPUT,
#                     LLMTestCaseParams.ACTUAL_OUTPUT,
#                 ],
#                 threshold=self.threshold,
#                 model=self.judge,
#                 verbose_mode=self.verbose,
#             ),
    
#             GEval(
#                 name="Clarity",
#                 criteria="Is the translated text clear, well-structured, and easy to understand?",
#                 evaluation_params=[
#                     LLMTestCaseParams.INPUT,
#                     LLMTestCaseParams.ACTUAL_OUTPUT
#                 ],
#                 threshold=self.threshold,
#                 model=self.judge,
#                 verbose_mode=self.verbose,
#             ),
    
#             AnswerRelevancyMetric(
#                 threshold=self.threshold,
#                 model=self.judge,
#                 include_reason=self.verbose
#             ),
#         ]


#     # -------------------------------
#     # Single Translation Evaluation
#     # -------------------------------
    
#     def evaluate_translation(
#         self,
#         source_text: str,
#         translated_text: str,
#     ) -> Dict[str, Any]:
    
#         test_case = LLMTestCase(
#             input=source_text,
#             actual_output=translated_text,
#         )
    
#         metric_results = []
#         passed_count = 0
    
#         for metric in self.metrics:
    
#             metric_name = getattr(metric, "name", metric.__class__.__name__)
    
#             try:
#                 metric.measure(test_case)
    
#                 score = getattr(metric, "score", 0.0) or 0.0
#                 reason = getattr(metric, "reason", "") or ""
    
#                 is_passed = score >= self.threshold
#                 if is_passed:
#                     passed_count += 1
    
#                 metric_results.append({
#                     "name": metric_name,
#                     "score": round(score, 2),
#                     "passed": is_passed,
#                     "reason": reason,
#                 })
    
#                 time.sleep(2)
    
#             except Exception as e:
#                 logger.exception(f"Metric failure: {metric_name}")
    
#                 metric_results.append({
#                     "name": metric_name,
#                     "score": 0.0,
#                     "passed": False,
#                     "reason": f"Evaluation error: {str(e)}",
#                 })
    
#         total_metrics = len(metric_results)
    
#         overall_score = (
#             sum(m["score"] for m in metric_results) / total_metrics
#             if total_metrics > 0 else 0
#         )
    
#         return {
#             "overall_score": round(overall_score, 2),
#             "passed": passed_count,
#             "failed": total_metrics - passed_count,
#             "metrics": metric_results,
#         }



from typing import List, Dict, Any
from deepeval.test_case import LLMTestCase, LLMTestCaseParams
from deepeval.metrics import GEval, AnswerRelevancyMetric
from deepeval.models import GPTModel


class TranslationEvaluator:

    def __init__(
        self,
        api_key: str,
        judge_model_name: str = "gpt-4o-mini",
        threshold: float = 0.5,
        temperature: float = 0.0,
    ):
        self.threshold = threshold

        self.judge = GPTModel(
            model=judge_model_name,
            api_key=api_key,
            temperature=temperature,
        )

        self.metrics = self._initialize_metrics()

    # -----------------------------------
    # Metric Initialization
    # -----------------------------------

    def _initialize_metrics(self) -> List:

        return [

            AnswerRelevancyMetric(
                threshold=self.threshold,
                model=self.judge,
            ),

            GEval(
                name="Correctness",
                criteria="Is the translation factually accurate and semantically equivalent to the source?",
                evaluation_params=[
                    LLMTestCaseParams.INPUT,
                    LLMTestCaseParams.ACTUAL_OUTPUT,
                ],
                threshold=self.threshold,
                model=self.judge,
            ),

            GEval(
                name="Completeness",
                criteria="Does the translation preserve all important information from the source?",
                evaluation_params=[
                    LLMTestCaseParams.INPUT,
                    LLMTestCaseParams.ACTUAL_OUTPUT,
                ],
                threshold=self.threshold,
                model=self.judge,
                strict_mode=False,
            ),

            GEval(
                name="Clarity",
                criteria="Is the translated text clear, well structured and easy to understand?",
                evaluation_params=[
                    LLMTestCaseParams.INPUT,
                    LLMTestCaseParams.ACTUAL_OUTPUT,
                ],
                threshold=self.threshold,
                model=self.judge,
                strict_mode=False,
            ),
        ]

    # -----------------------------------
    # Evaluation
    # -----------------------------------

    def evaluate_translation(
        self,
        source_text: str,
        translated_text: str,
    ) -> Dict[str, Any]:

        test_case = LLMTestCase(
            input=source_text,
            actual_output=translated_text,
        )

        results = []

        for metric in self.metrics:

            metric_name = getattr(metric, "name", metric.__class__.__name__)

            metric.measure(test_case)

            score = metric.score if metric.score is not None else 0.0

            results.append({
                "metric": metric_name,
                "score": score,
                "passed": metric.is_successful()
                if metric.score is not None
                else False,
                "reason": metric.reason,
            })

        overall_score = (
            sum(r["score"] for r in results) / len(results)
            if results else 0.0
        )

        return {
            "input": source_text,
            "overall_score": round(overall_score, 3),
            "passed_metrics": sum(r["passed"] for r in results),
            "failed_metrics": len(results) - sum(r["passed"] for r in results),
            "metrics": results,
        }
