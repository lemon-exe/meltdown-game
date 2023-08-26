import pygame as pyg
import time
import random


from pygame import mixer
  


WIDTH = 1080
HEIGHT = 720
TICK_RATE = 500 #low is faster tjicks
POL_CAP = 5000
EPOCH = time.time() * 1000


def imgImport(name, w, h, rot=0):
    return pyg.transform.rotate(pyg.transform.scale(pyg.image.load("dist/assets/img/" + name), (w, h)), rot)


company_name = ""
popup = False
tab = 0 #count for which tab we are currently on (0-3)
ticks = 0
warn_time = [0, 0, 1, -1] #[time, have, required, tab] 
warn = {
    "time":0,
    "had":0,
    "req":1,
    "tab":-1
}
activ_int = 1000*120 #1 second x 120, every 2 minutes it'll run the chance of event
game_state = 0

pol_amt = 0.0 # tracks pollution amt
money_amt = 10.0 # tracks money amt


pol_rate = 1 #.5
money_rate = 10 #.15
pub_amt = pol_rate/5.0
pub_rate = 1.0
disc_rate = 1.0

upgrade_track = [0, 0, 0, 0]
base_costs = [
    [40, 100, 540, 1200],
    [10, 200, 1150, 1900],
    [12, 24, 36, 50],
    [50, 150, 220, 400]
]
upgrade_costs = [
    [40, 100, 540, 1200],
    [10, 200, 1150, 1900],
    [12, 24, 36, 50],
    [50, 150, 220, 400]
]
popup_info = {
    "type": -1, # 0, 1 or 2
    "name": "group name",
    "amt": -1 #amt deduction for wtv
}


WIN = pyg.display.set_mode((WIDTH, HEIGHT))
pyg.display.set_caption("Meltdown")
pyg.display.set_icon(pyg.image.load("dist/assets/img/icon.png"))


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

#product buttons
pro_1_rect = pyg.Rect(WIDTH*0.05, HEIGHT*0.78, WIDTH*0.1, WIDTH*0.1)
pro_2_rect = pyg.Rect(WIDTH*0.20, HEIGHT*0.78, WIDTH*0.1, WIDTH*0.1)
pro_3_rect = pyg.Rect(WIDTH*0.35, HEIGHT*0.78, WIDTH*0.1, WIDTH*0.1)
pro_4_rect = pyg.Rect(WIDTH*0.50, HEIGHT*0.78, WIDTH*0.1, WIDTH*0.1)

#propoganda buttons
pr_pro_1_rect = pyg.Rect(WIDTH*0.05, HEIGHT*0.75, WIDTH*0.1, WIDTH*0.05)
pr_pro_2_rect = pyg.Rect(WIDTH*0.20, HEIGHT*0.75, WIDTH*0.1, WIDTH*0.05)
pr_pro_3_rect = pyg.Rect(WIDTH*0.35, HEIGHT*0.75, WIDTH*0.1, WIDTH*0.05)
pr_pro_4_rect = pyg.Rect(WIDTH*0.50, HEIGHT*0.75, WIDTH*0.1, WIDTH*0.05)

#lobbying buttons
pr_lob_1_rect = pyg.Rect(WIDTH*0.05, HEIGHT*0.85, WIDTH*0.1, WIDTH*0.05)
pr_lob_2_rect = pyg.Rect(WIDTH*0.20, HEIGHT*0.85, WIDTH*0.1, WIDTH*0.05)
pr_lob_3_rect = pyg.Rect(WIDTH*0.35, HEIGHT*0.85, WIDTH*0.1, WIDTH*0.05)
pr_lob_4_rect = pyg.Rect(WIDTH*0.50, HEIGHT*0.85, WIDTH*0.1, WIDTH*0.05)


activ_bttn = imgImport("buttons/activ_bttn.png", WIDTH*0.1, HEIGHT*0.05)


activ_rect = activ_bttn.get_rect(topleft=(0.71*WIDTH, 0.38*HEIGHT))

#the bar covering the pollution img (to hide progress ig)
#pol_bar_rect = pyg.Rect(WIDTH*0.025, HEIGHT*0.1223, WIDTH*0.045, HEIGHT*0.415)


BACKIMG = imgImport("background_img.png", WIDTH, HEIGHT)

#(PARTO) my additions coming in, trying to mess with opacity
WORLDWATER = imgImport("water_1.png", int(WIDTH*0.8), int(HEIGHT*0.58)).convert_alpha()
alpha = 255
WORLDWATERPOLLUTION = imgImport("water_p_1.png", int(WIDTH*0.8), int(HEIGHT*0.58)).convert_alpha()
alpha_Water = 0 # IF THIS VALUE GETS HIGHER THE WATER GETS MORE POLLUTED (VALUE GOES TO 255 MAX)

