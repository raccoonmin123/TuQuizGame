import tkinter as tk
import pymysql
import subprocess

window = tk.Tk()
window.title("LoginPage")
window.geometry("500x300")

conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='root', db='tuQuizGame', charset='utf8')


def login():
    email = entry_id.get()
    password = entry_pw.get()

    cursor = conn.cursor()
    sql = "SELECT * FROM user WHERE email = %s AND password = %s"
    cursor.execute(sql, (email, password))

    result = cursor.fetchone()
    if result:
        print("로그인 성공!")
        subprocess.Popen(["python", "tuQuizGameMain.py"])
    else:
        print("로그인 실패: 아이디나 비밀번호가 틀렸습니다.")
    cursor.close()


def open_sign_up():
    subprocess.Popen(["python", "signUp.py"])


label_id = tk.Label(window, text="아이디:")
label_id.pack()

entry_id = tk.Entry(window)
entry_id.pack()

label_pw = tk.Label(window, text="비밀번호:")
label_pw.pack()

entry_pw = tk.Entry(window, show="*")
entry_pw.pack()

button_login = tk.Button(window, text="로그인", fg="red", command=login)
button_login.pack()

button_signup = tk.Button(window, text="회원가입", command=open_sign_up)
button_signup.pack()

window.mainloop()
