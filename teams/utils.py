import requests
from django.conf import settings

DOMAIN = settings.MAILGUN_DOMAIN 
API_KEY = settings.MAILGUN_API_KEY


def send_invite(email, token):
    invite_url = "https://getbaser.xyz/accept-invite?token=" + str(token)
    response = requests.post(
        "https://api.eu.mailgun.net/v3/{}/messages".format(DOMAIN),
        auth=("api", API_KEY),
        data={
            "from": "Baser Invites <welcome@{}>".format(DOMAIN),
            "to": [email],
            "subject": "Team Invite to Baser",
            "html": '<h1>Hi 👋 you\'ve been invited to join a Baser team!</h1><br /><p>Click on the invite below to join the team:</p><br /><a href="{}">Accept Invite</a>'.format(
                (invite_url)
            ),
        },
    )
    return response

