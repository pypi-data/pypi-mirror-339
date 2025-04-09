# directory_manager

`directory_manager` — удобная библиотека для управления файлами и директориями в Python.

Она предоставляет готовые инструменты для:
- создания и удаления директорий и файлов
- копирования с фильтрацией по расширениям
- очистки директорий без удаления самих папок
- архивирования и разархивирования `.zip`
- логирования всех операций

## Установка
```bash
pip install directory_manager
```

## Пример
```python
from directory_manager import DirectoryManager
from pathlib import Path

dm = DirectoryManager("workspace")

# Создание папки и файла
dm.create_dir(Path("workspace/new_folder"))
dm.create_file(Path("workspace/new_folder/example.txt"), "Привет, мир!")

# Копирование всех .txt файлов без вложенности
dm.copy_flat(Path("workspace"), Path("backup"), extensions=[".txt"])

# Архивация
dm.zip_dir(Path("workspace"), Path("workspace.zip"))

# Очистка папки
dm.clear_dir(Path("workspace"))
```