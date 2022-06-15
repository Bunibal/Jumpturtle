
# -*- coding: cp1252 -*-
#Sebastian Bittner, Stephan Buchner
#Letzte Änderung : 18.03.2020

import pygame, sys, random, math, time, os
#allgemeiner shit
FPS = 70
GRAVITATION = 600
GEHV = 500.0
SPRUNGCAP = 800
F_VSCHUSS = 2
groesse = breite, hoehe = 1536,825
HOEHEBODEN = int(0.9*hoehe)
#Nüsse
MINNUTS = 0.4
NUSSGESCHWINDIGKEIT = 350
NUTSINSACK = 3
#baum
WALNUSSBAMLUCK = 2
DEFMAXBAMOIDA = 2
NUESSEWALNUTTREE = 3
NUSSERTNECOOLDOWN = 10
#items
ITEMSBRIEFTAUBE = 1
ITEMV = 200
SHRINKINGDURATION = 20
GUNDURATION = 4
GUNINTERVAL = 0.2
SHIELDDURATION = 2
#Feinde
V_WILDSCHWEIN = 600
STARTBOAR = 3
#Bosse
V_MENSCH = 200
ABSTANDM_RAND = 200
BOTTLEVY = -300
MINBOTTLES = 4
MINNUTSM = 1.5



os.chdir(os.getcwd() + "/resources")
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,0)
pygame.init()

screen = pygame.display.set_mode(groesse)

background = pygame.image.load ("backgroundbeach.png").convert()
background = pygame.transform.scale(background, (groesse))

pygame.mixer.init()
music = ['jumpymuggefeatsb.mp3','jumpymuggefeatsb2.mp3',
         'jumpymuggefeatsb3.mp3', "blue_monday_bossa.mp3", "oceanwaves.mp3",
         "Unity.mp3", "duck.mp3", "moonshine.mp3"]
pygame.mixer.music.load(random.choice(music))

#globale variablen


#soundeffekte laden
bitch = pygame.mixer.Sound("Gotcha Bitch.wav")
gameover = pygame.mixer.Sound("Mario Game Over.wav")
nope = pygame.mixer.Sound("Nope.wav")
explosion = pygame.mixer.Sound("Roblox Rocket Explosion.wav")
sad = pygame.mixer.Sound("Sad Trombone.wav")
seagull = pygame.mixer.Sound("seagull chirping.wav")
weed = pygame.mixer.Sound("Smoke Weed Everyday.wav")
continued = pygame.mixer.Sound("to be continued.wav")
win = pygame.mixer.Sound("WIN A BATTLE POKEMON.wav")
howl = pygame.mixer.Sound("Wolf Howl.wav")
boar = pygame.mixer.Sound("wildboar.wav")


keymemory = [False,False]
TRANSPARENCY= (13,66,23)
menu = False
levelmenus = False

pygame.display.flip()
##Achtung umgekehrt!!!!!!!!!!
##["M","M","M","M","M","M","M","M","M","M","M","M","M","M","M","M","M","M","M","M","M","M","M",
##                        "M","M","M","M","M","M","M","M","M","M","M","M","FP","FP","FP","FP","FP","FP","FP","FP","FP","FP","FP","FP","FP","FP","FP","FP","FP",
##                        "M","M","M","M","M","M", "M","M","M","M","M","BT","BT","BT","BT","BT","BT","BT","BT","BT","BT","BT","BT",
##                        "M","M","M","M","M","M","M","M","M","M","M","M","M","M","M","M","M","M","M","M","M","M","M","M",
##                        "M","M","M","M","M","M","M","M","M","M","M","M","M","M"],
##                    ["M","M","F","M","M","F", "M", "M",],
##                    ["M", "FP","BT", "M","F","M","M","M","F","FP","M"],
##                    ["M","FP","F","M","FP","W","M","M", "BT","F","M","M"],
##                    ["M","F","M","M","W","FP","W","M","BT","M","F","M"],
##                    ["FP","FP","W","F","FP","BT","M","W","FP","M","F","M","W","F","M","FP","BT"],
##                    ["M","M","M","M","M","M","M","M","M","M","M","M","M","M","M","M","M","M","M","M","M","M","M","M","M",]
##


class LevelInfo:
    def __init__(self, name, lvlnr, objekte_norm, objekte_speziell = [], zeit = 60, verteilung = None, items = ["S", "M", "MG"], nuesse = 0, maxbaeume = DEFMAXBAMOIDA):
        if verteilung == None:
            verteilung = lambda i : i/len(objekte_norm)
        self.startzeiten = []
        for i in range(len(objekte_norm)):
            frueheste = int(zeit * verteilung(i))
            spaeteste = int(zeit * verteilung(i + 1))
            self.startzeiten.append((objekte_norm[i],
                random.randint(frueheste, spaeteste)))                           
        for ob in objekte_speziell:
            self.startzeiten.append((ob[0], random.randint(ob[1], ob[2])))
        self.zeit = zeit
        self.name = name
        self.lvlnr = lvlnr
        self.nuesse = nuesse*NUTSINSACK
        self.items = items
        self.maxbamoida = maxbaeume

def makePartitionLevel(name, lvlnr, objekte, objekte_speziell = [], zeit = 120, items = ["S", "M", "MG"], nuesse = 0, maxbaeume = DEFMAXBAMOIDA):
    partLaenge = [len(sublevel) for sublevel in objekte]
    zeitProPart = 1/len(objekte)
    gesObj = []
    for part in objekte:
        gesObj = gesObj + part
        
    def vert(i):
        start = 0
        for lng in partLaenge:
            if i<lng:
                return start + zeitProPart * i/lng
            start += zeitProPart
            i -= lng
        return 1
            
    level = LevelInfo(name, lvlnr, gesObj, objekte_speziell, zeit, vert, items, nuesse, maxbaeume)
    return level
    
