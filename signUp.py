import tkinter as tk
import pymysql
import subprocess

window = tk.Tk()
window.title("SignUpPage")
window.geometry("500x350")

conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='root', db='tuQuizGame', charset='utf8')


def register():
    username = entry_id.get()
    password = entry_pw.get()
    nickname = entry_nickname.get()

    cursor = conn.cursor()
    sql = "INSERT INTO user (email, password, name) VALUES (%s, %s, %s)"

    try:
        cursor.execute(sql, (username, password, nickname))
        conn.commit()
        print("회원가입 성공!")
        label_message.config(text="회원가입 성공!", fg="green")
    except Exception as e:
        print("회원가입 실패:", e)
        label_message.config(text="회원가입 실패: 이미 존재하는 아이디입니다.", fg="red")
    cursor.close()


label_id = tk.Label(window, text="아이디:")
label_id.pack()

entry_id = tk.Entry(window)
entry_id.pack()

label_pw = tk.Label(window, text="비밀번호:")
label_pw.pack()

entry_pw = tk.Entry(window, show="*")
entry_pw.pack()

label_nickname = tk.Label(window, text="닉네임:")
label_nickname.pack()

entry_nickname = tk.Entry(window)
entry_nickname.pack()

button_register = tk.Button(window, text="회원가입", fg="blue", command=register)
button_register.pack()

label_message = tk.Label(window, text="")
label_message.pack()

window.mainloop()
