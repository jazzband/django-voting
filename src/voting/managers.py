# coding: utf-8

from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.db.models import Sum, Count
from django.contrib.contenttypes.models import ContentType

ZERO_VOTES_ALLOWED = getattr(settings, 'VOTING_ZERO_VOTES_ALLOWED', False)

class VoteManager(models.Manager):
    def get_score(self, obj):
        """
        Get a dictionary containing the total score for ``obj`` and
        the number of votes it's received.
        """
        ctype = ContentType.objects.get_for_model(obj)
        result = self.filter(
            object_id=obj._get_pk_val(),
            content_type=ctype
        ).aggregate(
            score=Sum('vote'),
            num_votes=Count('vote')
        )

        if result['score'] is None:
            result['score'] = 0
        return result

    def get_scores_in_bulk(self, objects):
        """
        Get a dictionary mapping object ids to total score and number
        of votes for each object.
        """
        object_ids = [o._get_pk_val() for o in objects]
        if not object_ids:
            return {}

        ctype = ContentType.objects.get_for_model(objects[0])

        queryset = self.filter(
            object_id__in=object_ids,
            content_type=ctype,
        ).values(
            'object_id',
        ).annotate(
            score=Sum('vote'), 
            num_votes=Count('vote')
        )

        vote_dict = {}
        for row in queryset:
            vote_dict[row['object_id']] = {
                'score': int(row['score']),
                'num_votes': int(row['num_votes']),
            }

        return vote_dict

    def record_vote(self, obj, user, vote):
        """
        Record a user's vote on a given object. Only allows a given user
        to vote once, though that vote may be changed.

        A zero vote indicates that any existing vote should be removed.
        """
        if vote not in (+1, 0, -1):
            raise ValueError('Invalid vote (must be +1/0/-1)')
        ctype = ContentType.objects.get_for_model(obj)
        try:
            v = self.get(user=user, content_type=ctype,
                         object_id=obj._get_pk_val())
            if vote == 0 and not ZERO_VOTES_ALLOWED:
                v.delete()
            else:
                v.vote = vote
                v.save()
        except models.ObjectDoesNotExist:
            if not ZERO_VOTES_ALLOWED and vote == 0:
                return
            self.create(user=user, content_type=ctype,
                        object_id=obj._get_pk_val(), vote=vote)

    def get_top(self, model, limit=10, reversed=False):
        """
        Get the top N scored objects for a given model.

        Yields (object, score) tuples.
        """
        ctype = ContentType.objects.get_for_model(model)
        results = self.filter(content_type=ctype).values('object_id').annotate(score=Sum('vote'))
        if reversed:
            results = results.order_by('score')
        else:
            results = results.order_by('-score')

        # Use in_bulk() to avoid O(limit) db hits.
        objects = model.objects.in_bulk([item['object_id'] for item in results[:limit]])

        # Yield each object, score pair. Because of the lazy nature of generic
        # relations, missing objects are silently ignored.
        for item in results[:limit]:
            id, score = item['object_id'], item['score']
            if not score:
                continue
            if id in objects:
                yield objects[id], int(score)

    def get_bottom(self, Model, limit=10):
        """
        Get the bottom (i.e. most negative) N scored objects for a given
        model.

        Yields (object, score) tuples.
        """
        return self.get_top(Model, limit, True)

    def get_for_user(self, obj, user):
        """
        Get the vote made on the given object by the given user, or
        ``None`` if no matching vote exists.
        """
        if not user.is_authenticated:
            return None
        ctype = ContentType.objects.get_for_model(obj)
        try:
            vote = self.get(content_type=ctype, object_id=obj._get_pk_val(),
                            user=user)
        except models.ObjectDoesNotExist:
            vote = None
        return vote

    def get_for_user_in_bulk(self, objects, user):
        """
        Get a dictionary mapping object ids to votes made by the given
        user on the corresponding objects.
        """
        vote_dict = {}
        if len(objects) > 0:
            ctype = ContentType.objects.get_for_model(objects[0])
            votes = list(self.filter(content_type__pk=ctype.id,
                                     object_id__in=[obj._get_pk_val() \
                                                    for obj in objects],
                                     user__pk=user.id))
            vote_dict = dict([(vote.object_id, vote) for vote in votes])
        return vote_dict
