'''Actual Code Begins'''
# Import Modules #

from __future__ import division

import  pygame, math, os, ctypes
from    fractions       import *
from    pygame          import *
from    pygame.locals   import *
from    math            import *

from collections import OrderedDict

# Resolution Check - Get Max Res #
MAX_WIDTH   = ctypes.windll.user32.GetSystemMetrics(0) # Get System Res X #
MAX_HEIGHT  = ctypes.windll.user32.GetSystemMetrics(1) # Get System Res Y #

# Resolution Check - Get Aspect Ratio #
RES_GCD             = gcd(MAX_WIDTH , MAX_HEIGHT)
ASPECT_RATIO_W      = MAX_WIDTH      // RES_GCD
ASPECT_RATIO_H      = MAX_HEIGHT    //  RES_GCD
ASPECT_RATIO_VAL    = MAX_HEIGHT / MAX_WIDTH

print ("DEBUGSTRING - Resolution - " +str(MAX_WIDTH) +"x" +str(MAX_HEIGHT) +" | Res Val - " +str(ASPECT_RATIO_VAL))
print ("DEBUGSTRING - Technical Aspect Ratio - " +str(ASPECT_RATIO_W) +":" +str(ASPECT_RATIO_H))

# Resolution Check - Get height from a base of 320 Pix. #
TRUE_DEFAULT_WIDTH  = 512
TRUE_DEFAULT_HEIGHT = int(TRUE_DEFAULT_WIDTH * ASPECT_RATIO_VAL) # Don't ask, // wasn't enough.
print (ASPECT_RATIO_VAL)
print ("DEBUGSTRING - Final Res = " +str(TRUE_DEFAULT_WIDTH) +"x" +str(TRUE_DEFAULT_HEIGHT))


# Resolution Check - Set Resolutions #
# Set Current + Default Width to Aspect Ratio * 20
SCREEN_WIDTH        = TRUE_DEFAULT_WIDTH
SCREEN_HEIGHT       = TRUE_DEFAULT_HEIGHT
DEFAULT_WIDTH       = SCREEN_WIDTH
DEFAULT_HEIGHT      = SCREEN_HEIGHT
SAVED_WIDTH         = SCREEN_WIDTH
SAVED_HEIGHT        = SCREEN_HEIGHT

# Set up display and dupe surface #
FLAGS_RESIZABLE      = RESIZABLE
FLAGS_FULLSCREEN    = HWSURFACE |   DOUBLEBUF   | FULLSCREEN
TRUE_DISPLAY        = pygame.display.set_mode( (DEFAULT_WIDTH, DEFAULT_HEIGHT), FLAGS_RESIZABLE)
SCREEN_DISPLAY      = pygame.Surface((DEFAULT_WIDTH, DEFAULT_HEIGHT), HWSURFACE, 8)
TRUE_DISPLAY.set_alpha(None)

# Load PyGame & Sound System #
pygame.mixer.pre_init(44100, -16, 2, 1024)   # irrc, only default OGGs from Audacity work.
pygame.init()
pygame.mouse.set_visible(True)

#os.environ['SDL_VIDEO_CENTERED'] ='1'

pygame.display.set_caption("Hello")


FONT_SIZE       = 15
FONT_TRUE_SIZE  = 12
FONT_MAX_W      = DEFAULT_WIDTH     //FONT_TRUE_SIZE     # Max font elements wide
FONT_MAX_H      = DEFAULT_HEIGHT    //FONT_TRUE_SIZE     # Max font elements high
GAME_FONT       = pygame.font.SysFont("pixrpg01", FONT_SIZE, False)
DEBUG_FONT      = pygame.font.SysFont("emulogic", 8, False)
Debug_Height    = FONT_SIZE -4

# Horizon - Used for FOV Calc #
Horizon_XPos = DEFAULT_WIDTH//2
Horizon_YPos = DEFAULT_HEIGHT//2

