from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

print(load_dotenv())

model = ChatOpenAI(model="gpt-3.5-turbo-0125")

print(model.invoke("Hi"))
