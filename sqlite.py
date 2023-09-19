import sqlite3
from pathlib import Path
import threading

# Объявление "замка"
lock = threading.Lock()

dataBasePath = Path('DataBase', 'user.id.db')

# Инициализация БД
try:
  conn = sqlite3.connect(dataBasePath, check_same_thread=False)
  cur = conn.cursor()
  cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
    userid INT,
    fname TEXT,
    status INT,
    lMessageCode TEXT,
    weeklyData TEXT,
    aimCode TEXT,
    mailAgree TEXT
    );
        """)
  conn.commit()
except:
  print('Ошибка при инициализации БД')


# Добавить нового пользователя в БД
def addUser(userID, userName):
  try:
    with lock:
      cur.execute("INSERT INTO users VALUES(?, ?, ?, ?, ?, ?, ?);", (
        userID, userName, 0, '', "0", '0',
        "True"))  #в случае отсутствия пользователя в базе данных добавляет его
      conn.commit()
  except:
    return print('Ошибка при добавлении нового пользователя в БД')


# Проверка на существование пользователя
def checkUser(userID, userName):
  try:
    fndStroke = getUserStatus(userID)
    if (fndStroke == None):
      addUser(userID, userName)
    return 1
  except:
    return print('Ошибка при проверке на существование пользователя')


# Достать статус из БД по ID пользователя
def getUserStatus(userID):
  try:
    with lock:
      cur.execute("""SELECT status FROM users WHERE userid = ?""", (userID, ))
      fndStroke = cur.fetchone()
      conn.commit()
      if (fndStroke):
        fndStroke = fndStroke[0]
    return fndStroke
  except:
    return print('Ошибка при поиске статуса в БД')


# Установка статуса пользователю
def setStatus(userID, status):
  try:
    with lock:
      cur.execute("""UPDATE users SET status = ? WHERE userid = ?""",
                  (status, userID))
      conn.commit()
    return 1
  except:
    return print('Ошибка при установке статуса пользователя в БД')


# Очистка статуса пользователя
def clearStatus(userID):
  try:
    with lock:
      cur.execute("""UPDATE users SET status = ? WHERE userid = ?""",
                  (0, userID))
      conn.commit()
    return 1
  except:
    return print('Ошибка при очистке статуса пользователя в БД')


# Достать Код Цели из БД по ID пользователя
def getAimCode(userID):
  try:
    with lock:
      cur.execute("SELECT aimCode FROM users WHERE userid = ?", (userID, ))
      aimCode = cur.fetchone()
      conn.commit()
    return aimCode[0]
  except:
    return print('Ошибка при поиске Кода Цели в БД')


# Установка NC Кода Цели
def setNCAimCode(userID):
  try:
    with lock:
      cur.execute("UPDATE users SET aimCode = ? WHERE userid = ?",
                  ("NC", userID))
      conn.commit()
    return 1
  except:
    return print('Ошибка при установка NC кода')


# Установка  Кода Цели
def setAimCode(userID, aimCode):
  try:
    with lock:
      cur.execute("UPDATE users SET aimCode = ? WHERE userid = ?",
                  (aimCode, userID))
      conn.commit()
    return 1
  except:
    return print('Ошибка при установка Кода Цели')


# Получение кода последнего сообщения из БД
def getLMessageCode(userID):
  try:
    with lock:
      cur.execute("SELECT lMessageCode FROM users WHERE userid = ?",
                  (userID, ))
      lMessageCode = cur.fetchone()[0]
      conn.commit()
    return int(lMessageCode)
  except:
    return print('Ошибка при получении кода последнего сообщения')


# Установка кода последнего сообщения
def setLMessageCode(userID, lMessageCode):
  try:
    with lock:
      cur.execute("UPDATE users SET lMessageCode = ? WHERE userid = ?",
                  (lMessageCode, userID))
      conn.commit()
    return 1
  except:
    return print('Ошибка при установке кода последнего сообщения')


# Достать множество ID пользователей
def getAllUserIDs():
  #try:
  with lock:
    ids = set()
    cur.execute("SELECT userid FROM users WHERE mailAgree = ?", ("True", ))
    found = cur.fetchall()
    for i in found:
      ids.add(int(i[0]))
    conn.commit()
  return list(ids)


#except:
#return print('Ошибка при получении всех ID пользователей с TRUE рассылкой')


# Достать weeklyData
def getWeeklyData(userID):
  try:
    with lock:
      cur.execute("SELECT weeklyData FROM users WHERE userid = ?", (userID, ))
      weeklyData = cur.fetchone()[0]
      conn.commit()
    return weeklyData
  except:
    return print('Ошибка при получении кода последнего сообщения')


# Установка weeklyData
def setWeeklyData(userID, weeklyData):
  try:
    with lock:
      cur.execute("UPDATE users SET weeklyData = ? WHERE userid = ?",
                  (weeklyData, userID))
      conn.commit()
    return 1
  except:
    return print('Ошибка при установке кода последнего сообщения')


# Достать mailAgree
def getMailAgree(userID):
  try:
    cur.execute("SELECT mailAgree FROM users WHERE userid = ?", (userID, ))
    found = cur.fetchone()
    return found[0] if found else print('Код рассылки не установлен')
  except:
    return print('Ошибка при получении кода рассылки')


# Разрешить рассылку
def setMailAgreeTrue(userID):
  try:
    cur.execute("UPDATE users SET mailAgree = ? WHERE userid = ?",
                ("True", userID))
  except:
    return print('Ошибка при резрешении рассылки')


# Запретить рассылку
def setMailAgreeFalse(userID):
  try:
    cur.execute("UPDATE users SET mailAgree = ? WHERE userid = ?",
                ("False", userID))
  except:
    return print('Ошибка при запрете рассылки')


# 0 -> Главное меню
# 1(000) -> Узнать ответы (Номер задания)
# 2(000) -> Показать случайное задание
# 3 000 -> Сгенерировать случайный вариант
#   001 -> Анкета варианта
#   002 -> Подтверждение сохранения результатов анкеты
#   003 -> Сохранение разультатов анкеты
# 4 000 -> Цели
#   001 -> Очистка целей
#   002 -> Подтверждение очистки целей
#   003 -> Моя неделя
#   004 -> Установка количества вариантов в неделю
#   005 -> Успешная установка количества вариантов
#
#   009 -> 0 Аим Код
# 5 000 -> Полезные ссылки
#   001 -> Получить файлы

# 9 000 -> Admin Panel
#   001 -> Глобальная рассылка
