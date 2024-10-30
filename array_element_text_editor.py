import tkinter as tk
from threading import Thread
from multiprocessing import Queue
from time import sleep


class TextEditor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.queue_to_gui = Queue()
        self.queue_from_gui = Queue()

        self.title("Editor")
        self.geometry("825x520")

        # настройка сетки для растягивания виджетов
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)  # растягиваемая строка для виджетов Text

        # лейбл со счётчиком элементов массива
        self.counter_label = tk.Label(self, text='')
        self.counter_label.grid(row=0, column=0, columnspan=2, sticky="n", pady=(5, 0))

        # текстовые поля
        self.text_input = tk.Text(self, wrap="word")
        self.text_input.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        self.text_output = tk.Text(self, wrap="word")
        self.text_output.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

        # кнопка
        self.button = tk.Button(self, text="Сохранить/Далее", command=self.command_btn)
        self.button.grid(row=2, column=0, columnspan=2, pady=(5, 10))

        # запуск потоков для обработки массива и очереди
        Thread(target=iterating_over_array_and_editing_items, daemon=True, args=[self.queue_to_gui, self.queue_from_gui]).start()
        Thread(target=self.queue_to_gui_reading, daemon=True).start()

    def queue_to_gui_reading(self):
        while True:
            if not self.queue_to_gui.empty():
                data = self.queue_to_gui.get()
                text = data['text']
                counter = data['counter']
                self.text_input.insert("end", text)
                self.counter_label.config(text=counter)
            sleep(0.1)

    def command_btn(self):
        text = self.text_output.get(1.0, tk.END)
        self.queue_from_gui.put(text)
        self.text_input.delete(1.0, tk.END)
        self.text_output.delete(1.0, tk.END)


def iterating_over_array_and_editing_items(queue_to_gui=None, queue_from_gui=None) -> list or tuple:
    ###
    # блок для чтения массива из файла или использование глобальной переменной
    array = ['my_data_1', 'my_data_2', 'my_data_3']  # заменить на необходимые данные
    ###

    len_array = str(len(array))
    for i in range(len(array)):
        item = array[i]

        ###
        # блок обмена значением с потоком gui
        if queue_to_gui:
            queue_to_gui.put(
                {
                    'counter': f'{str(i)}/{len_array}',
                    'text': item
                }
                )
        while True:
            if not queue_from_gui.empty():
                edited_item = queue_from_gui.get()
                break
            sleep(0.1)
        ###

        array[i] = edited_item


def run_app():
    """
    Графический интерфейс для ручного редактирования элементов массива на лету.
    Сконфигурировать функцию iterating_over_array_and_editing_items под нужды.
    """"
    app = TextEditor()
    app.mainloop()

