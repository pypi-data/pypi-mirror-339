import json
import os

class GramDatabase:
    def __init__(self, GRAMBASE):
        self.GRAMBASE = GRAMBASE


        
        self.data = {}
        self.is_open = False

    def create_table(self, **kwargs):
        """Создает новую таблицу (файл) и заполняет ее данными, или обновляет существующую."""
        if os.path.exists(self.GRAMBASE):
            print(f"Ошибка: Таблица '{self.GRAMBASE}' уже существует. Используйте open_table для изменения.")
            return self #Возвращаем self для цепочки вызовов
        self.data = kwargs
        self._save_data()
        return self #Возвращаем self для цепочки вызовов


    def open_table(self):
        """Открывает существующую таблицу для изменения."""
        if self.is_open:
            print("Таблица уже открыта.")
            return self #Возвращаем self для цепочки вызовов
        try:
            with open(self.GRAMBASE, 'r') as f:
                self.data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            print(f"Ошибка: Таблица '{self.GRAMBASE}' не найдена или повреждена.")
            self.data = {}  # Создаем пустую таблицу в памяти, если не удалось загрузить
        self.is_open = True
        return self #Возвращаем self для цепочки вызовов

    def closeSave_table(self):
        """Закрывает таблицу и сохраняет изменения."""
        if self.is_open:
            self.is_open = False
            self._save_data()
        else:
            print("Ошибка: Попытка закрыть таблицу, которая не была открыта.")
        return self #Возвращаем self для цепочки вызовов

    def delete_table(self):
        """Удаляет файл базы данных."""
        if os.path.exists(self.GRAMBASE):
            os.remove(self.GRAMBASE)
            print(f"Таблица '{self.GRAMBASE}' удалена.")
            self.data = {}
        else:
            print(f"Таблица '{self.GRAMBASE}' не существует.")
        return self #Возвращаем self для цепочки вызовов

    def delete_key(self, key):
        """Удаляет ключ из таблицы."""
        if not self.is_open:
            print("Ошибка: Сначала необходимо открыть таблицу с помощью open_table().")
            return self #Возвращаем self для цепочки вызовов
        if key in self.data:
            del self.data[key]
            print(f"Ключ '{key}' удален.")
        else:
            print(f"Ключ '{key}' не найден.")
        return self #Возвращаем self для цепочки вызовов

    def create_key(self, key, value):
        """Создает новый ключ."""
        if not self.is_open:
            print("Ошибка: Сначала необходимо открыть таблицу с помощью open_table().")
            return self #Возвращаем self для цепочки вызовов
        self.data[key] = value
        print(f"Ключ '{key}' добавлен.")
        return self #Возвращаем self для цепочки вызовов


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

