from sympy import diff
import tracemalloc
import time


def function(func_str: str, x: float):
    return eval(func_str, {'x': x})


def bisection(a, b, e, func_str):
    while abs(a - b) > 2 * e:
        x0 = (a + b) / 2
        fx = function(func_str, x0)
        fa = function(func_str, a)
        fb = function(func_str, b)
        if fx * fa < 0:
            b = x0
        elif fx * fb < 0:
            a = x0
        # проверка на 0 на концах отрезка и в текущей точке (например для x**2 - 1 [0, 2]),
        # убрать если обработка таких случаев не нужна
        else:
            if fa == 0:
                return a
            if fb == 0:
                return b
            if fx == 0:
                return x0

        # print('[{}, {}]'.format(a, b))
    return (b + a) / 2


def chord(a, b, e, func_str):
    x1 = 0
    x0 = -10000
    while abs(x1 - x0) > e:
        x0 = x1
        fa = function(func_str, a)
        fb = function(func_str, b)
        if fb != fa:
            x1 = a - fa * (b - a) / (fb - fa)
        else:
            x1 = a
        fx = function(func_str, x1)
        if fx * fa < 0:
            b = x1
        elif fx * fb < 0:
            a = x1
        # проверка на 0 на концах отрезка и в текущей точке (например для x**2 - 1 [0, 2]),
        # убрать если обработка таких случаев не нужна
        else:
            if fa == 0:
                return a
            if fb == 0:
                return b
            if fx == 0:
                return x1

        # print('[{}, {}]'.format(a, b))
    return a if abs(a) < abs(b) else b


def newton(a, b, e, func_str):
    x1 = (a + b) / 2
    x0 = -10000
    while abs(x1 - x0) > e:
        x0 = x1
        fa = function(func_str, a)
        fdx = function(str(diff(func_str)), x0)
        fx0 = function(func_str, x0)
        if fdx != 0:
            x1 = x0 - fx0 / fdx
        else:
            x1 = x0
        fx = function(func_str, x1)
        if fx * fa < 0:
            b = x1
        # проверка на 0 на концах отрезка и в текущей точке (например для x**2 - 1 [0, 2]),
        # убрать если обработка таких случаев не нужна заменить на
        # else a = x1
        elif fa != 0:
            if fx == 0:
                return x1
            a = x1
        else:
            return a

        # print('[{}, {}]'.format(a, b))
    return b if abs(a) < abs(b) else a


def compare_time():
    bi = 0
    ch = 0
    ne = 0

    for i in range(0, REPEATS):
        start_time = time.perf_counter()
        bisection(a, b, e, func_str)
        bi += time.perf_counter() - start_time

        start_time = time.perf_counter()
        chord(a, b, e, func_str)
        ch += time.perf_counter() - start_time

        start_time = time.perf_counter()
        newton(a, b, e, func_str)
        ne += time.perf_counter() - start_time

    print("Метод бисекции: {} cекунд на решение: {}.".format(bi / REPEATS, bisection(a, b, e, func_str)))
    print("Метод хорд: {} cекунд на решение: {}.".format(ch / REPEATS, chord(a, b, e, func_str)))
    print("Метод Ньютона: {} cекунд на решение: {}.".format(ne / REPEATS, newton(a, b, e, func_str)))


def compare_memory():
    bi_memory = 0
    ch_memory = 0
    ne_memory = 0

    for i in range(0, REPEATS):
        tracemalloc.start()
        bisection(a, b, e, func_str)
        _, bi_memory_diff = tracemalloc.get_traced_memory()
        bi_memory += bi_memory_diff
        tracemalloc.stop()

        tracemalloc.start()
        chord(a, b, e, func_str)
        _, ch_memory_diff = tracemalloc.get_traced_memory()
        ch_memory += ch_memory_diff
        tracemalloc.stop()

        tracemalloc.start()
        newton(a, b, e, func_str)
        _, ne_memory_diff = tracemalloc.get_traced_memory()
        ne_memory += ne_memory_diff
        tracemalloc.stop()

    print("Метод бисекции: {} байт на решение: {}.".format(bi_memory / REPEATS, bisection(a, b, e, func_str)))
    print("Метод хорд: {} байт на решение: {}.".format(ch_memory / REPEATS, chord(a, b, e, func_str)))
    print("Метод Ньютона: {} байт на решение: {}.".format(ne_memory / REPEATS, newton(a, b, e, func_str)))


REPEATS = 1000
func_str = input("Введите функцию (используйте x как переменную): ")

a = float(input("Начало отрезка: "))
b = float(input("Конец отрезка: "))
e = float(input("Погрешность: "))

print()
compare_time()
print()
compare_memory()
