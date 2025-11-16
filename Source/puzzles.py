from utils import *

# цвета
clWhite, clGainsboro, clSilver, clGray, clBlack     = '#F0F0F0', '#C0C0C0', '#A0A0A0', '#707070', '#202020'
clCyan, clDeepSky, clTeal, clBlue, clNavy           = '#00FFFF', '#00BFFF', '#008080', '#0000FF', '#000080'
clCoral, clRed, clCrimson, clIndian, clBrown        = '#FF7F50', '#FF0000', '#DC143C', '#CD5C5C', '#800000'
clYellow, clOrange, clKhaki, clGolden, clOlive      = '#FFFF00', '#FF6000', '#F0E68C', '#DDBB20', '#808000'
clGreenYellow, clLime, clSea, clGreen, clDarkGreen  = '#ADFF2F', '#00FF00', '#3cb371', '#008000', '#006400'
clPink, clFuchsia, clPale, clOrchid, clLilia, clPurple = '#FF69B4', '#FF00FF', '#D07090', '#DA70D6', '#D080F0', '#800080'
clChocolate, clPeru, clSandyBrown           = '#C26519', '#CD853F', '#F4A460'
clIndigo, clDarkSlate, clSlate              = '#4B0082', '#483D8B', '#6A5ACD'
clSeaGreen, clAquaMarine, clDarkSeaGreen    = '#2E8B57', '#66CDAA', '#8FBC8F'

puzzle = []
puzzle_solved = [ [ 1, 2, 3, 4],
                  [ 5, 6, 7, 8],
                  [ 9,10,11,12],
                  [13,14,15, 0] ]
puzzle_parts = [
    dict(num=1, para=2, angle=0, color=clWhite),
    dict(num=3, para=4, angle=0, color=clCyan),
    dict(num=5, para=6, angle=0, color=clCyan),
    dict(num=7, para=8, angle=0, color=clWhite),
    dict(num=9, para=10, angle=0, color=clWhite),
    dict(num=11, para=12, angle=0, color=clCyan),
    dict(num=13, para=14, angle=0, color=clCyan),
    dict(num=15, para=None, angle=0, color=clWhite) ]

puzzles_mas = [ "Solved puzzle", "Original task", "Swap - 15/14-13", "Rotate part - 13-14", "Mirror puzzle", "Rotate 90 puzzle", "Rotate 180 puzzle", "Rotate 270 puzzle" ]
puzzle_name = puzzles_mas[0]

moves = 0

def puzzle_parts_init(puzzle):
    global puzzle_parts
    for part in puzzle_parts:
        x1,y1 = find_index(puzzle, part["num"])
        if part["para"]==0:
            part["angle"] = 0
        else:
            x2,y2 = find_index(puzzle, part["para"])

            if y1==y2:
                part["angle"] = 0 if x1<x2 else 180
            elif x1==x2:
                part["angle"] = 90 if y1>y2 else 270
            else:
                part["angle"] = 0

def puzzle_set(puzzle_name):
    puzzle_start = []
    if puzzle_name in puzzles_mas:
        if puzzle_name == "Solved puzzle":
            puzzle_start = [ [ 1,  2,  3,  4],
                             [ 5,  6,  7,  8],
                             [ 9, 10, 11, 12],
                             [13, 14, 15,  0]]
        elif puzzle_name == "Original task":
            puzzle_start = [ [13,14,15, 0],
                             [ 9,10,11,12],
                             [ 5, 6, 7, 8],
                             [ 1, 2, 3, 4] ]
        elif puzzle_name == "Swap - 15/14-13":
            puzzle_start = [ [ 1,  2,  3,  4],
                             [ 5,  6,  7,  8],
                             [ 9, 10, 11, 12],
                             [15, 13, 14,  0]]
        elif puzzle_name == "Rotate part - 13-14":
            puzzle_start = [ [ 1,  2,  3,  4],
                             [ 5,  6,  7,  8],
                             [ 9, 10, 11, 12],
                             [14, 13, 15,  0]]
        elif puzzle_name == "Mirror puzzle":
            puzzle_start = [ [ 3,  4,  1,  2],
                             [ 7,  8,  5,  6],
                             [11, 12,  9, 10],
                             [ 0, 15, 13, 14]]
        elif puzzle_name == "Rotate 90 puzzle":
            puzzle_start = [ [13,  9,  5,  1],
                             [14, 10,  6,  2],
                             [15, 11,  7,  3],
                             [ 0, 12,  8,  4]]
        elif puzzle_name == "Rotate 180 puzzle":
            puzzle_start = [ [ 0, 15, 14, 13],
                             [12, 11, 10,  9],
                             [ 8,  7,  6,  5],
                             [ 4,  3,  2,  1]]
        elif puzzle_name == "Rotate 270 puzzle":
            puzzle_start = [ [ 4,  8, 12,  0],
                             [ 3,  7, 11, 15],
                             [ 2,  6, 10, 14],
                             [ 1,  5,  9, 13]]
    else:
        puzzle_start = [[1, 2, 3, 4],
                        [5, 6, 7, 8],
                        [9, 10, 11, 12],
                        [13, 14, 15, 0]]
    puzzle_parts_init(puzzle_start)
    return puzzle_start

