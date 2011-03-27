from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'djzilla.views.home', name='home'),
    # url(r'^zilla/', include('zilla.jukebox.urls')),

    # Accounts:
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^accounts/profile/$', 'zilla.views.profile'),
    url(r'^accounts/register/$', 'zilla.views.register'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout'),

    # Jukebox:
    url(r'^jukebox/', "zilla.jukebox.views.index"),

    # Admin:
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
