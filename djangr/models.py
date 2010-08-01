from django.db import models

class Photo(models.Model):
    """
    Store photo details returned by the flickr api.
    """
    title = models.CharField(max_length=180)
    description = models.TextField(null=True, blank=True)
    farm = models.IntegerField()
    secret = models.CharField(max_length=50)
    server = models.IntegerField()
    
    photoxml = models.XMLField(schema_path=None)
    phoinfoxml = models.XMLField(schema_path=None)
    
    longitude = models.FloatField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    
    def geturl(self, size='s'):
        return ('http://farm%(farm)s.static.flickr.com/%(server)s' +\
            '/%(id)s_%(secret)s%(size)s.jpg') % {
            'farm': self.farm, 
            'server': self.server, 
            'id': self.id, 
            'secret': self.secret, 
            'size': size and '_%s' % size or ''}
