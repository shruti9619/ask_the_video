from langchain_openai import ChatOpenAI
from dot_env import load_dotenv

print(load_dotenv())


model = ChatOpenAI(model="gpt-3.5")