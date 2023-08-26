



import random
import pygame as pyg
import time
import sys




WIDTH = 1350
HEIGHT = 900
TICK_RATE = 500 #low is faster ticks
POL_CAP = 5000

tab = 0 #count for which tab we are currently on (0-3)
ticks = 0
WIN = pyg.display.set_mode((WIDTH, HEIGHT))
pyg.display.set_caption("Meltdown")
pyg.display.set_icon(pyg.image.load("assets/img/icon.png"))


# Tab buttons (x, y, width, height)
tab1_rect = pyg.Rect(0, 0.675 * HEIGHT, WIDTH*0.25, HEIGHT*0.048)
tab2_rect = pyg.Rect(WIDTH*0.25, 0.675 * HEIGHT, WIDTH*0.25, HEIGHT*0.048)
tab3_rect = pyg.Rect(WIDTH*0.5, 0.675 * HEIGHT, WIDTH*0.25, HEIGHT*0.048)
tab4_rect = pyg.Rect(WIDTH*0.75, 0.675 * HEIGHT, WIDTH*0.25, HEIGHT*0.048)

#expansion buttons
exp_prov_rect = pyg.Rect(WIDTH*0.05, HEIGHT*0.78, WIDTH*0.1, WIDTH*0.1)
exp_nat_rect = pyg.Rect(WIDTH*0.20, HEIGHT*0.78, WIDTH*0.1, WIDTH*0.1)
exp_con_rect = pyg.Rect(WIDTH*0.35, HEIGHT*0.78, WIDTH*0.1, WIDTH*0.1)
exp_glo_rect = pyg.Rect(WIDTH*0.50, HEIGHT*0.78, WIDTH*0.1, WIDTH*0.1)

#the bar covering the pollution img (to hide progress ig)
pol_bar_rect = pyg.Rect(WIDTH*0.025, HEIGHT*0.1233, WIDTH*0.045, HEIGHT*0.415)

pol_amt = 0.0 # tracks pollution amt
money_amt = 0.0 # tracks money amt
pub_amt = POL_CAP - pol_amt #public satisfaction is inverse pollution 

pol_rate = 0.1
money_rate = 0.15

upgrade_track = [0, 0, 0]
upgrade_costs = [
    [40, 100, 540, 1200]
]
news_queue = []

def imgImport(name, w, h, rot=0):
    return pyg.transform.rotate(pyg.transform.scale(pyg.image.load("assets/img/" + name), (w, h)), rot)

EPOCH = time.time() * 1000
BACKIMG = imgImport("background_img.png", WIDTH, HEIGHT)

#(PARTO) my additions coming in, trying to mess with opacity
WORLDWATER = imgImport("water_1.png", int(WIDTH*0.8), int(HEIGHT*0.58)).convert_alpha()
alpha = 100
WORLDWATERPOLLUTION = imgImport("water_p_1.png", int(WIDTH*0.8), int(HEIGHT*0.58)).convert_alpha()
alpha_Water =100 # IF THIS VALUE GETS HIGHER THE WATER GETS MORE POLLUTED (VALUE GOES TO 255 MAX)

WORLD = imgImport("world.png", int(WIDTH*0.8), int(HEIGHT*0.58))
TAB1 = imgImport("tab1.png", WIDTH, 0.35*HEIGHT)
TAB2 = imgImport("tab2.png", WIDTH, 0.35*HEIGHT)
TAB3 = imgImport("tab3.png", WIDTH, 0.35*HEIGHT)
TAB4 = imgImport("tab4.png", WIDTH, 0.35*HEIGHT)
POL_BAR = imgImport("pol_bar.png", WIDTH*0.05, HEIGHT*0.5)
NEWS_BOX = imgImport("news.png", WIDTH*.16, HEIGHT*.28)
ACTIVE_INT = imgImport("activist.png", WIDTH*0.4, HEIGHT*0.4) #pop up


