from openai import OpenAI
from langchain_openai import ChatOpenAI
from langchain.chains import create_sql_query_chain
from langchain_community.utilities import SQLDatabase
OpenAI.api_key = "YOURKEY"
# Initialize the OpenAI client
client = OpenAI()
dbconnection='postgresql://postgres:pass@localhost:5432/chinook'
question1 = 'List invoices and customer names for customers living in Brazil'
db = SQLDatabase.from_uri(dbconnection)
llm = ChatOpenAI(model='gpt-3.5-turbo', temperature=0)
chain = create_sql_query_chain(llm, db)
response = chain.invoke({"question": question1})
result1=db.run(response)
sqlandresult=response +"---"+result1
print(sqlandresult)
   