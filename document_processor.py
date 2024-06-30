import logging

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_huggingface.llms import HuggingFacePipeline
from langchain_core.runnables import RunnablePassthrough

logging.root.setLevel(logging.INFO)
logger = logging.getLogger(__name__)

def setup_vector_store(docs: list):
    logger.info("Setting up vector store")

    embedding_model = HuggingFaceEmbeddings(
        model_name="BAAI/bge-small-en-v1.5"
    )

    vector_store = FAISS.from_texts(
        texts=[doc['text'] for doc in docs],
        embedding=embedding_model,
    )

    return vector_store.as_retriever()

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def rag_pipeline(retriever, query: str):
    logger.info("Setting up RAG pipeline")
    llm = HuggingFacePipeline.from_model_id(
    model_id ="gpt2", 
    task="text-generation",
    model_kwargs = {'temperature': 1e-5},
    )

    custom_prompt = """ You are a youtube assistant who helps answer user questions and 
    user requests by looking at the video transcripts.

    The user query and transcript would be given below as information to you.
    If you don't know the answer, say that you don't know. 
    Use three sentences maximum and keep the answer concise.

    Transcript documents for reference: {transcript_docs}
    Query: {query}

    """

    prompt = PromptTemplate.from_template(custom_prompt)
    parser = StrOutputParser()
    chain = (
            {"transcript_docs": retriever | format_docs, "query": RunnablePassthrough()}
            | prompt  
            # | llm 
            # | parser
            )

    return chain.stream({ query})




