import pymysql

# root = tk.Tk()
# root.title("TuQuizGame")
# root.geometry("800x600")
# label = tk.Label(root, text="Hello World!")


conn = pymysql.connect(host='127.0.0.1', port = 3306 , user='root', password='root', db='tuQuizGame', charset='utf8')

cursor = conn.cursor()
sql = "SELECT * FROM user"
cursor.execute(sql)

result = cursor.fetchall()
for res in result:
    print(res)

# root.mainloop()