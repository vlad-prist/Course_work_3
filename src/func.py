import requests
from datetime import date


def load_inform():
    '''
    Распаковка файла json через requests
    :return: type list. Все данные из файла
    '''
    datas = requests.get("https://www.jsonkeeper.com/b/81IJ").json()
    return datas


def get_executed():
    '''
    Фильтрация операций по EXECUTED
    :return: type list. Все данные из файла по фильтру EXECUTED
    '''
    datas = load_inform()
    executed = [data for data in datas if data.get('state') == 'EXECUTED']
    return executed


def get_split_date(date_str):
    '''
    Разбиваем дату по букве Т, и возвращаем первую часть строки (дату без времени)
    :param date_str: Дата строкой
    :return:
    '''
    split_date = date_str.split("T")[0]
    conv_date = date.fromisoformat(split_date)
    return conv_date


def get_last_operations():
    '''
    Функция сортировки по последним операциям (отбираем по дате)
    :return: type list. Последние 5 операций
    '''
    last_datas = sorted(get_executed(), key=lambda x: get_split_date(x['date']), reverse=True)
    return last_datas[:5]


def get_changed_time(date_str):
    '''
    Изменение формата даты
    :param date_str: Принимает полный список last_datas, по ключу Дата
    :return: дата формата 01.01.2024
    '''
    split_date = date_str.split("T")[0]
    conv_date = date.fromisoformat(split_date)
    return conv_date.strftime("%d.%m.%Y")


def parse_bank_creds(bank_info):
    '''
    Функция которая шифрует банковскую информацию по шаблону: Счет **1234 или Visa 1234 56** **** 4321
    Информацию по ключам from и to разделяем на цифры и текстовую часть, для шифрования
    :param bank_info: Принимает полный список last_datas
    :return: возвращает маску для шифрования
    '''
    bank_digits = bank_info.split()[-1]
    bank_name = bank_info.split()[:-1]
    if "Счет" in bank_name:
        bank_digits = "**" + bank_digits[-4:]
    else:
        bank_digits = bank_digits[:4] + " " + bank_digits[5:7] + "**" + " " + "*" * 4 + " " + bank_digits[-4:]
    mask_ = ' '.join(bank_name) + ' ' + bank_digits
    return mask_


def parse_adr(bank_info: dict):
    '''
    На основании функции parse_bank_creds выводим результат банковских операций, подставив маску

    :param bank_info: принимает полную банковскую операцию в виде словаря (из last_datas по ключам from и to)
    :return: вовзаращает строку для отображения операций
    '''
    from_inform = bank_info.get('from', 'Нет данных')
    to_inform = bank_info.get('to')
    to_inform = parse_bank_creds(to_inform)
    if from_inform != 'Нет данных':
        from_inform = parse_bank_creds(from_inform)
        result_str = f"{from_inform} -> {to_inform}"
    else:
        result_str = f"{to_inform}"

    return result_str



