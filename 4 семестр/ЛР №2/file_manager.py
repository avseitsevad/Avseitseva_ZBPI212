import os
import shutil
from settings import WORKING_DIRECTORY

def create_folder(folder_name): #Создает новую папку в рабочей директории
    folder_path = os.path.join(WORKING_DIRECTORY, folder_name)
    if not os.path.exists(folder_path):
      os.mkdir(folder_path)
      print(f"Папка '{folder_name}' успешно создана")
     else:
      print("Папка с таким именем уже существует")

def delete_folder(folder_name): #Удаляет папку из рабочей директории
    folder_path = os.path.join(WORKING_DIRECTORY, folder_name)
    if os.path.exists(folder_path):
      os.rmdir(folder_path)
      print(f"Папка '{folder_name}' успешно удалена")
    else:
      print("Папки с таким именем не существует")

def change_directory(folder_name):
    # Изменяет рабочую директорию на указанную папку внутри текущей рабочей директории
    if folder_name == "..":
        # Переход на уровень вверх
        parent_directory = os.path.dirname(WORKING_DIRECTORY)
        if parent_directory != WORKING_DIRECTORY:
            WORKING_DIRECTORY = parent_directory
            print("Переход на уровень вверх выполнен")
        else:
            print("Невозможно перейти на уровень вверх")
    else:
        # Переход внутри текущей рабочей директории
        target_directory = os.path.join(WORKING_DIRECTORY, folder_name)
        if os.path.isdir(target_directory):
            WORKING_DIRECTORY = target_directory
            print(f"Переход в папку '{folder_name}' выполнен")
        else:
            print(f"Папка '{folder_name}' не существует")
            
def create_file(file_name): #Создает новый пустой файл в рабочей директории.
    file_path = os.path.join(WORKING_DIRECTORY, file_name)
    if not os.path.exists(file_path):
      with open(file_path, 'w'):
          pass
      print(f"Файл '{file_name}' успешно создан")
    else:
      print("Файл с таким именем уже существует")

def write_to_file(file_name, content): # Записывает текст в указанный файл.
    file_path = os.path.join(WORKING_DIRECTORY, file_name)
    if not os.path.exists(file_path):
      create_file(file_name)
    else:
      with open(file_path, 'w') as file:
          file.write(content)
      print(f"Текст успешно записан в файл '{file_name}'")

def view_file(file_name): # Выводит содержимое текстового файла
    file_path = os.path.join(WORKING_DIRECTORY, file_name)
    if os.path.isfile(file_path):
        with open(file_path, 'r') as file:
            content = file.read()
            print(f"Содержимое файла '{file_name}':")
            print(content)
    else:
        print(f"Файл '{file_name}' не существует")

def delete_file(file_name): # Удаляет файл из рабочей директории.
    file_path = os.path.join(WORKING_DIRECTORY, file_name)
    if os.path.isfile(file_path):
        os.remove(file_path)
        print(f"Файл '{file_name}' успешно удален")
    else:
        print("Файла с таким именем не существует")
        
def copy_file(source_file_name, destination_file_name):
    # Копирует файл из одной папки в другую.
    source_file_path = os.path.join(WORKING_DIRECTORY, source_file_name)
    destination_file_path = os.path.join(WORKING_DIRECTORY, destination_file_name)
    if os.path.isfile(source_file_path):
        shutil.copy(source_file_path, destination_file_path)
        print(f"Файл '{source_file_name}' успешно скопирован в '{destination_file_name}'")
    else:
        print(f"Файл '{source_file_name}' не существует")

def move_file(source_file_name, destination_file_name):
    #Перемещает файл из одной папки в другую.
    source_file_path = os.path.join(WORKING_DIRECTORY, source_file_name)
    destination_file_path = os.path.join(WORKING_DIRECTORY, destination_file_name)
    if os.path.isfile(source_file_path):
        shutil.move(source_file_path, destination_file_path)
        print(f"Файл '{source_file_name}' успешно перемещен в '{destination_file_name}'.")
    else:
        print(f"Файл '{source_file_name}' не существует.")

def rename_file(file_name, new_name): #Переименовывает файл.
    file_path = os.path.join(WORKING_DIRECTORY, file_name)
    new_path = os.path.join(WORKING_DIRECTORY, new_name)
    if os.path.isfile(file_path):
        os.rename(file_path, new_path)
        print(f"Файл '{file_name}' успешно переименован в '{new_name}'.")
    else:
        print(f"Файл '{file_name}' не существует.")

def run_file_manager():
    while True:
        command = input("Введите команду: ")
        command_parts = command.split()

        if command_parts[0] == "create_folder":
            create_folder(command_parts[1])
        elif command_parts[0] == "delete_folder":
            delete_folder(command_parts[1])
        elif command_parts[0] == "change_directory":
            change_directory(command_parts[1])
        elif command_parts[0] == "create_file":
            create_file(command_parts[1])
        elif command_parts[0] == "write_to_file":
            file_name = command_parts[1]
            content = ' '.join(command_parts[2:])
            write_to_file(file_name, content)
        elif command_parts[0] == "view_file":
            view_file(command_parts[1])
        elif command_parts[0] == "delete_file":
            delete_file(command_parts[1])
        elif command_parts[0] == "copy_file":
            copy_file(command_parts[1], command_parts[2])
        elif command_parts[0] == "move_file":
            move_file(command_parts[1], command_parts[2])
        elif command_parts[0] == "rename_file":
            rename_file(command_parts[1], command_parts[2])
        elif command_parts[0] == "exit":
            break
        else:
            print("Неверная команда. Попробуйте еще раз")

if __name__ == "__main__":
    run_file_manager()
