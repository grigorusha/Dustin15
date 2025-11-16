# Dustin Tight
# https://www.cs.brandeis.edu/~storer/JimPuzzles/ZPAGES/zzzDustinPuzzle.html
# https://patents.google.com/patent/US1993211A/en?oq=US+1993211

# from numba import jit
import random, webbrowser

import pygame, pygame_gui
from pygame_gui import UIManager

from puzzles import *
from utils import *

# TODO 0. + Вывод головоломки решенной
# TODO 0. + Перемещение фишки
# TODO 0. + Ресет и Скрамбл
# TODO 0. + Строка состояния: сколько ходов
# TODO 0. + Кнопки поворот рамки влево-вправо
# TODO 0. + Проверка решенного состояния
# TODO 0. + Выбор разных целевых позиций

# TODO 2. Анимация перемещения и Вращения доски
# TODO 2. Поиск решения - ускорение Нумба

VERSION = "1.0"

# Константы
DISK_RADIUS,LINK_SIZE = 30,20
board_size, border_size = DISK_RADIUS * 2 * 4, 10
board_shift, disk_shift = (50, 80), 2
WIDTH, HEIGHT = DISK_RADIUS*2*4+2*board_shift[0], DISK_RADIUS*2*4+2*board_shift[1]+10

# Инициализация Pygame
pygame.init()
random.seed()

# Настройка экрана
screen = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.SysFont('arial', 32, True)
pygame.display.set_caption("Dustin Tight - v"+VERSION)
status_label, info_label = None, None

manager = UIManager((WIDTH, HEIGHT), 'theme.json')


def init_game(puzzle_name):
    global puzzle,moves

    puzzle = puzzle_set(puzzle_name)
    if len(puzzle)==0: return

    status_update()

####################################################################################################
####################################################################################################

def status_init():
    from pygame_gui.elements import UILabel
    status_label = UILabel( relative_rect=pygame.Rect(board_shift[0], 5, int(WIDTH)-2*board_shift[0], 20), text="Dustin Tight puzzle simulator" )
    info_label = UILabel( relative_rect=pygame.Rect(board_shift[0], int(HEIGHT)-70, int(WIDTH)-2*board_shift[0], 20), text="Info: " )
    return status_label, info_label

def status_update():
    status_label.set_text("Dustin Tight puzzle simulator")
    status_label.rebuild_from_changed_theme_data()

    solved = ""
    if puzzle_solved==puzzle:
        solved = ". Solved !"

    info_label.set_text("Moves: "+str(moves)+solved)
    info_label.rebuild_from_changed_theme_data()

