from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^tests/test_package/',include('test_package.urls',namespace="t_p")), # look for test pages
                       url(r'^exp1/demo/',include('mTurk1.demo_urls',namespace="mturk1_demo", app_name="mturk1")),
                       url(r'^exp1/live/',include('mTurk1.live_urls',namespace="mturk1_live", app_name="mturk1")),
                       url(r'^admin/', include(admin.site.urls)),
                       #url(r'^(.+)$','mTurk1.views.tasks_no_match'), #look for everything else......... (needed?)
  
)
