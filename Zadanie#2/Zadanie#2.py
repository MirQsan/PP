import os
import shutil
import datetime


def set_working_directory(path):
    try:
        os.chdir(path)
        print(f'Рабочая папка изменена на: {path}')
    except FileNotFoundError:
        print('Указанной папки не существует!')


def create_file(name, text=None):
    with open(name, 'w', encoding='utf-8') as f:
        if text:
            f.write(text)


def create_folder(name):
    try:
        os.mkdir(name)
    except FileExistsError:
        print('Такая папка уже есть!')


def get_list(folders_only=False):
    result = os.listdir()
    if folders_only:
        result = [f for f in result if os.path.isdir(f)]
    print(result)


def delete_file(name):
    if os.path.isdir(name):
        os.rmdir(name)
    else:
        os.remove(name)


def copy_file(name, new_name):
    if os.path.isdir(name):
        try:
            shutil.copytree(name, new_name)
        except FileExistsError:
            print('Такая папка уже есть!')
    else:
        shutil.copy(name, new_name)


def move_file(name, new_location):
    if os.path.isdir(name):
        try:
            shutil.move(name, new_location)
        except FileNotFoundError:
            print('Такой папки не существует!')
    else:
        try:
            shutil.move(name, new_location)
        except FileNotFoundError:
            print('Такого файла не существует!')


def rename_file(name, new_name):
    try:
        os.rename(name, new_name)
    except FileNotFoundError:
        print('Такого файла не существует!')


def read_file(name):
    try:
        with open(name, 'r', encoding='utf-8') as f:
            content = f.read()
            print(content)
    except FileNotFoundError:
        print('Такого файла не существует!')


def save_info(message):
    current_time = datetime.datetime.now()
    result = f'{current_time} - {message}'
    with open('log.txt', 'a', encoding='utf-8') as f:
        f.write(result + '\n')


def print_help():
    print("Доступные команды:")
    print("1. cd <directory_path> - Изменить рабочий каталог")
    print("2. cf <file_name> [<text>] - Создать файл")
    print("3. mkdir <directory_name> - Создать папку")
    print("4. ls - Список файлов и папок")
    print("5. rm <file_name> - Удалить файл или папку")
    print("6. cp <source> <destination> - Скопировать файл или папку")
    print("7. mv <source> <destination> - Переместить файл или папку")
    print("8. rn <old_name> <new_name> - Переименовать файл или папку")
    print("9. cat <file_name> - Прочитать файл")
    print("10. exit - Выйти из файлового менеджера")


if __name__ == '__main__':
    print("Добро пожаловать в Mir File Manager!")
    print_help()

    while True:
        command = input("Введите команду: ").split()

        if not command:
            continue

        if command[0] == 'exit':
            print("Завершение...")
            break

        if command[0] == 'cd':
            if len(command) == 2:
                set_working_directory(command[1])
            else:
                print("Неверная команда! Используйте: cd <directory_path>")

        elif command[0] == 'cf':
            if len(command) >= 2:
                create_file(command[1], ' '.join(command[2:]))
            else:
                print("Неверная команда! Используйте: cf <file_name> [<text>]")

        elif command[0] == 'mkdir':
            if len(command) == 2:
                create_folder(command[1])
            else:
                print("Неверная команда! Используйте: mkdir <directory_name>")

        elif command[0] == 'ls':
            get_list()

        elif command[0] == 'rm':
            if len(command) == 2:
                delete_file(command[1])
            else:
                print("Неверная команда! Используйте: rm <file_name>")

        elif command[0] == 'cp':
            if len(command) == 3:
                copy_file(command[1], command[2])
            else:
                print("Неверная команда! Используйте: cp <source> <destination>")

        elif command[0] == 'mv':
            if len(command) == 3:
                move_file(command[1], command[2])
            else:
                print("Неверная команда! Используйте: mv <source> <destination>")

        elif command[0] == 'rn':
            if len(command) == 3:
                rename_file(command[1], command[2])
            else:
                print("Неверная команда! Используйте: rn <old_name> <new_name>")

        elif command[0] == 'cat':
            if len(command) == 2:
                read_file(command[1])
            else:
                print("Неверная команда! Используйте: cat <file_name>")

        else:
            print("Неверная команда! Введите 'help' для поиска доступных команд.")
