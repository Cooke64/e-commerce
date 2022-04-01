import logging
from functools import wraps


def create_logger():
    logging.basicConfig(
        level=logging.DEBUG,
        filename='program.log',
        format='%(asctime)s, %(levelname)s, %(message)s, %(name)s'
    )
    logger = logging.getLogger("main")
    return logger


def loger_errors(function):
    @wraps(function)
    def wrapper(request, *args, **kwargs):
        logger = create_logger()
        try:
            response = function(request, *args, **kwargs)
            logger.info('Работает')
            return response,
        except:
            err = f"Ошибка в функции {function.__name__} "
            err += function.__name__
            logger.error(err)
            raise

    return wrapper

