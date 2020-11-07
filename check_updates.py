import sys
import requests
import datetime
import time
from pytz import timezone
import sendgrid
from sendgrid.helpers.mail import *
import os
from dotenv import load_dotenv

def send_email(subject, content):
	load_dotenv()
	sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
	from_email = Email(os.environ.get('SENDGRID_FROM_EMAIL'))
	to_email = To(os.environ.get('SENDGRID_TO_EMAIL'))
	subject = subject
	content = Content("text/html", content)
	mail = Mail(from_email, to_email, subject, content)
	response = sg.client.mail.send.post(request_body=mail.get())

def check_updates(url, frequency=60):

	#Time Zone formatting
	gmt = timezone('GMT')
	eastern = timezone('US/Eastern')
	input_datetime_format = "%a, %d %b %Y %H:%M:%S %Z"
	output_datetime_format = "%b %d %Y %H:%M %Z"

	prev_check = None

	while url:
		response = requests.head(url)
		
		if response.status_code==200:
			
			datetime_str = response.headers["last-modified"] #Thu, 29 Oct 2020 14:42:12 GMT
			current = datetime.datetime.now(eastern)
			most_recent_check = gmt.localize(datetime.datetime.strptime(datetime_str, input_datetime_format)).astimezone(eastern)
			
			if (prev_check and most_recent_check > prev_check):
				subject = "[HTTP Update Checker] File has been updated on {most_recent_check}"\
					.format(most_recent_check=most_recent_check.strftime(output_datetime_format))
				content = "[{current}] The last-modified date for <a href={url}> monitored file </a>\
				 changed from: {prev_check} to: {most_recent_check}.<br/>\
				 This is an automated message. Do not reply."\
					.format(current=current.strftime("%b %d %Y %H:%M:%S %Z"), url=url,\
					prev_check=prev_check.strftime(output_datetime_format),\
					most_recent_check=most_recent_check.strftime(output_datetime_format))
				print(subject)
				send_email(subject, content)
			else:
				print("[{current}] No updates, most recent update on: {most_recent_check}"\
					.format(current=current.strftime(output_datetime_format),\
					most_recent_check=most_recent_check.strftime(output_datetime_format)))

			prev_check = most_recent_check

		time.sleep(frequency)


if __name__ == '__main__':
	# First argument must be a file url, i.e:
	# python check_updates.py "https://cdn.star.nesdis.noaa.gov/GOES16/ABI/FD/GEOCOLOR/678x678.jpg"
	check_updates(*sys.argv[1:])