WORLD = imgImport("world.png", int(WIDTH*0.8), int(HEIGHT*0.58))
ol1 = imgImport("overlays/prov_map.png", int(WIDTH*0.8), int(HEIGHT*0.58))
ol2 = imgImport("overlays/nat_map.png", int(WIDTH*0.8), int(HEIGHT*0.58))
ol3 = imgImport("overlays/cont_map.png", int(WIDTH*0.8), int(HEIGHT*0.58))
ol4 = imgImport("overlays/world_map.png", int(WIDTH*0.8), int(HEIGHT*0.58))

TAB1 = imgImport("tab1.png", WIDTH, 0.35*HEIGHT)
TAB2 = imgImport("tab2.png", WIDTH, 0.35*HEIGHT)
TAB3 = imgImport("tab3.png", WIDTH, 0.35*HEIGHT)
TAB4 = imgImport("tab4.png", WIDTH, 0.35*HEIGHT)
POL_BAR = imgImport("pol_bar.png", WIDTH*0.05, HEIGHT*0.5)
NEWS_BOX = imgImport("news.png", WIDTH*.16, HEIGHT*.28)
ACTIVE_INT = imgImport("Act_popup.png", WIDTH*0.5, HEIGHT*0.25) #activists pop-up



lock = imgImport("buttons/lock.png", WIDTH*0.1, WIDTH*0.1)
buy = imgImport("buttons/buy.png", WIDTH*0.1, WIDTH*0.1)
lock_half = imgImport("buttons/lock_half.png", WIDTH*0.1, WIDTH*0.05)
buy_half = imgImport("buttons/buy_half.png", WIDTH*0.1, WIDTH*0.05)

exp_prov = imgImport("buttons/exp/exp_prov.png", WIDTH*0.1, WIDTH*0.1)
exp_nat = imgImport("buttons/exp/exp_nat.png", WIDTH*0.1, WIDTH*0.1)
exp_con = imgImport("buttons/exp/exp_con.png", WIDTH*0.1, WIDTH*0.1)
exp_glo = imgImport("buttons/exp/exp_glo.png", WIDTH*0.1, WIDTH*0.1)

pro_1 = imgImport("buttons/pro/pro_1.png", WIDTH*0.1, WIDTH*0.1)
pro_2 = imgImport("buttons/pro/pro_2.png", WIDTH*0.1, WIDTH*0.1)
pro_3 = imgImport("buttons/pro/pro_3.png", WIDTH*0.1, WIDTH*0.1)
pro_4 = imgImport("buttons/pro/pro_4.png", WIDTH*0.1, WIDTH*0.1)

pr_pro_1 = imgImport("buttons/pr/pr_pro_1.png", WIDTH*0.1, WIDTH*0.05)
pr_pro_2 = imgImport("buttons/pr/pr_pro_2.png", WIDTH*0.1, WIDTH*0.05)
pr_pro_3 = imgImport("buttons/pr/pr_pro_3.png", WIDTH*0.1, WIDTH*0.05)
pr_pro_4 = imgImport("buttons/pr/pr_pro_4.png", WIDTH*0.1, WIDTH*0.05)

pr_lob_1 = imgImport("buttons/pr/pr_lob_1.png", WIDTH*0.1, WIDTH*0.05)
pr_lob_2 = imgImport("buttons/pr/pr_lob_2.png", WIDTH*0.1, WIDTH*0.05)
pr_lob_3 = imgImport("buttons/pr/pr_lob_3.png", WIDTH*0.1, WIDTH*0.05)
pr_lob_4 = imgImport("buttons/pr/pr_lob_4.png", WIDTH*0.1, WIDTH*0.05)

#expansion descriptions
exp_prov_des = imgImport("buttons/exp/exp_prov_des.png", WIDTH*0.12, WIDTH*0.12)
exp_nat_des = imgImport("buttons/exp/exp_nat_des.png", WIDTH*0.12, WIDTH*0.12)
exp_con_des = imgImport("buttons/exp/exp_con_des.png", WIDTH*0.12, WIDTH*0.12)
exp_glo_des = imgImport("buttons/exp/exp_glo_des.png", WIDTH*0.12, WIDTH*0.12)

#product descriptions
pro_1_des = imgImport("buttons/pro/pro_1_des.png", WIDTH*0.12, WIDTH*0.12)
pro_2_des = imgImport("buttons/pro/pro_2_des.png", WIDTH*0.12, WIDTH*0.12)
pro_3_des = imgImport("buttons/pro/pro_3_des.png", WIDTH*0.12, WIDTH*0.12)
pro_4_des = imgImport("buttons/pro/pro_4_des.png", WIDTH*0.12, WIDTH*0.12)

