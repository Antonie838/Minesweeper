import pygame as pg
import random
pg.init()
vel_okna = 800
okno = pg.display.set_mode((vel_okna, vel_okna))
pg.display.set_caption('MineSweeper')


vel = 40
pocet = 16
zacatek_pole = (vel_okna/2)-((vel*(pocet)+(pocet-2)*5)/2)
objects = []
buttons = []
hry = []
plocha_ = []
stav_hry = 1
start = False
cas = pg.time.Clock()

# Grafika
pozadi = pg.image.load('obr/pozadi.png').convert()
plocha_fake = pg.image.load('obr/plocha_fake.png').convert()
zakryty = pg.image.load('obr/pole_zakryte.png').convert()
vlajka = pg.image.load('obr/vlajka.png').convert()
otaznik = pg.image.load('obr/otaznik.png').convert()
odkryty_prazdny = pg.image.load('obr/pole_odkryte.png').convert()
odkryty_1 = pg.image.load('obr/1.png').convert()
odkryty_2 = pg.image.load('obr/2.png').convert()
odkryty_3 = pg.image.load('obr/3.png').convert()
odkryty_4 = pg.image.load('obr/4.png').convert()
odkryty_5 = pg.image.load('obr/5.png').convert()
odkryty_6 = pg.image.load('obr/6.png').convert()
odkryty_7 = pg.image.load('obr/7.png').convert()
odkryty_8 = pg.image.load('obr/8.png').convert()
bomba = pg.image.load('obr/bomba.png').convert()
bomba_vybouchla = pg.image.load('obr/bomba_odbouchla.png').convert()
vyhra_obr = pg.image.load('obr/vyhra.png').convert_alpha()
prohra_obr = pg.image.load('obr/prohra.png').convert_alpha()

class hrat_znova:
    def __init__(self, vysledek):
        self.vysledek = vysledek
        self.sirka = 500
        self.vyska = 150                
        self.x = (vel_okna / 2) - (self.sirka / 2)
        self.y = (vel_okna / 2) - (self.vyska / 2)   
        self.rect = pg.Rect(self.x, self.y, self.sirka, self.vyska)
        hry.append(self)
    def grafika(self):
        if self.vysledek == 1:       #stav_hry
            okno.blit(vyhra_obr, self.rect)
        if self.vysledek == -1:       #stav_hry
            okno.blit(prohra_obr, self.rect)

        

class pole:
    def __init__(self, x: int, y: int, souradnice_x, souradnice_y, miny_okolo: int):
        self.x = x
        self.y = y
        self.souradnice_x = souradnice_x
        self.souradnice_y = souradnice_y
        self.miny_okolo = miny_okolo
        self.otocen = False
        self.vlajka_ = False
        self.otaznik_ = False
        self.zmacknut = False
        self.vel = vel
        self.pocet = pocet
        self.rect = pg.Rect(self.x, self.y, self.vel, self.vel)
        objects.append(self)
    def grafika(self):
        if self.otocen == False:
            okno.blit(zakryty, self.rect)
            if self.vlajka_ == True:
                okno.blit(vlajka, self.rect)
            elif self.otaznik_ == True:
                okno.blit(otaznik, self.rect)
        else:
            if self.miny_okolo == -2:
                okno.blit(bomba_vybouchla, self.rect)
            elif self.miny_okolo == -1:
                okno.blit(bomba, self.rect)
            elif self.miny_okolo == 0:
                okno.blit(odkryty_prazdny, self.rect)
            elif self.miny_okolo == 1:
                okno.blit(odkryty_1, self.rect)
            elif self.miny_okolo == 2:
                okno.blit(odkryty_2, self.rect)
            elif self.miny_okolo == 3:
                okno.blit(odkryty_3, self.rect)
            elif self.miny_okolo == 4:
                okno.blit(odkryty_4, self.rect)
            elif self.miny_okolo == 5:
                okno.blit(odkryty_5, self.rect)
            elif self.miny_okolo == 6:
                okno.blit(odkryty_6, self.rect)
            elif self.miny_okolo == 7:
                okno.blit(odkryty_7, self.rect)
            elif self.miny_okolo == 8:
                okno.blit(odkryty_8, self.rect)
    def otocit(self):
        global stav_hry
        global start
        mouse_pos = pg.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if pg.mouse.get_pressed()[0]:
                if self.vlajka_ == False and self.otaznik_ == False and self.miny_okolo != -1:
                    self.otocen = True
                    start = True
                    if not self.zmacknut:
                        self.zmacknut = True
                if self.vlajka_ == False and self.otaznik_ == False and self.miny_okolo == -1:
                    if start == True:
                        self.otocen = True
                        self.miny_okolo = -2        # odbouchl minu
                    stav_hry = -1
                    if not self.zmacknut:
                        self.zmacknut = True
    def vlajka(self):
        '''vykresní vlajku'''
        mouse_pos = pg.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if pg.mouse.get_pressed()[2]:
                if self.otocen == False and self.vlajka_ == False and self.otaznik_ == False and not self.zmacknut: # zapne vlajku
                    self.vlajka_ = True
                    if not self.zmacknut:
                        self.zmacknut = True
                elif self.vlajka_ == True and not self.zmacknut: # zapne otazník
                    self.vlajka_ = False
                    self.otaznik_ = True
                    if not self.zmacknut:
                        self.zmacknut = True
                elif self.otaznik_ == True and not self.zmacknut: #vypne otazník
                    self.otaznik_ = False
                    if not self.zmacknut:
                        self.zmacknut = True
            else:
                self.zmacknut = False
    
