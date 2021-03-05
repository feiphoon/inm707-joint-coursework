import numpy as np
from maze import Maze
from maze import step


class TD_Learning():
    
    def __init__(self, Maze, alpha, gamma):
        
        self.maze_environment = Maze.size
        self.alpha = alpha
        self.gamma = gamma
        self.generation_start_coords = Maze.generation_start_coords
        self.values = np.zeros( (self.maze_environment*self.maze_environment) )

    #TODO I need to change this i am not sure how this works yet

    def update_values(self, s_current, reward_next, s_next -->next_position):
        
        self.values[s_current] = self.values[s_current] + self.alpha * ( reward_next + self.gamma*self.values[s_next] - self.values[s_current] )
        
    def display_values(self) -> None:
        
        value_matrix = np.zeros( (self.maze_environment, self.maze_environment) )

    
        for i in range(self.maze_environment):
            for j in range(self.maze_environment):

                state = self.generation_start_coords[i, j]
                
                value_matrix[i,j] = self.values[state]
                
        return value_matrix


     #TODO completing the TD_learning_episode
     def TD_learning_episode(TD, Maze):   
          s = 
          self.done 

          while not done:
              action = 
              s_next, r, done = 
              TD.update_values()

              s = s.next


        