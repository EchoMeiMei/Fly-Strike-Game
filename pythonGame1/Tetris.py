# -*- coding = utf-8 -*-
# @time : 2021/9/18 19:54
# @Author : Wu
# @File : Tetris.py
# @Software : PyCharm

import tkinter as tk
import random

FPS=500
R=20
C=12
cell_size=30
height=R*cell_size
width=C*cell_size

SHAPES={
    "O":[(-1,-1),(0,-1),(-1,0),(0,0)],
    "Z":[(-1,-1),(0,-1),(0,0),(1,0)],
    "S":[(0,-1),(1,-1),(-1,0),(0,0)],
    "T":[(-1,-1),(0,-1),(1,-1),(0,0)],
    "I":[(0,-2),(0,-1),(0,0),(0,1)],
    "L":[(-1,-2),(-1,-1),(-1,0),(0,0)],
    "J":[(0,-2),(0,-1),(-1,0),(0,0)]
}

SHAPESCOLOR={
    "O":"blue",
    "Z":"Cyan",
    "S":"red",
    "T":"yellow",
    "I":"green",
    "L":"purple",
    "J":"orange"
}

def draw_cell_by_cr(canvas,c,r,color="#CCCCCC"):
    x0=c*cell_size
    y0=r*cell_size

    x1=c*cell_size+cell_size
    y1=r*cell_size+cell_size
    canvas.create_rectangle(x0,y0,x1,y1,fill=color,outline="white",width=2)

def draw_black_board(canvas):
    for ri in range(R):
        for ci in range (C):
            draw_cell_by_cr(canvas,ci,ri)

def draw_cells(canvas,c,r,cell_list,color="#CCCCCC"):
    for cell in cell_list:
        cell_c,cell_r=cell
        ci=cell_c+c
        ri=cell_r+r
        if 0<=c<C and 0<=r<R:
            draw_cell_by_cr(canvas,ci,ri,color)

win=tk.Tk()

canvas=tk.Canvas(win,width=width,height=height)
canvas.pack()
draw_black_board(canvas)

block_list=[]
for i in range(R):
    i_row=[''for j in range(C)]
    block_list.append(i_row)

def draw_block_move(canvas,block,direction=[0,0]):
    shape_type=block['kind']
    c,r=block['cr']
    cell_list=block['cell_list']

    draw_cells(canvas,c,r,cell_list)

    dc,dr=direction
    new_c,new_r=c+dc,r+dr
    block['cr']=[new_c,new_r]
    draw_cells(canvas,new_c,new_r,cell_list,SHAPESCOLOR[shape_type])


def generate_new_block():
    #随机生成俄罗斯方块
    kind=random.choice(list(SHAPES.keys()))
    cr=[C//2,0]
    new_block={
        "kind":kind,
        "cell_list":SHAPES[kind],
        "cr":cr
    }
    return new_block

def check_move(block,direction=[0,0]):
    cc,cr=block['cr']
    cell_list=block['cell_list']

    for cell in cell_list:
        cell_c,cell_r=cell
        c=cell_c+cc+direction[0]
        r=cell_r+cr+direction[1]

        if c<0 or c>=C or r>=R:
            return False

        if r>=0 and block_list[r][c]:
            return False
    return True

def save_to_block_list(block):
    shape_type=block['kind']
    cc,cr=block['cr']
    cell_list=block['cell_list']

    for cell in cell_list:
        cell_c,cell_r=cell
        c=cell_c+cc
        r=cell_r+cr
        block_list[r][c]=shape_type

def horizontal_move_block(event):
    direction=[0,0]
    if event.keysym=='Left':
        direction=[-1,0]
    elif event.keysym=='Right':
        direction=[1,0]
    else:
        return

    global current_block
    if current_block is not None and check_move(current_block,direction):
        draw_block_move(canvas,current_block,direction)

def rotate_block(event):
    global current_block
    if current_block is None:
        return

    cell_list=current_block['cell_list']
    rotate_list=[]
    for cell in cell_list:
        cell_c,cell_r=cell
        rotate_cell=[cell_r,cell_c]
        rotate_list.append(rotate_cell)

    block_after_rotate={
        'kind':current_block['kind'],
        'cell_list':rotate_list,
        'cr':current_block['cr']
    }
    if check_move(block_after_rotate):
        cc,cr=current_block['cr']
        draw_cell_by_cr(canvas,cc,cr,current_block['cell_list'])
        draw_cell_by_cr(canvas, cc, cr, rotate_list,SHAPESCOLOR[current_block['kind']])
        current_block=block_after_rotate

def land(event):
    global current_block
    if current_block is None:
        return
    cell_list=current_block['cell_list']
    cc,cr=current_block['cr']
    min_height=R
    for cell in cell_list:
        cell_c,cell_r=cell
        c,r=cell_c+cc,cell_r+cr
        if block_list[r][c]:
            return

        h=0
        for ri in range(r+1,R):
            if block_list[ri][c]:
                break
            else:
                h+=1
        if h<min_height:
            min_height=h
    down=[0,min_height]
    if check_move(current_block,down):
        draw_block_move(canvas,current_block,down)

def game_loop():
    win.update()
    global current_block
    if current_block is None:
        new_block=generate_new_block()
        draw_block_move(canvas,new_block)
        current_block=new_block
    else:
        if check_move(current_block,[0,1]):
            draw_block_move(canvas,current_block,[0,1])
        else:
            save_to_block_list(current_block)
            current_block=None

    win.after(FPS,game_loop)

current_block=None

canvas.focus_set()
canvas.bind("<KeyPress-Left>",horizontal_move_block)
canvas.bind("<KeyPress-Right>",horizontal_move_block)
canvas.bind("<KeyPress-Up>",rotate_block)
canvas.bind("<KeyPress-Down>",land)

game_loop()
win.mainloop()