import pygame
import random
import time as tim

_screen_width = 900
_screen_height = 500
_play_width = 600  #20 blocks of 30 width
_play_height = 300 #10 blocks of 30 height
_block_size = 30

_top_left_x = (_screen_width - _play_width) // 2
_top_left_y = (_screen_height - _play_height) // 2

#colors

colors = ['green','orange','red','blue','yellow','pink']
player_shape = [1,1,1]

#field
field = [(x,y) for x in range(20) for y in range(10)]

#colors field

field_colors = dict()
for pos in field:
    field_colors[pos] = 'black'

#directions

directions = [(-1,0),(-1,1),(-1,-1),(1,0),(1,1),(1,-1)]

#class constructor

class player(object):
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.color = random.choice(colors)
        self.shape = player_shape
        
class ball(object):
    def __init__(self,x,y,direction,color='white'):
        self.x = x
        self.y = y
        self.direction = direction
        self.color = color
        
#create player
def create_player(x,y):
    return player(x,y)

#create ball
def create_ball(x,y,direction):
    return ball(x,y,direction)
    

#window constructor

def draw_game_field(win):
    pygame.draw.line(win,'white',(_top_left_x,_top_left_y),(_top_left_x+_play_width,_top_left_y),5)
    pygame.draw.line(win,'white',(_top_left_x,_top_left_y+_play_height),(_top_left_x+_play_width,_top_left_y+_play_height),5)
    pygame.draw.line(win,'white',(_top_left_x,_top_left_y-2),(_top_left_x,_top_left_y+_play_height+2),10)
    pygame.draw.line(win,'white',(_top_left_x+_play_width,_top_left_y-2),(_top_left_x+_play_width,_top_left_y+_play_height+2),10)
    pygame.draw.line(win,'green',(_top_left_x+(_play_width/2),_top_left_y-2),(_top_left_x+(_play_width/2),_top_left_y+_play_height+2),10)

    

def draw_grid(win,x,y):

    for y in range(y+1):
        pygame.draw.line(win,'grey',(_top_left_x,_top_left_y+y*_block_size),(_top_left_x+_play_width,_top_left_y+y*_block_size ))
        for x in range(x+1):
            pygame.draw.line(win,'grey',(_top_left_x+x*_block_size,_top_left_y),(_top_left_x+x*_block_size,_top_left_y+_play_height))

#cell painter

def delete_cell(win,field_colors,pos,long):

    x,y = pos
    for i in range(long):
        field_colors[(x,y+i)] = 'black'
    
    
def change_cell(win,field_colors,pos,color,long):

    x,y = pos
    for i in range(long):
        field_colors[(x,y+i)] = color

        
def paint_cell(win,field_colors):
    
    for pos in field_colors.keys():
        x,y = pos          
        color = field_colors[pos]
        pygame.draw.rect(win, color, (_top_left_x+x*_block_size,_top_left_y+y*_block_size, _block_size,_block_size),0)

    draw_grid(win,20,10)

#ball behaviour
    
def ball_behaviour(win,field_colors,ball_x,ball_y,p1_x,p1_y,p2_x,p2_y,direction,color):

    delete_cell(win,field_colors,(ball_x,ball_y),1)
    x,y = direction
    ball_x += x
    ball_y += y
    pos_ok = verify_ball(ball_x,ball_y, field_colors)

    if pos_ok:
        
        change_cell(win,field_colors,(ball_x,ball_y),color,1)

    else:

        
        if y == 0 and x in(1,-1):
            ball_x += x*-1
            ball_y += y*-1
            direction = x*-1,random.randrange(-1,1)

        elif y in (1,-1) and ball_x not in(0,19):
            ball_x += x*-1
            ball_y += y*-1
            direction = x,y*-1

        else:                     
            ball_x += x*-1
            ball_y += y*-1
            direction = x*-1,random.randrange(-1,1)

        
        change_cell(win,field_colors,(ball_x,ball_y),color,1)
        

    return ball_x,ball_y,direction

def verify_ball(x,y, field_colors):
    
    
    if (x in(-1,20)) or (y in(-1,10)) or (field_colors[(x,y)] != 'black'):
        return False
    else:
        return True

