import os
import logging
from django.shortcuts import render
from mTurk1.models import Experiment_group, Pass_key_group

from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponseRedirect

from mTurk1.python.view_functions import validate_setup_files, dump_to_json,\
    process_reports_from_post, warning_reports
from django.core.urlresolvers import reverse




    
SITE_ROOT = os.path.dirname(os.path.realpath(__file__))
logger = logging.getLogger('django')




#This view collects all the keys associated with the current experiemnt
#Returns either an  error page, or a page of keys associated with the experiment
def display_keys(request, cur_app,exp_name):
    logger.info("view - display key")
   
    try:
       
        experiment=Experiment_group.objects.get(name=exp_name)
        logger.debug("OK: Experiment_group found : name= %s" %exp_name)
    except:
        logger.exception("Could not get an experiment_group with name %s" %exp_name)
        error_message="There is no valid experiment at this time."
        return render(request,'mTurk1/error_page.html',{'error_message':error_message})

    #If an experiment is found, then continue

    #Check for active keys in the experiment
    active_keys_set=experiment.pass_key_group_set.filter(active_key=True)
    active_keys=[]
    for key in active_keys_set:
        active_keys.append(key.user_key)
        
    #Check for inactive keys
    inactive_keys_set=experiment.pass_key_group_set.filter(active_key=False)
    inactive_keys=[]
    for key in inactive_keys_set:
        inactive_keys.append(key.user_key)
    
    if len(active_keys)>=1 or len(inactive_keys)>=1:
        
        return render(request,'mTurk1/display_keys.html',{'active_keys':active_keys, 'inactive_keys':inactive_keys, 'exp_name':exp_name })
    else:
        error_message="No keys for this experiemnt could be found"
        return render(request, 'mTurk1/error_page.html', {'error_message':error_message})





def simulation(request, key,exp_name,cur_app):
    
    #Get the key from the url
    #Check key from url against database
        #Check existence of key
        #Check key is active
    #Check if POST data
        #Process POST data
    #If not POSt, then direct user to simulation
    
    
    
    #Check if key exists
    try:
        current_pkg=Pass_key_group.objects.get(user_key=key)
    except:
        logger.debug("Key does not exist")
        logger.exception("Key does not exist")
        raise Http404
        
    #Check if key is active
    if current_pkg.active_key==False:
        logger.debug("Key is not active")
        logger.exception("Key is not active")
        raise Http404
    
    #If there is POST data present, check to see if it is a valid report POST
    if request.method=='POST':
        logger.info("Request.method=POST found")
        logger.info("BEGIN process_reports_from_post")
        
        
        if cur_app=='mturk1_live':
            report_type='LIVE'
        elif cur_app=='mturk1_demo':
            report_type='DEMO'
        else:
            report_type='AUTO' 
            
        
        process_reports=process_reports_from_post(request.POST,current_pkg,key,report_type=report_type)
        
        valid_reports=process_reports['valid_reports']
        invalid_reports=process_reports['invalid_reports']
        
        logger.info("Valid reports: %s" %valid_reports)
        logger.info("Invalid reports: %s" %invalid_reports)
        
        
        
        #If process reports returned successfully
        if valid_reports>=1:
            reward_key=current_pkg.reward_key

            return HttpResponseRedirect(reverse((cur_app+':thankyou_post'), args=[exp_name,key, reward_key]))
        else:
            return_variables={"url_key":key,"exp_name":exp_name, "cur_app":cur_app,'valid_reports':valid_reports,'invalid_reports':invalid_reports}
            return render(request,'mTurk1/error_page.html',return_variables)  
    
    #If there was no post data, then proceed to loading the simulation
    #Get the setup files 
    try:
        sim_instance=current_pkg.simulation_instance
        simulation=sim_instance.simulation
        sim_setup=simulation.sim_setup
        agent_setup=simulation.agent_setup
        view_setup=sim_instance.view_instance
        logger.debug("OK: Found _setup database entries")
        
        validate_setup_files(sim_setup.sim_file,agent_setup.agent_file,view_setup.view_file)
        logger.debug("OK: Ran validation checks on _setup files") 
             
        json_dump=dump_to_json(sim_setup.sim_file,agent_setup.agent_file,view_setup.view_file)
        logger.debug("OK: dumped all json files")
            
        sim_settings=json_dump[0]
        agent_settings=json_dump[1]
        view_settings=json_dump[2]
        logger.debug("OK: assigned json_dump to variables")
    except:
        logger.debug("Could not load simulation")
        logger.exception("Could not load simulation")
        raise Http404
    
    return render(request,'uSim/simulation_testM1.html',{'json_sim_settings':sim_settings,'json_view_settings':view_settings,'json_agent_settings':agent_settings})   
    #return render(request, 'mTurk1/error_page.html', {'error_message':error_message})
    

