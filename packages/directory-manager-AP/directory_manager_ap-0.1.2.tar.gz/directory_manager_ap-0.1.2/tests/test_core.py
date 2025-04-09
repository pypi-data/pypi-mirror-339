import zipfile
from unittest.mock import patch
from directory_manager_AP import DirectoryManager

# Метод create_dir
# === Тест: создание новой директории ===
def test_create_new_directory(tmp_path):
    dm = DirectoryManager(base_directory=tmp_path)
    test_dir = tmp_path / "my_folder"
    # Убеждаемся, что папка ещё не существует
    assert not test_dir.exists()
    # Пытаемся создать папку
    dm.create_dir(test_dir)
    # Проверяем, что папка появилась и это действительно директория
    assert test_dir.exists()
    assert test_dir.is_dir()

# Метод create_dir
# === Тест: создание уже существующей директории ===
def test_create_existing_directory(tmp_path):
    dm = DirectoryManager(base_directory=tmp_path)
    test_dir = tmp_path / "already_here"
    test_dir.mkdir()
    # Предварительно создаём папку вручную
    assert test_dir.exists()
    # Повторный вызов метода create_dir не должен вызвать ошибку
    dm.create_dir(test_dir)
    # Убеждаемся, что папка всё ещё существует
    assert test_dir.exists()

# Метод create_dir
# === Тест: попытка создать директорию вне base_directory ===
def test_create_outside_base_directory(tmp_path):
    dm = DirectoryManager(base_directory=tmp_path)
    outside_dir = tmp_path.parent / "evil_folder"
    assert not outside_dir.exists()
    # Папка вне базовой директории не должна быть создана
    dm.create_dir(outside_dir)
    assert not outside_dir.exists() # Не должна создаться

# Метод _is_inside_base_directory
# === Тест: проверка _is_inside_base_directory для допустимого пути ===
def test_is_inside_base_directory_true(tmp_path):
    dm = DirectoryManager(base_directory=tmp_path)
    inside_path = tmp_path / "nested"
    # Проверка должна вернуть True
    assert dm._is_inside_base_directory(inside_path)

# Метод _is_inside_base_directory
# === Тест: проверка _is_inside_base_directory для внешнего пути ===
def test_is_inside_base_directory_false(tmp_path):
    dm = DirectoryManager(base_directory=tmp_path)
    outside_path = tmp_path.parent / "outside"
    # Проверка должна вернуть False
    assert not dm._is_inside_base_directory(outside_path)

# Метод list_dir
# === Тест: чтение содержимого директории с файлами ===
def test_list_dir_with_files(tmp_path):
    dm = DirectoryManager(base_directory=tmp_path)
    test_dir = tmp_path / "data"
    test_dir.mkdir()

    # Создаем два тестовых файла
    (test_dir / "file1.txt").write_text("Hello")
    (test_dir / "file2.txt").write_text("World")

    # Получаем содержимое директории
    contents = dm.list_dir(test_dir)

    # Проверяем, что найдено ровно два файла с нужными именами
    assert len(contents) == 2
    names = [p.name for p in contents]
    assert "file1.txt" in names
    assert "file2.txt" in names

# Метод list_dir
# === Тест: чтение пустой директории ===
def test_list_dir_empty(tmp_path):
    dm = DirectoryManager(base_directory=tmp_path)
    empty_dir = tmp_path / "empty"
    empty_dir.mkdir()

    # Пустая директория должна возвращать пустой список
    contents = dm.list_dir(empty_dir)
    assert contents == []

# Метод list_dir
# === Тест: чтение несуществующей директории ===
def test_list_dir_non_existing(tmp_path):
    dm = DirectoryManager(base_directory=tmp_path)
    missing_dir = tmp_path / "no_such_dir"

    # Метод не должен падать и должен вернуть пустой список
    contents = dm.list_dir(missing_dir)
    assert contents == []

# Метод list_dir
# === Тест: передан файл вместо директории ===
def test_list_dir_given_file(tmp_path):
    dm = DirectoryManager(base_directory=tmp_path)
    file_path = tmp_path / "some_file.txt"
    file_path.write_text("I'm not a folder")

    # Метод должен вернуть пустой список и не вызывать ошибку
    contents = dm.list_dir(file_path)
    assert contents == []

