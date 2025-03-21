from typing import List, Dict
from langchain_core.documents import Document
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# stemming
from nltk.stem import PorterStemmer

nltk.download("punkt")
nltk.download("stopwords")

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough


from setup_configs import get_logger


logger = get_logger()


def preprocess_func(text: str) -> List[str]:
    """
    Preprocess the text

    Args:
        text (str): Input text

    Returns:
        List[str]: Preprocessed text
    """
    # Lowercase the input text
    lowered = text.lower()
    text_tokens = word_tokenize(lowered)
    ps = PorterStemmer()
    stop_words = set(stopwords.words("english"))
    remove_sw = [ps.stem(word) for word in text_tokens if not word in stopwords.words()]
    return remove_sw


def populate_vector_store(docs: list) -> EnsembleRetriever:
    """
    Populate the vector store with the documents

    Args:
        docs (list): List of documents

    Returns:
        EnsembleRetriever: Ensemble retriever
    """
    logger.info("Setting up vector store")

    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vector_store = FAISS.from_texts(
        texts=[doc["text"] for doc in docs],
        embedding=embedding_model,
    )

    bm25_retriever = BM25Retriever.from_texts(
        texts=[doc["text"] for doc in docs], preprocess_func=preprocess_func, k=10
    )
    semantic_retriever = vector_store.as_retriever(search_kwargs={"k": 10})
    ensemble_retriever = EnsembleRetriever(
        retrievers=[bm25_retriever, semantic_retriever], weights=[0.5, 0.5], k=10
    )
    logger.info("vector store setup successful")
    return ensemble_retriever


def format_docs(docs: List[Document]) -> str:
    """
    Format the documents for the prompt

    Args:
        docs (List[Document]): List of documents

    Returns:
        str: Formatted documents
    """
    logger.info(f"Number of retrievals {len(docs)}")
    join_docs = "\n\n".join(doc.page_content for doc in docs)
    logger.info(join_docs)
    return join_docs


def rag_pipeline(retriever, query: str, llm, chat_history: List[Dict] = None) -> str:
    """
    RAG pipeline

    Args:
        retriever: Ensemble retriever
        query (str): User query
        llm: Language model
        chat_history (List[Dict], optional): Chat history. Defaults to None.

    Returns:
        str: Response
    """

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
