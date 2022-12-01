# Yanjun Meng
# CS-UY 1114
# Final project
# December 9 2018

import turtle
import time
import random
import math

user1x, user2x, user1points, user2points = 0
ballx, bally, ballvx, ballvy = 0
turn = ''
endGame = False

def draw_frame():
    """
    Given the current state of the game in
    the global variables, draw all visual
    elements on the screen.
    """

    # draw middle line
    turtle.width(1)
    turtle.up()
    turtle.goto(-turtle.window_width()/2,0)
    for i in range(64):
        turtle.down()
        turtle.forward(10)
        turtle.up()
        turtle.forward(10)
    # draw the ball
    turtle.width(6)
    turtle.up()
    turtle.goto(ballx, bally)
    turtle.down()
    turtle.dot()
    # draw computer's paddle
    turtle.up()
    turtle.goto(user2x, -(turtle.window_height() / 4))
    turtle.seth(0)
    turtle.down()
    turtle.fd(100)
    # draw user's paddle
    turtle.up()
    turtle.goto(user1x, turtle.window_height() / 4)
    turtle.seth(0)
    turtle.down()
    turtle.fd(100)
    # draw user's score
    turtle.up()
    turtle.goto(-turtle.window_width() / 2 + 20, turtle.window_height() / 2 - 20)
    turtle.down()
    turtle.write("your score: "+str(user1points), font=(100))
    # draw computer's score
    turtle.up()
    turtle.goto(-turtle.window_width() / 2 + 20, -turtle.window_height() / 2 + 20)
    turtle.down()
    turtle.write("computer's score: "+str(user2points), font = (100))


def key_left():
    """
    Adjust the position of the user's paddle
    appropriately whenever
    the user press the left arrow.
    """
    global user1x
    frame = -turtle.window_width() / 2
    if user1x >= frame:
        user1x -= 20
    else:
        user1x = frame


def key_right():
    """
    Adjust the position of the user's paddle
    appropriately whenever
    the user press the right arrow.
    """
    global user1x
    frame = turtle.window_width() / 2 - 100
    if user1x <= frame:
        user1x += 20
    else: # paddle out of frame
        user1x = frame


def reset():
    """
    Reset the global variables representing
    the position and velocity of the ball and
    the position of the paddles to their initial
    state, effectively restarting the game.
    """
    global user1x, user2x
    global ballvx, ballvy
    global ballx, bally
    global speed
    global user1points, user2points
    global turn

    user1x, user2x = 0, 0
    ballx, bally = 0, 0
    angle = math.radians(random.choice([random.randint(20,160), \
                                        random.randint(200,340)]))
    ballvx, ballvy = math.cos(angle)*speed, math.sin(angle)*speed
    user1points, user2points = 0, 0
    update_position()
    if bally < 0:
        turn = 'ai'
    elif bally > 0:
        turn = 'user'


def ai():
    """
    Perform the 'artificial intelligence' of
    the game, by moving the computer's paddle
    towards the ball in an attempt to get
    under it.
    """
    global user2x
    global bally
    global ballx
    global speed

    width = turtle.window_width()/2
    pad_center = user2x+50
    pad_end = user2x+100

    if pad_center != ballx:
        if pad_end < width and user2x > -width:
            if pad_center >= ballx:
                user2x -= speed
            elif user2x <= ballx:
                user2x += speed
        elif user2x+100 >= width: #paddle out of frame
            user2x -= speed
        elif user2x <= -width: #paddle out of frame
            user2x += speed

def update_velocity_user():
    '''
    Detect where the ball hits the user's paddle and
    update the ball's direction/velocity accordingly.
    '''
    global user1x
    global ballvx, ballvy
    global ballx
    global user1points

    # hits at the center:
    if user1x+50 == ballx:
        ballvx = 0
        ballvy = -speed

    # hits at extreme left:
    elif user1x-5 <= ballx <= user1x+5:
        ballvx = -math.sin(math.radians(70)) * speed
        ballvy = -math.cos(math.radians(70)) * speed

    # hits at extreme right:
    elif user1x+95 <= ballx <= user1x+105:
        ballvx = math.sin(math.radians(70)) * speed
        ballvy = -math.cos(math.radians(70)) * speed

    # hits at left side:
    elif user1x+5 < ballx < user1x+50:
        angle = math.fabs((user1x+50-ballx)/50*70)
        ballvx = -math.sin(math.radians(angle)) * speed
        ballvy = -math.cos(math.radians(angle)) * speed

    # hits at right side:
    elif user1x+50 < ballx < user1x+95:
        angle = math.fabs((ballx-(user1x+50))/50*70)
        ballvx = math.sin(math.radians(angle)) * speed
        ballvy = -math.cos(math.radians(angle)) * speed

