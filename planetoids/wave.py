"""
Subcontroller module for Planetoids

This module contains the subcontroller to manage a single level (or wave) in the 
Planetoids game.  Instances of Wave represent a single level, and should 
correspond to a JSON file in the Data directory. Whenever you move to a new 
level, you are expected to make a new instance of the class.

The subcontroller Wave manages the ship, the asteroids, and any bullets on 
screen. These are model objects. Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or models.py.
Whether a helper method belongs in this module or models.py is often a 
complicated issue.  If you do not know, ask on Ed Discussions and we will answer
.

# Nicolas Trejo (nt286)
# 12/5/2022
"""
from game2d import *
from consts import *
from models import *
import random
import datetime

# PRIMARY RULE: Wave can only access attributes in models.py via getters/setters
# Level is NOT allowed to access anything in app.py (Subcontrollers are not 
#permitted
# to access anything in their parent. To see why, take CS 3152)

class Wave(object):
    """
    This class controls a single level or wave of Planetoids.
    This subcontroller has a reference to the ship, asteroids, and any bullets 
    on screen.It animates all of these by adding the velocity to the position 
    at each step. It checks for collisions between bullets and asteroids or 
    asteroids and the ship (asteroids can safely pass through each other). A
    bullet collision either breaks up or removes a asteroid. A ship collision 
    kills the player. 
    
    The player wins once all asteroids are destroyed.  The player loses if they
    run out of lives. When the wave is complete, you should create a NEW 
    instance of Wave (in Planetoids) if you want to make a new wave of 
    asteroids.
    
    If you want to pause the game, tell this controller to draw, but do not
    update.  See subcontrollers.py from Lecture 25 for an example.  This class
    will be similar to than one in many ways.
    
    All attributes of this class are to be hidden. No attribute should be 
    accessed without going through a getter/setter first. However, just because
    you have an attribute does not mean that you have to have a getter for it.
    For example, the Planetoids app probably never needs to access the 
    attribute for the bullets, so there is no need for a getter there. But at a
    minimum, you need getters indicating
    whether you one or lost the game.
    """
    # LIST ANY ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    # THE ATTRIBUTES LISTED ARE SUGGESTIONS ONLY AND CAN BE CHANGED AS YOU SEE 
    #FIT
    # Attribute _data: The data from the wave JSON, for reloading 
    # Invariant: _data is a dict loaded from a JSON file
    #
    # Attribute _ship: The player ship to control 
    # Invariant: _ship is a Ship object
    #
    # Attribute _asteroids: the asteroids on screen 
    # Invariant: _asteroids is a list of Asteroid, possibly empty
    #
    # Attribute _bullets: the bullets currently on screen 
    # Invariant: _bullets is a list of Bullet, possibly empty
    #
    # Attribute _lives: the number of lives left 
    # Invariant: _lives is an int >= 0
    #
    # Attribute _firerate: the number of frames until the player can fire again 
    # Invariant: _firerate is an int >= 0
    #
    # Attribute _pewSound: the sound object for the bullets
    # Invariant: _pewSound is an instance of Sound
    #
    # Attribute _explosionSound: the sound object for the when the ship explodes
    # Invariant: _explosionSound is an instance of Sound
    
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getdata(self):
        """This is a getter method for the data about the wave"""
        return self._data
    
    def getship(self):
        return self._ship
    
    def getasteroids(self):
        return self._asteroids
    
    def getlives(self):
        return self._lives
    
    # INITIALIZER (standard form) TO CREATE SHIP AND ASTEROIDS
    def __init__(self,json= DEFAULT_WAVE):
        """This is the  initializer for the Wave Class

        Parameter json: The dictionary contining information about the level
        Precondition: json is a dictionary.
        """
        self._pewSound = Sound('pew1.wav')
        self._explosionsound= Sound('explosion.wav')
        self._lives= 2
        self._data= json
        ship_dict= self.getdata()["ship"]
        ship_x= ship_dict["position"][0]
        ship_y= ship_dict["position"][1]
        shipang= ship_dict["angle"]
        self._ship= Ship(ship_x, ship_y, shipang)
        self._asteroids= []
        self._bullets= []
        self._firerate= 0
        asteroid_data= self.getdata()["asteroids"]
        for i in range(len(asteroid_data)):
            cur_ast_dic= asteroid_data[i]
            if cur_ast_dic["size"] == "large":
                cur_ast_rad= LARGE_RADIUS
                cur_ast_source= LARGE_IMAGE
                cur_ast_speed= LARGE_SPEED
            if cur_ast_dic["size"] == "medium":
                cur_ast_rad= MEDIUM_RADIUS
                cur_ast_source= MEDIUM_IMAGE
                cur_ast_speed= MEDIUM_SPEED
            if cur_ast_dic["size"] == "small":
                cur_ast_rad= SMALL_RADIUS
                cur_ast_source= SMALL_IMAGE
                cur_ast_speed= SMALL_SPEED
            self._asteroids= self._asteroids +[Asteroid(cur_ast_rad, \
            cur_ast_dic["position"], cur_ast_source, cur_ast_speed, \
            cur_ast_dic["direction"], cur_ast_dic["size"])]

    # UPDATE METHOD TO MOVE THE SHIP, ASTEROIDS, AND BULLETS
    def update(self, input):
        """This is the method that updates the Wave Class

        Parameter input: The Input class from planetoids
        Precondition: input is a class.
        """
        if self._ship != None:
            da= 0
            if input.is_key_down('up') == True:
                self._ship.add_impulse()
            if input.is_key_down('left') == True:
                da= da+ SHIP_TURN_RATE
                self._ship.turn(da)
            if input.is_key_down('right') == True:
                da= da- SHIP_TURN_RATE
                self._ship.turn(da)
            if(input.is_key_down('spacebar'))and self._firerate>=BULLET_RATE:
                self._firerate= 0
                self._bullets= self._bullets +[Bullet(self._ship.get_x(),self\
                ._ship.get_y(), self._ship.get_ang(), self._ship.get_facing())]
                self._pewSound.play()
            self._ship.upd_pos()
            self._ship.wrap()
            self._firerate = self._firerate +1
            for x in range(len(self._bullets)):
                self._bullets[x].upd_pos()
            ii=0
            while ii < len(self._bullets):
                if (self._bullets[ii].x > GAME_WIDTH+DEAD_ZONE)or\
                (self._bullets[ii].y > GAME_WIDTH + DEAD_ZONE):
                    del self._bullets[ii]
                else:
                    ii= ii +1
            self._det_col()
            
    # DRAW METHOD TO DRAW THE SHIP, ASTEROIDS, AND BULLETS
    def draw(self,view):
        """This is a method to draw the ship
        
        Parameter view: This represents the canvas that will be drawn on.
        Precondition: view is provided in the method call through planetoids..
        """
        if self._ship != None:
            self._ship.draw(view)
        for x in range(len(self._asteroids)):
            if self._asteroids != []:
                self._asteroids[x].draw(view)
        for y in range(len(self._bullets)):
            self._bullets[y].draw(view)
   
    # HELPER METHODS FOR PHYSICS AND COLLISION DETECTION
    def _det_col(self):
        """This is a helper method that detects colision and resolves it"""
        i=0
        num= len(self._bullets)
        while i in range(len(self._bullets)):
            x=0
            while x < len(self._asteroids) and (num == len(self._bullets)):
                if math.dist([self._bullets[i].get_x(),self._bullets[i].get_y()\
                ],[self._asteroids[x].get_x(), self._asteroids[x].get_y()])\
                < (BULLET_RADIUS + self._asteroids[x].get_radius())*2:  
                    self._break_up(self._asteroids[x],self._bullets[i])
                    del self._asteroids[x]
                    del self._bullets[i]
                else:
                    x=x+1
            i=i+1
        i=0
        while i < (len(self._asteroids)) and self._ship != None:
            if math.dist([self._ship.get_x(),self._ship.get_y()],\
            [self._asteroids[i].get_x(), self._asteroids[i].get_y()]) < \
            (SHIP_RADIUS + self._asteroids[i].get_radius()):
                self._break_up(self._asteroids[i],self._ship)
                del self._asteroids[i]
                self._ship = None
                self._explosionsound.play()
            else:
                self._asteroids[i].upd_pos()
                self._asteroids[i].wrap()
                i=i+1
          
    def _break_up(self,ast,ext):
        """This is a helper method that breaks up/ destroys the asteroids when 
        collided with."""

        size_list= ["small", "medium", "large"]
        if ast.get_size()== "medium":
            used_size_num=0
            used_rad= SMALL_RADIUS
            used_source= SMALL_IMAGE
            used_speed= SMALL_SPEED
        if ast.get_size() == "large":
            used_size_num=1
            used_rad= MEDIUM_RADIUS
            used_source= MEDIUM_IMAGE
            used_speed= MEDIUM_SPEED
        if ast.get_size() != "small":
            self.help_break_up(ast,ext,used_size_num,used_rad,used_source,\
            used_speed,size_list)
                
    def help_break_up(self,ast,ext,used_size_num,used_rad,used_source,\
        used_speed,size_list):
        """This is helper method for the _break_up method to break up the
        asteroids
        """
        if isinstance(ext,Bullet)or (isinstance(ext,Ship)and \
            ext.get_velocity() != Vector2(0,0)):
            col_vector= Vector2.normalize(ext.get_velocity())
        if isinstance(ext, Ship) and ext.get_velocity() == Vector2(0,0):
            col_vector= Vector2.normalize(ext.get_facing())
        res_vector1_x= (col_vector.x *math.cos(2*(math.pi)/3)- col_vector.y * \
        math.sin(2*(math.pi)/3))
        res_vector1_y= ((col_vector.x *math.sin(2*(math.pi)/3)+ col_vector.y *\
        math.cos(2*(math.pi)/3)))
        res_vector1= introcs.Vector2(res_vector1_x,res_vector1_y)
        res_vector1= Vector2.normalize(res_vector1)
        res_vector2_x= (col_vector.x *math.cos(4*(math.pi)/3)- col_vector.y * \
        math.sin(4*(math.pi)/3))
        res_vector2_y= ((col_vector.x *math.sin(4*(math.pi)/3)+ col_vector.y * \
        math.cos(4*(math.pi)/3)))
        res_vector2= introcs.Vector2(res_vector2_x,res_vector2_y)
        res_vector2= Vector2.normalize(res_vector2)
        pos_col_vector_x= ((used_rad*col_vector.x)+ast.get_x())
        pos_col_vector_y= (used_rad*col_vector.y)+ast.get_y()
        pos_col_vector= (pos_col_vector_x,pos_col_vector_y)
        pos_res1_vector_x= (used_rad*res_vector1_x)+(ast.get_x())
        pos_res1_vector_y= (used_rad*res_vector1_y)+ast.get_y()
        pos_res1_vector= (pos_res1_vector_x,pos_res1_vector_y)
        pos_res2_vector_x= (used_rad*res_vector2_x)+(ast.get_x())
        pos_res2_vector_y= (used_rad*res_vector2_y+ast.get_y())
        pos_res2_vector= (pos_res2_vector_x,pos_res2_vector_y)
        self.help_help_break_up(used_rad,pos_col_vector,pos_res1_vector, \
        pos_res2_vector,col_vector,res_vector1_x, res_vector1_y,res_vector2_x,\
        res_vector2_y,used_source, used_speed, size_list,used_size_num)
        
    def help_help_break_up(self,used_rad,pos_col_vector,pos_res1_vector, \
    pos_res2_vector, col_vector,res_vector1_x, res_vector1_y, res_vector2_x, \
    res_vector2_y,used_source, used_speed, size_list, used_size_num):
        """This is a helper method that helps help_break_up
        """
        self._asteroids.append(Asteroid(used_rad,pos_col_vector,used_source, \
        used_speed,[col_vector.x,col_vector.y], size_list[used_size_num] ))
        self._asteroids.append(Asteroid(used_rad,pos_res1_vector,used_source, \
        used_speed,[res_vector1_x,res_vector1_y], size_list[used_size_num] ))
        self._asteroids.append(Asteroid(used_rad,pos_res2_vector,used_source, \
        used_speed,[res_vector2_x,res_vector2_y], size_list[used_size_num] ))

    def _re_init_ship_(self):
        """This is a method that rests the ship after a life has been lost
        """
        ship_dict= self.getdata()["ship"]
        self._shippos= ship_dict["position"]
        ship_x= self._shippos[0]
        ship_y= self._shippos[1]
        shipang= ship_dict["angle"]
        self._ship= Ship(ship_x, ship_y, shipang)
        self._lives= self._lives-1
        

           