from otree.api import *


doc = """
Pre-Game Survey
"""


class Constants(BaseConstants):
    name_in_url = 'screening'
    players_per_group = None
    num_rounds = 1
    treatments = ['prime_red_bettopp', 'prime_red_worseopp', 'prime_cap_bettopp', 'prime_cap_worseopp',
                                           'noprime_red_bettopp', 'noprime_red_worseopp', 'noprime_cap_bettopp', 'noprime_cap_worseopp']

def creating_session(subsession):
    session = subsession.session
    session.num_fin = 0
    session.num_participants_finished_east = 0
    session.num_participants_finished_west = 0
    session.num_gender_fem = 0
    session.num_gender_male = 0
    session.num_yob_1 = 0
    session.num_yob_2 = 0
    session.num_participants_red = 0
    session.num_participants_cap = 0

    ps = subsession.get_players()
    if subsession.round_number == 1:
        # If the app has more than one round and treatments are constant across rounds,
        # assign treatments only in the first round
        if subsession.round_number == 1:
            # Import modules needed
            from itertools import cycle
            from random import shuffle

            # In-place random permutation of the list of players
            shuffle(ps)
            treatments = cycle(Constants.treatments)

            # Loop through all the shuffled participants
            for p in ps:
                # Select the next treatment (starting from the previous one) stored in treatments
                t = next(treatments)
                # Assign it to the player field "treatment"
                p.treatment = t
                # If the treatment has to be referenced also in other rounds and/or apps,
                # then store it in the dictionary of the "participant" called "vars" (this is in-built in oTree).
                # "vars" is a dictionary, so we use the normal syntax used to update dictionaries
                p.participant.vars['treat'] = t

                # Store the same treatment to the player field "treatment" in the subsequent rounds.
        else:
            for p in ps:
                p.treatment = p.participant.vars['treatment']

        print('Treatment is:', p.treatment )



    for player in subsession.get_players():
        participant = player.participant
        # redistribution
        if participant.treat == 'prime_red_bettopp' or participant.treat == 'prime_red_worseopp' or participant.treat == 'noprime_red_bettopp' or participant.treat == 'noprime_red_worseopp':
            participant.redistribution = True
        else:
            participant.redistribution = False
        print('1. Participant has red.', participant.redistribution)

        # prime
        if participant.treat == 'prime_red_bettopp' or participant.treat == 'prime_red_worseopp' or participant.treat == 'prime_cap_bettopp' or participant.treat == 'prime_cap_worseopp':
            participant.prime = True
        else:
            participant.prime = False
        print('2. Participant has prime', participant.prime)

        # better opponents
        if participant.treat == 'prime_red_bettopp' or participant.treat == 'noprime_red_bettopp' or participant.treat == 'prime_cap_bettopp' or participant.treat == 'noprime_cap_bettopp':
            participant.better_opp = True
        else:
            participant.better_opp = False
        print('3. Participant has better opponents', participant.better_opp)


        player.treatment = participant.treat
        player.redistribution = participant.redistribution
        print('red.', player.redistribution, participant.redistribution)
        player.prime = participant.prime
        print('prime', player.prime, participant.prime)
        player.bett_opp = participant.better_opp
        print('bett opp.', player.bett_opp, participant.better_opp)

        if participant.redistribution is True:
            session.num_participants_red += 1
            participant.num_capi = 0
            participant.num_redi = 0
            participant.num_redi = session.num_participants_red
            player.num_red = session.num_participants_red # only for me now to control
            print('Num red.:', participant.num_redi, player.num_red)

        if participant.redistribution is False:
            session.num_participants_cap += 1
            participant.num_capi = 0
            participant.num_redi = 0
            participant.num_capi = session.num_participants_cap
            player.num_cap = session.num_participants_cap # only for me now to control
            print('Num cap.:', participant.num_capi, player.num_cap)


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
   pass

### LIST

