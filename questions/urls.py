from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mooblesms.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'questions.views.viewQuestion'),
    url(r'^createQuestion/?([0-9]*)/?([0-9]*)$', 'questions.views.createQuestion'),
)
