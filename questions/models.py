from django.db import models

# Create your models here.
class Question(models.Model):
	question = models.CharField(max_length=200)
	# comma separated
	answerChoices = models.CharField(max_length=200)
	correctChoice = models.CharField(max_length=200)
	level = models.IntegerField()
	pub_date = models.DateTimeField('date published')
	created_on = models.DateField(auto_now_add=True)

	def save(self, *args, **kwargs):
		import re

		if not re.match('^([\D\d]+(?:,?[\D\d]+)?)$', self.answerChoices):
			raise ValueError('%s field must contain csv.')
		else:
			super(Question, self).save(*args, **kwargs)

class QuestionLog(models.Model):
	from subscriber.models import Subscriber

	question = models.ForeignKey(Question, related_name='question_reference')
	subsciber = models.ForeignKey(Subscriber, related_name='subscriber_reference')
	reply = models.CharField(max_length=200)
	isComplete = models.BooleanField()
	created_on = models.DateField(auto_now_add=True)
