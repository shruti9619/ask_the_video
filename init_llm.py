import logging
import os


from langchain_huggingface.llms import HuggingFacePipeline
from langchain_openai import AzureChatOpenAI

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


logging.root.setLevel(logging.INFO)
logger = logging.getLogger(__name__)


def init_huggingface_llm():
    
    llm = HuggingFacePipeline.from_model_id(
    model_id ="facebook/blenderbot_small-90M", 
    task = "text-generation",
    model_kwargs = {'temperature': 1e-5, 
                    #'do-sample': True
                    },
    pipeline_kwargs={"max_new_tokens": 200}
    )

    return llm

def init_openai_llm():

    llm = AzureChatOpenAI(
                    deployment_name='gpt-4-turbo',
                    temperature = 0.0001
                )
    return llm



