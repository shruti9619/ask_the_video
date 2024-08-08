from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough


from setup_configs import get_logger


logger = get_logger()


def populate_vector_store(docs: list):
    logger.info("Setting up vector store")

    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vector_store = FAISS.from_texts(
        texts=[doc['text'] for doc in docs],
        embedding=embedding_model,
    )
    logger.info("vector store setup successful")
    return vector_store.as_retriever(k = 10)

def format_docs(docs):
    logger.info(f"Number of retrievals {len(docs)}")
    join_docs = "\n\n".join(doc.page_content for doc in docs)
    logger.info(join_docs)
    return join_docs


def rag_pipeline(retriever, query: str, llm, chat_history: List[Dict] = []):
    logger.info("Setting up RAG pipeline")

    custom_prompt = """ You are a youtube assistant who helps answer user questions and user requests 
    by looking at the video transcripts. The user query and transcript would be given below as information to you. 
    If you don't know the answer, say that you don't know. Take content only from the provided context and do not add 
    your own knowledge without the context being present in the transcripts while forming the answers.

    Transcript documents for reference: 
    {transcript_docs}

    Here's the User Query: {query}

    """

    prompt = PromptTemplate.from_template(custom_prompt)
    parser = StrOutputParser()
    chain = (
            {"transcript_docs": retriever | format_docs, "query": RunnablePassthrough()}
            | prompt  
            | llm 
            | parser
            )

    return chain.stream(query)




