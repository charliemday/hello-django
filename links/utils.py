import urllib.request
import requests

from django.conf import settings

def request_brandfetch(domain = None):

    if domain is None:
        return None

    brandfetch_api_url = 'https://api.brandfetch.io/v2/brands/{}'.format(domain)

    response = requests.get(brandfetch_api_url, headers={
        'Authorization': 'Bearer {}'.format(settings.BRANDFETCH_API_TOKEN)
    })

    if response.status_code == 200:
        data = response.json()
        logos = data.get('logos')
        if logos:
            logo_url = None

            for l in logos:
                if l.get('type') == 'symbol':
                    logo_url = l.get('formats')[0].get('src')

            return logo_url
    pass


def extract_domain(url = None):
    """
    Extract the domain from a url
    """

    if url is None:
        return None

    domain = urllib.parse.urlparse(url).netloc
    domain_arr = domain.split('.')

    if len(domain_arr) > 2:
        return '.'.join(domain_arr[-2:]) 

    return domain