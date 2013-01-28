from mTurk1.python.database_functions import process_tutorial_settings,\
    generate_experiment, check_lists, generate_tutorial
import logging
import sys
from mTurk1.models import Experiment_group, Tutorial_instance, Simulation
logger = logging.getLogger('django')


def create_tutorial(tutorial_settings, experiment_name=None):
    #Process tutorial settings
    
    tutorial_name=tutorial_settings.tutorial_name
    agent_list=tutorial_settings.agent_list
    view_list=tutorial_settings.view_list
    sim_list=tutorial_settings.sim_list
    
    logger.info("ATTEMPT: Check lists are valid")
    valid_lists=check_lists(sim_list,agent_list,view_list)
    if all(list is True for list in valid_lists):
        logger.info("OK: All lists valid")
    else:
        logger.error("FAILED: Invalid lists. Lists labeled false are invalid. Sim: %s ; Agent: %s; View: %s" %(valid_lists[0],valid_lists[1], valid_lists[2]))
        sys.exit(1)
                
    #Check if the tutorial settings has only 1 view
    number_of_views=len(view_list)
    if number_of_views!=1:       
        logger.error("Tutorials can only have 1 view associated with them at present.")
        sys.exit(1) 
           
    #Check if tutorial name exists
    tutorial_name_exists=Simulation.objects.filter(simulation_name=tutorial_name).exists()
    if tutorial_name_exists:
        logger.error("There already exists a tutorial_instance named %s" %tutorial_name)
        sys.exit(1)    
    #If user does not supply experiment name then try to strip "_tutorial" from the experiment_name, and use that 
    #if experiment_name==None:
        #logger.info("ATTEMPT experiment_name arg not provided. Attempting to strip '_tutorial' from %s" %tutorial_settings[4])
        #try:
            #tutorial_name=tutorial_settings[4]
            #if tutorial_name.endswith('_tutorial'):
                #experiment_name=tutorial_name[:-len('_tutorial')]
                #logger.info("OK experiment_name defined as: %s" %experiment_name)
            #else:
                #raise
        #except:
            #logger.error("No experiemnt_name provided, and could not strip '_tutorial' from end of %s." %tutorial_settings[4])
            #sys.exit(1)    
    #Check if experiment exists:
    #experiment_name_exists=Experiment_group.objects.filter(name=experiment_name).exists()        
    #join mode only works if the experiment exists    
    #if create_mode=='join':
        #if experiment_name_exists:
            #try:
                #generate_experiment(*tutorial_settings)
            #except:
                #logger.exception("Could not generate experiment")
                #sys.exit(1)
        #else:
            #logger.error("The experiment name:%s ,does not exist as Experiment_group" %experiment_name)
            #sys.exit(1)
    generate_tutorial(sim_list, agent_list, view_list, tutorial_name)
            
    
       
    
    

if __name__ == "__main__":

    from mTurk1.simulations.sim_test_1.configTutorial import TutorialSettings as tutorial_settings    
    create_tutorial(tutorial_settings)