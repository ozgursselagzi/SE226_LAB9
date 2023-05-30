import mysql.connector
from tkinter import Tk, Button, StringVar, OptionMenu, messagebox, Entry, Label, Text

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Ozgur.33",
    database="se226_LAB9"
)

cursor = db.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS marvel_movies (
        ID INT PRIMARY KEY,
        MOVIE VARCHAR(255),
        DATE DATE,
        MCU_PHASE VARCHAR(10)
    )
""")

with open("Marvel.txt", "r") as file:
    for line in file:
        data = line.strip().split("\t")
        if len(data) == 4:
            movie_id = int(data[0].split()[0])
            movie_name = " ".join(data[0].split()[1:])
            release_date = data[1]
            mcu_phase = data[2]
            cursor.execute("""
                INSERT INTO marvel_movies (ID, MOVIE, DATE, MCU_PHASE)
                VALUES (%s, %s, STR_TO_DATE(%s, '%M%d,%Y'), %s)
            """, (movie_id, movie_name, release_date, mcu_phase))

db.commit()


def add_button_clicked():
    def ok_button_clicked():
        movie_id = int(entry.get())
        movie_name = entry2.get()
        release_date = entry3.get()
        mcu_phase = entry4.get()

        cursor.execute("""
            INSERT INTO marvel_movies (ID, MOVIE, DATE, MCU_PHASE)
            VALUES (%s, %s, STR_TO_DATE(%s, '%M%d,%Y'), %s)
        """, (movie_id, movie_name, release_date, mcu_phase))

        db.commit()
        messagebox.showinfo("Success", "Movie added successfully!")
        top.destroy()

    def cancel_button_clicked():
        top.destroy()

    top = Tk()
    top.geometry("300x200")

    label = Label(top, text="Add Movie")
    label.pack()

    label2 = Label(top, text="ID")
    label2.pack()
    entry = Entry(top)
    entry.pack()

    label3 = Label(top, text="Movie")
    label3.pack()
    entry2 = Entry(top)
    entry2.pack()

    label4 = Label(top, text="Date")
    label4.pack()
    entry3 = Entry(top)
    entry3.pack()

    label5 = Label(top, text="MCU Phase")
    label5.pack()
    entry4 = Entry(top)
    entry4.pack()

    ok_button = Button(top, text="Ok", command=ok_button_clicked)
    ok_button.pack()

    cancel_button = Button(top, text="Cancel", command=cancel_button_clicked)
    cancel_button.pack()

    top.mainloop()


def list_all_button_clicked():
    cursor.execute("SELECT * FROM marvel_movies")
    movies = cursor.fetchall()

    result_text.delete(1.0, "end")

    for movie in movies:
        result_text.insert("end", f"{movie}\n")


def list_all_movies():
    cursor.execute("SELECT MOVIE FROM marvel_movies")
    movies = cursor.fetchall()

    result_text.delete(1.0, "end")

    for movie in movies:
        result_text.insert("end", f"{movie[0]}\n")


def remove_the_incredible_hulk():
    cursor.execute("DELETE FROM marvel_movies WHERE MOVIE = 'TheIncredibleHulk'")
    db.commit()
    messagebox.showinfo("Success", "TheIncredibleHulk removed successfully!")


def list_phase_2_movies():
    cursor.execute("SELECT MOVIE FROM marvel_movies WHERE MCU_PHASE = 'Phase2'")
    movies = cursor.fetchall()

    result_text.delete(1.0, "end")

    for movie in movies:
        result_text.insert("end", f"{movie[0]}\n")


def fix_thor_ragnarok_date():
    cursor.execute(
        "UPDATE marvel_movies SET DATE = STR_TO_DATE('November3,2017', '%M%d,%Y') WHERE MOVIE = 'Thor:Ragnarok'")
    db.commit()
    messagebox.showinfo("Success", "Thor:Ragnarok date fixed successfully!")


root = Tk()
root.geometry("400x300")

selected_id = StringVar(root)
selected_id.set("Select ID")
id_dropdown = OptionMenu(root, selected_id, *range(1, 24))
id_dropdown.pack()

result_text = Text(root, height=10, width=40)
result_text.pack()

add_button = Button(root, text="Add", command=add_button_clicked)
add_button.pack()

list_all_button = Button(root, text="List All", command=list_all_button_clicked)
list_all_button.pack()

root.mainloop()
