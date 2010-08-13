from django.db import models

class Photo(models.Model):
    """
    Store photo details returned by the flickr api.
    """
    active = models.BooleanField()
    title = models.CharField(max_length=180)
    date = models.DateTimeField() # date taken, 'date' is polymorphic
    dateuploaded = models.DateTimeField()
    owner = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    farm = models.IntegerField()
    secret = models.CharField(max_length=50)
    server = models.IntegerField()
    
    xml = models.XMLField(schema_path=None)
    infoxml = models.XMLField(schema_path=None)
    
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
            
    class Meta(object):
        ordering = ['-date',]
