import logging

logging.basicConfig(filename='logs.log', encoding='utf-8', level=logging.DEBUG)


def write_log(kind, msg):
    if kind == 'info':
        logging.info(msg)
    elif kind == 'error':
        logging.error(msg)
    else:
        logging.debug(msg)

