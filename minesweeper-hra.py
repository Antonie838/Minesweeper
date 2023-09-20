import pygame as pg
import random
pg.init()
pg.display.set_caption('MineSweeper')


# globální proměnné
vel = 40
pocet = 16
vel_okna = (pocet*vel + (pocet - 1)*5) + 80
okno = pg.display.set_mode((vel_okna, vel_okna))
zacatek_pole = (vel_okna/2)-((vel*(pocet)+(pocet-1)*5)/2)
objects = []
hry = []
plocha_ = []
obtiznost = 'nic'
stav_hry = 1
start = False
cas = pg.time.Clock()

# Grafika
pozadi = pg.image.load('obr/pozadi.png').convert()
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
menu = pg.image.load('obr/menu.png').convert_alpha()
easy_obr = pg.image.load('obr/easy.png').convert_alpha()
medium_obr = pg.image.load('obr/medium.png').convert_alpha()
hard_obr = pg.image.load('obr/hard.png').convert_alpha()
konec = pg.image.load('obr/konec.png').convert_alpha()


class button:
    '''
    Třída reprezentuje dimenze tlačítka.
    ...
    Atributy
    --------
    x : int
        x-souřadnice v pixelech
    y : int
        y-souřadnice v pixelech
    sirka : int
        šířka v pixelech
    vyska : int
        výška v pixelech
    obtiz : str
        Vyhodnocuje obtížnost hry, která se následovně pustí, tj. 'easy', 'medium', 'hard', nebo 'konec', kde 'konec' značí konec hry.
    '''
    def __init__(self, x, y, sirka, vyska, obtiz):
        '''
        Vrací objekt třídy button.
        ...
        Parametry
        ---------
        x : int
            x-souřadnice v pixelech
        y : int
            y-souřadnice v pixelech
        sirka : int
            šířka v pixelech
        vyska : int
            výška v pixelech
        obtiz : str
            Vyhodnocuje obtížnost hry, která se následovně pustí, tj. 'easy', 'medium', 'hard', nebo 'konec', kde 'konec' značí konec hry.
        '''
        self.sirka = sirka
        self.vyska = vyska              
        self.x = x
        self.y = y
        self.obtiznost = obtiz
        self.spusteno = False
        self.rect = pg.Rect(self.x, self.y, self.sirka, self.vyska)
        self.zmacknut = False
    def zmacknout(self):
        '''
        Zmáčkne tlačítko a uloží příslušnou obtížnost.
        '''
        global obtiznost
        mouse_pos = pg.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if pg.mouse.get_pressed()[0]:
                self.spusteno = True
                obtiznost = self.obtiznost
                if not self.zmacknut:
                    self.zmacknut = True
            else:
                self.zmacknut = False
                
class hrat_znova:
    '''
    Třída reprezentuje menu s volbou dalších her.
    ...
    Atributy
    --------
    vysledek : int
        Číslo určující výsledek hry, kde 0 znamená první spuštění hry, 1 výhru a -1 prohru.
    '''
    def __init__(self, vysledek):
        '''
        Vrací objekt třídy hrat_znova.
        ...
        Parametry
        ---------
        vysledek : int
            Číslo určující výsledek hry, kde 0 znamená první spuštění hry, 1 výhru a -1 prohru.
        '''
        self.vysledek = vysledek
        self.sirka = 500
        self.vyska = 250
        self.x = (vel_okna / 2) - (self.sirka / 2)
        self.y = (vel_okna / 2) - (self.vyska / 2)   
        self.rect = pg.Rect(self.x, self.y, self.sirka, self.vyska)
        self.easy = button(vel_okna/2 - 190, 380, 120, 40, 'easy')
        self.medium = button(vel_okna/2 - 60, 380, 120, 40, 'medium')
        self.hard = button(vel_okna/2 + 70, 380, 120, 40, 'hard')
        self.konec = button(vel_okna/2 - 190, 430, 380, 40, 'konec')
        hry.append(self)
    def grafika(self):
        '''
        Vykreslí menu s příslušnými popisky a tlačítky.
        '''
        if self.vysledek == 0:       #stav_hry
            okno.blit(menu, self.rect)
        if self.vysledek == 1:       #stav_hry
            okno.blit(vyhra_obr, self.rect)
        if self.vysledek == -1:       #stav_hry
            okno.blit(prohra_obr, self.rect)
        okno.blit(easy_obr, self.easy)
        okno.blit(medium_obr, self.medium)
        okno.blit(hard_obr, self.hard)
        okno.blit(konec, self.konec)

class pole:
    '''
    Třída reprezentující jedno hrací políčko.
    ...
    Atributy
    --------
    x : int
        x-souřadnice v pixelech
    y : int
        y-souřadnice v pixelech
    souradnice_x : int
        x-souřadnice v matici plocha_
    souradnice_y : int
        y-souřadnice v matici plocha_
    miny_okolo : int
        počet sousedních min
    '''
    def __init__(self, x: int, y: int, souradnice_x: int, souradnice_y: int, miny_okolo: int):
        '''
        Vrací objekt třídy pole.
        ...
        Parametry
        ---------
        x : int
            x-souřadnice v pixelech
        y : int
            y-souřadnice v pixelech
        souradnice_x : int
            x-souřadnice v matici plocha_
        souradnice_y : int
            y-souřadnice v matici plocha_
        miny_okolo : int
            počet sousedních min
        '''
        self.x = x
        self.y = y
        self.souradnice_x = souradnice_x
        self.souradnice_y = souradnice_y
        self.miny_okolo = miny_okolo
        self.otocen = False
        self.vlajka_ = False
        self.otaznik_ = False
        self.zmacknut = False
        self.zmacka_vlajka = False
        self.vel = vel
        self.pocet = pocet
        self.rect = pg.Rect(self.x, self.y, self.vel, self.vel)
        objects.append(self)
    def grafika(self):
        '''
        Vykreslí grafiku pole.
        '''
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
        '''
        Odkryje hodnotu pole.
        '''
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
            else:
                self.zmacknut = False
    def vlajka(self):
        '''
        Vykresní vlajku a otazník.
        '''
        mouse_pos = pg.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if pg.mouse.get_pressed()[2]:
                if self.otocen == False and self.vlajka_ == False and self.otaznik_ == False and not self.zmacka_vlajka: # zapne vlajku
                    self.vlajka_ = True
                    if not self.zmacka_vlajka:
                        self.zmacka_vlajka = True
                elif self.vlajka_ == True and not self.zmacka_vlajka: # zapne otazník
                    self.vlajka_ = False
                    self.otaznik_ = True
                    if not self.zmacka_vlajka:
                        self.zmacka_vlajka = True
                elif self.otaznik_ == True and not self.zmacka_vlajka: #vypne otazník
                    self.otaznik_ = False
                    if not self.zmacka_vlajka:
                        self.zmacka_vlajka = True
            else:
                self.zmacka_vlajka = False
    
