import csv
import os
import sys
import random
import json


class GeneratorOfAbonents:

    def __init__(self, mcc='250', mnc='07', prefix_number='7911', full_len_of_number=11, realm='ims.protei.ru',
                 number_of_abonents=1000):
        self._generated_csv = './csv_files/generated/'
        self._generated_json = './json_files/generated/'
        if not os.path.exists(self._generated_csv): os.makedirs(self._generated_csv)
        if not os.path.exists(self._generated_json): os.makedirs(self._generated_json)
        self.prefix_number: str = prefix_number
        self.full_len_of_number: int = full_len_of_number
        self.realm: str = realm
        self.number_of_abonents: int = number_of_abonents

    def __calculate_len_msin(self, mcc, mnc):
        self.len_msin = 15 - len(mcc) - len(mnc)

    def __calculate_len_generic_number(self, full_len_of_number):
        self.len_generic_number = full_len_of_number - len(self.prefix_number)

    def __check_validate_args(self, mcc, mnc, prefix_number, full_len_of_number, number_of_abonents):  # Почему нельзя сделать self для всех аргументов?
        if len(mcc) != 3:
            print('MCC содержит некорректное число символов. Должно быть 3 цифры')
            sys.exit()
        if 2 > len(mnc) > 3 or len(mnc) < 2:
            print('MNC содержит некорректное число символов. Должно быть 2 или 3 цифры')
            sys.exit()
        if self.len_msin < self.len_generic_number:
            print('Слишком много абонентов для генерации. Длины MSIN не хватает')
            sys.exit()
        if len(prefix_number) >= full_len_of_number:
            print('Префикс не может быть равен или быть длиннее самого номера')
            sys.exit()
        if self.len_generic_number < len(str(number_of_abonents)):
            print('Слишком много абонентов для генерации. Длины генерируемого номера не хватает для заданного числа абонентов')
            sys.exit()
        print('Параметры для генератора валидны')
        return None

    def generate_csv_file(self, mcc: str = '250', mnc: str = '07', prefix_number: str = '7911', full_len_of_number: int = 11,
                          realm: str = 'ims.protei.ru', number_of_abonents:int = 1000,  output_file_name_csv=None):
        self.__calculate_len_msin(mcc, mnc)
        self.__calculate_len_generic_number(full_len_of_number)
        self.__check_validate_args(mcc, mnc, prefix_number, full_len_of_number, number_of_abonents)
        if output_file_name_csv is None:
            output_file_name_csv = str(random.randrange(0, 1000000000000, 1)) + '.csv'
        output_file_csv = self._generated_csv + output_file_name_csv
        with open(output_file_csv, mode='w') as csv_file:
            abonents_csv_writer = csv.writer(csv_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for serial_number in range(1, number_of_abonents + 1):
                #собираем IMPI
                generate_MSIN = str(serial_number).zfill(self.len_msin)
                IMPI = str(mcc + mnc + generate_MSIN)
                #собираем номер абонента
                generate_number = str(serial_number).zfill(self.len_generic_number)
                userpart = str(prefix_number + generate_number)
                #записываем все в одну строку csv
                abonents_csv_writer.writerow([IMPI, userpart, realm])
        return output_file_csv

    def __discription_of_specific_abonent(self, serial_number, mcc, mnc, realm):
        self.dict_of_abon = dict()
        generate_MSIN = str(serial_number).zfill(self.len_msin)
        IMPI = int(mcc + mnc + generate_MSIN)
        self.dict_of_abon["IMPI"] = IMPI
        self.dict_of_abon["realm"] = realm

    def generate_json_file(self, mcc: str = '250', mnc: str = '07', prefix_number: str = '7911', full_len_of_number: int = 11,
                          realm: str = 'ims.protei.ru', number_of_abonents:int = 1000,  output_file_name_json=None):
        self.__calculate_len_msin(mcc, mnc)
        self.__calculate_len_generic_number(full_len_of_number)
        self.__check_validate_args(mcc, mnc, prefix_number, full_len_of_number, number_of_abonents)
        if output_file_name_json is None:
            output_file_name_json = str(random.randrange(0, 1000000000000, 1)) + '.json'
        output_file_json = self._generated_json + output_file_name_json
        dictionary_abonents = dict()
        for serial_number in range(1, number_of_abonents + 1):
            self.__discription_of_specific_abonent(serial_number, mcc, mnc, realm)
            dictionary_abonents[serial_number] = self.dict_of_abon
        with open(output_file_json, mode='w') as json_file:
            json.dump(dictionary_abonents, json_file)
        return output_file_json

    def generate_csv_and_json_file(self, mcc: str = '250', mnc: str = '07', prefix_number: str = '7911', full_len_of_number: int = 11,
                          realm: str = 'ims.protei.ru', number_of_abonents:int = 1000,  output_file_name_csv=None,  output_file_name_json=None):
        self.__calculate_len_msin(mcc, mnc)
        self.__calculate_len_generic_number(full_len_of_number)
        self.__check_validate_args(mcc, mnc, prefix_number, full_len_of_number, number_of_abonents)
        if output_file_name_csv is None:
            output_file_name_csv = str(random.randrange(0, 1000000000000, 1)) + '.csv'
        output_file_csv = self._generated_csv + output_file_name_csv
        if output_file_name_json is None:
            output_file_name_json = str(random.randrange(0, 1000000000000, 1)) + '.json'
        output_file_json = self._generated_json + output_file_name_json
        dictionary_abonents = dict()
        with open(output_file_csv, mode='w') as csv_file:
            abonents_csv_writer = csv.writer(csv_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for serial_number in range(1, number_of_abonents + 1):
                # описываем параметры для абонента и вносим в словарь
                self.__discription_of_specific_abonent(serial_number, mcc, mnc, realm)
                dictionary_abonents[serial_number] = self.dict_of_abon
                #собираем IMPI
                generate_MSIN = str(serial_number).zfill(self.len_msin)
                IMPI = str(mcc + mnc + generate_MSIN)
                #собираем номер абонента
                generate_number = str(serial_number).zfill(self.len_generic_number)
                userpart = str(prefix_number + generate_number)
                #записываем все в одну строку csv
                abonents_csv_writer.writerow([IMPI, userpart, realm])
        with open(output_file_json, mode='w') as json_file:
            json.dump(dictionary_abonents, json_file)
        return output_file_csv, output_file_json


if __name__ == "__main__":
    list_abonents = GeneratorOfAbonents()
#    list_abonents.generate_csv_file()
#    list_abonents.generate_json_file()
    list_abonents.generate_csv_and_json_file()




# Почему я не могу сразу сделать list_abonents =generator_of_abonets.generate_csv_file() - У Кати вроде так и работает
# Не понимаю почему атрибуты класса не видны аргументам методов
# Генерить сразу 2 файла или по одному?
# Не понятно почему при вызове функции надо писать self, а в аргументах самой функции нет