import sqlite3
from datetime import date
from tkinter import *
from tkinter import ttk

import matplotlib.pyplot as plt
import pygal


# 初始化
def init(*args):
    # sqlite3连接代码
    conn = sqlite3.connect('sqlite3.db')
    c = conn.cursor()

    # 如果YE表不存在则创建。
    sql = "CREATE TABLE IF NOT EXISTS YE (ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, RQ TEXT NOT NULL UNIQUE, ZSYH INTEGER NOT NULL, ZFB INTEGER NOT NULL, YE INTEGER NOT NULL)"

    # 执行sql
    c.execute(sql)

    # 提交数据
    conn.commit()

    # 关闭连接
    conn.close()


# 初始化
init()


# 数据插入或更新
def submit(*args):
    # sqlite3连接代码
    conn = sqlite3.connect('sqlite3.db')
    c = conn.cursor()

    # 表中无当日数据则插入，否则更新。
    sql = "SELECT COUNT(*) COUNT FROM YE WHERE RQ = (SELECT DATE('NOW'))"
    for row in c.execute(sql):
        if row[0] == 0:
            sql = "INSERT INTO YE (RQ, ZSYH, ZFB, YE) VALUES ((SELECT DATE('NOW')), ?, ?, ?)"
        else:
            sql = "UPDATE YE SET ZSYH = ?, ZFB = ?, YE = ? WHERE RQ = (SELECT DATE('NOW'))"

    # 捕获错误处理
    try:
        # 预编译sql参数
        ye = (zsyh_zsyh.get(), zfb_zfb.get(), float(zsyh_zsyh.get()) + float(zfb_zfb.get()))

        # 执行sql
        c.execute(sql, ye)

        # 提交数据
        conn.commit()

    except ValueError:
        print("Oops!  That was no valid number.  Try again...")

    # 清空Treeview数据
    [tree.delete(item) for item in tree.get_children()]

    # 重新生成Treeview数据
    sql = "SELECT * FROM YE WHERE STRFTIME('%Y', RQ) = STRFTIME('%Y', 'NOW') AND STRFTIME('%m', RQ) = STRFTIME('%m', 'NOW') ORDER BY RQ DESC"
    for row in c.execute(sql):
        tree.insert("", "end", text=row[0],
                    values=(row[0], row[1], round(row[2], 2), round(row[3], 2), round(row[4], 2)))

    # 关闭连接
    conn.close()


def count(*args):
    # sqlite3连接代码
    conn = sqlite3.connect('sqlite3.db')
    c = conn.cursor()

    rq = []
    ye = []
    title = ''

    # 获取下拉框年份
    year = "'" + str(year_StringVar.get()) + "'"

    # 获取下拉框月份
    month = "'" + str(month_StringVar.get()) + "'"

    # 年统计
    if year_month_day_StringVar.get() == "year":
        sql = "SELECT RQ, SUM(YE) / COUNT(RQ) YE FROM YE GROUP BY STRFTIME('%Y', RQ) ORDER BY RQ ASC"
        for row in c.execute(sql):
            rq.append(row[0][0:4])
            ye.append(row[1])

    # 月统计
    if year_month_day_StringVar.get() == "month":
        sql = "SELECT RQ, SUM(YE) / COUNT(RQ) YE FROM YE WHERE STRFTIME('%Y', RQ) = " + year + " GROUP BY STRFTIME('%m', RQ) ORDER BY RQ ASC"
        for row in c.execute(sql):
            rq.append(row[0][5:7])
            ye.append(row[1])

        # pygal标题
        title = str(year_StringVar.get()) + '年'

    # 日统计
    if year_month_day_StringVar.get() == "day":
        sql = "SELECT RQ, YE FROM YE WHERE STRFTIME('%Y', RQ) = " + year + " AND STRFTIME('%m', RQ) = " + month + " ORDER BY RQ ASC"
        for row in c.execute(sql):
            rq.append(row[0][8:])
            ye.append(row[1])

        # pygal标题
        title = str(year_StringVar.get()) + '年' + str(month_StringVar.get()) + '月'

    # 关闭连接
    conn.close()

    # matplotlib.pyplot的X轴和Y轴
    plt.plot(rq, ye)

    # matplotlib.pyplot的X轴和Y轴点的大小
    plt.scatter(rq, ye, s=66)

    # matplotlib.pyplot的X轴标签
    plt.xlabel("rq")

    # matplotlib.pyplot的Y轴标签
    plt.ylabel("ye")

    # matplotlib.pyplot的标题
    plt.title("YE")

    # matplotlib.pyplot的展现
    plt.show()

    # Basic simple line graph:
    line_chart = pygal.Line()
    line_chart.title = title + '余额'
    line_chart.x_labels = map(str, rq)
    line_chart.add("余额", ye)
    line_chart.render_to_file('ye.svg')


