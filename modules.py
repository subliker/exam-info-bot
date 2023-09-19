from localization import loc
import random
import json
import numpy as np
import os
from pathlib import Path
import datetime
import defaultBtns
import matplotlib.pyplot as plt
from telebot import types

plt.switch_backend('Agg')
from keyboa import Keyboa

plt.rcParams.update({'font.size': 6})


def getTasksFromDBText(text, dataBase):
  for i in range(len(dataBase)):
    text += (str(i + 1) + ',') if dataBase[i] else ''
  return text[:-1]


def sklCh(ch, s):
  return s + (''
              if ch[-1] == '1' else 'a' if ch[-1] in ['2', '3', '4'] else 'ов')


class mainMenu:
  mainMenuSchema = loc["mainMenuSchema"]

  def getWelcomeText(self):
    return self.mainMenuSchema["main"]

  def getMailAgreeBtn(self, mailAgree):
    return types.InlineKeyboardButton(
      text=self.mainMenuSchema['mailAgreeTrueBtn']['text'],
      callback_data=self.mainMenuSchema['mailAgreeTrueBtn']['callback_data']
    ) if mailAgree == "True" else  types.InlineKeyboardButton(
      text=self.mainMenuSchema['mailAgreeFalseBtn']['text'],
      callback_data=self.mainMenuSchema['mailAgreeFalseBtn']['callback_data']) if mailAgree == "False" else print("Что-то не так с кодом рассылки")

  def getChangeMailAgreeTrueSuccessText(self):
    return self.mainMenuSchema['changeMailAgreeTrueSuccessText']

  def getChangeMailAgreeFalseSuccessText(self):
    return self.mainMenuSchema['changeMailAgreeFalseSuccessText']


class showAnswer:
  showAnswerSchema = loc['showAnswerSchema']
  defaultBtns = loc['defaultBtns']

  def getChooseTopicText(self):
    return self.showAnswerSchema['title'] + self.showAnswerSchema['chooseTopic']

  def getChooseTaskText(self, apTask):
    return self.showAnswerSchema['title'] + self.showAnswerSchema[
      'chosen_1'] + str(apTask) + self.showAnswerSchema['chosen_2']

  def getAnswerText(self):
    return self.showAnswerSchema['title'] + self.showAnswerSchema['answer']

  def getAnswerBtns(self, answer):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    answerSite = types.WebAppInfo(answer)
    answerLinkBtn = types.InlineKeyboardButton(
      text=self.showAnswerSchema['answerLinkBtn'], url=answer)
    exitBtn = types.InlineKeyboardButton(
      text=self.defaultBtns['exBtn'][0]['text'],
      callback_data=self.defaultBtns['exBtn'][0]['callback_data'])
    answerBtn = types.InlineKeyboardButton(
      text=self.showAnswerSchema['linkBtn'], web_app=answerSite)
    keyboard.add(answerBtn)
    keyboard.add(answerLinkBtn)
    keyboard.add(exitBtn)
    return keyboard


class randomTask:
  randomTaskSchema = loc['randomTaskSchema']

  def getChooseTopicText(self):
    return self.randomTaskSchema['title'] + self.randomTaskSchema['chooseTopic']

  def getChooseTaskText(self, ntTask):
    ntText = str(ntTask)
    if ntTask == 19:
      ntText += ', 20, 21'
    return self.randomTaskSchema['title'] + self.randomTaskSchema[
      'chosen_1'] + ntText + self.randomTaskSchema['chosen_2']

  def getAnswerBtns(self, link, isChecked=False):
    btns = [
      {
        "text": self.randomTaskSchema['linkBtn'],
        "url": link
      },
      {
        self.randomTaskSchema['addTaskBtn'] if not isChecked else self.randomTaskSchema['addTaskBtnChecked']:
        "checkTask"
      },
    ]
    btns += self.randomTaskSchema['btns']
    return Keyboa(btns, copy_text_to_callback=True)


class genVar:
  genVarSchema = loc['genVarSchema']

  def getMainText(self):
    return self.genVarSchema['title'] + self.genVarSchema['main']

  def getAnswerBtns(self, link):
    btns = [
      {
        "text": self.genVarSchema['linkBtn'],
        "url": link
      },
    ]
    btns += self.genVarSchema['btns']
    return Keyboa(btns, copy_text_to_callback=True)


