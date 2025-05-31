import os
from langchain_together import ChatTogether
from together import Together
#worked on 12may25s
os.environ['TOGETHER_API_KEY'] = 'YOURKEY'
client = Together()

llm = ChatTogether(
    model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
    temperature=0,
)
from langchain_community.utilities import SQLDatabase

# Note: to run in Colab, you need to upload the nba_roster.db file in the repo to the Colab folder first.
#db = SQLDatabase.from_uri("sqlite:///nba_roster.db", sample_rows_in_table_info=0)
db = SQLDatabase.from_uri("postgresql://postgres:PASS@localhost:5432/chinook", sample_rows_in_table_info=0)
def get_schema():
    return db.get_table_info()
#question = "What team is Stephen Curry on?"
question = "how many employees are there?"
prompt = f"""Based on the table schema below, write a SQL query that would answer the user's question; just return the SQL query and nothing else.

Scheme:
{get_schema()}

Question: {question}

SQL Query:"""

print(prompt)
answer = llm.invoke(prompt).content
print(answer)
# note this is a dangerous operation and for demo purpose only; in production app you'll need to safe-guard any DB operation
#result = db.run(answer)
#result