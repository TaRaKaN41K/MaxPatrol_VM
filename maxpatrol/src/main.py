from ui.VMScannerInterface import VMScannerInterface
from database.Database import Database
from logger.Logger import Logger

from dotenv import load_dotenv
import os

load_dotenv()

db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")

DATABASE_URL = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

if __name__ == '__main__':

    ssh_logger = Logger("SSH")
    db_logger = Logger("DB")
    flask_logger = Logger("UI")

    db = Database(db_url=DATABASE_URL, logger=db_logger)

    interface = VMScannerInterface(db=db, logger=flask_logger, ssh_logger=ssh_logger)
    interface.run()
