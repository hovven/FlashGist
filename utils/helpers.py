import logging


def setup_logging():
    logging.basicConfig(filename='logs/app.log', level=logging.INFO,
                        format='%(asctime)s [%(levelname)s] - %(message)s')
    return logging
