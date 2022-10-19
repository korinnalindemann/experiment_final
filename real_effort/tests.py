import random

from otree.api import *
from . import *
from random import randint

# classes/methods needed for writing tests: expect, Bot, Submission
class PlayerBot(Bot):

    def play_round(self):
        if self.player.round_number == 1:
            yield instr
        yield Instructions1
        yield Submission(Game, check_html=False)
        yield Results_Round
        if self.player.participant.redistribution == 1:
            yield Results_Red
        else:
            yield Results_Cap