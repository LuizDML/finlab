from pathlib import Path
from dotenv import load_dotenv
from guardrails.hub import ProfanityFree
from openai import OpenAI

from guardrails import Guard

# Pra usar as informações do .env
env_path = Path(__file__).resolve().parents[1] / "api" / "config" / ".env"
load_dotenv(env_path)

client = OpenAI(base_url="https://api.groq.com/openai/v1")


def groq_wrapper(*, messages, **kwargs) -> str:
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages,
    )
    return response.choices[0].message.content


guard = Guard().use(ProfanityFree(on_fail="exception"))
query = "FAANG representa quais fucking empresas de tecnologia?"

try:
    guard.validate(query)
except Exception as e:
    print(e)

validated_response = guard(
    groq_wrapper,
    messages=[
        {
            "role": "user",
            "content": query,
        }
    ],
)

print(validated_response.validated_output)