class herni_plocha:
    '''
    Třída reprezentující celou herní plochu.
    ...
    Atributy
    --------
    resta_mina : list
        souřadnice pole, na kterém nebude mina
    '''
    def __init__(self, resta_mina = [-1, -1]):
        '''
        Vrací objekt třídy herni_plocha.
        ...
        Parametry
        ---------
        resta_mina : list
            souřadnice pole, na kterém nebude mina
        '''
        self.resta_mina = resta_mina
        for i in range(pocet):
            radek = []
            for j in range(pocet):
                k = random.random()
                if k < 0.85:
                    pol = pole(zacatek_pole+i*vel+i*5, zacatek_pole+j*vel+j*5, i, j, 0)
                else:
                    if i == self.resta_mina[0] and j == self.resta_mina[1]:
                        pol = pole(zacatek_pole+i*vel+i*5, zacatek_pole+j*vel+j*5, i, j, 0)
                    else:
                        pol = pole(zacatek_pole+i*vel+i*5, zacatek_pole+j*vel+j*5, i, j, -1)
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
        '''
        Vytvoří vlnu volných políček po kliknutí.
        ...
        Parametry
        ---------
        obj : pole
        '''
        obj_x = obj.souradnice_x
        obj_y = obj.souradnice_y
        if plocha_[obj_x][obj_y].otocen == False:
            if obj.miny_okolo != -1:
                for i in range(-1, 2):
                    if obj.souradnice_x + i >= 0 and obj.souradnice_x + i < pocet:
                        for j in range(-1, 2):
                            if obj.souradnice_y + j >= 0 and obj.souradnice_y + j < pocet:
                                if plocha_[obj_x+i][obj_y+j].otocen == True and plocha_[obj_x+i][obj_y+j].miny_okolo > -1:
                                    if plocha_[obj_x+i][obj_y+j].miny_okolo == 0:
                                        obj.otocen = True

def mainloop():
    '''
    Funkce reprezentující hlavní hrací smyčku.
    '''
    global okno
    global vel_okna
    global start
    global stav_hry
    global plocha_
    global objects
    global hry
    global pocet
    global obtiznost
    global zacatek_pole
    global plocha
    okno.fill((38, 13, 52))
    hrat_znova(0)

    a = True
    run = True
    prohra = False
    vyhra = False
    while run:
        pg.time.delay(50)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
        if prohra or vyhra or start == False:
            e = False
            if obtiznost == 'easy':
                pocet = 8
                e = True
            if obtiznost == 'medium':
                pocet = 12
                e = True
            if obtiznost == 'hard':
                pocet = 16
                e = True
            if obtiznost == 'konec':
                run = False
                a = False
            if e == True:
                obtiznost = 'nic'
                plocha_ = []
                objects = []
                hry = []
                start = False
                stav_hry = 0
                zacatek_pole = (vel_okna/2)-((vel*(pocet)+(pocet-1)*5)/2)
                plocha = herni_plocha()
                mainloop()
        if not prohra and not vyhra:
            if obtiznost == 'easy' or obtiznost == 'medium' or obtiznost == 'hard' or obtiznost == 'konec':
                obtiznost = 'nic'
        if pg.mouse.get_pressed()[0] and start == False and stav_hry == -1:         # první neni mina
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
            stav_hry = 1
            a = True            
        stav_hry = 1
        for object in objects:                                                      # průchod přes všechny pole
            if a:                                                                   # funkce u polí proběhnou pouze běhěm hry
                object.grafika()
                object.otocit() 
                object.vlajka()
                plocha.vlna(object)
            if stav_hry == -1 and start == True:                                    # odkrytí všech min po přohře
                if object.miny_okolo == -1 or object.miny_okolo == -2:
                    object.otocen = True
                    object.grafika()
            if object.miny_okolo != -1:                                             # smyčka vyhodnocující stav_hry
                if object.otocen == False:
                    if stav_hry != -1:
                        stav_hry = 0
            if stav_hry == 0:
                continue
        if stav_hry == -1 and start == True:                                        # prohra
            a = False
            prohra = True
            hrat_znova(-1)
        if stav_hry == 1 and start == True:                                         # výhra
            a = False
            vyhra = True
            hrat_znova(1)
        for x in hry:                                                               # grafika hracího menu
            if stav_hry != 0:
                x.grafika()
            x.easy.zmacknout()
            x.medium.zmacknout()
            x.hard.zmacknout()
            x.konec.zmacknout()
        
        pg.display.update()
        cas.tick(32)

mainloop()
pg.quit()
