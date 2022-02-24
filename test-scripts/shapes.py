import os
import time
import logging
import requests
import json
from libs.functions import get_icon, indent, indentThirds, paste, write_weather, get_desc 
from datetime import datetime
from libs.waveshare_epd import epd7in5b_V2
from PIL import Image, ImageDraw, ImageFont

FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'

try:
    # Display init, clear
    display = epd7in5b_V2.EPD()
    display.init()
    display.Clear() # 0: Black, 255: White

    h = display.height #480
    w = display.width #800
    #print('width:', w) #800
    #print('height:', h) #480
    hHalf = display.height / 2
    wHalf = display.width / 2


    #### IMAGE CODE ####
    tempText = ImageFont.truetype(FONT, 90, index=0)
    bodyText = ImageFont.truetype(FONT, 30, index=0)
    timeText = ImageFont.truetype(FONT, 20, index=0)
    condText = ImageFont.truetype(FONT, 40, index=0)
    imageBlack = Image.new(mode='1', size=(w, h), color=255)
    drawBlack = ImageDraw.Draw(imageBlack)
    imageRed = Image.new(mode='1', size=(w, h), color=255)
    drawRed = ImageDraw.Draw(imageRed)
    dt = datetime.now()


    drawBlack.rectangle((0,0,400,240), fill=0, outline=0)
    drawBlack.rectangle((50,50,350,190), fill=1, outline=1)
    drawRed.rectangle((100,100,300,140), fill=0, outline=0)
    drawRed.rectangle((400,0,800,240), fill=0, outline=0)
    drawBlack.rectangle((400,240,800,480), fill=0, outline=0)
    drawRed.rectangle((0,240,400,480), fill=0, outline=0)
    drawRed.text((indentThirds('some stuff',condText,w), 2), 'some stuff', font=condText, fill=1, align='left')

    gomezText = 'GoMeZ gOmEz GoMeZ'
    
    drawRed.text((indent(gomezText,tempText,w), 0), gomezText, font=tempText, fill=1, align='left')
    drawBlack.text((indent(gomezText,tempText,w), 0), gomezText, font=tempText, fill=0, align='left')
    
    drawRed.text((indent(gomezText,tempText,w), 60), gomezText, font=tempText, fill=0, align='left')
    drawBlack.text((indent(gomezText,tempText,w), 60), gomezText, font=tempText, fill=1, align='left')

    drawRed.text((indent(gomezText,tempText,w), 120), gomezText, font=tempText, fill=1, align='left')
    drawBlack.text((indent(gomezText,tempText,w), 120), gomezText, font=tempText, fill=0, align='left')

    drawRed.text((indent(gomezText,tempText,w), 180), gomezText, font=tempText, fill=0, align='left')
    drawBlack.text((indent(gomezText,tempText,w), 180), gomezText, font=tempText, fill=1, align='left')

    drawRed.text((indent(gomezText,tempText,w), 240), gomezText, font=tempText, fill=1, align='left')
    drawBlack.text((indent(gomezText,tempText,w), 240), gomezText, font=tempText, fill=0, align='left')

    drawRed.text((indent(gomezText,tempText,w), 300), gomezText, font=tempText, fill=0, align='left')
    drawBlack.text((indent(gomezText,tempText,w), 300), gomezText, font=tempText, fill=1, align='left')

    drawRed.text((indent(gomezText,tempText,w), 360), gomezText, font=tempText, fill=1, align='left')
    drawBlack.text((indent(gomezText,tempText,w), 360), gomezText, font=tempText, fill=0, align='left')

    drawRed.text((indent(gomezText,tempText,w), 420), gomezText, font=tempText, fill=0, align='left')
    drawBlack.text((indent(gomezText,tempText,w), 420), gomezText, font=tempText, fill=1, align='left')

    drawRed.text((indent(gomezText,tempText,w), 480), gomezText, font=tempText, fill=0, align='left')
    drawBlack.text((indent(gomezText,tempText,w), 480), gomezText, font=tempText, fill=1, align='left')

    display.display(display.getbuffer(imageBlack),display.getbuffer(imageRed))
    



except IOError as e:
    print(e)