# Used for mouse snapping #
SCREEN_HalfX = DEFAULT_WIDTH//2
SCREEN_HalfY = DEFAULT_HEIGHT//2
    
# Game Constants #
GAME_CLOCK                  = pygame.time.Clock()
GAME_FPS                    = 144
CONST_MILLISECONDS          = 1000//GAME_FPS     # Number of Milliseconds per Frame



# Global Timer #
Global_Timer                = 0
Global_Timer_Max            = 2 ** 32
Global_Timer_TimeScale      = 1
Global_Timer_Paused         = False

Demo_Timer                  = 0
Demo_Timer_Max              = GAME_FPS * 3

PlayerControlEnabled    = True

Player_XPos = 0
Player_YPos = 0
Player_ZPos = 0
Player_Height = 64
Player_Stand_Height = 64
Player_Crouch_Height = 32
Player_BaseSpeed = 1
Player_Hitbox_Width = 15
Player_Hitbox_Height = 15


Moving                  = False
MovingLeft              = False
MovingRight             = False
MovingUp                = False
MovingDown              = False
Jumping                 = False
Crouching               = False
Gravity                 = 0
Player_JumpForce        = 2
TerminalVelocity        = 512

Player_Pitch    = 0
Player_Roll     = 0

tau = pi * 2
Rotate_270Deg   =   tau - (pi/2)
Rotate_180Deg   =   pi
Rotate_90Deg    =   pi/2
Rotate_45Deg    =   pi/4

FPS_MouseFocus = True
pygame.mouse.set_pos(SCREEN_HalfX, SCREEN_HalfY)

Mouse_RelX = 0
Mouse_RelY = 0

FullScreen = False

TEX_PALETTE = pygame.image.load('palette.png').convert(8)

COLPAL = []

# Very Kludged in. If you have an error, replace 16s below with TEX_PALETTE.get_width and get_height respectively.
for x in range (16):
    for y in range (16):
        #COLPAL.append(TEX_PALETTE.get_at((y, x)))          Old code, use if we can add without Alphas
        COLPAL.append( (TEX_PALETTE.get_at((y, x))[0], TEX_PALETTE.get_at((y, x))[1], TEX_PALETTE.get_at((y, x))[2]) ) # Workaround that adds RGB, not A.

TEX_PALETTE = pygame.transform.scale(TEX_PALETTE, (TEX_PALETTE.get_width() * 4, TEX_PALETTE.get_height() * 4))
# Color Consts #
COL_COLORKEY = COLPAL[255]


# Textures #
TEX_WORLD_TEXTURES = pygame.image.load('worldTex.png').convert(8)

# Below technically aren't consts, but are used to define what object gets alligned to Palette Sections
PAL_GREYS           = range(0,31)       # 32 Colors of Black to White
PAL_SKIN            = range(32, 63)     # Color of your skin and some guns in Viewmodel
PAL_EXPLODE         = range(64, 79)     # Color of explosions
PAL_BLOOD           = range(64, 71)     # Also reds used for explosions
PAL_YELLOWS         = range(80, 95)     # Yellow Colors
PAL_RUSTIC          = range(96, 111)    # Rustic Metals used in some viewmodels & textures
PAL_WATER_LIGHT     = range(112, 119)   # Light Blues
PAL_WATER_DARK      = range(120, 127)   # Dark Blues
PAL_FOLIAGE_LIGHT   = range(128, 135)   # Olivey Foliage that's light
PAL_FOLIAGE_DARK    = range(136, 143)   # Darker Pool Table Green
PAL_ORANGES         = range(144, 151)   # Orange Colors
PAL_SHRUBS          = range(152, 155)   # Small Section of Browns
PAL_FOLIAGE_FADED   = range(156, 159)   # Light, dying foluage
PAL_TEALS           = range(160, 167)   # Selection of Teal Colors
PAL_MID_DARKS       = range(168, 175)   # Tad out of order, but dark to mid colors.
PAL_PINKS           = range(176, 191)   # Evening Skybox Pinks, etc
PAL_SKY_DARK        = range(192, 199)   # Used for Night Skies
PAL_RUST1           = range(200, 207)   # Rustic again, more orange colored
PAL_SKY_LIGHT       = range(208, 215)   # Used for morning skies
PAL_BLUE_ACCENTS    = range(215, 223)   # Dark Blue used on certain stone, etc.
PAL_PASTALS         = range(224, 239)   # Used for bright moments
PAL_DARKS           = range(240, 247)   # Used for dimming and low brightness
PAL_RUST2           = range(248, 254)   # Misc Rust
PAL_COLORKEY        = 255               # Ignored Color, used as an Alpha


