import keyboard
import pyperclip
import time
# pip install keyboard pyperclip


class LineClipboardCopier:
    """
    Горячие клавиши для копирования элементов списка в буфер обмена. Каждое нажатие копирует следующий элемент списка
    Параллельно можно использовать другие горячие клавиши для константных строк <word>
    """

    _word = "Какое то слово"
    _items_list = []
    # **************
    _hotkey_for_items_list = 'left alt + x'
    _hotkey_for_word = 'left alt + z'

    def __init__(self, path2file='text.txt'):
        self._items_list = self._read_file_convert_text_to_list(path2file)
        self.current_index = 0
        self.len_items_list = len(self._items_list)

    def _read_file_convert_text_to_list(self, path2file):
        delimiter = '\n'
        with open(path2file, 'r', encoding="utf-8") as f:
            text = f.read()
        return [item.strip() for item in text.split(delimiter)]

    def _copy_list_item_to_clipboard(self):
        if self.current_index >= self.len_items_list:
            print("the list is over!")
            keyboard.unhook_all()
            return
        current_item = self._items_list[self.current_index]
        if self.current_index != 0:
            print(f'<- prev element: {self._items_list[self.current_index - 1]}')
        print(f'*** current element: {self._items_list[self.current_index]}')
        if self.current_index < self.len_items_list - 1:
            print(f'-> next element: {self._items_list[self.current_index + 1]}')
        print('-' * 10)

        pyperclip.copy(current_item)
        self.current_index += 1

    def _copy_word_to_clipboard(self):
        pyperclip.copy(self._word)

    def _register_hotkeys(self):
        keyboard.add_hotkey(self._hotkey_for_items_list, self._copy_list_item_to_clipboard)
        keyboard.add_hotkey(self._hotkey_for_word, self._copy_word_to_clipboard)

    def run(self):
        self._register_hotkeys()
        try:
            while True:
                time.sleep(0.1)
        except Exception as e:
            print(f"Произошла ошибка: {e}")
        finally:
            keyboard.unhook_all()


if __name__ == '__main__':
    hk = LineClipboardCopier()
    hk.run()
