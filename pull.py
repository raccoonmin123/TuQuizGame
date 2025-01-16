import tkinter as tk
from tkinter import messagebox
import random
import mysql.connector
from hashlib import sha256
import time

# window = tk.Tk()
# window.geometry("500x300")

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
    "password": "sk0716kyh!",
    "database": "tuQuizGame",
}


# 비밀번호 해싱 함수
def hash_password(password):
    return sha256(password.encode()).hexdigest()


# 회원가입 기능
def register_user(username, password, nickname):
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        # 아이디 중복 체크
        cursor.execute("SELECT * FROM user WHERE email = %s", (username,))
        if cursor.fetchone():
            messagebox.showerror("회원가입 오류", "이미 존재하는 아이디입니다.")
            return

        # 새 사용자 추가
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

        # 아이디로 닉네임과 비밀번호 해시값을 조회
        cursor.execute("SELECT name, Pw FROM user WHERE email = %s", (username,))
        result = cursor.fetchone()

        if result:
            stored_nickname, stored_password_hash = result
            # 비밀번호 확인
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


# 문제를 데이터베이스에서 가져오는 함수 (카테고리별로 필터링)
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
            print("씨발")

        return questions
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        return []
    finally:
        if 'connection' in locals():
            connection.close()


# MySQL 데이터베이스 연결 및 문제 추가 함수
def add_question_to_db(question, answer_a, answer_b, answer_c, answer_d, correct, name, user_id):
    try:
        # MySQL 데이터베이스 연결
        conn = mysql.connector.connect(
            host="127.0.0.1",  # 데이터베이스 호스트
            user="root",       # 사용자명
            password="sk0716kyh!",  # 비밀번호
            database="tuQuizGame"    # 데이터베이스 이름
        )
        cursor = conn.cursor()

        # 데이터베이스에 문제 추가
        query = '''
            INSERT INTO questions (question, answer_a, answer_b, answer_c, answer_d, correct, name, user_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        '''
        data = (question, answer_a, answer_b, answer_c, answer_d, correct, name, user_id)
        cursor.execute(query, data)

        conn.commit()  # 변경사항 저장
        conn.close()   # 연결 종료

        # 문제 추가가 완료되었을 때 GUI에 표시할 메시지
        messagebox.showinfo("문제 추가 완료", f"문제가 성공적으로 추가되었습니다!\n\n질문: {question}\n옵션 A: {answer_a}\n옵션 B: {answer_b}\n옵션 C: {answer_c}\n옵션 D: {answer_d}\n정답: {correct}\n카테고리: {name}")

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"에러가 발생했습니다: {err}")
        print(f"Database Error: {err}")


# def save_quiz_result_to_db(username, score, total_time):
#     try:
#         connection = mysql.connector.connect(**DB_CONFIG)
#         cursor = connection.cursor()
#
#         # 사용자 ID 찾기
#         cursor.execute("SELECT user_id FROM users WHERE email = %s", (username,))
#         user_id = cursor.fetchone()
#
#         if not user_id:
#             messagebox.showerror("Error", "사용자를 찾을 수 없습니다.")
#             return
#
#         user_id = user_id[0]  # 첫 번째 값이 user_id입니다.
#         current_time = time.strftime('%Y-%m-%d %H:%M:%S')  # 현재 날짜 및 시간
#
#         query = """
#         INSERT INTO quiz_history (user_id, score, total_time, quiz_date)
#         VALUES (%s, %s, %s, %s)
#         """
#         cursor.execute(query, (user_id, score, total_time, current_time))
#         connection.commit()
#         messagebox.showinfo("성공", "퀴즈 기록이 저장되었습니다.")
#
#     except mysql.connector.Error as err:
#         messagebox.showerror("Database Error", f"Error: {err}")
#     finally:
#         if 'connection' in locals():
#             connection.close()

# 퀴즈 기록을 조회하는 함수
# def view_quiz_history(username):
#     try:
#         connection = mysql.connector.connect(**DB_CONFIG)
#         cursor = connection.cursor()
#
#         # 사용자 ID 찾기
#         cursor.execute("SELECT user_id FROM users WHERE email = %s", (username,))
#         user_id = cursor.fetchone()
#
#         if not user_id:
#             messagebox.showerror("Error", "사용자를 찾을 수 없습니다.")
#             return
#
#         user_id = user_id[0]
#
#         query = """
#         SELECT score, total_time, quiz_date FROM quiz_history
#         WHERE user_id = %s
#         ORDER BY quiz_date DESC
#         """
#         cursor.execute(query, (user_id,))
#         rows = cursor.fetchall()
#
#         if rows:
#             # 기록을 보여주는 창
#             history_window = tk.Tk()
#             history_window.title(f"{username}님의 퀴즈 기록")
#             history_window.geometry("600x400")
#
#             history_label = tk.Label(history_window, text=f"{username}님의 퀴즈 기록", font=("Arial", 14))
#             history_label.pack(pady=20)
#
#             history_text = tk.Text(history_window, width=70, height=15)
#             history_text.pack(pady=10)
#             history_text.insert(tk.END, "점수  |  소요 시간  |  날짜\n")
#             history_text.insert(tk.END, "-" * 60 + "\n")
#
#             for row in rows:
#                 history_text.insert(tk.END, f"{row[0]}  |  {row[1]:.2f}초  |  {row[2]}\n")
#
#             close_button = tk.Button(history_window, text="닫기", command=history_window.quit, font=("Arial", 12))
#             close_button.pack(pady=20)
#
#             history_window.mainloop()
#         else:
#             messagebox.showinfo("기록 없음", "현재 퀴즈 기록이 없습니다.")
#     except mysql.connector.Error as err:
#         messagebox.showerror("Database Error", f"Error: {err}")
#     finally:
#         if 'connection' in locals():
#             connection.close()