#pr propoganda des
pr_pro_1_des = imgImport("buttons/pr/pr_pro_1_des.png", WIDTH*0.12, WIDTH*0.12)
pr_pro_2_des = imgImport("buttons/pr/pr_pro_2_des.png", WIDTH*0.12, WIDTH*0.12)
pr_pro_3_des = imgImport("buttons/pr/pr_pro_3_des.png", WIDTH*0.12, WIDTH*0.12)
pr_pro_4_des = imgImport("buttons/pr/pr_pro_4_des.png", WIDTH*0.12, WIDTH*0.12)

#pr lobbying des
pr_lob_1_des = imgImport("buttons/pr/pr_lob_1_des.png", WIDTH*0.12, WIDTH*0.12)
pr_lob_2_des = imgImport("buttons/pr/pr_lob_2_des.png", WIDTH*0.12, WIDTH*0.12)
pr_lob_3_des = imgImport("buttons/pr/pr_lob_3_des.png", WIDTH*0.12, WIDTH*0.12)
pr_lob_4_des = imgImport("buttons/pr/pr_lob_4_des.png", WIDTH*0.12, WIDTH*0.12)

vic_img = imgImport("victory.png", 0.683*WIDTH, 0.418*HEIGHT)
def_img = imgImport("defeat.png", 0.683*WIDTH, 0.418*HEIGHT)


pyg.font.init()
doc_font = pyg.font.Font("dist/assets/fonts/ShareTech.ttf", 15)
display_font = pyg.font.Font("dist/assets/fonts/ShareTech.ttf", 36)

def update_costs():
    global upgrade_costs
    for i in range(len(upgrade_costs)-1):
        for j in range(len(upgrade_costs[i])):
            upgrade_costs[i][j] = round(base_costs[i][j] * disc_rate, 2)

def time_passed():
    return int(time.time() * 1000 - EPOCH)

def draw_text(text, x, y, color, display=False):
    ##print(str(x) +  " " + str(y))
    img = ""
    if(display): img = display_font.render(text, True, color)
    else: img = doc_font.render(text, True, color)
    WIN.blit(img, (x, y))

def not_enough(required, current):
    warn["had"] = current
    warn['req'] = required
    print('not enough')



 
activ_count = 0.5  #messing with it

def activ_inter():
    global activ_int
    global activ_count
    if time_passed() >= activ_int*activ_count:
        print("acti")
        activ_count+= 0.5 #messing with it
        activ_prob()
        


def activ_prob():
   global popup
   prob = random.randint(1,100) #the numbers represent the % chance of event happening 
   print(prob, pub_amt)
   if prob <= (pub_amt*95 + 5)*pub_rate:
       init_act()
       popup=True
   
        
def pol_tick():
    global pol_amt
    pol_amt += pol_rate

def money_tick():
    global money_amt
    money_amt += money_rate
     

def init_act():
    global pol_amt, pub_amt, money_amt, popup_info

    type = random.randint(1,3)
    if type == 1:
        pub_prob = random.randint(10,40)
        pub_loss = (pub_prob/100)*(pub_amt)
        pub_amt -= pub_loss
        activ_group = ['WeLoveLiving', 'StayGreen', 'ReduceReuseRefute', 'FightingCorpGreed', 'AreYouProud?']
        list1_num = random.randint(0,4)
#        text = 'ACTIVIST INTERFERENCE: ' + activ_group[list1_num] + '  organization holds protests lasting 3 days, \n widespread public awareness campaign (Public Satisfaction down by: ' + str(round(pub_loss, 2)) + ")"
        popup_info["type"] = 0
        popup_info["name"] = activ_group[list1_num]
        popup_info["amt"] = round(pub_loss, 2)
        
        #draw_text(text, 0.4*WIDTH, 0.32*HEIGHT, (255,255,255))
        print("drawn1")

    elif type ==2: 
        mon_prob = random.randint(20,60)
        money_loss = (mon_prob/100)*(money_amt) #why isn't this registering 
        money_amt -= money_loss
        activists = ['Public', 'Workers Union', 'Charity Group']
        list2_num = random.randint(0,2)
        #text = 'ACTIVIST INTERFERENCE: ' + activists[list2_num] + ' *Company* for $' + str(money_loss)
        
        popup_info["type"] = 1
        popup_info["name"] = activists[list2_num]
        popup_info["amt"] = round(money_loss, 2)

        #draw_text(text, 0.4*WIDTH, 0.32*HEIGHT, (255,255,255))
        print("drawn2")

    elif type ==3: 
        pol_prob = random.randint(10,30)
        pol_loss = (pol_prob/100)*(pol_amt) #why isn't this registering 
        print("pol loss", pol_loss, pol_amt)
        pol_amt -= pol_loss
        nerds = ['Child Prodigie invents new', 'Scientists improve', 'That one Harvard kid', 'Your archnemis spitefully makes a']
        list3_num = random.randint(0,2)
        #text = ' Breaking News: ' + nerds[list3_num] + ' new carbon dioxide reversal tool that can aid in combating air pollution!\n (Pollution down by:' + str(round(pol_loss, 2)) + "ppm)"

        popup_info["type"] = 2
        popup_info['name'] = nerds[list3_num]
        popup_info['amt'] = round(pol_loss, 2)


        #draw_text(text, 0.4*WIDTH, 0.32*HEIGHT, (255,255,255))
        print("drawn3")
        


