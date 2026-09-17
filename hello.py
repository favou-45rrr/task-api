from dotenv import load_dotenv
import os

load_dotenv()

llm_url = os.getenv("LLM_BASE_URL")
llm_api_key = os.getenv("LLM_API_KEY")
llm_model = os.getenv("LLM_MODEL")

from openai import OpenAI
client = OpenAI(base_url=llm_url, api_key=llm_api_key)

res = client.chat.completions.create(
    model=llm_model,
    messages=[{"role": "user", "content": "Reply with exactly the word: ready"}],
)
print(res.choices[0].message.content)