#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  4 00:45:03 2023

@author: dev
"""

import tkinter as tk
import time
from minesweeper_helpers import generate_hidden_numbers, generate_mines

X_SIZE = None
Y_SIZE = None
NUM_MINES = None
TEXT_SIZE = None
BUTTONS = None
ROOT = None
MESSAGE_LABEL = None
START_TIME = None
GAME_OVER = None
STOPWATCH_LABEL = None
FLAGS_LABEL = None
FIRST_CLICK = True
LAYOUT_BUTTONS = [[None for _ in range(2)] for _ in range(2)]
BASE_ARR = None
NUMBERS = None


def init():
    global X_SIZE
    global Y_SIZE
    global NUM_MINES
    global TEXT_SIZE
    global BUTTONS
    global ROOT
    global MESSAGE_LABEL
    global START_TIME
    global GAME_OVER
    global STOPWATCH_LABEL
    global FLAGS_LABEL
    global FIRST_CLICK
    global BASE_ARR
    global NUMBERS

    FIRST_CLICK = True

    NUM_MINES = int(0.15*X_SIZE*Y_SIZE)
    TEXT_SIZE = 8
    BUTTONS = [[None for _ in range(Y_SIZE)] for _ in range(X_SIZE)]
    MESSAGE_LABEL = None
    START_TIME = None
    GAME_OVER = False
    STOPWATCH_LABEL = None
    FLAGS_LABEL = None

    BASE_ARR = generate_mines(X_SIZE, Y_SIZE, NUM_MINES)
    NUMBERS = generate_hidden_numbers(BASE_ARR, X_SIZE, Y_SIZE)

    BASE_ARR = BASE_ARR[1:X_SIZE+1, 1:Y_SIZE+1]
    NUM_MINES = sum(sum(BASE_ARR))

    return BASE_ARR, NUMBERS, NUM_MINES


def count_flags():
    global BUTTONS

    flags = 0
    for i in range(X_SIZE):
        for j in range(Y_SIZE):
            if BUTTONS[i][j].cget("background") == "sky blue":
                flags += 1
    return flags


def check_win():
    global NUM_MINES

    return count_flags() == NUM_MINES


def burst(BASE_ARR):
    global BUTTONS
    global MESSAGE_LABEL
    global GAME_OVER
    global NUM_MINES

    GAME_OVER = True

    for i in range(X_SIZE):
        for j in range(Y_SIZE):
            if BASE_ARR[i, j] == 1:
                if BUTTONS[i][j].cget("background") == "sky blue":
                    BUTTONS[i][j].config(
                        text="X", bg="light green", disabledforeground="white", state=tk.DISABLED)
                else:
                    BUTTONS[i][j].config(
                        text="X", bg="crimson", disabledforeground="white", state=tk.DISABLED)
                ROOT.update()
                time.sleep(0.99/(NUM_MINES))  # Delay is in seconds
            else:
                BUTTONS[i][j].config(state=tk.DISABLED)

    MESSAGE_LABEL.config(text="Game Over! You Lost....")


def show_numbers(BASE_ARR, NUMBERS, x, y):
    global X_SIZE
    global Y_SIZE
    global BUTTONS
    global ROOT

    pixels_to_check = [(x, y)]

    def reveal_next_cell():
        nonlocal pixels_to_check

        if pixels_to_check:
            x, y = pixels_to_check.pop(0)

            if BASE_ARR[x, y] == 0 and BUTTONS[x][y]['state'] != tk.DISABLED:
                if NUMBERS[x, y] == 0:
                    BUTTONS[x][y].config(bg="gray", state=tk.DISABLED)
                    for dx in [-1, 0, 1]:
                        for dy in [-1, 0, 1]:
                            new_x, new_y = x + dx, y + dy
                            if 0 <= new_x < X_SIZE and 0 <= new_y < Y_SIZE:
                                pixels_to_check.append((new_x, new_y))
                else:
                    BUTTONS[x][y].config(
                        text=NUMBERS[x, y], bg="white", disabledforeground="green")

            # Delay is in milliseconds
            ROOT.after(int(400/(X_SIZE*Y_SIZE)), reveal_next_cell)

    reveal_next_cell()


def start_stopwatch():
    global STOPWATCH_LABEL
    global START_TIME

    if START_TIME is None:
        START_TIME = time.time()
        update_stopwatch()


def format_time():
    global START_TIME

    current_time = int(time.time() - START_TIME)
    mins, secs = divmod(current_time, 60)
    mins = '0'+str(mins) if mins < 10 else str(mins)
    secs = '0'+str(secs) if secs < 10 else str(secs)
    time_text = mins+':'+secs

    return time_text


def update_stopwatch():
    global STOPWATCH_LABEL

    time_text = format_time()
    if not GAME_OVER:  # Check if the stopwatch should continue updating
        STOPWATCH_LABEL.config(text="Time: {}".format(time_text))
        # Continue updating every second
        STOPWATCH_LABEL.after(1000, update_stopwatch)
    else:
        STOPWATCH_LABEL.config(text="Time: {}".format(time_text))


def reveal_cell(BASE_ARR, NUMBERS, x, y, left_click=False):
    global X_SIZE
    global Y_SIZE
    global BUTTONS
    global FLAGS_LABEL
    global NUM_MINES
    global GAME_OVER
    global FIRST_CLICK

    if left_click:  # Left click (reveal)
        if BUTTONS[x][y]['text'] == "F":
            return  # Skip burst if cell is flagged

        # if color of cell is white, do reveal_onclick
        if BUTTONS[x][y].cget("background") == "white":
            reveal_onclick(BASE_ARR, NUMBERS, x, y)

        if BASE_ARR[x, y] == 1:
            burst(BASE_ARR)
            return
        elif NUMBERS[x, y] == 0:
            show_numbers(BASE_ARR, NUMBERS, x, y)
        else:
            BUTTONS[x][y].config(text=NUMBERS[x, y],
                                 bg="white", disabledforeground="green")

    else:  # Right click (flagging)
        if BUTTONS[x][y]['text'] == "":
            BUTTONS[x][y].config(text="F", bg="sky blue",
                                 disabledforeground="blue")
        elif BUTTONS[x][y]['text'] == "F":
            BUTTONS[x][y].config(text="", bg="light gray",
                                 disabledforeground="black")

    if FIRST_CLICK:
        start_stopwatch()
        FIRST_CLICK = False

    if check_win():
        MESSAGE_LABEL.config(text="Congratulations! You won....")
        GAME_OVER = True
        for i in range(X_SIZE):
            for j in range(Y_SIZE):
                BUTTONS[i][j].config(state=tk.DISABLED)

    FLAGS_LABEL.config(
        text="Mines caught: {} / {}".format(count_flags(), NUM_MINES))
    return


def reveal_onclick(BASE_ARR, NUMBERS, x, y):
    global BUTTONS

    flags = 0
    for i in range(max(x-1, 0), min(x+2, X_SIZE)):
        for j in range(max(y-1, 0), min(y+2, Y_SIZE)):
            if BUTTONS[i][j].cget("background") == "sky blue":
                flags += 1

    if flags == NUMBERS[x, y]:
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                new_x, new_y = x + i, y + j
                if (0 <= new_x < X_SIZE) and (0 <= new_y < Y_SIZE) and BUTTONS[new_x][new_y].cget("background") != "white":
                    reveal_cell(BASE_ARR, NUMBERS, new_x,
                                new_y, left_click=True)
                    time.sleep(1/(X_SIZE*Y_SIZE))

    return


def choose_layout():
    global ROOT

    if ROOT == None:
        ROOT = tk.Tk()
        ROOT.title('Minesweeper')

    def text_config(i, j):
        if 2*i+j == 0:
            return "8x8\n9 mines"
        elif 2*i+j == 1:
            return "16x16\n38 mines"
        elif 2*i+j == 2:
            return "16x32\n76 mines"
        else:
            return "32x32\n153 mines"

    for i in range(2):
        ROOT.rowconfigure(i, weight=1)
        for j in range(2):
            ROOT.columnconfigure(j, weight=1)
            LAYOUT_BUTTONS[i][j] = tk.Button(
                ROOT,
                width=30,
                height=15,
                text=text_config(i, j),
                font=("Arial", 20),
                command=lambda i=i, j=j: create_layout(2*i+j)
            )

            LAYOUT_BUTTONS[i][j].bind(
                "<Button-3>", lambda event, i=i, j=j: create_layout(2*i+j))
            LAYOUT_BUTTONS[i][j].grid(row=i, column=j, sticky="nsew")

    ROOT.mainloop()
    return


def create_layout(opt):
    global X_SIZE
    global Y_SIZE
    global LAYOUT_BUTTONS
    global BASE_ARR
    global NUMBERS
    global NUM_MINES

    if opt == 0:
        X_SIZE, Y_SIZE = 8, 8
    elif opt == 1:
        X_SIZE, Y_SIZE = 16, 16
    elif opt == 2:
        X_SIZE, Y_SIZE = 16, 32
    else:
        X_SIZE, Y_SIZE = 32, 32

    for i in range(2):
        for j in range(2):
            LAYOUT_BUTTONS[i][j].destroy()

    start()

    return BASE_ARR, NUMBERS, NUM_MINES


def start():
    global BUTTONS
    global ROOT
    global MESSAGE_LABEL
    global FLAGS_LABEL
    global STOPWATCH_LABEL
    global NUM_MINES
    global X_SIZE
    global Y_SIZE
    global LAYOUT_BUTTONS
    global BASE_ARR
    global NUMBERS

    BASE_ARR, NUMBERS, NUM_MINES = init()

    for i in range(X_SIZE):
        ROOT.rowconfigure(i, weight=1)
        for j in range(Y_SIZE):
            ROOT.columnconfigure(j, weight=1)
            BUTTONS[i][j] = tk.Button(
                ROOT,
                width=4,
                height=2,
                text="",
                command=lambda i=i, j=j: reveal_cell(
                    BASE_ARR, NUMBERS, i, j, left_click=True)
            )

            BUTTONS[i][j].bind("<Button-3>", lambda event, i=i,
                               j=j: reveal_cell(BASE_ARR, NUMBERS, i, j, left_click=False))
            BUTTONS[i][j].grid(row=i, column=j, sticky="nsew")

    side_panel = tk.Frame(ROOT)
    side_panel.grid(row=0, column=Y_SIZE, rowspan=X_SIZE + 2, sticky="ns")

    STOPWATCH_LABEL = tk.Label(
        side_panel, text="Time: 00:00", font=("Arial", 14))
    STOPWATCH_LABEL.pack(pady=10)

    FLAGS_LABEL = tk.Label(
        side_panel, text="Mines caught: 0 / {}".format(NUM_MINES), font=("Arial", 14))
    FLAGS_LABEL.pack(pady=10)

    MESSAGE_LABEL = tk.Label(ROOT, text="", font=("Arial", 20))
    MESSAGE_LABEL.grid(row=X_SIZE, columnspan=Y_SIZE, sticky="ew")

    restart_button = tk.Button(ROOT, height=2, text="Restart", font=(
        "Arial", 20), command=restart_game)
    restart_button.grid(row=X_SIZE + 1, columnspan=Y_SIZE, sticky="ew")


def restart_game():
    global BUTTONS
    global ROOT
    global MESSAGE_LABEL
    global FLAGS_LABEL
    global NUM_MINES
    global GAME_OVER

    GAME_OVER = False

    MESSAGE_LABEL.config(text="")

    for i in range(X_SIZE):
        for j in range(Y_SIZE):
            BUTTONS[i][j].destroy()

    start()

    FLAGS_LABEL.config(text="Mines caught: 0 / {}".format(NUM_MINES))


choose_layout()
