#import necessary libraries

import copy
import random
import pygame
import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from button import Button

#initialization
pygame.init()
#game variables
cards = [ '2', '3','4','5','6','7','8','9','10','J','Q','K','A']
values = {
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10":10,
    "A": 11,
    "J": 10,
    "K": 10,
    "Q": 10,

}




one_deck = 4 * cards
decks = 4


#Pygame Window
WIDTH = 1400
HEIGHT = 900
screen = pygame.display.set_mode([WIDTH, HEIGHT],pygame.FULLSCREEN)
bg_img = pygame.image.load('bb.jpg')
bg_img = pygame.transform.scale(bg_img, (WIDTH,HEIGHT))
screen = pygame.display.set_mode([WIDTH,HEIGHT], pygame.FULLSCREEN)
bg_img2 = pygame.image.load('bdb.png')
bg_img2 = pygame.transform.scale(bg_img2,(WIDTH,HEIGHT))
bg_img1 = pygame.image.load('bg.jpg')
bg_img1 = pygame.transform.scale(bg_img1,(WIDTH,HEIGHT-100))
pygame.display.set_caption('Blackjack!  ')

i = 0
fps = 60
timer = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf',30)
smaller_font = pygame.font.Font('freesansbold.ttf',20)
active = 2
player_score = 0
dealer_score = 0
#win , loss, draw/push
records = [0,0,0,0]
score_board = [0,0,0]
initial_deal = False
my_hand = []
AI_hand = []
AI_score = 0
dealer_hand = []
outcome = 0
game_deck = []
reveal_dealer =  False
hand_active = False
add_score = False
s_board = [0,0,0]
results = ['', 'PLAYER BUSTED o_O', 'Player WINS! :)', 'DEALER WINS :(', 'TIE GAME...', 'AI_WINS! ^_^']

# deal cards by selecting randomly from deck, and make function for one card at a time 
def deal_cards(current_hand, current_deck):
    card = random.randint(0, len(current_deck)) 
    current_hand.append(current_deck[card - 1])
    current_deck.pop(card-1)
    return current_hand, current_deck

# draw scores for player and dealer on screen
def draw_scores(player,dealer,ai):
    screen.blit(font.render(f'Player\'s Score[{player}]', True, 'white'),(550,400))
    screen.blit(font.render(f'AI\'s Score[{ai}]', True, 'white'),(1050,400))
    if reveal_dealer:
        screen.blit(font.render(f'Dealer\'s Score[{dealer}]',True,'white'),(250,400))


#Draw cards visually onto screen
def draw_cards(player, dealer, reveal,ai):
    for i in range(len(player)):
        pygame.draw.rect(screen,'white',[500 + (70 * i), 160 + (5 * i), 120, 220], 0,5)
        screen.blit(font.render(player[i], True, 'black'),(505 + 70 * i , 165 + 5*i))
        screen.blit(font.render(player[i], True, 'black'),(505 + 70 * i , 335 + 5*i))
        pygame.draw.rect(screen,'red',[500 + (70 * i), 160 + (5 * i), 120, 220], 5,5)
    
    for i in range(len(ai)):
        pygame.draw.rect(screen, 'white', [1000 + (70 * i), 160 + (5 * i), 120, 220], 0, 5)
        screen.blit(font.render(ai[i], True, 'black'), (1005 + 70 * i, 165 + 5 * i))
        screen.blit(font.render(ai[i], True, 'black'), (1005+ 70 * i, 335 + 5 * i))
        pygame.draw.rect(screen, 'yellow', [1000 + (70 * i), 160 + (5 * i), 120, 220], 5, 5)
    # if player hasnt finised turn , dealer will hide one card
    for i in range(len(dealer)):
        pygame.draw.rect(screen,'white',[70 + (70 * i), 160 + (5 * i), 120, 220], 0,5)
        if i!= 0 or reveal:
            screen.blit(font.render(dealer[i], True, 'black'),(75 + 70 * i , 165 + 5*i))
            screen.blit(font.render(dealer[i], True, 'black'),(75 + 70 * i , 335 + 5*i))
        else:
            screen.blit(font.render('???', True, 'black'),(75 + 70 * i , 165 + 5*i))
            screen.blit(font.render('???', True, 'black'),(75 + 70 * i , 335 + 5*i))   
        pygame.draw.rect(screen,'blue',[70 + (70 * i), 160 + (5 * i), 120, 220], 5,5)

