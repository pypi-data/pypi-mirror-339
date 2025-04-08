import numpy as np

from .data.load_data import load_star_temperatures, load_star_brightness

#спектр АЧТ в фотонах
def black_body_phot(lmbd, T):
    h = 6.63e-34 #Дж * сек
    c = 3e8 # м / сек
    k = 1.38e-23 # Дж / К
    lmbd = lmbd * 1e-9 # м
    u = 2 * c / (lmbd**4) / (np.exp(h * c / (lmbd) / k / T) - 1)
    return u #уже в фотонах/сек (поделено на hc/lambda)

#на вход подаем галактические координаты (l -- долгота, b -- широта) и массив длин волн, по которым строим спектр
def star_spectrum(l, b, lmbd):
    j = int((1800 - round(l*10)) + 3600) #пересчет из галактических к позиции в массиве
    i = int(900 + round(b*10))
    star_brightness = load_star_brightness()
    star_temperatures = load_star_temperatures()    
    A = star_brightness[b][l]
    T = star_temperatures[b][l]
    spectrum = A * black_body_phot(lmbd, T)
    return spectrum