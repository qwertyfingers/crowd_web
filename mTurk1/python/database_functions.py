from mTurk1.models import  Agent_setup,\
    View_setup, Sim_setup, Simulation, validate_setup_file, Simulation_instance,\
    Pass_key_group, Experiment_group, Tutorial_instance
import os
from django.core.exceptions import ValidationError
import logging
import sys


logger = logging.getLogger('django')


def process_tutorial_settings(tutorial_settings):
    
    logger.info("ATTEMPT: assign variables to experiment_settings")
    #TRY: set up the varaibles for creating an experiment
    try: 
        
        tutorial_name=tutorial_settings.tutorial_name
        agent_list=tutorial_settings.agent_list
        sim_list=tutorial_settings.sim_list
        view_list=tutorial_settings.view_list
        logger.info("OK: assigned varaibles to experiment settings")
    except:
        logger.info("FAILED: assign variables to experiment settings")
        logger.exception("create_database: Could not create sim, agent and view lists ")
        raise
    
    logger.info("ATTEMPT: validate sim,agent and view lists ")
    try:   
        valid_lists=check_lists(sim_list,agent_list,view_list)
        if all(list is True for list in valid_lists):
            logger.debug("create_database: All lists valid")
        else:
            logger.debug("create_databse: INVALID lists (labelled False). Sim: %s ; Agent: %s; View: %s" %(valid_lists[0],valid_lists[1], valid_lists[2]))
            raise
    except:
        logger.exception("create_database: Could not run valid_lists")
        raise
    logger.info("OK: lists valid")
    return [sim_list,agent_list,view_list,tutorial_name]


def check_lists(sim_list,agent_list,view_list):
    
    valid_sim_list=False
    valid_agent_list=False
    valid_view_list=False
    
    if len(sim_list)==1:
        valid_sim_list=True
    elif len(sim_list)<1:
        logger.debug("sim_list<1")
    elif len(sim_list>1):
        logger.debug("sim_list>1")
      
    if len(agent_list)==1:  
        valid_agent_list=True
    elif len(agent_list)<1:
        logger.debug("agent_list<1")
    elif len(agent_list)>1:
        logger.debug("agent_list>1")
    
    if len(view_list)<1:
        valid_view_list=False
    elif len(view_list)>=1:
        valid_view_list=True
    
    return[valid_sim_list,valid_agent_list,valid_view_list]  
    

def create_agent_files(agent_array):
    """"""
    count=0
    max_count=len(agent_array)
    for agent_file in agent_array:
        agent=Agent_setup(agent_file=agent_file)
        db_agents=[]   
        try:
            agent.full_clean()
            agent.save()
            count=count+1
            db_agents.append(agent)
        except ValidationError as e:
            logger.debug(e)
    logger.info("Agent files successful: %s of %s" %(count, max_count))                  
    return db_agents

def create_sim_files(sim_array):
    """"""
    count=0
    max_count=len(sim_array)
    db_sims=[]
    for sim_file in sim_array:
        sim=Sim_setup(sim_file=sim_file)   
        try:
            sim.full_clean()
            sim.save()
            count=count+1
            db_sims.append(sim)
        except ValidationError as e:
            logger.debug(e)
    logger.info("Sim files successful: %s of %s" %(count, max_count))  
    return db_sims

def create_view_files(view_array):
    """"""
    count=0
    max_count=len(view_array)
    db_views=[]
    for view_file in view_array:
        view=View_setup(view_file=view_file) 
        try:
            view.full_clean()
            view.save()
            count=count+1
            db_views.append(view)
        
        except ValidationError as e:
            logger.debug(e)
            
    logger.info("View files successful: %s of %s" %(count, max_count)) 
    return db_views
    
def create_simulation(sim_name,sim_setup,agent_setup,view_array):
    """"""
    simulation=Simulation(simulation_name=sim_name,sim_setup=sim_setup,agent_setup=agent_setup)
    simulation.save()
    for view in view_array:
        simulation.view_setup.add(view)
    return simulation

