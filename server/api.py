import os
os.environ['http_proxy'] = "http://127.0.0.1:8890"
os.environ['https_proxy'] = "http://127.0.0.1:8890"

from openai import OpenAI

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)


completion=client.chat.completions.create(
     model="gpt-3.5-turbo",
     messages=[
         {"role":"user","content":"你好，请你介绍一下你自己."}
     ]
 )
print(completion.choices[0].message.content)

