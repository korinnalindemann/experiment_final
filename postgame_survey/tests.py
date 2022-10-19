import random

from otree.api import *
from . import *
from random import randint

# classes/methods needed for writing tests: expect, Bot, Submission
class PlayerBot(Bot):

    def play_round(self):
        yield PS2, dict(redpref = random.randint(0,10))
        yield PS3, dict(redpref_state =  random.randint(0,10),
                        redpref_tax = random.randint(0,10))
        yield PS4, dict(man_check =  random.randint(0,10))
        yield PS5, dict(attcheck1 = random.choice(['Ja', 'Nein', 'Weiß nicht']),
                        attcheck2 = random.choice(['Beide haben weniger Punkte erzielt als ich',
               'Jemand hat mehr und jemand hat weniger Punkte erzielt als ich',
               'Beide haben mehr Punkte erzielt als ich',
               'Weiß nicht' ]))

        yield PS12, dict(state_edu = random.choice(['Baden-Württemberg','Bayern', 'Berlin', 'Brandenburg', 'Bremen',
              'Hamburg', 'Hessen', 'Mecklenburg-Vorpommern', 'Niedersachsen',
              'Nordrhein-Westfalen', 'Rheinland-Pfalz', 'Saarland', 'Sachsen',
              'Sachsen-Anhalt', 'Schleswig-Holstein', 'Thüringen']))
        yield PS14, dict(ruralurban = random.choice(['Eher ländlich',  'Etwas zwischen ländlich und städtisch', 'Eher städtisch','Weiß nicht']))
        yield PS15, dict(soc_statfam = random.choice(['Unterschicht',
                   'Untere Mittelschicht',
                   'Mittelschicht',
                   'Obere Mittelschicht',
                   'Oberschicht']))
        yield PS16, dict(occupation=random.choice(
            ['Vollzeit beschäftigt', 'Teilzeit beschäftigt', 'Selbständig', 'Nicht berufstätig (Hausfrau/Hausmann)',
             'In schulischer oder universitärer Ausbildung', 'Lehrling/Azubi', 'Momentan arbeitslos',
             'Rente/pensioniert',
             'In Mutterschutz/Elternzeit', 'Anderes']))
        yield PS17, dict(ethnic_min = random.choice(['Ja', 'Nein', 'Weiß nicht']))
        yield PS18, dict(income = random.randint(1,10))
        yield Thanks, dict(consent2 = random.choice([0,1]))
        yield Submission(Redirect, check_html=False)