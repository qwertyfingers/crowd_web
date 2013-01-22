from mTurk1.models import Experiment_group
import logging
import sys
import os
import urlparse
import httplib
logger = logging.getLogger('django')



def list_experiment_keys(exp_name):
    logger.info("ATTEMPT: get Experiment_group with name: %s" %exp_name)
    try:
        exp=Experiment_group.objects.get(name=exp_name)
        logger.info("OK: Found Experiment_group with name %s" %exp_name)
    except:
        logger.exception("Could not get experiment with name %s" %exp_name)
        sys.exit()
    
    
    
    #Check for active keys in the experiment
    active_keys_set=exp.pass_key_group_set.filter(active_key=True)
    active_keys=[]
    
    logger.info("ATTEMPT: Find active and inactive user keys")
    for key in active_keys_set:
        active_keys.append(key.user_key)
        
    #Check for inactive keys
    inactive_keys_set=exp.pass_key_group_set.filter(active_key=False)
    inactive_keys=[]
    for key in inactive_keys_set:
        inactive_keys.append(key.user_key)

    logger.info("OK: Found %s active user_key" %len(active_keys))
    logger.info("OK: Found %s inactive user_key" %len(inactive_keys))
    
    return[active_keys, inactive_keys]

def create_relative_urls(exp_name,keys):
    """Creates strings of the following structure
            <exp_name>\live\<key>/
    """    
    relative_urls=[]
    for key in keys:
        rel_url=exp_name+"/live/instructions/"+key+"/"
        relative_urls.append(rel_url)
    
    return relative_urls  
    
def create_absolute_urls(exp_name,keys,domain_path):
    rel_urls=create_relative_urls(exp_name,keys)
    
    absolute_urls=[]
    for rel in rel_urls:
       
        abs_url=domain_path+str(rel)
        absolute_urls.append(abs_url)
    
    return absolute_urls



def get_server_status_code(url):
    """
    Download just the header of a URL and
    return the server's status code.
    """
    # http://stackoverflow.com/questions/1140661
    host, path = urlparse.urlparse(url)[1:3]    # elems [1] and [2]
    try:
        conn = httplib.HTTPConnection(host)
        conn.request('HEAD', path)
        return conn.getresponse().status
    except StandardError:
        return None
    
    
def check_absolute_urls(abs_urls):
    status_codes=[]
    all_good=True
    for url in abs_urls:
        sc= get_server_status_code(url)
        status_codes.append(sc)
        if sc != 200:
            all_good=False
    
    return status_codes
    if all_good:
        logger.info("All abs urls gave 200 response")
    else:
        logger.info("Not all urls gave 200 response")
        
        
        
        
        
        
#MAIN

if __name__ == "__main__":
    exp_name="experiment_1"
    domain_path="http://127.0.0.1:8000/"
    #domain_path="http://qwertyfinger.webfactional.com/experiments/"
     
    [active_keys,inactive_keys]=list_experiment_keys(exp_name)
    
    active_abs_urls=create_absolute_urls(exp_name,active_keys,domain_path)
    status_codes=check_absolute_urls(active_abs_urls)
    logger.info("Status codes of active absolute urls: %s" %status_codes)
    
    inactive_abs_urls=create_absolute_urls(exp_name,inactive_keys,domain_path)
    status_codes_inactive=check_absolute_urls(inactive_abs_urls)
    logger.info("Status codes of inactive absolute urls: %s" %status_codes_inactive)
    
    
    
            