class checkVar:
  checkVarSchema = loc['checkVarSchema']
  errorsSchema = loc['errorsSchema']

  def getMainText(self):
    return self.checkVarSchema['title'] + self.checkVarSchema['main']

  def getSureText(self, userID, isInDb, aimDataBaseDump):
    if not isInDb:
      return self.errorsSchema['somethingGoesWrong']
    sureSchema = self.checkVarSchema['sureSchema']
    return self.checkVarSchema[
      'title'] + sureSchema['main_n'] + getTasksFromDBText(
        '', aimDataBaseDump[userID]) + sureSchema['n_main']

  def getSaveText(self, aimUserDataBase):
    saveSchema = self.checkVarSchema['saveSchema']
    return self.checkVarSchema[
      'title'] + saveSchema['main_n'] + getTasksFromDBText(
        '', aimUserDataBase) + saveSchema['n_main']

  def prepareAimCode(self, oldAimCode, newAimUserDataBase):
    oldAimCode = json.loads(oldAimCode) if oldAimCode not in ['NC', '0'
                                                              ] else [0] * 27
    aimCode = [(oldAimCode[i] + newAimUserDataBase[i])
               for i in range(len(newAimUserDataBase))]
    return json.dumps(aimCode)

  def getCheckVarButtons(self, aimUserDataBase):
    if aimUserDataBase == []:
      return defaultBtns.kCheckVar
    btns = []
    for i in range(1, 28):
      if (aimUserDataBase[i - 1] == 1):
        btn = {}
        btn[str(i) + ' ✅'] = str(i)
        btns.append(btn)
      else:
        btn = {}
        btn[str(i)] = str(i)
        btns.append(btn)
    btn = {"Готово": "Done"}
    btns.append(btn)
    return Keyboa(items=btns, items_in_row=3, front_marker='cv')


class aim:
  # aimCode => Количество выполненных заданий (1);(2);...(27); ([0:27]) + количесто выполненных вариантов ([27]) (Индексы уже сплитованного кода (;))
  aimSchema = loc['aimSchema']

  def getMainText(self, aimCode, weeklyData):
    text = self.aimSchema['title'] + (self.aimSchema['blank'] if aimCode in
                                      ['NC', '0'] else self.aimSchema['text'])
    if weeklyData in ['NC', '0']:
      return text
    weekDataScheme = self.aimSchema['weekDataScheme']
    weeklyData = json.loads(weeklyData)
    varCount = str(weeklyData['varCount'])
    compVar = str(weeklyData['compVar'])
    if compVar != '0':
      text += weekDataScheme['main_comp'] + compVar + sklCh(
        compVar, weekDataScheme['vars']) + (
          weekDataScheme['comp_main_count'] + varCount +
          weekDataScheme['count_main'] if varCount != '0' else
          (weekDataScheme['countEmpty_main']))
    else:
      text += (
        weekDataScheme['main_compEmpty'] + varCount +
        weekDataScheme['compEmpty_count_main']
      ) if varCount != '0' else weekDataScheme['main_compEmpty_countEmpty']
    return text

  def getWelcomeText(self):
    return self.aimSchema['mainWelcome']

  def getGraph(self, aimCode, userID):
    values = json.loads(aimCode) if aimCode not in ['NC', '0'] else [0] * 27
    index = np.arange(27)
    plt.clf()
    plt.bar(index, values, width=0.7)
    plt.xticks(index, [
      '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13',
      '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25',
      '26', '27'
    ])
    # plt.yticks(np.arange(max(values) + 1),
    #            [str(i) for i in range(0,
    #                                   max(values) + 1)])
    graphName = str(userID) + str(int(datetime.datetime.now().timestamp()))
    figPath = Path('data', graphName + '.png')
    plt.savefig(figPath)
    return (open(figPath, 'rb'), graphName)

  def clearTempGraph(self, graphName):
    return os.remove('data/' + graphName + '.png')

  def addTaskToAimCode(self, aimCode, numTask):
    values = json.loads(aimCode) if aimCode not in ['NC', '0'] else [0] * 27
    values[numTask - 1] += 1
    if (numTask == 19):
      values[19] += 1
      values[20] += 1
    return json.dumps(values)

  def getClearText(self):
    return self.aimSchema['clear']


