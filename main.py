import pygame
from pygame.locals import *
import sys

class Bullet:
    def __init__(self,id,screen):
        self.id=id
        self.speed=SPEED+1
        self.direction=[0,0]
        self.pos=[GAME_WIDTH+1,GAME_HEIGHT+1]
        self.screen=screen
        if(self.id==1):
            self.colour=PLAYER1_COLOUR
            self.direction[0]=1
        if(self.id==2):
            self.colour=PLAYER2_COLOUR
            self.direction[0]=-1

    def render(self):
        if(self.id==1):
            offset=-10
        else:
            offset=10
        pygame.draw.line(self.screen,self.colour,(self.pos[0],self.pos[1]),(self.pos[0]+offset,self.pos[1]))

    def update(self):
        self.pos[0]+=self.speed*self.direction[0]
        self.pos[1]+=self.speed*self.direction[1]

class Player:
    def __init__(self,screen,colour,id,speed):
        self.colour=colour
        self.screen=screen
        self.id=id
        self.speed=speed
        self.bullet=Bullet(self.id,self.screen)
        if(self.id==1):
            self.pos=[GAME_WIDTH/4,GAME_HEIGHT/2]
        if(self.id==2):
            self.pos=[GAME_WIDTH*(3/4),GAME_HEIGHT/2]
        self.direction=[0,0]
        self.BULLETFIRED=False
        self.hp=1

    def render(self):
        pygame.draw.rect(self.screen,self.colour,[self.pos[0],self.pos[1],PLAYER_WIDTH,PLAYER_WIDTH])
        if(self.BULLETFIRED):
            self.bullet.render()
        #self.direction[0]=0
        #self.direction[1]=0

    def update(self):
        self.pos[0]+=self.speed*self.direction[0]
        self.pos[1]+=self.speed*self.direction[1]

        if(self.id==1):
            if(self.pos[0]<=0):
                self.pos[0]=0
            if(self.pos[0]>=GAME_WIDTH/2-PLAYER_WIDTH):
                self.pos[0]=GAME_WIDTH/2-PLAYER_WIDTH
            if(self.pos[1]<=0):
                self.pos[1]=0
            if(self.pos[1]>=GAME_HEIGHT-PLAYER_WIDTH):
                self.pos[1]=GAME_HEIGHT-PLAYER_WIDTH

        if (self.id==2):
            if(self.pos[0]<=GAME_WIDTH/2):
                self.pos[0]=GAME_WIDTH/2
            if(self.pos[0]>=GAME_WIDTH-PLAYER_WIDTH):
                self.pos[0]=GAME_WIDTH-PLAYER_WIDTH
            if(self.pos[1]<=0):
                self.pos[1]=0
            if(self.pos[1]>=GAME_HEIGHT-PLAYER_WIDTH):
                self.pos[1]=GAME_HEIGHT-PLAYER_WIDTH

        if(self.BULLETFIRED):
            self.bullet.update()
            if(self.bullet.pos[0]<0 or self.bullet.pos[0]>GAME_WIDTH or self.bullet.pos[1]<0 or self.bullet.pos[1]>GAME_HEIGHT):
                self.BULLETFIRED=False

    def fire_bullet(self):
        if(self.BULLETFIRED==False):
            self.bullet.pos[0]=self.pos[0]#+PLAYER_WIDTH
            self.bullet.pos[1]=self.pos[1]#+PLAYER_WIDTH/2
            self.bullet.direction[1]=self.direction[1]
            self.BULLETFIRED=True