def gen_pop():
    text = ""
    text2 = ""
    if popup_info["type"] == 0:
        text = 'ACTIVIST INTERFERENCE: ' + popup_info["name"] + '  organization holds protests lasting'
        text2 = '3 days,  widespread public awareness campaign (Public Satisfaction down by: ' + str(popup_info["amt"]) + ")"

    elif popup_info["type"] == 1:
        text = 'ACTIVIST INTERFERENCE: ' + popup_info["name"] + ' sues ' + company_name + ' for $' + str(popup_info["amt"]) + "K."
    elif popup_info["type"] == 2:
        text = ' Breaking News: ' + popup_info["name"] + ' new carbon dioxide reversal tool '
        text2 = 'that can aid in combating air pollution! (Pollution down by:' + str(popup_info["amt"]) + "ppm)"


    draw_text(text, 0.34*WIDTH, 0.32*HEIGHT, (127, 224 , 164))
    draw_text(text2, 0.345*WIDTH, 0.35*HEIGHT, (127, 224 , 164))

def menu():
    Start = False
    global company_name
    play_x = 0.5
    play_y = 0.5
    anipos_x = 0
    anipos_y = 0
    up = True
    msavex = 0
    msavey = 0
    while Start == False:
        thisanimationwillworkisayso = False
        mx, my = pyg.mouse.get_pos()
        msavex = mx
        msavey = my
        menuBackground = imgImport("menu/menu_img.png", WIDTH, HEIGHT).convert()
        play = imgImport("menu/playButton.png", play_x*WIDTH, play_y*HEIGHT)
        play_rect = play.get_rect(topleft = (0.26*WIDTH, 0.695*HEIGHT))
        WIN.blit(menuBackground,(0, 0))
        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                pyg.quit()
                exit() 
            keys_pressed = pyg.key.get_pressed()
            
            if event.type == pyg.MOUSEBUTTONDOWN:
                if play_rect.collidepoint(msavex, msavey):
                    Start = True

            if keys_pressed[pyg.K_SPACE]:
                print ('uh')
                Start = True
            """
            if play_rect.collidepoint(msavex, msavey):
                if up == True:
                    play_x += 0.005
                    play_y += 0.005
                    anipos_x += 0.002*WIDTH
                    anipos_y += 0.001*HEIGHT
                    if play_x >= 0.55:
                        up = False
                    thisanimationwillworkisayso = True
                if up == False:
                    play_x -= 0.005
                    play_y -= 0.005
                    anipos_x -= 0.002*WIDTH
                    anipos_y -= 0.001*HEIGHT
                    if play_x <= 0.5:
                        up = True
                    thisanimationwillworkisayso = True
            
        #trying to get the animation working but idk anymore
        if thisanimationwillworkisayso == False:
                WIN.blit(play, (0.26*WIDTH, 0.695*HEIGHT))
        elif play_rect.collidepoint(msavex, msavey):
            WIN.blit(play, (0.26*WIDTH-anipos_x, 0.695*HEIGHT-anipos_y))"""
        pyg.display.update()

    #menu to select your name/ colony or whatever
    Start = False
    while Start == False:
        mousepos = pyg.mouse.get_pos()
        text_surface = display_font.render(company_name, None, (127, 224, 164))
        name_popup = imgImport('menu/nameEnter.png', 0.8*WIDTH, 0.8*HEIGHT)
        popupButton = imgImport('menu/menu_button.png', 0.2*WIDTH, 0.1*HEIGHT)
        popupButton_rect = popupButton.get_rect(topleft = (0.6*WIDTH, 0.8*HEIGHT))
        
        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                pyg.quit()
                exit() 
            keys_pressed = pyg.key.get_pressed()
            if keys_pressed[pyg.K_RETURN]:
                Start = True
            if event.type == pyg.KEYDOWN:
                company_name = company_name + pyg.key.name(event.key)
            if keys_pressed[pyg.K_BACKSPACE]:
                company_name = company_name.replace("backspace", "")
                company_name = company_name[:-1]
            company_name = company_name.replace("space", " ")
            company_name = company_name.replace("return", "")
            company_name = company_name.replace("caps lock", "")
            if popupButton_rect.collidepoint(mousepos)and event.type == pyg.MOUSEBUTTONDOWN:
                Start = True
        WIN.blit(name_popup, (0.1*WIDTH, 0.14*HEIGHT))
        #WIN.blit(popupButton, (0.48*WIDTH, 0.57*HEIGHT))
        WIN.blit(popupButton, (0.6*WIDTH, 0.8*HEIGHT))
        WIN.blit(text_surface, (0.1*WIDTH+90, 0.13*HEIGHT+180))
        pyg.display.update()

