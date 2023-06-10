from hashlib import sha1
from settings import SETTING


def check_hash(number: int) -> int:
    """Функция, которая проверяет совпадение хэша
    Args:
        number (int): номер карты
    Returns:
        int: номер карты
    """
    return number \
        if sha1(
        f'{SETTING["begin_digits"]}{number}{SETTING["last_digits"]}'.encode()).hexdigest() == f'{SETTING["hash"]}' \
        else False


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
    bin = [int(i) for i in SETTING['begin_digits']]
    code = [int(i) for i in number]
    end = [int(i) for i in SETTING['last_digits']]
    all_number = bin + code + end
    all_number = all_number[::-1]
    for i in range(0, len(all_number), 2):
        all_number[i] *= 2
        if all_number[i] > 9:
            all_number[i] -= 9
    if sum(all_number) % 10 == 0:
        return True
    else:
        return False
