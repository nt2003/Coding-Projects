"""
Models module for Planetoids

This module contains the model classes for the Planetoids game. Anything that 
you interact with on the screen is model: the ship, the bullets, and the 
planetoids.

We need models for these objects because they contain information beyond the 
simple
shapes like GImage and GEllipse. In particular, ALL of these classes need a 
velocity representing their movement direction and speed (and hence they all 
need an additional attribute representing this fact). But for the most part, 
that is all they need. You will only need more complex models if you are adding 
advanced features like scoring.

You are free to add even more models to this module. You may wish to do this 
when you add new features to your game, such as power-ups. If you are unsure 
about whether to make a new class or not, please ask on Ed Discussions.

# Nicolas Trejo (nt286)
# 12/5/2022
"""
from consts import *
from game2d import *
from introcs import *
import math

# PRIMARY RULE: Models are not allowed to access anything in any module other 
#than
# consts.py. If you need extra information from Gameplay, then it should be a 
# parameter in your method, and Wave should pass it as a argument when it calls 
# the method.

# START REMOVE
# HELPER FUNCTION FOR MATH CONVERSION
def degToRad(deg):
    """
    Returns the radian value for the given number of degrees
    
    Parameter deg: The degrees to convert
    Precondition: deg is a float
    """
    return math.pi*deg/180
# END REMOVE


class Bullet(GEllipse):
    """
    A class representing a bullet from the ship
    
    Bullets are typically just white circles (ellipses). The size of the bullet 
    is determined by constants in consts.py. However, we MUST subclass GEllipse,
    because we need to add an extra attribute for the velocity of the bullet.
    
    The class Wave will need to look at this velocity, so you will need getters 
    for the velocity components. However, it is possible to write this 
    assignment with no setters for the velocities. That is because the velocity
    is fixed and cannot change once the bolt is fired.
    
    In addition to the getters, you need to write the __init__ method to set the
    starting velocity. This __init__ method will need to call the __init__ from
    GEllipse as a helper. This init will need a parameter to set the direction 
    of the velocity.
    
    You also want to create a method to update the bolt. You update the bolt by 
    adding the velocity to the position. While it is okay to add a method to 
    detect collisions in this class, you may find it easier to process 
    collisions in wave.py.

    Attribute x: the x position of the center of the bullet.
    Invariant: x is an int>=0
    
    Attribute y: the y position of the center of the bullet
    Invariant: y is an int>=0
    """
    # LIST ANY ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    # Attribute _velocity: The direction and speed the bullet is travelling
    # Invariant: _velocity is a Vector2 object

    # Attribute _direction: The direction the bullet is facing
    # Invariant: _direction is a Vector2 object

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def get_x(self):
        """This is a getter for the x position of the center of the bullet"""
        return self.x
    
    def get_y(self):
        """This is a getter for the y position of the center of the bullet"""
        return self.y
    
    def get_direction(self):
        """This is a getter for the direction of the bullet"""
        return self._direction
    
    def get_velocity(self):
        """This is a getter for the velocity of the bullet"""
        return self._velocity
    
    # INITIALIZER TO SET THE POSITION AND VELOCITY
    def __init__(self,x, y, ang, facing):
        """This is the  initializer for the Bullet Class

        Parameter x: The x value for the center of the bullet
        Precondition: x is an int>=0.

        Parameter y: The y value for the center of the bullet
        Precondition: y is an int>=0.

        Parameter ang: The angle that the bullet will shoot at
        Precondition: ang is an angle in radians.
        
        Parameter facing: The direction that the ship is facing
        Precondition: facing is a vector.
        """
        x_pos= (facing.x *SHIP_RADIUS) +x
        y_pos= (facing.y*SHIP_RADIUS) +y
        super().__init__(x=x_pos,y=y_pos, height= (BULLET_RADIUS*2),\
        width=(BULLET_RADIUS*4), fillcolor= BULLET_COLOR, ang=ang)
        self._velocity= facing.__mul__(BULLET_SPEED)
        self._direction= ang

    # ADDITIONAL METHODS (MOVEMENT, COLLISIONS, ETC)
    def upd_pos(self):
        """This is a method that updates the position of the Bullet"""

        self.x= self.x + self._velocity.x
        self.y= self.y + self._velocity.y
    

