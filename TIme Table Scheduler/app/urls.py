from django.conf.urls import url, include
from .views import *

urlpatterns = [
    url(r'^login page1', login1),
    url(r'page2/login',signup),
	url(r'^$', index),
    url(r'^accept_data/', accept),
    url(r'^printf/', printf),
    url(r'^demo/', tt_generator),
    url(r'^viewas/', viewAs),
    url(r'^fileupload/',simple_upload),
    url(r'^savedtt/',savedTT),
    url(r'^download/',export_into_excel),
	url(r'^learn_more/',learn_more),

]
