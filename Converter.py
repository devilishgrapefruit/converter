from tkinter import *
import tkinter.ttk as ttk
import urllib.request
import xml.dom.minidom
import datetime
import matplotlib
import matplotlib.pyplot as plt


def convert_button():
    if txt.get().isdigit():
        value = float(txt.get())
    else:
        return

    convert1 = float(allconvertors[allnames.index(combo_one.get())].replace(",", ".")) /\
               allnominal[allnames.index(combo_one.get())]
    convert2 = float(allconvertors[allnames.index(combo_two.get())].replace(",", ".")) /\
               allnominal[allnames.index(combo_two.get())]
    value = '{:.2f}'.format(convert1 / convert2 * value)
    lbl.configure(text=value)


# Окно приложения
window = Tk()
window.title("Конвертер валют")
window.geometry("1280x720")

# Вкладки
tab_control = ttk.Notebook(window)
tab1 = ttk.Frame(tab_control)
tab2 = ttk.Frame(tab_control)
tab_control.add(tab1, text="Калькулятор валют")
tab_control.add(tab2, text="Динамика курса")

# парсинг с сайта
allnames = []
allconvertors = []
allnominal = []
data = datetime.datetime.now()
data = data.strftime("%d/%m/%Y")
response = urllib.request.urlopen("http://www.cbr.ru/scripts/XML_daily.asp?date_req=" + data)
dom = xml.dom.minidom.parse(response) #Получение дом структуры файла
nodeArray = dom.getElementsByTagName("Valute")
for node in nodeArray:
    childlist = node.childNodes
    allnominal.append(int(childlist[2].childNodes[0].nodeValue))
    allnames.append(childlist[3].childNodes[0].nodeValue)
    allconvertors.append(childlist[4].childNodes[0].nodeValue)

allnames.append("Русских рублей")
allconvertors.append("1,0")
allnominal.append(1)

#Калькулятор валют

# Первый курс
combo_one = ttk.Combobox(tab1)
combo_one["values"] = allnames
combo_one.grid(column=0, row=0)
combo_one.place(x=40, y=30)

# Второй курс
combo_two = ttk.Combobox(tab1)
combo_two["values"] = allnames
combo_two.grid(column=0, row=0)
combo_two.place(x=40, y=60)

# Ввод числа
txt = Entry(tab1, width=16)
txt.grid(column=0, row=0)
txt.place(x=200, y=30)

# Текст
lbl = Label(tab1, text="0")
lbl.grid(column=0, row=0)
lbl.place(x=200, y=60)

# Кнопка
btn = Button(tab1, text="Конвертировать", command=convert_button)
btn.grid(column=0, row=0)
btn.place(x=320, y=27)


#Динамика курса

# Узнать ценну определенной валюты в определенной дате
def drawgra():
    if selected.get() == 1:
        week()
    elif selected.get() == 2:
        month()
    elif selected.get() == 3:
        year()


def info(date, name):
    if (name == "Русских рублей"):
        return "1,0"
    response = urllib.request.urlopen("http://www.cbr.ru/scripts/XML_daily.asp?date_req=" + date)
    dom = xml.dom.minidom.parse(response)
    nodeArray = dom.getElementsByTagName("Valute")
    for node in nodeArray:
        childlist = node.childNodes
        if childlist[3].childNodes[0].nodeValue == name:
            return childlist[4].childNodes[0].nodeValue


# Неделя
weeks = []
now = datetime.datetime.now().isoweekday()
for day in range(4):
    weeks.append((datetime.datetime.now() - datetime.timedelta(days=day * 7 + now)).strftime("%d/%m/%Y") + " - " +
                 (datetime.datetime.now() - datetime.timedelta(days=day * 7 + now + 6)).strftime("%d/%m/%Y"))

# Месяц
num_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
spisofmonths = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август",
                "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]
months = []
for i in range(4):
    m = ((datetime.datetime.now() - datetime.timedelta(days=i * 30)).strftime("%m %Y"))
    months.append(spisofmonths[int(m.split()[0]) - 1] + ' - ' + m.split()[1])

# Год
years = []
for i in range(4):
    years.append((datetime.datetime.now() - datetime.timedelta(days=i * 365)).strftime("%Y"))


# Поменять на недели
def switchweek():
    combo_two_2["values"] = weeks


# Поменять на месяцы
def switchmonth():
    combo_two_2["values"] = months


