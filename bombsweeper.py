import random
import pygame
pygame.init()

def show_text(font,display,msg,x,y):
    text = font.render(msg,False,(255,0,0))
    display.blit(text,(x,y))

class GAME:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.imgs = [pygame.image.load('assets/blank.png'),
                     pygame.image.load('assets/highlight.png'),
                     pygame.image.load('assets/flag.png'),
                     pygame.image.load('assets/clicked.png'),
                     pygame.image.load('assets/question.png'),]
        self.nimgs = [pygame.image.load('assets/n'+str(i)+'.png') for i in range(9)]
        self.imgs[1].set_alpha(100)

    def sizeit(self):
        self.sizer = 30#40 if len(self.game2)<21 else 30#min([700//len(self.game2),700//len(self.game2[0])])
        gamesize = [self.sizer*len(self.game2[0]),self.sizer*len(self.game2)]
        self.display = pygame.display.set_mode(gamesize)
        pygame.display.set_caption('bombsweeper')
        for i in range(len(self.imgs)):
            self.imgs[i] = pygame.transform.scale(self.imgs[i],(self.sizer,self.sizer))
        for i in range(len(self.nimgs)):
            self.nimgs[i] = pygame.transform.scale(self.nimgs[i],(self.sizer,self.sizer))
        
    def displays(self):
        pos = pygame.mouse.get_pos()
        pos = [pos[0]//self.sizer,pos[1]//self.sizer]
        for x in range(len(self.game2[0])):
            for y in range(len(self.game2)):
                if self.game2[y][x] == 0:#
                    self.display.blit(self.imgs[0],(x*self.sizer,y*self.sizer))
                elif self.game2[y][x] == 1:
                    self.display.blit(self.imgs[2],(x*self.sizer,y*self.sizer))
                if [x,y]==pos:
                    self.display.blit(self.imgs[1],(x*self.sizer,y*self.sizer))
                if self.game2[y][x] == 3:
                    self.display.blit(self.nimgs[self.game[y][x]],(x*self.sizer,y*self.sizer))
        pygame.display.update()

    def make(self,size,bombs,pos):
        game = [[0 for x in range(size[0])] for y in range(size[1])]
        places = [[a,b] for a in range(size[0]) for b in range(size[1])]
        no = [[a,b] for a in range(pos[1]-1,pos[1]+2) for b in range(pos[0]-1,pos[0]+2)]
        for x in range(len(no)):
            if no[x] in places:
                places.remove(no[x])
        for z in range(bombs):
            x = random.randint(0,len(places)-1)
            game[places[x][1]][places[x][0]] = -1
            places.pop(x)
        for x in range(len(game[0])):
            for y in range(len(game)):
                if game[y][x] == 0:
                    n = 0
                    for a in range(-1,2):
                        for b in range(-1,2):
                            if x+a>-1 and a+x<len(game[0]) and b+y>-1 and b+y<len(game):
                                if game[y+b][x+a]==-1:
                                    n+=1
                    game[y][x] = n
        return game

    def start(self):#...
        #self.play(25,25,140)
        self.play(20,20,90)
        while True:##
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    return
            self.clock.tick(60)

    def flow(self,pos):
        for x in range(-1,2):
            for y in range(-1,2):
                if x+pos[0]>-1 and pos[0]+x<len(self.game[0]) and y+pos[1]>-1 and y+pos[1]<len(self.game):
                    a = False
                    if self.game2[y+pos[1]][x+pos[0]] != 3:
                        a = True
                    self.game2[y+pos[1]][x+pos[0]] = 3
                    if not(x==0 and y ==0):
                        if self.game[y+pos[1]][x+pos[0]] == 0:
                            if a:
                                self.flow([x+pos[0],y+pos[1]])

    def explode(self):
        self.booms = [pygame.transform.scale(pygame.image.load('assets/boom1.png'),(self.sizer,self.sizer)),
                      pygame.transform.scale(pygame.image.load('assets/boom2.png'),(self.sizer,self.sizer)),
                      pygame.transform.scale(pygame.image.load('assets/boom.png'),(self.sizer,self.sizer))]
        for i in range(len(self.booms)):
            pygame.time.delay(200)
            for x in range(len(self.game[0])):
                for y in range(len(self.game)):
                    if self.game[y][x] == -1 and self.game2[y][x] != 1:#flag
                        self.display.blit(self.booms[i],(x*self.sizer,y*self.sizer))
                        pygame.display.update()
                        pygame.event.pump()

    def play(self,x,y,bombs):
        self.game = False
        self.game2 = [[0 for r in range(x)] for e in range(y)]
        self.sizeit()
        while True:
            self.displays()
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif e.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    pos = [pos[0]//self.sizer,pos[1]//self.sizer]
                    if e.button == 1:
                        if self.game == False:
                            self.game = self.make([x,y],bombs,[pos[1],pos[0]])
                        if self.game2[pos[1]][pos[0]] == 0:
                            if self.game[pos[1]][pos[0]] == -1:
                                self.explode()
                                return
                            elif self.game[pos[1]][pos[0]] == 0:
                                self.flow(pos)
                            self.game2[pos[1]][pos[0]] = 3
                    elif e.button == 3:
                        if self.game2[pos[1]][pos[0]] == 0:
                            self.game2[pos[1]][pos[0]] = 1
                        elif self.game2[pos[1]][pos[0]] == 1:
                            self.game2[pos[1]][pos[0]] = 0
            self.clock.tick(60)
        
gamer = GAME()
gamer.start()
