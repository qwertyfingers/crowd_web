from django.conf.urls import patterns, url




urlpatterns = patterns('mTurk1.views',
                       url(r'^(?P<key>[A-Z0-9]{30})/$', 'simulation',{'cur_app':'mturk1_live'},name='simulation',),
                       url(r'^(?P<key>[A-Z0-9]{30})(?P<reward_key>[A-Z0-9]{30})/thankyou/$', 'thankyou_post',{'cur_app':'mturk1_live'},  name='thankyou_post',)
                       )