

"""
    Various controllers I use to make life easier.
"""

from constants import MAX_CAR_VEL
from structs import *
from extra_math import *

"""
    Aligns the car to a forward, up vector pair. If the up vector is not defined, then
    the function will simply keep the roof facing teh same way it has been facing.
"""
def Align_Car_To(self, packet, vector, up = Vec3()):
    
    my_car = packet.game_cars[self.index]
    
    car_rot = my_car.rotation
    
    car_rot_vel = my_car.angular_velocity
    
    local_euler = car_rot_vel.align_from(car_rot)
    
    align_local = vector.align_from(car_rot)
    
    local_up = up.align_from(car_rot)
    
    # Improving this
    rot_ang_const = 0.25
    stick_correct = 6.0
    
    a1 = math.atan2(align_local.y, align_local.x)
    a2 = math.atan2(align_local.z, align_local.x)
    
    if local_up.y == 0 and local_up.z == 0:
        a3 = 0.0
    else:
        a3 = math.atan2(local_up.y, local_up.z)
    
    yaw = correct(0.0, -a1 + local_euler.z * rot_ang_const, stick_correct)
    pitch = correct(0.0, -a2 - local_euler.y * rot_ang_const, stick_correct)
    roll = correct(0.0, -a3 - local_euler.x * rot_ang_const, stick_correct)
    
    self.controller_state.yaw = clamp_1(yaw)
    self.controller_state.pitch = clamp_1(pitch)
    self.controller_state.roll = clamp_1(roll)
    
    self.controller_state.steer = clamp_1(yaw)


"""
    It drives
"""
def drive(agent, packet, target, time = 0):
    my_car = packet.game_cars[agent.index]
    car_to_pos = target - (my_car.location - my_car.hitbox_offset.align_to(my_car.rotation))
    target_vel = car_to_pos.length() / not_zero(time) # * sign(my_car.velocity.dot(car_to_pos))
    actual_vel = my_car.velocity.dot(car_to_pos.normal())
    
    c_p_l = car_to_pos.align_from(my_car.rotation)
    
    up = Vec3(z=1).align_to(my_car.rotation)
    
    s_val = math.atan2(c_p_l.y, c_p_l.x)
    
    agent.controller_state.steer = clamp_1(s_val * 3)
    
    if abs(s_val) > math.pi * 0.4 and my_car.velocity.length() > 400 and up.z > 0.8:
        agent.controller_state.handbrake = True
        agent.controller_state.throttle = 1
    elif target_vel > actual_vel:
        agent.controller_state.throttle = 1
        agent.controller_state.boost = my_car.velocity.length() < MAX_CAR_VEL - 5 and my_car.has_wheel_contact
    elif target_vel > actual_vel + 100:
        agent.controller_state.throttle = 1
        agent.controller_state.boost = False
    elif target_vel > actual_vel + 400:
        agent.controller_state.throttle = 0.3
        agent.controller_state.boost = False
    else:
        agent.controller_state.throttle = 0
        agent.controller_state.boost = False
    





