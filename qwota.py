import tkinter as tk
from tkinter import scrolledtext, colorchooser, messagebox


# Создание основного класса мессенджера
class QwotaMessenger:
    def init(self, root):
        self.root = root
        self.root.title("Qwota Messenger")
        self.root.geometry("400x500")

        # Список для хранения сообщений
        self.messages = []

        # Создание области для отображения сообщений
        self.chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, state='disabled', height=20, width=50)
        self.chat_area.pack(pady=10)

        # Поле для ввода нового сообщения
        self.message_entry = tk.Entry(root, width=40)
        self.message_entry.pack(side=tk.LEFT, padx=10)

        # Кнопка для отправки сообщения
        self.send_button = tk.Button(root, text="Отправить", command=self.send_message)
        self.send_button.pack(side=tk.RIGHT, padx=10)

        # Привязка клавиши Enter к отправке сообщения 
        self.message_entry.bind("<Return>", lambda event: self.send_message())

        # Метод для отправки сообщения
    def send_message(self):
        message = self.message_entry.get()
        if message.strip():  # Проверка, что сообщение не пустое
            self.messages.append(message)  # Добавление сообщения в список
            self.update_chat_area()  # Обновление области чата
            self.message_entry.delete(0, tk.END)  # Очистка поля ввода

    # Метод для обновления области чата
    def update_chat_area(self):
        self.chat_area.config(state='normal')  # Разблокировка текстового поля
        self.chat_area.delete(1.0, tk.END)  # Очистка текущего содержимого
        for msg in self.messages:
            self.chat_area.insert(tk.END, f"> {msg}\n")  # Добавление сообщений
        self.chat_area.config(state='disabled')  # Блокировка текстового поля 
        self.chat_area.yview(tk.END)  # Прокрутка вниз

    # Метод для очистки чата
    def clear_chat(self):
        self.messages.clear()  # Очистка списка сообщений
        self.update_chat_area()  # Обновление чата

    # Метод для изменения цвета фона
    def izmenit_color(self):
        color = colorchooser.askcolor(title="Выберите цвет фона")
        if color[1]:  # Если выбранный цвет не None, изменяем фон
            self.chat_area.config(bg=color[1])  # Устанавливаем новый цвет фона


# Запуск приложения
if __name__ == "main":
    root = tk.Tk()
    app = QwotaMessenger(root)
    root.mainloop()