# Метод list_dir
# === Тест: попытка чтения директории вне base_directory ===
def test_list_dir_outside_base_directory(tmp_path):
    dm = DirectoryManager(base_directory=tmp_path)
    outside_dir = tmp_path.parent / "evil_folder"
    outside_dir.mkdir()

    # Метод должен отказать в доступе и вернуть []
    contents = dm.list_dir(outside_dir)
    assert contents == []

# Метод copy_contents
# === Тест: копирование всех файлов без фильтра ===
def test_copy_all_files(tmp_path):
    dm = DirectoryManager(base_directory=tmp_path)
    src = tmp_path / "src"
    dst = tmp_path / "dst"
    src.mkdir()

    # Создаем тестовые файлы
    (src / "a.c").write_text("int main() {}")
    (src / "b.h").write_text("#pragma once")
    (src / "c.txt").write_text("text file")

    # Копируем всё
    dm.copy_contents(src, dst)

    # Проверка: все 3 файла скопированы
    files = {f.name for f in dst.iterdir()}
    assert files == {"a.c", "b.h", "c.txt"}

# Метод copy_contents
# === Тест: копирование только .c и .h файлов ===
def test_copy_filtered_files(tmp_path):
    dm = DirectoryManager(base_directory=tmp_path)
    src = tmp_path / "src"
    dst = tmp_path / "dst"
    src.mkdir()

    # Создаем разные файлы
    (src / "main.c").write_text("// C code")
    (src / "defs.h").write_text("// Header")
    (src / "readme.md").write_text("Markdown")

    # Копируем только .c и .h
    dm.copy_contents(src, dst, extensions=[".c", ".h"])

    # Проверка: только два нужных файла
    files = {f.name for f in dst.iterdir()}
    assert files == {"main.c", "defs.h"}

# Метод copy_contents
# === Тест: игнорируются файлы с неподходящим расширением ===
def test_skip_unwanted_extensions(tmp_path):
    dm = DirectoryManager(base_directory=tmp_path)
    src = tmp_path / "src"
    dst = tmp_path / "dst"
    src.mkdir()

    (src / "file.py").write_text("print('hi')")
    (src / "file.c").write_text("int main(){}")

    # Только .c разрешено
    dm.copy_contents(src, dst, extensions=[".c"])

    files = {f.name for f in dst.iterdir()}
    assert files == {"file.c"}

# Метод copy_contents
# === Тест: копирование вложенных директорий с фильтрацией ===
def test_copy_nested_structure(tmp_path):
    dm = DirectoryManager(base_directory=tmp_path)
    src = tmp_path / "project"
    dst = tmp_path / "backup"
    src.mkdir()

    # Создаем вложенную папку и файлы
    nested = src / "src"
    nested.mkdir()
    (nested / "module.c").write_text("...")
    (nested / "note.txt").write_text("...")

    # Копируем только .c
    dm.copy_contents(src, dst, extensions=[".c"])

    # Проверка: структура сохранена, а файл .txt не скопирован
    copied_nested = dst / "src"
    assert (copied_nested / "module.c").exists()
    assert not (copied_nested / "note.txt").exists()

# Метод copy_contents
def test_copy_contents_src_outside_base(tmp_path):
    dm = DirectoryManager(base_directory=tmp_path)

    # src вне base_dir
    src = tmp_path.parent / "not_allowed"
    src.mkdir()
    dst = tmp_path / "dst"

    dm.copy_contents(src, dst)

    # dst не должен быть создан
    assert not dst.exists()

# Метод copy_contents
def test_copy_contents_src_does_not_exist(tmp_path):
    dm = DirectoryManager(base_directory=tmp_path)

    # src внутри base_dir, но не существует
    src = tmp_path / "missing"
    dst = tmp_path / "dst"

    dm.copy_contents(src, dst)

    # Ничего не скопировано
    assert not dst.exists()

