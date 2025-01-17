import tkinter as tk
from tkinter import messagebox
import random
import mysql.connector
from hashlib import sha256
import time

# 데이터베이스 연결 정보
# DB_CONFIG = {
#     "host": "127.0.0.1",
#     "port": 3306,
#     "user": "root",
#     "password": "sk0716kyh!",
#     "database": "tuQuizGame",
# }

DB_CONFIG = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "root",
    "database": "tuQuizGame",
}

def hash_password(password):
    return sha256(password.encode()).hexdigest()

def register_user(username, password, nickname):
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM user WHERE email = %s", (username,))
        if cursor.fetchone():
            messagebox.showerror("회원가입 오류", "이미 존재하는 아이디입니다.")
            return

        password_hash = hash_password(password)
        query = "INSERT INTO user (email, Pw, name) VALUES (%s, %s, %s)"
        cursor.execute(query, (username, password_hash, nickname))
        connection.commit()
        messagebox.showinfo("회원가입 성공", "회원가입이 완료되었습니다! 로그인하세요.")
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
    finally:
        if 'connection' in locals():
            connection.close()


def login_user(username, password):
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        cursor.execute("SELECT name, Pw FROM user WHERE email = %s", (username,))
        result = cursor.fetchone()

        if result:
            stored_nickname, stored_password_hash = result
            if stored_password_hash == hash_password(password):
                messagebox.showinfo("로그인 성공", f"{stored_nickname}님, 환영합니다!")
                return True
            else:
                messagebox.showerror("로그인 실패", "비밀번호가 잘못되었습니다.")
        else:
            messagebox.showerror("로그인 실패", "아이디가 존재하지 않습니다.")
        return False
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        return False
    finally:
        if 'connection' in locals():
            connection.close()

def get_questions_from_db(category=None):
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        if category:
            cursor.execute(
                "SELECT question, answer_a, answer_b, answer_c, answer_d, Correct , name FROM questions WHERE name = %s",
                (category,))
            print("why")
        else:
            cursor.execute("SELECT question, answer_a, answer_b, answer_c, answer_d, Correct , name FROM questions")

        rows = cursor.fetchall()

        questions = []
        for row in rows:
            question = {
                "question": row[0],
                "options": [f"A) {row[1]}", f"B) {row[2]}", f"C) {row[3]}", f"D) {row[4]}"],
                "answer": row[5]
            }
            questions.append(question)

        return questions
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        return []
    finally:
        if 'connection' in locals():
            connection.close()


def add_question_to_db(question, answer_a, answer_b, answer_c, answer_d, correct, name, user_id):
    try:
        # conn = mysql.connector.connect(
        #     host="127.0.0.1",
        #     user="root",
        #     password="sk0716kyh!",
        #     database="tuQuizGame"
        # )

        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="root",
            database="tuQuizGame"
        )
        cursor = conn.cursor()

        query = '''
            INSERT INTO questions (question, answer_a, answer_b, answer_c, answer_d, correct, name, user_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        '''
        data = (question, answer_a, answer_b, answer_c, answer_d, correct, name, user_id)
        cursor.execute(query, data)

        conn.commit()
        conn.close()

        messagebox.showinfo("문제 추가 완료", f"문제가 성공적으로 추가되었습니다!\n\n질문: {question}\n옵션 A: {answer_a}\n옵션 B: {answer_b}\n옵션 C: {answer_c}\n옵션 D: {answer_d}\n정답: {correct}\n카테고리: {name}")

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"에러가 발생했습니다: {err}")
        print(f"Database Error: {err}")


