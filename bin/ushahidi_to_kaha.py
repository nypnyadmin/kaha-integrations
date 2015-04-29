#!/usr/bin/env python

"""
module Integration with SparrowSMS feed through NYPNY to Kaha.Co
Add authors
"""

__authors__ = 'Nitin Sharma (nitin@nypny.com)'
__copyright__ = 'Copyright (c) 2015'
__license__ = 'MIT'
__version__ = '0.1'

import requests

def fetch_incidents():
    """ Fetching Incidents from SparrowSMS"""
    _url = 'http://help.sparrowsms.com/api?task=incidents'
    help_offered_incidents = []    
    help_required_incidents = []    


    response = requests.get(_url)
    json_resp = response.json()
    incident_list = json_resp["payload"]["incidents"]
    for incident in incident_list:
	category_list = incident.get("categories", [])
        for categories in category_list:
	    category = categories.get("category", {})
	    if 'Help Offered' == category.get("title", None):
	        help_offered_incidents.append(incident)
	    elif 'Help Needed' == category.get("title", None): 
	        help_required_incidents.append(incident)
    
    print help_required_incidents 


if __name__=='__main__':

    fetch_incidents()
