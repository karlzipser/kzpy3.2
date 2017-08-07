'''
Created on May 8, 2017

@author: picard
'''
from omgtools import *
from kzpy3.data_analysis.trajectory_generator.trajectory_tools import *
import cv2
import sys
import matplotlib.pyplot as plt


framerate = 1. / 30.
show_situation = True
# This framerate should be at one point for the whole module

def get_state(own_xy, timestep_start, timestep_end):

    # Init our own position
    init_xy = own_xy[timestep_start]
         
    # Get our intended heading based on three timesteps in the future
    # which add as slight smoothing
    heading = get_heading(own_xy[timestep_start:timestep_start + timestep_end])
    # Get the velocity over the first two timesteps
    velocity = get_velocities([own_xy[timestep_start], own_xy[timestep_start + 1]], framerate)
    return init_xy, heading, velocity

def sample_result_to_trajectory(values, no_of_samples):
    
    if len(values) == no_of_samples:
        return values
    if len(values) < no_of_samples:
        raise NotImplementedError("The case that there are less trajectory points has not been implemented")
    else:
        n = len(values)
        m = no_of_samples
        # substract one for the 0 value which we want to have
        index = [i * n // m + n // (2 * m) for i in range(m)]
        index.pop(len(index) - 1)
        index.insert(0, 0)
        
        return values[index]
    

def get_evasive_trajectory(own_xy, other_xy, timestep_start, plan_horizon, d_timestep_goal):
    '''
    Returns a short term evasion trajectory, in steering commands for 
    as many timesteps ahead as given in between timestep_start and timestep_ahead.
    Note that the trajectory will start one timestep further than timestep_start because
    one timestep is needed to retrieve information about the start conditions
     
    FOR NOW, OTHER_XY IS ONLY ONE OTHER VEHICLE    
    '''
    
    init_xy_own, heading_own, velocity_own = get_state(own_xy, timestep_start, 4)  # smooth heading over 3 timesteps in the future

    goal_xy, goal_heading, goal_velocity = get_state(own_xy, timestep_start + d_timestep_goal, 4) 
    
      
    # make and set-up vehicle
    vehicle = Bicycle(length=0.4, options={'plot_type': 'car', 'substitution': False})  # Holonomic(shapes=Circle(0.25))
    vehicle.define_knots(knot_intervals=2)
    
    velocity_abs = np.hypot(velocity_own[0][0], velocity_own[0][1])
    
    # plan from the last known position
    vehicle.set_initial_conditions(state=[init_xy_own[0], init_xy_own[1], heading_own, 0.0])  # the assumption is that 
    # for the time being that the steering angle is 0. This can be changed in the future, based on existing data.

    # plan as if the current movement should be continued
    # little tweak, heading_own = terminal heading
    vehicle.set_terminal_conditions([goal_xy[0], goal_xy[1], heading_own])
    vehicle.set_options({'safety_distance': 0.2})
    
    print goal_xy
    print goal_heading
    print init_xy_own 
    print heading_own
    # make and set-up environment #TODO
    environment = Environment(room={'shape': Square(15.)})
    
    # get velocities of other vehicles
    # other_positions = other_xy[timestep_start:timestep_start+process_timesteps]
    
    init_xy_other, heading_other, velocity_init_other = get_state(other_xy, timestep_start, 4)
    end_xy_other, end_heading_other, velocity_end_other = get_state(other_xy, timestep_start + plan_horizon - 2, timestep_start + plan_horizon - 1)
    
    obstacle_start_time = 0.
    obstacle_end_time = plan_horizon * (1. / 30.)
    

    traj = {'velocity': {'time': [obstacle_start_time, obstacle_end_time],
                     'values': [velocity_init_other, velocity_end_other]}}
    # sys.exit(0)
    environment.add_obstacle(Obstacle({'position': np.array(init_xy_other)}, shape=Circle(0.25),
        simulation={'trajectories': traj}))
    
    # print(np.array(init_xy_other))
    # sys.exit(0)
    # create a point-to-point problem
    problem = Point2point(vehicle, environment, freeT=True)
    
    problem.set_options({'solver_options':
    {'ipopt': {'ipopt.hessian_approximation': 'limited-memory'}}})
    
    problem.init()
     
    # simulate, plot some signals and save a movie
    simulator = Simulator(problem, sample_time=1. / 30., update_time=1. / 30.)
    
    # vehicle.plot('input', labels=['v_x (m/s)', 'v_y (m/s)'])
    # problem.plot('scene')
    if show_situation:
    #    plt.close("all")
        problem.plot('scene')
#     vehicle.plot('input', knots=True, labels=['v (m/s)', 'ddelta (rad/s)'])
#    vehicle.plot('state', knots=True, labels=[
#                  'x (m)', 'y (m)', 'theta (rad)', 'delta (rad)'])
#     if vehicle.options['substitution']:
#         vehicle.plot('err_pos', knots=True)
#         vehicle.plot('err_dpos', knots=True)

    
    # Right now a very simple behaviour will only calculate the 
    # trajectory once    
    simulation_steps = 1
        
    simulator.deployer.reset()
    
    for i in range(0, simulation_steps):
        simulator.update()
        simulator.update_timing()
    
    # return trajectories and signals
    trajectories, signals = {}, {}
    for vehicle in simulator.problem.vehicles:
        trajectories[str(vehicle)] = vehicle.traj_storage
        signals[str(vehicle)] = vehicle.signals
    
    
    return sample_result_to_trajectory(vehicle.traj_storage['delta'][0][0], plan_horizon)
    
if __name__ == '__main__':

    pass
    
