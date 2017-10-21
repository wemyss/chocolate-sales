import json
import os
import requests

def send_email(amount):
	API_KEY = os.environ.get('API_KEY')
	DOMAIN_NAME = os.environ.get('DOMAIN_NAME')
	MAILING_LIST = os.environ.get('MAILING_LIST')

	if not (API_KEY and DOMAIN_NAME and MAILING_LIST):
		print("Invalid environment variables")
		return

	return requests.post(
		("https://api.mailgun.net/v3/%s/messages" % DOMAIN_NAME),
		auth = ("api", API_KEY),
		data = {
			"from": ("Chocolate sales <mailgun@%s>" % DOMAIN_NAME),
		  	"to": MAILING_LIST,
		  	"subject": ("Chocolate Sale | $%s" % amount),
		  	"text": ("It's on sale at Coles! The price is $%s" % value)
		}
	)

def get_chocolate_price():
	r = requests.get('https://shop.coles.com.au/search/resources/store/20601/productview/bySeoUrlKeyword/green-blacks-organic-85%25-dark-chocolate?catalogId=10576')

	data = r.json()

	# get chocolate value, alternatively do a string regex if the object names change on website updates
	return 3.5#float(data['catalogEntryView'][0]['p1']['o'])


############
### MAIN ###
############

value = get_chocolate_price()

if value < 4:
	print("It's on sale! The price is $%s" % value)
	print(send_email(value))
else:
	print("No sale :( price is $%s" % value)





