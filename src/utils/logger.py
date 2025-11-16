import logging
from pathlib import Path


class Logger:

    def __init__(self, name='APP_LOGGER', log_file='./logs/app.log'):
        self.name = name
        self.log_file = Path(log_file)

        self.log_file.parent.mkdir(parents=True, exist_ok=True)

        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(logging.DEBUG)

        if not self.logger.handlers:

            file_handler = logging.FileHandler(self.log_file, mode='a', encoding='utf-8')
            file_handler.setLevel(logging.DEBUG)

            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)

            formatter = logging.Formatter(
                '[%(asctime)s] [%(levelname)s] %(message)s',
                datefmt = '%Y-%m-%d %H:%M:%S'
            )

            file_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)

            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)

        
    def get_logger(self):
        return self.logger
    

