import boto3
import json
import os
import requests

SALE_KEY = 'wasOnSale'
MAX_SALE_PRICE = 4

def send_email(amount):
	API_KEY = os.environ.get('API_KEY')
	DOMAIN_NAME = os.environ.get('DOMAIN_NAME')
	EMAIL_LIST = os.environ.get('EMAIL_LIST')

	if not (API_KEY and DOMAIN_NAME and EMAIL_LIST):
		print("Invalid environment variables")
		return

	for email in EMAIL_LIST.split(','):
		print(email)
		result = requests.post(
			("https://api.mailgun.net/v3/%s/messages" % DOMAIN_NAME),
			auth = ("api", API_KEY),
			data = {
				"from": ("Chocolate sales <chocolate-sales@%s>" % DOMAIN_NAME),
				"to": email,
				"subject": ("Chocolate Sale | $%s" % amount),
				"text": ("It's on sale at Coles! The price is $%s" % value)
			}
		)
		print(result.text)


def get_chocolate_price():
	# TODO: Add error handling and notification system for when this URL fails
	r = requests.get('https://shop.coles.com.au/search/resources/store/20601/productview/bySeoUrlKeyword/green-blacks-organic-85%25-dark-chocolate?catalogId=10576')

	data = r.json()

	return float(data['catalogEntryView'][0]['p1']['o'])



############
### MAIN ###
############
db = boto3.resource(
	'dynamodb',
	aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID'),
	aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY'),
	region_name = 'ap-southeast-2'
)
table = db.Table('chocolate-sales')


value = get_chocolate_price()
isOnSale = value < MAX_SALE_PRICE
wasOnSale = False


# Get previous sale check
try:
	response = table.get_item(
		Key = {
			'name': SALE_KEY
		}
	)

except ClientError as e:
	print(e.response['Error']['Message'])

else:
	wasOnSale = response['Item']['value']


# If sale just started send an email
if isOnSale:
	if wasOnSale:
		print("It's been on sale for a while now. skip email alert")
	else:
		print("It's on sale! The price is $%s" % value)
		send_email(value)

else:
	print("No sale :( price is $%s" % value)


# Update the db with latest sale check
table.put_item(
	Item = {
		'name': SALE_KEY,
		'value': isOnSale,
	}
)




