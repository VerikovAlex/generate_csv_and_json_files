import csv
import os
import sys
import random
import json
import uuid
from typing import Dict, Tuple

from pydantic import BaseModel

# Описание через аннотацию типов конфиги для генерации
class BuilderConfig(BaseModel):
    number_of_abonents: int = 1000
    mcc: str = '250'
    mnc: str = '07'
    prefix_number: str = '7911'
    full_len_of_number: int = 11
    realm: str = 'ims.protei.ru'
    server_name: str = 'scscf1.ims.protei.ru'
    capability: list = [1, 2, 3, 4]
    probability_capability: float = 0.1
    output_json_folder = './json_files/generated'
    output_csv_folder = './csv_files/generated'

# Функция проверки используемых для генерации параметров
    def validate_params(self):
        if len(self.mcc) != 3:
            print('MCC содержит некорректное число символов. Должно быть 3 цифры')
            sys.exit()
        if 2 > len(self.mnc) > 3 or len(self.mnc) < 2:
            print('MNC содержит некорректное число символов. Должно быть 2 или 3 цифры')
            sys.exit()
        if 15 - len(self.mcc) - len(self.mnc) < self.full_len_of_number - len(self.prefix_number):
            print('Слишком много абонентов для генерации. Длины MSIN не хватает')
            sys.exit()
        if self.full_len_of_number - len(self.prefix_number) >= self.full_len_of_number:
            print('Префикс не может быть равен или быть длиннее самого номера')
            sys.exit()
        if self.probability_capability > 1:
            print('Вероятность выставления Capability не может быть больше 1')
            sys.exit()
        print('Параметры для генератора валидны')


class Builder:

    @staticmethod
    def get_config():
        return BuilderConfig()

# Метод генерирования профиля абонента, получаем для конкретного абонента словарь с описанием его профиля
    @staticmethod
    def __generate_abonent(serial_number, config: BuilderConfig) -> Tuple[str, Dict]:
        r = {'servername':None, 'capability':None}
        phone_number = str(
            config.prefix_number + str(serial_number).zfill(config.full_len_of_number - len(config.prefix_number)))
        r['IMPI'] = str(
            config.mcc + config.mnc + str(serial_number).zfill(15 - len(config.mcc) - len(config.mnc)))
        r['realm'] = config.realm
        r['capability'] = config.capability if random.random() < config.probability_capability else None
        if not r['capability']:
            r['servername'] = config.server_name
        # if random.random() < config.probability_capability:
        #     r['capability'] = config.capability
        #     r['servername'] = None
        # else:
        #     r['capability'] = None
        #     r['servername'] = config.server_name
        return phone_number, r



# Метод, вызывающий генерирование абонентов и заполняющий csv и json файлы с ними
    @staticmethod
    def build(config: BuilderConfig, csv_enabled: bool = True, json_enabled: bool = True):
        config.validate_params()
        filename_csv = None
        filename_json = None
        if csv_enabled:
            filename_csv = str(uuid.uuid4()) + '.csv'
            if not os.path.exists(config.output_csv_folder):
                os.makedirs(config.output_csv_folder)
            with open(os.path.join(config.output_csv_folder, filename_csv), mode='w') as f:
                csv_writer = csv.writer(f, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                for serial in range(1, config.number_of_abonents + 1):
                    phone_number, abonent = Builder.__generate_abonent(serial, config)
                    csv_writer.writerow([abonent['IMPI'], phone_number, abonent['realm']])

        if json_enabled:
            filename_json = str(uuid.uuid4()) + '.json'
            if not os.path.exists(config.output_json_folder):
                os.makedirs(config.output_json_folder)
            with open(os.path.join(config.output_json_folder, filename_json), mode='w+') as f:
                result = {}
                for serial in range(1, config.number_of_abonents + 1):
                    phone_number, abonent = Builder.__generate_abonent(serial, config)
                    result[phone_number] = abonent
                json.dump(result, f)

        if filename_csv and filename_json:
            return filename_csv, filename_json
        if filename_csv:
            return filename_csv
        else:
            return filename_json

    # Метод, вызывающий генерирование абонентов и заполняющий только json
    @staticmethod
    def build_json(config: BuilderConfig):
        return Builder.build(config=config, json_enabled=True, csv_enabled=False)

    # Метод, вызывающий генерирование абонентов и заполняющий только csv
    @staticmethod
    def build_csv(config: BuilderConfig):
        return Builder.build(config=config, json_enabled=False, csv_enabled=True)


if __name__ == "__main__":
    config = BuilderConfig()
    config.number_of_abonents = 2000
    config.mcc = '480'
    config.mnc = '01'
    config.prefix_number='8981'
    config.realm = 'abracadabra.protei.ru'
    config.server_name = 'scscf1.abracadabra.protei.ru'
    config.capability = [1, 2, 3, 4, 5]
    config.probability_capability = 0.5
    Builder.build(config)
#    Builder.build_csv(config)
#    Builder.build_json(config)

    # config.number_of_abonents = 1_000_000
    # from timeit import timeit
    #
    # time_taken = timeit("Builder.build_csv(config)", globals=globals(), number=1)
    # print(f'{time_taken:0.6f} seconds')
