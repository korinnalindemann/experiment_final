import random

from otree.api import *
from . import *
from random import randint

# classes/methods needed for writing tests: expect, Bot, Submission
class PlayerBot(Bot):

    def play_round(self):
        yield Welcome
        yield Einwilligung, dict(consent = 1)
        if self.player.consent == 0:
            yield Submission(SorryFull, check_html=False)
        if self.player.consent == 1:
            yield P1, dict(gender = random.choice(['Weiblich', 'Männlich', 'Divers']),
                           yob = random.randint(1940,2004),
                           edu = random.choice(['Hochschulabschluss, Volksschulabschluss',
                                                'Mittlere Reife, Realabschluss, Polytechnische Oberschule mit Abschluss 10. Klasse',
                                                'Fachhochschulabschluss, Abitur, erweiterte Oberschule mit Abschluss 12. Klasse',
                                                'Fachhochschul- oder Universitätsabschluss (z.B. Bachelor, Master, Diplom, Staatsexamen)',
                                                'Promotion, Habilitation']),
                           state_now = random.choice(['Baden-Württemberg','Bayern', 'Berlin', 'Brandenburg', 'Bremen',
                                                      'Hamburg', 'Hessen', 'Mecklenburg-Vorpommern', 'Niedersachsen',
                                                      'Nordrhein-Westfalen', 'Rheinland-Pfalz', 'Saarland', 'Sachsen',
                                                      'Sachsen-Anhalt', 'Schleswig-Holstein', 'Thüringen']),
                           born_de = "Ja"),
            if self.player.born_de == "Ja":
                yield P6, dict(pol_int = random.choice(['Überhaupt nicht interessiert', 'Eher nicht interessiert', 'Eher interessiert', 'Sehr interessiert', '']))
                yield P7, dict(pollr = random.randint(0,10))
                yield P8, dict(partyid = random.choice(['AfD', 'CDU', 'CSU', 'FDP', 'SPD', 'Bündnis 90/Die Grünen', 'Die Linke', 'andere', 'keine', '']),
                           partyid_oth = random.choice(['Piraten', 'Tierschutzupartei', '']))
                yield P9, dict(poltrust_gov = random.randint(1,7),
                        poltrust_pol = random.randint(1,7),
                        poltrust_med = random.randint(1,7))
                if self.player.participant.prime == 1:
                    yield P10, dict(prime1=random.choice(['Stimme überhaupt nicht zu', 'Stimme eher nicht zu', 'Stimme eher zu', 'Stimme voll und ganz zu']))
                    yield P11, dict(prime2=random.choice(['Stimme überhaupt nicht zu', 'Stimme eher nicht zu', 'Stimme eher zu', 'Stimme voll und ganz zu']))
            else:
                yield SorryFull2