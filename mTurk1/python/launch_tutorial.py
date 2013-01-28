#Script to be run from the command line



# set up the environment using the settings module
import logging
#Set up logger.
logger = logging.getLogger('django')
import sys
sys.path=(['/home/qwertyfinger/webapps/crowd_web/crowd_web'])+sys.path
from django.core.management import setup_environ
from crowd_web import settings
setup_environ(settings)



import argparse
from create_tutorial import create_tutorial
from mTurk1.models import  Simulation

#Setup the Django settings environment settings.
#Change from <my_site> import settings
#from django.core.management import setup_environ
#from crowd_web import settings
#setup_environ(settings)






#Set up command line arguments. These are required postional arguments
parser=argparse.ArgumentParser()
parser.add_argument("sim_folder", help="name of specific simulation folder in simulations folder")
parser.add_argument("config",help="Name of config file in specific simulation folder")
args=parser.parse_args()


#Create string from command line arguments
config_import='mTurk1.simulations.'+args.sim_folder+'.'+args.config


logger.info("Looking for TutorialSettings in: %s" %config_import)
_temp=__import__(config_import, globals={}, locals={}, fromlist=['TutorialSettings'], level=-1)
TutorialSettings=_temp.TutorialSettings
logger.info("Found TutorialsSettings")
tutorial_name=TutorialSettings.tutorial_name

#Check if experiment_name exists.
try:
    tutorial_exists=Simulation.objects.filter(simulation_name=tutorial_name).exists()   
except:
    logger.error("Could not check for existence of tutorial Name: %s" %tutorial_name)
    
#Check if Experiment exists. If it does, do nothing. If it doesn't then create Experiment
if args.mode==1:
    if tutorial_exists:
        logger.info("Tutorial %s already exists" %tutorial_name)
    else:
        logger.info("Experiment does not exist. Running create_tutorial")
        result=create_tutorial(TutorialSettings)
        
        logger.info("OK: CREATED TUTORIAL")