class Ship(GImage):
    """
    A class to represent the game ship.
    
    This ship is represented by an image. The size of the ship is determined by 
    constants in consts.py. However, we MUST subclass GEllipse, because we need 
    to add an extra attribute for the velocity of the ship, as well as the 
    facing vecotr (not the same) thing.
    
    The class Wave will need to access these two values, so you will need 
    getters for them. But per the instructions,these values are changed 
    indirectly by applying thrust or turning the ship. That means you won't 
    want setters for these attributes, but you will want methods to apply 
    thrust or turn the ship.
    
    This class needs an __init__ method to set the position and initial facing 
    angle.This information is provided by the wave JSON file. Ships should start
    with a shield
    enabled.
    
    Finally, you want a method to update the ship. When you update the ship, you
    apply the velocity to the position. While it is okay to add a method to 
    detect collisions in this class, you may find it easier to process 
    collisions in wave.py.

    Attribute x: the x position of the center of the ship.
    Invariant: x is an int>=0
    
    Attribute y: the y position of the center of the ship
    Invariant: y is an int>=0

    Attribute angle: the angle that the ship is facing
    Invariant: angle is an angle in degrees
    """
    # LIST ANY ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY

    # Attribute _velocity: The direction and speed the ship is travelling
    # Invariant: _velocity is a Vector2 object

    # Attribute _facing: The direction the ship is facing
    # Invariant: _facing is a Vector2 object

    # Attribute _impulse: The force times the time
    # Invariant: _impulse is a Vector2 object

    # Attribute _ang: The angle that the ship is pointing in
    # Invariant: _ang is an 0<= int <= 360.

    

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def get_velocity(self):
        """This is a getter for the velocity of the ship"""
        return self._velocity
    
    def get_facing(self):
        """This is a getter for the facing of the ship"""
        return self._facing
    
    def get_impulse(self):
        """This is a getter for the impulse of the ship"""
        return self._impulse
    
    def get_x(self):
        """This is a getter for the x position of the center of the ship"""
        return self.x
    
    def get_y(self):
        """This is a getter for the y position of the center of the ship"""
        return self.y
    
    def get_ang(self):
        """This is a getter for the angle the Ship is pointing at."""
        return self._ang
    
    # INITIALIZER TO CREATE A NEW SHIP
    def __init__(self, x, y, ang):
        """This is the Initializer for the Ship Class
        
        Parameter x: The x position of the ship
        Precondition: x is an int >= 0.

        Parameter y: The y position of the ship
        Precondition: y is an int >= 0.

        Parameter ang: The angle that the ship is pointing in
        Precondition: ang is an 0<= int <= 360.

        """
        
        super().__init__(x=x,y=y, height= (SHIP_RADIUS*2),\
        width=(SHIP_RADIUS*2), source= SHIP_IMAGE, angle=ang)
        self._velocity= introcs.Vector2(x=0,y=0)
        rad= (ang *math.pi)/180
        self._facing=  introcs.Vector2(math.cos(rad),math.sin(rad))
        self._ang= ang
        self.x=x
        self.y=y
        
    # ADDITIONAL METHODS (MOVEMENT, COLLISIONS, ETC)
    def turn(self, da):
        """This is a method that turns the ship
        
        Parameter da: The amount the angle is being changed by in degrees
        Precondition: da is an int >= 0.
        """
        assert isinstance(da, int)
        self.angle= self.angle+ da
        rad= (self.angle * math.pi)/180
        self._facing=  introcs.Vector2(math.cos(rad),math.sin(rad))         

    def add_impulse(self):
        """This is a method that increments the velocity by impulse"""
        
        self._impulse= self._facing.__mul__(SHIP_IMPULSE)
        self._velocity= self._velocity + self._impulse
        if self._velocity.length() >= SHIP_MAX_SPEED:
            self._velocity= (Vector2.normalize(self._velocity)).__mul__\
            (SHIP_MAX_SPEED)
        
    def upd_pos(self):
        """This is a method that updates the position of the ship"""
        self.x= self.x + self._velocity.x
        self.y= self.y + self._velocity.y
        
    def wrap(self):
        """This is a method that wraps the ship around the screen"""
        if self.x < -DEAD_ZONE:
            self.x= self.x + (GAME_WIDTH + 2*DEAD_ZONE)
        if self.x > GAME_WIDTH + DEAD_ZONE:
            self.x= self.x - (GAME_WIDTH + 2*DEAD_ZONE)
        if self.y < -DEAD_ZONE:
            self.y= self.y + (GAME_HEIGHT + 2*DEAD_ZONE)
        if self.y > GAME_WIDTH + DEAD_ZONE:
            self.y= self.y - (GAME_HEIGHT + 2*DEAD_ZONE)
    
            
