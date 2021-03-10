# coding: utf-8

from __future__ import unicode_literals

from django.conf.urls import url
from .views import vote_on_object_with_lazy_model


urlpatterns = [
    url(
        r"^vote/(?P<app_label>[\w\.-]+)/(?P<model_name>\w+)/"
        "(?P<object_id>\d+)/(?P<direction>up|down|clear)/$",
        vote_on_object_with_lazy_model,
        {
            "allow_xmlhttprequest": True,
        },
        name="voting_vote",
    ),
]
