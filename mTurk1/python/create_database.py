import logging
from mTurk1.python.database_functions import generate_experiment, check_lists
import sys
logger = logging.getLogger('django')




#Takes experiment_settings and attempts to create the corresponding database

def create_experiment(experiment_settings):         
    logger.debug("create_experiment")
    logger.info("ATTEMPT: get names and lists from experiment_settings")
        
    sim_name=experiment_settings.sim_name
    exp_name=experiment_settings.exp_name
    agent_list=experiment_settings.agent_list
    sim_list=experiment_settings.sim_list
    view_list=experiment_settings.view_list
      
    logger.info("OK: get names and lists from experiment settings")
    #Check that theres only 1 sim and 1 agent
    
    logger.info("ATTEMPT: Check lists are valid")
    valid_lists=check_lists(sim_list,agent_list,view_list)
    if all(list is True for list in valid_lists):
        logger.info("OK: All lists valid")
    else:
        logger.error("FAILED: Invalid lists. Lists labeled false are invalid. Sim: %s ; Agent: %s; View: %s" %(valid_lists[0],valid_lists[1], valid_lists[2]))
        sys.exit(1)
      
    generate_experiment(sim_list,agent_list,view_list,sim_name,exp_name)

   





#===============================================================================
#Main
#===============================================================================      
if __name__ == "__main__":
    
    #get settings file
    from mTurk1.simulations.sim_test_1.configExp2 import ExperimentSettings
    #TRY: get settings from ExperimentSettings module
    experiment_settings=ExperimentSettings
    
    logger.info("Running: create_database") 
    create_experiment(experiment_settings)
    logger.info("Finished: create_database, successful")
    
    
    