#Calculate score
def calculate_score(hand):
    #calculate handscore fresh every time, check how many aces we have
    hand_score = 0
    aces_count = hand.count('A')
    for i in range(len(hand)):
        for j in range(8):
            if hand[i] == cards[j]:
                hand_score += int(hand[i])

        #for 10 and face cards add 10
        if hand[i] in ['10','J','Q','K']:
            hand_score += 10

        #for aces start by adding 11, we will check the value first
        elif hand[i] == 'A':
            hand_score += 11

    if hand_score > 21 and aces_count > 0:
        for i in range(aces_count):
            if hand_score > 21:
                hand_score -= 10

    return hand_score            

def AI_cards(hand,current_deck):
    value = calculate_score(hand)
    need = 21 - value
    more = 0
    less = 0
    card_A = 0
    total_card = len(current_deck)
    for i in range(len(current_deck)):
        if (current_deck[i] == "A"):
            card_A = card_A +1
        if (values[current_deck[i]] < need):
            less += 1
        else:
            more += 1
    prob_higher = float(more/total_card * 1.0)
    prob_lower = float(less/total_card * 1.0)  
    risk = float(card_A / total_card *  1.0)  
    if(prob_lower + (2*risk) >= prob_higher or prob_higher-prob_lower<0.001):
        hand, current_deck = deal_cards(hand, current_deck)
    return hand, current_deck       

def get_font(size):
    return pygame.font.Font("font.ttf", size)
