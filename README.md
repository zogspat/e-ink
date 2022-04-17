# e-ink
Inspired by https://www.engineersneedart.com/systemsix/systemsix.html...
A full write-up on this code is at https://the-plot.com/blog/?p=1691

The quickstart.py script is a lightly adapted version of Google's example code to use Python with their Calendar API: https://developers.google.com/calendar/api/quickstart/python

NB: unless you go through the process of publishing the client (in the Google OAuth consent screen), the access and refresh tokens will expire after 7 days. Publishing infers that the client is available to anyone, so this isn't appropriate for this type of process. The simple alternative is to create a service account, and then to give that account read access to the shared calendar. The implementation for this is in the serviceAccCalAccess.py file.

Not included here is a copy of the lib directory that the WaveShare screen requires. 
