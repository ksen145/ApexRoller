import tkinter as tk
import random
from tkinter import messagebox

class RollApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Apex Roller")
        self.root.geometry("450x550")
        self.root.config(bg="#f0f0f0")
        self.root.iconbitmap("assets/apex-logo.ico")
        
        # Переменные для отслеживания состояния
        self.is_first_roll = True
        self.previous_excluded = None
        self.all_names = []
        self.previous_selected = []
        
        # Создание GUI
        self.create_widgets()
    
    def create_widgets(self):
        # Заголовок
        title_label = tk.Label(
            self.root, 
            text="Apex Roller", 
            font=("Arial", 16, "bold"),
            bg="#f0f0f0",
            pady=10
        )
        title_label.pack()
        
        # Рамка для ввода имен
        input_frame = tk.LabelFrame(
            self.root, 
            text="Enter four names", 
            padx=15, 
            pady=15,
            bg="#f0f0f0",
            font=("Arial", 10)
        )
        input_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Поля для ввода имен
        self.name_entries = []
        for i in range(4):
            frame = tk.Frame(input_frame, bg="#f0f0f0")
            frame.pack(fill=tk.X, pady=5)
            
            tk.Label(
                frame, 
                text=f"Name {i+1}:",
                font=("Arial", 10),
                width=6,
                bg="#f0f0f0"
            ).pack(side=tk.LEFT, padx=(0, 5))
            
            entry = tk.Entry(frame, font=("Arial", 10))
            entry.pack(side=tk.LEFT, expand=True, fill=tk.X)
            self.name_entries.append(entry)
        
        # Фрейм для кнопок
        button_frame = tk.Frame(self.root, bg="#f0f0f0")
        button_frame.pack(pady=10)
        
        # Кнопка для ролла
        self.roll_button = tk.Button(
            button_frame, 
            text="Roll", 
            command=self.perform_roll,
            font=("Arial", 12, "bold"),
            bg="#4CAF50",
            fg="white",
            padx=20,
            pady=5,
            relief=tk.RAISED,
            borderwidth=2
        )
        self.roll_button.pack(side=tk.LEFT, padx=5)
        
        # Кнопка для сброса
        self.reset_button = tk.Button(
            button_frame, 
            text="Reset", 
            command=self.reset,
            font=("Arial", 12, "bold"),
            bg="#f44336",
            fg="white",
            padx=20,
            pady=5,
            relief=tk.RAISED,
            borderwidth=2
        )
        self.reset_button.pack(side=tk.LEFT, padx=5)
        
        # Фрейм для вывода результатов
        result_frame = tk.LabelFrame(
            self.root, 
            text="Results", 
            padx=15, 
            pady=15,
            bg="#f0f0f0",
            font=("Arial", 10)
        )
        result_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Текстовое поле для вывода результатов
        self.result_text = tk.Text(
            result_frame, 
            height=12, 
            width=40,
            font=("Arial", 11),
            bg="white",
            relief=tk.SUNKEN,
            borderwidth=2
        )
        self.result_text.pack(fill=tk.BOTH, expand=True)
        
        # Добавляем скроллбар
        scrollbar = tk.Scrollbar(self.result_text)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.result_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.result_text.yview)
        
        # Определение тегов форматирования
        self.result_text.tag_config("title", font=("Arial", 12, "bold"))
        self.result_text.tag_config("selected", font=("Arial", 11), foreground="green")
        self.result_text.tag_config("label", font=("Arial", 11, "bold"))
        self.result_text.tag_config("excluded", font=("Arial", 11), foreground="red")
        self.result_text.tag_config("note", font=("Arial", 10, "italic"), foreground="gray")
        
    def reset(self):
        # Сбрасываем состояние
        self.is_first_roll = True
        self.previous_excluded = None
        self.all_names = []
        self.previous_selected = []
        
        # Очищаем результаты
        self.result_text.delete(1.0, tk.END)
        
        # Разблокируем поля ввода
        for entry in self.name_entries:
            entry.config(state=tk.NORMAL)
            entry.delete(0, tk.END)
        
        # Фокус на первом поле
        self.name_entries[0].focus()
        
    def perform_roll(self):
        # Если первый ролл, проверяем и фиксируем имена
        if self.is_first_roll:
            # Получаем имена из полей ввода
            self.all_names = [entry.get().strip() for entry in self.name_entries]
            
            # Проверяем, что все имена введены
            if not all(self.all_names):
                messagebox.showerror("Error", "Please fill in all name fields.")
                return
            
            if len(set(self.all_names)) != 4:
                messagebox.showerror("Error", "All names must be different.")
                return
                
            # Блокируем поля ввода после первого ролла
            for entry in self.name_entries:
                entry.config(state=tk.DISABLED)
        
        # Логика для первого и последующих роллов
        if self.is_first_roll:
            # Первый ролл: выбираем 3 из 4 случайным образом
            selected_names = random.sample(self.all_names, 3)
            self.previous_selected = selected_names.copy()
            
            # Определяем, кто не был выбран
            self.previous_excluded = [name for name in self.all_names if name not in selected_names][0]
            
            self.is_first_roll = False
            roll_type = "First roll"
        else:
            # Для второго и последующих роллов:
            # 1. Прошлый исключенный должен быть включен
            # 2. Из оставшихся трех нужно исключить одного случайного
            
            # Выбираем случайное имя для исключения из тех, кто был выбран в прошлый раз
            new_excluded = random.choice(self.previous_selected)
            
            # Выбираем всех кроме нового исключенного
            selected_names = [name for name in self.all_names if name != new_excluded]
            
            # Обновляем для следующего ролла
            self.previous_excluded = new_excluded
            self.previous_selected = selected_names.copy()
            
            roll_type = "Repeat roll"
        
        # Отображаем результаты с цветным форматированием
        self.result_text.insert(tk.END, f"\n{roll_type}:\n", "title")
        
        for i, name in enumerate(selected_names, 1):
            self.result_text.insert(tk.END, f"{i}. {name}\n", "selected")
        
        self.result_text.insert(tk.END, "\nDidn't drop: ", "label")
        self.result_text.insert(tk.END, f"{self.previous_excluded}\n", "excluded")
        
        if not self.is_first_roll:
            self.result_text.insert(tk.END, "(Will be included in the next roll)\n", "note")
        
        # Автоматическая прокрутка к последнему результату
        self.result_text.see(tk.END)

# Запуск приложения
if __name__ == "__main__":
    root = tk.Tk()
    app = RollApp(root)
    root.mainloop()