# 查询
def select(*args):
    # sqlite3连接代码
    conn = sqlite3.connect('sqlite3.db')
    c = conn.cursor()

    # 获取下拉框年份
    year = "'" + str(year_StringVar.get()) + "'"

    # 获取下拉框月份
    month = "'" + str(month_StringVar.get()) + "'"

    sql = ""

    # 年查询
    if year_month_day_StringVar.get() == "year":
        sql = "SELECT * FROM YE WHERE STRFTIME('%Y', RQ) = " + year + " ORDER BY RQ DESC"

    # 月查询
    if year_month_day_StringVar.get() == "month":
        sql = "SELECT * FROM YE WHERE STRFTIME('%Y', RQ) = " + year + " AND STRFTIME('%m', RQ) = " + month + " ORDER BY RQ DESC"

    # 清空Treeview数据
    [tree.delete(item) for item in tree.get_children()]

    # 重新生成Treeview数据
    for row in c.execute(sql):
        tree.insert("", "end", text=row[0],
                    values=(row[0], row[1], round(row[2], 2), round(row[3], 2), round(row[4], 2)))

    # 关闭连接
    conn.close()


def select_year(*args):
    # sqlite3连接代码
    conn = sqlite3.connect('sqlite3.db')
    c = conn.cursor()

    sql = "SELECT DISTINCT (STRFTIME('%Y', RQ)) YEAR FROM YE ORDER BY STRFTIME('%Y', RQ) DESC"

    year = []

    [year.append(row[0]) for row in c.execute(sql)]

    # 关闭连接
    conn.close()

    return year


def select_month(*args):
    # sqlite3连接代码
    conn = sqlite3.connect('sqlite3.db')
    c = conn.cursor()

    sql = "SELECT DISTINCT (STRFTIME('%m', RQ)) MONTH FROM YE WHERE STRFTIME('%Y', RQ) = STRFTIME('%Y', 'NOW') ORDER BY STRFTIME('%m', RQ) DESC"

    month = []

    [month.append(row[0]) for row in c.execute(sql)]

    # 关闭连接
    conn.close()

    return month


def select_month_of_year(*args):
    # sqlite3连接代码
    conn = sqlite3.connect('sqlite3.db')
    c = conn.cursor()

    year = "'" + str(year_StringVar.get()) + "'"

    sql = "SELECT DISTINCT (STRFTIME('%m', RQ)) MONTH FROM YE WHERE STRFTIME('%Y', RQ) = " + year + " ORDER BY STRFTIME('%m', RQ) ASC"

    month = []

    [month.append(row[0]) for row in c.execute(sql)]

    month_Combobox['values'] = month

    month_Combobox.current(0)

    # 关闭连接
    conn.close()


# tkinter代码
root = Tk()
root.title("余额")

frame = ttk.Frame(root)

# 日期Label
rq = ttk.Label(frame, text="日期：")
rq_rq = ttk.Label(frame, text=date.today())

# 招商银行Entry
zsyh = ttk.Label(frame, text="招商银行：")
zsyh_zsyh = StringVar()
zsyh_zsyh_zsyh = ttk.Entry(frame, textvariable=zsyh_zsyh)

# 支付宝Entry
zfb = ttk.Label(frame, text="支付宝：")
zfb_zfb = StringVar()
zfb_zfb_zfb = ttk.Entry(frame, textvariable=zfb_zfb)

