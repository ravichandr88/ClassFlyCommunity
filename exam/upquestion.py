"""
This page accepts excel sheet and prepares the students account for the exam
"""


from pandas import read_excel
import requests

file_name = 'eh_test.xlsx'
my_sheet = 'Sheet1'

df = read_excel(file_name, sheet_name = my_sheet)
print(df.head()) # shows headers
qst = []
p=0
# url='http://localhost:8000/pathques'
url = 'https://www.classfly.in/pathques'
# url = 'https://www.google.co.in'
exam_id = 3 #Exam subject id

for index, row in df.iterrows():
    if (row['question'] == '') or (row['a'] == '') or (row['b'] == '') or (row['c'] == '') or (row['d'] == '') or (row['answer'] == ''):
        print(index, 'something missing')
        continue
    data={'question':row['question'],'answer_a':row['a'],'answer_b':row['b'],'answer_c':row['c'],'answer_d':row['d'],'correct_ans':str(row['answer']).lower(),'exam_sub_id':exam_id}
    resp = requests.post(url,data)

    #  print([ row['name'],row['email'],row['phone']])
    if str(resp.status_code) != '200':
        print(resp.json())
        df.iloc[index,3]=resp.json()['message']
        row['message']=resp.json()['message']
        
# print(df.iloc[1:,:])
df = df.iloc[1:,:]
print(df)


df.to_excel("response.xlsx")