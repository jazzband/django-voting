from django.contrib.auth.models import User 
from django.test import TestCase

from voting.models import Vote 
from voting.tests.models import Item

# Basic voting ###############################################################

class BasicVotingTests(TestCase):

    def setUp(self):
        self.item = Item.objects.create(name='test1')
        self.users = []
        for username in ['u1', 'u2', 'u3', 'u4']:
            self.users.append(User.objects.create_user(username, '%s@test.com' % username, 'test'))

    def test_novotes(self):
        result = Vote.objects.get_score(self.item)
        self.assertEqual(result, {'score': 0, 'num_votes': 0})

    def test_onevoteplus(self):
        Vote.objects.record_vote(self.item, self.users[0], +1)
        result = Vote.objects.get_score(self.item)
        self.assertEqual(result, {'score': 1, 'num_votes': 1})

    def test_onevoteminus(self):
        Vote.objects.record_vote(self.item, self.users[0], -1)
        result = Vote.objects.get_score(self.item)
        self.assertEqual(result, {'score': -1, 'num_votes': 1})

    def test_onevotezero(self):
        Vote.objects.record_vote(self.item, self.users[0], 0)
        result = Vote.objects.get_score(self.item)
        self.assertEqual(result, {'score': 0, 'num_votes': 0})

    def test_allvoteplus(self):
        for user in self.users:
            Vote.objects.record_vote(self.item, user, +1)
        result = Vote.objects.get_score(self.item)
        self.assertEqual(result, {'score': 4, 'num_votes': 4})
        for user in self.users[:2]:
            Vote.objects.record_vote(self.item, user, 0)
        result = Vote.objects.get_score(self.item)
        self.assertEqual(result, {'score': 2, 'num_votes': 2})
        for user in self.users[:2]:
            Vote.objects.record_vote(self.item, user, -1)
        result = Vote.objects.get_score(self.item)
        self.assertEqual(result, {'score': 0, 'num_votes': 4})

    def test_wrongvote(self):
        try:
            Vote.objects.record_vote(self.item, self.users[0], -2)
        except ValueError as e:
            self.assertEqual(e.args[0], "Invalid vote (must be +1/0/-1)")
        else:
            self.fail("Did nor raise 'ValueError: Invalid vote (must be +1/0/-1)'")

# Retrieval of votes #########################################################

class VoteRetrievalTests(TestCase):
    def setUp(self):
        self.items = []
        for name in ['test1', 'test2', 'test3', 'test4']:
            self.items.append(Item.objects.create(name=name))
        self.users = []
        for username in ['u1', 'u2', 'u3', 'u4']:
            self.users.append(User.objects.create_user(username, '%s@test.com' % username, 'test'))
        for user in self.users:
            Vote.objects.record_vote(self.items[0], user, +1)
        for user in self.users[:2]:
            Vote.objects.record_vote(self.items[0], user, 0)
        for user in self.users[:2]:
            Vote.objects.record_vote(self.items[0], user, -1)
        Vote.objects.record_vote(self.items[1], self.users[0], +1)
        Vote.objects.record_vote(self.items[2], self.users[0], -1)
        Vote.objects.record_vote(self.items[3], self.users[0], 0)

    def test_get_pos_vote(self):
        vote = Vote.objects.get_for_user(self.items[1], self.users[0])
        result = (vote.vote, vote.is_upvote(), vote.is_downvote())
        expected = (1, True, False)
        self.assertEqual(result, expected)

    def test_get_neg_vote(self):
        vote = Vote.objects.get_for_user(self.items[2], self.users[0])
        result = (vote.vote, vote.is_upvote(), vote.is_downvote())
        expected = (-1, False, True)
        self.assertEqual(result, expected)

    def test_get_zero_vote(self):
        self.assertTrue(Vote.objects.get_for_user(self.items[3], self.users[0]) is None)

    def test_in_bulk1(self):
        votes = Vote.objects.get_for_user_in_bulk(self.items,
            self.users[0])
        self.assertEqual(
            [(id, vote.vote) for id, vote in votes.items()],
            [(1, -1), (2, 1), (3, -1)]) 
        
    def test_empty_items(self):
        result = Vote.objects.get_for_user_in_bulk([], self.users[0])
        self.assertEqual(result, {})

    def test_get_top(self):
        for user in self.users[1:]:
            Vote.objects.record_vote(self.items[1], user, +1)
            Vote.objects.record_vote(self.items[2], user, +1)
            Vote.objects.record_vote(self.items[3], user, +1)
        result = list(Vote.objects.get_top(Item))
        expected = [(self.items[1], 4), (self.items[3], 3), (self.items[2], 2)]
        self.assertEqual(result, expected)

    def test_get_bottom(self):
        for user in self.users[1:]:
            Vote.objects.record_vote(self.items[1], user, +1)
            Vote.objects.record_vote(self.items[2], user, +1)
            Vote.objects.record_vote(self.items[3], user, +1)
        for user in self.users[1:]:
            Vote.objects.record_vote(self.items[1], user, -1)
            Vote.objects.record_vote(self.items[2], user, -1)
            Vote.objects.record_vote(self.items[3], user, -1)
        result = list(Vote.objects.get_bottom(Item))
        expected = [(self.items[2], -4), (self.items[3], -3), (self.items[1], -2)]
        self.assertEqual(result, expected)

    def test_get_scores_in_bulk(self):
        for user in self.users[1:]:
            Vote.objects.record_vote(self.items[1], user, +1)
            Vote.objects.record_vote(self.items[2], user, +1)
            Vote.objects.record_vote(self.items[3], user, +1)
        for user in self.users[1:]:
            Vote.objects.record_vote(self.items[1], user, -1)
            Vote.objects.record_vote(self.items[2], user, -1)
            Vote.objects.record_vote(self.items[3], user, -1)
        result = Vote.objects.get_scores_in_bulk(self.items)
        expected = {
            1: {'score': 0, 'num_votes': 4},
            2: {'score': -2, 'num_votes': 4},
            3: {'score': -4, 'num_votes': 4},
            4: {'score': -3, 'num_votes': 3},
        }
        self.assertEqual(result, expected)

    def test_get_scores_in_bulk_no_items(self):
        result = Vote.objects.get_scores_in_bulk([])
        self.assertEqual(result, {})