#draw game conditions and buttons
def draw_game(active, record=[0,0,0,0], result=[0,0,0],s_board= [0,0,0]):
    button_list = []
    #initially on startup only option is to deal new hand

    if active == 0:
        screen.blit(bg_img,(0,0))
        deal1 = pygame.draw.rect(screen, 'white', [900,50,300,80], 0, 2)
        pygame.draw.rect(screen, 'purple', [900,50,300,80] , 3, 5)
        deal_text = font.render('Black Jack 1.0', True, 'black')
        screen.blit(deal_text, (970,280))
        button_list.append(deal1)
        deal2 = pygame.draw.rect(screen,'white',[900,250,300,80],0,2)
        pygame.draw.rect(screen, 'purple', [900, 250, 300, 80], 3, 5)
        deal_text = font.render('Black Jack 2.0', True, 'black')
        screen.blit(deal_text,(970,280))
        button_list.append(deal2)
        deal3 = pygame.draw.rect(screen,'white',[900,450,300,80],0,2)
        pygame.draw.rect(screen,'purple',[900, 450, 300, 80], 3, 5)
        deal_text = font.render('Wanna Back?', True,'black')
        screen.blit(deal_text,(970,480))
        button_list.append(deal3)

    # once game started, shot hit and stand buttons and win/loss records 
    elif active == 1:
        hit = pygame.draw.rect(screen, 'white', [0,550,300,50], 0, 5)
        pygame.draw.rect(screen, 'purple', [0,550,300,50] , 3, 5)
        hit_text = font.render('HIT ME', True, 'black')
        screen.blit(hit_text, (105,565))
        button_list.append(hit)

        stand = pygame.draw.rect(screen, 'white', [300,550,300,50], 0, 5)
        pygame.draw.rect(screen, 'purple', [300,550,300,50] , 3, 5)
        stand_text = font.render('STAND', True, 'black')
        screen.blit(stand_text, (405,565))
        button_list.append(stand)

        quit = pygame.draw.rect(screen,'white',[600,550,300,50],0,5)
        pygame.draw.rect(screen,'purple',[600,550,300,50],3,5)
        stand_text = font.render('QUIT',True,'black')
        screen.blit(stand_text,(705,565))
        button_list.append(quit)

        score_text = smaller_font.render(f'Wins: {record[0]} Losses: {record[1]} Draws: {record[2]},AI: {record[3]}',True, 'white')
        screen.blit(score_text, (5,640))

        score_text = smaller_font.render(f'Plaers score: {s_board[0]} Dealers score: {s_board[1]} AI score: {s_board[2]}', True, 'white')
        screen.blit(score_text,(5,660))

    elif active == 2:
        screen.blit(bg_img2,(0,0))  
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        MENU_TEXT = get_font(100).render("BLACK JACK",True,"Yellow") 
        MENU_RECT = MENU_TEXT.get_rect(center=(700,200)) 

        color = "#03fce3"

        PLAY_BUTTON = Button(image= pygame.image.load("Play Rect.png"), pos = (700,350),text_input = "PLAY",
                             font = get_font(55), base_color = color, hovering_color="White")
        
        QUIT_BUTTON = Button(image =pygame.image.load("Quit Rect.png"),pos = (700,550),
                             text_input = "QUIT", font= get_font(55),base_color= color, hovering_color="White")
        screen.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)
        return PLAY_BUTTON, QUIT_BUTTON,MENU_MOUSE_POS    
    # if there is an outcome for the hand that was playes, display a restart button 
    if result != 0 and active ==1:
        screen.blit(font.render(results[result], True, 'white'), (15,25)) 
        deal = pygame.draw.rect(screen, 'white', [150,220,300,100], 0, 5)
        pygame.draw.rect(screen, 'green', [150,220,300,120] , 3, 5)
        pygame.draw.rect(screen, 'black', [153,223,294,117] , 3, 5)
        deal_text = font.render('NEW HAND', True, 'black')
        screen.blit(deal_text, (165,250))
        button_list.append(deal)
    return button_list


#check endgame conditions function
def check_endgame(AI_S,hand_act, deal_score, play_score, result, totals, add ,sc_board):
    # check end game scenarios is player has stood, busted or blackjacked
    # result 1- player bust, 2-win, 3-loss, 4-push
    if not hand_act and deal_score >= 17:
        if play_score > 21:
            result = 1
        elif (deal_score < play_score <= 21 and AI_S< play_score<=21)or (deal_score > 21 and play_score > AI_S and play_score <=21) or (dealer_score > 21 and play_score<=21 and AI_S>21):
            result = 2
        elif (play_score < deal_score <= 21 and AI_S < deal_score<=21) or (AI_S>21 and play_score<deal_score<=21):
            result = 3

        elif (((AI_S <=21 and play_score> 21 and deal_score>21) or (deal_score<=21 and deal_score<= AI_S) or (play_score<AI_S<=21)) and AI_S<=21):
            result = 5  
        elif(AI_S == dealer_score or AI_S == player_score):
            result = 4
        if add:
            #player-0 dealer-1 tie-2 ai-3
            if result == 1 or result == 3:
                totals[1] += 1
                sc_board[0] = sc_board[0]
                sc_board[1] = sc_board[1] + 20
                sc_board[2] = sc_board[2] + 20
            elif result == 2:
                totals[0] += 1
                sc_board[0] = sc_board[0] + 30
                sc_board[1] = sc_board[1]
                sc_board[2] = sc_board[2]
            elif result == 5:
                totals[3] +=1
                sc_board[0] = sc_board[0]
                sc_board[1] = sc_board[1]
                sc_board[2] = sc_board[2] + 30

            else:
                totals[2] += 1
            add = False
    return result, totals, add, score_board                  







#main game loop
run = True

