from django.shortcuts import render, redirect

def registerUser(request):
	from django.contrib.auth.models import User
	from subscriber.forms import RegistrationForm
	from subscriber.models import Subscriber

	form = RegistrationForm()
	if request.POST:
		form = RegistrationForm(request.POST)
		if form.is_valid():
			user = User.objects.create_user(
				form.cleaned_data['username'], 
				password=form.cleaned_data['password']
			)
			user.save()
			dictToSave = {
				'user' : user,
				'mobileNumber' : form.cleaned_data['mobileNumber'],
				'level' : 0,
				'mooblePoint' : 0
			}
			sub = Subscriber(**dictToSave)
			sub.save()
			return redirect('/')
	template_values = {
		'form' : form
	}
	return render(request, 'registration/registration.html', template_values)

def test_view(request):
	from django import http

	response = http.HttpResponse()
	response.write('hi')
	return response
