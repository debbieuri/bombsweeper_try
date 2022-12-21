import pyautogui as pp
#pp.PAUSE=0.001
class solver:
    def __init__(self):
        z=pp.screenshot()
        a=pp.locateOnScreen('assets_solver/blank.png',confidence=0.9)#empty game only 
        if a==None:
            notfound
        self.ss=30#a.width
        self.s=[a.left,a.top]
        self.size=[0,0]
        g=self.s.copy()
        while pp.onScreen(g[0]+self.ss,g[1]+self.ss):
            a=pp.locateOnScreen('assets_solver/blank.png',confidence=0.9,region=(g[0],g[1],self.ss,self.ss))
            if a==None:
                break
            self.size[0]+=1
            g[0]+=self.ss
        g=self.s.copy()
        while pp.onScreen(g[0]+self.ss,g[1]+self.ss):
            a=pp.locateOnScreen('assets_solver/blank.png',confidence=0.9,region=(g[0],g[1],self.ss,self.ss))
            if a==None:
                break
            self.size[1]+=1
            g[1]+=self.ss
        pp.moveTo(self.s)
        print(self.ss,self.size)
        self.ways = [[0,-1],[1,-1],[1,0],[1,1],[0,1],[-1,1],[-1,0],[-1,-1]]

    def get(self,x,y):
        if pp.locateOnScreen('assets_solver/blank.png',confidence=0.8,region=(self.s[0]+x*self.ss,self.s[1]+y*self.ss,self.ss,self.ss))!=None:
            #print('blank')
            return 0
        if pp.locateOnScreen('assets_solver/n0.png',confidence=0.8,region=(self.s[0]+x*self.ss,self.s[1]+y*self.ss,self.ss,self.ss))!=None:
            #print('0')
            return 9
        for i in range(1,9):
            if pp.locateOnScreen('assets_solver/n'+str(i)+'.png',confidence=0.8,region=(self.s[0]+x*self.ss,self.s[1]+y*self.ss,self.ss,self.ss))!=None:
                #print(i)
                return i
        print('noooooooooo :(',x,y)

    def getall(self,x,y):
        self.g[x][y]=self.get(x,y)
        if self.g[x][y]==9:
            for w in self.ways:
                if x+w[0]>=0 and x+w[0]<self.size[0]:
                    if y+w[1]>=0 and y+w[1]<self.size[1]:
                        if self.g[x+w[0]][y+w[1]]==0:
                            self.getall(x+w[0],y+w[1])         

    def check_d(self,g):
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                if g[x][y]>0 and g[x][y]!=9:#0...
                    b=0
                    e=[]
                    for way in self.ways:
                        if x+way[0]>=0 and x+way[0]<self.size[0]:
                            if y+way[1]>=0 and y+way[1]<self.size[1]:
                                if g[x+way[0]][y+way[1]]==-1 or g[x+way[0]][y+way[1]]==-3:
                                    b+=1
                                elif g[x+way[0]][y+way[1]]==0:
                                    e.append(way)
                    if e!=[]:
                        if b==g[x][y]:
                            return [False,x,y,e]
                        elif g[x][y]-b==len(e):
                            return [True,x,y,e]
        return False

    def solve(self):
        self.g=[[0 for y in range(self.size[1])]for x in range(self.size[0])]
        while True:
            a=self.check_d(self.g)
            if a!=False:
                if a[0]:
                    for w in a[3]:
                        pp.moveTo((self.s[0]+(a[1]+w[0])*self.ss+self.ss//2,self.s[1]+(a[2]+w[1])*self.ss+self.ss//2))
                        pp.click(button='right')
                        self.g[a[1]+w[0]][a[2]+w[1]]=-1
                else:
                    for w in a[3]:
                        pp.moveTo((self.s[0]+(a[1]+w[0])*self.ss+self.ss//2,self.s[1]+(a[2]+w[1])*self.ss+self.ss//2))
                        pp.click()
                        self.getall(a[1]+w[0],a[2]+w[1])
                continue

            if self.check_u():
                continue
            
            if self.desperate_measure()==False:
                return

    def check_u(self):#just needs to call itself once and then it should be good enough!
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                if self.g[x][y]>0 and self.g[x][y]!=9:
                    b=0
                    e=[]
                    for way in self.ways:
                        if x+way[0]>=0 and x+way[0]<self.size[0]:
                            if y+way[1]>=0 and y+way[1]<self.size[1]:
                                if self.g[x+way[0]][y+way[1]]==-1:
                                    b+=1
                                elif self.g[x+way[0]][y+way[1]]==0:
                                    e.append(way)
                    if e!=[]:
                        if self.g[x][y]-b==len(e)-1:#all but 1 are bombs
                            ggg=[]
                            for w in e:
                                gg=[[y for y in x]for x in self.g]#unless .copy() is faster
                                gg[x+w[0]][y+w[1]]=-3#-1
                                while True:
                                    a=self.check_d(gg)
                                    if a==False:
                                        break
                                    if a[0]:
                                        for ww in a[3]:
                                            gg[a[1]+ww[0]][a[2]+ww[1]]=-3
                                    else:
                                        for ww in a[3]:
                                            gg[a[1]+ww[0]][a[2]+ww[1]]=-2
                                ggg.append([[y for y in x]for x in gg])
                            for xx in range(self.size[0]):
                                for yy in range(self.size[1]):
                                    for i in range(len(ggg)):
                                        if ggg[i][xx][yy]!=-2:
                                            break
                                    else:
                                        pp.moveTo((self.s[0]+xx*self.ss+self.ss//2,self.s[1]+yy*self.ss+self.ss//2))
                                        pp.click()
                                        self.getall(xx,yy)
                                        return True
                            for xx in range(self.size[0]):
                                for yy in range(self.size[1]):
                                    for i in range(len(ggg)):
                                        if ggg[i][xx][yy]!=-3:
                                            break
                                    else:
                                        pp.moveTo((self.s[0]+xx*self.ss+self.ss//2,self.s[1]+yy*self.ss+self.ss//2))
                                        pp.click(button='right')
                                        self.g[xx][yy]=-1
                                        return True
        return False
                            
            

    def desperate_measure(self):
        print('DESPERATE TIMES')
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                if self.g[x][y]==0:
                    pp.moveTo((self.s[0]+x*self.ss+self.ss//2,self.s[1]+y*self.ss+self.ss//2))
                    pp.click()
                    self.getall(x,y)
                    if self.g[x][y]==None:
                        print('epic fail!!!')
                        return False
                    if self.g[x][y]<=0:
                        print('epic fail!!!')
                        return False
                    return True
        print('solved?')
        return False

S=solver()
S.solve()
