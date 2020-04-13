import numpy as np
import pandas as pd
from datetime import datetime

#
# account = pd.read_csv('./data/account.csv')
# account['date'] = pd.to_datetime(account['date'], format = '%y%m%d')
# account.to_csv('./transData/account.csv')

# client = pd.read_csv('./data/client.csv')
# dates = list(client['birth_number'])
# length = len(dates)
#
# gender = []
# age = []
# for i in range(length):
#     birth = str(dates[i])
#     g = 'M'
#     month = birth[2:4]
#     #year = int(birth[:2])
#     ### if the client is female
#     if int(month) > 50:
#         g = 'F'
#         month = str(int(month) - 50)
#         month = month.zfill(2)
#     # print(birth)
#     #year = str(year + 21)
#     #str.zfill(year, 2)
#     birth = "".join((birth[:2], month, birth[4:]))
#     birth = '19'+birth
#     date = datetime.strptime(birth, '%Y%m%d').date()
#     #date = date.year + 21
#     age.append(1999 - date.year)
#     #print(date)
#     dates[i] = date
#     gender.append(g)
#     #print(age)
# client['birth_number'] = dates
#
# client['gender'] = gender
# client['age'] = age
# print(client)
# client.to_csv('./transData/client.csv')


loan = pd.read_csv('./transData/loan.csv')
# account.drop(index = True)
print(loan['account_id'].is_unique)
## loan['date'] = pd.to_datetime(loan['date'], format='%y%m%d')
# account.to_csv('./transData/account.csv', index = False)
trans = pd.read_csv('./transData/transaction.csv')
