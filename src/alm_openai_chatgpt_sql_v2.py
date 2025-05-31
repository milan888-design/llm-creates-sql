import pyodbc
import sys 
from datetime import datetime
from openai import OpenAI
from prettytable import PrettyTable
from langchain_openai import ChatOpenAI
from langchain.chains import create_sql_query_chain
from langchain_community.utilities import SQLDatabase
OpenAI.api_key = "sk-YOURKEY"
# Initialize the OpenAI client
#to test using command line
#C:\Users\name\AppData\Local\Programs\Python\Python311\python.exe c:\pyfiles\alm_openai_chatgpt_sql_v2.py topic171 row_id dbconnection tbd 1
#
client = OpenAI()

if __name__ == '__main__':
    arg1 = sys.argv[1]
    arg2 = sys.argv[2]
    arg3 = sys.argv[3]
    arg4 = sys.argv[4]
    arg5 = sys.argv[5]
    #arg0 is the file name, arg1 is guid/row_id, arg2 is row_id or batch_id, arg3-dbconnection arg4 is tbd arg5 is 1 or 2 or 3
    

if arg5=="1":
    sqlpart1="select row_id,spo_llm_model1 as llm_model,spo_prompt1||' '||CASE WHEN spo_prompt1_detail is NULL THEN ' ' ELSE spo_prompt1_detail END as prompt_detail from st_supertriple_v2 where row_id='"

if arg5=="2":
    sqlpart1="select row_id,spo_llm_model2 as llm_model,spo_prompt2||' '||CASE WHEN spo_prompt2_detail is NULL THEN ' ' ELSE spo_prompt2_detail END as prompt_detail from st_supertriple_v2 where row_id='"

if arg5=="3":
    sqlpart1="select row_id,spo_llm_model3 as llm_model,spo_prompt3||' '||CASE WHEN spo_prompt3_detail is NULL THEN ' ' ELSE spo_prompt3_detail END as prompt_detail from st_supertriple_v2 where row_id='"

#open log file
file1log = open('C:/pyfiles/almchatgpt_v2_log.txt', 'a')
file1log.writelines("------"+'\n')
#cnxn = pyodbc.connect('Dsn=ps16alm64;uid=postgres;pwd=Welcome123')
#cnxn2 = pyodbc.connect('Dsn=ps16alm64;uid=postgres;pwd=Welcome123')
cnxn = pyodbc.connect(arg4)
cnxn2 = pyodbc.connect(arg4)
cursor = cnxn.cursor()	
cursor2 = cnxn2.cursor()	
print(arg1)
print(arg2)
print(arg3)
print(arg4)
print(arg5)
file1log.writelines(str(datetime.now())+"-start process for py file-"+arg1+'\n')
file1log.writelines(str(datetime.now())+"-start process for row_id-"+arg2+'\n')
file1log.writelines(str(datetime.now())+"-start process for row_id-"+arg3+'\n')
file1log.writelines(str(datetime.now())+"-start process for row_id-"+arg4+'\n')
file1log.writelines(str(datetime.now())+"-start process for row_id-"+arg5+'\n')
sqlpart2=arg1
sqlpart3="';"
sqlfinal=sqlpart1+sqlpart2+sqlpart3
print(sqlfinal)
file1log.writelines(str(datetime.now())+"-start process for select sql-"+sqlfinal+'\n')
cursor.execute(sqlfinal)

row = cursor.fetchone() 
while row:
    question1 = row.prompt_detail
    print(question1)
    #db = SQLDatabase.from_uri("postgresql://postgres:welcome@localhost:5432/chinook")
    db = SQLDatabase.from_uri(arg3)
    llm = ChatOpenAI(model=row.llm_model, temperature=0)
    chain = create_sql_query_chain(llm, db)
    response = chain.invoke({"question": question1})
    #mylist=db.run(response)
    #sqltext2=response +"---"+mylist
    sqltext2=response
    sqltext2=sqltext2.replace("'","~")
    sqltext2=sqltext2.replace('"','!')
    print(sqltext2)
    file1log.writelines(str(datetime.now())+"-start process for py file-"+sqltext2+'\n')
# Print the table
    #sqltext2=sqltext2.replace("'","#")
    if arg5=="1":
        sqltext1="update st_supertriple_v2 set spo_answer1='"

    if arg5=="2":
        sqltext1="update st_supertriple_v2 set spo_answer2='"

    if arg5=="3":
        sqltext1="update st_supertriple_v2 set spo_answer3='"

    sqltext3="' where row_id='"
    sqltext4=arg1
    sqltext5="';"
    sqltextfinal=sqltext1+sqltext2+sqltext3+sqltext4+sqltext5
    #print(sqltextfinal)
    file1log.writelines(str(datetime.now())+"-start process for update sql-"+sqltextfinal+'\n')
    cursor2.execute(sqltextfinal)
    cnxn2.commit()                
    row = cursor.fetchone()

cursor.close()
cnxn.close()
cursor2.close()
cnxn2.close()

#open log file
file1log.writelines(str(datetime.now())+"-end process for source file-"+arg1+'\n')
file1log.writelines("======"+'\n')
file1log.close()