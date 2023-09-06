import zipfile
import re
import os
import uuid
import shutil
from datetime import datetime

def remove_duplicates(passwords):
    unique_passwords = []
    duplicates = []
    seen = set()
    for password in passwords:
        if password not in seen:
            unique_passwords.append(password)
            seen.add(password)
        else:
            duplicates.append(password)
    return unique_passwords, duplicates

def extract_passwords_from_zip(zip_file_path, url):
    passwords = []

    with zipfile.ZipFile(zip_file_path, 'r') as zip_file:
        for file_name in zip_file.namelist():
            if file_name.lower().endswith('.txt') and 'passwords.txt' in file_name.lower():
                with zip_file.open(file_name) as txt_file:
                    contents = txt_file.read().decode('latin-1')
                    matches = re.findall(r'URL:\s*(.*?)\nUsername:\s*(.*?)\nPassword:\s*(.*?)\n', contents)
                    for match in matches:
                        if url.strip().lower() in match[0].strip().lower():
                            passwords.append(match)

    passwords, duplicates = remove_duplicates(passwords)

    if passwords:
        save_path = '/storage/emulated/0/BOTS AQUI/REDLINES AQUI'
        os.makedirs(save_path, exist_ok=True)
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
        file_prefix = f'{timestamp}'
        file_extension = '.txt'
        file_path = os.path.join(save_path, f'{file_prefix}.txt')

        with open(file_path, 'w') as txt_file:
            txt_file.write('LOGINS ACHADOS:\n\n')
            for i, password in enumerate(passwords):#codigin by @gabriel.mooraiss
                txt_file.write(f'LOGIN [{i+1:03}]\n')
                txt_file.write(f'url: {password[0]}\nlogin: {password[1]}\npassword: {password[2]}\n')
                txt_file.write('\n\n')

            if duplicates:
                txt_file.write('LOGINS DUPLICADOS AQUI:\n\n')
                for i, duplicate in enumerate(duplicates):
                    txt_file.write(f'LOGIN [{i+1:03}] [DUP] url: {duplicate[0]}\n')
                    txt_file.write(f'login: {duplicate[1]}\npassword: {duplicate[2]}\n')
                    txt_file.write('\n\n')

    return passwords, duplicates

def search_url():
    while True:
        url = input("Qual a URL que você deseja buscar? (Digite 'sair' para encerrar) ")
        if url.lower() == 'sair':
            break

        zip_files = []
        directory = '/data/data/com.termux/files/home/storage/downloads'
        for file in os.listdir(directory):
            if file.lower().endswith('.zip'):
                zip_files.append(file)

        if len(zip_files) == 0:
            print("Nenhum arquivo .zip encontrado no diretório especificado.")
        else:
            print("Arquivos .zip disponíveis:")
            for i, file in enumerate(zip_files):
                print(f"{i+1}. {file}")
            selection = input("Selecione o número do arquivo .zip que você deseja usar: ")
            selection = int(selection) - 1

            if selection < 0 or selection >= len(zip_files):
                print("Seleção inválida.")
            else:
                zip_file_path = os.path.join(directory, zip_files[selection])

                senhas, duplicatas = extract_passwords_from_zip(zip_file_path, url)

                if len(senhas) == 0:
                    print("Nenhuma senha encontrada para a URL especificada.")
                else:
                    print("LOGINS ACHADOS:", len(senhas))
                    print("FORAM SALVOS NO TXT!!")
                    if duplicatas:
                        print("LOGINS DUPLICADOS (QUANTIDADE):", len(duplicatas))
                    print("")

