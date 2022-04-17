from googleapiclient.discovery import build
from google.oauth2 import service_account
import datetime
from googleapiclient.errors import HttpError

def main():
    key_file = '/path/to/exported/service/account/keyfile.json'

    scope = ("https://www.googleapis.com/auth/calendar.readonly",)
    creds = service_account.Credentials.from_service_account_file(key_file, scopes=scope)
    try:
        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        print('Getting the upcoming 10 events')
        # change from primary using the list method: https://developers.google.com/calendar/api/v3/reference/calendarList/list
        events_result = service.events().list(calendarId='yourCalendarIDHere@group.calendar.google.com', timeMin=now,
                                              maxResults=10, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
            return

        # Prints the start and name of the next 10 events
        eventsFile = open("/home/donal/screen/events.txt", "w")
        eventsTableHTML = open("/home/donal/screen/eventsTable.html", "w")
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
