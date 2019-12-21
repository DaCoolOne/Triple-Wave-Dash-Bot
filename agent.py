
"""
    Main bot code. If you are looking for the actual triple wave dash function,
    please head to actions.py
"""


from rlbot.agents.base_agent import BaseAgent
from rlbot.utils.game_state_util import GameState, BallState, Physics, Vector3

from structs import *
from actions import *

# Rendering is commented out.
class Bowtie(BaseAgent):
    
    def initialize_agent(self):
        self.packet = Packet()
        self.controller_state = None
        self.action = None
        self.maneuver = Action()
        self.maneuver_complete = True
        self.has_removed_ball = False
    
    def set_maneuver(self, a):
        self.maneuver_complete = False
        self.maneuver = a
    
    def get_output(self, gtp):
        
        # self.renderer.begin_rendering()
        
        if not self.has_removed_ball:
            ball_state = BallState(Physics(location=Vector3(0, 0, 3000)))
            game_state = GameState(ball=ball_state)
            self.set_game_state(game_state)
            self.has_removed_ball = True
        
        self.controller_state = Controller()
        self.packet.update(gtp)
        
        if self.action is None:
            self.action = Test_Maneuver()
        
        my_car = self.packet.game_cars[self.index]
        
        if self.maneuver_complete:
            self.action = self.action.update(self, self.packet)
            # self.renderer.draw_string_3d(my_car.location.UI_Vec3(), 2, 2, type(self.action).__name__, self.renderer.yellow())
        else:
            
            self.action.idle(self, self.packet)
            
            self.maneuver_complete = self.maneuver.update(self, self.packet)
            # self.renderer.draw_string_3d(my_car.location.UI_Vec3(), 2, 2, type(self.maneuver).__name__, self.renderer.red())
        
        # self.renderer.end_rendering()
        
        return self.controller_state.get()
        
    
