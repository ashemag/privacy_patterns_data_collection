import smtplib
from email.mime.text import MIMEText
import socket



class Emailer():
	default_content = "Hey there! This is a test from our python script!"

	def send_email(self, content=default_content, recipients = ['ashe.magalhaes@gmail.com']): 
		me = 'ashe.magalhaes@gmail.com'
		for recipient in recipients: 
			msg = MIMEText(content)
			msg['Subject'] = 'Automated FTC Scraper Update'
			msg['From'] = me
			msg['To'] = recipient
	
			mail = smtplib.SMTP('smtp.gmail.com', 587)
			try: 
				mail.ehlo() #handshake with server 
				mail.starttls()
				mail.login(me, os.environ['EmailKey'])
				mail.sendmail(me, recipient, msg.as_string())
				mail.quit()

			except Exception, error: 
				print "ERROR!"
				print(error)
				
#for testing 
if __name__ == "__main__":
	e = Emailer()
	e.send_email() 




