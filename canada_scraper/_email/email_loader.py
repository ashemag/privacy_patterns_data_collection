import smtplib
from email.mime.text import MIMEText
import socket
import os 
import boto3
from botocore.exceptions import ClientError

class Emailer():
	default_content = "Hey there! This is a test from our python script!"

	def send_email(self, recipient, content= default_content): 
		SENDER = 'ashe.magalhaes@gmail.com'
		AWS_REGION = "us-west-2"
		SUBJECT = "Automated Privacy Cases Scraper Update"
		BODY_TEXT = (content)        
		# The character encoding for the email.
		CHARSET = "UTF-8"
		# Create a new SES resource and specify a region.
		client = boto3.client('ses',region_name=AWS_REGION)
		# Try to send the email.
		try:
			#Provide the contents of the email.
			response = client.send_email(
				Destination={
					'ToAddresses': [
						recipient,
					],
				},
				Message={
					'Body': {
						'Text': {
							'Charset': CHARSET,
							'Data': BODY_TEXT,
						},
					},
					'Subject': {
						'Charset': CHARSET,
						'Data': SUBJECT,
					},
				},
				Source=SENDER,
			)
		except ClientError as e:
			print(e.response['Error']['Message'])
		else:
			print("Email sent! Message ID:"),
			print(response['ResponseMetadata']['RequestId'])

#for testing 
if __name__ == "__main__":
	e = Emailer()
	e.send_email() 




