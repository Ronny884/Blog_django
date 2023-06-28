from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os


class Encryption:

    def encrypt_file(self, db_name_without_extension, password):
        """
        Функция шифрует новую БД: создаёт соль и сохраняет её в отдельный файл, что также шифруется под ключ из
        указанного мастер-пароля (сохраняется в переменную) и соль, что прописана в коде. Вызывается функция, если
        пользователь после создания БД в окне 5 вернётся в главное меню, если из окна 9 (10) при работе сданной БД
        решит вернуться в окно 3 или окно 1, а также, если закроет программу, нажав на крестик
        :param db_name_without_extension: название файла без расширения
        :param password: мастер-пароль, введённый в 5 окне
        """
        try:
            # формируем ключ для файла с солью
            salt_for_salt = b'\xfbJ\x05\x14d\x0b\xb3\xd5o\x9b<\xbb\x84l\xb0\xb1\x8b\xe9\x10\x0c\xa8\xde\x1c3\x91\xac\xcaK\xe9\xc9\xafa'
            key_for_salt = PBKDF2(password, salt_for_salt, dkLen=32)

            salt = get_random_bytes(32)  # формируем соль для файла новой БД
            key = PBKDF2(password, salt, dkLen=32)  # формируем ключ для файла новой БД

            if not os.path.exists(f'{os.getcwd()}/Alpha'):
                os.mkdir(f'{os.getcwd()}/Alpha')

            # сохраняем соль в файл
            with open(f'{os.getcwd()}/Alpha/{db_name_without_extension}.bin', 'wb') as file:
                file.write(salt)

            # зашифровываем этот файл под фиксированную соль salt_for_salt и пароль
            iv = get_random_bytes(16)
            cipher = AES.new(key_for_salt, AES.MODE_CBC, iv)
            with open(f'{os.getcwd()}/Alpha/{db_name_without_extension}.bin', 'rb') as file:
                plaintext = file.read()
                ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))
            with open(f'{os.getcwd()}/Alpha/{db_name_without_extension}.bin', 'wb') as file:
                file.write(iv + ciphertext)

            # зашифровываем непосредственно сам файл с БД, что к тому моменту уже сохранена
            iv = get_random_bytes(16)
            cipher = AES.new(key, AES.MODE_CBC, iv)
            with open(f'{os.getcwd()}/Database/{db_name_without_extension}.db', 'rb') as file:
                plaintext = file.read()
                ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))
            with open(f'{os.getcwd()}/Database/{db_name_without_extension}.db', 'wb') as file:
                file.write(iv + ciphertext)
            # print('База зашифрована')
        except:
            # print('Шифрование не удалось')
            pass



    def decrypt_file(self, db_name_without_extension, password):
        """
        Функция для дешифровки сначала файла с солью, затем файла БД в случае верного мастер-пароля. Вызывается после
        ввода мастер-пароля в окне 4 при начале работы с ранее сохранённой базой.
        :param db_name_without_extension: название файла без расширения
        :param password: мастер-пароль, что пользователь вводит в окне 4, который проверяется в блоке try-except при
        дешифровке файла с солью
        """
        try:
            # формируем ключ для файла с солью
            salt_for_salt = b'\xfbJ\x05\x14d\x0b\xb3\xd5o\x9b<\xbb\x84l\xb0\xb1\x8b\xe9\x10\x0c\xa8\xde\x1c3\x91\xac\xcaK\xe9\xc9\xafa'
            key_for_salt = PBKDF2(password, salt_for_salt, dkLen=32)

            # расшифровываем файл с солью, не изменяя его и берём оттуда соль
            with open(f'{os.getcwd()}/Alpha/{db_name_without_extension}.bin', 'rb') as file:
                data = file.read()
                iv = data[:16]
                ciphertext = data[16:]
                cipher = AES.new(key_for_salt, AES.MODE_CBC, iv)
                plaintext_salt = unpad(cipher.decrypt(ciphertext), AES.block_size)

            # формируем ключ для файла БД
            key = PBKDF2(password, plaintext_salt, dkLen=32)

            # расшифровываем вайл с БД
            with open(f'{os.getcwd()}/Database/{db_name_without_extension}.db', 'rb') as file:
                data = file.read()
                iv = data[:16]
                ciphertext = data[16:]
                cipher = AES.new(key, AES.MODE_CBC, iv)
                plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
            with open(f'{os.getcwd()}/Database/{db_name_without_extension}.db', 'wb') as file:
                file.write(plaintext)
            return True
        except:
            return False

#
# a = Encryption()
# a.encrypt_file('Nikita_Sivko', '111111111')
# # for i in range(5):
#     a.encrypt_file_for_new_db('222', '222222222')
#     a.decrypt_file('222', '222222222')



