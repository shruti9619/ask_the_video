import logging

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_huggingface.llms import HuggingFacePipeline
from langchain_core.runnables import RunnablePassthrough

logging.basicConfig()
logger = logging.getLogger(__name__)

def setup_vector_store(docs: list):
    logger.info("Setting up vector store")

    embedding_model = HuggingFaceEmbeddings(
        model_name="BAAI/bge-small-en-v1.5"
    )

    vector_store = FAISS.from_embeddings(
        [doc['text'] for doc in docs],
        embedding_model,
    )

    return vector_store.as_retriever()


def rag_pipeline(retriever, query: str):
    logger.info("Setting up RAG pipeline")
    llm = HuggingFacePipeline.from_model_id(
    model_id ="gpt2", 
    task="text-generation",
    model_kwargs = {'temperature': 1e-5},
    )

    prompt = """ You are a youtube assistant who helps answer user questions and 
    user requests by looking at the video transcripts.

    The user query and transcript would be given below as information to you.

    Transcript documents for reference: {transcript_docs}
    Query: {query}

    """

    prompt = ChatPromptTemplate.from_template("You are a youtube assistant who looks")
    parser = StrOutputParser()
    chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | prompt  
            | llm 
            | parser
            )

    return chain.stream({ query})



