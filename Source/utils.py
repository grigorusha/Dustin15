import sys,os
from math import radians, cos,sin,tan, pi, sqrt

def mas_pos(mas_xy, pos):
    # получить элемент массива независимо от выхода индекса за границы
    ll = len(mas_xy)
    while pos >= ll:
        pos -= ll
    return mas_xy[pos]

def find_element(pos, mas):
    # поиск элемента массива по номеру (индекс в первой ячейке)
    for elem in mas:
        if typeof(elem)=="list":
            if elem[0] == pos:
                return elem
        elif typeof(elem)=="dict":
            if elem["num"] == pos:
                return elem
    return ""

def find_index(mas, element):
    if len(mas)==0: return None
    if typeof(mas[0]) != "list":
        # одномерный массив
        try:
            pos = mas.index(element)
        except:
            pos = None
        return pos
    else:
        # двумерный массив
        for y,str in enumerate(mas):
            try:
                x = str.index(element)
                return x,y
            except:
                continue
        return None,None

def dicmas_find(mas, index, element):
    # ищем по индексу элемент в массиве из словарей
    return next((item for item in mas if item[index] == element), None)

def compare_xy(x, y, tolerance):
    # сравнение двух величин, с учетом погрешности
    return round(abs(x - y), tolerance) <= 10**(-tolerance)

def typeof(your_var):
    if (isinstance(your_var, int)):
        return 'int'
    elif (isinstance(your_var, float)):
        return 'float'
    elif (isinstance(your_var, list)) or (isinstance(your_var, tuple)):
        return 'list'
    elif (isinstance(your_var, dict)):
        return 'dict'
    elif (isinstance(your_var, bool)):
        return 'bool'
    elif (isinstance(your_var, str)):
        return 'str'
    else:
        return "type is unknown"

def is_number(s):
    if typeof(s)!= "str": return False
    try:
        float(s) # for int, long and float
    except ValueError:
        try:
            complex(s) # for complex
        except ValueError:
            return False
    return True

def calc_length(x1, y1, x2, y2):
    # длина отрезка
    x, y = x2 - x1, y2 - y1
    return sqrt(x*x + y*y)

######################################################################################

def rotate_matrix(matrix, turn):
    # поворот двумерной матрицы NxN. нужно для вращения граней
    # turn 1 - angle 90, turn 2 - angle 180, turn -1/3 - angle -90/270,
    cube_size = len(matrix)
    layers = cube_size//2
    for ll in range(layers):
        size = cube_size-ll*2-1
        for pos in range(size):
            pos1 = matrix[ll][pos+ll]
            pos2 = matrix[pos+ll][cube_size-1-ll]
            pos3 = matrix[cube_size-1-ll][cube_size-1-ll-pos]
            pos4 = matrix[cube_size-1-ll-pos][ll]

            if turn == 1:
                matrix[ll][pos+ll] = pos4
                matrix[pos+ll][cube_size-1-ll] = pos1
                matrix[cube_size-1-ll][cube_size-1-ll-pos] = pos2
                matrix[cube_size-1-ll-pos][ll] = pos3
            elif turn == 2:
                matrix[ll][pos + ll] = pos3
                matrix[pos + ll][cube_size - 1 - ll] = pos4
                matrix[cube_size - 1 - ll][cube_size - 1 - ll - pos] = pos1
                matrix[cube_size - 1 - ll - pos][ll] = pos2
            elif turn == -1 or turn == 3:
                matrix[ll][pos + ll] = pos2
                matrix[pos + ll][cube_size - 1 - ll] = pos3
                matrix[cube_size - 1 - ll][cube_size - 1 - ll - pos] = pos4
                matrix[cube_size - 1 - ll - pos][ll] = pos1

    return matrix

######################################################################################


def check_os_platform():
    import platform
    return platform.system().lower()

def close_spalsh_screen():
    if check_os_platform() != "windows": return

    try:  # pyinstaller spalsh screen
        import pyi_splash
        pyi_splash.close()
    except:
        pass

def get_pyinstaller_temp_path():
    """
    Возвращает путь к временной директории PyInstaller,
    если скрипт запущен из one-file исполняемого файла.
    """
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        # Мы запущены из PyInstaller one-file bundle
        # sys._MEIPASS содержит путь к временной папке
        return sys._MEIPASS
    elif getattr(sys, 'frozen', False):
        # Если это frozen, но _MEIPASS не найден (например, --onedir или старый PyInstaller)
        # sys.executable указывает на интерпретатор внутри папки
        return os.path.dirname(sys.executable)
    else:
        # Мы запущены в обычной среде Python
        return os.path.dirname(os.path.abspath(__file__))