# Метод copy_contents
# === Тест: ошибка при копировании файла → покрытие блока except ===
def test_copy_contents_copy2_raises_exception(tmp_path):
    dm = DirectoryManager(base_directory=tmp_path)

    # Создаем исходную папку с одним файлом
    src = tmp_path / "src"
    src.mkdir()
    file = src / "fail.txt"
    file.write_text("test")

    dst = tmp_path / "dst"

    # Мокаем shutil.copy2 так, чтобы он выбрасывал исключение
    with patch("shutil.copy2", side_effect=OSError("copy failed")):
        dm.copy_contents(src, dst)

    # Убедимся, что целевая директория создана, но файл не скопирован
    assert dst.exists()
    assert not (dst / "fail.txt").exists()

# Метод copy_flat
# === Тест: копирование всех файлов без сохранения структуры ===
def test_copy_flat_all_files(tmp_path):
    dm = DirectoryManager(base_directory=tmp_path)
    src = tmp_path / "src"
    dst = tmp_path / "flat"
    nested = src / "subdir"
    nested.mkdir(parents=True)

    # Создаем файлы в корне и во вложенной папке
    (src / "a.c").write_text("C file")
    (nested / "b.h").write_text("Header")
    (nested / "note.txt").write_text("Just text")

    # Копируем все файлы в одну папку
    dm.copy_flat(src, dst)

    # Проверка: все 3 файла должны быть в целевой папке
    files = {f.name for f in dst.iterdir()}
    assert files == {"a.c", "b.h", "note.txt"}

# Метод copy_flat
# === Тест: копирование только .c и .h файлов ===
def test_copy_flat_filtered_files(tmp_path):
    dm = DirectoryManager(base_directory=tmp_path)
    src = tmp_path / "src"
    dst = tmp_path / "flat"
    src.mkdir()

    # Создаем файлы разных типов
    (src / "main.c").write_text("// c code")
    (src / "defs.h").write_text("// header")
    (src / "info.md").write_text("markdown")

    # Копируем только .c и .h
    dm.copy_flat(src, dst, extensions=[".c", ".h"])

    # Проверка: скопированы только разрешённые файлы
    files = {f.name for f in dst.iterdir()}
    assert files == {"main.c", "defs.h"}

# Метод copy_flat
# === Тест: вложенная структура не сохраняется ===
def test_copy_flat_structure_is_flat(tmp_path):
    dm = DirectoryManager(base_directory=tmp_path)
    src = tmp_path / "src"
    dst = tmp_path / "flat"
    deep = src / "nested" / "very_deep"
    deep.mkdir(parents=True)

    # Создаем файл глубоко внутри
    (deep / "deep_file.c").write_text("...")

    # Копируем всё
    dm.copy_flat(src, dst)

    # Проверка: файл оказался прямо в целевой папке, без структуры
    flat_file = dst / "deep_file.c"
    assert flat_file.exists()

# Метод copy_flat
# === Тест: при совпадении имён происходит перезапись ===
def test_copy_flat_overwrites_files(tmp_path):
    dm = DirectoryManager(base_directory=tmp_path)
    src = tmp_path / "src"
    dst = tmp_path / "flat"
    src.mkdir()
    dst.mkdir()

    # Создаем одинаково названные файлы в разных папках
    (src / "same.c").write_text("from src")
    (dst / "same.c").write_text("old content")

    # Копируем
    dm.copy_flat(src, dst, extensions=[".c"])

    # Проверка: файл был перезаписан
    with (dst / "same.c").open() as f:
        content = f.read()
    assert content == "from src"

# Метод copy_flat
# === Тест: копирование вне базовой директории (src) ===
def test_copy_flat_src_outside_base(tmp_path):
    dm = DirectoryManager(base_directory=tmp_path)

    src = tmp_path.parent / "outside_src"
    dst = tmp_path / "dst"
    src.mkdir()

    dm.copy_flat(src, dst)

    # Проверяем: dst не создан, ничего не скопировано
    assert not dst.exists()

# Метод copy_flat
# === Тест: src не существует или не является директорией ===
def test_copy_flat_src_does_not_exist(tmp_path):
    dm = DirectoryManager(base_directory=tmp_path)

    src = tmp_path / "missing"
    dst = tmp_path / "dst"

    dm.copy_flat(src, dst)

    # Целевая папка не создаётся
    assert not dst.exists()

