from Vector import Vector

###############################
#
# Cameron Morris
# 9/13/2024
# cmorris@uccs.edu
#
# Constants file for magical game property of dave the magical cheese wizard
###############################

class Constants:
    #Game Constants
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    Frame_Rate = 60
    Background_Color = (100,149,237)
    Target_Line_Color = (255,0,255)
    Flee_Line_Color = (255,0,0)
    Line_Thickness = 3
    Velocity_Line_Color = (0,0,255)

    #Player Constants
    Player_Color = (255,255,0)
    Player_Initial_Spawn = (Vector)(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    Player_Speed = 5.5
    Player_Size = 10

    #Enemy Constants
    Enemy_Size = 10
    Enemy_Speed = 5
    Enemy_Color = (0,255,0)
    Enemy_Detection_Dist = 200
    Enemy_Random_Wander_Factor = 0.75
    Enemy_Spawn_Count = 10





