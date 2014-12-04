from django.db import models

class UserImage(models.Model):
	latitude = models.DecimalField(null=True,max_digits=10,decimal_places=4)
	longitude = models.DecimalField(null=True, max_digits=10,decimal_places=4)
	image_url = models.CharField(null=True)

	class Meta:
    	 app_label = 'userimage'