# Метод copy_flat
# === Тест: ошибка при копировании файла (copy_flat) → покрытие except ===
def test_copy_flat_copy2_raises_exception(tmp_path):
    dm = DirectoryManager(base_directory=tmp_path)

    src = tmp_path / "src"
    dst = tmp_path / "dst"
    src.mkdir()
    (src / "bad.txt").write_text("fail")

    # Мокаем shutil.copy2 чтобы выбросить исключение
    with patch("shutil.copy2", side_effect=OSError("flat copy fail")):
        dm.copy_flat(src, dst)

    # Убеждаемся, что файл не был скопирован
    assert not (dst / "bad.txt").exists()

# Метод copy_file
# === Тест: копирование одного файла в директорию ===
def test_copy_single_file(tmp_path):
    dm = DirectoryManager(base_directory=tmp_path)

    # Создаём исходный файл и целевую папку
    src_file = tmp_path / "main.c"
    dst_dir = tmp_path / "backup"
    src_file.write_text("int main() {}")

    # Копируем файл
    dm.copy_file(src_file, dst_dir)

    # Проверка: файл скопирован в целевую папку
    copied_file = dst_dir / "main.c"
    assert copied_file.exists()
    assert copied_file.read_text() == "int main() {}"

# Метод copy_file
# === Тест: целевая директория создаётся автоматически ===
def test_copy_file_creates_target_dir(tmp_path):
    dm = DirectoryManager(base_directory=tmp_path)

    # Исходный файл
    src_file = tmp_path / "utils.h"
    src_file.write_text("#pragma once")

    # Целевая папка не существует
    dst_dir = tmp_path / "nested" / "include"

    # Копирование должно создать папку и скопировать файл
    dm.copy_file(src_file, dst_dir)
    assert (dst_dir / "utils.h").exists()

# Метод copy_file
# === Тест: если исходный файл не существует — ничего не копируется ===
def test_copy_file_nonexistent(tmp_path):
    dm = DirectoryManager(base_directory=tmp_path)

    # Не существующий файл
    src_file = tmp_path / "ghost.c"
    dst_dir = tmp_path / "dst"

    # Попытка копирования — не должна вызвать ошибку
    dm.copy_file(src_file, dst_dir)

    # Убедимся, что целевая папка не была создана
    assert not dst_dir.exists()

# Метод copy_file
# === Тест: попытка скопировать директорию как файл — должна быть проигнорирована ===
def test_copy_file_given_directory(tmp_path):
    dm = DirectoryManager(base_directory=tmp_path)

    src_dir = tmp_path / "not_a_file"
    src_dir.mkdir()

    dst_dir = tmp_path / "target"

    # Попытка скопировать папку как файл
    dm.copy_file(src_dir, dst_dir)

    # Папка должна остаться пустой
    assert not dst_dir.exists()

# Метод copy_file
# === Тест: копирование вне base_directory запрещено ===
def test_copy_file_outside_base(tmp_path):
    dm = DirectoryManager(base_directory=tmp_path)

    # Файл вне base_dir
    src = tmp_path.parent / "outside.c"
    src.write_text("bad")

    dst = tmp_path / "here"

    # Попытка копировать вне base_dir
    dm.copy_file(src, dst)

    # Ничего не должно быть скопировано
    assert not dst.exists()

# Метод copy_file
def test_copy_file_copy2_raises_exception(tmp_path):
    dm = DirectoryManager(base_directory=tmp_path)

    src_file = tmp_path / "source.txt"
    dst_dir = tmp_path / "dest"

    src_file.write_text("data")

    with patch("shutil.copy2", side_effect=OSError("copy file fail")):
        dm.copy_file(src_file, dst_dir)

    assert not (dst_dir / "source.txt").exists()

# Метод delete_path
# === Тест: удаление обычного файла ===
def test_delete_file(tmp_path):
    dm = DirectoryManager(base_directory=tmp_path)

    # Создаём файл
    file_path = tmp_path / "delete_me.txt"
    file_path.write_text("bye")

    assert file_path.exists()

    # Удаляем файл
    dm.delete_path(file_path)

    # Файл должен исчезнуть
    assert not file_path.exists()