class Asteroid(GImage):
    """
    A class to represent a single asteroid.
    
    Asteroids are typically are represented by images. Asteroids come in three 
    different sizes (SMALL_ASTEROID, MEDIUM_ASTEROID, and LARGE_ASTEROID) that 
    determine the choice of image and asteroid radius. We MUST subclass GImage,
    because we need extra attributes for both the size and the velocity of the
    asteroid.
    
    The class Wave will need to look at the size and velocity, so you will need
    getters for them.  However, it is possible to write this assignment with no 
    setters for either of these. That is because they are fixed and cannot 
    change when the planetoid is created. 
    
    In addition to the getters, you need to write the __init__ method to set 
    the size and starting velocity. Note that the SPEED of an asteroid is 
    defined in const.py, so the only thing that differs is the velocity 
    direction.
    
    You also want to create a method to update the asteroid. You update the 
    asteroid by adding the velocity to the position. While it is okay to add 
    a method to detect collisions in this class, you may find it easier to 
    process collisions in wave.py.
    """
    pass
    # LIST ANY ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    # Attribute _size: The size of the asteroid
    # Invariant: _size is either small, medium or large

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def get_x(self):
        """This is a getter for the x position of the center of the asteroid"""
        return self.x
    
    def get_y(self):
        """This is a getter for the y position of the center of the asteroid"""
        return self.y
    
    def get_velocity(self):
        """This is a getter for the velocity of the asteroid"""
        return self._velocity
    
    def get_direction(self):
        """This is a getter for the direction that the asteroid is pointing"""
        return self._direction
    
    def get_size(self):
        """This is a getter for the size of the asteroid"""
        return self._size
    
    def get_radius(self):
        """This is a getter for the radius of the asteroid"""
        return self._radius
    
    # INITIALIZER TO CREATE A NEW ASTEROID
    def __init__(self, radius, position, source, speed,direction,size):
        """This is the initializer for the Asteroid class

        Parameter radius: The radius of the asteroid
        Precondition: radius is an int >= 0.

        Parameter position: The position that the asteroid should be placed
        Precondition: position is a tuple of int>=0

        Parameter source: The image of the asteroid
        Precondition: source is a string.

        Parameter direction: The direction that the asteroid should move
        Precondition: direction is a tuple of int.

        Parameter size: The size of the asteroid image
        Precondition: size is a string.

        """
        super().__init__(x=position[0],y=position[1], height= (radius*2),\
        width=(radius*2), source= source)
        if direction==[0,0]:
            self._velocity= (Vector2(0,0))
        else:
            self._velocity=introcs.Vector2(x=direction[0],y=direction[1])
            self._velocity= (Vector2.normalize(self._velocity)).__mul__(speed)
        self._size= size
        self._direction= direction
        if size== "small":
            self._radius= SMALL_RADIUS
        if size== "medium":
            self._radius= MEDIUM_RADIUS
        if size== "large":
            self._radius= LARGE_RADIUS
       
    # ADDITIONAL METHODS (MOVEMENT, COLLISIONS, ETC)
    def upd_pos(self):
        """This is a method that updates the position of the Asteroid"""
        
        self.x= self.x + self._velocity.x
        self.y= self.y + self._velocity.y
         
    def wrap(self):
        """This is a method that wraps the asteroid around the screen"""
        if self.x < -DEAD_ZONE:
            self.x= self.x + (GAME_WIDTH + 2*DEAD_ZONE)
        if self.x > GAME_WIDTH + DEAD_ZONE:
            self.x= self.x - (GAME_WIDTH + 2*DEAD_ZONE)
        if self.y < -DEAD_ZONE:
            self.y= self.y + (GAME_HEIGHT + 2*DEAD_ZONE)
        if self.y > GAME_WIDTH + DEAD_ZONE:
            self.y= self.y - (GAME_HEIGHT + 2*DEAD_ZONE)
    
    # IF YOU NEED ADDITIONAL MODEL CLASSES, THEY GO HERE
