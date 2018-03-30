import smtplib
from email.mime.text import MIMEText

import os,sys,inspect #to access ConfigLoader
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
from config.config_loader import ConfigLoader

class Emailer():
	default_content = "Hey there! This is a test from our python script!"

	def send_email(self, content=default_content, recipients = ['ashemag@stanford.edu']): 
		config_data = ConfigLoader().config()
		me = 'ashe@cs.stanford.edu'
		for recipient in recipients: 
			msg = MIMEText(content)
			msg['Subject'] = 'Automated FTC Scraper Update'
			msg['From'] = me
			msg['To'] = recipient

			# Send the message via our own SMTP server, but don't include the
			# envelope header.
			s = smtplib.SMTP('localhost')
			s.sendmail(me, [recipient], msg.as_string())
			s.quit() 
			print("Finshed sending!")


#for testing 
if __name__ == "__main__":
	e = Emailer()
	e.send_email() 