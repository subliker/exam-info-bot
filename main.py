if (__name__ != '__main__'):
  exit()

import config
import telebot
import linkGenerating
import sqlite
import defaultBtns
import adminManager
from modules import *
from background import keep_alive

# Подключение к боту
bot = telebot.TeleBot(config.token)


# Действия на комманду "/start"
@bot.message_handler(commands=['start'])
def welcome(message):
  userID = message.from_user.id
  userName = message.from_user.id
  sqlite.checkUser(userID, userName)
  if (userID in currentData().usersInfo):
    aimCurrentSessionDump = currentData().usersInfo.pop(userID)
  sqlite.clearStatus(userID)
  if userID in adminManager.getAdminUserIDs():
    rm = defaultBtns.kStartAdmin()
  else:
    rm = defaultBtns.kStart()
  rm.add(mainMenu().getMailAgreeBtn(sqlite.getMailAgree(userID)))
  msg = bot.send_message(userID,
                         mainMenu().getWelcomeText(),
                         parse_mode='html',
                         reply_markup=rm)
  sqlite.setLMessageCode(userID, msg.message_id)


# Обработчик событий
@bot.callback_query_handler(func=lambda Call: True)
def callAnswer(call):
  userID = call.from_user.id
  userName = call.from_user.first_name
  status = sqlite.getUserStatus(userID)
  sqlite.checkUser(userID, userName)
  if (call.data == 'mainMenu'):  #'Главное меню'
    if (userID in currentData().usersInfo):
      currentSessionDump = currentData().usersInfo.pop(userID)
    sqlite.clearStatus(userID)
    if userID in adminManager.getAdminUserIDs():
      rm = defaultBtns.kStartAdmin()
    else:
      rm = defaultBtns.kStart()
    rm.add(mainMenu().getMailAgreeBtn(sqlite.getMailAgree(userID)))
    msg = bot.send_message(userID,
                           mainMenu().getWelcomeText(),
                           parse_mode='html',
                           reply_markup=rm)
    sqlite.setLMessageCode(userID, msg.message_id)
  elif (call.data == 'showAnswer'):  #'Узнать ответы'
    sqlite.setStatus(userID, status=1000)
    msg = bot.send_message(userID,
                           showAnswer().getChooseTopicText(),
                           reply_markup=defaultBtns.kShowAnswer(),
                           parse_mode='html')
    sqlite.setLMessageCode(userID, msg.message_id)
  elif (call.data[:2] == 'ap'):
    apTask = int(call.data[2:])
    if status == 1000:
      bot.delete_message(userID, sqlite.getLMessageCode(userID))
    sqlite.setStatus(userID, status=apTask + 1000)
    bot.send_message(userID,
                     showAnswer().getChooseTaskText(apTask),
                     parse_mode='html')
  elif (call.data == 'showRandomTask'):  #'Показать случайное задание'
    sqlite.setStatus(userID, status=2000)
    msg = bot.send_message(userID,
                           randomTask().getChooseTopicText(),
                           reply_markup=defaultBtns.kShowRandomTask(),
                           parse_mode='html')
    sqlite.setLMessageCode(userID, msg.message_id)
  elif (call.data[:2] == 'nt'):
    ntTask = int(call.data[2:])
    currentData().usersInfo[userID] = ntTask
    link = linkGenerating.getGeneratedLinkPolyakovByTasks(ntTask)
    if status == 2000:
      bot.delete_message(userID, sqlite.getLMessageCode(userID))
    msg = bot.send_message(call.from_user.id,
                           randomTask().getChooseTaskText(ntTask),
                           parse_mode='html',
                           reply_markup=randomTask().getAnswerBtns(link)())
    sqlite.setStatus(userID, status=ntTask + 2000)
    sqlite.setLMessageCode(userID, lMessageCode=msg.message_id)
  elif (call.data == 'genVar'):  #'Сгенерировать случайный вариант' 3000
    sqlite.setStatus(userID, status=3000)
    bot.send_message(
      userID,
      genVar().getMainText(),
      reply_markup=genVar().getAnswerBtns(
        linkGenerating.getGeneratedLinkPolyakovByTasks('27all'))(),
      parse_mode='html')
  elif (call.data == 'checkVar'):  # Анкета варианта 3001
    userInfo = []
    if (userID in currentData().usersInfo):
      userInfo = currentData().usersInfo.pop(userID)
    if (sqlite.getUserStatus(userID) == 3002):
      currentData().usersInfo[userID] = userInfo
      bot.delete_message(userID, sqlite.getLMessageCode(userID))
    msg = bot.send_message(
      chat_id=userID,
      text=checkVar().getMainText(),
      reply_markup=checkVar().getCheckVarButtons(userInfo)(),
      parse_mode='html')
    sqlite.setStatus(userID, 3001)
    sqlite.setLMessageCode(userID, lMessageCode=msg.message_id)
  elif (call.data[:2] == 'cv'
        and call.data != 'cvDone'):  # Кнопки в Анкете варианта
    if sqlite.getUserStatus(userID) == 3001:
      cvTask = int(call.data[2:])  #фиксирование заданий
      if (userID in currentData().usersInfo):
        userInfo = currentData().usersInfo[userID]
      else:
        userInfo = [0] * 27
      userInfo[cvTask - 1] = int(not (userInfo[cvTask - 1]))
      currentData().usersInfo[userID] = userInfo
      bot.edit_message_reply_markup(
        chat_id=userID,
        message_id=sqlite.getLMessageCode(userID),
        reply_markup=checkVar().getCheckVarButtons(userInfo)())
  elif (call.data == 'cvDone'
        ):  # Подтверждение сохранения результатов анкеты 3002
    if (sqlite.getUserStatus(userID) == 3001):
      usersInfo = currentData().usersInfo
      checkVarMsg = sqlite.getLMessageCode(userID)
      msg = bot.edit_message_text(chat_id=userID,
                                  message_id=checkVarMsg,
                                  text=checkVar().getSureText(
                                    userID, userID in usersInfo, usersInfo),
                                  reply_markup=defaultBtns.kСheckVarSureBtns(),
                                  parse_mode='html')
      sqlite.setStatus(userID, 3002)
      sqlite.setLMessageCode(userID, lMessageCode=msg.message_id)
    else:
      bot.send_message(chat_id=userID,
                       text=errors().getSGWText(),
                       parse_mode='html',
                       reply_markup=defaultBtns.exBtn())
  elif (call.data == 'saveCheckVar'):  # Сохранение разультатов анкеты 3003
    msg = 0
    if (sqlite.getUserStatus(userID) != 3002):
      bot.send_message(userID,
                       errors().getSGWText(),
                       parse_mode='html',
                       reply_markup=defaultBtns.exBtn())
    else:
      userInfo = currentData().usersInfo.pop(userID)
      aimCode = checkVar().prepareAimCode(sqlite.getAimCode(userID), userInfo)
      sqlite.setAimCode(userID, aimCode)
      weeklyData = sqlite.getWeeklyData(userID)
      sqlite.setWeeklyData(userID, myWeek().addCompVar(weeklyData))
      msg = bot.edit_message_text(chat_id=userID,
                                  message_id=sqlite.getLMessageCode(userID),
                                  text=checkVar().getSaveText(userInfo),
                                  parse_mode='html',
                                  reply_markup=defaultBtns.exBtn())
    sqlite.setStatus(userID, 3003)
    if (msg):
      sqlite.setLMessageCode(userID, lMessageCode=msg.message_id)
  elif (call.data == 'checkTask'):  # Добавление задания в Цели
    if (userID in currentData().usersInfo):
      currentTask = int(currentData().usersInfo.pop(userID))
      link = linkGenerating.getGeneratedLinkPolyakovByTasks(currentTask)
      sqlite.setAimCode(
        userID,
        aim().addTaskToAimCode(sqlite.getAimCode(userID), currentTask))
      bot.edit_message_reply_markup(reply_markup=randomTask().getAnswerBtns(
        link, isChecked=True)(),
                                    chat_id=userID,
                                    message_id=sqlite.getLMessageCode(userID))
  elif (call.data == 'aim'):
    aimCode = sqlite.getAimCode(userID)
    weeklyData = sqlite.getWeeklyData(userID)
    if myWeek().isOldWeekData(weeklyData):
      weeklyData = myWeek().clearOldWeekData(weeklyData)
      sqlite.setWeeklyData(userID, weeklyData)
    if (status == 4009):
      sqlite.setNCAimCode(userID)
      aimCode = 'NC'
    if (aimCode == '0'):
      msg = bot.send_message(userID,
                             aim().getWelcomeText(),
                             parse_mode='html',
                             reply_markup=defaultBtns.kAimWelcomeBtns())
      sqlite.setStatus(userID, 4009)
    else:
      if (status in [4000, 4001, 4002, 4003]):
        bot.delete_message(userID, sqlite.getLMessageCode(userID))
      graphPic, graphName = aim().getGraph(aimCode, userID)
      msg = bot.send_photo(caption=aim().getMainText(aimCode, weeklyData),
                           chat_id=userID,
                           photo=graphPic,
                           reply_markup=defaultBtns.kAimBtns(),
                           parse_mode='html')
      aim().clearTempGraph(graphName)
      sqlite.setStatus(userID, 4000)
    sqlite.setLMessageCode(userID, msg.message_id)
  elif (call.data == 'clearAim'):
    msg = bot.delete_message(userID, sqlite.getLMessageCode(userID))
    msg = bot.send_message(chat_id=userID,
                           text=aim().getClearText(),
                           parse_mode='html',
                           reply_markup=defaultBtns.kAimClear())
    sqlite.setStatus(userID, 4001)
    sqlite.setLMessageCode(userID, msg.message_id)
  elif (call.data == 'clearAimSure'):
    sqlite.setNCAimCode(userID)
    msg = bot.delete_message(userID, sqlite.getLMessageCode(userID))
    msg = bot.send_photo(caption=aim().getMainText(
      "NC", sqlite.getWeeklyData(userID)),
                         chat_id=userID,
                         photo=aim().getGraph("NC", userID)[0],
                         reply_markup=defaultBtns.kAimBtns(),
                         parse_mode='html')
    sqlite.setStatus(userID, 4002)
    sqlite.setLMessageCode(userID, msg.message_id)
  elif (call.data == 'myWeekStart'):
    if status == 4003:
      lMessageCode = sqlite.getLMessageCode(userID)
      bot.delete_message(userID, lMessageCode)
    sqlite.setWeeklyData(userID, "NC")
    msg = bot.send_message(userID,
                           myWeek().getMainEmptyText(),
                           parse_mode='html',
                           reply_markup=defaultBtns.kMyWeekBtns())
    sqlite.setStatus(userID, 4003)
    sqlite.setLMessageCode(userID, msg.message_id)
  elif (call.data == 'myWeek'):
    weeklyData = sqlite.getWeeklyData(userID)
    userName = call.from_user.first_name
    if myWeek().isOldWeekData(weeklyData):
      weeklyData = myWeek().clearOldWeekData(weeklyData)
      sqlite.setWeeklyData(userID, weeklyData)
    if status in [4000, 4005]:
      lMessageCode = sqlite.getLMessageCode(userID)
      bot.delete_message(userID, lMessageCode)
    if weeklyData == '0':
      msg = bot.send_message(userID,
                             myWeek().getWelcomeText(),
                             parse_mode='html',
                             reply_markup=defaultBtns.kMyWeekWelcomeBtns())
    elif weeklyData == 'NC':
      msg = bot.send_message(userID,
                             myWeek().getMainEmptyText(),
                             parse_mode='html',
                             reply_markup=defaultBtns.kMyWeekBtns())
    else:
      msg = bot.send_message(userID,
                             myWeek().getMainText(weeklyData),
                             parse_mode='html',
                             reply_markup=defaultBtns.kMyWeekBtns())
    sqlite.setStatus(userID, 4003)
    sqlite.setLMessageCode(userID, msg.message_id)
  elif (call.data == 'setWeekVarCount'):
    if status == 4003:
      lMessageCode = sqlite.getLMessageCode(userID)
      bot.delete_message(userID, lMessageCode)
    msg = bot.send_message(userID,
                           myWeek().getChangeVarCountText(),
                           parse_mode='html')
    sqlite.setStatus(userID, 4004)
    sqlite.setLMessageCode(userID, msg.message_id)
  elif (call.data == 'adminPanel'):
    if (userID not in adminManager.getAdminUserIDs()):
      bot.send_message(userID,
                       errors().getAdminBlockText(),
                       reply_markup=defaultBtns.exBtn())
    else:
      bot.send_message(userID,
                       'Admin Panel',
                       reply_markup=defaultBtns.kAdminPanel())
      sqlite.setStatus(userID, 9000)
  elif (call.data == 'globalMail'):
    if (userID not in adminManager.getAdminUserIDs()):
      bot.send_message(userID,
                       errors().getAdminBlockText(),
                       reply_markup=defaultBtns.exBtn())
    else:
      bot.send_message(userID,
                       globalMail().getMainText(),
                       reply_markup=defaultBtns.kAdminPanel())
      sqlite.setStatus(userID, 9001)
  elif call.data == 'support':
    bot.send_message(userID,
                     support().getMainText(),
                     reply_markup=defaultBtns.exBtn(),
                     parse_mode='html')
  elif call.data == 'usefulLinks':
    msg = bot.send_message(userID,
                           usefulLinks().getMainText(),
                           reply_markup=defaultBtns.kUsefulLinks(),
                           parse_mode='html')
    sqlite.setStatus(userID, 5000)
    sqlite.setLMessageCode(userID, msg.message_id)
  elif call.data == 'getTaskFiles':
    if status == 5000:
      bot.delete_message(userID, sqlite.getLMessageCode(userID))
    bot.send_message(userID, getTaskFiles().getMainText(), parse_mode='html')
    sqlite.setStatus(userID, 5001)
  elif call.data == "prMat":
    bot.send_message(userID,
                     usefulLinks().getPrMatText(),
                     parse_mode='MarkdownV2',
                     reply_markup=defaultBtns.kPrMat())
  elif call.data == "mailAgreeTrue":
    if status == 0:
      mainMenuBtns = defaultBtns.kStartAdmin() if userID in adminManager.getAdminUserIDs() else defaultBtns.kStart()
      sqlite.setMailAgreeTrue(userID)
      mainMenuBtns.add(mainMenu().getMailAgreeBtn(sqlite.getMailAgree(userID)))
      bot.edit_message_reply_markup(userID,
                                    sqlite.getLMessageCode(userID),
                                    reply_markup=mainMenuBtns)
    else:
      sqlite.setMailAgreeTrue(userID)
      bot.send_message(userID, mainMenu().getChangeMailAgreeTrueSuccessText())
  elif call.data == "mailAgreeFalse":
    if status == 0:
      mainMenuBtns = defaultBtns.kStartAdmin() if userID in adminManager.getAdminUserIDs() else defaultBtns.kStart()

      sqlite.setMailAgreeFalse(userID)
      mainMenuBtns.add(mainMenu().getMailAgreeBtn(sqlite.getMailAgree(userID)))
      bot.edit_message_reply_markup(userID,
                                    sqlite.getLMessageCode(userID),
                                    reply_markup=mainMenuBtns)
    else:
      sqlite.setMailAgreeFalse(userID)
      bot.send_message(userID, mainMenu().getChangeMailAgreeFalseSuccessText())


