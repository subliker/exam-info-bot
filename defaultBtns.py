from keyboa import Keyboa
from localization import loc
# Кнопка выйти в главное меню
exBtn = Keyboa(items=loc['defaultBtns']['exBtn'])

# Кнопки в главном меню
kStart = Keyboa(items=loc['mainMenuSchema']['btns'],
                copy_text_to_callback=True)

# Кнопки в главном меню (АДМИН)
kStartAdmin = Keyboa(items=loc['mainMenuSchema']['btnsAdmin'],
                     copy_text_to_callback=True)

# Кнопки в АДМИН панели
kAdminPanel = Keyboa(items=loc['adminPanelSchema']['btns'],
                     copy_text_to_callback=True)

# Кнопки в меню Показать ответы
kShowAnswer = Keyboa(items=loc['showAnswerSchema']['tasks'],
                     items_in_row=3,
                     front_marker='ap')

# Кнопки в меню Показать случайное задание
kShowRandomTask = Keyboa(items=loc['randomTaskSchema']['tasks'],
                         items_in_row=3,
                         front_marker='nt')

# Кнопки в меню Цели Приветствие
kAimWelcomeBtns = Keyboa(items=loc['aimSchema']['btnsWelcome'],
                         copy_text_to_callback=True)

# Кнопки в меню Цели
kAimBtns = Keyboa(items=loc['aimSchema']['btns'], copy_text_to_callback=True)

# Кнопки в подтверждении очистки Целей
kAimClear = Keyboa(items=loc['aimSchema']['btnsSure'],
                   copy_text_to_callback=True)

# Кнопки в меню Сгенерировать вариант
kCheckVar = Keyboa(items=loc['checkVarSchema']['btns'],
                   items_in_row=3,
                   front_marker='cv')

# Кнопки подтверждения Результатов варианта
kСheckVarSureBtns = Keyboa(items=loc['checkVarSchema']['sureSchema']['btns'],
                           copy_text_to_callback=True)

# Кнопки при первом старте Моей Недели
kMyWeekWelcomeBtns = Keyboa(items=loc['myWeekSchema']['btnsWelcome'],
                            copy_text_to_callback=True)

# Кнопки в меню Моя неделя
kMyWeekBtns = Keyboa(items=loc['myWeekSchema']['btns'],
                     copy_text_to_callback=True)

# Кнопки при подтверждении установки количества вариантов в неделю
kMyWeekVarCountSureBtns = Keyboa(
  items=loc['myWeekSchema']['varCountSureScheme']['btns'],
  copy_text_to_callback=True)

# Кнопки в Полезные ссылки
kUsefulLinks = Keyboa(items=loc['usefulLinksSchema']['btns'],
                      copy_text_to_callback=True)

# Кнопки материалов для подготовки
kPrMat = Keyboa(items=loc['usefulLinksSchema']['prMatBtns'],
                copy_text_to_callback=True)