# Метод delete_path
# === Тест: удаление директории рекурсивно ===
def test_delete_directory(tmp_path):
    dm = DirectoryManager(base_directory=tmp_path)

    # Создаём папку с вложенными файлами
    dir_path = tmp_path / "folder"
    dir_path.mkdir()
    (dir_path / "a.txt").write_text("test")
    (dir_path / "b.txt").write_text("test")

    assert dir_path.exists()

    # Удаляем папку
    dm.delete_path(dir_path)

    # Папка и всё её содержимое должно исчезнуть
    assert not dir_path.exists()

# Метод delete_path
# === Тест: попытка удалить несуществующий путь ===
def test_delete_nonexistent_path(tmp_path):
    dm = DirectoryManager(base_directory=tmp_path)
    ghost = tmp_path / "not_here.txt"

    # Метод не должен упасть, просто ничего не делает
    dm.delete_path(ghost)

    # Убеждаемся, что ничего не появилось
    assert not ghost.exists()

# Метод delete_path
# === Тест: попытка удалить базовую директорию — запрещено ===
def test_delete_base_directory(tmp_path):
    dm = DirectoryManager(base_directory=tmp_path)

    # Метод должен отказать в удалении base_dir
    dm.delete_path(tmp_path)

    # base_dir должен остаться на месте
    assert tmp_path.exists()
    assert tmp_path.is_dir()

# Метод delete_path
# === Тест: попытка удалить путь вне base_dir — запрещено ===
def test_delete_outside_base(tmp_path):
    dm = DirectoryManager(base_directory=tmp_path)

    # Создаём внешний файл
    external = tmp_path.parent / "external.txt"
    external.write_text("I am outside")

    dm.delete_path(external)

    # Он должен остаться, потому что вне base_dir
    assert external.exists()

# Метод delete_path
# === Тест: ошибка при удалении директории (delete_path) → покрытие except ===
def test_delete_path_raises_exception(tmp_path):
    dm = DirectoryManager(base_directory=tmp_path)

    path = tmp_path / "folder"
    path.mkdir()

    # Мокаем shutil.rmtree чтобы выбросить исключение
    with patch("shutil.rmtree", side_effect=OSError("delete fail")):
        dm.delete_path(path)

    # Путь остаётся (удаление не произошло)
    assert path.exists()

# Метод create_file
# === Тест: создание нового файла ===
def test_create_file(tmp_path):
    dm = DirectoryManager(base_directory=tmp_path)
    file_path = tmp_path / "folder" / "test.txt"

    # Убедимся, что файла ещё нет
    assert not file_path.exists()

    # Создаём файл с текстом
    dm.create_file(file_path, content="Hello, world!")

    # Проверяем, что файл появился и содержит нужный текст
    assert file_path.exists()
    assert file_path.read_text(encoding="utf-8") == "Hello, world!"

# Метод create_file
# === Тест: создание файла с автосозданием директории ===
def test_create_file_creates_directories(tmp_path):
    dm = DirectoryManager(base_directory=tmp_path)
    nested_path = tmp_path / "deep" / "more" / "file.txt"

    # Папка "deep/more" не существует
    assert not nested_path.parent.exists()

    # Метод должен сам создать папки
    dm.create_file(nested_path, content="Nested")

    assert nested_path.exists()
    assert nested_path.read_text(encoding="utf-8") == "Nested"

# Метод create_file
# === Тест: попытка перезаписать файл без флага overwrite ===
def test_create_file_no_overwrite(tmp_path):
    dm = DirectoryManager(base_directory=tmp_path)
    file_path = tmp_path / "keep.txt"

    # Создаём файл вручную
    file_path.write_text("Original")

    # Пытаемся перезаписать без флага — не должно измениться
    dm.create_file(file_path, content="Should not overwrite", overwrite=False)

    # Файл остался с оригинальным содержимым
    assert file_path.read_text(encoding="utf-8") == "Original"

