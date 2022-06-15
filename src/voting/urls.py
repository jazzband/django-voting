from django.urls import re_path

from .views import vote_on_object_with_lazy_model

urlpatterns = [
    re_path(
        r"^vote/(?P<app_label>[\w\.-]+)/(?P<model_name>\w+)/"
        r"(?P<object_id>\d+)/(?P<direction>up|down|clear)/$",
        vote_on_object_with_lazy_model,
        {
            "allow_xmlhttprequest": True,
        },
        name="voting_vote",
    ),
]