class myWeek:
  myWeekSchema = loc['myWeekSchema']

  def getMainText(self, weeklyData):
    weeklyData = json.loads(weeklyData)
    varCount = str(weeklyData['varCount'])
    compVar = str(weeklyData['compVar'])
    return self.myWeekSchema['title'] + self.myWeekSchema[
      'varCount'] + varCount + self.myWeekSchema[
        'varCountDot'] + self.myWeekSchema[
          'compVar'] + compVar + self.myWeekSchema['compVarDot']

  def getWelcomeText(self):
    return self.myWeekSchema['title'] + self.myWeekSchema['mainWelcome']

  def addCompVar(self, weeklyData):
    if weeklyData in ['NC', '0']:
      currWeekID = 'y' + str(datetime.datetime.now().year) + 'm' + str(
        datetime.datetime.now().isocalendar()[1])
      weeklyData = {"varCount": 0, "compVar": 1, "currWeekID": currWeekID}
    else:
      weeklyData = json.loads(weeklyData)
      weeklyData['compVar'] += 1
    return json.dumps(weeklyData)

  def isOldWeekData(self, weeklyData):
    return (json.loads(weeklyData)['currWeekID'] != 'y' +
            str(datetime.datetime.now().year) + 'm' +
            str(datetime.datetime.now().isocalendar()[1])
            ) if weeklyData not in ['NC', '0'] else 0

  def clearOldWeekData(self, weeklyData):
    if weeklyData in ['NC', '0']:
      return 0
    weeklyData = json.loads(weeklyData)
    weeklyData['compVar'] = 0
    currWeekID = 'y' + str(datetime.datetime.now().year) + 'm' + str(
      datetime.datetime.now().isocalendar()[1])
    weeklyData['currWeekID'] = currWeekID
    return json.dumps(weeklyData)

  def changeVarCount(self, weeklyData, varCount):
    try:
      varCount = int(varCount)
    except:
      return (self.myWeekSchema['incorrectVarCount'], 'e')
    if varCount >= 64:
      return (self.myWeekSchema['tooManyVarCount'], 'e')
    if varCount <= 0:
      return (self.myWeekSchema['notNaturalVarCount'], 'e')
    if weeklyData == 'NC':
      currWeekID = 'y' + str(datetime.datetime.now().year) + 'm' + str(
        datetime.datetime.now().isocalendar()[1])
      weeklyDataR = {
        "varCount": varCount,
        "compVar": 0,
        "currWeekID": currWeekID
      }
    else:
      weeklyDataR = json.loads(weeklyData)
      weeklyDataR['varCount'] = varCount
    return (json.dumps(weeklyDataR), 1)

  def getMainEmptyText(self):
    return self.myWeekSchema['title'] + self.myWeekSchema['mainEmpty']

  def getChangeVarCountText(self):
    return self.myWeekSchema['title'] + self.myWeekSchema['changeVarCount']

  def getChangeVarCountSureText(self):
    return self.myWeekSchema['title'] + self.myWeekSchema[
      'varCountSureScheme']['main']


class globalMail:
  globalMailScheme = loc['globalMailSchema']

  def getMainText(self):
    return self.globalMailScheme['main']

  def send(self,
           bot,
           msgData,
           ids,
           caption='',
           isPhoto=False,
           isAudio=False,
           filename=''):
    if ids == []:
      return print('Не зарегистрировано ниодного пользователя на рассылку')
    if type(msgData) == str:
      for userId in ids:
        bot.send_message(userId, msgData, parse_mode='html')
    elif type(msgData) == bytes and isPhoto:
      for userId in ids:
        bot.send_photo(userId, msgData, caption=caption, parse_mode='html')
    elif type(msgData) == bytes and isAudio:
      for userId in ids:
        bot.send_audio(userId, msgData, caption=caption, parse_mode='html')
    elif type(msgData) == bytes:
      for userId in ids:
        bot.send_document(userId, msgData, caption=caption, parse_mode='html')
    return 1


class support:
  supportSchema = loc['supportSchema']

  def getMainText(self):
    return self.supportSchema['title'] + self.supportSchema['main']


class usefulLinks:
  usefulLinksSchema = loc['usefulLinksSchema']

  def getMainText(self):
    return self.usefulLinksSchema['title']

  def getPrMatText(self):
    return self.usefulLinksSchema['prMatMain'].replace("{bkslh}",
                                                       "\\").replace(
                                                         '{lbr}', '\n')


class getTaskFiles:
  getTaskFilesSchema = loc['getTaskFilesSchema']

  def getMainText(self):
    return self.getTaskFilesSchema['title'] + self.getTaskFilesSchema['main']

  def getAnswer(self, task):
    if task not in ['3', '9', '10', '17', '18', '22', '24', '26', '27']:
      return self.getTaskFilesSchema['incorrectTask']
    return self.getTaskFilesSchema['title'] + self.getTaskFilesSchema['answer']

  def getAnswerBtns(self, task):
    btns = [{
      "text": self.getTaskFilesSchema['linkBtn'],
      "url": 'https://kpolyakov.spb.ru/download/' + task + 'data.zip'
    }] if task in ['3', '9', '10', '17', '18', '22', '24', '26', '27'] else []
    btns += self.getTaskFilesSchema['btns']
    return Keyboa(btns, copy_text_to_callback=True)


class currentData:
  usersInfo = {}


class errors:
  errorsSchema = loc['errorsSchema']

  def getSGWText(self):
    return self.errorsSchema['somethingGoesWrong']

  def getAdminBlockText(self):
    return self.errorsSchema['noAdminBlock']


class additionalData:
  jokesSchema = loc['noMeanTextJokes']

  def getRandomJoke(self):
    return self.jokesSchema[random.randint(0, len(self.jokesSchema) - 1)]
