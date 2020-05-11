
import logging.handlers


def init_logger(log_name):
    logger = logging.getLogger(log_name)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s - %(threadName)s - %(levelname)s "
                                  "%(filename)s:%(lineno)-4d - %(message)s")

    if not len(logger.handlers):
        stdout_handler = logging.StreamHandler()
        stdout_handler.setFormatter(formatter)
        logger.addHandler(stdout_handler)

        file_handler = logging.handlers.RotatingFileHandler(
            f"logs/{log_name}.log",
            maxBytes=100 * 1024 * 1024,
            backupCount=5,
            encoding='utf8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    return logger
