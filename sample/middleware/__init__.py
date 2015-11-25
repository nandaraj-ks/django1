class HandleRequests(object):
	def process_request(self, request):
		import re
		import logging
		from django import http
		from django.shortcuts import render

		if not request.user.is_authenticated() and not re.match(SAFE_TO_REDIRECT_URI_REGEX, request.path):
			logging.info('User not logged in. Going to redirect to Login page.')
			return http.HttpResponseRedirect('/accounts/login/?next=%s' % request.path)
		return None
SAFE_TO_REDIRECT_URI_REGEX = '(/test)|(/accounts/login/)|(/admin/)|(/register)|(/createQuestion/([0-9]+)/([0-9]+))'