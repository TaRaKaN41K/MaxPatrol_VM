from flask import Flask, render_template, request
from database.Database import Database
from ssh_connection.SSHClient import SSHClient
from logger.Logger import Logger


class VMScannerInterface:
    def __init__(self, db: Database, logger: Logger, ssh_logger: Logger):
        self.logger = logger
        self.ssh_logger = ssh_logger
        self.db = db
        self.app = Flask(__name__)
        self.setup_routes()

    def setup_routes(self):
        @self.app.route('/')
        def index():
            self.logger.info("Загрузка главной страницы.")
            return render_template('index.html')

        @self.app.route('/start_scan', methods=['POST'])
        def start_scan():
            try:
                ip = request.form['ip']
                port = int(request.form['port'])
                username = request.form['username']
                password = request.form['password']
                commands = ['uname -m', 'lsb_release -a']

                self.logger.info(f"Начало сканирования для {ip}:{port}")

                ssh_connect = SSHClient(hostname=ip, port=port, username=username, password=password, logger=self.ssh_logger)
                if not ssh_connect.connect():
                    error_text = f"Ошибка подключения к {ip}:{port}"
                    self.logger.error(error_text)
                    return render_template('error.html', error=error_text)

                output_dict = ssh_connect.execute_commands(commands=commands)
                ssh_connect.close()

                if output_dict[commands[0]]['output'] and output_dict[commands[1]]['output']:
                    lsb_release = output_dict['lsb_release -a']['output'].strip('\n').split('\n')
                    result_dict = {}
                    for line in lsb_release:
                        key, value = line.split(":\t")
                        result_dict[key.strip()] = value.strip()

                    result_dict['architecture'] = output_dict['uname -m']['output'].strip('\n')

                    self.db.add_scan_result(
                        ip=ip,
                        port=port,
                        os_name=result_dict['Distributor ID'],
                        os_version=result_dict['Release'],
                        architecture=result_dict['architecture']
                    )

                    self.logger.info(f"Сканирование для {ip}:{port} завершено успешно.")
                    return render_template(
                        'scan_result.html',
                        ip=ip,
                        port=port,
                        username=username,
                        os=result_dict['Distributor ID'],
                        version=result_dict['Release'],
                        architecture=result_dict['architecture']
                    )
                else:
                    uname_error = output_dict[commands[0]]['error']
                    lsb_release_error = output_dict[commands[1]]['error']
                    error_text = f"Ошибка выполнения команд для {ip}:{port}: uname - {uname_error}, lsb_release - {lsb_release_error}"
                    self.logger.error(error_text)
                    return render_template('error.html', error=error_text)
            except Exception as e:
                self.logger.error(f"Критическая ошибка при запуске сканирования: {e}")
                return render_template('error.html', error=e)

        @self.app.route('/database')
        def show_database():
            try:
                self.logger.info("Запрос на получение данных из базы.")
                scan_results = self.db.get_scan_results()
            except Exception as e:
                self.logger.error(f"Ошибка при получении данных из базы данных: {e}")
                return render_template('error.html', error=e)
            return render_template('database.html', results=scan_results)

    def run(self):
        self.logger.info("Запуск веб-сервера Flask.")
        self.app.run(host='0.0.0.0', port=5000, debug=True)
