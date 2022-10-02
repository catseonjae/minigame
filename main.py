import pygame
import sys
import random
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 720

BLACK=(0,0,0)
WHITE=(255,255,255)
RED=(255,0,0)
ORANGE=(255,50,0)
YELLOW=(255,255,0)
GREEN=(0,255,0)
BLUE=(0,0,255)
INDIGO=(0,5,255)
PURPLE=(100,0,255)

block = [BLACK,RED,GREEN,BLUE,YELLOW]

pygame.init()
pygame.display.set_caption("Component")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))



block_size=32
board=[[random.randint(1,4) for j in range(10)] for i in range(20)]
start=[SCREEN_WIDTH/2-block_size*5,SCREEN_HEIGHT/2-block_size*10]
end=[SCREEN_WIDTH/2+block_size*5,SCREEN_HEIGHT/2+block_size*10]
hold=[-1,-1]
score=0

def down():
    global board
    for i in range(10):
        up=19
        b=0
        for j in range(20):
            y=19-j
            while up>=0 and board[up][i]==0:
                up-=1
            if up<0:
                board[y][i]=0
            else:
                board[y][i]=board[up][i]
            up-=1

def distribute(size):
    ret=[]
    while size>0:
        if size<=2:
            ret.append(size)
            break
        t=random.randint(2,min(5,size))
        ret.append(t)
        size-=t
    return ret
def generate():
    component=[]
    q=[]
    for i in range(10):
        if board[0][i]==0:
            q.append([i,0])
    while q!=[]:
        now=q[0]
        del q[0]
        if now in component:
            continue
        component.append(now)
        for i in range(4):
            x=now[0]+dx[i]
            y=now[1]+dy[i]
            if [x,y] in component:
                continue
            if x<0 or x>=10 or y<0 or y>=20:
                continue
            if board[y][x]!=0:
                continue
            q.append([x,y])
    distribution=distribute(len(component))
    idx=0
    for i in distribution:
        c=random.randint(1,4)
        for j in range(i):
            now=component[idx]
            board[now[1]][now[0]]=c
            idx+=1
dy=[0,-1,0,1]
dx=[1,0,-1,0]
def remove(a,b,c):
    component=[]
    q=[a,b]
    while q!=[]:
        now=q[0]
        del q[0]
        if now in component:
            continue
        component.append(now)
        for i in range(4):
            x=now[0]+dx[i]
            y=now[1]+dy[i]
            if [x,y] in component:
                continue
            if x<0 or x>=10 or y<0 or y>=20:
                continue
            if board[y][x]!=c:
                continue
            q.append([x,y])
    if len(component)<7:
        return
    global score
    score+=len(component)**2
    for x,y in component:
        board[y][x]=0
    display()
    import time
    time.sleep(0.5)
    down()
    generate()
    global hold
    hold=[-1,-1]


def press():
    global hold
    pos = pygame.mouse.get_pos()
    if pos[0]<start[0] or pos[1]<start[1]:
        return
    if pos[0]>end[0] or pos[1]>end[1]:
        return
    pos=[pos[i]-start[i] for i in range(2)]
    pos=[int(pos[i]//block_size) for i in range(2)]
    if hold==[-1,-1]:
        hold=pos
    elif pos==hold:
        hold=[-1,-1]
    else:
        if board[hold[1]][hold[0]]!=board[pos[1]][pos[0]]:
            return
        remove(pos,hold,board[hold[1]][hold[0]])
def min(a, b):
    if a<b:
        return a
    return b
def dark(color):
    return (min(255,(color[i])*0.5) for i in range(3))



clock = pygame.time.Clock()
def display():
    screen.fill(BLACK)
    for i in range(20):
        for j in range(10):
            color=block[board[i][j]]
            if i<5:
                color=(min(255,(color[0])*0.5),min(255,(color[1])*0.5),min(255,(color[2])*0.5))
            pygame.draw.rect(screen, color, (start[0]+block_size*j,start[1]+block_size*i,block_size,block_size))
    if hold != [-1,-1]:
        i=hold[1]
        j=hold[0]
        pygame.draw.rect(screen, WHITE,(start[0]+block_size*j,start[1]+block_size*i,block_size,block_size),5)
    pygame.display.update()
while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type==pygame.MOUSEBUTTONDOWN:
            press()
    display()
    # print(score)
