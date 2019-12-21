

"""
    I don't recommend messing with these, not because it's messy
    but because it's completely unrelated to anything.
"""

from rlbot.agents.base_agent import SimpleControllerState
from rlbot.utils.structures.game_data_struct import Vector3 as UI_Vec3

from extra_math import *

import random

SLICE_RATE = 60
SLICE_TICK_RATE = 1/SLICE_RATE

"""
    THE WORLD'S BEST VECTOR CLASS
"""
class Vec3:
    def __init__(self, x=0, y=0, z=0):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
    
    def __add__(self, val):
        return Vec3(self.x + val.x, self.y + val.y, self.z + val.z)
    
    def __sub__(self, val):
        return Vec3(self.x - val.x, self.y - val.y, self.z - val.z)
    
    def __mul__(self, val):
        return Vec3(self.x * val, self.y * val, self.z * val)
    
    def sq_length(self):
        return self.x * self.x + self.y * self.y + self.z * self.z
    
    def length(self):
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)
    
    def set(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    def update(self, v):
        self.x = float(v.x)
        self.y = float(v.y)
        self.z = float(v.z)
    
    def align_to(self, rot):
        v = Vec3(self.x, self.y, self.z)
        v.set(v.x, math.cos(rot.roll) * v.y + math.sin(rot.roll) * v.z, math.cos(rot.roll) * v.z - math.sin(rot.roll) * v.y)
        v.set(math.cos(-rot.pitch) * v.x + math.sin(-rot.pitch) * v.z, v.y, math.cos(-rot.pitch) * v.z - math.sin(-rot.pitch) * v.x)
        v.set(math.cos(-rot.yaw) * v.x + math.sin(-rot.yaw) * v.y, math.cos(-rot.yaw) * v.y - math.sin(-rot.yaw) * v.x, v.z)
        return v
    
    def align_from(self, rot):
        v = Vec3(self.x, self.y, self.z)
        v.set(math.cos(rot.yaw) * v.x + math.sin(rot.yaw) * v.y, math.cos(rot.yaw) * v.y - math.sin(rot.yaw) * v.x, v.z)
        v.set(math.cos(rot.pitch) * v.x + math.sin(rot.pitch) * v.z, v.y, math.cos(rot.pitch) * v.z - math.sin(rot.pitch) * v.x)
        v.set(v.x, math.cos(-rot.roll) * v.y + math.sin(-rot.roll) * v.z, math.cos(-rot.roll) * v.z - math.sin(-rot.roll) * v.y)
        return v
    
    def UI_Vec3(self):
        return UI_Vec3(self.x, self.y, self.z)
    
    def copy(self):
        return Vec3(self.x, self.y, self.z)
    
    def flatten(self):
        return Vec3(self.x, self.y, 0)
    
    def normal(self, n = 1):
        l = n / max(self.length(), 0.0001)
        return Vec3(self.x * l, self.y * l, self.z * l)
    
    def tostring(self):
        return str(self.x) + "," + str(self.y) + "," + str(self.z)
    
    def cast(v):
        return Vec3(float(v.x), float(v.y), float(v.z))
    
    def dot(v1, v2):
        return v1.x*v2.x+v1.y*v2.y+v1.z*v2.z
    
    def cross(v1, v2):
        return Vec3(
            v1.y * v2.z - v1.z * v2.y,
            v1.z * v2.x - v1.x * v2.z,
            v1.x * v2.y - v1.y * v2.x
        )
    
    # Returns the angle between two vectors
    def angle_between(v1, v2):
        return math.acos(v1.normal().dot(v2.normal()))
    
    def angle_2d(self):
        return math.atan2(self.y, self.x)
    
    def lerp(v1, v2, t):
        return (v1 * (1-t) + v2 * t)

class Rotator:
    
    def __init__(self, yaw = 0, pitch = 0, roll = 0):
        self.yaw = yaw
        self.pitch = pitch
        self.roll = roll
    
    def cast(r):
        return Rotator(r.yaw, r.pitch, r.roll)
    
    def angle_between(r1, r2):
        return Vec3(1).align_to(r1).angle_between(Vec3(1).align_to(r2))
    
    def flatten(r):
        return Rotator(r.yaw)
    
    def copy(r):
        return Rotator(r.yaw, r.pitch, r.roll)
    
    def update(self, r):
        self.yaw = float(r.yaw)
        self.pitch = float(r.pitch)
        self.roll = float(r.roll)

class Box:
    
    def __init__(self, length = 0, width = 0, height = 0):
        self.length = length
        self.width = width
        self.height = height
    
    def cast(b):
        return Box(b.length, b.width, b.height)
    
    def update(self, b):
        self.length = float(b.length)
        self.width = float(b.width)
        self.height = float(b.height)
    
    def copy(self, c):
        return Box(self.length, self.width, self.height)
    

class Ball:
    def __init__(self):
        self.location = Vec3()
        self.velocity = Vec3()
        self.angular_velocity = Vec3()
        self.rotation = Rotator()
    
    def update(self, b):
        p = b.physics
        self.location.update(p.location)
        self.velocity.update(p.velocity)
        self.angular_velocity.update(p.angular_velocity)
        self.rotation.update(p.rotation)
    

class Car:
    def __init__(self, c):
        self.hitbox_offset = Vec3.cast(c.hitbox_offset)
        self.hitbox = Box.cast(c.hitbox)
        p = c.physics
        self.location = Vec3.cast(p.location)
        self.velocity = Vec3.cast(p.velocity)
        self.angular_velocity = Vec3.cast(p.angular_velocity)
        self.rotation = Rotator.cast(p.rotation)
        self.boost = c.boost
        self.team = c.team
        self.has_wheel_contact = c.has_wheel_contact
        self.is_demolished = c.is_demolished
    
    def update(self, c):
        p = c.physics
        self.location = Vec3.cast(p.location)
        self.velocity = Vec3.cast(p.velocity)
        self.angular_velocity = Vec3.cast(p.angular_velocity)
        self.rotation = Rotator.cast(p.rotation)
        self.boost = c.boost
        # self.team = c.team
        self.has_wheel_contact = c.has_wheel_contact
        self.is_demolished = c.is_demolished
        # self.hitbox = Box.cast(c.hitbox)

class GameInfo:
    def __init__(self):
        self.seconds_elapsed = 0
        self.is_round_active = False
        self.is_kickoff_pause = False
        self.world_gravity_z = 0
    
    def update(self, g):
        self.seconds_elapsed = g.seconds_elapsed
        self.is_round_active = g.is_round_active
        self.is_kickoff_pause = g.is_kickoff_pause
        self.world_gravity_z = g.world_gravity_z

class Packet:
    
    def __init__(self):
        self.game_ball = Ball()
        self.game_info = GameInfo()
        self.game_cars = []
    
    def update(self, packet):
        c_list = packet.game_cars
        self.game_info.update(packet.game_info)
        self.game_ball.update(packet.game_ball)
        if packet.num_cars == len(self.game_cars):
            for i in range(packet.num_cars):
                self.game_cars[i].update(c_list[i])
        else:
            self.game_cars = []
            for i in range(packet.num_cars):
                c = Car(c_list[i])
                self.game_cars.append(c)
    

class Controller:
    def __init__(self):
        self.steer = 0
        self.throttle = 0
        self.pitch = 0
        self.yaw = 0
        self.roll = 0
        self.jump = False
        self.boost = False
        self.handbrake = False
    
    def reset_direction(self):
        self.steer = 0
        self.pitch = 0
        self.yaw = 0
        self.roll = 0
    
    def get(self):
        return SimpleControllerState(
            clamp_1(self.steer),
            clamp_1(self.throttle),
            clamp_1(self.pitch),
            clamp_1(self.yaw),
            clamp_1(self.roll),
            self.jump,
            self.boost,
            self.handbrake,
        )
