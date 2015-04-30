#!/usr/bin/env python

"""
module Integration with SparrowSMS feed through NYPNY to Kaha.Co
Add authors
"""

__authors__ = 'Nitin Sharma (nitin@nypny.com), Anup Dhamala (anupdhml@gmail.com)'
__copyright__ = 'Copyright (c) 2015'
__license__ = 'MIT'
__version__ = '0.1'

import requests
import csv
import smtplib
import pprintpp

from email.mime.multipart import MIMEMultipart
from email.MIMEText import MIMEText

SMTPSERVER   = 'localhost'
SENDER_EMAIL = 'noreply@savefromearthquakenepal.org'
SENDER_NAME  = 'Save from Earthquake Nepal'
RECIPIENTS = ['anupdhml@gmail.com', 'nishansubedi@gmail.com', 'cashless.brtother@gmail.com']

INCIDENT_FILENAME = 'incidents.csv'

def fetch_incidents():
    """ Fetching Incidents from SparrowSMS"""
    _url = 'http://help.sparrowsms.com/api?task=incidents'
    incidents = []

    response = requests.get(_url)
    json_resp = response.json()
    incident_list = json_resp["payload"]["incidents"]

    for incident_content in incident_list:
        incident = incident_content.get('incident', []);
        incident["categories"] = ""
        incident["media_links"] = ""

	category_list = incident_content.get("categories", [])
        for categories in category_list:
	    category = categories.get("category", {})
            category_title = category.get("title", None)
            if category_title:
                separator = '' if (incident["categories"] == "") else ' AND '
                incident["categories"] += separator + category_title

	media_list = incident_content.get("media", [])
        for media in media_list:
            media_link = media.get("link_url", None)
            if media_link:
                separator = '' if (incident["media_links"] == "") else ' AND '
                incident["media_links"] += separator + media_link

        incidents.append(incident)
        #break;

    return incidents


def to_csv(incidents, filename):
    """ Dump the incidents to csv"""
    csv_columns = [
        'categories',
        'incidentactive',
        'incidentdate',
        'incidentdescription',
        'incidentid',
        'incidentmode',
        'incidenttitle',
        'incidentverified',
        'locationid',
        'locationlatitude',
        'locationlongitude',
        'locationname',
        'media_links',
    ]

    with open(filename, 'w') as csvfile:
        incidentwriter = csv.writer(csvfile, dialect='excel')
        incidentwriter.writerow(csv_columns)
        for incident in incidents:
            row = [incident.get(column) for column in csv_columns]
            #pprintpp.pprint(row)
            # encode some chars properly
            incidentwriter.writerow([unicode(str).encode("utf-8") for str in row])


def send_email(sender_name, sender_email, receiver_emails, subject, body, attachment_filename, smtpserver='localhost'):
    """email utility function"""

    msg = MIMEMultipart('alternative')

    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = ','.join(receiver_emails)
    content = MIMEText(body, 'plain')
    msg.attach(content)

    f = file(attachment_filename)
    attachment = MIMEText(f.read())
    attachment.add_header('Content-Disposition', 'attachment', filename=attachment_filename)
    msg.attach(attachment)

    try:
        #print msg
        smtp_obj = smtplib.SMTP(smtpserver)
        smtp_obj.sendmail(sender_email, receiver_emails, msg.as_string())
        print 'Successfully sent email'
    except smtplib.SMTPException:
        print 'Error: unable to send email'


if __name__=='__main__':
    incidents = fetch_incidents()
    pprintpp.pprint(incidents)

    to_csv(incidents, INCIDENT_FILENAME)

    send_email(
        SENDER_NAME, SENDER_EMAIL, RECIPIENTS,
        'ushahidi incidents', 'Incidents file from ushahidi is attached :)',
        INCIDENT_FILENAME, SMTPSERVER
    )