def update_velocity_ai():
    '''
    Detect where the ball hits the computer's paddle and
    update the ball's direction/velocity accordingly.
    '''
    global user2x
    global ballvx, ballvy
    global ballx

    # hits at the center:
    if user2x+50 == ballx:
        ballvx = 0
        ballvy = speed
    # hits at extreme left:
    elif user2x-5 <= ballx <= user2x+5:
        ballvx = -math.sin(math.radians(70)) * speed
        ballvy = math.cos(math.radians(70)) * speed
    # hits at extreme right:
    elif user2x+95 <= ballx <= user2x+105:
        ballvx = math.sin(math.radians(70)) * speed
        ballvy = math.cos(math.radians(70)) * speed
    # hits at left half:
    elif user2x+5 < ballx < user2x+50:
        angle = math.fabs((user2x+50-ballx)/50*70)
        ballvx = -math.sin(math.radians(angle)) * speed
        ballvy = math.cos(math.radians(angle)) * speed
    # hits at right half:
    elif user2x+50 < ballx < user2x+95:
        angle = math.fabs((ballx-(user2x+50))/50*70)
        ballvx = math.sin(math.radians(angle)) * speed
        ballvy = math.cos(math.radians(angle)) * speed

def update_score():
    '''
    Detect who misses the ball and update the score accordingly.
    '''
    global bally
    global user1points, user2points

    if bally < 0:
        user1points += 1
    elif bally > 0:
        user2points += 1

def update_position():
    '''e
    Update the ball's position based on latest velocity.
    '''
    global ballx, bally
    global ballvx, ballvy

    ballx += ballvx
    bally += ballvy

def physics():
    """
    Handles the physics of the game
    by updating the position and velocity of the
    ball depending on its current location.
    """
    global ballx, bally
    global ballvx, ballvy
    global user1points, user2points
    global speed
    global user1x, user2x
    global endGame
    global turn

    width = turtle.window_width() / 2
    paddley = turtle.window_height()/4

    # when user hits the ball:
    if paddley-20 < bally < paddley and user1x-5 < ballx < user1x+105 \
       and turn == 'user':
        update_velocity_user()
        user1points += 1
        turn = 'ai'

    # when computer hits the ball:
    elif -paddley < bally < -paddley+20 and user2x-5 < ballx < user2x+105\
         and turn == 'ai':
        update_velocity_ai()
        user2points += 1
        turn = 'user'

    # when the ball is missed:
    elif math.fabs(bally) > paddley or math.fabs(ballx)-3 >= width:
        update_score()
        reset()

    # when the ball hits the wall:
    elif width-20 < ballx < width or -width < ballx < -width+20:
        ballvx = -ballvx

    update_position()

    # check if there's a winner
    if user1points == 8 or user2points == 8:
        endGame = True

def restart():
    '''
    Let user restart or exit the game.
    '''
    global endGame

    answer = input('Restart game? (y/n) \n').lower()
    if answer == 'y':
        endGame = False
        main()
    elif answer == 'n':
        turtle.bye()
    else:
        print('Invalid answer. ', end = '')
        restart()

def mode():
    '''
    Let user choose how hard they want the game to be.
    '''
    global speed
    choice = input("Choose 'hard', 'medium', 'easy', or 'whatever': \n").lower()
    modes = {'hard': 18, 'medium': 14, 'easy': 10, 'whatever': \
             random.randint(14,18)}
    if choice in modes.keys():
        speed = modes[choice]
        print('Game starts in 1 second. \n')
        time.sleep(1)
    else:
        print('Invalid choice. ', end = '')
        mode()

def main():
    """
    Run the game.
    """
    global endGame

    mode()
    turtle.tracer(0, 0)
    turtle.hideturtle()
    turtle.onkey(key_left, "Left")
    turtle.onkey(key_right, "Right")
    turtle.listen()
    reset()
    turtle.bgcolor('black')
    turtle.pencolor('white')
    while not endGame:
        physics()
        ai()
        turtle.clear()
        draw_frame()
        turtle.update()
        time.sleep(0.05)
    restart()


main()