def create_sim_instance(simulation, view_setup):
    """"""
    logger.debug("TRY create sim_instance")
    try:
        sim_instance=Simulation_instance(simulation=simulation,view_instance=view_setup)
        sim_instance.save()
        logger.debug("Created sim_instance")
        return sim_instance
    except ValidationError as e:
            logger.debug(e)

def create_tutorial_instance(simulation, view_setup):
    """"""
    logger.debug("ATTEMPTcreate tutorial_instance")
    try:
        tutorial_instance=Tutorial_instance(simulation=simulation,view_instance=view_setup)
        tutorial_instance.save()
        logger.debug("Created tutorial_instance")
        return tutorial_instance
    except ValidationError as e:
            logger.debug(e)
       
def create_pass_key_group(sim_instance, experiment):
    """"""
    logger.debug("Creating pass_key_group")
    pass_group=Pass_key_group(simulation_instance=sim_instance,experiment_group=experiment)
    pass_group.save()
    return pass_group

def create_experiment_group(experiment_name):
    """"""
    logger.debug("Creating experiment_group")
    experiment_group=Experiment_group(name=experiment_name)
    experiment_group.save()
    return experiment_group
  
def generate_experiment(sim_list, agent_list, view_list,sim_name,exp_name,exp_type="LIVE"):
    
    logger.info("ATTEMPT: generate experiment")
    db_agent=create_agent_files(agent_list)
    db_sim=create_sim_files(sim_list)
    db_view_list=create_view_files(view_list) 
    db_simulation=create_simulation(sim_name,db_sim[0],db_agent[0],db_view_list)#TODO test
    db_experiment=create_experiment_group(exp_name)
    for db_view in db_view_list:
        db_sim_instance=create_sim_instance(db_simulation, db_view)#TODO test
        db_pass_key_group=create_pass_key_group(db_sim_instance, db_experiment)#TODO test
    logger.info("OK: generate_experiment")

def generate_tutorial(sim_list,agent_list,view_list,tutorial_name):
    logger.info("ATTEMPT: generate_tutorial")
    db_agent=create_agent_files(agent_list)
    db_sim=create_sim_files(sim_list)
    db_view_list=create_view_files(view_list)
    db_simulation=create_simulation(tutorial_name,db_sim[0],db_agent[0],db_view_list)#TODO test
    db_tutorial_instance=create_tutorial_instance(db_simulation,db_view_list[0])
        
def validate_simulation_files(simulation): #Checks that the simulation files are still valid e.g. havent been moved
    """"""
    sim_name=simulation.simulation_name
    logger.debug("Checking simulation: %s" %sim_name)
    sim_valid=True
    
    #Check sim file        
    sim_file=simulation.sim_setup.sim_file
    try:
        validate_setup_file(sim_file)
        logger.debug("VALID sim_file: %s" % sim_file)
        
    except ValidationError as e:
        logger.debug("INVALID sim_file: %s" % sim_file)
        logger.debug(e)
        sim_valid=False
    
    #Check agent files
    agent_file=simulation.agent_setup.agent_file
    try:
        validate_setup_file(agent_file)
        logger.debug("VALID agent_file: %s" % agent_file)
        
    except ValidationError as e:
        logger.debug("INVALID agent_file: %s" % agent_file)
        logger.debug(e)
        sim_valid=False
    
    view_setup_list=simulation.view_setup.all()
    
    for view_setup in view_setup_list:
        view_file=view_setup.view_file
        try:
            validate_setup_file(view_file)
            logger.debug("VALID view_file: %s" % view_file)
        except ValidationError as e:
            logger.debug("INVALID view_file %s" % view_file )
            logger.debug(e)
            sim_valid=False
            
    return sim_valid
    
    
def agent_path(setup_folder,agent_file): 
        return os.path.join(setup_folder,'agent_files',agent_file)
def sim_path(setup_folder,sim_file): 
        return os.path.join(setup_folder,'sim_files',sim_file)
def view_path(setup_folder,setup_file): 
        return os.path.join(setup_folder,'view_files',setup_file)                   
        

    