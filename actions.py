
from constants import GAME_SPEED
from rlbot.utils.game_state_util import GameState, GameInfoState

from controller import *
from extra_math import *
from structs import *

# Base action class
class Action:
    def update(self, agent, packet):
        raise NotImplementedError
    # Idle is called when a maneuver has precedence over an action.
    def idle(self, agent, packet):
        pass

# Base maneuver class
class Maneuver:
    def update(self, agent, packet):
        raise NotImplementedError

# This is the heart of the function. Tweaking these values should give one
# an idea of how tight the windows are for some of these movements.
class Triple_Dash(Maneuver):
    def __init__(self):
        self.first_frame = True
        self.has_done_micro_jump = False
        self.forward = Vec3()
        self.start_location = Vec3()
        self.stage = 0
        self.start = 0
    
    def update(self, agent, packet):
        my_car = packet.game_cars[agent.index]
        
        # The first part of this function could probably be its own maneuver, but I'm too lazy to do that.
        # This performs the initial jump to set up the micro jump.
        if not self.has_done_micro_jump:
            if self.first_frame:
                self.first_frame = False
                self.start = packet.game_info.seconds_elapsed
                agent.controller_state.jump = True
                
                game_info_state = GameInfoState(game_speed=GAME_SPEED)
                
                game_state = GameState(game_info=game_info_state)
                
                agent.set_game_state(game_state)
            
            delta = packet.game_info.seconds_elapsed - self.start
            
            if my_car.location.z < 17 and delta > 0.7:
                self.has_done_micro_jump = True
                self.first_frame = True
            
        else:
            if self.first_frame:
                self.first_frame = False
                
                self.start = packet.game_info.seconds_elapsed
                self.start_location = my_car.location
                self.forward = Vec3(1).align_to(my_car.rotation).flatten().normal()
                self.side = Vec3(self.forward.y, -self.forward.x)
                
                # One frame jump
                agent.controller_state.jump = True
                
            
            # Calulate delta time
            delta = packet.game_info.seconds_elapsed - self.start
            
            # Boost through everything
            agent.controller_state.boost = True
            
            # Handbrake!
            agent.controller_state.handbrake = self.stage >= 2
            
            # The actual logic. More branches than an oak tree, but, ya know...
            if delta < 0.35:
                Align_Car_To(agent, packet, self.forward, Vec3(0, 0, 1))
            elif delta < 0.74:
                Align_Car_To(agent, packet, self.forward + self.side * 0.25 + Vec3(0, 0, 1), Vec3(0, 0, 1))
            elif self.stage < 1:
                self.stage += 1
                agent.controller_state.jump = True
                agent.controller_state.pitch = -1
                agent.controller_state.yaw = 0
                agent.controller_state.roll = -0.4
                agent.controller_state.steer = 0
            elif delta < 1:
                agent.controller_state.roll = -1
            elif self.stage < 2:
                self.stage += 1
                agent.controller_state.jump = True
                agent.controller_state.pitch = -1
                agent.controller_state.yaw = 1
                agent.controller_state.roll = 1
                agent.controller_state.steer = 0
            elif delta < 1.2:
                agent.controller_state.roll = 1
            elif self.stage < 3:
                self.stage += 1
                agent.controller_state.jump = True
                agent.controller_state.pitch = -1
                agent.controller_state.yaw = -1
                agent.controller_state.roll = -1
                agent.controller_state.steer = 0
            elif delta < 3:
                drive(agent, packet, my_car.location + my_car.velocity)
                agent.controller_state.boost = False
            else:
                # How to exit the maneuver
                return True
            
            return False
            
        

# Responsible for testing stuff
class Test_Maneuver(Action):
    
    def __init__(self):
        pass
    
    def update(self, agent, packet):
        
        # Drives to the middle of the field, stops, then runs the triple wave dash thingy.
        my_car = packet.game_cars[agent.index]
        drive(agent, packet, Vec3())
        
        if Vec3(1).align_to(my_car.rotation).dot(my_car.location.normal()) < -0.95:
            agent.controller_state.boost = False
            agent.controller_state.throttle = 0
            
            if my_car.velocity.length() <= 0.5:
                agent.set_maneuver(Triple_Dash())
        
        return self
    
