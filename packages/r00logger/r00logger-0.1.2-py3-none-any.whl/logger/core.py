import inspect
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from loguru import logger as log

from .helpers.constants import DEFAULT_LOG_LEVEL, ENV_LEVEL_NAME

_LOGGER_LIB_DIR = Path(__file__).parent.resolve()


def _find_and_load_dotenv():
    """
    Ищет .env файл, начиная от директории первого скрипта в стеке вызовов,
    который НЕ является частью библиотеки logger, и загружает его.
    """
    try:
        stack = inspect.stack()
        script_path = None

        # Итерируем по стеку вызовов (начиная с [1], т.к. [0] - это _find_and_load_dotenv)
        for frame_info in stack[1:]:
            # Получаем абсолютный путь к файлу фрейма
            frame_filename = Path(frame_info.filename).resolve()

            # Проверяем, НЕ находится ли этот файл внутри директории нашей библиотеки
            # Используем строковое представление для startswith
            if not str(frame_filename).startswith(str(_LOGGER_LIB_DIR)):
                script_path = frame_filename
                # print(f"DEBUG: Found potential script path: {script_path}") # Для отладки
                break # Нашли первый файл вне библиотеки, это наш искомый скрипт

        if script_path is None:
            print("WARNING: Could not determine the calling script's path outside the logger library.")
            return False

        # Теперь ищем .env вверх от директории найденного скрипта
        start_dir = script_path.parent
        current_dir = start_dir

        # print(f"DEBUG: Starting .env search from: {start_dir}") # Для отладки

        while True: # Безопаснее использовать while True с явным break
            dotenv_path = current_dir / ".env"
            # print(f"DEBUG: Checking for .env at: {dotenv_path}") # Для отладки
            if dotenv_path.is_file():
                loaded = load_dotenv(dotenv_path=dotenv_path, override=True)
                return loaded # Загрузили или нашли, выходим

            # Проверяем, достигли ли мы корневой директории
            if current_dir == current_dir.parent:
                # print("DEBUG: Reached root directory, .env not found.") # Для отладки
                break # Дошли до корня, прекращаем поиск

            # Переходим на уровень выше
            current_dir = current_dir.parent

        # Если вышли из цикла, значит .env не найден
        return False

    except Exception as e:
        # Используем print для вывода ошибки, т.к. логгер может быть не готов
        print(f"WARNING: Error during .env search/load: {e}")
        import traceback
        print(traceback.format_exc()) # Печатаем стектрейс ошибки поиска
        return False


def add_stdout():
    # Вывод в консоль (stdout) с цветом и другим уровнем:
    # get_level = os.getenv("LOG_LEVEL")
    # log_level = "TRACE" if not os.getenv("LOG_LEVEL") else get_level

    _find_and_load_dotenv()
    log_level = os.environ.get(ENV_LEVEL_NAME, DEFAULT_LOG_LEVEL).upper()
    print('LOG_LEVEL:', log_level)
    log.add(
        sys.stdout,  # Приемник - стандартный вывод
        level=log_level,  # Показывать сообщения от DEBUG и выше
        colorize=True,  # Включить цвета
        backtrace=True,  # Всегда включать подробный стектрейс (если есть)
        diagnose=True,  # Включать значения переменных в стектрейс (может быть медленно)
        format="<blue>{time:HH:mm:ss}</blue> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> | <level>{message}</level>"
    )


def add_serialize():
    # Структурированное логирование (JSON) - ИДЕАЛЬНО для Docker и систем агрегации:
    log.add(
        sys.stderr,  # Вывод в stderr (стандарт для Docker)
        level="TRACE",
        serialize=True  # Вывод в формате JSON
    )


def log_test():
    log.trace("Это сообщение для отладки (по умолчанию не видно)")
    log.debug("Это сообщение для отладки (по умолчанию не видно)")
    log.info("Какая-то информационная заметка")
    log.warning("Предупреждение, что-то может пойти не так")
    log.error("Произошла ошибка, но программа может продолжать работу")
    log.critical("Критическая ошибка, программа, скорее всего, упадет")

    try:
        variable = 0
        result = 1 / variable
    except ZeroDivisionError:
        log.exception("Произошло исключение!")  # Автоматически добавит стектрейс


# Переменная LOG_LEVEL может быть установлена в .env файле или в системе
log.remove()
add_stdout()
