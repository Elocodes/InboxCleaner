"""
create authentication to interact with gmail API.
create django views that use the Gmail API functions
"""
from django.shortcuts import render
from django.http import JsonResponse

import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


def get_gmail_service():
    """Get Gmail API service."""
    SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json')
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '/vagrant/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return build('gmail', 'v1', credentials=creds)

def move_messages_to_trash(request):
    """Move unread emails to the trash, max of 100"""
    try:
        service = get_gmail_service()
        results = service.users().messages().list(userId='me', q='is:unread', maxResults=100).execute()
        messages = results.get('messages', [])
        if messages:
            message_ids = [msg['id'] for msg in messages]
            for message_id in message_ids:
                service.users().messages().modify(userId='me', id=message_id,
                                                  body={'removeLabelIds': ['INBOX'],
                                                        'addLabelIds': ['TRASH']}).execute()
            return JsonResponse({'status': 'Success', 'message': 'Unread emails moved to Trash.'})
        else:
            return JsonResponse({'status': 'Success', 'message': 'No unread emails found.'})
    except Exception as e:
        return JsonResponse({'status': 'Error', 'message': str(e)}, status=500)
