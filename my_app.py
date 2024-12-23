from flask import Flask, render_template_string
import pandas as pd
import sqlite3


### Задача 1.

conn = sqlite3.connect('my_presents.db')

cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    present TEXT NOT NULL,
    price INTEGER NOT NULL,
    status TEXT NOT NULL
)
''')

data = [
    ("Михаил Михайлович", "Носки", 1000, "Куплен"),
    ("Иван Иванович", "Бритва", 1500, "Не куплен"),
    ("Елена Васильевна", "Духи", 3000, "Куплен"),
    ("Семен Семенович", "Деньги", 3000, "Куплен"),
    ("Петр Петрович", "Коньяк", 5000, "Не куплен"),
    ("Мария Ивановна", "Платье", 5000, "Куплен"),
    ("Алексей Алексеевич", "Мышь", 3000, "Куплен"),
    ("Сергей Сергеевич", "Куртка", 6000, "Куплен"),
    ("Василиса Матвеевна", "Туфли", 4000, "Куплен"),
    ("Екатерина Владимировна", "Шуба", 50000, "Куплен")
]

cursor.execute('SELECT COUNT(*) FROM users')
count = cursor.fetchone()[0]

if count == 0:
        cursor.executemany('''
        INSERT INTO users (name, present, price, status) VALUES (?, ?, ?, ?)
        ''', data)

        conn.commit()

cursor.execute('SELECT * FROM users')
rows = cursor.fetchall()

print("Данные в таблице users:")
for row in rows:
    print(row)

conn.close()



###Задача 2.
app = Flask(__name__)

def get_data():
    conn = sqlite3.connect('my_presents.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users')
    rows = cursor.fetchall()
    conn.close()
    return rows


@app.route('/')
def index():
    data = get_data()

    html_template = '''
    <html>
        <head>
            <title>Таблица данных</title>
        </head>
        <body>
            <h1>Содержимое таблицы</h1>
            <table border="1">
                <tr>
                    <th>ID</th>
                    <th>Имя</th>
                    <th>Подарок</th>
                    <th>Цена</th>
                    <th>Статус</th>
                </tr>
                {% for row in data %}
                <tr>
                    <td>{{ row[0] }}</td>
                    <td>{{ row[1] }}</td>
                    <td>{{ row[2] }}</td>
                    <td>{{ row[3] }}</td>
                    <td>{{ row[4] }}</td>
                </tr>
                {% endfor %}
            </table>
        </body>
    </html>
    '''

    return render_template_string(html_template, data=data)


if __name__ == '__main__':
   app.run(debug=True)