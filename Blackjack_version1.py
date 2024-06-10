#import necessary libraries

import copy
import random
import pygame
import os


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

#initialization
pygame.init()


one_deck = 4 * cards
decks = 4


#Pygame Window
WIDTH = 900
HEIGHT = 900
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('BlackJack version1')

fps = 60
timer = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf',44)
smaller_font = pygame.font.Font('freesansbold.ttf',36)
active = False
player_score = 0
dealer_score = 0
#win , loss, draw/push
records = [0,0,0]
initial_deal = False
my_hand = []
dealer_hand = []
outcome = 0
reveal_dealer = False

# deal cards by selecting randomly from deck, and make function for one card at a time 
def deal_cards(current_hand, current_deck):
    card = random.randint(0, len(current_deck)) 
    current_hand.append(current_deck[card - 1])
    current_deck.pop(card-1)
    print(current_hand,current_deck)
    return current_hand, current_deck

#Draw cards visually onto screen
def draw_cards(player, dealer, reveal):
    for i in range(len(player)):
        pygame.draw.rect(screen,'white',[70 + (70 * i), 460 + (5 * i), 120, 220], 0,5)
        screen.blit(font.render(player[i], True, 'black'),(75 + 70 * i , 465 + 5*i))
        screen.blit(font.render(player[i], True, 'black'),(75 + 70 * i , 635 + 5*i))
        pygame.draw.rect(screen,'red',[70 + (70 * i), 460 + (5 * i), 120, 220], 5,5)
    
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
def calculatee_score(hand):
    #calculate handscore fresh every time, check how many aces we have


#draw game conditions and buttons
def draw_game(active, record):
    button_list = []
    #initially on startup only option is to deal new hand

    if not active:
        deal = pygame.draw.rect(screen, 'white', [150,20,300,100], 0, 5)
        pygame.draw.rect(screen, 'green', [150,20,300,100] , 3, 5)
        deal_text = font.render('DEAL HAND', True, 'black')
        screen.blit(deal_text, (165,50))
        button_list.append(deal)

    # once game started, shot hit and stand buttons and win/loss records 
    else:
        hit = pygame.draw.rect(screen, 'white', [0,700,300,100], 0, 5)
        pygame.draw.rect(screen, 'green', [0,700,300,100] , 3, 5)
        hit_text = font.render('HIT ME', True, 'black')
        screen.blit(hit_text, (55,700))
        button_list.append(hit)
        stand = pygame.draw.rect(screen, 'white', [300,700,300,100], 0, 5)
        pygame.draw.rect(screen, 'green', [300,700,300,100] , 3, 5)
        stand_text = font.render('STAND', True, 'black')
        screen.blit(stand_text, (355,700))
        button_list.append(stand)
        score_text = smaller_font.render(f'Wins: {record[0]} Losses: {record[1]} Draws: {record[2]}',True, 'white')
        screen.blit(score_text, (15,800))
    
    return button_list






#main game loop
run = True

while run:
    # run game at our framerate and fill screen with bg color
    timer.tick(fps)
    screen.fill('black')
    # intitial deal to player and dealer
    if initial_deal:

        for i in range(2):
            my_hand , game_deck = deal_cards(my_hand, game_deck)
            dealer_hand , game_deck = deal_cards(dealer_hand, game_deck)
        print(my_hand, dealer_hand)
        initial_deal = False    
    #once game is activated , and dealt, calculate scores and display cards
    
    if active:
        player_score = calculate_score(my_hand)
        draw_cards(my_hand, dealer_hand,reveal_dealer)

    buttons = draw_game(active,records)

    #event handling, if quit pressed, then exit game

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONUP: 
            if not active:
                if buttons[0].collidepoint(event.pos):
                    active = True  
                    initial_deal = True
                    game_deck = copy.deepcopy(decks * one_deck)
                    my_hand = [] 
                    dealer_hand = []

    pygame.display.flip()     
pygame.quit()       
