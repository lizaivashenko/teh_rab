import tkinter as tk
import webbrowser

def open_yandex():
    query = entry.get()
    if query:
        query_encoded = query.replace(" ", "+")
        search_url = f'https://yandex.ru/images/search?text={query_encoded}'
        webbrowser.open(search_url)

root = tk.Tk()
root.title("Поиск изображений на Яндекс")

label = tk.Label(root, text="Введите запрос для поиска картинки:")
label.pack(pady=5)

entry = tk.Entry(root, width=50)
entry.pack(pady=5)

search_button = tk.Button(root, text="Найти", command=open_yandex)
search_button.pack(pady=5)

root.mainloop()