# User defined, be careful of this, as we can change the colors to anything. These are just defaults.
COL_WHITE = COLPAL[31]


SCREEN_DISPLAY.set_palette(COLPAL)
SCREEN_DISPLAY.set_colorkey(COL_COLORKEY)



def rotate2D(pos,rad): x,y=pos; s,c = sin(rad), cos(rad); return x*c-y*s, y*c+x*s

def crash():
    print ("DEBUGSTRING - MANUAL CRASH")
    0/0


'''Init Textures'''

print ("\n=== BEGIN GAME LOOP ===")


OOB_ColMin = 235

OOB_Col = OOB_ColMin

OOB_ColMax = 240
OOB_Forward = True


FullScreen

Surf = pygame.Surface((50, 50))

Surf.fill((255,255,255))


'''TODO THIS IS A TEST MAP'''


def rotate2D(pos,rad): x,y=pos; s,c = sin(rad), cos(rad); return x*c-y*s, y*c+x*s


def crash():
    print ("DEBUGSTRING - MANUAL CRASH")
    0/0



SECTOR_TYPE = 0
SECTOR_POS = 1
SECTOR_DIM = 2
SECTOR_FLOORY = 3   # Get YPos of Floor Plane
SECTOR_CEILY = 4    # Get YPos of Ceiling Plane
SECTOR_THING = 5    # Thing Info, list entities, etc



THING_ID = 0
THING_FLAGS = 1
THING_ID_PLAYER = 0


walls =[

    # Top LeftX and Y, End X and Y
    [(0,0), (256, 128)],
    [(0,0), (-256, -256)]
    ,
    
    ]





# FOV Code
FOV = 150
FOV_Rad = radians(FOV)
CONST_ANGLE_PER_PIXEL = radians(FOV/DEFAULT_WIDTH) # Used for Beam RayCaster; how many degrees is a pixel
FarZ = 32768 # After this many units, stop tracing the raycas

