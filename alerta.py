from twilio.rest import Client
def enviarMensaje(sid, auth_token, mensaje, numero_cel, twi): 
    client = Client(sid, auth_token)
    client.messages.create(body=mensaje,from_=twi,to=numero_cel)