from pathlib import Path
from .logger import logger
import shutil
import zipfile

class DirectoryManager:
    def __init__(self, base_directory=None):
        """
        Инициализация класса DirectoryManager с базовой директорией.
        Если базовая директория не указана, используется текущая рабочая директория.
        """
        self.base_dir = Path(base_directory) if base_directory else Path.cwd()
        logger.info(f"Директория {self.base_dir} создана")

    def create_dir(self, directory: Path) -> None:
        """
        Создает указанную директорию, если она не существует.
        :param directory: Путь к создаваемой директории.
        """
        if self._is_inside_base_directory(directory):
            if not directory.exists():
                directory.mkdir(parents=True, exist_ok=True)
                logger.info(f"Директория {directory} создана")
            else:
                logger.warning(f"Директория {directory} уже создана")
        else:
            logger.warning(f"Директория {directory} не лежит в базовой директории {self.base_dir}")

    def _is_inside_base_directory(self, target_path: Path) -> bool:
        """
        Проверяет, находится ли указанный путь внутри базовой директории.
        :param target_path: Путь, который нужно проверить.
        :return: True, если путь внутри базовой директории, иначе False.
        """
        return target_path.resolve().is_relative_to(self.base_dir.resolve())

    def list_dir(self, directory: Path) -> list[Path]:
        """
        Возвращает список файлов и папок в указанной директории.
        :param directory: Путь к директории
        :return: Список путей внутри директории
        """
        if not self._is_inside_base_directory(directory):
            logger.warning(f"Директория {directory} не лежит в базовой директории {self.base_dir}")
            return []

        if not directory.exists():
            logger.warning(f"Директория {directory} не существует")
            return []

        if not directory.is_dir():
            logger.warning(f"{directory} — это не директория")
            return []

        items = list(directory.iterdir())
        logger.info(f"Содержимое {directory}: {[item.name for item in items]}")
        return items

    def copy_contents(self, src: Path, dst: Path, extensions: list[str] = None) -> None:
        """
        Копирует содержимое директории src в директорию dst,
        сохраняя вложенные папки и файлы. Можно указать фильтр по расширениям.

        :param src: Путь к исходной директории
        :param dst: Путь к целевой директории (будет создана при необходимости)
        :param extensions: Список разрешённых расширений файлов (например: [".c", ".h"]).
                           Если None — копируются все файлы.
        """
        if not self._is_inside_base_directory(src) or not self._is_inside_base_directory(dst):
            logger.warning(f"Один из путей не находится в пределах {self.base_dir}")
            return

        if not src.exists() or not src.is_dir():
            logger.warning(f"Исходная директория {src} не существует или не является директорией")
            return

        dst.mkdir(parents=True, exist_ok=True)

        for item in src.iterdir():
            target = dst / item.name

            # Обработка поддиректорий — копируем рекурсивно
            if item.is_dir():
                self.copy_contents(item, target, extensions)
            else:
                # Если расширения указаны, проверяем подходит ли
                if extensions is not None and item.suffix not in extensions:
                    logger.info(f"Пропущен файл {item.name} (не подходит по расширению)")
                    continue
                try:
                    shutil.copy2(item, target)
                    logger.info(f"Скопировано: {item} → {target}")
                except Exception as e:
                    logger.error(f"Ошибка при копировании {item}: {e}")

    def copy_flat(self, src: Path, dst: Path, extensions: list[str] = None) -> None:
        """
        Копирует все файлы из src и всех вложенных папок в dst без сохранения иерархии.
        Можно указать фильтр по расширениям (например: [".c", ".h"]).

        :param src: Исходная директория
        :param dst: Целевая директория
        :param extensions: Список допустимых расширений файлов (если None — копируются все)
        """
        if not self._is_inside_base_directory(src) or not self._is_inside_base_directory(dst):
            logger.warning(f"Один из путей не находится в пределах {self.base_dir}")
            return

        if not src.exists() or not src.is_dir():
            logger.warning(f"Исходная директория {src} не существует или не является директорией")
            return

        dst.mkdir(parents=True, exist_ok=True)

        # Обход всех файлов во всех вложенных папках
        for file in src.rglob("*"):
            if file.is_file():
                # Фильтрация по расширениям
                if extensions is not None and file.suffix not in extensions:
                    logger.info(f"Пропущен файл {file.name} (не подходит по расширению)")
                    continue
                try:
                    target = dst / file.name
                    shutil.copy2(file, target)
                    logger.info(f"Скопировано: {file} → {target}")
                except Exception as e:
                    logger.error(f"Ошибка при копировании {file}: {e}")

    def copy_file(self, src_file: Path, dst_dir: Path) -> None:
        """
        Копирует один файл в указанную директорию.

        :param src_file: Путь к исходному файлу
        :param dst_dir: Папка, в которую нужно скопировать файл
        """
        if not self._is_inside_base_directory(src_file) or not self._is_inside_base_directory(dst_dir):
            logger.warning(f"Путь вне базовой директории: {src_file} или {dst_dir}")
            return

        if not src_file.exists() or not src_file.is_file():
            logger.warning(f"{src_file} не существует или не является файлом")
            return

        try:
            dst_dir.mkdir(parents=True, exist_ok=True)
            target_path = dst_dir / src_file.name
            shutil.copy2(src_file, target_path)
            logger.info(f"Файл скопирован: {src_file} → {target_path}")
        except Exception as e:
            logger.error(f"Ошибка при копировании файла {src_file}: {e}")

    def delete_path(self, path: Path) -> None:
        """
        Удаляет указанный файл или директорию (рекурсивно).
        Корневая base_dir не удаляется — только её содержимое.

        :param path: Путь к файлу или директории
        """
        if not self._is_inside_base_directory(path):
            logger.warning(f"Попытка удалить вне базовой директории: {path}")
            return

        # Не позволяем удалить сам base_dir
        if path.resolve() == self.base_dir.resolve():
            logger.warning(f"Удаление base_dir запрещено: {path}")
            return

        if not path.exists():
            logger.warning(f"Путь не существует: {path}")
            return

        try:
            if path.is_dir():
                shutil.rmtree(path)
                logger.info(f"Директория удалена: {path}")
            else:
                path.unlink()
                logger.info(f"Файл удалён: {path}")
        except Exception as e:
            logger.error(f"Ошибка при удалении {path}: {e}")

    def create_file(self, path: Path, content: str = "", overwrite: bool = False) -> None:
        """
        Создаёт файл по указанному пути с заданным содержимым.
        При необходимости создаёт директории.

        :param path: Путь к создаваемому файлу
        :param content: Строка, которая будет записана в файл
        :param overwrite: Если False — не затирать существующий файл
        """
        if not self._is_inside_base_directory(path):
            logger.warning(f"Попытка создать файл вне базовой директории: {path}")
            return

        if path.exists() and not overwrite:
            logger.warning(f"Файл уже существует и не будет перезаписан: {path}")
            return

        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("w", encoding="utf-8") as f:
                f.write(content)
            logger.info(f"Файл создан: {path}")
        except Exception as e:
            logger.error(f"Ошибка при создании файла {path}: {e}")

    def delete_file(self, path: Path) -> None:
        """
        Удаляет указанный файл.

        :param path: Путь к удаляемому файлу
        """
        if not self._is_inside_base_directory(path):
            logger.warning(f"Попытка удалить файл вне базовой директории: {path}")
            return

        if not path.exists():
            logger.warning(f"Файл не существует: {path}")
            return

        if not path.is_file():
            logger.warning(f"{path} не является файлом")
            return

        try:
            path.unlink()
            logger.info(f"Файл удалён: {path}")
        except Exception as e:
            logger.error(f"Ошибка при удалении файла {path}: {e}")

    def clear_dir(self, directory: Path) -> None:
        """
        Удаляет всё содержимое указанной директории, но не саму директорию.

        :param directory: Путь к директории
        """
        if not self._is_inside_base_directory(directory):
            logger.warning(f"Попытка очистить вне базовой директории: {directory}")
            return

        if not directory.exists() or not directory.is_dir():
            logger.warning(f"Папка {directory} не существует или не является директорией")
            return

        for item in directory.iterdir():
            try:
                if item.is_dir():
                    shutil.rmtree(item)
                    logger.info(f"Удалена папка: {item}")
                else:
                    item.unlink()
                    logger.info(f"Удалён файл: {item}")
            except Exception as e:
                logger.error(f"Ошибка при удалении {item}: {e}")

    def zip_dir(self, src: Path, archive_path: Path) -> None:
        """
        Архивирует содержимое директории src в zip-архив archive_path.
        :param src: Путь к архивируемой директории
        :param archive_path: Путь к создаваемому .zip-файлу
        """
        if not self._is_inside_base_directory(src) or not self._is_inside_base_directory(archive_path):
            logger.warning(f"Один из путей вне базовой директории: {src} или {archive_path}")
            return

        if not src.exists() or not src.is_dir():
            logger.warning(f"Источник {src} не существует или не является директорией")
            return

        try:
            archive_path.parent.mkdir(parents=True, exist_ok=True)
            with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as zipf:
                for file in src.rglob("*"):
                    zipf.write(file, file.relative_to(src))
            logger.info(f"Создан архив: {archive_path}")
        except Exception as e:
            logger.error(f"Ошибка при архивировании {src}: {e}")

    def unzip(self, archive_path: Path, extract_to: Path) -> None:
        """
        Распаковывает zip-архив в указанную директорию.
        :param archive_path: Путь к .zip-файлу
        :param extract_to: Папка, куда будет выполнена распаковка
        """
        if not self._is_inside_base_directory(archive_path) or not self._is_inside_base_directory(extract_to):
            logger.warning(f"Один из путей вне базовой директории: {archive_path} или {extract_to}")
            return

        if not archive_path.exists() or not zipfile.is_zipfile(archive_path):
            logger.warning(f"{archive_path} не существует или не является .zip-архивом")
            return

        try:
            extract_to.mkdir(parents=True, exist_ok=True)
            with zipfile.ZipFile(archive_path, "r") as zipf:
                zipf.extractall(extract_to)
            logger.info(f"Архив {archive_path} распакован в {extract_to}")
        except Exception as e:
            logger.error(f"Ошибка при распаковке {archive_path}: {e}")

    def rename(self, old_path: Path, new_path: Path) -> None:
        """
        Переименовывает файл или директорию внутри base_dir.

        :param old_path: Текущий путь
        :param new_path: Новый путь
        """
        if not self._is_inside_base_directory(old_path) or not self._is_inside_base_directory(new_path):
            logger.warning(f"Один из путей вне базовой директории: {old_path} → {new_path}")
            return

        if not old_path.exists():
            logger.warning(f"Исходный путь не существует: {old_path}")
            return

        try:
            old_path.rename(new_path)
            logger.info(f"Переименовано: {old_path} → {new_path}")
        except Exception as e:
            logger.error(f"Ошибка при переименовании {old_path}: {e}")