def victory():
    WIN.blit(BACKIMG, (0, 0)) #putting images at coordinates (origin top left)
    WIN.blit(vic_img, (0.158*WIDTH, 0.224*HEIGHT))
    pyg.display.update()

def defeat():
    WIN.blit(BACKIMG, (0, 0)) #putting images at coordinates (origin top left)
    WIN.blit(def_img, (0.158*WIDTH, 0.224*HEIGHT))
    pyg.display.update()

def draw():
    
    mx, my = pyg.mouse.get_pos()

    

    #WIN.fill((0, 0, 0))
    WIN.blit(BACKIMG, (0, 0)) #putting images at coordinates (origin top left)
    WIN.blit(WORLD, (WIDTH*0.18, HEIGHT*0.05))
    if upgrade_track[0] == 1:
        WIN.blit(ol1, (WIDTH*0.18, HEIGHT*0.05))
    elif upgrade_track[0] == 2:
        WIN.blit(ol2, (WIDTH*0.18, HEIGHT*0.05))
    elif upgrade_track[0] == 3:
        WIN.blit(ol3, (WIDTH*0.18, HEIGHT*0.05))
    elif upgrade_track[0] == 4:
        WIN.blit(ol4, (WIDTH*0.18, HEIGHT*0.05))
    WIN.blit(WORLDWATER, (WIDTH*0.18, HEIGHT*0.05)) #draw the water background 
    WIN.blit(WORLDWATERPOLLUTION, (WIDTH*0.18, HEIGHT*0.05)) #draw the water background green
    #WIN.blit(NEWS_BOX, (0.12*WIDTH, 0.3*HEIGHT))
    
    if popup == True: 
        WIN.blit(ACTIVE_INT, (0.32*WIDTH, 0.2*HEIGHT))

        WIN.blit(activ_bttn, (0.71*WIDTH, 0.38*HEIGHT))
        gen_pop() #ELIMATE AFTER TESTING

    
    #tabs
    match tab:
        case 0: #expansion buttons

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
            if(upgrade_track[0] > 3):
                WIN.blit(buy, (WIDTH*0.50, HEIGHT*0.78))
            
            # descriptions
            if (exp_prov_rect.collidepoint(mx, my)):
                WIN.blit(exp_prov_des, (WIDTH*0.04, HEIGHT*0.6))
            elif exp_nat_rect.collidepoint(mx, my) and upgrade_track[0] > 0:
                WIN.blit(exp_nat_des, (WIDTH*0.19, HEIGHT*0.6))
            elif exp_con_rect.collidepoint(mx, my) and upgrade_track[0] > 1:
                WIN.blit(exp_con_des, (WIDTH*0.34, HEIGHT*0.6))
            elif exp_glo_rect.collidepoint(mx, my) and upgrade_track[0] > 2:
                WIN.blit(exp_glo_des, (WIDTH*0.49, HEIGHT*0.6))

            
            ###print("1")
        case 1:
            WIN.blit(TAB2, (0, HEIGHT*0.65))

            WIN.blit(pro_1, (WIDTH*0.05, HEIGHT*0.78))
            WIN.blit(pro_2, (WIDTH*0.20, HEIGHT*0.78))
            WIN.blit(pro_3, (WIDTH*0.35, HEIGHT*0.78))
            WIN.blit(pro_4, (WIDTH*0.50, HEIGHT*0.78))
            
            if(upgrade_track[1] < 1):
                WIN.blit(lock, (WIDTH*0.20, HEIGHT*0.78))
            if(upgrade_track[1] < 2):
                WIN.blit(lock, (WIDTH*0.35, HEIGHT*0.78))
            if(upgrade_track[1] < 3):
                WIN.blit(lock, (WIDTH*0.50, HEIGHT*0.78))
            
            if(upgrade_track[1] > 0):
                WIN.blit(buy, (WIDTH*0.05, HEIGHT*0.78))
            if(upgrade_track[1] > 1):
                WIN.blit(buy, (WIDTH*0.20, HEIGHT*0.78))
            if(upgrade_track[1] > 2):
                WIN.blit(buy, (WIDTH*0.35, HEIGHT*0.78))
            if(upgrade_track[1] > 3):
                WIN.blit(buy, (WIDTH*0.50, HEIGHT*0.78))
            
            # descriptions
            if (pro_1_rect.collidepoint(mx, my)):
                WIN.blit(pro_1_des, (WIDTH*0.04, HEIGHT*0.6))
            elif pro_2_rect.collidepoint(mx, my) and upgrade_track[1] > 0:
                WIN.blit(pro_2_des, (WIDTH*0.19, HEIGHT*0.6))
            elif pro_3_rect.collidepoint(mx, my) and upgrade_track[1] > 1:
                WIN.blit(pro_3_des, (WIDTH*0.34, HEIGHT*0.6))
            elif pro_4_rect.collidepoint(mx, my) and upgrade_track[1] > 2:
                WIN.blit(pro_4_des, (WIDTH*0.49, HEIGHT*0.6))


        
        case 2:
            WIN.blit(TAB3, (0, HEIGHT*0.65))

            WIN.blit(pr_pro_1, (WIDTH*0.05, HEIGHT*0.75))
            WIN.blit(pr_pro_2, (WIDTH*0.20, HEIGHT*0.75))
            WIN.blit(pr_pro_3, (WIDTH*0.35, HEIGHT*0.75))
            WIN.blit(pr_pro_4, (WIDTH*0.50, HEIGHT*0.75))
            
            if(upgrade_track[2] < 1):
                WIN.blit(lock_half, (WIDTH*0.20, HEIGHT*0.75))
            if(upgrade_track[2] < 2):
                WIN.blit(lock_half, (WIDTH*0.35, HEIGHT*0.75))
            if(upgrade_track[2] < 3):
                WIN.blit(lock_half, (WIDTH*0.50, HEIGHT*0.75))
            
            if(upgrade_track[2] > 0):
                WIN.blit(buy_half, (WIDTH*0.05, HEIGHT*0.75))
            if(upgrade_track[2] > 1):
                WIN.blit(buy_half, (WIDTH*0.20, HEIGHT*0.75))
            if(upgrade_track[2] > 2):
                WIN.blit(buy_half, (WIDTH*0.35, HEIGHT*0.75))
            if(upgrade_track[2] > 3):
                WIN.blit(buy_half, (WIDTH*0.50, HEIGHT*0.75))
            
            if (pr_pro_1_rect.collidepoint(mx, my)):
                WIN.blit(pr_pro_1_des, (WIDTH*0.04, HEIGHT*0.57))
            elif pr_pro_2_rect.collidepoint(mx, my) and upgrade_track[2] > 0:
                WIN.blit(pr_pro_2_des, (WIDTH*0.19, HEIGHT*0.57))
            elif pr_pro_3_rect.collidepoint(mx, my) and upgrade_track[2] > 1:
                WIN.blit(pr_pro_3_des, (WIDTH*0.34, HEIGHT*0.57))
            elif pr_pro_4_rect.collidepoint(mx, my) and upgrade_track[2] > 2:
                WIN.blit(pr_pro_4_des, (WIDTH*0.49, HEIGHT*0.57))
            

            #lobbying
            WIN.blit(pr_lob_1, (WIDTH*0.05, HEIGHT*0.85))
            WIN.blit(pr_lob_2, (WIDTH*0.20, HEIGHT*0.85))
            WIN.blit(pr_lob_3, (WIDTH*0.35, HEIGHT*0.85))
            WIN.blit(pr_lob_4, (WIDTH*0.50, HEIGHT*0.85))
            
            if(upgrade_track[3] < 1):
                WIN.blit(lock_half, (WIDTH*0.20, HEIGHT*0.85))
            if(upgrade_track[3] < 2):
                WIN.blit(lock_half, (WIDTH*0.35, HEIGHT*0.85))
            if(upgrade_track[3] < 3):
                WIN.blit(lock_half, (WIDTH*0.50, HEIGHT*0.85))
            
            if(upgrade_track[3] > 0):
                WIN.blit(buy_half, (WIDTH*0.05, HEIGHT*0.85))
            if(upgrade_track[3] > 1):
                WIN.blit(buy_half, (WIDTH*0.20, HEIGHT*0.85))
            if(upgrade_track[3] > 2):
                WIN.blit(buy_half, (WIDTH*0.35, HEIGHT*0.85))
            if(upgrade_track[3] > 3):
                WIN.blit(buy_half, (WIDTH*0.50, HEIGHT*0.85))

            if (pr_lob_1_rect.collidepoint(mx, my)):
                WIN.blit(pr_lob_1_des, (WIDTH*0.04, HEIGHT*0.67))
            elif pr_lob_2_rect.collidepoint(mx, my) and upgrade_track[3] > 0:
                WIN.blit(pr_lob_2_des, (WIDTH*0.19, HEIGHT*0.67))
            elif pr_lob_3_rect.collidepoint(mx, my) and upgrade_track[3] > 1:
                WIN.blit(pr_lob_3_des, (WIDTH*0.34, HEIGHT*0.67))
            elif pr_lob_4_rect.collidepoint(mx, my) and upgrade_track[3] > 2:
                WIN.blit(pr_lob_4_des, (WIDTH*0.49, HEIGHT*0.67))
            
        case 3:
            WIN.blit(TAB4, (0, HEIGHT*0.65))

            draw_text(("Public Satisfaction: " + f"{round(100-(pub_amt*100), 2):,}" + "% " ), WIDTH*0.1, HEIGHT*0.75, (55, 45, 51), display=True)
            draw_text(("Pollution Rate: " + f"{round(pol_rate*120, 2):,}" + "ppm/minute " ), WIDTH*0.1, HEIGHT*0.82, (55, 45, 51), display=True)
            draw_text(("Income: $" + f"{round(money_rate*120, 2):,}" + "K/minute " ), WIDTH*0.1, HEIGHT*0.89, (55, 45, 51), display=True)

    # pollution bar
    WIN.blit(POL_BAR, (WIDTH*0.03, HEIGHT*0.08))            
    pyg.draw.rect(WIN, (96, 107, 94), pyg.Rect(WIDTH*0.035, HEIGHT*0.1525, WIDTH*0.045, HEIGHT*0.415*(1 - pol_amt/POL_CAP)))


    



    # balance text
    draw_text(("Balance: $" + f"{round(money_amt, 2):,}" + "K " ), WIDTH*0.01, HEIGHT*0.04, (200, 200, 200))
    

    #pyg.display.update()

