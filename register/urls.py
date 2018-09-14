from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.LogInView.as_view(), name='login'),
]
