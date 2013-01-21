import argparse
from create_database import create_experiment_database
import logging
from mTurk1.models import Experiment_group

#for testing, remove when live
from mTurk1.simulations.sim_test_1.configExp import ExperimentSettings




#Set up logger.
logger = logging.getLogger('django')


#Set up command line arguments. These are required postional arguments
parser=argparse.ArgumentParser()
parser.add_argument("sim_folder", help="name of specific simulation folder in simulations folder")
parser.add_argument("config",help="Name of config file in specific simulation folder")
parser.add_argument("-m","--mode",help="The mode to operate in ",action="count", default=1)
args=parser.parse_args()


#Create string from command line arguments
config_import='mTurk1.simulations.'+args.sim_folder+'.'+args.config


logger.info("Looking for ExperimentSettings in: %s" %config_import)
_temp=__import__(config_import, globals={}, locals={}, fromlist=['ExperimentSettings'], level=-1)
ExperimentSettings=_temp.ExperimentSettings
logger.info("Found ExperimentSettings")
experiment_name=ExperimentSettings.exp_name

#Check if experiment_name exists.
try:
    experiment_exists=Experiment_group.objects.filter(name=experiment_name).exists()   
except:
    logger.error("Could not check for existence of Experiment Name: %s" %experiment_name)
    
#Check if Experiment exists. If it does, do nothing. If it doesn't then create Experiment
if args.mode==1:
    if experiment_exists:
        logger.info("Experiment %s already exists" %experiment_name)
    else:
        logger("Experiment does not exists. Running create_experiment_database")
        result=create_experiment_database(ExperimentSettings)
    #result=create_experiment_database(config_import)

