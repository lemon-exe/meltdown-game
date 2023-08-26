



import pygame as pyg
import sys




WIDTH = 900
HEIGHT = 600
FPS = 144

tab = 0 #count for which tab we are currently on (0-3)
WIN = pyg.display.set_mode((WIDTH, HEIGHT))
pyg.display.set_caption("Meltdown")
pyg.display.set_icon(pyg.image.load("assets/img/icon.png"))


# Tab buttons (x, y, width, height)
tab1_rect = pyg.Rect(0, 0.675 * HEIGHT, WIDTH*0.25, HEIGHT/24)
tab2_rect = pyg.Rect(WIDTH*0.25, 0.675 * HEIGHT, WIDTH*0.25, HEIGHT/24)
tab3_rect = pyg.Rect(WIDTH*0.5, 0.675 * HEIGHT, WIDTH*0.25, HEIGHT/24)
tab4_rect = pyg.Rect(WIDTH*0.75, 0.675 * HEIGHT, WIDTH*0.25, HEIGHT/24)

#the bar covering the pollution img (to hide progress ig)
pol_bar_rect = pyg.Rect(WIDTH*0.025, HEIGHT*0.1233, WIDTH*0.045, HEIGHT*0.415)

pol_amt = 0.0 # tracks pollution amt
money_amt = 0 # tracks money amt

def imgImport(name, w, h, rot=0):
    return pyg.transform.rotate(pyg.transform.scale(pyg.image.load("assets/img/" + name), (w, h)), rot)

BACKIMG = imgImport("background_img.png", WIDTH, HEIGHT) 
WORLD = imgImport("world.png", int(WIDTH*0.8), int(HEIGHT*0.58))
TAB1 = imgImport("tab1.png", WIDTH, 0.35*HEIGHT)
TAB2 = imgImport("tab2.png", WIDTH, 0.35*HEIGHT)
TAB3 = imgImport("tab3.png", WIDTH, 0.35*HEIGHT)
TAB4 = imgImport("tab4.png", WIDTH, 0.35*HEIGHT)
POL_BAR = imgImport("pol_bar.png", WIDTH*0.05, HEIGHT*0.5)



pyg.font.init()
doc_font = pyg.font.Font("assets/fonts/ShareTech.ttf", 16)

def draw_text(text, x, y, color):
    ##print(str(x) +  " " + str(y))
    img = doc_font.render(text, True, color)
    WIN.blit(img, (x, y))

def draw():
    

    #WIN.fill((0, 0, 0))
    WIN.blit(BACKIMG, (0, 0)) #putting images at coordinates (origin top left)
    WIN.blit(WORLD, (WIDTH*0.18, HEIGHT*0.05))
    
    """ pyg.draw.rect(WIN, (50, 50, 50), tab1_rect)
    pyg.draw.rect(WIN, (100, 100, 100), tab2_rect)
    pyg.draw.rect(WIN, (150, 150, 150), tab3_rect)
    pyg.draw.rect(WIN, (200, 200, 200), tab4_rect) """

    #tabs
    match tab:
        case 0:
            WIN.blit(TAB1, (0, HEIGHT*0.65))

            ###print("1")
        case 1:
            WIN.blit(TAB2, (0, HEIGHT*0.65))
        
        case 2:
            WIN.blit(TAB3, (0, HEIGHT*0.65))
        
        case 3:
            WIN.blit(TAB4, (0, HEIGHT*0.65))

    # pollution bar
    WIN.blit(POL_BAR, (WIDTH*0.03, HEIGHT*0.08))            
    pyg.draw.rect(WIN, (96, 107, 94), pyg.Rect(WIDTH*0.035, HEIGHT*0.1533, WIDTH*0.045, HEIGHT*0.415*(1 - pol_amt/1)))

    # balance text
    draw_text(("Balance: $" + f"{money_amt:,}" + " " ), WIDTH*0.01, HEIGHT*0.04, (200, 200, 200))
    pyg.display.update()

def pol_tick():
    global pol_amt
    pol_amt += 0.01

def money_tick(amt):
    global money_amt
    money_amt += amt

def main():
    global tab
    clock = pyg.time.Clock() #controlls fps and whatnot
    pyg.mouse.set_cursor(pyg.cursors.diamond)
    
     

    run = True
    #thing to start the
    Start = False
    # game loop. this will be active to run the game
    pyg.init()
    


    
    while run == True:
        clock.tick(FPS) #again, controls fps 
        

        if(int(pyg.time.get_ticks()) % 50 == 0):
            pol_tick()
            money_tick(2)
            ##print("--------")
            

        
        
        for event in pyg.event.get():
            if event.type == pyg.QUIT: run = False
            mx, my = pyg.mouse.get_pos()

            if event.type == pyg.MOUSEBUTTONDOWN:
                if event.button == 1: #left/primary click
                    
                    if tab1_rect.collidepoint(mx, my) and tab != 0:
                        money_tick(5)
                        #print("clicked1")
                        tab = 0
                        #print(tab)

                    elif tab2_rect.collidepoint(mx, my) and tab != 1:
                        money_tick(10000)
                        #print("clicked2")
                        tab = 1
                        #print(tab)
                    
                    elif tab3_rect.collidepoint(mx, my) and tab != 2:
                        money_tick(5)
                        #print("clicked3")
                        tab = 2
                        #print(tab)
                    
                    elif tab4_rect.collidepoint(mx, my) and tab != 3:
                        money_tick(5)
                        #print("clicked4")
                        tab = 3
                        #print(tab)
        keys_pressed = pyg.key.get_pressed()


        # game is over

        ##print(pol_amt)
        


        draw()
        #updates display. display wont change if this isnt here
        pyg.display.update()
    pyg.quit()

# dont touch this; if u have question abt it dm jaden
if __name__ == "__main__":
    main()