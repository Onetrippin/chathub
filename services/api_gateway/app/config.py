import os

AUTH_URL = os.getenv('AUTH_URL', 'http://auth-service:8000')
USER_URL = os.getenv('USER_URL', 'http://user-service:8001')
MESSAGE_URL = os.getenv('MESSAGE_URL', 'http://message-service:8002')
INTEGRATION_URL = os.getenv('INTEGRATION_URL', 'http://integration-service:8003')
AI_URL = os.getenv('AI_URL', 'http://ai-service:8004')
NOTIFICATION_URL = os.getenv('NOTIF_URL', 'http://notification-service:8005')

JWT_PUBLIC_KEY = os.getenv('JWT_PUBLIC_KEY')
