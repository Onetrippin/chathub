import os

AUTH_URL = os.getenv("AUTH_URL", "http://auth-service:8000")
USER_URL = os.getenv("USER_URL", "http://user-service:8001")
MESSAGE_URL = os.getenv("MESSAGE_URL", "http://message-service:8002")
INTEGRATION_URL = os.getenv("INTEGRATION_URL", "http://integration-service:8003")
AI_URL = os.getenv("AI_URL", "http://ai-service:8004")
NOTIFICATION_URL = os.getenv("NOTIF_URL", "http://notification-service:8005")

JWT_PUBLIC_KEY = os.getenv("JWT_PUBLIC_KEY")

HTTP_IMPERSONATE = os.getenv("HTTP_IMPERSONATE", "chrome123")
HTTP_TIMEOUT_SECONDS = float(os.getenv("HTTP_TIMEOUT_SECONDS", "20"))
HTTP_RETRIES = int(os.getenv("HTTP_RETRIES", "2"))

GATEWAY_TITLE = os.getenv("GATEWAY_TITLE", "API Gateway")
GATEWAY_VERSION = os.getenv("GATEWAY_VERSION", "1.0.0")
