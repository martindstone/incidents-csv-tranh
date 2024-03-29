import json
import requests

BASE_URL = 'https://api.pagerduty.com'

def request(api_key=None, oauth_token=None, endpoint=None, method="GET", params=None, data=None, addheaders=None):

	if not api_key and not oauth_token:
		return None
	if not endpoint:
		return None


	url = '/'.join([BASE_URL, endpoint])
	headers = {
		"Accept": "application/vnd.pagerduty+json;version=2"
	}

	if data != None:
		headers["Content-Type"] = "application/json"

	if api_key:
		headers["Authorization"] = "Token token={}".format(api_key)
	else:
		headers["Authorization"] = "Bearer {}".format(oauth_token)

	if addheaders:
		headers.update(addheaders)

	req = requests.Request(
		method=method,
		url=url,
		headers=headers,
		params=params,
		json=data
	)

	prepped = req.prepare()
	response = requests.Session().send(prepped)
	return response.json()

def fetch(api_key=None, oauth_token=None, endpoint=None, params=None):
	my_params = {}
	if params:
		my_params = params.copy()

	fetched_data = []
	offset = 0
	array_name = endpoint.split('/')[-1]
	while True:
		r = request(api_key=api_key, oauth_token=oauth_token, endpoint=endpoint, params=my_params)
		fetched_data.extend(r[array_name])
		if not (("more" in r) and r["more"]):
			break
		offset += r["limit"]
		my_params["offset"] = offset
	return fetched_data

def fetch_incidents(api_key=None, oauth_token=None):
	return fetch(api_key=api_key, oauth_token=oauth_token, endpoint="incidents", params=params)

def fetch_users(api_key=None, oauth_token=None, params=None):
	return fetch(api_key=api_key, oauth_token=oauth_token, endpoint="users", params=params)

def fetch_escalation_policies(api_key=None, oauth_token=None, params=None):
	return fetch(api_key=api_key, oauth_token=oauth_token, endpoint="escalation_policies", params=params)

def fetch_services(api_key=None, oauth_token=None, params=None):
	return fetch(api_key=api_key, oauth_token=oauth_token, endpoint="services", params=params)