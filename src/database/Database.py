from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError, OperationalError

from database.models import VMScanResult, Base
from logger.Logger import Logger


class Database:
    def __init__(self, db_url: str, logger: Logger):
        self.logger = logger
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)
        try:
            self.init_db()
        except OperationalError as e:
            self.logger.error(f"Ошибка подключения к базе данных: {e}")

    def init_db(self):
        """Создаем таблицы, если их еще нет"""
        try:
            Base.metadata.create_all(self.engine)
            self.logger.info("Таблицы успешно созданы или уже существуют.")
        except SQLAlchemyError as e:
            self.logger.error(f"Ошибка при инициализации базы данных: {e}")

    def add_scan_result(self, ip, port, os_name, os_version, architecture):
        """Добавление новой записи в таблицу"""
        session = self.Session()
        try:
            new_result = VMScanResult(
                ip_address=ip,
                port=port,
                os_name=os_name,
                os_version=os_version,
                architecture=architecture
            )
            session.add(new_result)
            session.commit()
            self.logger.info(f"Запись для {ip}:{port} успешно добавлена.")
        except SQLAlchemyError as e:
            session.rollback()
            self.logger.error(f"Ошибка при добавлении записи: {e}")
        finally:
            session.close()

    def get_scan_results(self):
        """Получение всех записей из таблицы"""
        session = self.Session()
        try:
            results = session.query(VMScanResult).all()
            self.logger.info(f"Получено {len(results)} записей из таблицы.")
            return results
        except SQLAlchemyError as e:
            self.logger.error(f"Ошибка при получении записей: {e}")
            return []
        finally:
            session.close()
