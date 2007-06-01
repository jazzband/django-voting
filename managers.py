from django.db import backend, connection, models
from django.contrib.contenttypes.models import ContentType

class VoteManager(models.Manager):
    def get_score(self, obj):
        """
        Get a dictionary containing the total score for ``obj`` and
        the number of votes it's received.
        """
        query = """
        SELECT SUM(vote), COUNT(*)
        FROM %s
        WHERE content_type_id = %%s
          AND object_id = %%s""" % backend.quote_name(self.model._meta.db_table)
        ctype = ContentType.objects.get_for_model(obj)
        cursor = connection.cursor()
        cursor.execute(query, [ctype.id, obj._get_pk_val()])
        result = cursor.fetchall()[0]
        return {'score': result[0] or 0, 'num_votes': result[1]}

    def get_scores_in_bulk(self, objects):
        """
        Get a dictionary mapping object ids to total score and number
        of votes for each object.
        """
        query = """
        SELECT object_id, SUM(vote), COUNT(vote)
        FROM %s
        WHERE content_type_id = %%s
          AND object_id IN (%s)
        GROUP BY object_id""" % (
            backend.quote_name(self.model._meta.db_table),
            ','.join(['%s'] * len(objects))
        )
        ctype = ContentType.objects.get_for_model(objects[0])
        cursor = connection.cursor()
        cursor.execute(query, [ctype.id] + [obj._get_pk_val() for obj in objects])
        results = cursor.fetchall()
        return dict([(object_id, {
                          'score': score,
                          'num_votes': num_votes,
                      }) for object_id, score, num_votes in results])

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
            v = self.get(user=user, content_type=ctype, object_id=obj._get_pk_val())
            if vote == 0:
                v.delete()
            else:
                v.vote = vote
                v.save()
        except models.ObjectDoesNotExist:
            if vote != 0:
                self.create(user=user, content_type=ctype,
                            object_id=obj._get_pk_val(), vote=vote)

    def get_top(self, Model, limit=10, reversed=False):
        """
        Get the top N scored objects for a given model.

        Yields (object, score) tuples.
        """
        ctype = ContentType.objects.get_for_model(Model)
        query = """
        SELECT object_id, SUM(vote)
        FROM %s
        WHERE content_type_id = %%s
        GROUP BY object_id""" % backend.quote_name(self.model._meta.db_table)
        if reversed:
            query += ' HAVING SUM(vote) < 0 ORDER BY SUM(vote) ASC LIMIT %s'
        else:
            query += ' HAVING SUM(vote) > 0 ORDER BY SUM(vote) DESC LIMIT %s'
        cursor = connection.cursor()
        cursor.execute(query, [ctype.id, limit])
        results = cursor.fetchall()

        # Use in_bulk() to avoid O(limit) db hits.
        objects = Model.objects.in_bulk([id for id, score in results])

        # Yield each object, score pair. Because of the lazy nature of generic
        # relations, missing objects are silently ignored.
        for id, score in results:
            if id in objects:
                yield objects[id], score

    def get_bottom(self, Model, limit=10):
        """
        Get the bottom (i.e. most negative) N scored objects for a given model.

        Yields (object, score) tuples.
        """
        return self.get_top(Model, limit, True)

    def get_for_user(self, obj, user):
        """
        Get the vote made on the given object by the given user, or
        ``None`` if no matching vote exists.
        """
        if not user.is_authenticated():
            return None
        ctype = ContentType.objects.get_for_model(obj)
        try:
            vote = self.get(content_type=ctype, object_id=obj._get_pk_val(), user=user)
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
                                     object_id__in=[obj._get_pk_val() for obj in objects],
                                     user__pk=user.id))
            vote_dict = dict([(vote.object_id, vote) for vote in votes])
        return vote_dict
