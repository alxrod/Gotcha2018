from django.conf.urls import url

from . import views

urlpatterns = [
	url(r"^$", views.index, name="index"),
	url(r"^pull-user/(?P<player_id>[0-9]+)/$", views.getPlayer, name="getPlayer"),
	url(r"^pull-rel/(?P<rel_id>[0-9]+)/$", views.getTargetRel, name="getTargetRel"),
	url(r"^tag/(?P<tagger_id>[0-9]+)/$", views.tagPlayer, name="tagPlayer"),
	url(r"^get-recent/$", views.getRecent, name="getRecent"),
	url(r"^out-rel/$", views.getClassTags, name="getClassTags"),
	
]