def quiz_game(category=None):
    print("데이터는 가져옴")
    questions = get_questions_from_db(category)
    print("가져왔는데 안띄워짐")
    if not questions:
        messagebox.showerror("Error", "문제를 불러오지 못했습니다. 데이터베이스를 확인하세요.")
        return

    random.shuffle(questions)

    def next_question():
        nonlocal question_index, score
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        if question_index < len(questions):
            q = questions[question_index]
            question_label.config(text=f"문제 {question_index + 1}: {q['question']}")
            for i, option in enumerate(q["options"]):
                option_buttons[i].config(text=option, state=tk.NORMAL)
        else:
            end_time = time.time()
            total_time = end_time - start_time
            if score == len(questions):
                messagebox.showinfo("퀴즈 종료", f"축하합니다! 모든 문제를 맞췄습니다!\n"
                                             f"최종 점수: {score}/{len(questions)}\n"
                                             f"소요 시간: {total_time:.2f}초")
            else:
                messagebox.showinfo("퀴즈 종료", f"퀴즈가 끝났습니다.\n"
                                             f"최종 점수: {score}/{len(questions)}")

            try:
                query = "INSERT INTO record (name, time, score) VALUES (%s, %s, %s)"
                cursor.execute(query, (category, total_time, score))
                connection.commit()
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error: {err}")
                print(f"Database Error: {err}")

            connection.close()
            window.destroy()

    def check_answer(selected_option):
        nonlocal question_index, score
        correct_answer = questions[question_index]["answer"]
        if selected_option == correct_answer:
            score += 1
            messagebox.showinfo("정답", "정답입니다!")
        else:
            messagebox.showinfo("오답", f"오답입니다. 정답은 {correct_answer}입니다.")
        question_index += 1
        next_question()

    window = tk.Tk()
    window.title("퀴즈 게임")
    window.geometry("600x500")
    window.resizable(False, False)

    question_index = 0
    score = 0
    start_time = time.time()

    question_label = tk.Label(window, text="", wraplength=550, justify="center", font=("Arial", 16))
    question_label.pack(pady=20)

    option_buttons = []
    for i in range(4):
        btn = tk.Button(window, text="", font=("Arial", 14), width=25,
                        command=lambda opt=chr(65 + i): check_answer(opt))
        btn.pack(pady=10)
        option_buttons.append(btn)

    next_question()

    window.mainloop()


def login_screen():
    def login_action():
        username = username_entry.get()
        password = password_entry.get()

        if not username or not password:
            messagebox.showerror("Login Error", "아이디와 비밀번호를 모두 입력하세요.")
            return

        if login_user(username, password):
            login_window.quit()
            create_game_or_add_question_screen()

    login_window = tk.Tk()
    login_window.title("로그인")
    login_window.geometry("400x300")
    login_window.resizable(False, False)

    tk.Label(login_window, text="아이디:", font=("Arial", 12)).grid(row=0, column=0, pady=10, padx=10, sticky="e")
    username_entry = tk.Entry(login_window, font=("Arial", 12), width=25)
    username_entry.grid(row=0, column=1, pady=10, padx=10)

    tk.Label(login_window, text="비밀번호:", font=("Arial", 12)).grid(row=1, column=0, pady=10, padx=10, sticky="e")
    password_entry = tk.Entry(login_window, show="*", font=("Arial", 12), width=25)
    password_entry.grid(row=1, column=1, pady=10, padx=10)

    login_button = tk.Button(login_window, text="로그인", command=login_action, font=("Arial", 12), width=20)
    login_button.grid(row=2, column=0, columnspan=2, pady=15)

    tk.Button(login_window, text="회원가입", command=lambda: register_screen(login_window),
              font=("Arial", 12), width=20).grid(row=3, column=0, columnspan=2, pady=10)

    login_window.mainloop()

def create_game_or_add_question_screen():
    window = tk.Tk()
    window.title("게임 또는 문제 추가")
    window.geometry("500x400")
    window.resizable(False, False)

    tk.Label(window, text="원하는 작업을 선택하세요", font=("Arial", 14)).pack(pady=20)

    tk.Button(window, text="게임 시작", command=lambda: select_category_for_game(window),
              font=("Arial", 12), width=20).pack(pady=10)
    tk.Button(window, text="문제 추가", command=create_question_interface,
              font=("Arial", 12), width=20).pack(pady=10)
    tk.Button(window, text="기록 보기", command=match_info,
              font=("Arial", 12), width=20).pack(pady=10)

    window.mainloop()


def match_info():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        cursor.execute("SELECT name , time, score FROM record ")
        records = cursor.fetchall()

        if records:
            record_text = "종류         소요 시간(초)        점수\n"
            record_text += "-" * 50 + "\n"
            for record in records:
                record_text += f"{record[0]}              {float(record[1]):.2f}               {record[2]}\n"

            messagebox.showinfo("기록 보기", record_text)
        else:
            messagebox.showinfo("기록 보기", "기록이 없습니다.")

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        print(f"Database Error: {err}")
    finally:
        if 'connection' in locals():
            connection.close()

