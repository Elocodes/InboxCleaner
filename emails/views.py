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
        print("Credentials loaded from token.json")

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            print("credentials refreshed")

        else:
            print("running local server for oauth2 flow...")
            flow = InstalledAppFlow.from_client_secrets_file(
                    '/vagrant/InboxCleaner/emails/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0, open_browser=False)
            print("oauth2 flow completed")

        with open('token.json', 'w') as token:
            token.write(creds.to_json())
            print("credentials saved to token.json")

    return build('gmail', 'v1', credentials=creds)

def move_messages_to_trash(request):
    """Move unread emails to the trash, max of 100"""
    try:
        service = get_gmail_service()
        print("gmail service obtained successfully")

        results = service.users().messages().list(userId='me', q='is:unread', maxResults=5).execute()
        messages = results.get('messages', [])
        if messages:
            print(f"found {len(messages)} unread emails")
            message_ids = [msg['id'] for msg in messages]
            for message_id in message_ids:
                service.users().messages().modify(userId='me', id=message_id,
                                                  body={'removeLabelIds': ['INBOX'],
                                                        'addLabelIds': ['TRASH']}).execute()
            return JsonResponse({'status': 'Success', 'message': 'Unread emails moved to Trash.'})
        else:
            print("no unread emails found")
            return JsonResponse({'status': 'Success', 'message': 'No unread emails found.'})
    except Exception as e:
        print(f"Error: {str(e)}")
        return JsonResponse({'status': 'Error', 'message': str(e)}, status=500)
