import logging
from langchain_huggingface.llms import HuggingFacePipeline


logging.root.setLevel(logging.INFO)
logger = logging.getLogger(__name__)

def init_huggingface_llm():
    
    llm = HuggingFacePipeline.from_model_id(
    model_id ="numind/NuExtract-tiny", 
    task = "text-generation",
    model_kwargs = {'temperature': 1e-5, 
                    #'do-sample': True
                    },
    pipeline_kwargs={"max_new_tokens": 200}
    )

    return llm