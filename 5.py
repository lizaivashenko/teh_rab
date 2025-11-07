import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class PunktVidachiApp:
    def __init__(self, master):
        self.master = master
        master.title("Пункт выдачи заказов")
        master.geometry("450x350")
        
        self.button_colors = {
            'search': {'bg': "#68666f", 'fg': "#000000", 'active_bg': "#68666f", 'active_fg': "#68666f"},
            'vydat': {'bg': "#4eb019", 'fg': "#000000", 'active_bg': "#4eb019", 'active_fg': "#4eb019"},
            'vernut': {'bg': "#e74c3c", 'fg': "#ffffff", 'active_bg': "#c0392b", 'active_fg': "#ffffff"},
            'qr': {'bg': "#1e90ff", 'fg': "#ffffff", 'active_bg': "#63b8ff", 'active_fg': "#ffffff"},
        }
        
        self.set_dark_theme()

        self.company_label = ttk.Label(master, text="🎁 GoBox🚀", style="Company.TLabel")
        self.company_label.pack(pady=10)

        self.search_frame = ttk.Frame(master)
        self.search_frame.pack(pady=5)

        self.order_code_label = ttk.Label(self.search_frame, text="Код заказа:", style="Dark.TLabel")
        self.order_code_label.pack(side=tk.LEFT, padx=(0, 5))

        self.order_code_entry = ttk.Entry(self.search_frame, style="Dark.TEntry", width=20)
        self.order_code_entry.pack(side=tk.LEFT)

        search_colors = self.button_colors['search']
        self.search_button = tk.Button(self.search_frame, text="🔎", 
                                     bg=search_colors['bg'], fg=search_colors['fg'],
                                     activebackground=search_colors['active_bg'],
                                     activeforeground=search_colors['active_fg'],
                                     font=("Arial", 10, "bold"),
                                     relief="raised", bd=1,
                                     width=4,
                                     command=lambda: self.show_order_info(self.order_code_entry.get()))
        self.search_button.pack(side=tk.LEFT, padx=(5, 5))

        qr_colors = self.button_colors['qr']
        self.qr_button = tk.Button(self.search_frame, text="QR", 
                                 bg=qr_colors['bg'], fg=qr_colors['fg'],
                                 activebackground=qr_colors['active_bg'],
                                 activeforeground=qr_colors['active_fg'],
                                 font=("Arial", 10, "bold"),
                                 relief="raised", bd=1,
                                 width=6,
                                 command=self.show_qr_message)
        self.qr_button.pack(side=tk.LEFT, padx=(0, 0))

        self.orders_label = ttk.Label(master, text="Информация о заказе:", style="Dark.TLabel")
        self.orders_label.pack(pady=(10, 0))

        self.orders_text = tk.Text(master, height=5, width=50, wrap=tk.WORD, state=tk.DISABLED,
                                  bg="#2b2b2b", fg="#ffffff", insertbackground="#ffffff",
                                  selectbackground="#404040", selectforeground="#ffffff")
        self.orders_text.pack(pady=5)

        self.buttons_frame = ttk.Frame(master)
        self.buttons_frame.pack(pady=15)

        vydat_colors = self.button_colors['vydat']
        self.vydat_button = tk.Button(self.buttons_frame, text="Выдать ✅", 
                                    bg=vydat_colors['bg'], fg=vydat_colors['fg'],
                                    activebackground=vydat_colors['active_bg'],
                                    activeforeground=vydat_colors['active_fg'],
                                    font=("Arial", 12, "bold"),
                                    relief="raised", bd=2,
                                    width=10,
                                    height=2,
                                    command=self.vydat_zakaz)
        self.vydat_button.pack(side=tk.LEFT, padx=20)

        vernut_colors = self.button_colors['vernut']
        self.vernut_button = tk.Button(self.buttons_frame, text="Вернуть ↩️", 
                                     bg=vernut_colors['bg'], fg=vernut_colors['fg'],
                                     activebackground=vernut_colors['active_bg'],
                                     activeforeground=vernut_colors['active_fg'],
                                     font=("Arial", 12, "bold"),
                                     relief="raised", bd=2,
                                     width=10,
                                     height=2,
                                     command=self.vernut_zakaz)
        self.vernut_button.pack(side=tk.LEFT, padx=20)

        self.zakazy = {
            "12345": "Заказ №12345: Ячейка №45 Телефон: +7 (123) 456-7812, Товары: Смартфон Samsung Galaxy S23, Чехол силиконовый",
            "67890": "Заказ №67890: Ячейка №12 Телефон: +7 (234) 567-8934, Товары: Наушники AirPods Pro, Кабель Lightning",
            "54321": "Заказ №54321: Ячейка №67 Телефон: +7 (345) 678-9056, Товары: Сумка для ноутбука",
            "12346": "Заказ №12346: Ячейка №23 Телефон: +7 (905) 615-0112, Товары: Умные часы Apple Watch, Зарядное устройство",
            "12347": "Заказ №12347: Ячейка №89 Телефон: +7 (903) 833-5394, Товары: Планшет iPad Air, Стилус Apple Pencil",
            "12348": "Заказ №12348: Ячейка №34 Телефон: +7 (479) 203-6547, Товары: Фитнес-браслет Xiaomi, Спортивный ремешок",
            "12349": "Заказ №12349: Ячейка №56 Телефон: +7 (303) 999-9999, Товары: Игровая консоль PlayStation 5, Игра Spider-Man 2, Когтеточка",
            "12340": "Заказ №12340: Ячейка №78 Телефон: +7 (654) 002-5945, Товары: Электронная книга PocketBook, Обложка для книги",
            "23456": "Заказ №23456: Ячейка №15 Телефон: +7 (784) 481-0214, Товары: Монитор Dell 27', Кронштейн для монитора",
            "23457": "Заказ №23457: Ячейка №42 Телефон: +7 (155) 626-3313, Товары: Клавиатура механическая, Компьютерная мышь, Набор полотенец",
            "23458": "Заказ №23458: Ячейка №91 Телефон: +7 (745) 451-3184, Товары: Внешний жесткий диск 1ТБ, Чехол для диска",
            "23459": "Заказ №23459: Ячейка №33 Телефон: +7 (715) 051-3487, Товары: Велосипент горный, Шлем защитный",
            "23450": "Заказ №23450: Ячейка №64 Телефон: +7 (111) 241-0548, Товары: Кроссовки беговые, Спортивные носки",
            "34567": "Заказ №34567: Ячейка №27 Телефон: +7 (222) 352-1657, Товары: Кофеварка автоматическая, Зерна кофе",
            "34568": "Заказ №34568: Ячейка №59 Телефон: +7 (333) 463-2768, Товары: Кухонный нож шеф-повара, Точилка для ножей",
            "34569": "Заказ №34569: Ячейка №81 Телефон: +7 (444) 574-3879, Товары: Набор постельного белья, Подушка ортопедическая",
            "34570": "Заказ №34570: Ячейка №16 Телефон: +7 (555) 685-4980, Товары: Детский конструктор LEGO, Книга сказок",
            "34571": "Заказ №34571: Ячейка №73 Телефон: +7 (666) 796-5091, Товары: Краска для волос, Бальзам-ополаскиватель",
            "45678": "Заказ №45678: Ячейка №48 Телефон: +7 (777) 807-6102, Товары: Мольберт художественный",
            "45679": "Заказ №45679: Ячейка №95 Телефон: +7 (888) 918-7213, Товары: Гитара акустическая, Чехол для гитары",
            "45680": "Заказ №45680: Ячейка №22 Телефон: +7 (999) 029-8324, Товары: Палатка туристическая, Спальный мешок, Набор масляных красок",
            "45681": "Заказ №45681: Ячейка №69 Телефон: +7 (101) 130-9435, Товары: Набор посуды керамической, Скатерть",
            "56789": "Заказ №56789: Ячейка №37 Телефон: +7 (202) 241-0546, Товары: Удочка рыболовная, Набор приманок",
            "56790": "Заказ №56790: Ячейка №84 Телефон: +7 (303) 352-1657, Товары: Микроскоп детский, Набор препаратов",
            "56791": "Заказ №56791: Ячейка №51 Телефон: +7 (404) 463-2768, Товары: Швейная машинка, Набор ниток",
            "56792": "Заказ №56792: Ячейка №76 Телефон: +7 (505) 574-3879, Товары: Набор инструментов, Рабочие перчатки",
            "11111": "Заказ №11111: Ячейка №70 Телефон: +7 (407) 248-3741, Товары: Стол обеденный",
        }

    def set_dark_theme(self):
        bg_color = "#1e1e1e"
        fg_color = "#B3AE1D"
        accent_color = "#B3AE1D"
        entry_bg = "#000000"
        entry_fg = "#000000"
        
        self.master.configure(bg=bg_color)
        
        self.style = ttk.Style()
        
        self.style.configure(".", background=bg_color, foreground=fg_color)
        
        self.style.configure("Company.TLabel",
                           font=("Verdana", 20, "bold"),
                           foreground=accent_color,
                           background=bg_color)
        
        self.style.configure("Dark.TLabel",
                           background=bg_color,
                           foreground=fg_color,
                           font=("Arial", 10))
        
        self.style.configure("Dark.TEntry",
                           fieldbackground=entry_bg,
                           foreground=entry_fg,
                           insertcolor=entry_fg,
                           borderwidth=1,
                           relief="sunken")
        
        self.style.configure("TFrame", background=bg_color)

    def update_button_color(self, button_name, bg=None, fg=None, active_bg=None, active_fg=None):
        if bg:
            self.button_colors[button_name]['bg'] = bg
        if fg:
            self.button_colors[button_name]['fg'] = fg
        if active_bg:
            self.button_colors[button_name]['active_bg'] = active_bg
        if active_fg:
            self.button_colors[button_name]['active_fg'] = active_fg
            
        if button_name == 'search':
            button = self.search_button
        elif button_name == 'vydat':
            button = self.vydat_button
        elif button_name == 'vernut':
            button = self.vernut_button
        elif button_name == 'qr':
            button = self.qr_button
        else:
            return
            
        colors = self.button_colors[button_name]
        button.configure(
            bg=colors['bg'],
            fg=colors['fg'],
            activebackground=colors['active_bg'],
            activeforeground=colors['active_fg']
        )

    def update_all_buttons(self, bg=None, fg=None, active_bg=None, active_fg=None):
        for button_name in ['search', 'vydat', 'vernut', 'qr']:
            self.update_button_color(button_name, bg, fg, active_bg, active_fg)

    def show_qr_message(self):
        messagebox.showwarning("Оборудование не подключено", 
                             "У вас не подключено оборудование для сканирования QR-кодов.\n\n"
                             "Пожалуйста, подключите сканер QR-кодов и повторите попытку.")

    def vydat_zakaz(self):
        order_code = self.order_code_entry.get()
        if order_code in self.zakazy:
            order_info = self.zakazy[order_code]
            messagebox.showinfo("Заказ выдан", f"Заказ {order_code} выдан успешно.\n{order_info}")
            self.clear_order_info()
            self.order_code_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Ошибка", "Заказ с таким кодом не найден.")

    def vernut_zakaz(self):
        order_code = self.order_code_entry.get()
        if order_code in self.zakazy:
            order_info = self.zakazy[order_code]
            messagebox.showinfo("Заказ возвращен", f"Заказ {order_code} возвращен.\n{order_info}")
            self.clear_order_info()
            self.order_code_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Ошибка", "Заказ с таким кодом не найден.")

    def show_order_info(self, order_code):
        if order_code in self.zakazy:
            order_info = self.zakazy[order_code]
            display_info = order_info

            self.orders_text.config(state=tk.NORMAL)
            self.orders_text.delete("1.0", tk.END)
            self.orders_text.insert("1.0", display_info)
            self.orders_text.config(state=tk.DISABLED)
        else:
            self.clear_order_info()
            messagebox.showinfo("Заказ не найден", "Заказ с таким кодом не найден.")

    def clear_order_info(self):
        self.orders_text.config(state=tk.NORMAL)
        self.orders_text.delete("1.0", tk.END)
        self.orders_text.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = PunktVidachiApp(root)
    root.mainloop()