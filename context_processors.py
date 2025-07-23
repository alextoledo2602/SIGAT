from django.conf import settings

def firebase_config(request):
    return {
        'FCM_API_KEY': settings.FCM_API_KEY,
        'FCM_AUTH_DOMAIN': settings.FCM_AUTH_DOMAIN,
        'FCM_PROJECT_ID': settings.FCM_PROJECT_ID,
        'FCM_STORAGE_BUCKET': settings.FCM_STORAGE_BUCKET,
        'FCM_SENDER_ID': settings.FCM_SENDER_ID,
        'FCM_APP_ID': settings.FCM_APP_ID,
    }