# Поменять на годы
def switchyears():
    combo_two_2["values"] = years


def week():
    week_value = []
    value = combo_one_2.get()
    for day in range(4):
        all = []
        for i in range(7):
            time = (datetime.datetime.now() - datetime.timedelta(days=day * 7 + now + i)).strftime("%d/%m/%Y")
            try:
                all.append(float((info(time, value)).replace(",", ".")) / allnominal[allnames.index(value)])
            except AttributeError:
                return
        week_value.append(all)
    try:
        fig.clear()
        plt.plot(['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'], week_value[weeks.index(combo_two_2.get())][::-1])
        plt.draw()
    except:
        return


def month():
    month_value = []
    help = str(spisofmonths.index(combo_two_2.get().split()[0]) + 1).rjust(2, '0')
    value = combo_one_2.get()
    now = datetime.datetime.now()
    while help != (now - datetime.timedelta(days=1)).strftime("%m"):
        now -= datetime.timedelta(days=1)
    now -= datetime.timedelta(days=1)
    while int((now - datetime.timedelta(days=1)).strftime("%m")) == int(now.strftime("%m")):
        now -= datetime.timedelta(days=1)
        month_value.append(float((info(now.strftime("%d/%m/%Y"), value)).replace(",", ".")) / allnominal[allnames.index(value)])
    try:
        fig.clear()
        plt.plot([str(i + 1) for i in range(0, len(month_value))], [month_value[::-1][i] for i in range(0, len(month_value[::-1]))])
        plt.draw()
    except:
        return


def year():
    year_value = []
    value = combo_one_2.get()
    value2 = combo_two_2.get()
    now = datetime.datetime.now()
    while value2 != (now - datetime.timedelta(weeks=1)).strftime("%Y"):
        now -= datetime.timedelta(weeks=1)
    now -= datetime.timedelta(weeks=1)
    while int((now - datetime.timedelta(weeks=1)).strftime("%Y")) == int(now.strftime("%Y")):
        now -= datetime.timedelta(weeks=1)
        year_value.append(float((info(now.strftime("%d/%m/%Y"), value)).replace(",", ".")) / allnominal[allnames.index(value)])
    try:
        if len(year_value) > 27:
            k = 3
        else:
            k = 1
        fig.clear()
        plt.plot([str(i + 1) for i in range(0, len(year_value), k)],
                 [year_value[i] for i in range(0, len(year_value), k)][::-1])
        plt.draw()
    except:
        return

# def quarter():
#     quarter_value = []

# Текст
lbl2 = Label(tab2, text="Валюта")
lbl2.grid(column=0, row=0)
lbl2.place(x=55, y=18)

# курс
combo_one_2 = ttk.Combobox(tab2)
combo_one_2["values"] = allnames
combo_one_2.grid(column=0, row=0)
combo_one_2.place(x=20, y=39)

# Текст
lbl3 = Label(tab2, text="Период")
lbl3.grid(column=0, row=0)
lbl3.place(x=240, y=18)

selected = IntVar()
# Кнопка 1
rad1 = Radiobutton(tab2, text='Неделя', value=1, command=switchweek, variable=selected)
rad1.grid(column=0, row=0)
rad1.place(x=240, y=60)

# Кнопка 2
rad2 = Radiobutton(tab2, text='Месяц', value=2, command=switchmonth, variable=selected)
rad2.grid(column=0, row=0)
rad2.place(x=240, y=83)

# Кнопка 3
rad4 = Radiobutton(tab2, text='Год', value=3, command=switchyears, variable=selected)
rad4.grid(column=0, row=0)
rad4.place(x=240, y=106)

# Текст
lbl4 = Label(tab2, text="Выбор периода")
lbl4.grid(column=0, row=0)
lbl4.place(x=360, y=18)

# Второй курс
combo_two_2 = ttk.Combobox(tab2)
combo_two_2.grid(column=0, row=0)
combo_two_2.place(x=326, y=50)

# ГРАФИК
matplotlib.use('TkAgg')
fig = plt.figure()
canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(fig, master=tab2)
plot_widget = canvas.get_tk_widget()
fig.clear()
plt.grid()
plot_widget.grid(row=0, column=0)
plot_widget.place(x=359, y=140)

# Кнопка
draw = Button(tab2, text="Построить график", command=drawgra)
draw.grid(column=0, row=0)
draw.place(x=50, y=100)

tab_control.pack(expand=True, fill=BOTH)
window.mainloop()
