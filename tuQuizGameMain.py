import tkinter as tk


# 퀴즈 게임 선택 함수
def start_quiz():
    selected_quiz = quiz_choice.get()

    if selected_quiz == "movie":
        print("영화 퀴즈를 선택하셨습니다!")
    elif selected_quiz == "game":
        print("게임 퀴즈를 선택하셨습니다!")
    elif selected_quiz == "food":
        print("음식 퀴즈를 선택하셨습니다!")
    else:
        print("퀴즈를 선택해주세요!")

window = tk.Tk()
window.title("Quiz Game")
window.geometry("400x300")

quiz_choice = tk.StringVar()

label_title = tk.Label(window, text="퀴즈를 선택하세요!", font=("Arial", 16))
label_title.pack(pady=20)

radio_movie = tk.Radiobutton(window, text="영화 퀴즈", variable=quiz_choice, value="movie")
radio_movie.pack()

radio_game = tk.Radiobutton(window, text="게임 퀴즈", variable=quiz_choice, value="game")
radio_game.pack()

radio_food = tk.Radiobutton(window, text="음식 퀴즈", variable=quiz_choice, value="food")
radio_food.pack()

button_start = tk.Button(window, text="퀴즈 시작", command=start_quiz)
button_start.pack(pady=20)

window.mainloop()
