from django.db import models

# Create your models here.
class Subscriber(models.Model):
	from django.contrib.auth.models import User

	user = models.OneToOneField(User, related_name='subscriber_user_reference')
	mobileNumber = models.CharField(max_length=10)
	level = models.IntegerField()
	mooblePoint = models.IntegerField()
	created_on = models.DateField(auto_now_add=True)