def verify_player(y):
        
    if (y in(0,10-4)):
        return False
    else:
        return True
    

#player movement
def player_behaviour(player,direction):

    if player == "P1" and direction == "UP":

        return p1_y

    elif player == "P1" and direction == "DOWN":
        return p1_y

    elif player == "P2" and direction == "UP":
        return p2_y
    
    elif player == "P2" and direction =="DOWN":
        return p2_y

    else: pass
        
    

#main
            
def game():

    #set up
    window = pygame.display.set_mode((_screen_width,_screen_height))
    pygame.display.set_caption("Pong Game")
    draw_grid(window,20,10)
    draw_game_field(window)

    #text initisl
    pygame.font.init()
    my_font = pygame.font.SysFont('Comic Sans MS', 30)
    text_surface = my_font.render("Let's PLAY!", True, "white",)
    window.blit(text_surface, ((_screen_width/2)-50,20))

        
    #clocks
    clock = pygame.time.Clock()
    time=0

    #create players and ball
    p1 = create_player(0,3)
    p2 = create_player(19,3)
    ball = create_ball(10,5,(0,0))

    #elements initial position

    change_cell(window,field_colors,(ball.x,ball.y),ball.color,1)
    paint_cell(window,field_colors)

    change_cell(window,field_colors,(p1.x,p1.y),p1.color,4)
    paint_cell(window,field_colors)

    change_cell(window,field_colors,(p2.x,p2.y),p2.color,4)
    paint_cell(window,field_colors)

    ball.direction = random.choice(directions)

    pygame.display.update()

    tim.sleep(1)

    run = True

    

    while run:
        
        time += clock.get_rawtime()
        clock.tick()


        if time/500 > 0.15:

            time = 0

            ball.x,ball.y,ball.direction = ball_behaviour(window,field_colors,ball.x,ball.y,p1.x,p1.y,p2.x,p2.y,ball.direction,ball.color)

            if ball.x in (0,19):
                if ball.x == 0:
                    player = "Player 2"
                if ball.x == 19:
                    player = "Player 1"

                text = f"GAME FINISHED! {player} wins!"
                #text final
                pygame.font.init()
                my_font = pygame.font.SysFont('Comic Sans MS', 30)
                text_surface = my_font.render(text, True, "white","red")
                window.blit(text_surface, ((_screen_width/4),20))
    
                run = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    
                if event.type == pygame.KEYDOWN:

                    #print(event.key)
                    
                    if event.key == pygame.K_LEFT:
                        #to change for: p1.y = player_behaviour()
                        pos_ok = verify_player(p1.y)
                        if pos_ok or p1.y == 10-4:
                            delete_cell(window,field_colors,(p1.x,p1.y),4)
                            p1.y -= 1
                            change_cell(window,field_colors,(p1.x,p1.y),p1.color,4)
                            #print('P1_UP')
                            
                    if event.key == pygame.K_RIGHT:
                        pos_ok = verify_player(p1.y)
                        if pos_ok or p1.y == 0:
                            delete_cell(window,field_colors,(p1.x,p1.y),4)
                            p1.y += 1
                            change_cell(window,field_colors,(p1.x,p1.y),p1.color,4)
                            #print('P1_DOWN')


                    if event.key == pygame.K_DOWN:
                        pos_ok = verify_player(p2.y)
                        if pos_ok or p2.y == 0:
                            delete_cell(window,field_colors,(p2.x,p2.y),4)
                            p2.y += 1
                            change_cell(window,field_colors,(p2.x,p2.y),p2.color,4)
                            #print('P2_DOWN')

                    if event.key == pygame.K_UP:
                        pos_ok = verify_player(p2.y)
                        if pos_ok or p2.y == 10-4:
                            delete_cell(window,field_colors,(p2.x,p2.y),4)
                            p2.y -= 1
                            change_cell(window,field_colors,(p2.x,p2.y),p2.color,4)
                            #print('P2_UP')

            paint_cell(window,field_colors)
            pygame.display.update()

        

if __name__ == "__main__":
    game()