# Метод create_file
# === Тест: перезапись файла с флагом overwrite ===
def test_create_file_with_overwrite(tmp_path):
    dm = DirectoryManager(base_directory=tmp_path)
    file_path = tmp_path / "replace.txt"
    file_path.write_text("Old content")

    # Перезаписываем файл
    dm.create_file(file_path, content="New content", overwrite=True)

    assert file_path.read_text(encoding="utf-8") == "New content"

# Метод create_file
# === Тест: попытка создать файл вне base_dir — запрещено ===
def test_create_file_outside_base_dir(tmp_path):
    dm = DirectoryManager(base_directory=tmp_path)
    outside_file = tmp_path.parent / "evil.txt"

    # Попытка должна проигнорироваться
    dm.create_file(outside_file, content="hack")

    # Файл не должен появиться
    assert not outside_file.exists()

# Метод create_file
def test_create_file_raises_exception(tmp_path):
    dm = DirectoryManager(base_directory=tmp_path)

    file_path = tmp_path / "fail.txt"

    # Мокаем open() чтобы выбросить исключение при записи
    with patch("pathlib.Path.open", side_effect=OSError("cannot write")):
        dm.create_file(file_path, content="data", overwrite=True)

    # Файл не должен быть создан
    assert not file_path.exists()

# Метод delete_file
# === Тест: удаление существующего файла ===
def test_delete_existing_file(tmp_path):
    dm = DirectoryManager(base_directory=tmp_path)
    file_path = tmp_path / "delete_me.txt"

    # Создаём файл
    file_path.write_text("temporary")

    # Убеждаемся, что он есть
    assert file_path.exists()

    # Удаляем файл
    dm.delete_file(file_path)

    # Проверка: файл исчез
    assert not file_path.exists()

# Метод delete_file
# === Тест: попытка удалить несуществующий файл ===
def test_delete_nonexistent_file(tmp_path):
    dm = DirectoryManager(base_directory=tmp_path)
    file_path = tmp_path / "not_here.txt"

    # Файл не существует, но метод не должен упасть
    dm.delete_file(file_path)

    # И всё ещё не существует
    assert not file_path.exists()

# Метод delete_file
# === Тест: попытка удалить директорию как файл ===
def test_delete_file_given_directory(tmp_path):
    dm = DirectoryManager(base_directory=tmp_path)
    dir_path = tmp_path / "folder"
    dir_path.mkdir()

    # Удаление папки как файла — не должно сработать
    dm.delete_file(dir_path)

    # Папка должна остаться
    assert dir_path.exists()
    assert dir_path.is_dir()

# Метод delete_file
# === Тест: попытка удалить файл вне base_dir ===
def test_delete_file_outside_base_dir(tmp_path):
    dm = DirectoryManager(base_directory=tmp_path)

    # Внешний файл
    outside_file = tmp_path.parent / "external.txt"
    outside_file.write_text("I am outside")

    # Попытка удалить должна быть заблокирована
    dm.delete_file(outside_file)

    # Файл остался
    assert outside_file.exists()

# Метод delete_file
def test_delete_file_raises_exception(tmp_path):
    dm = DirectoryManager(base_directory=tmp_path)

    path = tmp_path / "file.txt"
    path.write_text("data")

    # Мокаем unlink, чтобы выбросить исключение
    with patch("pathlib.Path.unlink", side_effect=OSError("unlink error")):
        dm.delete_file(path)

    # Файл всё ещё существует
    assert path.exists()

# Метод clear_dir
# === Тест: очистка папки с файлами и поддиректориями ===
def test_clear_directory_with_content(tmp_path):
    dm = DirectoryManager(base_directory=tmp_path)
    dir_path = tmp_path / "data"
    dir_path.mkdir()

    # Создаем файлы и поддиректорию внутри
    (dir_path / "a.txt").write_text("text")
    (dir_path / "b.log").write_text("log")
    subdir = dir_path / "sub"
    subdir.mkdir()
    (subdir / "deep.txt").write_text("nested")

    # Убедимся, что содержимое есть
    assert any(dir_path.iterdir())

    # Очищаем директорию
    dm.clear_dir(dir_path)

    # Директория осталась, но пуста
    assert dir_path.exists()
    assert dir_path.is_dir()
    assert list(dir_path.iterdir()) == []

