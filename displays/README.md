Directory for generate graphs to visualize SOC and velocity profiles.

## SOC_velocity_graph.py
Methods to generate graph of state of charge and speed against time travelled. See https://www.mdpi.com/2071-1050/9/10/1576/htm for reference for the curve generated.

### `calculate_SOC_values(v_profile, e_profile, distance, initial_soc, min_speed=None, max_speed=None)`
+ Instantiates Car object (from car_model.py) and ColoumbCounter object (from SoCEstimation.py) object to energy_used calculation and monitoring SOC levels.
+ Accepts v_profile, e_profile following parameter specifications in energy_used method. distance is a list of distances that we travel each speed in v_profile. initial_soc is a decimal representing the initial battery state (ie. 1 means fully charged). Accepts min_speed and max_speed with default values of None; this specifies the parameters for Car object initialization.
+ Returns array of state of charges, starting with initial_soc, and state of charge at the end of each interval of velocity.
+ Find energy used between each velocity/elevation interval and add to array. Last point is energy_used maintaining the last given velocity for the given distance.

### `generate_SOC_graph(v_profile, e_profile, distance, initial_soc=1)`
+ Same parameters as above. Default value for initial_soc is fully charged, 1.
+ Produces graph; x-axis is distance travelled, starting at 0 and distances over each interval. 
+ Left y-axis is velocity step function in red; right-axis is state of charge of battery in blue.
+ Since step function is wanted where velocity is shown over the following interval, step function "post" mode is used, and added a point at beginning of v_profile before graphing to be 0.