from func import (get_last_operations,
    get_changed_time,
    parse_adr)

def main():
    '''
    В главную функцию импортировали get_last_operations, которая предоставляет последние 5 операций last_datas (type list)
    Также импорт get_changed_time и parse_adr. Данные функции нужны для корректного отображения последних 5 операций
    :return: результат форматом:
    01.01.2019 Перевод организации
Visa Classic 1234 56** **** 4321 -> Счет **4321
12345.67 USD
    '''
    last_datas = get_last_operations()
    for data_ in last_datas:
        data_ = (f"{get_changed_time(data_['date'])} {data_['description']}\n"
                 f"{parse_adr(data_)}\n"
                 f"{data_['operationAmount']['amount']} {data_['operationAmount']['currency']['name']}\n"
                 )
        print(data_)

if __name__ == '__main__':
    main()