from memo_card_layout import*
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QTimer #new
from random import shuffle 
from memo_data import*
from memo_edit_layout import*
from memo_main_layout import *


######################################              Константы:              #############################################
main_width, main_height = 1000, 450 # начальные размеры главного окна
card_width, card_height = 600, 500 # начальные размеры окна "карточка"
time_unit = 1000    # столько длится одна единица времени из тех, на которые нужно засыпать 
                    # (в рабочей версии программы увеличить в 60 раз!)



text_wrong = 'Невірно'
text_correct = 'Вірно'

######################################          Глобальные переменные:      #############################################
questions_listmodel = QuestionListModel() # список вопросов
radio_list = [rbtn_1, rbtn_2, rbtn_3, rbtn_4] # список виджетов, который надо перемешивать (для случайного размещения ответов)
frm_card = 0 # здесь будет связываться вопрос с формой теста
win_card = QWidget() # окно карточки
win_main = QWidget() # окно редактирования вопросов, основное в программе

frm_edit = QuestionEdit(0, text_Question, text_Answer, text_Wrong1, text_Wrong2, text_Wrong3)
timer = QTimer()

# заносимо перемикачі до списку 

#наступны два видаляємо


######################################             Тестовые данные:         #############################################
def testlist():
    
    frm = Question('Яблуко', 'apple', 'application', 'pinapple', 'apply')
    questions_listmodel.form_list.append(frm)
    frm = Question('Дім', 'house', 'horse', 'hurry', 'hour')
    questions_listmodel.form_list.append(frm)
    frm = Question('Миша', 'mouse', 'mouth', 'muse', 'museum')
    questions_listmodel.form_list.append(frm)
    frm = Question('Число', 'number', 'digit', 'amount', 'summary')
    questions_listmodel.form_list.append(frm)

######################################     Функции для проведения теста:    #############################################

def set_card():
    ''' задаёт, как выглядит окно карточки'''
    win_card.resize(card_width, card_height)
    win_card.move(300, 300)
    win_card.setWindowTitle('Memory Card')
    win_card.setLayout(layout_card)

def set_main():
    ''' задаёт, как выглядит основное окно'''
    win_main.resize(main_width, main_height)
    win_main.move(100, 100)
    win_main.setWindowTitle('Список запитань')
    win_main.setLayout(layout_main)

def show_random():
    ''' показать случайный вопрос '''
    global frm_card # как бы свойство окна - текущая форма с данными карточки
    # получаем случайные данные, и случайно же распределяем варианты ответов по радиокнопкам:
    frm_card = random_AnswerCheck(questions_listmodel, lb_Question, radio_list, lb_Correct, lb_Result)
    # мы будем запускать функцию, когда окно уже есть. Так что показываем:
    frm_card.show() # загрузить нужные данные в соответствующие виджеты 
    show_question() # показать на форме панель вопросовq

def click_OK():
    ''' проверяет вопрос или загружает новый вопрос '''
    if btn_OK.text() != 'Наступне питання':
        frm_card.check()
        show_result()
    else:
        # надпись на кнопке равна 'Следующий', вот и создаем следующий случайный вопрос:
        show_random()

def add_form():
    questions_listmodel.insertRows()
    last = questions_listmodel.rowCount(0) - 1
    index = questions_listmodel.index(last)
    list_questions.setCurrentIndex(index)
    edit_question(index)
    txt_Question.setFocus(Qt.TabFocusReason)

def edit_question(index):
    if index.isValid():
        i = index.row()
        frm = questions_listmodel.form_list[i]
        frm_edit.change(frm)
        frm_edit.show()

def del_form():
    QAbstractListModel.removeRows(list_questions.currentIndex().row())
    edit_question(list_questions.currentIndex())



def back_to_menu():
    ''' возврат из теста в окно редактора '''
    win_card.hide()
    win_main.showNormal()

#?
def start_test():
    ''' при начале теста форма связывается со случайным вопросом и показывается'''
    show_random()
    win_card.show()
    win_main.showMinimized()

def sleap_card():
    win_card.hide()
    timer.setInterval(time_unit * box_Minutes.value())
    timer.start()

######################################      Установка нужных соединений:    #############################################
def connects():
    list_questions.setModel(questions_listmodel) # связать список на экране со списком вопросов
    btn_start.clicked.connect(start_test) # нажатие кнопки "начать тест" 
    btn_OK.clicked.connect(click_OK) # нажатие кнопки "OK" на форме теста
    btn_Menu.clicked.connect(back_to_menu) # нажатие кнопки "Меню" для возврата из формы теста в редактор вопросов
    list_questions.clicked.connect(edit_question)
    btn_add.clicked.connect(add_form)
    btn_delete.clicked.connect(del_form)
    btn_Sleep.clicked.connect(sleap_card)
    timer.timeout.connect(show_card)

def show_card():
    win_card.show()
    timer.stop()

testlist()
set_card()
set_main()
connects()

win_main.show()# міняємо card на main
app.exec_()

