from django import forms as djangoSimpleForm
from django.core.exceptions import ValidationError

class StrippedRegexField(djangoSimpleForm.RegexField):
    """A custom form field inheriting the RegexField class of django forms module.

    It helps us in getting an input value which matches a particular regular expression.

    It will have 2 default validation errors.
            1) if required is set as True
            2) if the regular expression check fails on your input.
                * you can pass a custom validation error by assigning the error string to arg 'error_message'.

    Example:
            StrippedRegexField(regex = '^[\D]+$', widget = forms.TextInput(), required = True)
            regex : a regular expression(both string and python re Pattern objects accepted) which should match your input.

    For more details on the args and validation please refer to the super classes.

    @author:  Jayakrishnan Damodaran
    """
    def clean(self, value):
        if value:
            value = value.strip()
        return super(StrippedRegexField, self).clean(value)

class RegistrationForm(djangoSimpleForm.Form):
	username = djangoSimpleForm.CharField(widget=djangoSimpleForm.TextInput(attrs={'class' : 'form-control'}), required=True)
	password = djangoSimpleForm.CharField(widget=djangoSimpleForm.PasswordInput(attrs={'class' : 'form-control'}), required=True)
	mobileNumber = StrippedRegexField(regex='^([\d]{10})$', widget=djangoSimpleForm.TextInput(attrs={'class' : 'form-control'}), required=True)

	def clean_mobileNumber(self):
		from subscriber.models import Subscriber

		if Subscriber.objects.filter(mobileNumber__exact=self.cleaned_data['mobileNumber']).count() > 0:
			raise ValidationError('Subscriber with mobile number already exists.')
		return self.cleaned_data['mobileNumber']
