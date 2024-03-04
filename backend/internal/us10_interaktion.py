"""
    This module has the functionality for the multi prompt to choose a template
    according to user input and generates answers.
"""
import os
from deep_translator import GoogleTranslator
from dotenv import find_dotenv, load_dotenv

from langchain.prompts.prompt import PromptTemplate
from langchain.chains.router import MultiPromptChain
from langchain.chains import ConversationChain
from langchain.chains.llm import LLMChain
from langchain.chains.router.llm_router import LLMRouterChain, RouterOutputParser
from langchain.chains.router.multi_prompt_prompt import MULTI_PROMPT_ROUTER_TEMPLATE
from langchain_openai import AzureChatOpenAI

from internal.prompt_template_data import BE_TEMP, SA_TEMP, GE_TEMP, BE_QA_TEMP
from internal.utils import template_concat
from internal.us7_generierung import get_value_from_config


def initial():
    """
    initialize connection to ai

    Raises:
        ValueError: _description_ no key found
        ValueError: _description_ no endpoint found

    Returns:
        _type_: large language model
    """
    load_dotenv(find_dotenv())
    openai_api_key = os.getenv("AZURE_OPENAI_KEY")
    if not openai_api_key:
        raise ValueError("< API Key > nicht gefunden!")
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    if not azure_endpoint:
        raise ValueError("< API Endpoint > nicht gefunden!")
    openai_api_version = os.getenv("AZURE_OPENAI_VERSION")
    chat_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")

    llm = AzureChatOpenAI(
        openai_api_key=openai_api_key,
        openai_api_version=openai_api_version,
        azure_endpoint=azure_endpoint,
        deployment_name=chat_deployment,
        model="gpt-3.5-turbo",
        temperature=0,
    )
    return llm

def __gen_prompt_infos(original_bescheid: str):
    """
    generates the prompts for the multiprompt chain

    Args:
        original_bescheid (str): Beschied to be appended to prompt

    Returns:
        _type_: List of Dictonaries of prompts
    """
    sachverhalt = get_value_from_config(key='sachverhalt')
    prompt_infos = [
            {
                "name": "adjustTemplate",
                "description": "Gut um generierte Bescheide zu bearbeiten und neu herzustellen",
                "prompt_template": template_concat(BE_TEMP, original_bescheid),
            },
            {
                "name": "aboutSachverhalt",
                "description": "Gut um Fragen bezüglich des Sachverhalts zu beantworten.",
                "prompt_template": template_concat(SA_TEMP, sachverhalt),
            },
            {
                "name": "generalQA",
                "description": """Gut um Input zu bearbeiten, der weder mit dem Sachverhalt \
                    noch mit dem generierten Bescheid zu tun haben.""",
                "prompt_template": template_concat(GE_TEMP, get_value_from_config(key='tutorial')),
            },
            {
                "name": "Bescheid_QA",
                "description": "Gut um Fragen zu beantworten, die zum generierten Bescheid sind.",
                "prompt_template": template_concat(BE_QA_TEMP, original_bescheid),
            },
        ]
    return prompt_infos

def multiple_prompt_chain(user_query: str, original_bescheid: str):
    """
    chooses a template and generates answer depending on user input

    Args:
        user_query (str): input from user
        original_bescheid (str): the current valid Bescheid

    Returns:
        str: answer of the ai
    """
    llm = initial()

    prompt_infos = __gen_prompt_infos(original_bescheid)

    destination_chain = {}
    for p_info in prompt_infos:
        prompt = PromptTemplate(template=p_info["prompt_template"], input_variables=["input"])
        chain = LLMChain(llm=llm, prompt=prompt)
        destination_chain[p_info["name"]] = chain

    default_chain = ConversationChain(llm=llm, output_key="text")

    destinations = [f"{p['name']}: {p['description']}" for p in prompt_infos]
    destinations_str = "\n".join(destinations)
    router_template = MULTI_PROMPT_ROUTER_TEMPLATE.format(destinations=destinations_str)
    router_prompt = PromptTemplate(
        template=router_template,
        input_variables=["input"],
        output_parser=RouterOutputParser(),
        validate_template=True,
    )

    router_chain = LLMRouterChain.from_llm(llm, router_prompt)

    chain = MultiPromptChain(
        router_chain=router_chain,
        destination_chains=destination_chain,
        default_chain=default_chain,
        verbose=True,
    )
    translator = GoogleTranslator(source="auto", target="german")
    return translator.translate(chain.run(input=user_query))
