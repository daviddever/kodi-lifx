import xbmc
import xbmcaddon
import xbmcgui
import os
import sys
import colorsys

from lifxlan import *

#def get_bulb_ips:
#        ips = []
#        num_lights = None
#        lifx = lifxlan.LifxLAN(num_lights)
#        devices = lifxlan.lifx.get_lights()     

#	for d in devices:
#        	ips.append(d.ip_addr)

#	return ips

lifxlan=LifxLAN()

useLegacyApi   = True
capture = xbmc.RenderCapture()

if useLegacyApi:
	capture.capture(32, 32, xbmc.CAPTURE_FLAG_CONTINUOUS)

#lights = get_bulb_ips()

#print 'Found LIFX lights'
#for d in lights:
#	print d
 

class PlayerMonitor( xbmc.Player ):
	def __init__( self, *args, **kwargs ):
		xbmc.Player.__init__( self )

	def onPlayBackStarted( self ):
		if not useLegacyApi:
			capture.capture(32, 32)


while not xbmc.abortRequested:
	xbmc.sleep(100)
	if capture.getCaptureState() == xbmc.CAPTURE_STATE_DONE:
		width = capture.getWidth();
		height = capture.getHeight();
		pixels = capture.getImage(1000);

		if useLegacyApi:
			capture.waitForCaptureStateChangeEvent(1000)
			
		pixels = capture.getImage(1000)

		red = [];
		green = [];
		blue = [];

                color = []

		for y in range(height):
			row = width * y * 4
			for x in range(width):
				red.append(pixels[row + x * 4 + 2]);
				green.append(pixels[row + x * 4 + 1]);
				blue.append(pixels[row + x * 4]);


		red = (sum(red)/len(red))/255.00;
		green = (sum(green)/len(green))/255.00;
		blue = (sum(blue)/len(blue))/255.00;

		hsb = colorsys.rgb_to_hsv(red, green, blue);

		huevalue = int(hsb[0]*65535);
		satvalue = int(hsb[1]*65535);
		brightnessvalue = int(hsb[2]*65535);

                color.append(huevalue)
                color.append(satvalue)
                color.append(brightnessvalue)
                color.append(4000)

		try:
			lifxlan.set_color_all_lights(color, rapid=True)
		except:
			print "Caught exception socket.error"


if ( __name__ == "__main__" ):

	player_monitor = PlayerMonitor()

	try:
		capture.getCaptureState()
	except AttributeError:
		useLegacyApi = False
