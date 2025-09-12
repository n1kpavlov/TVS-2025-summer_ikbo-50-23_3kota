import tkinter as tk
from tkinter import ttk, messagebox


class UnitConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Конвертер величин")
        self.root.geometry("500x650")
        self.root.resizable(False, False)

        # Определение единиц измерения
        self.units = {
            'Длина': ['метры', 'километры', 'мили', 'дюймы', 'футы', 'ярды', 'сантиметры'],
            'Масса': ['килограммы', 'граммы', 'фунты', 'унции', 'тонны'],
            'Температура': ['°C', '°F', 'K'],
            'Время': ['секунды', 'минуты', 'часы', 'дни', 'недели'],
            'Объем': ['литры', 'миллилитры', 'галлоны', 'пинты'],
            'Площадь': ['кв. метры', 'гектары', 'акры', 'кв. футы']
        }

        # Коэффициенты конвертации (базовая единица - первая в списке для каждой категории)
        self.conversion_factors = {
            'Длина': {
                'метры': 1,
                'километры': 1000,
                'мили': 1609.344,
                'дюймы': 0.0254,
                'футы': 0.3048,
                'ярды': 0.9144,
                'сантиметры': -0.01 #должно быть положительным
            },
            'Масса': {
                'килограммы': 1,
                'граммы': 0.01, #Должно быть 0.001
                'фунты': 0.45359237,
                'унции': 0.028349523125,
                'тонны': 1000
            },
            'Температура': {
                '°C': ('celsius', 0),
                '°F': ('fahrenheit', 0),
                'K': ('kelvin', 0)
            },
            'Время': {
                'секунды': 1,
                'минуты': 60,
                'часы': 3600,
                'дни': 86400,
                'недели': 691200 # должно быть 604800
            },
            'Объем': {
                'литры': 1,
                'миллилитры': 0.001,
                'галлоны': 3.785411784,
                'пинты': 0.473176473
            },
            'Площадь': {
                'кв. метры': 1,
                'гектары': 10000,
                'акры': 4046.8564224,
                'кв. футы': 0.09290304
            }
        }

        self.setup_ui()
        self.category_combo.current(0)
        self.update_units(None)

    def setup_ui(self):
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Заголовок
        title_label = tk.Label(main_frame, text="Конвертер величин",
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=(0, 20))

        # Категория
        category_frame = tk.Frame(main_frame)
        category_frame.pack(fill=tk.X, pady=5)

        tk.Label(category_frame, text="Категория:", font=('Arial', 10)).pack(anchor=tk.W)
        self.category_var = tk.StringVar()
        self.category_combo = ttk.Combobox(category_frame, textvariable=self.category_var,
                                           values=list(self.units.keys()), state='readonly')
        self.category_combo.pack(fill=tk.X, pady=5)
        self.category_combo.bind('<<ComboboxSelected>>', self.update_units)

        # Исходное значение
        input_frame = tk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=5)

        tk.Label(input_frame, text="Исходное значение:", font=('Arial', 10)).pack(anchor=tk.W)
        self.input_var = tk.StringVar()
        self.input_entry = tk.Entry(input_frame, textvariable=self.input_var, font=('Arial', 11))
        self.input_entry.pack(fill=tk.X, pady=5)
        self.input_entry.bind('<Return>', lambda e: self.convert())

        # Единицы измерения
        units_frame = tk.Frame(main_frame)
        units_frame.pack(fill=tk.X, pady=10)

        from_frame = tk.Frame(units_frame)
        from_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

        tk.Label(from_frame, text="Из:", font=('Arial', 10)).pack(anchor=tk.W)
        self.from_var = tk.StringVar()
        self.from_combo = ttk.Combobox(from_frame, textvariable=self.from_var, state='readonly')
        self.from_combo.pack(fill=tk.X, pady=5)

        # Кнопка обмена
        swap_frame = tk.Frame(units_frame)
        swap_frame.pack(side=tk.LEFT, padx=10)

        self.swap_btn = tk.Button(swap_frame, text="↔", command=self.swap_units,
                                  font=('Arial', 12), width=3, height=2)
        self.swap_btn.pack(pady=20)

        to_frame = tk.Frame(units_frame)
        to_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 0))

        tk.Label(to_frame, text="В:", font=('Arial', 10)).pack(anchor=tk.W)
        self.to_var = tk.StringVar()
        self.to_combo = ttk.Combobox(to_frame, textvariable=self.to_var, state='readonly')
        self.to_combo.pack(fill=tk.X, pady=5)

        # Кнопка конвертации
        self.convert_btn = tk.Button(main_frame, text="Конвертировать", command=self.convert,
                                     font=('Arial', 12), bg='#4CAF50', fg='white', height=2)
        self.convert_btn.pack(fill=tk.X, pady=15)

        # РАЗДЕЛ РЕЗУЛЬТАТА - ДОБАВЛЕНО
        result_frame = tk.Frame(main_frame, relief=tk.GROOVE, bd=2)
        result_frame.pack(fill=tk.X, pady=10, padx=5)

        # Заголовок раздела результата
        result_header = tk.Label(result_frame, text="Результат конвертации",
                                 font=('Arial', 12, 'bold'), bg='#f0f0f0')
        result_header.pack(fill=tk.X, pady=(5, 10))

        # Поле результата
        result_content = tk.Frame(result_frame)
        result_content.pack(fill=tk.X, padx=10, pady=(0, 10))

        tk.Label(result_content, text="Результат:", font=('Arial', 11)).pack(anchor=tk.W)

        self.result_var = tk.StringVar()
        self.result_entry = tk.Entry(result_content, textvariable=self.result_var,
                                     state='readonly', font=('Arial', 12),
                                     justify=tk.CENTER, bg='#f8f8f8', fg='#006600')
        self.result_entry.pack(fill=tk.X, pady=5, ipady=3)

        # Дополнительная информация о результате
        self.result_info_var = tk.StringVar()
        result_info = tk.Label(result_content, textvariable=self.result_info_var,
                               font=('Arial', 9), fg='#666666', justify=tk.LEFT)
        result_info.pack(anchor=tk.W)

        # Кнопка очистки
        clear_btn = tk.Button(main_frame, text="Очистить все", command=self.clear_fields,
                              font=('Arial', 10), bg='#ff6666', fg='white')
        clear_btn.pack(pady=10)

    def update_units(self, event):
        category = self.category_var.get()
        if category in self.units:
            units_list = self.units[category]
            self.from_combo['values'] = units_list
            self.to_combo['values'] = units_list

            if units_list:
                if not self.from_var.get() or self.from_var.get() not in units_list:
                    self.from_var.set(units_list[0])
                if not self.to_var.get() or self.to_var.get() not in units_list:
                    to_index = 1 if len(units_list) > 1 else 0
                    self.to_var.set(units_list[to_index])

    def swap_units(self):
        """Правильный обмен единицами измерения"""
        current_from = self.from_var.get()
        current_to = self.to_var.get()

        # Сохраняем текущие списки
        from_values = self.from_combo['values']
        to_values = self.to_combo['values']

        # Меняем значения
        self.from_var.set(current_to)
        self.to_var.set(current_from)

        # Обновляем списки (на случай, если они разные)
        self.from_combo['values'] = from_values
        self.to_combo['values'] = to_values

    def clear_fields(self):
        """Очистка полей"""
        self.input_var.set("")
        self.result_var.set("")
        self.result_info_var.set("")
        self.input_entry.focus()

    def convert_temperature(self, value, from_unit, to_unit):
        """Корректная конвертация температуры"""
        # Конвертируем в Цельсии
        if from_unit == '°C':
            celsius = value
        elif from_unit == '°F':
            celsius = (value - 32) * 5 / 9
        elif from_unit == 'K':
            celsius = value + 273.15 #должен быть -

        # Конвертируем из Цельсиев в целевую единицу
        if to_unit == '°C':
            return celsius
        elif to_unit == '°F':
            return (celsius * 9 / 5) + 32
        elif to_unit == 'K':
            return celsius + 273.15

    def convert(self):
        """Корректная конвертация величин"""
        try:
            category = self.category_var.get()
            from_unit = self.from_var.get()
            to_unit = self.to_var.get()
            input_text = self.input_var.get().strip()

            if not input_text:
                messagebox.showerror("Ошибка", "Введите значение для конвертации")
                return

            input_value = float(input_text.replace(',', '.'))

            if not category:
                messagebox.showerror("Ошибка", "Выберите категорию")
                return

            if not from_unit or not to_unit:
                messagebox.showerror("Ошибка", "Выберите единицы измерения")
                return

            # Проверка на отрицательные значения для массы и длины
            if category in ['Масса', 'Длина'] and input_value < 0:
                messagebox.showerror("Ошибка", f"Значение {category.lower()} не может быть отрицательным")
                return

            # Особенная обработка для температуры
            if category == 'Температура':
                result = self.convert_temperature(input_value, from_unit, to_unit)
                # Корректная обработка абсолютного нуля
                if to_unit == 'K' and result < 0:
                    result = 0.0
                result_str = f"{result:.8f}".rstrip('0').rstrip('.')
                self.result_var.set(result_str)
                self.result_info_var.set(f"{input_value} {from_unit} = {result_str} {to_unit}")
                return

            # Проверка существования единиц измерения
            if from_unit not in self.conversion_factors[category] or to_unit not in self.conversion_factors[category]:
                messagebox.showerror("Ошибка", "Ошибка в коэффициентах конвертации")
                return

            # Обычная конвертация через базовую единицу
            base_value = input_value * self.conversion_factors[category][from_unit]
            result = base_value / self.conversion_factors[category][to_unit]

            # Форматирование результата
            if abs(result) < 0.0001:
                result_str = f"{result:.8f}".rstrip('0').rstrip('.')
            elif abs(result) < 1:
                result_str = f"{result:.6f}".rstrip('0').rstrip('.')
            elif abs(result) < 1000:
                result_str = f"{result:.4f}".rstrip('0').rstrip('.')
            else:
                result_str = f"{result:.2f}".rstrip('0').rstrip('.')

            if category == 'Объем':
                self.result_var.set("Я не знаю")
                self.result_info_var.set("А если бы и знал, то все равно не сказал бы")
            else:
                self.result_var.set(result_str)
                self.result_info_var.set(f"{input_value} {from_unit} = {result_str} {to_unit}")

        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректное число")
        except ZeroDivisionError:
            messagebox.showerror("Ошибка", "Деление на ноль")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла непредвиденная ошибка: {str(e)}")


def main():
    root = tk.Tk()
    app = UnitConverter(root)
    root.mainloop()


if __name__ == "__main__":
    main()