class herni_plocha:
    def __init__(self, resta_mina = [-1, -1]):
        self.resta_mina = resta_mina
        self.poc_min = 40
        # vytvoření plochy
        for i in range(pocet):
            radek = []
            for j in range(pocet):
                k = random.random()
                if k < 0.85:
                    pol = pole(zacatek_pole+i*vel+i*5, zacatek_pole+j*vel+j*5, i, j, 0)
                else:
                    if i == self.resta_mina[0] and j == self.resta_mina[1]:
                        pol = pole(zacatek_pole+i*vel+i*5, zacatek_pole+j*vel+j*5, i, j, 0)
                    if self.poc_min == 0:
                        pol = pole(zacatek_pole+i*vel+i*5, zacatek_pole+j*vel+j*5, i, j, 0)
                    else:
                        pol = pole(zacatek_pole+i*vel+i*5, zacatek_pole+j*vel+j*5, i, j, -1)
                        self.poc_min -= 1
                radek.append(pol)
            plocha_.append(radek)
        for i in range(pocet):      # přiřazení čísel polím 
            for j in range(pocet):
                for x in range(-1, 2):
                    if i + x >= 0 and i + x < pocet:
                        for y in range(-1, 2):
                            if j + y >= 0 and j + y < pocet:
                                if plocha_[i][j].miny_okolo != -1:
                                    if plocha_[i+x][j+y].miny_okolo == -1:
                                        plocha_[i][j].miny_okolo += 1

    def vlna(self, obj: pole):
        '''vytvoří vlnu volných políček po kliknutí'''
        obj_x = obj.souradnice_x
        obj_y = obj.souradnice_y
        if plocha_[obj_x][obj_y].otocen == False:     # jestli je vedle mě jedno odkrytý s číslem nula a já nejsem -1 tak se odkreju 
            if obj.miny_okolo != -1:
                for i in range(-1, 2):
                    if obj.souradnice_x + i >= 0 and obj.souradnice_x + i < pocet:
                        for j in range(-1, 2):
                            if obj.souradnice_y + j >= 0 and obj.souradnice_y + j < pocet:
                                if plocha_[obj_x+i][obj_y+j].otocen == True and plocha_[obj_x+i][obj_y+j].miny_okolo > -1:
                                    if plocha_[obj_x+i][obj_y+j].miny_okolo == 0:
                                        obj.otocen = True

def mainloop():
    okno.fill((38, 13, 52))
    plocha = herni_plocha()
    global start
    global stav_hry
    global plocha_
    global objects
    global hry
    a = True
    run = True
    prohra = False
    vyhra = False
    while run:
        pg.time.delay(50)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if prohra or vyhra:
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_r:
                        run = False
                        for i in plocha_:
                            for j in i:
                                j.miny_okolo = 0
                        plocha_ = []
                        objects = []
                        hry = []
                        start = False
                        mainloop()
        if pg.mouse.get_pressed()[0] and start == False and stav_hry == -1:         # první neni mina
            okno.blit(plocha_fake, (zacatek_pole, zacatek_pole))
            okno.fill((38, 13, 52))
            for i in plocha_:
                        for j in i:
                            j.miny_okolo = 0
            mouse_pos = pg.mouse.get_pos()
            x = int((mouse_pos[0] - zacatek_pole + 5/2) // (vel + 5))
            y = int((mouse_pos[1] - zacatek_pole + 5/2) // (vel + 5))
            plocha_ = []
            plocha = herni_plocha([x, y])
            plocha_[x][y].otocen = True
            stav_hry = 0
            a = True            
        stav_hry = 1
        for object in objects:
            if a:
                object.grafika()
                object.otocit() 
                object.vlajka()
                plocha.vlna(object)
            if stav_hry == -1:
                if object.miny_okolo == -1 or object.miny_okolo == -2:
                    object.otocen = True
                    object.grafika()
            if object.miny_okolo != -1:
                if object.otocen == False:
                    if stav_hry != -1:
                        stav_hry = 0
            if stav_hry == 0:
                continue
        if stav_hry == -1 and start == True and run == True:
            a = False
            prohra = True
            # print('Prohrál jsi.')
            print(start)
            print(stav_hry)
            hrat_znova(-1)
        if stav_hry == 1 and run == True:
            vyhra = True
            a = False
            # print('vyhrál jsi!')
            hrat_znova(1)
        for x in hry:
            if stav_hry != 0:
                x.grafika()
        
        pg.display.update()
        cas.tick(32)

mainloop()
pg.quit()