while True:

    SCREEN_DISPLAY.fill(COLPAL[0])
    for event in pygame.event.get():
        
        if event.type == pygame.KEYDOWN:
            if event.key == K_a:
                MovingLeft = True
            if event.key == K_d:
                MovingRight = True
            if event.key == K_w:
                MovingUp = True
            if event.key == K_s:
                MovingDown = True
            if event.key == K_SPACE:
                Jumping = True
            if event.key == K_LCTRL:
                Crouching = True
            if event.key        == K_RETURN:
                FPS_MouseFocus = not FPS_MouseFocus
                
        if event.type == pygame.KEYUP:
            if event.key == K_a:
                MovingLeft = False
            if event.key == K_d:
                MovingRight = False
            if event.key == K_w:
                MovingUp = False
            if event.key == K_s:
                MovingDown = False
            if event.key == K_LCTRL:
                Crouching = False

        if event.type == VIDEORESIZE:
            if not FullScreen:
                SCREEN_WIDTH    = event.w
                SCREEN_HEIGHT   = event.h
                
                if SCREEN_WIDTH > MAX_WIDTH:
                    SCREEN_WIDTH = MAX_WIDTH
                
                if SCREEN_HEIGHT > MAX_HEIGHT:
                    SCREEN_HEIGHT = MAX_HEIGHT
                    
                
                SAVED_WIDTH     = SCREEN_WIDTH
                SAVED_HEIGHT    = SCREEN_HEIGHT
                
                TRUE_DISPLAY      = pygame.display.set_mode((SAVED_WIDTH, SCREEN_HEIGHT), FLAGS_RESIZABLE)

        if event.type == QUIT:
            pygame.quit()
            quit()
            print ("Thanks for playing!")


    CurrentFPS = GAME_CLOCK.get_fps()
    if CurrentFPS > GAME_FPS:
        CurrentFPS = GAME_FPS
    FPSRatio = 1 #GAME_FPS / (CurrentFPS + 1 )

    
    

    # Mouse Move
    if FPS_MouseFocus:
        pygame.mouse.set_pos(SCREEN_HalfX, SCREEN_HalfY)
        Mouse_CurrentX, Mouse_CurrentY = pygame.mouse.get_pos()
        Mouse_RelX  = SCREEN_HalfX - Mouse_CurrentX
        Mouse_RelY  = SCREEN_HalfY - Mouse_CurrentY
        Player_Pitch -= Mouse_RelX/1024

                
    # Game stores Pitch/Yaw as Radians; therefore, Pi Pitch/Yaw = 180Deg
    if Player_Pitch > tau:
        Player_Pitch = 0
    elif Player_Pitch < 0:
        Player_Pitch = tau


    
    Player_Speed = int (Player_BaseSpeed / (Player_Crouch_Height/Player_Height) * FPSRatio)
    Player_XMove = cos(Player_Pitch) * Player_Speed# Get Rotation of Player and Mult by this amount
    Player_ZMove = sin(Player_Pitch) * Player_Speed

    # If 0 - 90 Degrees
    # MovingLeft = -X, +Z

    if Player_Pitch > 0 and Player_Pitch < Rotate_90Deg:
        None
    elif Player_Pitch > Rotate_90Deg and Player_Pitch < pi:
        None
    elif Player_Pitch > pi and Player_Pitch < Rotate_270Deg:
        None
    elif Player_Pitch > Rotate_270Deg and Player_Pitch < tau:
        None

    # If 90 - 180
    # MovingLeft = +Z, +X

    # If 180 - 270
    # MovingLeft = +X, -Z

    # If 270 - 360
    # MovingLeft = -Z, -X
    if MovingLeft:
        Player_XPos -= Player_XMove
        Player_ZPos -= Player_ZMove
    if MovingRight:
        Player_XPos += Player_XMove
        Player_ZPos += Player_ZMove
    if MovingUp:
        Player_XPos += Player_ZMove
        Player_ZPos -= Player_XMove
    if MovingDown:
        Player_XPos -= Player_ZMove
        Player_ZPos += Player_XMove
        

    # Jump Code
    if Jumping:
        Gravity += 0.05
        Gravity *= 1.02
        Player_YPos += 5 - Gravity


    # TODO - Get current sector's floorpos instead of 0 #
    if Player_YPos <= 0:
        Gravity     = 0
        Player_YPos = 0
        Jumping     = False
        
    
    if Crouching:
        if not Jumping:
            Player_Height -= 4
            if Player_Height < Player_Crouch_Height:
                Player_Height = Player_Crouch_Height
            
    else:
        Player_Height += 4
        if Player_Height > Player_Stand_Height:
            Player_Height = Player_Stand_Height


    # We'll do a fake 3D below is the old algorithm
    


    # Translate and Draw Walls #



    

    
    
    # Translate and Draw Floors #