exp_prov = imgImport("buttons/exp_prov.png", WIDTH*0.1, WIDTH*0.1)
exp_nat = imgImport("buttons/exp_nat.png", WIDTH*0.1, WIDTH*0.1)
exp_con = imgImport("buttons/exp_con.png", WIDTH*0.1, WIDTH*0.1)
exp_glo = imgImport("buttons/exp_glo.png", WIDTH*0.1, WIDTH*0.1)
lock = imgImport("buttons/lock.png", WIDTH*0.1, WIDTH*0.1)
buy = imgImport("buttons/buy.png", WIDTH*0.1, WIDTH*0.1)
activ_bttn = imgImport("buttons/activ_bttn.png", WIDTH*0.1, HEIGHT*0.05)

popup = False
activ_rect = activ_bttn.get_rect(topleft=(0.615*WIDTH, 0.54*HEIGHT)) #sets a rectangle over image that will be used for collision detec for button

pyg.font.init()
doc_font = pyg.font.Font("assets/fonts/ShareTech.ttf", 16)



def time_passed():
    return int(time.time() * 1000 - EPOCH)

def draw_text(text, x, y, color):
    ##print(str(x) +  " " + str(y))
    img = doc_font.render(text, True, color)
    WIN.blit(img, (x, y))

def not_enough(required, current):
    print('not enough')

          

activ_int = 1000*120 #1 second x 120, every 2 minutes it'll run the chance of event
 
activ_count = 1

def activ_inter():
    global activ_int
    global activ_count
    if time_passed >= activ_int*activ_count:
        activ_count+= 1
        activ_prob()
        


def activ_prob():
   prob = random.randint(1,100) #the numbers represent the % chance of event happening 
   if pub_amt < 500 & prob <=30:
        gen_pop()
        popup = True
   elif pub_amt < 1500 & prob <=25:
       gen_pop() 
       popup = True
   elif pub_amt < 2500 & prob <=20:
       gen_pop()
       popup = True
   elif pub_amt < 3500 & prob <=15:
       gen_pop()
       popup = True
   elif pub_amt < 5000 & prob <=10:
       gen_pop()
       popup = True
        

     

def gen_pop():

    global money_amt
    global pub_amt
    global pol_amt

    type = random.randint(1,3)
    if type == 1:
        pub_prob = random.randint(10,40)
        pub_loss = (pub_prob/100)(pub_amt)
        pub_amt =- pub_loss
        activ_group = ['WeLoveLiving, StayGreen, ReduceReuseRefute, FightingCorpGreed, AreYouProud?']
        list1_num = random.randint(1,5)
        text = 'ACTIVIST INTERFERENCE: ' + activ_group[list1_num] + '  organization holds protests lasting 3 days, \n widespread public awareness campaign (Public Satisfaction down by: ' + pub_loss + ")"
        draw_text(text, 0.4*WIDTH, 0.32*HEIGHT, (255,255,255))
    if type ==2: 
        mon_prob = random.randint(20,60)
        money_loss = (mon_prob/100)(money_amt) #why isn't this registering 
        money_amt =- money_loss
        activists = ['Public', 'Workers Union', 'Charity Group']
        list2_num = random.randint(1,3)
        text = 'ACTIVIST INTERFERENCE: ' + activists[list2_num] + ' *Company* for $' + money_loss
        draw_text(text, 0.4*WIDTH, 0.32*HEIGHT, (255,255,255))
    if type ==3: 
        pol_prob = random.randint(10,30)
        pol_loss = (pol_prob/100)(pol_amt) #why isn't this registering 
        pol_amt =- pol_loss
        nerds = ['Child Prodigie invents new', 'Scientists improve', 'That one kid everyone knew was going to Harvard creates', 'Your archnemis spitefully makes a']
        list3_num = random.randint(1,3)
        text = ' Breaking News: ' + nerds[list3_num] + ' new carbon dioxide reversal tool that can aid in combating air pollution!\n (Pollution down by:' + pol_loss + ")"
        draw_text(text, 0.4*WIDTH, 0.32*HEIGHT, (255,255,255))

