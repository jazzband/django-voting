from django.db import backend, connection, models
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from voting.managers import VoteManager

# Generic relations were moved in Django revision 5172
try:
    from django.contrib.contenttypes import generic
except ImportError:
    import django.db.models as generic

SCORES = (
    ('+1', +1),
    ('-1', -1),
)

class Vote(models.Model):
    user = models.ForeignKey(User)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    object = generic.GenericForeignKey('content_type', 'object_id')
    vote = models.SmallIntegerField(choices=SCORES)

    objects = VoteManager()

    class Meta:
        db_table = 'votes'
        verbose_name = 'Vote'
        verbose_name_plural = 'Votes'
        # Enforce one vote per user per object
        unique_together = (('user', 'content_type', 'object_id'),)

    class Admin:
        pass

    def __str__(self):
        return '%s: %s on %s' % (self.user, self.vote, self.object)

    def is_upvote(self):
        return self.vote == 1

    def is_downvote(self):
        return self.vote == -1