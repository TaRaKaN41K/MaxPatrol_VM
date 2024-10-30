import paramiko
from typing import List, Dict

from logger.Logger import Logger


class SSHClient:
    def __init__(self, hostname: str, port: int, username: str, password: str, logger: Logger):
        self.logger = logger

        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.client = None

    def connect(self):
        """Устанавливает SSH-соединение с удаленной машиной."""
        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.client.connect(hostname=self.hostname, port=self.port, username=self.username, password=self.password)
            self.logger.info(f"Подключение к {self.hostname}:{self.port} выполнено успешно.")
            return True
        except paramiko.AuthenticationException:
            self.logger.error("Ошибка аутентификации при подключении к SSH.")
            return False
        except paramiko.SSHException as ssh_error:
            self.logger.error(f"Ошибка SSH: {ssh_error}")
            return False
        except Exception as e:
            self.logger.error(f"Ошибка подключения: {e}")
            return False

    def close(self):
        """Закрывает SSH-соединение."""
        if self.client:
            try:
                self.client.close()
                self.logger.info("SSH соединение закрыто.")
            except Exception as e:
                self.logger.error(f"Ошибка при закрытии соединения: {e}")

    def execute_commands(self, commands: List[str]) -> Dict[str, Dict[str, str]]:
        """Выполняет список команд и возвращает словарь с выводом и ошибками для каждой команды."""
        if self.client is None:
            self.logger.error("SSH-соединение не установлено.")
            raise Exception

        results = {}
        for command in commands:
            try:
                self.logger.info(f"Executing command: {command}")
                stdin, stdout, stderr = self.client.exec_command(command)
                output = stdout.read().decode('utf-8')
                error = stderr.read().decode('utf-8')

                if output:
                    self.logger.info(f"Output for '{command}': {output.strip()}")
                if error:
                    self.logger.error(f"Error for '{command}': {error.strip()}")

                results[command] = {"output": output, "error": error}
            except Exception as e:
                self.logger.error(f"Ошибка при выполнении команды '{command}': {e}")
                results[command] = {"output": "", "error": e}

        return results
