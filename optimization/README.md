# Optimization

Directory for optimization-related files and modules. Optimization predicts the car's state throughout the race and calculates the velocity profile which would allow us to race most effectively (gaining the most number of points).

## In this directory

+ `tests` directory
+ `optimizer.py`: Initial optimization effort that loads in data about a route and tries to optimize velocity profile using scipy's `optimize`
+ `COTAelevation.txt`, `COTAelevation_var.txt`: Information on COTA (Course of the Americas)
