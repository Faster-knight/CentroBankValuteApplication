import tkinter as tk
from tkinter import ttk
import xmltodict
import requests
import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from dateutil.relativedelta import relativedelta


class Application:
    first_url = 'https://www.cbr-xml-daily.ru/daily_json.js'
    second_url = 'https://www.cbr.ru/scripts/XML_dynamic.asp'
    date_size = 20  # Размер списка дат, при выборе промежутка времени
    data_size = 25  # Количество элементов в графике

    # метод возврата данных
    @staticmethod
    def get__str_date(date):
        day_str = str(date.day).zfill(2)  # создание двухзначного формата в строковом виде
        month_str = str(date.month).zfill(2) # создание двухзначного формата в строковом виде
        year_str = str(date.year)
        return f"{day_str}/{month_str}/{year_str}"

    def __init__(self, parent_head_object):
        # окно приложения
        self.parent = parent_head_object
        self.parent.title("Конвертер валют")
        # Создание вкладок
        tab_control = ttk.Notebook(self.parent)
        self.tab1 = ttk.Frame(tab_control)
        self.tab2 = ttk.Frame(tab_control)
        tab_control.add(self.tab1, text='Конвертер')
        tab_control.add(self.tab2, text='Динамика курса')
        tab_control.pack(expand=1, fill='both')
        # Получение списка валют
        self.currencies = dict()
        self.currencies_name = list()
        response = requests.get(self.first_url)
        self.currencies = response.json()
        self.currencies['Valute']['RUB'] = {'Name': 'Российский рубль', 'Value': 1, 'Nominal' : 1}
        self.currencies_name = list([i['Name'] for i in self.currencies['Valute'].values()])
        # первая вкладка приложения
        self.from_currency = tk.StringVar(value='Доллар США')
        self.to_currency = tk.StringVar(value='Российский рубль')
        self.from_currency_combobox = ttk.Combobox(self.tab1, values=self.currencies_name, textvariable=self.from_currency)
        self.to_currency_combobox = ttk.Combobox(self.tab1, values=self.currencies_name, textvariable=self.to_currency)
        self.amount_entry = tk.Entry(self.tab1)
        self.result_label = tk.Label(self.tab1, text='Результат: ')
        self.convert_button = tk.Button(self.tab1, text='Конвертировать', command=self.convert)
        # вторая вкладка приложения
        self.years, self.quarter, self.months, self.weeks = [], [], [], []
        current_year = datetime.date.today().year
        current_quarter = (datetime.date.today().month + 1) // 3 + 1
        current_month = datetime.date.today().month
        for i in range(self.date_size + 1):
            self.years.append(datetime.date(current_year - i, 1, 1))
            self.quarter.append(datetime.date(current_year, 1 + (current_quarter - 1) * 3, 1) - relativedelta(months=3*i))
            self.months.append(datetime.date(current_year, current_month + 1, 1) - relativedelta(months=i))
            self.weeks.append(datetime.date.today() - datetime.timedelta(days=7 * i))
        self.years_str, self.quarter_str, self.months_str, self.weeks_str = list(), list(), list(), list()
        for i in range(self.date_size):
            self.years_str.append(self.get__str_date(self.years[i + 1]) + "-" + self.get__str_date(self.years[i]))
            self.quarter_str.append(self.get__str_date(self.quarter[i + 1]) + "-" + self.get__str_date(self.quarter[i]))
            self.months_str.append(self.get__str_date(self.months[i + 1]) + "-" + self.get__str_date(self.months[i]))
            self.weeks_str.append(self.get__str_date(self.weeks[i + 1]) + "-" + self.get__str_date(self.weeks[i]))
        # Создание элементов для второй вкладки
        var = tk.StringVar()
        self.text_valute = tk.Label(self.tab2, text='Валюта')
        self.text_period = tk.Label(self.tab2, text='Период')
        self.text_choose_period = tk.Label(self.tab2, text='Выбор периода')
        self.first_currency = tk.StringVar(value='Доллар США')
        self.choosed_currency = ttk.Combobox(self.tab2, values=self.currencies_name, textvariable=self.first_currency)
        self.week_peroid = tk.Radiobutton(self.tab2, text='Неделя', variable=var, value=1, command=self.func_week_period)
        self.month_peroid = tk.Radiobutton(self.tab2, text='Месяц', variable=var, value=2, command=self.func_month_period)
        self.quarter_peroid = tk.Radiobutton(self.tab2, text='Квартал', variable=var, value=3, command=self.func_quarter_period)
        self.year_peroid = tk.Radiobutton(self.tab2, text='Год', variable=var, value=4, command=self.func_years_period)
        self.graphic_button = tk.Button(self.tab2, text='Построить график', command=self.graphic_draw)
        self.first_number_period = tk.StringVar(value="01/01/2023-09/01/2023")
        self.number_period = ttk.Combobox(self.tab2, values=self.currencies_name, textvariable=self.first_number_period)
        # Размещение элементов на первой вкладке
        self.from_currency_combobox.grid(row=0, column=0, padx=10, pady=10)
        self.to_currency_combobox.grid(row=1, column=0, padx=10, pady=10)
        self.amount_entry.grid(row=0, column=1, padx=10, pady=10)
        self.convert_button.grid(row=0, column=2, padx=10, pady=10)
        self.result_label.grid(row=1, column=1, padx=10, pady=10)
        # Размещение элементов на второй вкладке
        self.text_valute.grid(row=0, column=0, padx=10, pady=10)
        self.text_period.grid(row=0, column=1, padx=10, pady=10)
        self.text_choose_period.grid(row=0, column=2, padx=10, pady=10)
        self.choosed_currency.grid(row=2, column=0, padx=10, pady=10)
        self.week_peroid.grid(row=2, column=1, padx=10, pady=10)
        self.month_peroid.grid(row=3, column=1, padx=10, pady=10)
        self.quarter_peroid.grid(row=4, column=1, padx=10, pady=10)
        self.year_peroid.grid(row=5, column=1, padx=10, pady=10)
        self.graphic_button.grid(row=5, column=0, padx=10, pady=10)
        self.number_period.grid(row=0, column=3, padx=10, pady=10)

    def convert(self):
        # метод конвертации из одной валюты в другую
        # Обработка случая когда у нас ввод текста
        try:
            input_value = float(self.amount_entry.get())
        except ValueError:
            self.result_label.configure(text='Ошибка: некорректное значение')
            return
        from_currency = ''
        to_currency = ''
        count_from, count_to = 0, 0
        # пробегаемся по полученным валютам
        for i in self.currencies['Valute']:
            value = self.currencies['Valute'][i]['Name']
            if self.from_currency.get() == value:
                from_currency = i
                count_from = self.currencies['Valute'][i]['Nominal']
            if self.to_currency.get() == value:
                to_currency = i
                count_to = self.currencies['Valute'][i]['Nominal']
        from_currency_rate = self.currencies['Valute'][from_currency]['Value']
        to_currency_rate = self.currencies['Valute'][to_currency]['Value']
        result = input_value * from_currency_rate / to_currency_rate / count_from * count_to
        self.result_label.configure(text='Результат: {:.5f} {}'.format(result, to_currency))

    def func_week_period(self):
        # получение дат по неделям
        self.first_number_period.set(self.weeks_str[0])
        self.number_period['values'] = self.weeks_str

    def func_month_period(self):
        self.first_number_period.set(self.months_str[0])
        self.number_period['values'] = self.months_str

    def func_quarter_period(self):
        self.first_number_period.set(self.quarter_str[0])
        self.number_period['values'] = self.quarter_str

    def func_years_period(self):
        self.first_number_period.set(self.years_str[0])
        self.number_period['values'] = self.years_str

    def graphic_draw(self):
        # метод отрисовки графика
        date_1 = self.number_period.get()[:10]
        date_2 = self.number_period.get()[11:]
        valute = self.choosed_currency.get()
        if valute == "Российский рубль":
            return
        currency = ''
        # пробегаемся по валютам
        for i in self.currencies['Valute']:
            # если нашли нужную валюту
            if self.currencies['Valute'][i]['Name'] == valute:
                currency = self.currencies['Valute'][i]["ID"]
                break
        # параметры получения данных
        params = {
            'date_req1': date_1,
            'date_req2': date_2,
            'VAL_NM_RQ': currency,
        }
        response = requests.get(requests.get(self.second_url, params=params).url.replace("%2F", "/"))
        print(response.url) # показываем путь к данным на сайте сбера которые используем
        xml_data = response.content
        json_data = xmltodict.parse(xml_data)
        dates = []
        values = []
        nominals = []
        if 'Record' not in json_data['ValCurs'].keys():
            return
        for item in json_data['ValCurs']['Record']:
            date = item['@Date']
            value = item['Value']
            nominal = item['Nominal']
            dates.append(date)
            values.append(float(value.replace(',', '.')))
            nominals.append(float(nominal.replace(',', '.')))
        small_dates = dates
        small_values = values
        small_nominals = nominals
        # дополняем данные если обнаружили пробел
        if len(dates) > self.data_size:
            small_values = []
            small_dates = []
            small_nominals = []
            for i in range(0, len(dates), len(dates) // self.data_size):
                small_dates.append(dates[i])
                small_values.append(values[i])
                small_nominals.append(nominals[i])
        for i in range(len(small_values)):
            if small_nominals[i] is not None:
                small_values[i] = small_values[i] / small_nominals[i]
        # начинаем отрисовывать график по полученным данный
        fig = plt.figure(figsize=(10, 6))
        plt.xticks(range(len(small_dates)), small_dates, rotation=30)
        plt.plot(small_dates, small_values)
        if hasattr(self, 'canvas'):
            self.canvas.get_tk_widget().destroy()
        self.canvas = FigureCanvasTkAgg(fig, master=self.tab2)
        self.canvas.get_tk_widget().grid()
        self.canvas.draw()


if __name__ == "__main__":
    root = tk.Tk()
    app = Application(root)
    root.mainloop()
