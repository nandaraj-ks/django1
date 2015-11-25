from django import forms as djangoSimpleForm
from django.core.exceptions import ValidationError
from django.forms.widgets import RadioSelect
from django.utils.safestring import mark_safe

class HorizontalRadioRenderer(RadioSelect.renderer):
	""" this overrides widget method to put radio buttons horizontally
		instead of vertically.
	"""
	def render(self):
			"""Outputs radios"""
			# returnValue = 'u\n'
			# eachValue = []
			# for w in self:
			#     eachValue.append(u'%s\n' % w)
			#     if (len(eachValue) % 3 == 0):
			#         returnValue.join(eachValue)
			#         eachValue = []
			# if len(eachValue) > 0:
			#     returnValue.join(eachValue)
			# return mark_safe(returnValue)
			return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))

class HorizontalRadioSelect(RadioSelect):
	renderer = HorizontalRadioRenderer

class ChoiceForm(djangoSimpleForm.Form):
	def __init__(self, question, *args, **kwargs):
		super(ChoiceForm, self).__init__(*args, **kwargs)
		
		questionChoices = [(unicode(ch.strip()), unicode(ch.strip())) for ch in question.answerChoices.split(',')]
		self.fields['choiceSelect'].choices = questionChoices

	choiceSelect = djangoSimpleForm.ChoiceField(
		widget=HorizontalRadioSelect(),
		choices=[],
		required=False,
		initial=None
	)
	questionHidden = djangoSimpleForm.CharField(widget=djangoSimpleForm.HiddenInput())