# -*- coding = utf-8 -*-
# @time : 2021/9/15 22:35
# @Author : Wu
# @File : flyGame.py
# @Software : PyCharm

import pygame
import random
import math

#1.初始化界面
pygame.init()
screen=pygame.display.set_mode((800,600))  #设置显示屏幕宽*高=800*600
pygame.display.set_caption('飞机大战')
icon=pygame.image.load('R-C.jpg')
pygame.display.set_icon(icon)

#添加背景音效
pygame.mixer.music.load('bg.mp3')
pygame.mixer.music.play(-1)  #参数-1 为单曲循环

#添加射中音效
bao_sound=pygame.mixer.Sound('hit.mp3')

bgImg=pygame.image.load('bg.jpg')  #800*600
#5.飞机
playerImg=pygame.image.load('player.png')  #80*100
playerX=350
playerY=500
playerStep=0  #玩家移动

#分数
score=0
font=pygame.font.Font('freesansbold.ttf',32)
def show_score():
    text=f"Score:{score}"
    score_render=font.render(text,True,(0,255,0))
    screen.blit(score_render,(10,10))

#子弹发数
font2=pygame.font.Font('freesansbold.ttf',32)
def show_bullet_num():
    text=f"bullet_num:{bullet_num}"
    score_render=font2.render(text,True,(180,180,180))
    screen.blit(score_render,(10,40))

#游戏结束语
font1=pygame.font.Font('freesansbold.ttf',64)
def check_isOver():
    if is_over:
        text=f"Game Over"
        game_render=font1.render(text,True,(255,0,0))
        screen.blit(game_render,(200,275))

#游戏结束
is_over=False

#添加敌人
number_of_enemies=random.randint(6,12)

#定义一个敌人类
class Enemy():
    def __init__(self):
        self.Img=pygame.image.load('monster.png')
        self.x=random.randint(200,600)
        self.y=random.randint(50,250)
        self.step=random.uniform(0.2,0.35)
    #当被射中时，恢复位置
    def reset(self):
        self.x=random.randint(200,600)
        self.y=random.randint(50,70)

#子弹类
class Bullet():
    def __init__(self):
        self.Img=pygame.image.load('bullet.png')
        self.x=playerX+25
        self.y=playerY-10
        self.step=2  #子弹移动的速度

    def hit(self):
        global score
        for e in enemies:
            if (distance(self.x,self.y,e.x,e.y)<30):
                #射中
                bao_sound.play()
                bullets.remove(self)
                e.reset()
                score+=1
                print(score)

#两点之间的距离
def distance(bx,by,ex,ey):
    a=bx-ex
    b=by-ey
    return math.sqrt(a*a+b*b) #开根号



bullets=[]  #保存现有的子弹

enemies=[]
for i in range(number_of_enemies):
    enemies.append(Enemy())

#显示敌人并实现敌人下沉
def show_enemy():
    global is_over
    for e in enemies:
        screen.blit(e.Img,(e.x,e.y))
        #敌人移动
        e.x+=e.step
        if e.x>720 or e.x<0:
            e.step*=-1
            e.y+=20
            if e.y>450:
                is_over=True
                print("Game Over!")
                enemies.clear()

#显示并移动子弹
def show_bullets():
    for b in bullets:
        screen.blit(b.Img,(b.x,b.y))
        b.hit()  #是否击中
        b.y-=b.step      #移动子弹
        if b.y<0:
            bullets.remove(b)

def move_player():
    global playerX
    # 控制飞机的移动
    playerX += playerStep
    # 防止飞机出界
    if playerX > 720:
        playerX = 720
    if playerX < 0:
        playerX = 0
#游戏主循环
bullet_num=0
running=True
while True:
    screen.blit(bgImg,(0,0))   #坐标系定义：右上角为（0,0）
    show_score()  #显示分数
    show_bullet_num()
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        #通过键盘按键控制飞机的移动
        if event.type==pygame.KEYDOWN:  #按下按键，则开始移动
            if event.key==pygame.K_RIGHT:
                playerStep=0.5
            elif event.key==pygame.K_LEFT:  #松开按键，飞机停止
                playerStep=-0.5

            elif event.key==pygame.K_SPACE:
                print('发射子弹....')
                bullet_num+=1
                #创建一颗子弹
                b=Bullet()
                bullets.append(b)

        if event.type==pygame.KEYUP:
            playerStep=0


    screen.blit(playerImg,(playerX,playerY))    #绘制飞机

    move_player()
    show_enemy()
    show_bullets()
    check_isOver()   #显示游戏结束

    pygame.display.update()  #需要更新出所画上的东西


