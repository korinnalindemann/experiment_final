import random

from otree.api import *
from . import *
from random import randint

# classes/methods needed for writing tests: expect, Bot, Submission
class PlayerBot(Bot):

    def play_round(self):
        yield Vote_Red, dict(vote_rules = random.choice([0,1]))

        if self.player.participant.num_capi == 5:
            yield Instructions1
            yield Submission(Game, check_html=False)
            yield Results_Round
            if self.player.vote_rules == 1:
                yield Results_Red
            if self.player.vote_rules == 0:
                yield Results_Cap

        elif self.player.participant.num_redi == 5:
            yield Instructions1
            yield Submission(Game, check_html=False)
            yield Results_Round
            if self.player.vote_rules == 1:
                yield Results_Red
            if self.player.vote_rules == 0:
                yield Results_Cap

        else:
            yield NoGame