from django.conf.urls.defaults import *


urlpatterns = patterns('',
    url(r"^vote/(?P<app_label>[\w\.-]+)/(?P<model_name>\w+)/"\
        "(?P<object_id>\d+)/(?P<direction>up|down|clear)/$", 
        "voting.views.vote_on_object_with_lazy_model", { 
            "allow_xmlhttprequest": True, 
        },
        name="voting_vote"
    ),
)

