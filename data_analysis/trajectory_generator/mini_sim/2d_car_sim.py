#
# Tom's Pong
# A simple pong game with realistic physics and AI
# http://www.tomchance.uklinux.net/projects/pong.shtml
#
# Released under the GNU General Public License
from kzpy3.data_analysis.trajectory_generator.beacon_navigator.driver import Beacon_Driver
import rospy
from geometry_msgs.msg._Vector3 import Vector3
from marvelmind_nav.msg import hedge_pos as hedge_pos_msg
from marvelmind_nav.msg import beacon_pos_a as beacon_pos_a_msg

VERSION = "0.4"

try:
    import sys
    import random
    import math
    import os
    import getopt
    import pygame
    from socket import *
    from pygame.locals import *
    import numpy as np
except ImportError, err:
    print "couldn't load module. %s" % (err)
    sys.exit(2)

width = 1024
height = 768

def load_png(name):
    """ Load image and return image object"""
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
        if image.get_alpha is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except pygame.error, message:
        print 'Cannot load image:', fullname
        raise SystemExit, message
    return image, image.get_rect()


class Car(pygame.sprite.Sprite):

    def __init__(self, side):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png('car.png')
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.side = side
        self.speed = 10
        self.heading = 0
        self.state = "still"
        self.reinit()

    def reinit(self):
        self.state = "still"
        self.movepos = [width/2, height/2]
        if self.side == "left":
            self.rect.midleft = self.area.midleft
        elif self.side == "right":
            self.rect.midright = self.area.midright

    def update(self):
        newpos = self.rect.move(self.movepos)

        if self.area.contains(newpos):
            self.rect = newpos
        pygame.event.pump()

    def move_forward(self):
        self.movepos = [np.cos(self.heading) * (self.speed) , np.sin(self.heading) * (self.speed)]
        self.state = "moveup"
        
    def turn_left(self):
        self.heading += np.pi/12.
        self.state = "moveup"

    def turn_right(self):
        self.heading -= np.pi/12.
        self.state = "movedown"


def main():
    # Initialise screen
    pygame.init()

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Basic Pong')

    # Fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((255, 255, 255))

    # Initialise players
    global player1
   
    player1 = Car("car")

    # Initialise sprites
    playersprites = pygame.sprite.RenderPlain(player1)

    # Blit everything to the screen
    screen.blit(background, (0, 0))
    pygame.display.flip()

    # Initialise clock
    clock = pygame.time.Clock()

    beacon_driver = Beacon_Driver()
    
    hedge_pub = rospy.Publisher("/bair_car/hedge_pos", hedge_pos_msg, queue_size=10)
    beacon_pub = rospy.Publisher("/bair_car/beacons_pos_a", beacon_pos_a_msg,queue_size=10)
    heading_pub = rospy.Publisher("/bair_car/gyro_heading", Vector3,queue_size=10)
    
    rospy.init_node('hedge_tester', anonymous=True)
    
    
    
    i = 0
    
    
    # Event loop
    while 1:
        # Make sure game doesn't run at more than 60 frames per second
        clock.tick(10)
            
        i += 1
        
        if i % 10 == 0:
            beacon_pos1 = beacon_pos_a_msg(1,0.0,0.0,0.0)
            beacon_pos2 = beacon_pos_a_msg(2,3.0,0.0,0.0)
            beacon_pos3 = beacon_pos_a_msg(3,0.0,3.0,0.0)
            beacon_pos4 = beacon_pos_a_msg(4,3.0,3.0,0.0)
            
            beacon_pub.publish(beacon_pos1)
            beacon_pub.publish(beacon_pos2)
            beacon_pub.publish(beacon_pos3)
            beacon_pub.publish(beacon_pos4)
        
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN:
                if event.key == K_UP:
                    player1.move_forward()
                if event.key == K_LEFT:
                    player1.turn_left()
                if event.key == K_RIGHT:
                    player1.turn_right()
            elif event.type == KEYUP:
                if event.key == K_UP or event.key == K_DOWN:
                    player1.movepos = [0,0]
                    player1.state = "still"

        pos_x = (player1.rect[0] * 3.0) / width
        pos_y = (player1.rect[1] * 3.0) / height         

        hedge_heading = np.rad2deg(player1.heading)

        hedge_pos = hedge_pos_msg(i,pos_x,pos_y,0.0,0)
        hedge_heading = Vector3(80.0,0.0,0.0)
        
        hedge_pub.publish(hedge_pos)
        heading_pub.publish(hedge_heading)
        
        beacon_driver.get_steer_motor_cmd()

        screen.blit(background, player1.rect, player1.rect)
        playersprites.update()
        playersprites.draw(screen)
        pygame.display.flip()


if __name__ == '__main__': main()
