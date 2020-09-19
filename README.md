# Strategy
This is the Midnight Sun Strategy subteam repository. This contains all of the models and race strategy developed for MSXIV (and beyond!)

## What's here
 - Auxilary energy loss
 - Expected Solar Energy
 - A model of the car's energy consumption
 - A model of motor efficiency
 - A battery efficiency model
 - Model for race route and tracks
 - The SOC model
 - Our optimization strategy
 - Visualization of displays of our data
 
 ## Projects
 - Car Dynamics Model - Modelling the dynamic forces applied to the car 
 - Solar Energy Model - How much power is being obtained via the solar array
 - State of Charge (SoC) - Current battery and energy levels
 - Race Route and Track Planning - Determine the energy needs for the hills, turns and stops of the race route given external conditions
 - Optimization - What is the least amount of energy we can use given the route, weather and cary dynamics
 - Visualization - Dashboard interface for our models and graphs

## Getting Started
- Make sure Python3 is installed on your system (open a command prompt and type `python3` or `py`, you should be brought to an interactive Python session). If it's not, download the latest release at [here](https://www.python.org/downloads/). NOTE: Python 3.8 currently breaks our builds. Install Python 3.6 or 3.7
- Clone this repository by running `git clone https://github.com/uw-midsun/strategy.git`. This creates a local copy of code for you to make changes to.
- Navigate into the new folder with `cd strategy` and then run `pip3 install -r requirements` to download the python packages. If this doesn't work, try `py -3 -m pip install -r requirements.txt`.
- To make sure everything is up and working, run `pytest` from the command line. This should run a number of tests. If they all pass, you're all set to go!
- After making changes, be sure to run `pytest` before committing to make sure your changes haven't broken any tests. If they have, go fix them!
- If you've never used Git/GitHub before, read through [this tutorial](https://githowto.com/). All changes are made locally in a branch, committed, and pushed to the remote repository once completed. Then, go to [Github](https://github.com/uw-midsun/strategy/pulls) and open a new pull request ([PR](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/about-pull-requests)), which is requesting approval to merge the changes into the master branch. 
- Message Emma Wai on [Slack](https://uwmidsun.slack.com/) to say hello!

## How do I contribute?
Follow the instructions in [this document](https://docs.google.com/document/d/1l-6X7z27WU_xnj855kbdWLo3vj63uLxffjoZZrtylUU/edit?usp=sharing).
 - Join #gen-strategy on Slack
 - Follow the steps in the above Getting Started section to set up the repository on your computer
 - Message Emma or Michael (Shio) on Slack for a task/ticket on the JIRA board (https://uwmidsun.atlassian.net/jira/software/projects/STRAT/boards/12)
 - Fork the repository to a new branch. Try to name the branch something that summarizes the change or the ticket name
 - Move to the branch and make your changes locally. Finish and commit
 - In your commit message, lead off with the ticket you're addressing (i.e. "STRAT-31 Creating a tutorial")
 - Push the changes to an upstream branch
 - Open a Pull Request to the strategy repository and detail your changes. The PR will be reviewed by other team members.
 - If your PR has not been reviewed within 24 hours, copy the link and paste it into the gen-strategy channel on Slack.

## Questions?
Message Emma Wai or Michael Shiozaki on Slack.

## Additional Resources
- https://githowto.com/
- https://www.python.org/about/gettingstarted/
- https://docs.scipy.org/doc/numpy/user/quickstart.html
- https://uwmidsun.atlassian.net/wiki

## Onboarding Hello!
List your name here:
- Emma Wai
- Aryaman Singh