# Starting the mixer
mixer.init()

mixer.music.load("dist/assets/img/songs/song.mp3") 
# Setting the volume
mixer.music.set_volume(0.4)
# Start playing the song
mixer.music.play()


  

def main():
    global tab, ticks, pol_rate, money_rate, pol_amt, money_amt, upgrade_track, alpha_Water, popup, pub_amt, disc_rate, pub_rate, EPOCH
    #clock = pyg.time.Clock() #controlls fps and whatnot
    pyg.mouse.set_cursor(pyg.cursors.diamond)
    
    print(pub_amt)
    
    run = True
    
    # game loop. this will be active to run the game
    pyg.init()
    menu()
    EPOCH = time.time() * 1000
    while run:
        #clock.tick(FPS) #again, controls fps 
        #print(time_passed())
        pub_amt = (pol_rate-0.5)/5.0
        print(pol_amt, POL_CAP)
        if pol_amt >= POL_CAP:
            game_state = 1
            victory()
            for event in pyg.event.get():
                if event.type == pyg.QUIT: run = False
            
            continue
        if money_amt < 0:
            game_state = 2
            defeat()
            for event in pyg.event.get():
                if event.type == pyg.QUIT: run = False
            
            continue
        

        if(int(time_passed()/TICK_RATE) > ticks):
            ticks += 1
            pol_tick()
            money_tick()
            print("--------")
        
        activ_inter()

        
        enough = False
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
                                enough = True
                                continue
                            money_amt -= upgrade_costs[0][0]
                            money_rate += 0.208
                            pol_rate += 0.2
                            upgrade_track[0] += 1
                        elif exp_nat_rect.collidepoint(mx, my) and upgrade_track[0] == 1:
                            if(money_amt < upgrade_costs[0][1]):
                                not_enough(upgrade_costs[0][1], money_amt)
                                enough = True
                                continue
                            money_amt -= upgrade_costs[0][1]
                            money_rate += 0.392
                            pol_rate += 0.2
                            upgrade_track[0] += 1
                        elif exp_con_rect.collidepoint(mx, my) and upgrade_track[0] == 2:
                            if(money_amt < upgrade_costs[0][2]):
                                not_enough(upgrade_costs[0][2], money_amt)
                                enough = True
                                continue
                            money_amt -= upgrade_costs[0][2]
                            money_rate += 0.833
                            pol_rate += 0.3
                            upgrade_track[0] += 1
                        elif exp_glo_rect.collidepoint(mx, my) and upgrade_track[0] == 3:
                            if(money_amt < upgrade_costs[0][3]):
                                not_enough(upgrade_costs[0][3], money_amt)
                                enough = True
                                continue
                            money_amt -= upgrade_costs[0][3]
                            money_rate += 1.292
                            pol_rate += 0.7
                            upgrade_track[0] += 1

                    elif tab == 1:
                        if upgrade_track[1] == 4:
                            print("no dice")
                        elif pro_1_rect.collidepoint(mx, my) and upgrade_track[1] == 0:
                            if(money_amt < upgrade_costs[1][0]):
                                not_enough(upgrade_costs[1][0], money_amt)
                                enough = True
                                continue
                            money_amt -= upgrade_costs[1][0]
                            money_rate += 0.05
                            pol_rate += 0.5
                            upgrade_track[1] += 1
                        elif pro_2_rect.collidepoint(mx, my) and upgrade_track[1] == 1:
                            if(money_amt < upgrade_costs[1][1]):
                                not_enough(upgrade_costs[1][1], money_amt)
                                enough = True
                                continue
                            money_amt -= upgrade_costs[1][1]
                            money_rate += 0.125
                            pol_rate += 0.6
                            upgrade_track[1] += 1
                        elif pro_3_rect.collidepoint(mx, my) and upgrade_track[1] == 2:
                            if(money_amt < upgrade_costs[1][2]):
                                not_enough(upgrade_costs[1][2], money_amt)
                                enough = True
                                continue
                            money_amt -= upgrade_costs[1][2]
                            money_rate += 0.208
                            pol_rate += 0.75
                            upgrade_track[1] += 1
                        elif pro_4_rect.collidepoint(mx, my) and upgrade_track[1] == 3:
                            if(money_amt < upgrade_costs[1][3]):
                                not_enough(upgrade_costs[1][3], money_amt)
                                enough = True
                                continue
                            money_amt -= upgrade_costs[1][3]
                            money_rate += 0.625
                            pol_rate += 1.2
                            upgrade_track[1] += 1

                    elif tab == 2:
                        if upgrade_track[2] == 4:
                            print("no dice")

                        elif pr_pro_1_rect.collidepoint(mx, my) and upgrade_track[2] == 0:
                            if(money_amt < upgrade_costs[2][0]):
                                not_enough(upgrade_costs[2][0], money_amt)
                                enough = True
                                continue
                            money_amt -= upgrade_costs[2][0]
                            pub_rate = 0.9
                            upgrade_track[2] += 1

                        elif pr_pro_2_rect.collidepoint(mx, my) and upgrade_track[2] == 1:
                            if(money_amt < upgrade_costs[2][1]):
                                not_enough(upgrade_costs[2][1], money_amt)
                                enough = True
                                continue
                            money_amt -= upgrade_costs[2][1]
                            pub_rate = 0.8
                            upgrade_track[2] += 1

                        elif pr_pro_3_rect.collidepoint(mx, my) and upgrade_track[2] == 2:
                            if(money_amt < upgrade_costs[2][2]):
                                not_enough(upgrade_costs[2][2], money_amt)
                                enough = True
                                continue
                            money_amt -= upgrade_costs[2][2]
                            pub_rate = 0.7
                            upgrade_track[2] += 1

                        elif pr_pro_4_rect.collidepoint(mx, my) and upgrade_track[2] == 3:
                            if(money_amt < upgrade_costs[2][3]):
                                not_enough(upgrade_costs[2][3], money_amt)
                                enough = True
                                continue
                            money_amt -= upgrade_costs[2][3]
                            pub_rate = 0.6
                            upgrade_track[2] += 1
                        
                        
                        #lobbying
                        elif pr_lob_1_rect.collidepoint(mx, my) and upgrade_track[3] == 0:
                            if(money_amt < upgrade_costs[3][0]):
                                not_enough(upgrade_costs[3][0], money_amt)
                                enough = True
                                continue
                            money_amt -= upgrade_costs[3][0]
                            disc_rate = 0.95
                            upgrade_track[3] += 1

                        elif pr_lob_2_rect.collidepoint(mx, my) and upgrade_track[3] == 1:
                            if(money_amt < upgrade_costs[3][1]):
                                not_enough(upgrade_costs[3][1], money_amt)
                                enough = True
                                continue
                            money_amt -= upgrade_costs[3][1]
                            disc_rate = 0.88
                            upgrade_track[3] += 1

                        elif pr_lob_3_rect.collidepoint(mx, my) and upgrade_track[3] == 2:
                            if(money_amt < upgrade_costs[3][2]):
                                not_enough(upgrade_costs[3][2], money_amt)
                                enough = True
                                continue
                            money_amt -= upgrade_costs[3][2]
                            disc_rate = 0.78
                            upgrade_track[3] += 1

                        elif pr_lob_4_rect.collidepoint(mx, my) and upgrade_track[3] == 3:
                            if(money_amt < upgrade_costs[3][3]):
                                not_enough(upgrade_costs[3][3], money_amt)
                                enough = True
                                continue
                            money_amt -= upgrade_costs[3][3]
                            disc_rate = 0.65
                            upgrade_track[3] += 1


        
        keys_pressed = pyg.key.get_pressed()
        


        # game is over

        ##print(pol_amt)
        alpha_Water = pol_amt/POL_CAP * 255
        WORLDWATERPOLLUTION.set_alpha(alpha_Water) #opacityyy 
        WORLDWATER.set_alpha(alpha)

        draw()
        update_costs()
        if(enough):
            warn["tab"] = tab
            warn["time"] = time_passed()
            

        
        if time_passed() - warn["time"] <= 3000 and tab == warn["tab"]:
            
            draw_text(" !!    INSUFFICIENT FUNDS: $" + str(round(warn["had"], 2)) + "K / $" + str(warn["req"]) + "K    !!", WIDTH*0.68, HEIGHT*0.79, (0, 0, 0))
            
        if(popup):
            print('gen pop')
            gen_pop()
        
        #updates display. display wont change if this isnt here
        pyg.display.update()
    pyg.quit()

# dont touch this; if u have question abt it dm jaden
if __name__ == "__main__":
    
    main()