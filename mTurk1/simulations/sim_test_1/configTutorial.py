import os
from mTurk1.python.database_functions import sim_path, agent_path, view_path

#This is the tutorial for experiment_1

class TutorialSettings:
    
    #Name the tutorial
    tutorial_name='Tutorial_0.1'

    #Setup folder location
    setup_folder=os.path.abspath(os.path.join(os.path.dirname( __file__ ),'setup_files'))

    sim1=sim_path(setup_folder,"sim_settings_test_0.1.json")
    agent1=agent_path(setup_folder,"agent_settings_test_0.1.json")
    view1=view_path(setup_folder,"view_settings_test_0.1.json")

    sim_list=[sim1]
    agent_list=[agent1]
    view_list=[view1]
    

    
