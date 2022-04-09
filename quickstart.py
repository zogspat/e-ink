from __future__ import print_function

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        print('Getting the upcoming 10 events')
        # change from primary using the list method: https://developers.google.com/calendar/api/v3/reference/calendarList/list
        events_result = service.events().list(calendarId='yourSharedCalId_or_Primary_here@group.calendar.google.com', timeMin=now,
                                              maxResults=10, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
            return

        # Prints the start and name of the next 10 events
        eventsFile = open("events.txt", "w")
        eventsTableHTML = open("eventsTable.html", "w")
        eventsTableHTML.write("<html><head></head><body><font size=\"12\" face=\"Arial\">\n")
        eventsTableHTML.write("<table border=1><tr><th colspan=3 align=\"center\">Upcoming Events</th></tr>\n")
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            #print (datetime.datetime.strptime(start, '%Y-%m-%dT%H:%M:%S%z'))
            print(start, event['summary'])
            try:
                formattedDate = datetime.datetime.strptime(start, '%Y-%m-%dT%H:%M:%S%z')
            except ValueError:
                # recurring events like birthdays just have:
                formattedDate = datetime.datetime.strptime(start, '%Y-%m-%d')
                formattedDate = formattedDate.replace(hour=12)
            #print(formattedDate.strftime("%A %d/%m/%Y at %I:%M%p"))
            #print(event['summary'])
            eventString = formattedDate.strftime("%A %d/%m/%Y||%I:%M%p||"+event['summary']+"\n")
            eventsFile.write(eventString)
            eventTableHtmlString = formattedDate.strftime("<tr><td>%A %d/%m/%Y</td><td>%I:%M%p</td><td>"+event['summary']+"</td></tr>\n")
            eventsTableHTML.write(eventTableHtmlString)
        eventsFile.close()
        eventsTableHTML.write("</table></body></html>")
    except HttpError as error:
        print('An error occurred: %s' % error)


if __name__ == '__main__':
    main()
