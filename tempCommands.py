import sqlite
import json

cur = sqlite.cur
cur.execute("SELECT * FROM users")
data = cur.fetchall()
print('Количество пользователей: ', len(data))

# print(sqlite.setMailAgreeFalse(879224124))
# print(sqlite.getMailAgree(879224124))
# print(sqlite.setMailAgreeTrue(879224124))
# print(123)
