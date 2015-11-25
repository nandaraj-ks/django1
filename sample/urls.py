from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'sample.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    (r'^accounts/login/', 'django.contrib.auth.views.login'),
    (r'^logout', 'django.contrib.auth.views.logout_then_login'),
    url(r'^register$', 'sample.views.registerUser'),
    url(r'^test$', 'sample.views.test_view'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('questions.urls')),
)
