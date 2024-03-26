# TrajectoryOfProjectile
What Does This Do?
-
This program calculates the trajectory of a projectile based on its location in the world using Visual Crossing's Weather API.
It usues the average daily weather prediction of that day as it does use the weather forecast for the next 15 days including today. (16 days total)

Hardcoded into calcD function is 0.6 and 0.0446831364. 0.6 is the drag coefficient of a basketball along with 0.0446831364 being the reference area of a basketball. The projectile in this case is a basketball, however, it can be any weight you want it to be and travel as fast as you want. If you wanted to change the object, you would need to change these two numbers to your specifications.

Variables used to calculate the trajectory:
- Humidity
- Temperature
- Wind speed
- Wind direction
- Initial velocity
- Weight
- Angle at initial velocity

Output
- In terminal the program outputs the x and y coordinates every .1s the projectile travels
- At the end of the program it will take you to a graph displaying the trajectory of the projectile

Purpose
-
Purpose of this project is to gain experience using weather APIs and
using that information to calculate the x and y coordinates of the projectile.

How to Use
-
Create an account with Visual Crossing and get your API key in 'Account Details'

In run.sh
1. replace 'city' with city you want to launch in.
2. replace 'API_KEY' with your API key

In terminal
1. run chmod +x ./run.sh
2. run ./run.sh
3. input data

To get today's weather input 0 in the days into the days input
  
Warning
-
Inputting data with large gaps between weight and velocity may cause 
a high amount of CPU usage and may take awhile or not finish if your computer is not high performing.
