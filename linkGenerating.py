def getSelectCode(tasksValue):
  try:
    code = ''.join(reversed(tasksValue))
    code = hex(int(code, base=2))[2:]
    return code
  except:
    return 0


def getGeneratedLinkPolyakovByTasks(tasksValue):
  try:
    if (tasksValue == '27all'):
      tV = '1' * 27
    else:
      tV = '0' * (int(tasksValue) - 1) + '1' + '0' * (27 - int(tasksValue))
    sC = getSelectCode(tV)
    if (sC):
      link = 'https://kpolyakov.spb.ru/school/ege/gen.php?action=viewVar&select=' + sC + '&answers=on'
      return link
    else:
      return 0
  except:
    return 0


def getGeneratedLinkForAnswerPolyakov(taskTopic, taskNumber):
  try:
    link = 'https://kpolyakov.spb.ru/school/ege/getanswer.php?egeNo=' + str(
      taskTopic) + '&topicNo=' + str(taskNumber)
    return link
  except:
    return 0
