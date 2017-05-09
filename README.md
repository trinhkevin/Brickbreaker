**Members**

    Brian Byrne - bbyrne5
    Kevin Trinh - ktrinh1

**Sources**

    stars.png

    source: https://i.ytimg.com/vi/JquobII5VjA/maxresdefault.jpg

    https://gamedev.stackexchange.com/questions/22609/breakout-collision-detecting-the-side-of-collision

    https://www.reddit.com/r/pygame/comments/2pxiha/rectanglar_circle_hit_detection/

**Instructions**

    To run the game you first must have all the files: brickbreaker.py, player.py, sprites.py, constants.py, and stars.png.
    Then you must chose a port to connect to as well as an address, i.e. port 40110 on ash.campus.nd.edu (the default port and address).
    Each player must use the same port and address. Once that is chosen you run the game by calling player.py
    with a player number (1 or 2), the port, and the address. It is important to use python2.7 because of the twisted library.

        python2.7 player.py -u [PLAYER NUMBER] -p [PORT NUMBER] -s [ADDRESS]

    You MUST run Player 1 first. Player 1 listens for Player 2 so if you run Player 2 first they WILL NOT connect.
    Player 1's platform will be on top and Player 2's will be on the bottom.

**Controls**

    Use Spacebar to shoot the ball off of the platform then use the arrows to move the platform from side to side.
    Everytime you miss the ball one of the health bars (represented by * next to each player on the scoreboard)
    will go down and the ball will reset to the platform. When a player has no more *'s that player loses and the game is over.
    The goal is to just survive longer than your opponent. There is a bar of grey bricks in the middle that the ball cannot
    pass through so each player can only affect their side of the board. The detailed descriptions of each type of brick and their
    occurance rates are below except for the unbreakable grey blocks.


**Bricks and Percentages**

    Red       - 1 life, 1.5x until it hits platform again (YELLOW)  7%

    Green     - 1 life, +1 life                                     10%

    Blue      - 1 life, 0.5 until it hits platform again  (BLUE)    10%

    Yellow    - 1 life                                              40%

    Purple    - 2 lives                                             20%

    Orange    - 3 lives, ball insta-kill 3 seconds        (RED)     10%

    Rainbow   - 3 lives, turns opponents ball black for 3 seconds   3%
