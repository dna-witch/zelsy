### twilio for zelsy
# (805)262-9284

from twilio.rest import Client

# Your Account SID from twilio.com/console
account_sid = "ACe9dcc22c9db899868a627562292d7c4b"
# Your Auth Token from twilio.com/console
auth_token  = "0071b3cf8c984f389f9eb1e1b631806b"

client = Client(account_sid, auth_token)

message = client.messages.create(
    to="+19258954933",
    from_="+18052629284",
    body="Hello from Zelsy! Our goal at Zelsy is to connect people and teach them about mental health.")

print(message.sid)

message = client.messages.create(
    to="+19258954933",
    from_="+18052629284",
    body="Hello from Zelsy! Your friend, Erica, is in need of your friendship and support right now!")

print(message.sid)