def draw():
    
    print(time_passed())

    #WIN.fill((0, 0, 0))
    WIN.blit(BACKIMG, (0, 0)) #putting images at coordinates (origin top left)
    WIN.blit(WORLD, (WIDTH*0.18, HEIGHT*0.05))
    WIN.blit(WORLDWATER, (WIDTH*0.18, HEIGHT*0.05)) #draw the water background 
    WIN.blit(WORLDWATERPOLLUTION, (WIDTH*0.18, HEIGHT*0.05)) #draw the water background green
    WIN.blit(NEWS_BOX, (0.12*WIDTH, 0.3*HEIGHT))
    #Popup
    #print(popup)
    if popup == True: 
        WIN.blit(ACTIVE_INT, (0.32*WIDTH, 0.2*HEIGHT))

        WIN.blit(activ_bttn, (0.615*WIDTH, 0.54*HEIGHT))
        gen_pop() #ELIMATE AFTER TESTING
        

    

    #tabs
    match tab:
        case 0: #expansion buttons
            
            exp_prov_rect = pyg.Rect(WIDTH*0.05, HEIGHT*0.78, WIDTH*0.1, WIDTH*0.1)
            exp_nat_rect = pyg.Rect(WIDTH*0.20, HEIGHT*0.78, WIDTH*0.1, WIDTH*0.1)
            exp_con_rect = pyg.Rect(WIDTH*0.35, HEIGHT*0.78, WIDTH*0.1, WIDTH*0.1)
            exp_glo_rect = pyg.Rect(WIDTH*0.50, HEIGHT*0.78, WIDTH*0.1, WIDTH*0.1) 

            WIN.blit(TAB1, (0, HEIGHT*0.65))
            WIN.blit(exp_prov, (WIDTH*0.05, HEIGHT*0.78))
            WIN.blit(exp_nat, (WIDTH*0.20, HEIGHT*0.78))
            WIN.blit(exp_con, (WIDTH*0.35, HEIGHT*0.78))
            WIN.blit(exp_glo, (WIDTH*0.50, HEIGHT*0.78))
            
            if(upgrade_track[0] < 1):
                WIN.blit(lock, (WIDTH*0.20, HEIGHT*0.78))
            if(upgrade_track[0] < 2):
                WIN.blit(lock, (WIDTH*0.35, HEIGHT*0.78))
            if(upgrade_track[0] < 3):
                WIN.blit(lock, (WIDTH*0.50, HEIGHT*0.78))
            
            if(upgrade_track[0] > 0):
                WIN.blit(buy, (WIDTH*0.05, HEIGHT*0.78))
            if(upgrade_track[0] > 1):
                WIN.blit(buy, (WIDTH*0.20, HEIGHT*0.78))
            if(upgrade_track[0] > 2):
                WIN.blit(buy, (WIDTH*0.35, HEIGHT*0.78))
            
            
            ###print("1")
        case 1:
            WIN.blit(TAB2, (0, HEIGHT*0.65))
        
        case 2:
            WIN.blit(TAB3, (0, HEIGHT*0.65))
        
        case 3:
            WIN.blit(TAB4, (0, HEIGHT*0.65))

    # pollution bar
    WIN.blit(POL_BAR, (WIDTH*0.03, HEIGHT*0.08))            
    pyg.draw.rect(WIN, (96, 107, 94), pyg.Rect(WIDTH*0.035, HEIGHT*0.1533, WIDTH*0.045, HEIGHT*0.415*(1 - pol_amt/POL_CAP)))

    # balance text
    draw_text(("Balance: $" + f"{round(money_amt, 2):,}" + "K " ), WIDTH*0.01, HEIGHT*0.04, (200, 200, 200))
    pyg.display.update()

def pol_tick():
    global pol_amt
    pol_amt += pol_rate

def money_tick():
    global money_amt
    money_amt += money_rate

