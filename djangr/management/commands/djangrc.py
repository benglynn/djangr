from django.core.management.base import NoArgsCommand
import flickrapi
from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import tostring
from djangr.models import Photo

class Command(NoArgsCommand):
    
    def handle_noargs(self, **options):
        """
        Poll flickr for photos and update database
        Todo: delete existing after successfull poll before saving
        Todo: keys and ids from settings
        """
        
        api_key = '1891b7f6d1c2c6336353e6a0a6dace11'
        flickr = flickrapi.FlickrAPI(api_key)
        photos_el = flickr.photos_search(user_id='51991206@N08')
        Photo.objects.all().delete()
        
        for photo_el in photos_el.findall('photos/photo'):
            
            # Create photo instance with basic data
            photo = Photo()
            photo.id = int(photo_el.get('id'))
            photo.secret = photo_el.get('secret')
            # Get detailed info
            info_el = flickr.photos_getinfo(user_id='50893299@N07',
                photo_id=photo.id, secret=photo.secret)
            photo_el = info_el.find('photo')
            photo.description = photo_el.findtext('description')
            photo.title = photo_el.findtext('title')
            photo.farm = int(photo_el.get('farm'))
            photo.server = int(photo_el.get('server'))
            photo.save()