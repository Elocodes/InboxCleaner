"""
create authentication to interact with gmail API.
create django views that use the Gmail API functions
"""
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from datetime import datetime, timedelta

import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


def authenticate_gmail(request):
    """Get Gmail API service."""
    SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

    creds = None
    print("Current working directory:", os.getcwd())
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('/vagrant/InboxCleaner/emails/token.json')
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
    """Move specified unread emails to the trash, max of 100"""
    try:
        service = authenticate_gmail(request)
        print("gmail service obtained successfully")
        results = service.users().messages().list(userId='me', q=f'is:unread older_than:1m', maxResults=5).execute()
        messages = results.get('messages', [])
        if messages:
            print(f"found {len(messages)} unread emails")
            message_ids = [msg['id'] for msg in messages]
            for message_id in message_ids:
                service.users().messages().modify(userId='me', id=message_id,
                                                  body={'removeLabelIds': ['INBOX'],
                                                        'addLabelIds': ['TRASH']}).execute()
            return (len(messages))
            print ('unread emails moved to trash')
        else:
            print("no unread emails found")
            return JsonResponse({'status': 'Success', 'message': 'No unread emails found.'})
    except Exception as e:
        print(f"Error: {str(e)}")
        return JsonResponse({'status': 'Error', 'message': str(e)}, status=500)


def index(request):
    """ the landing page for inboxcleaner """
    return render(request, 'emails/index.html')


def choose_cleanup_date(request):
    """ calculates and displays to user that emails older
    than a month from current date will be trashed """
    if request.method == 'GET':
        cleanup_date = datetime.now() - timedelta(days=30)
        formatted_date = cleanup_date.strftime('%B %d, %Y')
        return render(request, 'emails/choose_cleanup_date.html', {'formatted_date': formatted_date})
    else:
        # Handle invalid or unexpected POST request
        return render(request, 'emails/cleanup_error.html', {'error_message': 'Invalid request'})


def cleanup_emails(request):
    """ call the function that authenticates and cleans email """
    if request.method == 'POST':
        try:
            num_emails_cleaned = move_messages_to_trash(request)
            return render(request, 'emails/cleanup_success.html', {'num_emails_cleaned': num_emails_cleaned})
        except ValueError:
            # Handle invalid date format
            return render(request, 'emails/cleanup_error.html', {'error_message': 'Invalid date format'})
        except Exception as e:
            # Handle other errors
            return render(request, 'emails/cleanup_error.html', {'error_message': str(e)})
    else:
        # Handle invalid or unexpected GET request
        return render(request, 'emails/cleanup_error.html', {'error_message': 'Invalid request'})
