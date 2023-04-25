import csv
import os
import sys
import random
import json


class GeneratorOfAbonents:

    def __init__(self):
        self._generated_csv = './csv_files/generated/'
        self._generated_json = './json_files/generated/'
        if not os.path.exists(self._generated_csv): os.makedirs(self._generated_csv)
        if not os.path.exists(self._generated_json): os.makedirs(self._generated_json)

    def __calculate_len_msin(self, mcc, mnc): # Вычисляем длину MSIN
        self.len_msin = 15 - len(mcc) - len(mnc)

    def __calculate_len_generic_number(self, full_len_of_number, prefix_number): # Вычисляем длину генерируемой части номера
        self.len_generic_number = full_len_of_number - len(prefix_number)

    def __check_validate_args(self, mcc, mnc, prefix_number, full_len_of_number, number_of_abonents, probability_server_name, probability_capability):
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
        if probability_server_name + probability_capability != 1:
            print('Сумма вероятностей выставления Server Name и Capability не равна 1')
            sys.exit()
        if probability_server_name > 1:
            print('Веротяность выставления Server Name не может быть больше 1')
            sys.exit()
        if probability_capability > 1:
            print('Веротяность выставления Capability не может быть больше 1')
            sys.exit()
        print('Параметры для генератора валидны')
        return None

    def generate_csv_file(self, mcc: str = '250', mnc: str = '07', prefix_number: str = '7911', full_len_of_number: int = 11,
                          realm: str = 'ims.protei.ru', number_of_abonents:int = 1000, server_name: str = "scscf1.ims.protei.ru",
                           capability: list = [1, 2, 3, 4, 5], probability_server_name: float = 0.9, probability_capability: float = 0.1,
                           output_file_name_csv=None):
        self.__calculate_len_msin(mcc, mnc)
        self.__calculate_len_generic_number(full_len_of_number, prefix_number)
        self.__check_validate_args(mcc, mnc, prefix_number, full_len_of_number, number_of_abonents, probability_server_name, probability_capability)
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

    def __discription_of_specific_abonent(self, serial_number, mcc, mnc, realm, server_name, capability, probability_server_name, probability_capability):
        self.dict_of_abon = dict()
        generate_MSIN = str(serial_number).zfill(self.len_msin)
        IMPI = int(mcc + mnc + generate_MSIN)
        self.dict_of_abon["IMPI"] = IMPI
        self.dict_of_abon["realm"] = realm
        random_number_to_make_decision = random.randint(0, 100)/100
        if random_number_to_make_decision <= probability_server_name:
            self.dict_of_abon["servername"] = server_name
        else:
            self.dict_of_abon["capability"] = capability

    def generate_json_file(self, mcc: str = '250', mnc: str = '07', prefix_number: str = '7911', full_len_of_number: int = 11,
                          realm: str = 'ims.protei.ru', number_of_abonents:int = 1000, server_name: str = "scscf1.ims.protei.ru",
                           capability: list = [1, 2, 3, 4, 5], probability_server_name: float = 0.9, probability_capability: float = 0.1,
                           output_file_name_json=None):
        self.__calculate_len_msin(mcc, mnc)
        self.__calculate_len_generic_number(full_len_of_number, prefix_number)
        self.__check_validate_args(mcc, mnc, prefix_number, full_len_of_number, number_of_abonents, probability_server_name, probability_capability)
        if output_file_name_json is None:
            output_file_name_json = str(random.randrange(0, 1000000000000, 1)) + '.json'
        output_file_json = self._generated_json + output_file_name_json
        dictionary_abonents = dict()
        for serial_number in range(1, number_of_abonents + 1):
            self.__discription_of_specific_abonent(serial_number, mcc, mnc, realm, server_name, capability, probability_server_name, probability_capability)
            dictionary_abonents[serial_number] = self.dict_of_abon
        with open(output_file_json, mode='w') as json_file:
            json.dump(dictionary_abonents, json_file)
        return output_file_json

    def generate_csv_and_json_file(self, mcc: str = '250', mnc: str = '07', prefix_number: str = '7911', full_len_of_number: int = 11,
                          realm: str = 'ims.protei.ru', number_of_abonents:int = 1000, server_name: str = "scscf1.ims.protei.ru",
                           capability: list = [1, 2, 3, 4, 5], probability_server_name: float = 0.9, probability_capability: float = 0.1,
                           output_file_name_csv=None,  output_file_name_json=None):
        self.__calculate_len_msin(mcc, mnc)
        self.__calculate_len_generic_number(full_len_of_number, prefix_number)
        self.__check_validate_args(mcc, mnc, prefix_number, full_len_of_number, number_of_abonents, probability_server_name, probability_capability)
        if output_file_name_csv is None:
            output_file_name_csv = str(random.randrange(0, 1000000000000, 1)) + '.csv' # Генерируем имя сsv файла
        output_file_csv = self._generated_csv + output_file_name_csv
        if output_file_name_json is None:
            output_file_name_json = str(random.randrange(0, 1000000000000, 1)) + '.json' # Генерируем имя json файла
        output_file_json = self._generated_json + output_file_name_json
        dictionary_abonents = dict() # Будущий словарь для сгенерированных абоненетов, который запишем в json
        with open(output_file_csv, mode='w') as csv_file:
            abonents_csv_writer = csv.writer(csv_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for serial_number in range(1, number_of_abonents + 1):
                #собираем IMPI абонента
                generate_MSIN = str(serial_number).zfill(self.len_msin)
                IMPI = str(mcc + mnc + generate_MSIN)
                #собираем номер абонента
                generate_number = str(serial_number).zfill(self.len_generic_number)
                userpart = str(prefix_number + generate_number)
                #записываем все в одну строку csv
                abonents_csv_writer.writerow([IMPI, userpart, realm])
                # генерим параметры для абонента и вносим в словарь
                self.__discription_of_specific_abonent(serial_number, mcc, mnc, realm, server_name, capability,
                                                       probability_server_name, probability_capability)
                dictionary_abonents[userpart] = self.dict_of_abon # Записываем в словарь параметры абонента
        with open(output_file_json, mode='w') as json_file:
            json.dump(dictionary_abonents, json_file)
        return output_file_csv, output_file_json


if __name__ == "__main__":
    list_abonents = GeneratorOfAbonents()
    list_abonents.generate_csv_file()
    list_abonents.generate_json_file()
#    list_abonents.generate_csv_and_json_file()




# Почему я не могу сразу сделать list_abonents =generator_of_abonets.generate_csv_file() - У Кати вроде так и работает
# Не понимаю почему атрибуты класса не видны аргументам методов
# Генерить сразу 2 файла или по одному?
# Не понятно почему при вызове функции надо писать self, а в аргументах самой функции нет