# Метод clear_dir
# === Тест: очистка пустой директории — не вызывает ошибок ===
def test_clear_empty_directory(tmp_path):
    dm = DirectoryManager(base_directory=tmp_path)
    empty_dir = tmp_path / "empty"
    empty_dir.mkdir()

    dm.clear_dir(empty_dir)

    # Папка должна остаться пустой
    assert empty_dir.exists()
    assert list(empty_dir.iterdir()) == []

# Метод clear_dir
# === Тест: попытка очистить файл вместо папки ===
def test_clear_dir_given_file(tmp_path):
    dm = DirectoryManager(base_directory=tmp_path)
    file_path = tmp_path / "not_a_folder.txt"
    file_path.write_text("I'm a file")

    dm.clear_dir(file_path)

    # Файл не должен быть удалён
    assert file_path.exists()

# Метод clear_dir
# === Тест: попытка очистить путь вне base_dir ===
def test_clear_dir_outside_base(tmp_path):
    dm = DirectoryManager(base_directory=tmp_path)
    outside_dir = tmp_path.parent / "danger"
    outside_dir.mkdir()

    dm.clear_dir(outside_dir)

    # Папка вне base_dir — не тронута
    assert outside_dir.exists()

# Метод clear_dir
def test_clear_dir_raises_exception(tmp_path):
    dm = DirectoryManager(base_directory=tmp_path)

    dir_to_clear = tmp_path / "my_folder"
    dir_to_clear.mkdir()
    file = dir_to_clear / "bad.txt"
    file.write_text("boom")

    # Мокаем unlink, чтобы сработал except
    with patch("pathlib.Path.unlink", side_effect=OSError("cannot remove")):
        dm.clear_dir(dir_to_clear)

    # Файл остаётся внутри директории
    assert file.exists()

# Метод zip_dir
# === Тест: создание архива из директории ===
def test_zip_dir_creates_archive(tmp_path):
    dm = DirectoryManager(base_directory=tmp_path)

    # Подготавливаем исходную директорию и файлы
    src_dir = tmp_path / "to_zip"
    src_dir.mkdir()
    (src_dir / "a.txt").write_text("A")
    (src_dir / "b.txt").write_text("B")

    archive_path = tmp_path / "archive.zip"

    # Архивируем
    dm.zip_dir(src_dir, archive_path)

    # Проверка: zip-файл создан и корректный
    assert archive_path.exists()
    assert zipfile.is_zipfile(archive_path)

    # Проверка содержимого архива
    with zipfile.ZipFile(archive_path, "r") as zipf:
        names = zipf.namelist()
        assert "a.txt" in names
        assert "b.txt" in names

# Метод zip_dir
# === Тест: zip_dir не архивирует, если путь вне base_dir ===
def test_zip_dir_outside_base(tmp_path):
    dm = DirectoryManager(base_directory=tmp_path)

    # src внутри, archive вне
    src_dir = tmp_path / "stuff"
    src_dir.mkdir()
    archive_out = tmp_path.parent / "bad.zip"

    dm.zip_dir(src_dir, archive_out)

    # Ничего не создаётся
    assert not archive_out.exists()

# Метод zip_dir
# === Тест: архивируемая директория не существует ===
def test_zip_dir_src_does_not_exist(tmp_path):
    dm = DirectoryManager(base_directory=tmp_path)
    src = tmp_path / "no_such_dir"
    archive = tmp_path / "archive.zip"

    # Метод должен просто завершиться без создания архива
    dm.zip_dir(src, archive)

    assert not archive.exists()

# === Тест: при ошибке архивирования вызывается except ===
def test_zip_dir_raises_exception(tmp_path):
    dm = DirectoryManager(base_directory=tmp_path)

    src = tmp_path / "src"
    src.mkdir()
    (src / "a.txt").write_text("content")

    archive = tmp_path / "archive.zip"

    # Мокаем zipfile.ZipFile, чтобы вызвать исключение
    with patch("zipfile.ZipFile", side_effect=OSError("zip fail")):
        dm.zip_dir(src, archive)

    # Архив не создан
    assert not archive.exists()

