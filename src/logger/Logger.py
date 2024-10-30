import logging
import os
from datetime import datetime


class Logger:
    def __init__(self, name: str, log_dir: str = "/logs"):
        # Создаем директорию для логов, если она не существует
        os.makedirs(log_dir, exist_ok=True)

        # Создаем поддиректорию для текущего типа логгера
        specific_log_dir = os.path.join(log_dir, name)
        os.makedirs(specific_log_dir, exist_ok=True)

        # Устанавливаем имя лог-файла с текущей датой
        log_file = os.path.join(specific_log_dir, f"{name}_{datetime.now().strftime('%Y-%m-%d')}.log")

        # Настройка логгера
        self.logger = logging.getLogger(name)
        if not self.logger.hasHandlers():  # Проверка на наличие обработчиков
            self.logger.setLevel(logging.DEBUG)

            # Формат сообщений в логах
            formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

            # Обработчик для записи логов в файл
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(formatter)

            # # Обработчик для вывода логов в консоль
            # console_handler = logging.StreamHandler()
            # console_handler.setLevel(logging.INFO)
            # console_handler.setFormatter(formatter)

            # Добавляем обработчики в логгер
            self.logger.addHandler(file_handler)
            # self.logger.addHandler(console_handler)

    def info(self, message: str):
        self.logger.info(message)

    def error(self, message: str):
        self.logger.error(message)

    def warning(self, message: str):
        self.logger.warning(message)

    def debug(self, message: str):
        self.logger.debug(message)
