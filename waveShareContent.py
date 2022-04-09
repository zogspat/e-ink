import feedparser
from datetime import datetime, timedelta
from PIL import Image, ImageDraw, ImageFont, ImageOps
import imgkit
import io
from random import seed
from random import randint
from os.path import exists
from os import path
import sys
libdir = "/home/donal/screen/lib"
sys.path.append(libdir)
fontPath = libdir+"/Font.ttc"
from waveshare_epd import epd7in5_V2

def findAndFlip():
   prominentThisTime = ""
   if exists("/home/donal/screen/lasttop.txt"):
      with open("/home/donal/screen/lasttop.txt") as f:
         lasttime = f.readline()
         f.close()
         #print("state exists; lasttime =", lasttime)
   else:
      print("new start; bootstrap by saying last time we showed the beeb")
      lasttime = "beeb"
   if (lasttime == "beeb"):
      prominentThisTime = "cal"
   else:
      prominentThisTime = "beeb"
   f = open("/home/donal/screen/lasttop.txt", "w")
   f.write(prominentThisTime)
   f.close()
   return prominentThisTime

def createBeebFrame(headFont, lcFont):
   feed = feedparser.parse('http://feeds.bbci.co.uk/news/rss.xml')
   #print(feed.entries[0].title)
   bbcHeadlines = Image.new('1', (525, 275), 1)
   bbcDraw = ImageDraw.Draw(bbcHeadlines)
   bbcDraw.text((125,5), 'Beeb Headlines','black', headFont)
   for x in range(0,10):
      #print(feed.entries[x].title, len(feed.entries[x].title))
      headlineString = feed.entries[x].title
      if (len(headlineString) > 60):
         #print("hit: ", feed.entries[x].title)
         headlineString = (headlineString[0:57]+"...")
      bbcDraw.text((5,(x*20)+30), headlineString, 'black', lcFont)
   #bbcHeadlines.save('beeb.bmp')
   beebWithBorder = ImageOps.expand(bbcHeadlines, border=1,fill='black')
   return beebWithBorder

def createCalFrame():
   eventsImg = Image.open(io.BytesIO(imgkit.from_url('file:///home/donal/screen/eventsTable.html', False)))
   w,h = eventsImg.size
   croppedEventsImg = eventsImg.crop((5,5, w-550, h,))

   #croppedEventsImg.save('events.bmp')
   return croppedEventsImg


def whatsUpTomorrow():
   nextUpMessage = "Nothing happening\ntomorrow"
   with open('/home/donal/screen/events.txt', "r") as eventDataFile:
      for line in eventDataFile:
         lineData = line.split("||")
         evStartDate = datetime.strptime(lineData[0], '%A %d/%m/%Y')
         #print("comparing event date", evStartDate.date(), "with ", (datetime.today().date()+timedelta(days = 1)))
         if (evStartDate.date() == (datetime.today().date() + timedelta(days = 1))):
            #print("we have an event tomorrow: ", lineData[2].rstrip())
            nextUpMessage = "First up tomorrow: \n" + lineData[2].rstrip()
            break
   return nextUpMessage

def drawToScreen(finalLayoutImg):
   try:
      epd = epd7in5_V2.EPD()
      epd.init()
      epd.Clear()
      epd.display(epd.getbuffer(finalLayoutImg))
   except IOError as e:
      print(e)

def main():
   # set up some font definitions:
   #lcFont = ImageFont.truetype("/usr/share/fonts/truetype/msttcorefonts/comic.ttf",14, encoding="unic")
   #headFont = ImageFont.truetype("/usr/share/fonts/truetype/msttcorefonts/comic.ttf",15, encoding="unic")
   #bannerFont = ImageFont.truetype("/usr/share/fonts/truetype/msttcorefonts/comic.ttf",25, encoding="unic")
   lcFont = ImageFont.truetype(libdir+"/Font.ttc", 18)
   headFont = ImageFont.truetype(libdir+"/Font.ttc", 20)
   nextUpFont = ImageFont.truetype(libdir+"/Font.ttc", 25)
   dateFont = ImageFont.truetype(libdir+"/Font.ttc", 40)
   # create main Image to hold the content:
   finalLayoutImg = Image.new('1', (800, 480), color = 'white')
   # create the beeb image:
   beebWithBorder = createBeebFrame(headFont, lcFont)
   # same for the calendar events table:
   calEvents = createCalFrame()
   whatHappeningTmrw = whatsUpTomorrow()
   currentDate = datetime.now().strftime("%A\n%d %B")
   # prepare the main image to be 'drawn' - i.e., so text can be added:
   mainLayoutDraw = ImageDraw.Draw(finalLayoutImg)
   mainLayoutDraw.text((20,30), whatHappeningTmrw, 'black', nextUpFont)
   mainLayoutDraw.text((570,350), currentDate, 'black', dateFont)
   # figure out if beeb or calendar data is prominent - i.e., pasted second and
   # in the left corner 
   prominentFrame = findAndFlip()
   if (prominentFrame == "beeb"):
      beebTopXY=(20,150)
      calBackXY=(325,10)
      finalLayoutImg.paste(calEvents, calBackXY)
      finalLayoutImg.paste(beebWithBorder, beebTopXY)
   else:
      beebBackXY=(260,11)
      calTopXY=(20,125)
      finalLayoutImg.paste(beebWithBorder, beebBackXY)
      finalLayoutImg.paste(calEvents, calTopXY)
   finalLayoutImg.save('final1.bmp')
   drawToScreen(finalLayoutImg)

if __name__ == '__main__':
    main()