# Метод unzip
# === Тест: распаковка архива в директорию ===
def test_unzip_extracts_contents(tmp_path):
    dm = DirectoryManager(base_directory=tmp_path)

    # Создаём архив вручную
    archive_path = tmp_path / "manual.zip"
    with zipfile.ZipFile(archive_path, "w") as zipf:
        zipf.writestr("dir1/file1.txt", "hello")
        zipf.writestr("dir2/file2.txt", "world")

    extract_to = tmp_path / "extracted"

    # Распаковываем архив
    dm.unzip(archive_path, extract_to)

    # Проверка: файлы распакованы
    assert (extract_to / "dir1" / "file1.txt").read_text() == "hello"
    assert (extract_to / "dir2" / "file2.txt").read_text() == "world"

# Метод unzip
# === Тест: unzip не извлекает, если архив вне base_dir ===
def test_unzip_outside_base(tmp_path):
    dm = DirectoryManager(base_directory=tmp_path)

    # Архив вне base_dir
    archive_path = tmp_path.parent / "bad.zip"
    with zipfile.ZipFile(archive_path, "w") as zipf:
        zipf.writestr("file.txt", "nope")

    extract_to = tmp_path / "here"

    dm.unzip(archive_path, extract_to)

    # Распаковки не произошло
    assert not extract_to.exists()

# Метод unzip
# === Тест: архив не существует или не является .zip ===
def test_unzip_invalid_archive(tmp_path):
    dm = DirectoryManager(base_directory=tmp_path)

    archive = tmp_path / "broken.zip"
    extract_to = tmp_path / "output"

    # Пишем туда текст, но это не zip-файл
    archive.write_text("not really zip")

    dm.unzip(archive, extract_to)

    # Распаковка не должна произойти
    assert not extract_to.exists()

# Метод unzip
# === Тест: ошибка при распаковке архива (unzip) → покрытие except ===
def test_unzip_extractall_raises_exception(tmp_path):
    dm = DirectoryManager(base_directory=tmp_path)

    archive = tmp_path / "test.zip"
    extract_to = tmp_path / "unpacked"

    # Создаем настоящий zip-файл
    with zipfile.ZipFile(archive, "w") as zipf:
        zipf.writestr("hello.txt", "data")

    # Мокаем extractall, чтобы вызвать ошибку
    with patch("zipfile.ZipFile.extractall", side_effect=OSError("unzip failed")):
        dm.unzip(archive, extract_to)

    # Папка может быть создана, но файл не должен быть распакован
    assert not (extract_to / "hello.txt").exists()

# Метод rename
# === Тест: успешное переименование файла ===
def test_rename_success(tmp_path):
    dm = DirectoryManager(base_directory=tmp_path)

    old_path = tmp_path / "old.txt"
    new_path = tmp_path / "new.txt"

    old_path.write_text("data")
    dm.rename(old_path, new_path)

    assert not old_path.exists()
    assert new_path.exists()
    assert new_path.read_text() == "data"


# === Тест: попытка переименовать файл вне base_dir ===
def test_rename_outside_base(tmp_path):
    dm = DirectoryManager(base_directory=tmp_path)

    outside = tmp_path.parent / "external.txt"
    outside.write_text("external")

    new_path = tmp_path / "renamed.txt"
    dm.rename(outside, new_path)

    # Файл не должен быть перемещён
    assert outside.exists()
    assert not new_path.exists()


# === Тест: попытка переименовать несуществующий файл ===
def test_rename_non_existing_file(tmp_path):
    dm = DirectoryManager(base_directory=tmp_path)

    missing = tmp_path / "missing.txt"
    new_path = tmp_path / "new_name.txt"

    dm.rename(missing, new_path)

    # Ничего не создано
    assert not new_path.exists()


# === Тест: ошибка при переименовании (искусственная) → покрытие except ===
def test_rename_raises_exception(tmp_path):
    dm = DirectoryManager(base_directory=tmp_path)

    old_path = tmp_path / "to_rename.txt"
    new_path = tmp_path / "new.txt"

    old_path.write_text("data")

    with patch("pathlib.Path.rename", side_effect=OSError("rename fail")):
        dm.rename(old_path, new_path)

    # Файл остаётся с прежним именем
    assert old_path.exists()
    assert not new_path.exists()