while run:
    # run game at our framerate and fill screen with bg color
    timer.tick(fps)
    screen.fill('#301934')
    # intitial deal to player and dealer
    if initial_deal:

        for i in range(2):
            my_hand , game_deck = deal_cards(my_hand, game_deck)
            dealer_hand , game_deck = deal_cards(dealer_hand, game_deck)
            AI_hand, game_deck = deal_cards(AI_hand,game_deck)
        initial_deal = False    
    #once game is activated , and dealt, calculate scores and display cards
    
    if active == 1 :
        player_score = calculate_score(my_hand)
        AI_score = calculate_score(AI_hand)
        draw_cards(my_hand, dealer_hand,reveal_dealer,AI_hand)
        
        if reveal_dealer:
            dealer_score = calculate_score(dealer_hand)
            if dealer_score < 17:
                dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)
        draw_scores(player_score, dealer_score,AI_score)
    if(active != 2):
        buttons = draw_game(active,records, outcome,score_board)  
    else:
        PLAY_BUTTON, QUIT_BUTTON,MENU_MOUSE_POS = draw_game( active, records, outcome,score_board) 


    

    #event handling, if quit pressed, then exit game

     # event handling, if quit pressed, then exit game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False 
        if event.type == pygame.MOUSEBUTTONUP:
            if active == 2:
               
                for button in [PLAY_BUTTON, QUIT_BUTTON]:
                     button.changeColor(MENU_MOUSE_POS)
                     button.update(screen)
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                     active = 0
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                     pygame.quit()
                pygame.display.update()
            elif active == 0:
                if buttons[0].collidepoint(event.pos):
                    active = True
                    initial_deal = True
                    game_deck = copy.deepcopy(decks * one_deck)
                    my_hand = []
                    AI_hand = []
                    dealer_hand = []
                    outcome = 0
                    hand_active = True
                    reveal_dealer = False
                    outcome = 0
                    add_score = True
                elif buttons[2].collidepoint(event.pos):
                    active = 2
                elif buttons[1].collidepoint(event.pos):
                    root = tk.Tk()
                    root.title('Black Jack 2.0    Level 1')
                    root.attributes("-fullscreen", True)
                    root.resizable(False, False)
                    root.geometry('+550+300')
                    logo()
                    create_status_bar()
                    create_game_board()
                    root.protocol('WM_DELETE_WINDOW', exit_app)
                    root.mainloop()
                    pygame.display.update()
                    #pygame.quit()
            

                

            else:
                # if player can hit, allow them to draw a card
                if buttons[0].collidepoint(event.pos) and player_score < 21 and hand_active:
                    
                    print("hit")
                    my_hand, game_deck = deal_cards(my_hand, game_deck)  
                    AI_hand, game_deck = AI_cards(AI_hand, game_deck)
                    print(AI_hand)
                    
                # allow player to end turn (stand)
                elif buttons[1].collidepoint(event.pos) and not reveal_dealer:
                    reveal_dealer = True
                    hand_active = False
                    
                elif buttons[2].collidepoint(event.pos):
                    screen.fill('Black')
                    active = 2
                   
                elif len(buttons) == 4:
                    if buttons[3].collidepoint(event.pos):
                        active = 1
                        initial_deal = True
                        game_deck = copy.deepcopy(decks * one_deck)
                        my_hand = []
                        AI_hand =[]
                        dealer_hand = []
                        outcome = 0
                        score_board = [0,0,0]
                        hand_active = True
                        reveal_dealer = False
                        outcome = 0
                        add_score = True
                        dealer_score = 0
                        player_score = 0


    # if player busts, automatically end turn - treat like a stand
    if hand_active and player_score >= 21:
        hand_active = False
        reveal_dealer = True

    outcome, records, add_score, score_board = check_endgame(AI_score,hand_active, dealer_score,player_score, outcome, records, add_score,score_board)

    pygame.display.flip()
pygame.quit()





       
