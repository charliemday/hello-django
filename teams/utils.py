import requests

DOMAIN = 'sandbox5b44c229493b4b48bab8c5076250044d.mailgun.org'
API_KEY = '16dd028df8eca92a05755cd39fafbdb4-76f111c4-d86a29ab'

def send_simple_message(email):
	return requests.post(
		"https://api.mailgun.net/v3/{}/messages".format(DOMAIN),
		auth=("api", API_KEY),
		data={"from": "Excited User <mailgun@{}>".format(DOMAIN),
			"to": [email],
			"subject": "Hello",
			"text": "Testing some Mailgun awesomness!"})