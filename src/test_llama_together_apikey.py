from together import Together
import os
#worked on 12may25
os.environ['TOGETHER_API_KEY'] = 'YOURKEY'
client = Together()

response = client.chat.completions.create(
    model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
    messages=[{"role": "user", "content": "What are some fun things to do in New York?"}],
)
print(response.choices[0].message.content)