fed_states = ['Baden-Württemberg','Bayern', 'Berlin', 'Brandenburg', 'Bremen',
              'Hamburg', 'Hessen', 'Mecklenburg-Vorpommern', 'Niedersachsen',
              'Nordrhein-Westfalen', 'Rheinland-Pfalz', 'Saarland', 'Sachsen',
              'Sachsen-Anhalt', 'Schleswig-Holstein', 'Thüringen']

ex_ddr = ['Mecklenburg-Vorpommern', 'Brandenburg', 'Sachsen-Anhalt', 'Sachsen', 'Thüringen']

## functions
def make_field_7(label):
    return models.IntegerField(
        blank = True,
        choices=[1,2,3,4,5,6,7],
        label=label,
        widget=widgets.RadioSelectHorizontal,
    )

def gen_seed(player):
    import random
    player.seed_cust = random.randrange(1,1000)
    print(player.seed_cust)
    return player.seed_cust

class Player(BasePlayer):
    treatment = models.StringField(initial = " ")
    prime = models.BooleanField(choices=[[1,True], [0, False]])
    redistribution = models.BooleanField(choices=[[1,True], [0,False]])
    bett_opp = models.BooleanField(choices=[[1,True], [0,False]])
    num_red = models.IntegerField(initial = 0)
    num_cap = models.IntegerField(initial=0)
    consent = models.BooleanField(
        label=' ',
        choices=[[1,'Ja'], [0,'Nein']]
    )
    gender = models.StringField(
       # blank = True,
        label = 'Was ist Ihr Geschlecht?',
        choices = ['Weiblich', 'Männlich', 'Divers'],
        widget = widgets.RadioSelect
    )
    yob = models.IntegerField(
     #   blank = True,
        label = 'In welchem Jahr sind Sie geboren?',
    )
    edu = models.StringField(
    #    blank = True,
        label = 'Was ist Ihr höchster Bildungsabschluss, den Sie erhalten haben?',
        choices = ['Kein oder noch kein Schulabschluss',
                   'Hochschulabschluss, Volksschulabschluss',
                   'Mittlere Reife, Realabschluss, Polytechnische Oberschule mit Abschluss 10. Klasse',
                   'Fachhochschulabschluss, Abitur, erweiterte Oberschule mit Abschluss 12. Klasse',
                   'Fachhochschul- oder Universitätsabschluss (z.B. Bachelor, Master, Diplom, Staatsexamen)',
                   'Promotion, Habilitation'],
        widget = widgets.RadioSelect
    )

    born_de = models.StringField(
        label = 'Sind Sie in Deutschland geboren?',
        choices = ['Ja', 'Nein'],
        widget =  widgets.RadioSelect
    )
    born_de_par = models.StringField(
        label = 'Sind beide Ihrer Eltern in Deutschland geboren?',
        choices = ['Ja', 'Nein'],
        widget =  widgets.RadioSelect
    )



    pol_int = models.StringField(
        label='Wie interessiert sind Sie im Allgemeinen an Politik?',
        choices=['Überhaupt nicht interessiert', 'Eher nicht interessiert', 'Eher interessiert', 'Sehr interessiert'],
        widget=widgets.RadioSelect,
        blank = True
    )

    pollr = models.IntegerField(
        blank = True,
        label='In der Politik spricht man manchmal von "links" und "rechts". Wo würden Sie sich selbst auf der untenstehenden Skala einordnen (0 = links, 10 = rechts)?',
        widget = widgets.RadioSelectHorizontal,
    )

    partyid = models.StringField(
        blank = True,
        label='In Deutschland neigen viele Leute längere Zeit einer bestimmten politischen Partei zu, obwohl sie auch ab und zu eine andere Partei wählen. Wie ist das bei Ihnen: Neigen Sie - ganz allgemein gesprochen – einer bestimmten Partei zu? Und wenn ja, welcher?',
        widget = widgets.RadioSelect,
    )

    partyid_oth = models.StringField(blank=True,
        label='Falls Sie "andere" ausgewählt haben, spezifizieren Sie bitte welche Partei.'
    )
    poltrust_gov = make_field_7(label = 'Regierung')
    poltrust_pol = make_field_7(label = 'Polizei')
    poltrust_med = make_field_7(label = 'Medien')
    seed_cust = models.IntegerField(initial = 0)
    prime1 = models.StringField(
        blank = True,
        label = 'Beruflicher, aber auch privater, Selbstverwirklichung wurde in der DDR Steine in den Weg gelegt.',
        widget=widgets.RadioSelect,
        choices=['Stimme überhaupt nicht zu', 'Stimme eher nicht zu', 'Stimme eher zu', 'Stimme voll und ganz zu']
    )
    prime2 = models.StringField(
        blank = True,
        label = 'Berufliche Perspektiven waren im sozialistischen Deutschland beschränkt. Zum Beispiel, auch wenn man sich im Beruf stark anstrengte und engagierte,'
                ' wurde man meistens nicht besser entlohnt als diejenigen, die die Extra-Meile nicht gegangen sind.',
     #   label = 'Vor der Wende hatten Menschen im Osten Deutschlands weniger persönliche und berufliche Zukunftsaussichten als diejenigen im Westen.',
        widget = widgets.RadioSelect,
        choices=['Stimme überhaupt nicht zu', 'Stimme eher nicht zu', 'Stimme eher zu',
                'Stimme voll und ganz zu']
    )
    state_now = models.StringField(
     #   blank = True,
        label = 'In welchem Bundesland leben Sie?',
        choices = fed_states
    )

