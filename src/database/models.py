from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

# Базовый класс для моделей
Base = declarative_base()


class VMScanResult(Base):
    __tablename__ = 'info_from_scanned_machines'

    id = Column(Integer, primary_key=True)
    ip_address = Column(String, nullable=False)
    port = Column(Integer, nullable=False)
    os_name = Column(String, nullable=False)
    os_version = Column(String, nullable=True)
    architecture = Column(String, nullable=True)
