#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  4 00:45:03 2023

@author: dev
"""

import tkinter as tk
import time
from minesweeper_helpers import generate_hidden_numbers, generate_mines

x_size = None
y_size = None
num_mines = None
text_size = None
buttons = None
root = None
message_label = None
start_time = None
game_over = None
stopwatch_label = None
flags_label = None
first_click = True
layout_buttons = [[None for _ in range(2)] for _ in range(2)]
base_arr = None
numbers = None

def init():
    global x_size
    global y_size
    global num_mines
    global text_size
    global buttons
    global root
    global message_label
    global start_time
    global game_over
    global stopwatch_label
    global flags_label
    global first_click
    global base_arr
    global numbers
    
    first_click = True

    num_mines = int(0.15*x_size*y_size)
    text_size = 8
    buttons = [[None for _ in range(y_size)] for _ in range(x_size)]
    message_label = None
    start_time = None
    game_over = False
    stopwatch_label = None
    flags_label = None
    
    base_arr = generate_mines(x_size, y_size, num_mines)
    numbers = generate_hidden_numbers(base_arr, x_size, y_size)
    
    base_arr = base_arr[1:x_size+1, 1:y_size+1]
    num_mines = sum(sum(base_arr))

    return base_arr, numbers, num_mines

def count_flags():
    global buttons

    flags = 0
    for i in range(x_size):
        for j in range(y_size):
            if buttons[i][j].cget("background") == "sky blue":
                flags += 1
    return flags

def check_win():
    global num_mines

    return count_flags() == num_mines

def burst(base_arr):
    global buttons
    global message_label
    global game_over
    global num_mines

    game_over = True

    for i in range(x_size):
        for j in range(y_size):
            if base_arr[i, j] == 1:
                if buttons[i][j].cget("background") == "sky blue":
                    buttons[i][j].config(text="X", bg="light green", disabledforeground="white", state=tk.DISABLED)
                else:
                    buttons[i][j].config(text="X", bg="crimson", disabledforeground="white", state=tk.DISABLED)
                root.update()
                time.sleep(0.99/(num_mines))  # Delay is in seconds
            else:
                buttons[i][j].config(state=tk.DISABLED)

    message_label.config(text="Game Over! You Lost....")


def show_numbers(base_arr, numbers, x, y):
    global x_size
    global y_size
    global buttons
    global root

    pixels_to_check = [(x, y)]

    def reveal_next_cell():
        nonlocal pixels_to_check

        if pixels_to_check:
            x, y = pixels_to_check.pop(0)

            if base_arr[x, y] == 0 and buttons[x][y]['state'] != tk.DISABLED:
                if numbers[x, y] == 0:
                    buttons[x][y].config(bg="gray", state=tk.DISABLED)
                    for dx in [-1, 0, 1]:
                        for dy in [-1, 0, 1]:
                            new_x, new_y = x + dx, y + dy
                            if 0 <= new_x < x_size and 0 <= new_y < y_size:
                                pixels_to_check.append((new_x, new_y))
                else:
                    buttons[x][y].config(text=numbers[x, y], bg="white", disabledforeground="green")

            root.after(int(400/(x_size*y_size)), reveal_next_cell)  # Delay is in milliseconds

    reveal_next_cell()

def start_stopwatch():
    global stopwatch_label
    global start_time

    if start_time is None:
        start_time = time.time()
        update_stopwatch()
    
def format_time():
    global start_time
    
    current_time = int(time.time() - start_time)
    mins, secs = divmod(current_time, 60)
    mins = '0'+str(mins) if mins<10 else str(mins)
    secs = '0'+str(secs) if secs<10 else str(secs)
    time_text = mins+':'+secs
    
    return time_text

def update_stopwatch():
    global stopwatch_label

    time_text = format_time()
    if not game_over:  # Check if the stopwatch should continue updating
        stopwatch_label.config(text="Time: {}".format(time_text))
        stopwatch_label.after(1000, update_stopwatch)  # Continue updating every second
    else:
        stopwatch_label.config(text="Time: {}".format(time_text))


def reveal_cell(base_arr, numbers, x, y, left_click=False):
    global x_size
    global y_size
    global buttons
    global flags_label
    global num_mines
    global game_over
    global first_click

    if left_click:  # Left click (reveal)
        if buttons[x][y]['text'] == "F":
            return  # Skip burst if cell is flagged

        # if color of cell is white, do reveal_onclick
        if buttons[x][y].cget("background") == "white":
            reveal_onclick(base_arr, numbers, x, y)

        if base_arr[x, y] == 1:
            burst(base_arr)
            return
        elif numbers[x, y] == 0:
            show_numbers(base_arr, numbers, x, y)
        else:
            buttons[x][y].config(text=numbers[x, y], bg = "white", disabledforeground="green")

    else:  # Right click (flagging)
        if buttons[x][y]['text'] == "":
            buttons[x][y].config(text="F", bg="sky blue", disabledforeground="blue")
        elif buttons[x][y]['text'] == "F":
            buttons[x][y].config(text="", bg="light gray",  disabledforeground="black")
            
    if first_click:
        start_stopwatch()
        first_click = False

    if check_win():
        message_label.config(text="Congratulations! You won....")
        game_over = True
        for i in range(x_size):
            for j in range(y_size):
                buttons[i][j].config(state=tk.DISABLED)

    flags_label.config(text="Mines caught: {} / {}".format(count_flags(), num_mines))
    return

def reveal_onclick(base_arr, numbers, x, y):
    global buttons

    flags = 0
    for i in range(max(x-1, 0), min(x+2, x_size)):
        for j in range(max(y-1, 0), min(y+2, y_size)):
            if buttons[i][j].cget("background") == "sky blue":
                flags += 1

    if flags == numbers[x, y]:
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                new_x, new_y = x + i, y + j
                if (0 <= new_x < x_size) and (0 <= new_y < y_size) and buttons[new_x][new_y].cget("background") != "white":
                    reveal_cell(base_arr, numbers, new_x, new_y, left_click=True)
                    time.sleep(1/(x_size*y_size))

    return

def choose_layout():
    global root
    
    if root == None:
        root = tk.Tk()
        root.title('Minesweeper')
    
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
        root.rowconfigure(i, weight=1)
        for j in range(2):
            root.columnconfigure(j, weight=1)
            layout_buttons[i][j] = tk.Button(
                root,
                width=30,
                height=15,
                text=text_config(i, j),
                font=("Arial", 20),
                command=lambda i=i, j=j: create_layout(2*i+j)
            )

            layout_buttons[i][j].bind("<Button-3>", lambda event, i=i, j=j: create_layout(2*i+j))
            layout_buttons[i][j].grid(row=i, column=j, sticky="nsew")
        
    root.mainloop()
    return

def create_layout(opt):
    global x_size
    global y_size
    global layout_buttons
    global base_arr
    global numbers
    global num_mines
    
    if opt == 0:
        x_size, y_size = 8, 8
    elif opt == 1:
        x_size, y_size = 16, 16
    elif opt == 2:
        x_size, y_size = 16, 32
    else:
        x_size, y_size = 32, 32
        
    for i in range(2):
        for j in range(2):
            layout_buttons[i][j].destroy()
            
    base_arr, numbers, num_mines = init()
    
    return base_arr, numbers, num_mines

def start():
    global buttons
    global root
    global message_label
    global flags_label
    global stopwatch_label
    global num_mines
    global x_size
    global y_size
    global layout_buttons
    global base_arr
    global numbers
    
    root = tk.Tk()
    root.title('Minesweeper')

    for i in range(x_size):
        root.rowconfigure(i, weight=1)
        for j in range(y_size):
            root.columnconfigure(j, weight=1)
            buttons[i][j] = tk.Button(
                root,
                width=4,
                height=2,
                text="",
                command=lambda i=i, j=j: reveal_cell(base_arr, numbers, i, j, left_click=True)
            )

            buttons[i][j].bind("<Button-3>", lambda event, i=i, j=j: reveal_cell(base_arr, numbers, i, j, left_click=False))
            buttons[i][j].grid(row=i, column=j, sticky="nsew")

    side_panel = tk.Frame(root)
    side_panel.grid(row=0, column=y_size, rowspan=x_size + 2, sticky="ns")

    stopwatch_label = tk.Label(side_panel, text="Time: 00:00", font=("Arial", 14))
    stopwatch_label.pack(pady=10)

    flags_label = tk.Label(side_panel, text="Mines caught: 0 / {}".format(num_mines), font=("Arial", 14))
    flags_label.pack(pady=10)

    message_label = tk.Label(root, text="", font=("Arial", 20))
    message_label.grid(row=x_size, columnspan=y_size, sticky="ew")

    restart_button = tk.Button(root, height=2, text="Restart", font=("Arial", 20), command=restart_game)
    restart_button.grid(row=x_size + 1, columnspan=y_size, sticky="ew")
    
    root.mainloop()

def restart_game():
    global buttons
    global root
    global message_label
    global flags_label
    global num_mines
    global game_over

    game_over = False

    message_label.config(text="")

    for i in range(x_size):
        for j in range(y_size):
            buttons[i][j].destroy()

    start()

    start_stopwatch()
    flags_label.config(text="Flags: 0 / {}".format(num_mines))

choose_layout()

# FIXME: REMOVE LATER
if x_size is not None:
    print('Size set!', x_size)
    
start()