class Game:
    def __init__(self,GAME_WIDTH,GAME_HEIGHT):
        self.screen=pygame.display.set_mode((GAME_WIDTH,GAME_HEIGHT))
        self.clock=pygame.time.Clock()
        self.p1=Player(self.screen,PLAYER1_COLOUR,1,SPEED)
        self.p2=Player(self.screen,PLAYER2_COLOUR,2,SPEED)
        self.GAME_OVER_FLAG=False
        self.font=pygame.font.SysFont("Consolas",20)

    def render(self):
        self.screen.fill(BACKGROUND_COLOUR)
        pygame.draw.line(self.screen,SEPERATION_COLOUR,(GAME_WIDTH/2,0),(GAME_WIDTH/2,GAME_HEIGHT))
        self.display_scores()
        self.p1.render()
        self.p2.render()
        pygame.display.flip()

    def get_input(self):
        for event in pygame.event.get():
            if(event.type==pygame.QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE)):
                pygame.quit()
                sys.exit()
            elif(event.type==KEYDOWN and self.GAME_OVER_FLAG==False):
                if(event.key==K_w):
                    self.p1.direction[1]=-1
                    self.p1.direction[0]=0
                elif(event.key==K_a):
                    self.p1.direction[0]=-1
                    self.p1.direction[1]=0
                elif(event.key==K_s):
                    self.p1.direction[1]=1
                    self.p1.direction[0]=0
                elif(event.key==K_d):
                    self.p1.direction[0]=1
                    self.p1.direction[1]=0
                elif(event.key==K_y):
                    self.p1.direction[0]=0
                    self.p1.direction[1]=0
                elif(event.key==K_t):
                    self.p1.fire_bullet()
                elif(event.key==K_UP):
                    self.p2.direction[1]=-1
                    self.p2.direction[0]=0
                elif(event.key==K_LEFT):
                    self.p2.direction[0]=-1
                    self.p2.direction[1]=0
                elif(event.key==K_DOWN):
                    self.p2.direction[1]=1
                    self.p2.direction[0]=0
                elif(event.key==K_RIGHT):
                    self.p2.direction[0]=1
                    self.p2.direction[1]=0
                elif(event.key==K_KP5):
                    self.p2.direction[0]=0
                    self.p2.direction[1]=0
                elif(event.key==K_KP4):
                    self.p2.fire_bullet()

    def update(self):
        if (self.p1.bullet.pos[0]>=self.p2.pos[0] and self.p1.bullet.pos[0]<=self.p2.pos[0]+PLAYER_WIDTH and self.p1.bullet.pos[1]>=self.p2.pos[1] and self.p1.bullet.pos[1]<=self.p2.pos[1]+PLAYER_WIDTH):
            self.p2.hp-=1
            self.p1.bullet.pos[0]=GAME_WIDTH+1
            self.p1.bullet.pos[1]=GAME_HEIGHT+1
            self.p1.BULLETFIRED=False
        if (self.p2.bullet.pos[0]>=self.p1.pos[0] and self.p2.bullet.pos[0]<=self.p1.pos[0]+PLAYER_WIDTH and self.p2.bullet.pos[1]>=self.p1.pos[1] and self.p2.bullet.pos[1]<=self.p1.pos[1]+PLAYER_WIDTH):
            self.p1.hp-=1
            self.p2.bullet.pos[0]=GAME_WIDTH+1
            self.p2.bullet.pos[1]=GAME_HEIGHT+1
            self.p2.BULLETFIRED=False

        self.p1.update()
        self.p2.update()

    def display_scores(self):
        s1=self.font.render("HP:"+str(self.p1.hp),1,(100,0,0))
        self.screen.blit(s1,(10,10))
        s2=self.font.render("HP:"+str(self.p2.hp),1,(0,100,0))
        self.screen.blit(s2,(GAME_WIDTH-10-5*10-15,10))


    def game_over_check(self):
        if(self.p1.hp==0):
            self.GAME_OVER_FLAG=True
            print("GAME OVER!! PLAYER 2 WINS!!")
        elif(self.p2.hp==0):
            self.GAME_OVER_FLAG=True
            print("GAME OVER!! PLAYER 1 WINS!!")

        if(self.GAME_OVER_FLAG==True):
            self.font=pygame.font.SysFont("Consolas",50)
            while 1:
                self.clock.tick(FRAMES_PER_SECOND)
                self.get_input()
                self.screen.fill((255,0,0))
                if(self.p1.hp==0):
                    f=self.font.render("GAME OVER!! PLAYER 2 WINS!!",1,(0,200,0))
                else:
                    f=self.font.render("GAME OVER!! PLAYER 1 WINS!!",1,(200,0,0))
                self.screen.blit(f,(0,0))#(GAME_WIDTH/2-100,GAME_HEIGHT/2))



BACKGROUND_COLOUR=(0,0,0)
SEPERATION_COLOUR=(255,255,255)
GAME_WIDTH=800
GAME_HEIGHT=800
PLAYER_WIDTH=10
PLAYER1_COLOUR=(255,0,0)
PLAYER2_COLOUR=(0,255,0)
SPEED=5
FRAMES_PER_SECOND=60

pygame.init()
game=Game(GAME_WIDTH,GAME_HEIGHT)


while 1:
    game.clock.tick(FRAMES_PER_SECOND)
    game.get_input()
    game.update()
    game.render()
    game.game_over_check()
