from datetime import datetime
from django.core.management.base import NoArgsCommand
import flickrapi
from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import tostring
from djangr.models import Photo
from django.conf import settings

class Command(NoArgsCommand):
    
    def handle_noargs(self, **options):
        """
        Poll flickr for photos and create save an onject to the database for
        each that isn't currently represented.
        
        Todo: keys and ids from settings
        """
        for account in settings.DJANGR_ACCOUNTS:
        
            flickr = flickrapi.FlickrAPI(account['api_key'])
            photos_el = flickr.photos_search(user_id=account['user_id'])
        
            for photo_el in photos_el.findall('photos/photo'):
            
                id = int(photo_el.get('id'))
                try:
                    photo = Photo.objects.get(id=id)
                    print 'Updating photo %s' % id
                except Photo.DoesNotExist:
                    print 'Creating a new photo %s' % id
                    photo = Photo()
                photo.id = id
                photo.xml = tostring(photo_el)
                photo.owner = photo_el.get('owner')
                photo.secret = photo_el.get('secret')
                info_el = flickr.photos_getinfo(
                    user_id=account['user_id'],
                    photo_id=photo.id, secret=photo.secret)
                photoinfo_el = info_el.find('photo')
                photo.infoxml = tostring(photoinfo_el)
                dateuploaded = float(photoinfo_el.get('dateuploaded'))
                photo.dateuploaded = datetime.fromtimestamp(dateuploaded)
                photo.description = photoinfo_el.findtext('description')
                photo.title = photoinfo_el.findtext('title')
                photo.farm = int(photoinfo_el.get('farm'))
                photo.server = int(photoinfo_el.get('server'))
                
                location = photoinfo_el.find('location')
                if location:
                    latitude = location.get('latitude')
                    longitude = location.get('longitude')
                    if latitude and longitude:
                        photo.longitude = longitude
                        photo.latitude = latitude
                photo.save()

            
# Example photo_el and its info_el
"""
<photo 
    farm="5" 
    id="4849809952" 
    isfamily="0" 
    isfriend="0" 
    ispublic="1" 
    owner="51991206@N08" 
    secret="d4d429a7fe" 
    server="4078" 
    title="Graham in the undergrowth" />
	
<photo dateuploaded="1280676409" farm="5" id="4849809952" isfavorite="0" license="0" media="photo" originalformat="jpg" originalsecret="bd80e144dd" rotation="0" secret="d4d429a7fe" server="4078" views="0">
	<owner location="" nsid="51991206@N08" realname="Ben Glynn" username="benglynn" />
	<title>Graham in the undergrowth</title>
	<description />
	<visibility isfamily="0" isfriend="0" ispublic="1" />
	<dates lastupdate="1280676436" posted="1280676409" taken="2010-07-31 13:44:40" takengranularity="0" />
	<editability canaddmeta="0" cancomment="0" />
	<usage canblog="0" candownload="1" canprint="0" canshare="1" />
	<comments>0</comments>
	<notes />
	<tags />
	<location accuracy="16" context="0" latitude="51.428858" longitude="-2.491025" place_id="r4cVRCaYAJV4HQ" woeid="11971">
		<neighbourhood place_id="r4cVRCaYAJV4HQ" woeid="11971">Barrs Court</neighbourhood>
		<locality place_id="4bjYj3.YApXUcg" woeid="13963">Bristol</locality>
		<county place_id="jLTl2QOYA5qMknc0pw" woeid="12602180">City of Bristol</county>
		<region place_id="pn4MsiGbBZlXeplyXg" woeid="24554868">England</region>
		<country place_id="DevLebebApj4RVbtaQ" woeid="23424975">United Kingdom</country>
	</location>
	<geoperms iscontact="0" isfamily="0" isfriend="0" ispublic="1" />
	<urls>
		<url type="photopage">http://www.flickr.com/photos/benglynn/4849809952/</url>
	</urls>
</photo>
"""