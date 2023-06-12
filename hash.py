from hashlib import sha1
from my_settings import my_function

setting = my_function("settings.json")

def check_hash(number:int) -> int:
    """Функция, которая проверяет совпадение хэша
    Args:
        number (int): номер карты
    Returns:
        :param setting: параметры карты
    """
    return number if sha1(f'{setting["begin_digits"]}{number}'
                          f'{setting["last_digits"]}'.encode()).hexdigest() == f'{setting["hash"]}' else False


def algorithm_luna(number: int):
    """Функция, которая проверяет номер карты используя алгоритм Луна
    Args:
        number (int):  серединные числа номера карты
    Returns:
        bool: True - если номер карты прошел проверку, иначе False
    """
    number = str(number)
    if len(number) != 6:
        return False
    bin = [int(i) for i in setting['begin_digits']]
    code = [int(i) for i in number]
    end = [int(i) for i in setting['last_digits']]
    all_number = bin + code + end
    all_number = all_number[::-1]
    for i in range(0, len(all_number), 2):
        all_number[i] *= 2
        if all_number[i] > 9:
            all_number[i] -= 9

    return True if sum(all_number) % 10 == 0 else False
