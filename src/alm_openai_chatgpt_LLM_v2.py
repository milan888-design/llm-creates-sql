import pyodbc
import sys 
from datetime import datetime
from openai import OpenAI
from prettytable import PrettyTable
OpenAI.api_key = "sk-YOURKEY"
# Initialize the OpenAI client
#to test using command line
#C:\Users\name\AppData\Local\Programs\Python\Python311\python.exe c:\pyfiles\alm_openai_chatgpt_LLM_v2.py topic171 row_id tbd tbd 1
client = OpenAI()

if __name__ == '__main__':
    arg1 = sys.argv[1]
    arg2 = sys.argv[2]
    arg3 = sys.argv[3]
    arg4 = sys.argv[4]
    arg5 = sys.argv[5]
    #arg0 is the file name, arg1 is guid/row_id, arg2 is row_id or batch_id, arg3-tbd arg4 is tbd arg5 is 1 or 2 or 3
    

if arg5=="1" and arg2=="row_id":
    sqlpart1="select row_id,spo_llm_model1 as llm_model,spo_prompt1||' '||CASE WHEN spo_prompt1_detail is NULL THEN ' ' ELSE spo_prompt1_detail END as prompt_detail from st_supertriple_v2 where row_id='"

if arg5=="2" and arg2=="row_id":
    sqlpart1="select row_id,spo_llm_model2 as llm_model,spo_prompt2||' '||CASE WHEN spo_prompt2_detail is NULL THEN ' ' ELSE spo_prompt2_detail END as prompt_detail from st_supertriple_v2 where row_id='"

if arg5=="3" and arg2=="row_id":
    sqlpart1="select row_id,spo_llm_model3 as llm_model,spo_prompt3||' '||CASE WHEN spo_prompt3_detail is NULL THEN ' ' ELSE spo_prompt3_detail END as prompt_detail from st_supertriple_v2 where row_id='"

#for batch_id
if arg5=="1" and arg2=="batch_id":
    sqlpart1="select row_id,spo_llm_model1 as llm_model,spo_prompt1||' '||CASE WHEN spo_prompt1_detail is NULL THEN ' ' ELSE spo_prompt1_detail END as prompt_detail from st_supertriple_v2 where batch_id='"

if arg5=="2" and arg2=="batch_id":
    sqlpart1="select row_id,spo_llm_model2 as llm_model,spo_prompt2||' '||CASE WHEN spo_prompt2_detail is NULL THEN ' ' ELSE spo_prompt2_detail END as prompt_detail from st_supertriple_v2 where batch_id='"

if arg5=="3" and arg2=="batch_id":
    sqlpart1="select row_id,spo_llm_model3 as llm_model,spo_prompt3||' '||CASE WHEN spo_prompt3_detail is NULL THEN ' ' ELSE spo_prompt3_detail END as prompt_detail from st_supertriple_v2 where batch_id='"


cnxn = pyodbc.connect('Dsn=ps16alm64;uid=postgres;pwd=PASS')
cnxn2 = pyodbc.connect('Dsn=ps16alm64;uid=postgres;pwd=PASS')
cursor = cnxn.cursor()	
cursor2 = cnxn2.cursor()	

sqlpart2=arg1
sqlpart3="';"
sqlfinal=sqlpart1+sqlpart2+sqlpart3
print(sqlfinal)
cursor.execute(sqlfinal)

row = cursor.fetchone() 
while row:
    system_message = {"role": "system", "content": "Your responses should not exceed five sentences in length."}

    user_prompt =row.prompt_detail
    user_model=row.llm_model
    print(user_prompt)
    print(user_model)
    # Add the user's question to the messages as a User Role
    messages = [system_message, {"role": "user", "content": user_prompt}]
    # Generate a completion using the user's question
    completion = client.chat.completions.create(model=user_model,messages=messages)
    #completion = client.chat.completions.create(model="gpt-3.5-turbo",messages=user_prompt)
    # Get the response and print it
    model_response = completion.choices
    #model_response = completion.choices[0].message["content"]

    #print(model_response)
    #print(model_response[0])
    print(model_response[0].message.content)
    sqltext2=model_response[0].message.content
    # Add the response to the messages as an Assistant Role
    #messages.append({"role": "assistant", "content": model_response})
    #messages.append({"content": model_response})

# Print the table
    #sqltext2=sqltext2.replace("'","#")
    sqltext2=sqltext2.replace("'","~")
    sqltext2=sqltext2.replace('"','~')
    if arg5=="1":
        sqltext1="update st_supertriple_v2 set spo_answer1='"

    if arg5=="2":
        sqltext1="update st_supertriple_v2 set spo_answer2='"

    if arg5=="3":
        sqltext1="update st_supertriple_v2 set spo_answer3='"

    sqltext3="' where row_id='"
    sqltext4=row.row_id
    sqltext5="';"
    sqltextfinal=sqltext1+sqltext2+sqltext3+sqltext4+sqltext5
    #print(sqltextfinal)
    cursor2.execute(sqltextfinal)
    cnxn2.commit()                
    row = cursor.fetchone()

    #open log file
    file1log = open('C:/pyfiles/almchatgpt_v2_log.txt', 'a')
    file1log.writelines("------"+'\n')
    file1log.writelines(str(datetime.now())+"-start process for update sql-"+sqltextfinal+'\n')
    file1log.writelines(str(datetime.now())+"-end process for source file-"+arg1+'\n')
    file1log.writelines("======"+'\n')
    file1log.close()


cursor.close()
cnxn.close()
cursor2.close()
cnxn2.close()

#open log file
file1log = open('C:/pyfiles/almchatgpt_v2_log.txt', 'a')
file1log.writelines("------"+'\n')
file1log.writelines(str(datetime.now())+"-start process for py file-"+sqltext2+'\n')
file1log.writelines(str(datetime.now())+"-start process for py file-"+arg1+'\n')
file1log.writelines(str(datetime.now())+"-start process for row_id-"+arg2+'\n')
file1log.writelines(str(datetime.now())+"-start process for row_id-"+arg3+'\n')
file1log.writelines(str(datetime.now())+"-start process for row_id-"+arg4+'\n')
file1log.writelines(str(datetime.now())+"-start process for row_id-"+arg5+'\n')
file1log.writelines(str(datetime.now())+"-start process for select sql-"+sqlfinal+'\n')
file1log.writelines(str(datetime.now())+"-start process for update sql-"+sqltextfinal+'\n')
file1log.writelines(str(datetime.now())+"-end process for source file-"+arg1+'\n')
file1log.writelines("======"+'\n')
file1log.close()