# 添加Button
submit_button = ttk.Button(frame, text="添加", command=submit)

# 年月日单选框
year_month_day_StringVar = StringVar()

year_Radiobutton = ttk.Radiobutton(frame, text='年', variable=year_month_day_StringVar, value='year')

month_Radiobutton = ttk.Radiobutton(frame, text='月', variable=year_month_day_StringVar, value='month')

day_Radiobutton = ttk.Radiobutton(frame, text='日', variable=year_month_day_StringVar, value='day')

# 默认选择月单选框
year_month_day_StringVar.set('month')

# 年下拉框
year_StringVar = StringVar()

year_Combobox = ttk.Combobox(frame, textvariable=year_StringVar)

year_Combobox.bind("<<ComboboxSelected>>", select_month_of_year)

year_Combobox['values'] = select_year()

if len(year_Combobox["values"]) == 0:
    pass
else:
    year_Combobox.current(0)

# 月下拉框
month_StringVar = StringVar()

month_Combobox = ttk.Combobox(frame, textvariable=month_StringVar)

month_Combobox['values'] = select_month()

if len(month_Combobox["values"]) == 0:
    pass
else:
    month_Combobox.current(0)

# 查询button
select_button = ttk.Button(frame, text="查询", command=select)

# 统计Button
count_button = ttk.Button(frame, text="统计", command=count)

# 表格Treeview，不显示表格头
tree = ttk.Treeview(frame, show="headings", columns=("ID", "日期", "招商银行", "支付宝", '余额'))

for column in tree['columns']:
    # 设置表格列以及居中
    tree.column(column, anchor='center')

    # 设置表格头
    tree.heading(column, text=column)

# sqlite3连接代码
conn = sqlite3.connect('sqlite3.db')
c = conn.cursor()

# 默认查询当前年月的数据
sql = "SELECT * FROM YE WHERE STRFTIME('%Y', RQ) = STRFTIME('%Y', 'NOW') AND STRFTIME('%m', RQ) = STRFTIME('%m', 'NOW') ORDER BY RQ DESC"

for row in c.execute(sql):
    tree.insert("", "end", text=row[0], values=(row[0], row[1], round(row[2], 2), round(row[3], 2), round(row[4], 2)))

# 关闭连接
conn.close()

# 滚动条Scrollbar
scrollbar = ttk.Scrollbar(frame, orient=VERTICAL, command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)

# 布局
rq.grid(column=0, row=0, columnspan=1, rowspan=1)
rq_rq.grid(column=1, row=0, columnspan=1, rowspan=1)

zsyh.grid(column=2, row=0, columnspan=1, rowspan=1)
zsyh_zsyh_zsyh.grid(column=3, row=0, columnspan=1, rowspan=1)

zfb.grid(column=4, row=0, columnspan=1, rowspan=1)
zfb_zfb_zfb.grid(column=5, row=0, columnspan=1, rowspan=1)

submit_button.grid(column=6, row=0, columnspan=1, rowspan=1)

year_Radiobutton.grid(column=0, row=1, columnspan=1, rowspan=1)
month_Radiobutton.grid(column=1, row=1, columnspan=1, rowspan=1)
day_Radiobutton.grid(column=2, row=1, columnspan=1, rowspan=1)

year_Combobox.grid(column=3, row=1, columnspan=1, rowspan=1)
month_Combobox.grid(column=4, row=1, columnspan=1, rowspan=1)

select_button.grid(column=0, row=2, columnspan=1, rowspan=1)
count_button.grid(column=1, row=2, columnspan=1, rowspan=1)

tree.grid(column=0, row=3, columnspan=8, rowspan=8)

scrollbar.grid(column=1, row=3, columnspan=8, rowspan=8, sticky=(N, S, E))

frame.grid(column=0, row=0, columnspan=8, rowspan=8)

# 输入框聚焦
zsyh_zsyh_zsyh.focus()

# 绑定回车事件
root.bind('<Return>', submit)

# 展现界面
root.mainloop()