# 퀴즈 게임 실행 함수 (카테고리 선택)

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
        if question_index < len(questions):
            q = questions[question_index]
            question_label.config(text=f"문제 {question_index + 1}: {q['question']}")
            for i, option in enumerate(q["options"]):
                option_buttons[i].config(text=option, state=tk.NORMAL)
        else:
            end_time = time.time()  # 종료 시간 기록
            total_time = end_time - start_time  # 소요 시간 계산
            if score == len(questions):  # 모든 문제를 맞췄을 때만 시간 표시
                messagebox.showinfo("퀴즈 종료", f"축하합니다! 모든 문제를 맞췄습니다!\n"
                                               f"최종 점수: {score}/{len(questions)}\n"
                                               f"소요 시간: {total_time:.2f}초")
            else:
                messagebox.showinfo("퀴즈 종료", f"퀴즈가 끝났습니다.\n"
                                               f"최종 점수: {score}/{len(questions)}")
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
    window.geometry("600x500")  # 창 크기 설정
    window.resizable(False, False)

    question_index = 0
    score = 0
    start_time = time.time()  # 시작 시간 기록

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


# 로그인 화면
def login_screen():
    def login_action():
        username = username_entry.get()
        password = password_entry.get()

        if not username or not password:
            messagebox.showerror("Login Error", "아이디와 비밀번호를 모두 입력하세요.")
            return

        if login_user(username, password):
            login_window.quit()  # 로그인 창을 종료
            create_game_or_add_question_screen()

    login_window = tk.Tk()
    login_window.title("로그인")
    login_window.geometry("400x300")  # 창 크기 설정
    login_window.resizable(False, False)  # 창 크기 조정 비활성화

    # 아이디와 비밀번호 입력 UI
    tk.Label(login_window, text="아이디:", font=("Arial", 12)).grid(row=0, column=0, pady=10, padx=10, sticky="e")
    username_entry = tk.Entry(login_window, font=("Arial", 12), width=25)
    username_entry.grid(row=0, column=1, pady=10, padx=10)

    tk.Label(login_window, text="비밀번호:", font=("Arial", 12)).grid(row=1, column=0, pady=10, padx=10, sticky="e")
    password_entry = tk.Entry(login_window, show="*", font=("Arial", 12), width=25)
    password_entry.grid(row=1, column=1, pady=10, padx=10)

    # 로그인 및 회원가입 버튼
    login_button = tk.Button(login_window, text="로그인", command=login_action, font=("Arial", 12), width=20)
    login_button.grid(row=2, column=0, columnspan=2, pady=15)

    tk.Button(login_window, text="회원가입", command=lambda: register_screen(login_window),
              font=("Arial", 12), width=20).grid(row=3, column=0, columnspan=2, pady=10)

    login_window.mainloop()


# 게임 시작 또는 문제 추가 선택 화면
def create_game_or_add_question_screen():
    window = tk.Tk()
    window.title("게임 또는 문제 추가")
    window.geometry("400x200")  # 창 크기 설정
    window.resizable(False, False)  # 창 크기 조정 비활성화

    tk.Label(window, text="원하는 작업을 선택하세요", font=("Arial", 14)).pack(pady=20)

    tk.Button(window, text="게임 시작", command=lambda: select_category_for_game(window),
              font=("Arial", 12), width=20).pack(pady=10)
    tk.Button(window, text="문제 추가", command=create_question_interface,
              font=("Arial", 12), width=20).pack(pady=10)

    window.mainloop()

# 문제 추가 인터페이스 함수 (카테고리 선택 추가)
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

        # 문제 추가
        add_question_to_db(question, answer_a, answer_b, answer_c, answer_d, correct, name, user_id)

    window = tk.Tk()
    window.title("퀴즈 추가")

    # 문제 항목 입력 UI
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



# 카테고리 선택 후 퀴즈 시작
def select_category_for_game(prev_window=None):
    if prev_window:
        prev_window.quit()  # 이전 창을 종료

    def start_quiz_with_category():
        category = category_var.get()
        quiz_game(category)

    window = tk.Tk()
    window.title("카테고리 선택")
    window.geometry("400x200")  # 창 크기 설정
    window.resizable(False, False)  # 창 크기 조정 비활성화

    tk.Label(window, text="카테고리 선택", font=("Arial", 14)).pack(pady=20)

    category_var = tk.StringVar(window)
    category_var.set("상식")  # 기본값 설정
    category_menu = tk.OptionMenu(window, category_var, "상식", "역사", "과학")
    category_menu.pack(pady=10)

    start_button = tk.Button(window, text="퀴즈 시작", command=start_quiz_with_category,
                             font=("Arial", 12), width=20)
    start_button.pack(pady=20)

    window.mainloop()


# 회원가입 화면
def register_screen(prev_window=None):
    if prev_window:
        prev_window.quit()  # 이전 창을 종료

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
    register_window.geometry("400x350")  # 창 크기 설정
    register_window.resizable(False, False)  # 창 크기 조정 비활성화

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