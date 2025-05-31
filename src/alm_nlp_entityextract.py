import pyodbc
import sys 
import spacy
from datetime import datetime
import en_core_web_sm
from spacy import displacy
#from rdflib import Graph, Literal, Namespace, RDF, URIRef
nlp = en_core_web_sm.load()

cnxn = pyodbc.connect('Dsn=ps16alm64;uid=postgres;pwd=PASS')
cnxn2 = pyodbc.connect('Dsn=ps16alm64;uid=postgres;pwd=PASS')
cursor = cnxn.cursor()	
cursor2 = cnxn2.cursor()	


if __name__ == '__main__':
    arg1 = sys.argv[1]
    arg2 = sys.argv[2]
    arg3 = sys.argv[3]
    #print(f'The value of arg1 is {arg1} and the value of arg2 is {arg2}.')

#sqlpart1="select row_id,spo_text from st_supertriple_v2 where row_id='"
if arg2=="row_id":
    sqlpart1="select row_id,model1_subject_attr_value,spo_text from st_supertriple_v2 where row_id='"

if arg2=="batch_id":
    sqlpart1="select row_id,model1_subject_attr_value,spo_text from st_supertriple_v2 where row_id='"

sqlpart2=arg1
sqlpart3="';"
sqlfinal=sqlpart1+sqlpart2+sqlpart3
cursor.execute(sqlfinal)

row = cursor.fetchone() 
while row:
    content = row.spo_text   
    statements = content.split ('.') 
    #content = "Men loves dog"
    # Split the content into statements
    #statements = content.split ('.')
    #print(statements)
    for statement in statements:
        if statement.strip ():
        # Parse the statement using spaCy
            doc2 = nlp (statement)
            for token in doc2:
            #print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_, token.shape_, token.is_alpha, token.is_stop)
                if token.dep_=="nsubj":
                    subject=token.text
                elif token.dep_=="ROOT":
                    predicate=token.text
                elif token.dep_=="dobj":
                    object=token.text      
            # Create RDF triples
            #triples.append ((subject, predicate, object))
            print("subject:"+subject+"  predicate:"+predicate+"  object:"+object)
            sqltext2="subject:"+subject+"  predicate:"+predicate+"  object:"+object+'\n'
            #triples.append ((subject, predicate, object))
            for ent in doc2.ents:
                #print(ent.text, ent.start_char, ent.end_char, ent.label_)
                print(ent.text+'#'+ ent.label_+'\n')
                sqltext2=sqltext2+ent.text+'#'+ ent.label_+'\n'
    sqltext1="update st_supertriple_v2 set spo_text_out='"
    #sqltext2="subject:"+subject+"  predicate:"+predicate+"  object:"+object
    sqltext3="' where row_id='"
    sqltext4=arg1
    sqltext5="';"
    sqltextfinal=sqltext1+sqltext2+sqltext3+sqltext4+sqltext5
    #print(sqltextfinal)
    cursor2.execute(sqltextfinal)
    cnxn2.commit()                
    row = cursor.fetchone()

cursor.close()
cnxn.close()
cursor2.close()
cnxn2.close()

#open log file
file1log = open('C:/pyfiles/almnlp_log.txt', 'a')
file1log.writelines("------"+'\n')
file1log.writelines(str(datetime.now())+"-start process for py file-"+arg1+'\n')
file1log.writelines(str(datetime.now())+"-start process for row_id-"+arg2+'\n')
file1log.writelines(str(datetime.now())+"-start process for select sql-"+sqlfinal+'\n')
file1log.writelines(str(datetime.now())+"-start process for update sql-"+sqltextfinal+'\n')
file1log.writelines(str(datetime.now())+"-end process for source file-"+arg1+'\n')
file1log.writelines("======"+'\n')
file1log.close()