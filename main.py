import boto3
import json
import os
import requests
from decimal import *


# DYNAMO DB SETUP & HELPERS
# ===========================================================
db = boto3.resource(
	'dynamodb',
	aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID'),
	aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY'),
	region_name = 'ap-southeast-2'
)
items_table = db.Table('sams-sales')
users_table = db.Table('sams-sales-users')

def price_is_lower_than_last_time(name, price):
	'''
	Return true if current price for the item is less than previous price, else false.
	'''
	try:
		response = items_table.get_item(
			Key = {
				'name': name,
			}
		)
	except ClientError as e:
		print(e.response['Error']['Message'])
	else:
		if 'Item' in response:
			prev_price = response['Item']['price']
			return price < prev_price
		else:
			return False

def update_price(name, price):
	'''
	Update the previous price of the item
	'''
	items_table.put_item(
		Item = {
			'name': name,
			'price': Decimal(str(price)),
		}
	)

def get_users():
	return users_table.scan()['Items']


# GATHER ITEM PRICES
# ===========================================================
def get_price_coles(url):
	r = requests.get(url)
	data = r.json()
	return float(data['catalogEntryView'][0]['p1']['o'])

def get_price_woolworths(url):
	r = requests.get(url)
	data = r.json()
	return float(data['Product']['Price'])

def get_cheaper_vendor(prices):
	cheaper_vendor = None
	for vendor, price in prices.items():
		if cheaper_vendor is None or price < prices[cheaper_vendor]:
			cheaper_vendor = vendor
	return cheaper_vendor

def get_items_on_sale(data):
	sale_items = []

	for item in data['items']:
		prices = {}

		# handle empty urls for coles or woolies
		if 'coles_url' in item:
			prices['coles'] = get_price_coles(data['coles_url_prefix'] + item['coles_url'])
		if 'woolworths_url' in item:
			prices['woolworths'] = get_price_woolworths(data['woolworths_url_prefix'] + item['woolworths_url'])


		cheaper_vendor = get_cheaper_vendor(prices)
		price = prices[cheaper_vendor]

		if price_is_lower_than_last_time(item['name'], price):
			sale_items.append({ 'name': item['name'], 'price': price, 'vendor': cheaper_vendor })

		update_price(item['name'], price)

	return sale_items


# HTML & EMAIL
# ===========================================================
with open('email-template.html', 'r') as myfile:
    _html_email_template = myfile.read().replace('\n', '').replace('\t', '')

def generate_email(sale_items):
	table_html = ''

	for item in sale_items:
		table_html += ('<tr><td>' + item['name'] + '</td>'
			'<td>$' + ('%.2f' % item['price']) + '</td>'
			'<td>' + item['vendor'].title() + '</td></tr>')

	return _html_email_template.replace('<!--INSERT_HERE-->', table_html, 1)

def send_email(email, body):
	API_KEY = os.environ.get('API_KEY')
	DOMAIN_NAME = os.environ.get('DOMAIN_NAME')

	if not (API_KEY and DOMAIN_NAME):
		print('Invalid environment variables')
		return

	result = requests.post(
		('https://api.mailgun.net/v3/%s/messages' % DOMAIN_NAME),
		auth = ('api', API_KEY),
		data = {
			'from': ('Sams Sales <sams-sales@%s>' % DOMAIN_NAME),
			'to': email,
			'subject': 'Stuff is on sale',
			'html': body
		}
	)
	print(result.text)


def user_wants_item(user, item):
	'''
	Return true if any item_keywords for the user are in the item name.
	'''
	return any(keyword in item['name'] for keyword in user['item_keywords'])

def notify_users(sale_items):
	users = get_users()

	for user in users:
		user_interested_items = [item for item in sale_items if user_wants_item(user, item)]
		if len(user_interested_items) > 0:
			send_email(user['email'], generate_email(user_interested_items))
			# print(user['email'] + '   ' + generate_email(user_interested_items) + '\n')



# MAIN
# ===========================================================
def main():
	data = json.load(open('items.json'))
	sale_items = get_items_on_sale(data)
	if len(sale_items) > 0:
		notify_users(sale_items)



main()