lvlmenu = LevelInfo("menu", -1, ["M"], zeit = 40000000)
tutorial = LevelInfo("Tutorial", 0, ["M","F"], zeit = 30)
lvl1 = LevelInfo("for noobs <3", 1, ["M","M","M","M","M","M", "F", "M","M","M","M","M","M","F","M","M","M","M","M"])
lvl2 = LevelInfo("goodluck!", 2, ["F","M","M","M","F","M", "M","M", "M","M", "M","M", "M", "W","M", "M","M", "M","M", "M","M", "M","F","M", "M","M", "M"])
lvl3 = LevelInfo("some MOEWE", 3, ["M","M","M","M","M","M","M","M","M","M","M","M","M","M","M","M","M","M","M","M","M","M","M","M","M","M","M","M","M","M","M","M",
                                   "M","M","M","M","M","M","M","M","M","M","M","M","M","M","M","M","M","M","M","M","M","M","M","M","M","M","M","M","M","M","M","M","M","M"])
lvl4 = LevelInfo("take care!", 4, ["FP","FP","FP","FP","FP","FP","BT", "FP","FP","FP","FP","FP","FP","FP","FP","FP","FP", "F", "BT"], nuesse = 3)
lvl5 = LevelInfo("ELI PASS AUF!", 5, ["W","F", "W", "M", "M", "BT", "M", "W", "M", "M", "BT", "M", "W", "M", "M", "BT", "M", "M", "M", "BT", "M"])
lvl6 = LevelInfo("Brieftaube", 6, ["W","W","W","W","W","W","W","W","BT","BT","BT","BT","BT","BT","BT","BT","BT","BT","BT","BT","BT","BT","BT","BT","BT","BT","BT","BT"], nuesse = 300)
lvl7 = makePartitionLevel("the classic", 7, [["FP","FP","W","F","FP","BT","M","W","FP","M","F","M","W","F","M","FP","BT"],
                          ["M","F","M","M","W","FP","W","M","BT","M","F","M"], ["M", "FP","BT", "M","F","M","M","M","F","FP","M"],
                          ["M","M","F","M","M","F", "M", "M"]], zeit = 150)
lvl8 = makePartitionLevel("99 penguins...",8,[["FP","FP","FP","FP","FP","FP","FP","FP","FP","FP","FP","FP","FP","FP","FP","FP","FP","FP","FP","FP","FP","FP","FP","FP","FP","FP"],
                                               ["BT", "M", "M","F", "M","BT", "M", "M","F", "M","BT", "M", "M","F", "M","BT", "M", "M","F", "M","BT", "M", "M","F", "M","BT", "M", "M","F"],
                                               ["BT", "W", "BT", "M","BT", "W", "BT", "M","BT", "W", "BT", "M","BT", "W", "BT", "M"],
                                               ["M","M","M","M","M","M","M","M","M","M","M","M","M"]] )
lvl9 = makePartitionLevel("Farmfest", 9, [["W","F","M", "W","F","M","W","F","FP","M","W","F","M", "W","F","M","W","F","M","W","FP","F","M", "W","F","M","W","F","M",
                                           "W","F","M", "W","F","M","W","F","M","FP","W","F","M", "W","F","M","W","F","M","W","FP","F","M", "W","F","M","W","F","M"],
                                          ["BT", "M", "BT", "BT", "M", "BT","BT", "M", "BT","BT", "M", "BT","BT", "M", "BT","BT", "M", "BT"]], nuesse = 10, maxbaeume = 4)
lvl10 = makePartitionLevel("Dunkler Wald", 10, [["F","W","F","F","W", "W","F","W","F","W","F","W","F","BT"],["F","M","F","W","F","F","M","F"],["F","BT","F","F","M"]], zeit = 90,
                          items = ["M"], nuesse = 10, maxbaeume = 0)
lvl11 = makePartitionLevel("about 99 foxes",11, [["F","F","F","F","F","F","F","F","F","F","F","F","BT","F","F","F","F","F","F","F","F","F","F","F","F","F","F","F","F","F","F","F","BT","F",
                                              "F","F","F","F","F","F","F","F","F","F","F","F","BT","F","F","F","F","F","F","F","F","F","F","F","F","F","F","F","F","F","F","F","BT","F"],
                           ["BT","BT","BT","BT","BT","BT","BT","BT"],
                           ["M", "M", "FP","M","M", "M", "FP","M","M", "M", "FP","M","M", "M", "FP","M","M", "M", "FP","M","M", "M", "FP","M","M", "M", "FP","M","M", "M", "FP","M"]],
                           zeit = 90, nuesse = 10)
lvl12 = makePartitionLevel("attack of human!", 12, [["ME"],["BT","W","WS","M","M","M", "M", "FP", "M", "M", "M","BT","W","WS","M","M","M", "M",
                                                            "FP", "M", "M", "M","BT","W","WS","M","M","M", "M", "FP", "M", "M", "M"]],
                                                    zeit = 80)
test = LevelInfo("Test", 13, ["ME"], verteilung = lambda i : 1, nuesse = 10)
lvllist= [tutorial, lvl1, lvl2, lvl3, lvl4, lvl5, lvl6, lvl7, lvl8, lvl9, lvl10, lvl11,lvl12, test]

#Gravitation berechnen
def berechneweg_g (v0, hoehe_ob):
    wegmitg = v0/FPS + GRAVITATION/(2*FPS**2)
    if  hoehe_ob + wegmitg <= HOEHEBODEN:
        return (wegmitg, False)
    else:
        return (HOEHEBODEN - hoehe_ob, True)

def abst(v1,v2):
    return (v2[0] - v1[0], v2[1] - v1[1])

def norm(v):
    return math.sqrt(v[0]**2 + v[1]**2)
    
