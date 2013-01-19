from django.conf.urls import patterns, url




urlpatterns = patterns('mTurk1.views',
                       url(r'^([A-Z0-9]{30})/$', 'simulation',{'cur_app':'mturk1_live'},name='simulation',),
                       url(r'^([A-Z0-9]{30})([A-Z0-9]{30})/thankyou/$', 'thankyou_post',{'cur_app':'mturk1_live'},  name='thankyou_post',)
                       )