import json

from analyzer_task.models import AnalyzerTask
from decouple import config
from langchain.prompts.prompt import PromptTemplate
from langchain_openai import ChatOpenAI

from .models import Prompt

OPENAI_API_KEY = config('OPENAI_API_KEY')


def create_llm_prompt(analyzer_task_id):
    analyzer_task = AnalyzerTask.objects.get(pk=analyzer_task_id)
    audio_text = analyzer_task.task_text
    hint_to_llm = analyzer_task.helper_instruction
    midjourney_template = f"""
        Given the song text:

        1. Understand this MidJourney Prompt Formula:
           {hint_to_llm}

        2. Based on the song's text {audio_text}, write me MidJourney prompts that use the formula to reflect its essence.

        3. Provide only the resulting prompts where prompt number is a key and prompt text is a value as json, return prompts without quotes and brackets.
    """
    midjourney_prompt_template = PromptTemplate(
        input_variables=["audio_text"],
        template=midjourney_template)
    llm = ChatOpenAI(temperature=0, model_name='gpt-4', api_key=OPENAI_API_KEY)
    chain = midjourney_prompt_template | llm
    result = chain.invoke(input={'audio_text': audio_text})
    json_result_prompt = json.loads(result.content)
    save_prompts(analyzer_task, json_result_prompt)


def save_prompts(analyzer_task, prompts):
    for prompt_content in prompts.values():
        Prompt.objects.create(
            prompt_content=prompt_content,
            task_id=analyzer_task)
