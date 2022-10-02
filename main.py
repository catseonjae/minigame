import pygame
import sys
import random
import time
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


pygame.init()
pygame.display.set_caption("Component")

class Component:
    def __init__(self, block_size=32,block=[BLACK,RED,GREEN,BLUE,WHITE],x_size=10,y_size=20):

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        block_size=32
        
        self.x_size=x_size
        self.y_size=y_size
        
        self.block = block
        self.block_size=block_size
        self.board=[[0 for j in range(x_size)] for i in range(y_size)]
        self.score=0

        self.event_queue=[]

        self.start=[SCREEN_WIDTH/2-self.block_size*5,SCREEN_HEIGHT/2-self.block_size*10]
        self.end=[SCREEN_WIDTH/2+self.block_size*5,SCREEN_HEIGHT/2+self.block_size*10]
        self.dy=[0,-1,0,1]
        self.dx=[1,0,-1,0]

        self.clicked=[-1,-1]
        self.white_cnt=0
        for i in self.board:
            for j in self.board:
                if j==len(self.block)-1:
                    self.white_cnt+=1
        self.started_time=time.time()
        self.finished_time=0
        self.generate()

    def cheat(self):
        for i in range(self.y_size):
            for j in range(self.x_size):
                self.board[i][j]=len(self.block)-1
        self.white_cnt=self.x_size*self.y_size
    def push(self):
        for i in range(10):
            up=19
            for j in range(20):
                y=19-j
                while up>=0 and self.board[up][i]==0:
                    up-=1
                if up<0:
                    self.board[y][i]=0
                else:
                    self.board[y][i]=self.board[up][i]
                up-=1
        self.generate()

    def distribute(self,size):
        ret=[]
        while size>0:
            if size<=2:
                ret.append(size)
                break
            t=random.randint(3,min(size,4))
            ret.append(t)
            size-=t
        return ret

    def generate(self):
        component=[]
        q=[]
        for i in range(10):
            if self.board[0][i]==0:
                q.append([i,0])
        while q!=[]:
            now=q[0]
            del q[0]
            if now in component:
                continue
            component.append(now)
            for i in range(4):
                x=now[0]+self.dx[i]
                y=now[1]+self.dy[i]
                if [x,y] in component:
                    continue
                if x<0 or x>=10 or y<0 or y>=20:
                    continue
                if self.board[y][x]!=0:
                    continue
                q.append([x,y])
        distribution=self.distribute(len(component))
        idx=0
        for i in distribution:
            c=random.randint(1,len(self.block)-1)
            if c==len(self.block)-1:
                self.white_cnt+=i
            for j in range(i):
                now=component[idx]
                self.board[now[1]][now[0]]=c
                idx+=1
    def remove(self):
        component=[]
        q=[self.clicked]
        color=self.board[self.clicked[1]][self.clicked[0]]
        if color==len(self.block)-1:
            return
        while q!=[]:
            now=q[0]
            del q[0]
            if now in component:
                continue
            component.append(now)
            for i in range(4):
                x=now[0]+self.dx[i]
                y=now[1]+self.dy[i]
                if [x,y] in component:
                    continue
                if x<0 or x>=10 or y<0 or y>=20:
                    continue
                if self.board[y][x]!=color:
                    continue
                q.append([x,y])
        self.score+=len(component)**2
        for x,y in component:
            self.board[y][x]=0
        self.push()

    def press(self):
        if self.done():
            return
        pos = pygame.mouse.get_pos()
        if pos[0]<self.start[0] or pos[1]<self.start[1]:
            return
        if pos[0]>self.end[0] or pos[1]>self.end[1]:
            return
        pos=[pos[i]-self.start[i] for i in range(2)]
        pos=[int(pos[i]//self.block_size) for i in range(2)]
        self.clicked=pos
        self.remove()
    def min(a, b):
        if a<b:
            return a
        return b
    def loop(self):
        import time
        t=time.time()
        done=[]
        for i in range(len(self.event_queue)):
            if self.event_queue[i][0]<=t:
                self.event_queue[i][1]()
                done.append(i)
        done.reverse()
        for i in done:
            del self.event_queue[i]
        self.display()


    def display(self):
        self.screen.fill(BLACK)
        for i in range(20):
            for j in range(10):
                color=self.block[self.board[i][j]]
                pygame.draw.rect(self.screen, color, (self.start[0]+self.block_size*j,self.start[1]+self.block_size*i,self.block_size,self.block_size))
        pygame.display.update()

    def display_end(self):
        self.screen.fill(BLACK)
        for i in range(20):
            for j in range(10):
                color=self.block[self.board[i][j]]
                pygame.draw.rect(self.screen, color, (self.start[0]+self.block_size*j,self.start[1]+self.block_size*i,self.block_size,self.block_size))
        font = pygame.font.SysFont("notosanscjkkr",30)
        text = font.render(f"finished at {round(self.finished_time-self.started_time,3)} ",True,BLACK)
        r=text.get_rect()
        r.centerx=SCREEN_WIDTH/2
        r.centery=SCREEN_HEIGHT/2
        self.screen.blit(text,r) 
        pygame.display.update()
    def done(self):
        return self.white_cnt==self.x_size*self.y_size
game=Component()
clock = pygame.time.Clock()
while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type==pygame.MOUSEBUTTONDOWN:
            game.press()
    if game.finished_time!=0:
        game.display_end()
    elif game.done():
        game.finished_time=time.time()
        game.display_end()
    else:
        game.loop()