#Alle Gegner im Spiel
class Moewe(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.richtung = random.choice([1, -1])
        self.image = pygame.image.load("moewe.bmp")
        self.image.set_colorkey(TRANSPARENCY)
        self.rect = self.image.get_rect()
        if self.richtung == 1:
            self.rect.right, self.rect.top = [0, int(hoehe*(random.randint(0,2)/10))]
            self.image = pygame.transform.flip(self.image, True, False)
        else:
            self.rect.left, self.rect.top = [breite, int(hoehe*(random.randint(0,2)/10))]     
        self.pos = self.rect.center
        self.vx = 450 * self.richtung
        self.nuesse = 4
        self.nutframes = 0
        self.desc = "Moewe"
        self.kollrip = True
        
    def bewegen(self):
        self.rect = self.rect.move(self.vx//FPS,0)
        self.nutframes +=1
        if abs(self.rect.centerx - turtle.rect.centerx) <= 600:
            if  (random.randint(1, FPS//6)==1 and
                self.nuesse >0) and self.nutframes/FPS >= MINNUTS:
                self.nuss_abwerfen()

    def nuss_abwerfen(self):
        nuss = Walnuss(self.rect.center, NUSSGESCHWINDIGKEIT * self.richtung, 10)
        spiel.akt_objekte.insert(0, nuss)
        spiel.gruppe_kollrip.add(nuss)
        self.nuesse -=1
        self.nutframes = 0
    def hit(self):
        spiel.gruppe_kollrip.remove(self)
        spiel.akt_objekte.remove(self)#
    def onCreate (self):
        seagull.play()
        
class Flyingpenguin(pygame.sprite.Sprite):
    def __init__ (self):
        pygame.sprite.Sprite.__init__(self)
        self.richtung = random.choice([1, -1])
        self.image = pygame.image.load("flyingpenguin.png")
        self.image.set_colorkey(TRANSPARENCY)
        self.rect = self.image.get_rect()
        if self.richtung == -1:
            self.rect.right, self.rect.top = [0, int(hoehe*(random.randint(0,2)/10))]
            self.image = pygame.transform.flip(self.image, True, False)
        else:
            self.rect.left, self.rect.top = [breite, int(hoehe*(random.randint(0,2)/10))]     
        self.pos = self.rect.center
        self.vx = 200 * -self.richtung
        self.vy = 0
        self.nuesse = 3
        self.nutframes = 0
        self.hp = 2
        self.desc = "Pinguin"
        self.kollrip = True

    def bewegen(self):
        wegy=[0]
        if self.hp <= 0:
            wegy = berechneweg_g(self.vy, self.rect.bottom)
            self.vy = self.vy + GRAVITATION/FPS
            if wegy[1]:
                self.vx = 0
        self.rect = self.rect.move(self.vx//FPS,wegy[0])
        self.nutframes +=1
        if abs(self.rect.centerx - turtle.rect.centerx) <= 400:
            if  (random.randint(1, FPS//6)==1 and
                self.nuesse >0) and self.nutframes/FPS >= MINNUTS/2:
                self.nuss_abwerfen()
    def nuss_abwerfen(self):
        if self.hp > 0:
            abst_zu_ttl = abst(self.rect.center,turtle.rect.center)
            absabst = max(1,norm(abst_zu_ttl)) #just to be sure
            nuss = Walnuss(self.rect.center,1000*abst_zu_ttl[0]/absabst, 1000*abst_zu_ttl[1]/absabst)
            spiel.akt_objekte.insert(0, nuss)
            spiel.gruppe_kollrip.add(nuss)
            self.nuesse -=1
            self.nutframes = 0
    def hit(self):
        self.hp -=1
        if self.hp <= 0:
            self.dying()
    def dying(self):
        spiel.gruppe_kollrip.remove(self)
        self.image = pygame.image.load("flyingpenguindead.png")
        self.image.set_colorkey(TRANSPARENCY)
        if self.richtung == -1:
            self.image = pygame.transform.flip(self.image, True, False)

class Fuchs(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        richtung = random.choice([-1,1])
        self.image = pygame.image.load("fuchs.bmp")
        self.image.set_colorkey(TRANSPARENCY)
        if richtung == -1:
            self.image = pygame.transform.flip(self.image, True, False)
        self.image = pygame.transform.scale(self.image, (150, 150))
        self.rect = self.image.get_rect()
        if richtung == 1:
            self.rect.right, self.rect.bottom = [0, HOEHEBODEN]
        else:
            self.rect.left, self.rect.bottom = [breite, HOEHEBODEN]
        self.geschw = [250//FPS * richtung, 0]
        self.hp = 2
        self.desc = "Fuchs"
        self.kollrip = True

    def bewegen(self):
        self.rect = self.rect.move(self.geschw)
    def hit(self):
        self.hp -=1
        if self.hp <= 0:
            spiel.gruppe_kollrip.remove(self)
            spiel.akt_objekte.remove(self)
        

class Wolf(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.richtung = random.choice([-1,1])
        self.image = pygame.image.load("wolf.bmp")
        pygame.transform.scale(self.image, (204,200))
        self.image.set_colorkey(TRANSPARENCY)
        if self.richtung == 1:
            self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect()
        if self.richtung == 1:
            self.rect.right, self.rect.bottom = [0, HOEHEBODEN]
        else:
            self.rect.left, self.rect.bottom = [breite, HOEHEBODEN]
        self.geschw = [250//FPS * self.richtung, 0]
        self.aktiv = True
        self.turncount = 2
        self.hp = 4
        self.desc = "Wolf"
        self.kollrip = True
        
    def bewegen(self):
        if self.aktiv:
            self.rect = self.rect.move(self.geschw)
            if random.randint(1,int(2.5*FPS)) == 1:
                self.aktiv = False
                self.passiv_zeit = random.randint(3,7)/10.0
            if random.randint(1,int(4*FPS)) == 1 and self.turncount > 0:
                self.turn(-self.richtung)
        else:
            self.passiv_zeit-=1.0/FPS
            if self.passiv_zeit<=0:
                self.aktiv = True
    def turn(self,richtung):
        if self.richtung != richtung:
             self.image = pygame.transform.flip(self.image, True, False)
        self.richtung = richtung
        self.turncount-=1
        self.geschw = [250//FPS * self.richtung, 0]
    def hit(self):
        self.hp -=1
        if self.hp <= 0:
            spiel.gruppe_kollrip.remove(self)
            spiel.akt_objekte.remove(self)
    def onCreate(self):
        howl.play()


class Wildschwein(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        richtung = random.choice([-1,1])
        self.image = pygame.image.load("wildschwein.bmp")
        self.image.set_colorkey(TRANSPARENCY)
        if richtung == -1:
            self.image = pygame.transform.flip(self.image, True, False)
        self.image = pygame.transform.scale(self.image, (250,175))
        self.rect = self.image.get_rect()
        if richtung == 1:
            self.rect.right, self.rect.bottom = [0, HOEHEBODEN]
        else:
            self.rect.left, self.rect.bottom = [breite, HOEHEBODEN]
        self.geschw = [V_WILDSCHWEIN//FPS * richtung, 0]
        self.hp = 3
        self.desc = "Wildschwein"
        self.zeit = 0
        self.kollrip = True

    def bewegen(self):
        self.zeit +=1
        if self.zeit >= STARTBOAR*FPS:
            self.rect = self.rect.move(self.geschw)
    def hit(self):
        self.hp -=1
        if self.hp <= 0:
            spiel.gruppe_kollrip.remove(self)
            spiel.akt_objekte.remove(self)
    def onCreate(self):
        self.zeit = 0
        boar.play()
# Bosse

class Mensch(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        richtung = random.choice([-1,1])
        self.image = pygame.image.load("Mensch.png")
        self.image.set_colorkey(TRANSPARENCY)
        if richtung == -1:
            self.image = pygame.transform.flip(self.image, True, False)
        self.image = pygame.transform.scale(self.image, (350,450))
        self.rect = self.image.get_rect()
        if richtung == 1:
            self.rect.right, self.rect.bottom = [0, HOEHEBODEN]
        else:
            self.rect.left, self.rect.bottom = [breite, HOEHEBODEN]
        self.geschwx = V_MENSCH * richtung
        self.hp = 10
        self.richtung = richtung
        self.aktiv = True
        self.desc = "Mensch"
        self.kollrip = False
        self.bottleframes = 0
        self.nutframes = 0
        self.bosse = True
        
    def bewegen(self):
        self.bottleframes +=1
        self.nutframes +=1
        if self.aktiv:
            self.rect = self.rect.move((self.geschwx//FPS,0))
            if menu != True:
                if random.randint(1,int(2.5*FPS)) == 1:
                    self.aktiv = False
                    self.passiv_zeit = random.randint(3,7)/10.0
                elif self.rect.centerx <= ABSTANDM_RAND:
                    if self.richtung == -1:
                        self.turn(1)
                elif breite - self.rect.centerx <= ABSTANDM_RAND:
                    if self.richtung == 1:
                        self.turn(-1)
                elif random.randint(1,int(10*FPS)) == 1:
                    self.turn(-self.richtung)
        else:
            self.passiv_zeit-=1.0/FPS
            if self.passiv_zeit<=0:
                self.aktiv = True
        if  random.randint(1, FPS//6)==1 and self.bottleframes/FPS >= MINBOTTLES:
                self.dosenwerfen()
                self.bottleframes = 0
        if  random.randint(1, FPS//6)==1 and self.nutframes/FPS >= MINNUTSM:
                self.nuss_werfen()
                self.nutframes = 0
    def turn(self, richtung):
        self.geschwx = richtung * V_MENSCH
        if self.richtung != richtung:
             self.image = pygame.transform.flip(self.image, True, False)
        self.richtung = richtung

    def dosenwerfen(self):
        if self.hp > 0:
            bottle = Beerbottle((self.rect.centerx + 150*self.richtung, self.rect.centery),  random.randint(-250,250),BOTTLEVY)
            spiel.akt_objekte.insert(0, bottle)
            spiel.gruppe_kollrip.add(bottle)
            self.bottleframes = 0
    def hit(self):
        self.hp -=1
        if self.hp <= 0:
            spiel.ragequit(self)
    def nuss_werfen(self):
        if self.hp > 0:
            abst_zu_ttl = abst(self.rect.center,turtle.rect.center)
            absabst = max(1,norm(abst_zu_ttl)) #just to be sure
            nuss = Walnuss(self.rect.center,250*abst_zu_ttl[0]/absabst, -750)
            spiel.akt_objekte.insert(0, nuss)
            spiel.gruppe_kollrip.add(nuss)
            self.nutframes = 0
##        
##class Mafiaturtle()
##class Krokodil()
##        
##fliegende tötende Dinger
class Walnuss(pygame.sprite.Sprite):
    
    def __init__(self, ort, vx, vy):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("walnuss.bmp")
        self.image.set_colorkey(TRANSPARENCY)
        self.image = pygame.transform.scale(self.image, (30,32))
        self.rect = self.image.get_rect()
        self.rect.center = ort
        self.vx = vx
        self.vy = vy
        self.aktiv = True
        self.item_type = "Walnuss"
        self.alive = True
        self.desc = "Walnuss"
        
    def bewegen(self):
        if self.aktiv:
            wegy, isamboden  = berechneweg_g(self.vy, self.rect.bottom)
            self.vy = self.vy + GRAVITATION / FPS
            self.rect = self.rect.move(self.vx // FPS, int(wegy))
            if isamboden:
                self.aktiv = not isamboden
                spiel.gruppe_kollrip.remove(self)
                spiel.gruppe_item.add(self)
                if self in spiel.gruppe_nussinluft:
                    spiel.gruppe_nussinluft.remove(self)
                    if random.randint(1,WALNUSSBAMLUCK) == 1 and spiel.baumcounter >= 1 and self.rect.centerx >= 0 and self.rect.centerx <= breite:
                        spiel.ragequit(self)
                        walnuttree = Walnuttree(self.rect.centerx)
                        spiel.akt_objekte.append(walnuttree)
                        spiel.baumcounter -= 1
                        

    def hit (self):
        if self.alive:
            spiel.ragequit(self)
            self.alive = False

class Beerbottle (pygame.sprite.Sprite):
     def __init__(self, ort, vx, vy):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("beerbottle.png")
        self.image.set_colorkey(TRANSPARENCY)
        self.image = pygame.transform.scale(self.image, (40,110))
        self.rect = self.image.get_rect()
        self.rect.center = ort
        self.vx = vx
        self.vy = vy
        self.desc = "Bottle"
        
     def bewegen(self):
        wegy, isamboden  = berechneweg_g(self.vy, self.rect.bottom)
        self.vy = self.vy + GRAVITATION / FPS
        self.rect = self.rect.move(self.vx // FPS, int(wegy))
        if isamboden:
            self.vx = 0
                        
     def hit (self):
        spiel.ragequit(self)
        self.alive = False

#freundliche Objekte
class Brieftaube (pygame.sprite.Sprite):
    def __init__ (self):
        pygame.sprite.Sprite.__init__(self)
        self.richtung = random.choice([1, -1])
        self.image = pygame.image.load("brieftaube.png")
        self.image = pygame.transform.scale(self.image, (58,54))
        self.image.set_colorkey(TRANSPARENCY)
        self.rect = self.image.get_rect()
        self.hp = 1
        
        if self.richtung == 1:
            self.rect.right, self.rect.top = [0, int(hoehe*(random.randint(0,2)/10))]
        else:
            self.rect.left, self.rect.top = [breite, int(hoehe*(random.randint(0,2)/10))]
            self.image = pygame.transform.flip(self.image, True, False)
        self.pos = self.rect.center
        self.vx = 300 * self.richtung
        self.itemcounter = ITEMSBRIEFTAUBE
        self.desc = "Taube"
        self.kollrip = False
        self.bosse = True
        
    def bewegen(self):
        self.rect = self.rect.move(self.vx//FPS,0)
        
    def dropitem (self):
        if self.itemcounter > 0:
            self.itemcounter -=1
            item_name = random.choice(spiel.levelinfo.items)
            item = item_zu_buchstabe[item_name](self.rect.center, (ITEMV * self.richtung, 10))
            spiel.akt_objekte.insert(0, item)
            spiel.gruppe_item.add(item)
            bitch.play()
            
    def hit (self):
        self.hp -=1
        if self.hp <= 0:
            self.dropitem ()
            spiel.ragequit (self)
            

class ItemSchild(pygame.sprite.Sprite):
    def __init__(self, ortmitte, v):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("schild.bmp")
        self.image.set_colorkey(TRANSPARENCY)
        self.image = pygame.transform.scale(self.image, (100,100))
        self.rect = self.image.get_rect()
        self.rect.center = ortmitte
        self.vx, self.vy = v
        self.posx, self.posy = ortmitte
        self.item_type = "Schild"
        self.triggerKey = pygame.K_DOWN
      
    def bewegen (self):
        weg, isamboden = berechneweg_g(self.vy, self.rect.bottom)
        self.posx += self.vx/FPS
        self.posy += weg
        self.vy = self.vy + GRAVITATION/FPS
        self.rect.center = (int(self.posx), int(self.posy))
        if isamboden:
            self.vx = 0
        
    def trigger(self, info = None):
      ##x, y = turtle_pos
      ##vx, vy = turtle_v
      effect = EffectNutShield(turtle, SHIELDDURATION)
      turtle.addEffect(effect)
      turtle.items.remove(self)

class ItemMuffin(pygame.sprite.Sprite):
    def __init__(self, ortmitte, v):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("muffin.bmp")
        self.image.set_colorkey(TRANSPARENCY)
        self.image = pygame.transform.scale(self.image, (100,100))
        self.rect = self.image.get_rect()
        self.rect.center = ortmitte
        self.vx, self.vy = v
        self.posx, self.posy = ortmitte
        self.item_type = "Muffin"
      
    def bewegen (self):
        weg, isamboden = berechneweg_g(self.vy, self.rect.bottom)
        self.posx += self.vx/FPS
        self.posy += weg
        self.vy = self.vy + GRAVITATION/FPS
        self.rect.center = (int(self.posx), int(self.posy))
        if isamboden:
            self.vx = 0
    def execute(self, ort):
        turtle.addEffect(Effectkleiner(turtle, SHRINKINGDURATION))
        turtle.image = pygame.transform.scale(turtle.image, (33,33))
        turtle.rect = turtle.image.get_rect()
        turtle.rect.centerx, turtle.rect.bottom = ort


class ItemMachineGun(pygame.sprite.Sprite):
    def __init__(self, ortmitte, v):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("machinegun.bmp")
        self.image.set_colorkey(TRANSPARENCY)
        self.image = pygame.transform.scale(self.image, (100,100))
        self.rect = self.image.get_rect()
        self.rect.center = ortmitte
        self.vx, self.vy = v
        self.posx, self.posy = ortmitte
        self.item_type = "MachineGun"
        self.triggerKey = pygame.K_UP
      
    def bewegen (self):
        weg, isamboden = berechneweg_g(self.vy, self.rect.bottom)
        self.posx += self.vx/FPS
        self.posy += weg
        self.vy = self.vy + GRAVITATION/FPS
        self.rect.center = (int(self.posx), int(self.posy))
        if isamboden:
            self.vx = 0
        
        
    def trigger(self, info = None):
      effect = EffectMachineGun(turtle, GUNDURATION)
      turtle.addEffect(effect)
      turtle.items.remove(self)
      
class Walnuttree(pygame.sprite.Sprite):
    def __init__ (self,ort):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("walnuttree.png").convert()
        self.image.set_colorkey(TRANSPARENCY)
        self.image = pygame.transform.scale(self.image, (424,450))
        self.rect = self.image.get_rect()
        self.rect.bottom = HOEHEBODEN
        self.rect.centerx = ort
        self.nutcounter = NUESSEWALNUTTREE
        spiel.gruppe_item.add(self)
        self.item_type = "walnuttree"
        self.frame = 0
        self.desc = "Walnussbaum"
        weed.play()
        
    def bewegen(self):
        self.frame +=1
        if self.frame/FPS >= NUSSERTNECOOLDOWN:
            self.nutcounter = NUESSEWALNUTTREE
            self.frame = 0
    def collisionturtle(self):
        if random.randint(1,5) == 1 and self.nutcounter > 0:
            self.nussabwerfen()

    def nussabwerfen(self): 
        self.nutcounter -=1
        nuss = Walnuss((self.rect.centerx + random.randint(-200,200), 400), 0, 0)
        spiel.akt_objekte.insert(random.randint(-1,0), nuss)         
#Effekte
class Effect:
    def __init__(self, hostOb, duration = -1):
      self.frames_verg = 0
      self.host = hostOb
      self.duration = duration
      self.properties = []
      self.image = None
    def bewegen(self):
        self.frames_verg += 1
        if self.duration != -1 and self.frames_verg >= self.duration * FPS:
            self.host.removeEffect(self)

    def onEffectEnd(self):
        pass
    def turn(self, richtung):
        pass

class EffectNutShield(Effect):
    def __init__(self, hostOb, duration):
        Effect.__init__(self, hostOb, duration)
        self.properties = ["IMMUNETONUTS"]
        self.image = pygame.image.load("schild.bmp")
        self.image.set_colorkey(TRANSPARENCY)
        self.image = pygame.transform.scale(self.image, (50,50))
        self.rect = self.image.get_rect()
        self.rect.center = turtle.rect.center

    def bewegen(self):
        Effect.bewegen(self)
        self.rect.center = turtle.rect.center


class Effectkleiner(Effect):
    def __init__(self,hostOb, duration):
        Effect.__init__(self, hostOb, duration)
        self.properties = ["SHRINK"]
    def onEffectEnd(self):
        if not turtle.hasProperty("SHRINK"):
            mittex, unten = turtle.rect.centerx, turtle.rect.bottom
            turtle.image = pygame.image.load("schildkroete.bmp")
            turtle.image.set_colorkey(TRANSPARENCY)
            turtle.image = pygame.transform.scale(turtle.image, (100,100))
            turtle.rect = turtle.image.get_rect()
            turtle.rect.left, turtle.rect.bottom = [mittex,unten]
            turtle.pos = turtle.rect.center
            if turtle.richtung == 1:
                turtle.image = pygame.transform.flip(turtle.image, True, False)

class EffectMachineGun (Effect):
    def __init__(self, hostOb, duration):
        Effect.__init__(self, hostOb, duration)
        self.properties = ["DRRRRR"]
        self.image = pygame.image.load("machinegun.bmp")
        self.image.set_colorkey(TRANSPARENCY)
        self.image = pygame.transform.scale(self.image, (75,75))
        self.rect = self.image.get_rect()
        self.rect.center = turtle.rect.center
        self.framesSinceShot = 0
        if turtle.richtung == 1:
            self.image = pygame.transform.flip(self.image, True, False)
    def bewegen(self):
        Effect.bewegen(self)
        self.rect.center = turtle.rect.center
        self.framesSinceShot += 1
        if self.framesSinceShot >= GUNINTERVAL * FPS:
            self.framesSinceShot = 0
            entfernung = [mausx - turtle.pos[0] , mausy - turtle.pos[1]]
            shootwalnut = Walnuss(turtle.rect.center,F_VSCHUSS* entfernung [0],F_VSCHUSS* entfernung [1])
            spiel.akt_objekte.insert(0, shootwalnut)
            spiel.gruppe_nussinluft.add(shootwalnut)
            
    def turn(self,richtung):
        self.image = pygame.transform.flip(self.image, True, False)

#Ende der Objekte(ausser turtle)

class JumpTurtle(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("schildkroete.bmp")
        self.image.set_colorkey(TRANSPARENCY)
        self.image = pygame.transform.scale(self.image, (100,100))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.bottom = [breite // 2, int(hoehe*0.9)]
        self.pos = self.rect.center
        pygame.display.flip()
        self.geschw = [0, 0]
        self.im_sprung = False
        self.richtung = -1
        self.nutcount = 0
        self.effects = []
        self.items = []
        self.hatschild = 0
        self.hatmachinegun = 0
        

    #führt die Bewegung in jedem Frame aus, auch im Sprung
    def gehen(self):
        wegy, isamboden = berechneweg_g (self.geschw[1], self.rect.bottom)
        if not isamboden:
            self.geschw[1] = self.geschw[1] + GRAVITATION/FPS
        else:
            self.im_sprung = False
            self.geschw = [0,0]
            if keymemory != [0,0]:
                self.turn(self.richtung)
        self.rect = self.rect.move(self.geschw[0]//FPS, int(wegy))
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= breite:
            self.rect.right = breite
        self.pos = self.rect.center
        #Effekte machen shit
##        for effect in self.effects:
##            effect.everyFrame()
    def springen(self,entfernung):#entfernung = Entfernung vom Punkt
        if not turtle.im_sprung:
            ent1 = math.sqrt(entfernung[0] ** 2 + entfernung[1] ** 2)
            if ent1 > 50:
                self.geschw = entfernung
            self.im_sprung = True
            if ent1 > SPRUNGCAP:
                self.geschw[0] = entfernung[0] * SPRUNGCAP / ent1
                self.geschw[1] = entfernung[1] * SPRUNGCAP / ent1
                
    def turn(self,richtung):
        if not self.im_sprung:
            self.geschw[0] = richtung*GEHV
        if self.richtung != richtung:
             self.image = pygame.transform.flip(self.image, True, False)
             for effect in self.effects:
                 effect.turn(richtung)
        self.richtung = richtung

    def shootnut (self, entfernung):
        if self.nutcount > (NUTSINSACK-1):
            shootwalnut = Walnuss(self.rect.center,F_VSCHUSS* entfernung [0],F_VSCHUSS* entfernung [1])
            spiel.akt_objekte.insert(0, shootwalnut)
            spiel.gruppe_nussinluft.add(shootwalnut)
            self.nutcount -=NUTSINSACK
        
    def sammeln (self, ob):
        if ob.item_type == "Walnuss":
            self.nutcount +=1
            spiel.gruppe_item.remove(ob)
            spiel.akt_objekte.remove(ob)
        elif ob.item_type == "walnuttree":
            ob.collisionturtle()
        elif ob.item_type == "Schild":
            self.hatschild +=1
            spiel.ragequit(ob)
            self.items.append(ob)
        elif ob.item_type == "MachineGun":
            self.hatmachinegun +=1
            spiel.ragequit(ob)
            self.items.append(ob)
        elif ob.item_type == "Muffin":
            spiel.ragequit(ob)
            ob.execute((self.rect.centerx, self.rect.bottom))
            
    def addEffect(self, effect):
        self.effects.append(effect)

    def removeEffect (self, effect):
        self.effects.remove(effect)
        effect.onEffectEnd()
      
    def useItem(self, key):
        for item in self.items:
            if item.triggerKey == key:   
                item.trigger()
                if item.item_type == "Schild":
                    turtle.hatschild -=1
                elif item.item_type == "MachineGun":
                    turtle.hatmachinegun -=1
                break
        
    def hasProperty(self, property_name):
        for effect in self.effects:
            if property_name in effect.properties:
                return True
        return False
    
class Spiel(object):
    def __init__(self):
        self.level = 0
        self.font1 = pygame.font.Font(None, 100)
        self.font2 = pygame.font.Font(None, 40)
        self.zeit=0
        self.akt_objekte = []
        self.gruppe_kollrip = pygame.sprite.Group()   # Gruppe: mit Kollision stirb man
        self.gruppe_item = pygame.sprite.Group()
        self.gruppe_nussinluft = pygame.sprite.Group()
        self.gruppe_bosse = pygame.sprite.Group()
        self.counter = 0
        pygame.mixer.music.play(-1)
        
    def meldung(self, text): #Damit wird eine Meldung angezigt
        text = self.font1.render(text, 2, (0,0,100))
        screen.blit(text, [breite/2-500, 100])

    def status(self): #Gibt die Zeit im rechten oberen Eck an
        text = self.font2.render("Zeit: %2i" %self.verb_zeit, 1, (0,0,0))
        screen.blit(text, [1075, 40])
        text = self.font2.render("Level: %1i" %self.level, 1, (0,0,0))
        screen.blit(text, [1075, 10])
        text = self.font2.render("Nüsse: %1.1f" %(turtle.nutcount/NUTSINSACK), 1, (0,0,0))
        screen.blit(text, [1075, 70])
        text = self.font2.render("Schild: %i" %(turtle.hatschild), 1, (0,0,0))
        screen.blit(text, [1275, 10])
        text = self.font2.render("Schleuder: %i" %(turtle.hatmachinegun), 1, (0,0,0))
        screen.blit(text, [1275, 40])

    def won (self):
            self.meldung("YOU WON")
            turtle.nutcount = 0
            turtle.items = []
            win.play()
            pygame.display.flip()
            pygame.time.delay(1000)
            screen.fill([255,255,255])
            menufkt()

        
    def start_neues_level(self, levelinfo):#Startet neues Level und legt Startzeiten für
        global  turtle, menu, levelmenus
        turtle = JumpTurtle()
        if menu == False and levelmenus == False:
            turtle.nutcount = levelinfo.nuesse
            screen.blit(background, (0,0))
            self.akt_objekte = []#Objekte fest
            self.gruppe_nussinluft = pygame.sprite.Group()
            self.gruppe_item = pygame.sprite.Group()
            self.gruppe_kollrip = pygame.sprite.Group()
            self.gruppe_bosse = pygame.sprite.Group()
            self.meldung("LEVEL %s" %levelinfo.name)
            pygame.display.flip()
            pygame.time.delay(3000)
            self.baumcounter = levelinfo.maxbamoida
        self.start_objekte = {}
        for obj_zeit in levelinfo.startzeiten:
            self.start_objekte[klasse[obj_zeit[0]]()] = obj_zeit[1]
        self.start = self.zeit
        self.zeitFuerLvl = levelinfo.zeit
        self.levelinfo = levelinfo

    def ragequit (self, ob):
        for gruppe in [self.gruppe_nussinluft,self.gruppe_item
                       ,self.gruppe_kollrip, self.akt_objekte, self.gruppe_bosse]:
            if ob in gruppe:
                gruppe.remove(ob)
    

    def koll_erk(self):
        nut_immune = turtle.hasProperty("IMMUNETONUTS")
        kolls =  pygame.sprite.spritecollide(turtle, self.gruppe_kollrip, False)
        for koll in kolls:
            if koll.desc != "Walnuss" or not nut_immune:
              return True
        return False
            
    def koll_goodthings (self):
        itemcollided = pygame.sprite.spritecollide(turtle, self.gruppe_item, False)
        for item in itemcollided:
            turtle.sammeln(item)
            
    def koll_hittingthings (self):
        for walnut in self.gruppe_nussinluft:
            hittingcollided = pygame.sprite.spritecollide(walnut, self.gruppe_kollrip, False)+pygame.sprite.spritecollide(walnut, self.gruppe_bosse, False)
            for objekt in hittingcollided:
                objekt.hit()
                walnut.hit()
                if objekt.desc == "Walnuss":
                  explosion.play()        
        
    def animieren(self):
        self.zeit +=1
        self.verb_zeit= self.zeitFuerLvl + (self.start - self.zeit)/FPS
        screen.blit(background, (0,0))
        turtle.gehen()
        for obj in self.akt_objekte:
            obj.bewegen()
            screen.blit(obj.image, obj.rect)
        self.koll_goodthings()
        self.koll_hittingthings()
        screen.blit(turtle.image, turtle.rect)
        for effect in turtle.effects:
            effect.bewegen()
            if effect.image != None:
                screen.blit(effect.image, effect.rect)
        self.status()   
        pygame.display.flip()
        for obj in self.start_objekte:
            if self.start_objekte[obj] >= self.verb_zeit:
                self.akt_objekte.append(obj)
                if obj.kollrip:
                    self.gruppe_kollrip.add(obj)
                elif obj.bosse:
                    self.gruppe_bosse.add(obj)
                try:
                    obj.onCreate()
                except:
                    pass
                self.start_objekte[obj] = -10
        if self.verb_zeit <= 0:
            for level in lvllist:
                if self.levelinfo.lvlnr + 1 == level.lvlnr:
                    self.start_neues_level(level)
                    return
            self.won()
        if self.koll_erk():
            self.meldung("GAME OVER!")
            random.choice([nope,gameover,sad]).play()
            pygame.mixer.music.load(random.choice(music))
            pygame.display.flip()
            pygame.time.delay(1000)
            self.level = 0
            turtle.nutcount = 0
            turtle.items = []
            screen.blit(background, (0,0))
            self.start_neues_level(self.levelinfo)
            pygame.mixer.music.play(-1)

    def menuanimieren(self):
        self.counter +=1
        if self.counter >= 2*FPS:
            obj = random.choice(list(klasse.values()))()
            self.akt_objekte.append(obj)
            self.counter = 0
        self.verb_zeit= self.zeitFuerLvl + (self.start - self.zeit)/FPS
        screen.blit(background, (0,0))
        turtle.gehen()
        for obj in spiel.akt_objekte:
            obj.bewegen()
            screen.blit(obj.image, obj.rect)
        
     

klasse = {"M":Moewe, "F":Fuchs, "W":Wolf, "FP":Flyingpenguin, "WS":Wildschwein, "ME":Mensch, "BT":Brieftaube} #Hier definieren was welcher Buchstabe sagt
item_zu_buchstabe = {"S":ItemSchild, "M": ItemMuffin, "MG": ItemMachineGun}
uhr = pygame.time.Clock()
turtle = JumpTurtle()
turtle_x = 0     # Wenn turtle_x == 1 , dann rechts, bei -1 links
mausx = breite - 70
mausy = hoehe - 70
mauspos = [mausx, mausy]
spiel = Spiel()
pause = False


def menufkt():
    global menu
    menu = True
    pygame.mixer.music.load(random.choice(music))
    pygame.mixer.music.play(-1)
    spiel.start_neues_level(lvlmenu)
    while menu:
        uhr.tick(FPS)
        spiel.menuanimieren()
        
        button_1 =pygame.Rect (50, 100, 200, 50)
        button_2 =pygame.Rect (50, 200, 200, 50)
        button_3 =pygame.Rect (50, 300, 200, 50)
        button_4 =pygame.Rect (50, 400, 200, 50)
            
        pygame.draw.rect (screen, (0, 0, 100), button_1)
        pygame.draw.rect (screen, (0, 0, 100), button_2)
        pygame.draw.rect (screen, (0, 0, 100), button_3)
        pygame.draw.rect (screen, (0, 0, 100), button_4)
        
        pygame.font.SysFont("chiller", 10)
        text1 = spiel.font2.render("start", 1, (240,240,255))
        screen.blit(text1, [100, 110])
        text2 = spiel.font2.render("Tutorial", 1, (240,240,255))
        screen.blit(text2, [100, 210])
        text3 = spiel.font2.render("levels", 1, (240,240,255))
        screen.blit(text3, [100, 310])
        text4 = spiel.font2.render("end game", 1, (240,240,255))
        screen.blit(text4, [100, 410])
        text5 = spiel.font2.render("sb is very nab", 1, (0,0,0))
        screen.blit(text5, [1175, 40])
   
        
        
        for event in pygame.event.get():
            mx, my = pygame.mouse.get_pos()
            click = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
            if button_1.collidepoint((mx,my)):
                if click:
                  menu = False
                  spiel.start_neues_level(lvl1)
            if button_2.collidepoint((mx,my)):
                if click:
                  spiel.start_neues_level(tutorial)
                  menu = False
            if button_3.collidepoint((mx,my)):
                if click:
                    levelmenu()
            if button_4.collidepoint((mx,my)):
                if click:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_s:
                    menu = False
        pygame.display.flip()


def levelmenu():
    global levelmenus, menu
    levelmenus = True
    y = 0
    x = 50
    buttons = []
    t = []
    pygame.font.SysFont("chiller", 10)
    for lvl in lvllist:
        y +=100
        if y > hoehe - 100:
            x = x + 350
            y = 100
        button = pygame.rect.Rect(x, y , 300, 50)
        text = spiel.font2.render(lvl.name, 1, (240, 240, 255))
        t.append(text)
        buttons.append(button)
    while levelmenus:
        uhr.tick(FPS)
        spiel.menuanimieren()
        for button in buttons:
            pygame.draw.rect(screen, (0,0,100), button)
        y = 0
        x = 100
        for text in t:
            y += 100
            if y > hoehe - 100:
                x = x + 350
                y = 100
            screen.blit(text, [x, y + 10])
        button_exit = pygame.rect.Rect(breite//2 -100,  hoehe - 50, 200, 50)
        pygame.draw.rect(screen, (0,0,100), button_exit)
        text_exit = spiel.font2.render("exit",1,(240,240,255))
        screen.blit(text_exit, [breite//2 - 50,  hoehe - 40])
        text5 = spiel.font2.render("sb is nab", 1, (0,0,0))
        screen.blit(text5, [1175, 40])
        
        for event in pygame.event.get():
            mx, my = pygame.mouse.get_pos()
            click = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
                for i in range(len(buttons)):
                    if buttons[i].collidepoint((mx,my)):
                        if click:
                          levelmenus = False
                          menu = False
                          spiel.start_neues_level(lvllist[i])
                if button_exit.collidepoint((mx,my)):
                    if click:
                        levelmenus = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_s:
                    levelmenus = False
        pygame.display.flip()    
    
menufkt()

while True:  
    uhr.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                keymemory[0] = True
                turtle.turn(1)
            elif event.key == pygame.K_LEFT:
                keymemory[1] = True
                turtle.turn(-1)
            elif event.key == pygame.K_SPACE:
                pause = not pause
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.key == pygame.K_m:
                menufkt()
            else:
                turtle.useItem(event.key)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                keymemory[0] = False
                if keymemory [1]:
                    turtle.turn(-1)                    
            if event.key == pygame.K_LEFT:
                keymemory[1] = False
                if keymemory [0]:
                    turtle.turn(1)
            if not turtle.im_sprung and keymemory == [False, False]:
                turtle.geschw = [0,0]
        elif event.type == pygame.MOUSEMOTION:
            mausx, mausy = mauspos = event.pos
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                turtle.springen([mausx - turtle.pos[0] , mausy - turtle.pos[1]])
            if event.button == pygame.BUTTON_RIGHT:
                turtle.shootnut([mausx - turtle.pos[0] , mausy - turtle.pos[1]])
    if not pause:
        spiel.animieren()