def main():
    global tab, ticks, pol_rate, money_rate, pol_amt, money_amt, upgrade_track, alpha_Water, popup
    #clock = pyg.time.Clock() #controlls fps and whatnot
    pyg.mouse.set_cursor(pyg.cursors.diamond)
    
     

    run = True
    
    # game loop. this will be active to run the game
    pyg.init()
    while run:
        #clock.tick(FPS) #again, controls fps 
        #print(time_passed())
        #print(money_rate)
        

        if(int(time_passed()/TICK_RATE) > ticks):
            ticks += 1
            pol_tick()
            money_tick()
            print("--------")
            

        activ_inter() #I DON"T KNOW WHERE TO PUT THIS 
        
        for event in pyg.event.get():
            if event.type == pyg.QUIT: run = False

            if event.type == pyg.MOUSEBUTTONDOWN:
                if event.button == 1: #left/primary click
                    mx, my = pyg.mouse.get_pos()
                    if activ_rect.collidepoint(mx, my):
          
                        if pyg.mouse.get_pressed()[0] == 1:
                            print("Clicked")
                            popup=False
                            print(popup)
                    if tab1_rect.collidepoint(mx, my) and tab != 0:
                        #money_tick(5)
                        #print("clicked1")
                        tab = 0
                        #print(tab)

                    elif tab2_rect.collidepoint(mx, my) and tab != 1:
                        #money_tick(10000)
                        #print("clicked2")
                        tab = 1
                        #print(tab)
                    
                    elif tab3_rect.collidepoint(mx, my) and tab != 2:
                        #money_tick(5)
                        #print("clicked3")
                        tab = 2
                        #print(tab)
                    
                    elif tab4_rect.collidepoint(mx, my) and tab != 3:
                        #money_tick(5)
                        #print("clicked4")
                        tab = 3
                        #print(tab)
                    elif tab == 0:
                        if upgrade_track[0] == 4:
                            print("no dice")
                        elif exp_prov_rect.collidepoint(mx, my) and upgrade_track[0] == 0:
                            if(money_amt < upgrade_costs[0][0]):
                                not_enough(upgrade_costs[0][0], money_amt)
                                continue
                            money_amt -= upgrade_costs[0][0]
                            money_rate += 0.083
                            pol_rate += 0.1
                            upgrade_track[0] += 1
                        elif exp_nat_rect.collidepoint(mx, my) and upgrade_track[0] == 1:
                            if(money_amt < upgrade_costs[0][1]):
                                not_enough(upgrade_costs[0][1], money_amt)
                                continue
                            money_amt -= upgrade_costs[0][1]
                            money_rate += 0.125
                            pol_rate += 0.1
                            upgrade_track[0] += 1
                        elif exp_con_rect.collidepoint(mx, my) and upgrade_track[0] == 2:
                            if(money_amt < upgrade_costs[0][2]):
                                not_enough(upgrade_costs[0][2], money_amt)
                                continue
                            money_amt -= upgrade_costs[0][2]
                            money_rate += 0.2
                            pol_rate += 0.1
                            upgrade_track[0] += 1
                        elif exp_glo_rect.collidepoint(mx, my) and upgrade_track[0] == 3:
                            if(money_amt < upgrade_costs[0][3]):
                                not_enough(upgrade_costs[0][3], money_amt)
                                continue
                            money_amt -= upgrade_costs[0][3]
                            money_rate += 0.541
                            pol_rate += 0.1
                            upgrade_track[0] += 1



        keys_pressed = pyg.key.get_pressed()
        


        # game is over

        ##print(pol_amt)
        
        WORLDWATERPOLLUTION.set_alpha(alpha_Water) #opacityyy 
        WORLDWATER.set_alpha(alpha)

        draw()
        #updates display. display wont change if this isnt here
        pyg.display.update()
    pyg.quit()

# dont touch this; if u have question abt it dm jaden
if __name__ == "__main__":
    main()