def thankyou_post(request,exp_name,key=None,reward_key=None,cur_app=None): 
    
  
    
    #Check key exists
    
    #Check key active
    
    #Check reward_key
    

    
    try:
        current_pkg=Pass_key_group.objects.get(user_key=key)
    except:
        logger.debug("Key does not exist")
        logger.exception("Key does not exist")
        raise Http404
        
    #Check if key is active
    if current_pkg.active_key==False:
        logger.debug("Key is not active")
        logger.exception("Key is not active")
        raise Http404
    
    #Check if reward_key is correct
    
    if current_pkg.reward_key==reward_key:
        #If both okay, then send to reward page
        return render(request, 'mTurk1/thankyou_page.html',{"url_key":key, "reward_key": reward_key})
    else:
        raise Http404 
    
    
def instructions(request,key,exp_name,cur_app):
    
    return render(request, 'uSim/instructions.html',{"url_key":key,"exp_name":exp_name, "cur_app":cur_app})


def instructions2(request,key,exp_name,cur_app):
    
    #Check if experiment exists
    #Check if key exists
    #Check if experiment has a single tutorial simulation
    #get the sim files for that simulation
    
    
    
    
        #Check if key exists
    logger.info("ATTEMPT: Get current pass key")
    try:
        current_pkg=Pass_key_group.objects.get(user_key=key)
    except:
        logger.debug("Key does not exist")
        logger.exception("Key does not exist")
        raise Http404
    logger.info("OK: Found current Key")   
    #Check if key is active
    logger.info("ATTEMPT: Check if key is active")
    if current_pkg.active_key==False:
        logger.debug("Key is not active")
        logger.exception("Key is not active")
        raise Http404
    logger.info("OK: Key is active")
    #Get the tutorial for the current simulation
    logger.info("ATTEMPT: Get current experiment and tutorial")
    try:
        current_experiment=Experiment_group.objects.get(name=exp_name)
        tutorial_instance=current_experiment.tutorial
    except:
        logger.exception("Could not get current experiment and tutorial_instance.")
        raise Http404
    logger.info("OK: Got current experiment")
    #If there is POST data present, check to see if it is a valid report POST
    
    if request.method=='POST':
        logger.info("Request.method=POST found")
        logger.info("BEGIN process_reports_from_post")
        
        if cur_app=='mturk1_live':
            report_type='TULI'
        elif cur_app=='mturk1_demo':
            report_type='TUDE'
        else:
            report_type='AUTO' 
        
        process_reports=process_reports_from_post(request.POST,current_pkg,key,report_type=report_type)
        valid_reports=process_reports['valid_reports']
        invalid_reports=process_reports['invalid_reports']
        total_reports=valid_reports+invalid_reports
        warning_rep=warning_reports(valid_reports, invalid_reports)
       
        return_variables={"url_key":key,"exp_name":exp_name, "cur_app":cur_app,'valid_reports':valid_reports, 'invalid_reports':invalid_reports,'warning':warning_rep}
        return render(request,'uSim/instructions_results.html', return_variables )
        
    
    #If there was no post data, then proceed to loading the simulation
    #Get the setup files 
    try:
        try:
            simulation=tutorial_instance.simulation
        except:
            logger.error("Could not find the tutorial_instance. Has one been assigned to the experiment %s" %exp_name)
            raise
        sim_setup=simulation.sim_setup
        agent_setup=simulation.agent_setup
        view_setup=tutorial_instance.view_instance
        logger.debug("OK: Found _setup database entries")
        
        validate_setup_files(sim_setup.sim_file,agent_setup.agent_file,view_setup.view_file)
        logger.debug("OK: Ran validation checks on _setup files") 
             
        json_dump=dump_to_json(sim_setup.sim_file,agent_setup.agent_file,view_setup.view_file)
        logger.debug("OK: dumped all json files")
            
        sim_settings=json_dump[0]
        agent_settings=json_dump[1]
        view_settings=json_dump[2]
        logger.debug("OK: assigned json_dump to variables")
    except:
        logger.debug("Could not load simulation")
        logger.exception("Could not load simulation")
        raise Http404
    
    return render(request,'uSim/simulation_testM1.html',{'json_sim_settings':sim_settings,'json_view_settings':view_settings,'json_agent_settings':agent_settings})   
    #return render(request, 'mTurk1/error_page.html', {'error_message':error_message})
  