##    SECTOR_TYPE = 0
##    SECTOR_POS = 1
##    SECTOR_DIM = 2
##    SECTOR_FLOORY = 3   # Get YPos of Floor Plane
##    SECTOR_CEILY = 4    # Get YPos of Ceiling Plane
##    SECTOR_THING = 5    # Thing Info, list entities, etc
    
    for wall in range (len(walls)):
        Start = (walls[wall][0][0] - Player_XPos , walls[wall][0][1] - Player_ZPos)
        End = (walls[wall][1][0] - Player_XPos , walls[wall][1][1] - Player_ZPos)
        #pygame.draw.line(SCREEN_DISPLAY, (COLPAL[254]), Start, End)

    # Copy Pasted Code, show a Cone of FOV   
    radar = (DEFAULT_WIDTH//2,DEFAULT_HEIGHT//2)
    radar_len = 64

    # Ray Caster Time!
    # For each pixel, we draw a straight line until we find a collision
    # If we find a collision, draw vertical columns
    # Draw back to front
    # If we find multiple collisions, we draw back to front
    # If we hit Void or FarZ, stop drawing the line

    for pixel in range (DEFAULT_WIDTH):

        # Triangular Distance Displacement to Fake FOV
        if pixel != 0:
            CPixel = FOV_Rad / (DEFAULT_WIDTH/pixel)
            if CPixel > 1:
                CPixel = 1 - (CPixel-1)
        else:
            CPixel = 0
        
        
    
        #+ (CONST_ANGLE_PER_PIXEL * pixel)
        rayX = radar[0] + cos((Player_Pitch - Rotate_90Deg) - FOV_Rad/2 + (CONST_ANGLE_PER_PIXEL * pixel) ) * FarZ
        rayY = radar[1] + sin((Player_Pitch - Rotate_90Deg) - FOV_Rad/2 + (CONST_ANGLE_PER_PIXEL * pixel) ) * FarZ

        
        
        # To work out if two lines intersect, we work out both lines Equations
        # Here's a Magic Hack I stole from someone translated from OG JavaScript Below
##            var lineSegmentsIntersect = (x1, y1, x2, y2, x3, y3, x4, y4) => {
##            var a_dx = x2 - x1;
##            var a_dy = y2 - y1;
##            var b_dx = x4 - x3;
##            var b_dy = y4 - y3;
##            var s = (-a_dy * (x1 - x3) + a_dx * (y1 - y3)) / (-b_dx * a_dy + a_dx * b_dy);
##            var t = (+b_dx * (y1 - y3) - b_dy * (x1 - x3)) / (-b_dx * a_dy + a_dx * b_dy);
##            return (s >= 0 && s <= 1 && t >= 0 && t <= 1);


        for wall in range (len(walls)):


            
            lineSegmentsIntersect = (radar[0], radar[1], rayX, rayY, walls[wall][0][0] - Player_XPos, walls[wall][0][1] - Player_ZPos, walls[wall][1][0] - Player_XPos, walls[wall][1][1] - Player_ZPos)
            
            a_dx = lineSegmentsIntersect[2] - lineSegmentsIntersect[0]
            a_dy = lineSegmentsIntersect[3] - lineSegmentsIntersect[1]
            b_dx = lineSegmentsIntersect[6] - lineSegmentsIntersect[4]
            b_dy = lineSegmentsIntersect[7] - lineSegmentsIntersect[5]
            s = (-a_dy * (lineSegmentsIntersect[0] - lineSegmentsIntersect[4]) + a_dx * (lineSegmentsIntersect[1] - lineSegmentsIntersect[5])) / (-b_dx * a_dy + a_dx * b_dy)
            t = (b_dx * (lineSegmentsIntersect[1] - lineSegmentsIntersect[5]) - b_dy * (lineSegmentsIntersect[0] - lineSegmentsIntersect[4])) / (-b_dx * a_dy + a_dx * b_dy)

            
            if (s > 0 and s <= 1 and t > 0 and t <= 1):
                # Emulate inverse straight lines by doing a single curve over the screen and fix it back

                # To work it out, we draw straight lines from the center of the screen

                # The FOV is 180 - Sum of 2 Angles
                # For example, if I draw 2 45deg lines from the center to the edges
                # The FOV is 90
                # Distance Factor =  1/tan(FOV * 0.5)

                # Distance Factor = Multi of Bars at edge of screen
                # Height of Wall = DEFAULT_HEIGHT / DistFactor
                # Slope Normal = Half Screen Width / (LineHeight/2)

                # Objects at the center are projected infinitely away
                # 


                # Work out WHERE the line intersected
                rayZ = (FarZ * t)


                

                # Work out how far away the Ray is based on it's Z Depth
                ZDepth = (FarZ/rayZ)
                
                if ZDepth > DEFAULT_HEIGHT:
                    ZDepth = DEFAULT_HEIGHT

                #ZDepth = sin(FOV_Rad * ZDepth)

                # Top Down Space Coords need to be converted to 3D Space Coordinates
                rayX = radar[0] + cos((Player_Pitch - Rotate_90Deg) - FOV_Rad/2 + (CONST_ANGLE_PER_PIXEL * pixel) ) * rayZ
                rayY = radar[1] + sin((Player_Pitch - Rotate_90Deg) - FOV_Rad/2 + (CONST_ANGLE_PER_PIXEL * pixel) ) * rayZ

                distX = rayX - Horizon_XPos
                distY = rayY - Horizon_YPos

                # Draw Line Tests
                if pixel == 0:
                    SCREEN_DISPLAY.blit(GAME_FONT.render("LD: " +str( ZDepth ) , 0, (255, 255, 240), 0, ), (0, 150) )
                elif pixel == DEFAULT_WIDTH//2:
                    SCREEN_DISPLAY.blit(GAME_FONT.render("MD: " +str( ZDepth ) , 0, (255, 255, 240), 0, ), (0, 180) )
                elif pixel == DEFAULT_WIDTH - 1:
                    SCREEN_DISPLAY.blit(GAME_FONT.render("RD:" +str( ZDepth ) , 0, (255, 255, 240), 0, ), (0, 210) )

                pygame.draw.line(SCREEN_DISPLAY, (0, 0, 255), (pixel, DEFAULT_HEIGHT//2 - (ZDepth//2)), (pixel, DEFAULT_HEIGHT//2 + (ZDepth//2)), 1)
                

            
                # Draw Center Lines
                '''
                if pixel in range(DEFAULT_WIDTH//2 - 2, DEFAULT_WIDTH//2 + 2):
                    pygame.draw.line(SCREEN_DISPLAY, (192, 192, 192), (Horizon_XPos, Horizon_YPos ), (rayX, rayY) , 1)
                else:
                    pygame.draw.line(SCREEN_DISPLAY, (96, 96, 96), (Horizon_XPos, Horizon_YPos ), (rayX, rayY) , 1)
                '''

            else:
                pass
                #pygame.draw.line(SCREEN_DISPLAY, (32, 32, 32), (Horizon_XPos, Horizon_YPos ), (rayX, rayY) , 1)

            

            
            #rayX, ZDepth = rotate2D((rayX,rayY), Player_Pitch)
            
            #rotate2D((rayX, rayY) , ZDepth)


            

            

            
            

            # TO draw a line that takes up part of the screen, we do
            # Take X + Y of the line's cutoff position and divide by ZDist


    ##            if LineDist == 0:
    ##
    ##                
    ##                pygame.draw.line(SCREEN_DISPLAY, (0, 0, 255), (pixel, 0 ), (pixel, DEFAULT_HEIGHT), 1)
    ##                
    ##            else:
    ##
    ##                LineScale =  FarZ - LineDist
    ##                
    ##                pygame.draw.line(SCREEN_DISPLAY, (0, 0, 255), (pixel, FarZ/LineDist ), (pixel, DEFAULT_HEIGHT - (FarZ/LineDist)), 1)
    ##        else:
    ##            pass
    ##            #pygame.draw.line(SCREEN_DISPLAY, (255, 0, 0) , radar , (rayX, rayY), 1)
    ##

        #pygame.draw.rect(SCREEN_DISPLAY, (255, 255, 240) , (Horizon_XPos - Player_Hitbox_Width // 2 , Horizon_YPos - Player_Hitbox_Height // 2, Player_Hitbox_Width, Player_Hitbox_Height) , 1)
        

    # Left Side of FOV
    x = radar[0] + cos((Player_Pitch - FOV_Rad)) * radar_len
    y = radar[1] + sin((Player_Pitch - FOV_Rad)) * radar_len
    #pygame.draw.line(SCREEN_DISPLAY, (255, 255, 0) , radar, (x,y), 1)

    # Middle of FOV
    x = radar[0] + cos((Player_Pitch - Rotate_90Deg)    ) * radar_len
    y = radar[1] + sin((Player_Pitch - Rotate_90Deg)    ) * radar_len
    #pygame.draw.line(SCREEN_DISPLAY, (255, 255, 0) , radar, (x,y), 1)   

    # Right Side of FOV
    x = radar[0] + cos( (Player_Pitch + FOV_Rad)) * radar_len
    y = radar[1] + sin( (Player_Pitch + FOV_Rad)) * radar_len
    #pygame.draw.line(SCREEN_DISPLAY, (255, 255, 0) , radar, (x,y), 1)



    
    if not FPS_MouseFocus:
        SCREEN_DISPLAY.blit(TEX_PALETTE, (DEFAULT_WIDTH - TEX_PALETTE.get_width(), 0))
        MCol = list(TRUE_DISPLAY.get_at(pygame.mouse.get_pos()))
        del MCol[3]
        
        COL_TEXT = GAME_FONT.render("COL " +str(COLPAL.index(TRUE_DISPLAY.get_at(pygame.mouse.get_pos()     ))) +" - " +str(MCol)  , 0, COL_WHITE, 0 )
        SCREEN_DISPLAY.blit(COL_TEXT, (DEFAULT_WIDTH - COL_TEXT.get_width(), TEX_PALETTE.get_height() + Debug_Height ))
    ''' Debug Information '''     
    SCREEN_DISPLAY.blit(GAME_FONT.render("FPS? " +str(int(CurrentFPS))+"/"+str(GAME_FPS) +" GT? " +str(Global_Timer) +" FPS RAT? " +str(FPSRatio), 0, COL_WHITE, 0), (0, 0))
    SCREEN_DISPLAY.blit(GAME_FONT.render("X" +str(round(Player_XPos,4)) +" Y" +str(round(Player_YPos,4)) +" Z" +str(round(Player_ZPos, 4)), 0, COL_WHITE, 0), (0, Debug_Height))
    SCREEN_DISPLAY.blit(GAME_FONT.render("JMP? " +str(Jumping) +" GRV? " +str(round(Gravity, 4)) +" CRCH? " +str(Crouching) +" HGT? " +str(Player_Height) , 0, COL_WHITE, 0), (0, Debug_Height * 2))
    SCREEN_DISPLAY.blit(GAME_FONT.render("PCH? " +str(round(Player_Pitch,3))  +" RLL? " +str(round(Player_Roll, 3)), 0, COL_WHITE, 0), (0, Debug_Height * 3))
    SCREEN_DISPLAY.blit(GAME_FONT.render("AX? " +str(round(degrees(Player_Pitch),3))  +" AZ? " +str(round(degrees(Player_Roll), 3)), 0, COL_WHITE, 0), (0, Debug_Height * 4))
    SCREEN_DISPLAY.blit(GAME_FONT.render("MSP? " +str(pygame.mouse.get_pos()) , 0, COL_WHITE, 0), (0, Debug_Height * 5))
    
    ''' Screen Renderer '''
    SCREEN_DISPLAY      = pygame.transform.scale(SCREEN_DISPLAY, (SCREEN_WIDTH, SCREEN_HEIGHT))
    TRUE_DISPLAY.blit(SCREEN_DISPLAY, (0,0))
    SCREEN_DISPLAY      = pygame.transform.scale(SCREEN_DISPLAY, (DEFAULT_WIDTH, DEFAULT_HEIGHT))
    pygame.display.flip()
    
    GAME_CLOCK.tick(GAME_FPS)
    Global_Timer += 1
    
