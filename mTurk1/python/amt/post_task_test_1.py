
from mTurk1.python.amt.helper_functions import (check_absolute_urls,
list_experiment_keys, create_absolute_urls)
import logging
from mTurk1.python.amt.post_exp_test import post_HIT1
logger = logging.getLogger('django')


# MTurk settings 
ACCESS_ID = 'AKIAJ7IROEGSSF4KJE3A'
SECRET_KEY = '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'
HOST = 'mechanicalturk.sandbox.amazonaws.com'

# Experiment Settings
domain_path = "http://127.0.0.1:8000/"
exp_name = "experiment_1"



#--------------------------------------------------------------------------

# Get the active keys for the experiment
[active_keys, inactive_keys] = list_experiment_keys(exp_name)

# Create absolute urls
active_abs_urls = create_absolute_urls(exp_name, active_keys, domain_path)

# Check that each url gives status code 200
status_codes = check_absolute_urls(active_abs_urls)
logger.info("Status Codes: %s" %status_codes)

#Post task to mechanical turk 

for abs_url in active_abs_urls:
    post_HIT1(ACCESS_ID,SECRET_KEY,HOST,abs_url)