def rename_zip():
    zip_files = []
    directory = '/data/data/com.termux/files/home/storage/downloads'
    for file in os.listdir(directory):
        if file.lower().endswith('.zip'):
            zip_files.append(file)

    if len(zip_files) == 0:
        print("Nenhum arquivo .zip encontrado no diretório especificado.")
    else:
        print("Arquivos .zip disponíveis:")
        for i, file in enumerate(zip_files):
            print(f"{i+1}. {file}")

        selection = input("Selecione o número do arquivo .zip que você deseja renomear: ")
        selection = int(selection) - 1

        if selection < 0 or selection >= len(zip_files):
            print("Seleção inválida.")
        else:
            zip_file_path = os.path.join(directory, zip_files[selection])

            password = input("Digite a senha do arquivo .zip (se não houver senha, deixe em branco): ")

            with zipfile.ZipFile(zip_file_path, 'r') as zip_file:
                if password:
                    try:
                        zip_file.setpassword(password.encode('latin-1'))
                    except Exception as e:
                        print("Senha incorreta.")
                        return

                txt_files = [file_info for file_info in zip_file.infolist() if os.path.basename(file_info.filename).lower() == 'passwords.txt']

                if len(txt_files) == 0:
                    print("Nenhum arquivo passwords.txt encontrado.")
                else:
                    save_path = '/storage/emulated/0/BOTS AQUI/REDLINES AQUI'
                    os.makedirs(save_path, exist_ok=True)
                    now = datetime.now()
                    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
                    file_prefix = f'{timestamp}'
                    file_extension = '.zip'
                    file_path = os.path.join(save_path, f'{file_prefix}.zip')

                    with zipfile.ZipFile(file_path, 'w') as new_zip:
                        total_files = len(txt_files)
                        progress = 0

                        folder_count = 1
                        files_per_folder = 20

                        temp_folder = '/storage/emulated/0/BOTS AQUI/TEMP'
                        os.makedirs(temp_folder, exist_ok=True)

                        for txt_file in txt_files:
                            file_name = os.path.basename(txt_file.filename)
                            file_data = zip_file.read(txt_file)
                            folder_name = f' [{folder_count:03d}]'
                            folder_path = os.path.join(temp_folder, folder_name)
                            os.makedirs(folder_path, exist_ok=True)

                            unique_suffix = str(uuid.uuid4())[:8]
                            new_file_name = f'{file_name[:-4]}_{timestamp}_{unique_suffix}.txt'
                            new_file_path = os.path.join(folder_path, new_file_name)

                            if b"""***********************************************
*   ____  _____ ____  _     ___ _   _ _____   *
*  |  _ | ____|  _ | |   |_ _|  | | ____|     *
*  | |_) |  _| | | | | |    | ||  | |  _|     *
*  |  _ <| |___| |_| | |___ | || |  | |___    *
*  |_| _|_____|____/|_____|___|_| _|_____|    *
*                                             *
*  Telegram :      *
***********************************************""" in file_data:
                                new_file_data = file_data.replace(
                                    b"""***********************************************
*   ____  _____ ____  _     ___ _   _ _____   *
*  |  _ | ____|  _ | |   |_ _|  | | ____|     *
*  | |_) |  _| | | | | |    | ||  | |  _|     *
*  |  _ <| |___| |_| | |___ | || |  | |___    *
*  |_| _|_____|____/|_____|___|_| _|_____|    *
*                                             *
*      *
***********************************************""",
                                    b""""""
                                )
                            else:
                                new_file_data = file_data.replace(
                                    b"""***********************************************
*   ____  _____ ____  _     ___ _   _ _____   *
*  |  _ | ____|  _ | |   |_ _|  | | ____|     *
*  | |_) |  _| | | | | |    | ||  | |  _|     *
*  |  _ <| |___| |_| | |___ | || |  | |___    *
*  |_| _|_____|____/|_____|___|_| _|_____|    *
*                                             *
*   *
""",
                                    b""" """
                                )

                            with open(new_file_path, 'wb') as new_file:
                                new_file.write(new_file_data)

                            new_zip.write(new_file_path, arcname=os.path.join(folder_name, new_file_name))

                            progress += 1

                            if progress % files_per_folder == 0 or progress == total_files:
                                folder_count += 1
                                if folder_count > 100:
                                    break

                            progress_percent = (progress / total_files) * 100
                            print(f"Progresso: {progress_percent:.2f}% completo", end='\r')

                    print("\nArquivo .zip renomeado com sucesso.")

                    shutil.rmtree(temp_folder)


while True:
    print("MENU:")
    print("1 - Pesquisar URL")
    print("2 - Renomear .zip")
    print("Digite 'sair' para encerrar")

    option = input("Selecione uma opção: ")
    if option == '1':
        search_url()
    elif option == '2':
        rename_zip()
    elif option.lower() == 'sair':
        break
    else:
        print("Opção inválida. Tente novamente.")

print("Encerrando")