def yob_choices(player):
    choices = list(range(2004, 1939,-1))
    return choices

def pollr_choices(player):
    choices = list(range(0,11,1))
    return choices

def partyid_choices(player):
    import random
    random.seed(player.seed_cust)
    choices = ['AfD', 'CDU', 'CSU', 'FDP', 'SPD', 'Bündnis 90/Die Grünen', 'Die Linke']
    random.shuffle(choices)
    choices.extend(['andere', 'keine'])
    return choices



def par_vars(player):
    participant = player.participant
    participant.state_now = player.state_now
    print(player.session.num_fin)




# PAGES

class Welcome(Page):
    pass

class Einwilligung(Page):
    form_model = 'player'
    form_fields = ['consent']

class SorryFull(Page):
    def is_displayed(player: Player):
        return player.consent == 0




class P1(Page):
    form_model = 'player'
    form_fields = ['gender',
                   'yob',
                   'edu',
                   'born_de',
                   'born_de_par',
                   'state_now']



    @staticmethod
    def before_next_page(player, timeout_happened):
        gen_seed(player)
        par_vars(player)


class SorryFull2(Page):

    def is_displayed(player: Player):
        return player.born_de == 'Nein' or player.born_de_par == 'Nein'

class P6(Page):
    form_model = 'player'
    form_fields = ['pol_int']

class P7(Page):
    form_model = 'player'
    form_fields = ['pollr']

class P8(Page):
    form_model = 'player'
    form_fields = ['partyid',
                   'partyid_oth']

class P9(Page):
    form_model = 'player'

    # randomise field order
    def get_form_fields(player):
        import random
        random.seed(player.seed_cust)
        fields = ['poltrust_gov',
                   'poltrust_pol',
                   'poltrust_med']
        random.shuffle(fields)
        return fields


class P10(Page): # Prime
    form_model = 'player'
    form_fields = ['prime1']

    @staticmethod
    def is_displayed(player: Player):
        return player.participant.prime is True

class P11(Page): # Prime
    form_model = 'player'
    form_fields = ['prime2']

    @staticmethod
    def is_displayed(player: Player):
        return player.participant.prime is True





page_sequence = [Welcome, Einwilligung,SorryFull,P1,SorryFull2,P6,P7,P8,P9,P10,P11]

