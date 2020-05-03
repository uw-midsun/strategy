# Strategy
A repository of the models and race strategy developed for MSXIV (and beyond!)
## What's here
 - Expected Solar Energy
 - A model of the car's energy consumption
 - A model of motor efficiency
 - A battery efficiency model
 - A SOC model
 - Our optimization strategy

## Getting Started
- Make sure Python3 is installed on your system (open a command prompt and type python3, you should be brought to an interactive Python session)
- Run pip3 install -r requirements (make sure you are in the code's directory)
- To make sure everything is up and working, run pytest from the command line. This should run a number of tests. If they all pass, you're all set to go!
- After making changes, be sure to run pytest before committing to make sure your changes haven't broken any tests. If they have, go fix them!

## How do I contribute?
 - Clone the repository (if you're unsure about this part, message Clarke VandenHoven on Slack)
 - Find a ticket on the JIRA board that sounds interesting (https://uwmidsun.atlassian.net/jira/software/projects/STRAT/boards/12)
 - If your task is not currently on the JIRA, create and assign yourself a ticket, and put the ticket under the appropriate Epic
 - Move onto a new branch and call it what you're trying to address (e.g. dynamicsfixes)
 - Make your changes locally and commit them
 - In your commit message, lead off with the ticket you're addressing (i.e. "STRAT-31 Creating a tutorial")
 - Push the changes to an upstream branch
 - Open a PR and it will be reviewed
 - If your PR has not been reviewed within 24 hours, copy the link and paste it into the gen-strategy channel on Slack

## Questions?
Message Clarke VandenHoven on Slack.

## Resources
- https://githowto.com/
- https://www.python.org/about/gettingstarted/
- https://docs.scipy.org/doc/numpy/user/quickstart.html
- https://uwmidsun.atlassian.net/wiki