@bot.message_handler(content_types='text')
def message_reply(message):
  userID = message.from_user.id
  userName = message.from_user.first_name
  sqlite.checkUser(userID, userName)
  userStatus = sqlite.getUserStatus(userID)
  if (userStatus // 1000 == 1):
    numberApTask = message.text
    answer = linkGenerating.getGeneratedLinkForAnswerPolyakov(
      userStatus - 1000, numberApTask)
    if ('err' in str(answer)):
      bot.reply_to(message,
                   errors().getSGWText(),
                   parse_mode='html',
                   reply_markup=defaultBtns.exBtn())
    elif (answer != None and answer != 0):
      if ('<br/>' in answer):
        answer = answer.replace('<br/>', '\n')
      bot.reply_to(message,
                   showAnswer().getAnswerText(),
                   reply_markup=showAnswer().getAnswerBtns(answer),
                   parse_mode='html')
    else:
      bot.reply_to(message, errors().getSGWText(), parse_mode='html')
  elif (userStatus == 9001):
    globalMail().send(bot, message.text, sqlite.getAllUserIDs())
  elif userStatus == 4004:
    weeklyData = sqlite.getWeeklyData(userID)
    weeklyData, changeStatus = myWeek().changeVarCount(weeklyData,
                                                       message.text)
    if changeStatus == 1:
      sqlite.setWeeklyData(userID, weeklyData)
      msg = bot.send_message(
        userID,
        myWeek().getChangeVarCountSureText(),
        parse_mode='html',
        reply_markup=defaultBtns.kMyWeekVarCountSureBtns()),
      sqlite.setStatus(userID, 4005)
      sqlite.setLMessageCode(userID, msg[0].message_id)
    if changeStatus == 'e':
      msg = bot.send_message(userID, weeklyData, parse_mode='html')
  elif userStatus == 5001:
    bot.reply_to(message,
                 getTaskFiles().getAnswer(message.text),
                 parse_mode='html',
                 reply_markup=getTaskFiles().getAnswerBtns(message.text)())
  else:
    jokes = additionalData().jokesSchema
    bot.reply_to(message,
                 additionalData().getRandomJoke(),
                 parse_mode='html',
                 reply_markup=defaultBtns.exBtn())


@bot.message_handler(content_types='photo')
def photoAnswer(message):
  userID = message.from_user.id
  photo = message.photo[-1].file_id
  status = sqlite.getUserStatus(userID)
  if (status == 9001):
    globalMail().send(bot,
                      bot.download_file(bot.get_file(photo).file_path),
                      sqlite.getAllUserIDs(),
                      caption=message.caption,
                      isPhoto=True)
  else:
    jokes = additionalData().jokesSchema
    bot.reply_to(message,
                 additionalData().getRandomJoke(),
                 parse_mode='html',
                 reply_markup=defaultBtns.exBtn())


@bot.message_handler(content_types='document')
def photoAnswer(message):
  userID = message.from_user.id
  doc = message.document.file_id
  status = sqlite.getUserStatus(userID)
  if (status == 9001):
    globalMail().send(bot,
                      bot.download_file(bot.get_file(doc).file_path),
                      sqlite.getAllUserIDs(),
                      caption=message.caption,
                      isPhoto=False)
  else:
    jokes = additionalData().jokesSchema
    bot.reply_to(message,
                 additionalData().getRandomJoke(),
                 parse_mode='html',
                 reply_markup=defaultBtns.exBtn())


@bot.message_handler(content_types='audio')
def photoAnswer(message):
  userID = message.from_user.id
  audio = message.audio.file_id
  status = sqlite.getUserStatus(userID)
  if (status == 9001):
    globalMail().send(bot,
                      bot.download_file(bot.get_file(audio).file_path),
                      sqlite.getAllUserIDs(),
                      caption=message.caption,
                      isAudio=True)
  else:
    bot.reply_to(message,
                 additionalData().getRandomJoke(),
                 parse_mode='html',
                 reply_markup=defaultBtns.exBtn())


keep_alive()
bot.infinity_polling()