def button_init():
    global puzzles_mas
    from pygame_gui.elements import UIButton, UIDropDownMenu, UITextBox, UICheckBox

    select_y, label_y, button_y = 30, int(HEIGHT)-117, int(HEIGHT)-42

    drop_size = 200
    drop_down_Puzzle = UIDropDownMenu( options_list=puzzles_mas, starting_option=puzzles_mas[0],
                                       relative_rect=pygame.Rect(int(WIDTH)//2-drop_size//2, select_y, drop_size, 30), manager=manager )

    button_Left  = UIButton((5, board_size//2+board_shift[1]-15, 30, 30), '<')
    button_Right = UIButton((int(WIDTH)-35, board_size//2+board_shift[1]-15, 30, 30), '>')

    button_Reset = UIButton((25, button_y, 70, 30), 'Reset')
    button_Scramble = UIButton((95, button_y, 90, 30), 'Scramble')
    button_About = UIButton((255, button_y, 70, 30), 'About')

    return (button_Reset, button_Scramble, button_About, drop_down_Puzzle, button_Left,button_Right)

def about_game():
    from pygame_gui.windows import UIMessageWindow

    message_window = UIMessageWindow( rect=pygame.Rect(board_shift[0],board_shift[1],board_size,board_size), window_title='About: Dustin 15 Simulator', always_on_top=True,
                     html_message='Grigorusha Puzzle Simulators: <a href="https://twistypuzzles.com/forum/viewtopic.php?t=38581">https://twistypuzzles.com/forum/viewtopic.php?t=38581</a><br>'+
                                  'Grigorusha Simulators Git: <a href="https://github.com/grigorusha/dustin">https://github.com/grigorusha/dustin</a>')
    return

####################################################################################################

def draw_digit(screen, num, color, x, y, angle):
    shift_y = 0
    text = font.render(str(num), True, color)
    rotated_text = pygame.transform.rotate(text, angle)
    text_rect = rotated_text.get_rect(center=(x, y+shift_y))
    screen.blit(rotated_text, text_rect)

def draw_puzzle():
    global puzzle,puzzle_parts

    shift = 3
    board = pygame.Rect(board_shift[0]-shift, board_shift[1]-shift, board_size+2*shift,board_size+2*shift)
    border = pygame.Rect(board_shift[0]-border_size-shift, board_shift[1]-border_size-shift, board_size+2*border_size+2*shift,board_size+2*border_size+2*shift)

    pygame.draw.rect(screen, clBlue, board)
    pygame.draw.rect(screen, clNavy, border, border_size)

    for pos_y1,str in enumerate(puzzle):
        for pos_x1,part in enumerate(str):
            if part%2==0: continue
            part_dict = dicmas_find(puzzle_parts, "num", part)
            para = part_dict["para"]
            x1,y1 = (pos_x1*2+1)*DISK_RADIUS + board_shift[0],(pos_y1*2+1)*DISK_RADIUS + board_shift[1]
            pygame.draw.circle(screen,part_dict["color"],(x1,y1),DISK_RADIUS-disk_shift)
            pygame.draw.aacircle(screen,clSeaGreen,(x1,y1),DISK_RADIUS-disk_shift+1, 2)
            if para!=None:
                pos_x2,pos_y2 = find_index(puzzle, para)
                x2,y2 = (pos_x2*2+1)*DISK_RADIUS + board_shift[0],(pos_y2*2+1)*DISK_RADIUS + board_shift[1]
                pygame.draw.circle(screen,part_dict["color"],(x2,y2),DISK_RADIUS-disk_shift)
                pygame.draw.aacircle(screen, clSeaGreen, (x2, y2), DISK_RADIUS - disk_shift + 1, 2)
                pygame.draw.line(screen,part_dict["color"],(x1,y1),(x2,y2),LINK_SIZE)

            draw_digit(screen, part, clBlack, x1,y1, part_dict["angle"])
            if para!=None:
                draw_digit(screen, para, clBlack, x2,y2, part_dict["angle"])

    return

####################################################################################################

def scramble_game(max_move=1000):
    num_pred = -1
    for nn in range(max_move):
        while True:
            while True:
                num = random.randint(1, 15)
                if num_pred!=num: break
            state = slide_part(num)
            if state:
                num_pred = num
                break
    return

def check_pos_part(x0,y0, x1,y1, x2=None,y2=None):
    if y0==y1:
        if x1==x0-1 or x1==x0+1:
            return 1
    elif x0==x1:
        if y1==y0-1 or y1==y0+1:
            return 1

    if x2!=None and y2!=None:
        if y0==y2:
            if x2==x0-1 or x2==x0+1:
                return 2
        elif x0==x2:
            if y2==y0-1 or y2==y0+1:
                return 2
    return 0

def slide_part(num):
    if num==0:
        return False
    elif num % 2 == 1: # 1,3,...,13,+15
        part = dicmas_find(puzzle_parts,"num",num)
    elif num % 2 == 0: # 2,4,...,14
        part = dicmas_find(puzzle_parts,"para",num)
    num,para = part["num"],part["para"]

    x0,y0 = find_index(puzzle, 0)
    x1,y1 = find_index(puzzle, num)
    x2,y2 = find_index(puzzle, para)

    if num==15:
        if check_pos_part(x0,y0, x1,y1):
            puzzle[y0][x0], puzzle[y1][x1] = num,0
            puzzle_parts_init(puzzle)
            return True
    else:
        res = check_pos_part(x0,y0, x1,y1, x2,y2)
        if res==1:
            puzzle[y0][x0], puzzle[y1][x1], puzzle[y2][x2] = num, para, 0
        elif res==2:
            puzzle[y0][x0], puzzle[y2][x2], puzzle[y1][x1] = para, num, 0
        if res:
            puzzle_parts_init(puzzle)
            return True
    return False

def check_and_part(mouse_pos):
    global puzzle, puzzle_parts
    xx,yy = mouse_pos

    if not ((board_shift[0]<xx<(WIDTH-board_shift[0])) and (board_shift[1]<yy<(HEIGHT-board_shift[1]))): return None

    x,y = (xx - board_shift[0])//(2*DISK_RADIUS), (yy - board_shift[1])//(2*DISK_RADIUS)
    x,y = 0 if x<0 else x, 0 if y<0 else y
    x,y = 3 if x>3 else x, 3 if y>3 else y

    num = puzzle[y][x]
    return num

def rotate_board(direction):
    global puzzle,puzzle_parts

    rotate_matrix(puzzle, direction)
    puzzle_parts_init(puzzle)
    # for part in puzzle_parts:
    #     part["angle"] = (part["angle"]-90*direction) % 360

####################################################################################################

def events_work(events, button_Reset, button_Scramble, button_About, drop_down_Puzzle, button_Left,button_Right):
    from pygame_gui import UI_BUTTON_PRESSED, UI_DROP_DOWN_MENU_CHANGED, UI_CHECK_BOX_CHECKED, UI_CHECK_BOX_UNCHECKED
    global puzzle, puzzle_name, moves

    for event in events:
        mouse_pos = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == button_Reset:
                init_game(puzzle_name)
                moves = 0
                status_update()
            elif event.ui_element == button_Scramble:
                scramble_game()
                moves = 0
                status_update()
            elif event.ui_element == button_About:
                about_game()

            elif event.ui_element == button_Left:
                rotate_board(-1)
                status_update()
            elif event.ui_element == button_Right:
                rotate_board(1)
                status_update()

        elif event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
            if event.ui_element == drop_down_Puzzle:
                puzzle_name = drop_down_Puzzle.selected_option[0]
                if puzzle_name:
                    init_game(puzzle_name)
                    moves = 0
                    status_update()
        elif event.type == pygame_gui.UI_TEXT_BOX_LINK_CLICKED:
            link = event.link_target
            if link != "":
                webbrowser.open(link, new=2, autoraise=True)

        elif event.type == pygame.MOUSEBUTTONDOWN and (event.button == 1):
            num = check_and_part(mouse_pos)
            if num:
                slide_part(num)
                moves += 1
                status_update()

        manager.process_events(event)

def main():
    global puzzle,puzzle_name, status_label,info_label

    close_spalsh_screen()

    current_path = get_pyinstaller_temp_path()
    icon = os.path.join(current_path,"Dustin15.png")
    if os.path.isfile(icon):
        pygame.display.set_icon(pygame.image.load(icon))

    status_label, info_label = status_init()
    init_game(puzzle_name)

    (button_Reset, button_Scramble, button_About, drop_down_Puzzle, button_Left,button_Right) = button_init()

    clock = pygame.time.Clock()
    while True:
        time_delta = clock.tick(60) / 1000.0

        # обработка событий
        events = pygame.event.get()
        events_work(events, button_Reset, button_Scramble, button_About, drop_down_Puzzle, button_Left,button_Right)

        # Отрисовка доски
        screen.fill(clWhite)

        # Рисуем Поле
        draw_puzzle()

        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.flip()
        clock.tick(60)

main()