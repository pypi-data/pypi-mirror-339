import json
import os

class GramDatabase:
    def __init__(self, GRAMBASE):
        self.GRAMBASE = GRAMBASE
        self.data = {}
        self.is_open = False

    def create_table(self, **kwargs):
        """Создает новую таблицу (файл) и заполняет ее данными."""
        if os.path.exists(self.GRAMBASE):
            print(f"Ошибка: Таблица '{self.GRAMBASE}' уже существует. Используйте open_table для изменения.")
            return
        self.data = kwargs
        self._save_data()

    def close_table(self):
        """Закрывает таблицу (только для совместимости). Ничего не делает."""
        print("close_table() больше не нужен. Таблица создается сразу после create_table().")
        pass # Ничего не делаем, чтобы не ломать старый код

    def open_table(self):
        """Открывает существующую таблицу для изменения."""
        if self.is_open:
            print("Таблица уже открыта.")
            return
        try:
            with open(self.GRAMBASE, 'r') as f:
                self.data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            print(f"Ошибка: Таблица '{self.GRAMBASE}' не найдена или повреждена.")
            self.data = {}  # Создаем пустую таблицу в памяти, если не удалось загрузить
        self.is_open = True

    def closeSave_table(self):
        """Закрывает таблицу и сохраняет изменения."""
        if self.is_open:
            self.is_open = False
            self._save_data()
        else:
            print("Ошибка: Попытка закрыть таблицу, которая не была открыта.")

    def delete_table(self):
        """Удаляет файл базы данных."""
        if os.path.exists(self.GRAMBASE):
            os.remove(self.GRAMBASE)
            print(f"Таблица '{self.GRAMBASE}' удалена.")
            self.data = {}
        else:
            print(f"Таблица '{self.GRAMBASE}' не существует.")

    def delete_key(self, key):
        """Удаляет ключ из таблицы."""
        if not self.is_open:
            print("Ошибка: Сначала необходимо открыть таблицу с помощью open_table().")
            return
        if key in self.data:
            del self.data[key]
            print(f"Ключ '{key}' удален.")
        else:
            print(f"Ключ '{key}' не найден.")

    def create_key(self,key,value):
        if not self.is_open:
            print("Ошибка: Сначала необходимо открыть таблицу с помощью open_table().")
            return
        self.data[key] = value
        print(f"Ключ '{key}' добавлен.")


    def _save_data(self):
        """Внутренний метод для сохранения данных в файл."""
        with open(self.GRAMBASE, 'w') as f:
            json.dump(self.data, f, indent=4)

    def __enter__(self):
        """Для использования в контекстном менеджере (with ... as ...:)"""
        self.open_table()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Автоматически закрывает и сохраняет изменения при выходе из контекстного менеджера."""
        self.closeSave_table()