def create_question_interface():
    def submit_question():
        question = question_entry.get()
        answer_a = answer_a_entry.get()
        answer_b = answer_b_entry.get()
        answer_c = answer_c_entry.get()
        answer_d = answer_d_entry.get()
        correct = correct_entry.get().upper()
        name = category_var.get()
        user_id = user_id_entry.get()

        if not (question and answer_a and answer_b and answer_c and answer_d and correct and name and user_id):
            messagebox.showerror("Error", "모든 필드를 입력해야 합니다.")
            return

        if correct not in ["A", "B", "C", "D"]:
            messagebox.showerror("Error", "정답은 A, B, C, D 중 하나여야 합니다.")
            return

        add_question_to_db(question, answer_a, answer_b, answer_c, answer_d, correct, name, user_id)

    window = tk.Tk()
    window.title("퀴즈 추가")

    tk.Label(window, text="문제:").grid(row=0, column=0, pady=5)
    question_entry = tk.Entry(window, width=50)
    question_entry.grid(row=0, column=1, pady=5)

    tk.Label(window, text="옵션 A:").grid(row=1, column=0, pady=5)
    answer_a_entry = tk.Entry(window, width=50)
    answer_a_entry.grid(row=1, column=1, pady=5)

    tk.Label(window, text="옵션 B:").grid(row=2, column=0, pady=5)
    answer_b_entry = tk.Entry(window, width=50)
    answer_b_entry.grid(row=2, column=1, pady=5)

    tk.Label(window, text="옵션 C:").grid(row=3, column=0, pady=5)
    answer_c_entry = tk.Entry(window, width=50)
    answer_c_entry.grid(row=3, column=1, pady=5)

    tk.Label(window, text="옵션 D:").grid(row=4, column=0, pady=5)
    answer_d_entry = tk.Entry(window, width=50)
    answer_d_entry.grid(row=4, column=1, pady=5)

    tk.Label(window, text="정답 (A/B/C/D):").grid(row=5, column=0, pady=5)
    correct_entry = tk.Entry(window, width=10)
    correct_entry.grid(row=5, column=1, pady=5)

    tk.Label(window, text="카테고리:").grid(row=6, column=0, pady=5)
    category_var = tk.StringVar(window)
    category_var.set("상식")  # 기본값 설정
    category_menu = tk.OptionMenu(window, category_var, "상식", "역사", "과학")
    category_menu.grid(row=6, column=1, pady=5)

    tk.Label(window, text="사용자 ID:").grid(row=7, column=0, pady=5)
    user_id_entry = tk.Entry(window, width=10)
    user_id_entry.grid(row=7, column=1, pady=5)

    submit_button = tk.Button(window, text="문제 추가", command=submit_question)
    submit_button.grid(row=8, column=0, columnspan=2, pady=10)

    window.mainloop()

def select_category_for_game(prev_window=None):
    if prev_window:
        prev_window.quit()

    def start_quiz_with_category():
        category = category_var.get()
        quiz_game(category)

    window = tk.Tk()
    window.title("카테고리 선택")
    window.geometry("400x200")
    window.resizable(False, False)

    tk.Label(window, text="카테고리 선택", font=("Arial", 14)).pack(pady=20)

    category_var = tk.StringVar(window)
    category_var.set("상식")
    category_menu = tk.OptionMenu(window, category_var, "상식", "역사", "과학")
    category_menu.pack(pady=10)

    start_button = tk.Button(window, text="퀴즈 시작", command=start_quiz_with_category,
                             font=("Arial", 12), width=20)
    start_button.pack(pady=20)

    window.mainloop()

def register_screen(prev_window=None):
    if prev_window:
        prev_window.quit()

    def register_action():
        username = username_entry.get()
        password = password_entry.get()
        nickname = nickname_entry.get()

        if not username or not password or not nickname:
            messagebox.showerror("회원가입 오류", "모든 필드를 입력하세요.")
            return

        register_user(username, password, nickname)

    register_window = tk.Tk()
    register_window.title("회원가입")
    register_window.geometry("400x350")
    register_window.resizable(False, False)

    tk.Label(register_window, text="아이디:", font=("Arial", 12)).grid(row=0, column=0, pady=10, padx=10, sticky="e")
    username_entry = tk.Entry(register_window, font=("Arial", 12), width=25)
    username_entry.grid(row=0, column=1, pady=10, padx=10)

    tk.Label(register_window, text="비밀번호:", font=("Arial", 12)).grid(row=1, column=0, pady=10, padx=10, sticky="e")
    password_entry = tk.Entry(register_window, show="*", font=("Arial", 12), width=25)
    password_entry.grid(row=1, column=1, pady=10, padx=10)

    tk.Label(register_window, text="닉네임:", font=("Arial", 12)).grid(row=2, column=0, pady=10, padx=10, sticky="e")
    nickname_entry = tk.Entry(register_window, font=("Arial", 12), width=25)
    nickname_entry.grid(row=2, column=1, pady=10, padx=10)

    register_button = tk.Button(register_window, text="회원가입", command=register_action,
                                 font=("Arial", 12), width=20)
    register_button.grid(row=3, column=0, columnspan=2, pady=20)

    register_window.mainloop()


if __name__ == "__main__":
    login_screen()