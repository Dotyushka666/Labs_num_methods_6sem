import numpy as np
import pandas as pd

def f(x):
    return np.sqrt(x) - 2 * np.cos(x)

def y(x:float, c:float):
    return c * np.exp(-x) + x**2 * np.sin(x)

def golden_selection_method(p:float = 3, q:float = 8, eps:float = .001):

    calculations = pd.DataFrame(data={'n': [], 'p': [], 'q': [], 'x1': [], 'x2': [], 'f(x1)': [],
                                            'f(x2)': [], 'p-q': []})
    K = [(3 - np.sqrt(5)) * 0.5, (np.sqrt(5) - 1) * 0.5]
    x = [p + K[0] * (q - p), p + K[1] * (q - p)]


    with open('points.txt', 'w') as file:
        pass
    iter = 0
    y = [f(_) for _ in x]
    while abs(q - p)/2 >= eps:
        if y[0] < y[1]:
            q = x[1]
            x[1] = x[0]
            x[0] =  p + K[0] * (q - p)
            y[1], y[0] = y[0], f(x[0])
        else:
            p = x[0]
            x[0] = x[1]
            x[1] = p + K[1] * (q - p)
            y[0], y[1] = y[1], f(x[1])
        iter += 1
        with open('points.txt', 'a') as file:
            file.write(str(q) + " " + str(p) + "\n")
        temp_calc = pd.DataFrame(data={'n': [iter], 'p': [p], 'q': [q], 'x1': [x[0]], 'x2': [x[1]], 'f(x1)': [f(x[0])],
                                            'f(x2)': [f(x[1])], 'p-q': [abs(p-q)]})
        calculations = pd.concat([calculations, temp_calc], ignore_index=True)
    
    calculations = np.round(calculations, 4)
    calculations.to_excel(f"golden_selection_method.xlsx")
    final_x = (p + q) / 2 #Абцисса точки минимума
    return final_x

def simpson_method(a:float, b:float, x_min:float, eps:float = .001):
    n = 2 #Количество разбиений отрезка интегрирования
    h = (b - a)/n
    s = (y(a, x_min) + 4 * y((a+b) / 2, x_min) + y(b, x_min)) * h/3    #Значение интеграла

    calc_simpson = pd.DataFrame({'n': [n], 'h': [h], 's': [s]})

    while True:
        n = 2 * n  #Увеличение разбиение отрезка интегрирования
        h = (b - a) / n #Шаг
        s1 = 0
        for i in range(1, n):
            s1 += (2 + i%2 * 2) * y(a + h * i, x_min) #Центральные точки
        s1 = s1 + y(a, x_min) + y(b, x_min) #Крайние точки
        s1 *= h/3

        calc_temp = pd.DataFrame({'n': [n], 'h': [h], 's': [s1]})
        calc_simpson = pd.concat([calc_simpson, calc_temp], ignore_index=True)

        if abs(s - s1) < eps:
            calc_simpson = np.round(calc_simpson, 4)
            calc_simpson.to_excel(f'simpson_method.xlsx')
            return s1
        s = s1

x_min = golden_selection_method()
print(f'С= {round(x_min, 4)}')
print('integral y(x)=', round(simpson_method(1, 3, x_min), 4))