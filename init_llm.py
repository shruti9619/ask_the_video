import logging

from dotenv import load_dotenv

from langchain_huggingface.llms import HuggingFacePipeline
from langchain_openai import AzureChatOpenAI


logging.root.setLevel(logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

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

    os.environ["AZURE_OPENAI_ENDPOINT"] = os.getenv("AZURE_OPENAI_ENDPOINT_USEAST")
    os.environ["AZURE_OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY_USEAST")
    os.environ["OPENAI_API_TYPE"] = os.getenv("OPENAI_API_TYPE")
    os.environ["OPENAI_API_VERSION"] = os.getenv("OPENAI_API_VERSION")

     llm = AzureChatOpenAI(
                    deployment_name='gpt-4-turbo',
                    temperature = 0.0001
                )
    return llm

    

