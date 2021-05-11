import time
import jwt
import aiof.config as config


settings = config.get_settings()

def decode_jwt(token: str):
    decoded = jwt.decode(token, settings.JwtPublicKey, algorithms=[settings.JwtAlgorithm])
    print(decoded)
    return {
        "access_token": decoded
    }

if __name__ == "__main__":
    print(decode_jwt("eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMSIsInB1YmxpY19rZXkiOiJiZDUzMTQ3OC0zYjM2LTRlZWEtODI4ZC1lODNlYWI3ZWEwNWMiLCJyb2xlIjoiQWRtaW4iLCJuYmYiOjE2MjA3NTI1MzEsImV4cCI6MTYyMDc1MzQzMSwiaWF0IjoxNjIwNzUyNTMxLCJpc3MiOiJhaW9mOmF1dGgiLCJhdWQiOiJhaW9mOmF1dGg6YXVkaWVuY2UifQ.h0Ktu8WpWZArrx8A36j1MWQS_4BKjXdqpUTdMQUDXKBjlG_P0I7NC6Jf0HijeaSOfXvlYyQycne3F1mOQezdKActKnKabRrrcllsOx_ihSQrfU9b8IfKCTye56x72I2AxP2EVXHj3r65KhfMJORW2ZefYphDmQduSqV-OY5wCa_0i5iCiMAedW09Sk50l2TBZ248i14a4VUKWE5l6jVKQ3WkdQnaOaNPdfGF2pyAgLBle-7q1cxJku52k8mQ8SuG-GPLS1zLO6smkP3xjyBBkQEIOCmrwVnUjqwa-ozUL33hKxPKzVkygDUGY9Ez-4PQObuPnl_ONWgMsJJbCD9AnA"))