from src.func import (load_inform,
                      get_executed,
                      get_split_date,
                      get_last_operations,
                      get_changed_time,
                      parse_bank_creds,
                      parse_adr)


def test_load_inform():
    ''' тест возвращения списка'''
    assert type(load_inform()) == list


def test_get_executed():
    ''' тест возвращения списка'''
    assert type(get_executed()) == list


def test_get_last_operations():
    ''' тест возвращения списка'''
    assert type(get_last_operations()) == list


def test_get_split_date():
    '''тестируем формат даты, подаем формат даты (как в файле json)'''
    test_data_split = "2019-08-30T01:09:46.296404"
    result = get_split_date(test_data_split)
    assert result.year == 2019
    assert result.month == 8
    assert result.day == 30


def test_get_changed_timee():
    '''тестируем формат даты, подаем формат даты строкой'''
    test_data_str = "2019-08-30"
    assert get_changed_time(test_data_str) == "30.08.2019"


def test_parse_bank_creds():
    '''тестируем шифрование банковских данных'''
    result_visa = parse_bank_creds("Visa 1234567898765432")
    result_count = parse_bank_creds("Счет 12345678901234567890")
    assert result_count == "Счет **7890"
    assert result_visa == "Visa 1234 67** **** 5432"



def test_parse_adr():
    '''тестируем перевод словаря в нужный ам формат'''
    test_bank_one = {"from": "Maestro 1234567898765432", "to": "Счет 12345678901234567890"}
    result = parse_adr(test_bank_one)
    test_bank_two = {"from": "Счет 12345678901234567890", "to": "Счет 12345678901234567890"}
    result_two = parse_adr(test_bank_two)
    test_bank_three = {"to": "Счет 12345678901234567890"}
    result_three = parse_adr(test_bank_three)
    assert result == "Maestro 1234 67** **** 5432 -> Счет **7890"
    assert result_two == "Счет **7890 -> Счет **7890"
    assert result_three == "Счет **7890"



