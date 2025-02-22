import paramiko
import logging
from datetime import datetime

# Настройка логирования
logging.basicConfig(
    filename='server_automation.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class SSHManager:
    def __init__(self, hostname, username, password, port=22):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.port = port
        self.client = None

    def connect(self):
        """Подключение к удаленному серверу."""
        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.client.connect(
                hostname=self.hostname,
                port=self.port,
                username=self.username,
                password=self.password,
                timeout=10
            )
            logging.info(f"✅ Подключено к {self.hostname}")
            print(f"✅ Подключено к {self.hostname}")
        except Exception as e:
            logging.error(f"❌ Ошибка подключения к {self.hostname}: {e}")
            print(f"❌ Ошибка подключения: {e}")
            self.client = None

    def execute_command(self, command):
        """Выполнение команды на сервере."""
        if self.client is None:
            logging.error("❌ Нет активного подключения.")
            return "Нет подключения"

        try:
            stdin, stdout, stderr = self.client.exec_command(command)
            output = stdout.read().decode().strip()
            error = stderr.read().decode().strip()

            if output:
                logging.info(f"📊 Результат команды '{command}': {output}")
                print(f"📊 Результат:\n{output}")

            if error:
                logging.warning(f"⚠️ Ошибка выполнения '{command}': {error}")
                print(f"⚠️ Ошибка:\n{error}")

            return output if output else error

        except Exception as e:
            logging.error(f"❌ Ошибка выполнения '{command}': {e}")
            print(f"❌ Ошибка выполнения команды: {e}")

    def close_connection(self):
        """Закрытие SSH-сессии."""
        if self.client:
            self.client.close()
            logging.info(f"🔒 Соединение с {self.hostname} закрыто.")
            print(f"🔒 Соединение закрыто.")

# -----------------------------
# ✅ Пример использования
if __name__ == "__main__":
    # Данные для подключения
    server_info = {
        "hostname": "your_server_ip",
        "username": "your_username",
        "password": "your_password"
    }

    # Список команд для выполнения
    commands = [
        "whoami",             # Пользователь
        "uptime",             # Время работы сервера
        "df -h",              # Использование диска
        "free -m",            # Оперативная память
        "uname -a"            # Информация о системе
    ]

    ssh_manager = SSHManager(**server_info)
    ssh_manager.connect()

    for cmd in commands:
        ssh_manager.execute_command(cmd)

    ssh_manager.close_connection()
