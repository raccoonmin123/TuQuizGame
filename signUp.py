import tkinter as tk
import pymysql
import subprocess

# Tkinter 윈도우 초기화
window = tk.Tk()
window.title("SignUpPage")
window.geometry("500x350")

# DB 연결
conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='root', db='tuQuizGame', charset='utf8')


def register():
    email = entry_id.get()
    password = entry_pw.get()
    name = entry_nickname.get()

    cursor = conn.cursor()
    sql = "INSERT INTO user (email, password, name) VALUES (%s, %s, %s)"

    try:
        cursor.execute(sql, (email, password, name))
        conn.commit()
        print("회원가입 성공!")
        subprocess.Popen(["python", "login.py"])
        label_message.config(text="회원가입 성공!", fg="green")  # 성공 메시지 출력

    except Exception as e:
        print("회원가입 실패:", e)
        label_message.config(text="회원가입 실패: 이미 존재하는 아이디입니다.", fg="red")  # 실패 메시지 출력
    cursor.close()


# UI 구성
label_id = tk.Label(window, text="이메일:")
label_id.pack()

entry_id = tk.Entry(window)
entry_id.pack()

label_pw = tk.Label(window, text="비밀번호:")
label_pw.pack()

entry_pw = tk.Entry(window, show="*")
entry_pw.pack()

label_nickname = tk.Label(window, text="닉네임:")
label_nickname.pack()

entry_nickname = tk.Entry(window)  # 닉네임 입력 필드 추가
entry_nickname.pack()

button_register = tk.Button(window, text="회원가입", fg="blue", command=register)
button_register.pack()

label_message = tk.Label(window, text="")
label_message.pack()

# Tkinter 이벤트 루프 실행
window.mainloop()
