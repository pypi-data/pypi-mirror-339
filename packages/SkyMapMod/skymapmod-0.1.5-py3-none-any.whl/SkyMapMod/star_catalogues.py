import numpy as np

from .data.load_data import load_star_temperatures, load_star_brightness

def print_temperature():
    """
    Пример функции, использующей массив температур звезд.
    """
    # Загружаем данные
    star_temperatures = load_star_temperatures()
    star_brightness = load_star_brightness()
    
    # Пример обработки данных
    print("Массив успешно загружен. Размер:", star_temperatures.shape)
    print(star_temperatures[811][3128])
    print(star_brightness[811][3128])