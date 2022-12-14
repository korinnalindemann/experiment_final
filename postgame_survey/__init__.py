from otree.api import *


doc = """
Post Game Survey
"""


class Constants(BaseConstants):
    name_in_url = 'postgame_survey'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass

def creating_session(subsession):
    pass


class Group(BaseGroup):
    pass

### FUNCTIONS
def make_field_11(label):
    return models.IntegerField(
        blank = True,
        choices=[0,1,2,3,4,5,6,7,8,9,10],
        label=label,
        widget=widgets.RadioSelectHorizontal,
    )
def make_field_radio(choices, label):
    return models.StringField(
        blank = True,
        choices=choices,
        label=label,
        widget=widgets.RadioSelect,
    )

def gen_seed2(player):
    import random
    player.seed_cust2 = random.randrange(1,1000)
    print(player.seed_cust2)
    return player.seed_cust2



### LIST

fed_states = ['Baden-Württemberg','Bayern', 'Berlin', 'Brandenburg', 'Bremen',
              'Hamburg', 'Hessen', 'Mecklenburg-Vorpommern', 'Niedersachsen',
              'Nordrhein-Westfalen', 'Rheinland-Pfalz', 'Saarland', 'Sachsen',
              'Sachsen-Anhalt', 'Schleswig-Holstein', 'Thüringen']


class Player(BasePlayer):
    num_fin = models.IntegerField(initial=0)
    num_participants_finished_east = models.IntegerField(initial=0)
    num_participants_finished_west = models.IntegerField(initial=0)
    num_finished_male = models.IntegerField(initial=0)
    num_finished_female = models.IntegerField(initial=0)
    num_finished_age1829 = models.IntegerField(initial=0)
    num_finished_age3039 = models.IntegerField(initial=0)
    num_finished_age4049 = models.IntegerField(initial=0)
    num_finished_age5059 = models.IntegerField(initial=0)
    num_finished_age6069 = models.IntegerField(initial=0)
    redpref = make_field_11(label = 'Wenn Sie die Regeln zu den Punkten innerhalb Ihrer Gruppe von Beginn an selbst bestimmen hätten können,'
                                  ' wie stark wären Sie für oder gegen eine gleichmäßige Umverteilung der Punkte zwischen den Gruppenmitgliedern'
                                  ' gewesen (0 = keine Punkteumverteilung, 10 = vollständige Punkteumverteilung)? ')

    redpref_state = make_field_11('Der Staat sollte Maßnahmen ergreifen, um Einkommensunterschiede zu vermindern.')
    redpref_tax = make_field_11('Steuern sollten erhöht werden, um Einkommensunterschiede zu vermindern.')
    man_check = make_field_11('Wie fair fanden Sie die Spiele (0 = gar nicht fair, '
                                  '10 = sehr fair)?')
    man_check2 = make_field_11('Wie vorteilhaft empfinden Sie Systeme mit hoher Umverteilung (0 = gar nicht vorteilhaft, '
                               '10 = sehr vorteilhaft)?')
    attcheck1 = models.StringField(
        blank = True,
        label = 'Wurden in Ihrer Gruppe die Punkte in den <b>ersten drei Spielen</b> zwischen Ihnen und Ihren Gegenspielern umverteilt?',
        choices = ['Ja', 'Nein', 'Weiß nicht'],
        widget = widgets.RadioSelect
    )
    attcheck2 = models.StringField(
        blank = True,
        label = 'Wie haben Ihre Gegenspieler in den <b>ersten drei Spielen</b> insgesamt abgeschlossen?',
        widget = widgets.RadioSelect
    )

    attcheck3 = models.StringField(
        blank = True,
        label = 'Wurden Sie früher in der Befragung nach Ihrer Zustimmung von Aussagen bezüglich der DDR befragt?',
        choices=['Ja', 'Nein', 'Weiß nicht'],
        widget = widgets.RadioSelect
    )

    state_edu = models.StringField(
        blank = True,
        label = 'In welchem Bundesland haben Sie Ihre obligatorische Schulbildung abgeschlossen?',
        choices = fed_states
    )

    edu = models.StringField(
        blank = True,
        label='Was ist Ihr höchster Bildungsabschluss, den Sie erhalten haben?',
        choices=['Kein oder noch kein Schulabschluss',
                 'Hauptschulabschluss, Volksschulabschluss',
                 'Mittlere Reife, Realabschluss, Polytechnische Oberschule mit Abschluss 10. Klasse',
                 'Fachhochschulabschluss, Abitur, erweiterte Oberschule mit Abschluss 12. Klasse',
                 'Fachhochschul- oder Universitätsabschluss (z.B. Bachelor, Master, Diplom, Staatsexamen)',
                 'Promotion, Habilitation'],
        widget=widgets.RadioSelect
    )

    occupation = models.StringField(
        blank = True,
        label = 'Was ist Ihr aktueller Beschäftigungsstatus?',
        choices = ['Vollzeit beschäftigt', 'Teilzeit beschäftigt', 'Selbständig', 'Nicht berufstätig (Hausfrau/Hausmann)',
                   'In schulischer oder universitärer Ausbildung', 'Lehrling/Azubi', 'Momentan arbeitslos', 'Rente/pensioniert',
                   'In Mutterschutz/Elternzeit', 'Anderes'],
        widget = widgets.RadioSelect
    )
    soc_statfam = make_field_radio(
        label = 'Wie würden Sie den sozialen Status (z.B. bezüglich Einkommen) Ihrer Familie einschätzen, während Sie aufgewachsen sind?',
        choices = ['Unterschicht',
                   'Untere Mittelschicht',
                   'Mittelschicht',
                   'Obere Mittelschicht',
                   'Oberschicht'],

    )
    ruralurban = make_field_radio(
        label = 'Leben Sie eher städtisch oder eher ländlich? Wenn Sie sich nicht sicher sind, geben Sie bitte eine Schätzung ab.',
        choices = ['Eher ländlich',  'Etwas zwischen ländlich und städtisch', 'Eher städtisch'],

    )

    ethnic_min = make_field_radio(
        label='Identifizieren Sie sich in Deutschland mit einer ethnischen Minderheit?',
        choices= ['Ja', 'Nein', 'Weiß nicht'],
    )
    income = models.IntegerField(
        blank = True,
        label = 'Wie hoch ist Ihr monatliches Haushaltseinkommen nach Abzügen (Netto-Einkommen)?'
                                         ' Falls Sie sich nicht sicher sind, geben Sie bitte eine Schätzung an.',
        choices=[
            [1, 'bis 1100 €'],
            [2, 'über 1100 bis 1500 €'],
            [3, 'über 1500 bis 1840 €'],
            [4, 'über 1840 bis 2200 €'],
            [5, 'über 2200 bis 2600 €'],
            [6, 'über 2600 bis 3040 €'],
            [7, 'über 3040 bis 3560 €'],
            [8, 'über 3560 bis 4250 €'],
            [9, 'über 4250 bis 5390 €'],
            [10, 'mehr als 5390 €']
        ],
        widget = widgets.RadioSelect
    )
    comment = models.LongStringField(blank=True,
                                     label= "Möchten Sie uns zum Schluss noch etwas mitteilen?")
    seed_cust2 = models.IntegerField(initial = 0)
    consent2 = models.BooleanField(label = '',
                                   choices = [[1, 'Ja'], [0,'Nein']])


def attcheck2_choices(player):
    choices = ['Beide haben weniger Punkte als ich erzielt',
               'Jemand hat mehr und jemand hat weniger Punkte als ich erzielt',
               'Beide haben mehr Punkte als ich erzielt',
               'Weiß nicht'
              ]
    return choices


ex_ddr = ['Mecklenburg-Vorpommern', 'Brandenburg', 'Sachsen-Anhalt', 'Sachsen', 'Thüringen']


def quota_full(player):
    participant = player.participant
    session = player.session
    if participant.state_now in ex_ddr:
        session.num_participants_finished_east += 1
        session.num_fin += 1
        print('Nr tot', session.num_fin)
        print('Nr. East', session.num_participants_finished_east)
    else:
        session.num_participants_finished_west += 1
        session.num_fin += 1
        print('Nr tot', session.num_fin)
        print('Nr. West', session.num_participants_finished_west)

    if participant.gender == "Weiblich":
        session.num_finished_female += 1
        print('Nr. Female', session.num_finished_female)

    elif participant.gender == "Männlich":
        session.num_finished_male += 1
        print('Nr. Male', session.num_finished_male)

    else:
        session.num_finished_divers += 1
        print('Nr. Divers', session.num_finished_divers)

    if participant.age in list(range(18, 30)):
        session.num_finished_age1829 += 1
        print('Nr. Age 18-29', session.num_finished_age1829)
    elif participant.age in list(range(30, 40)):
        session.num_finished_age3039 += 1
        print('Nr. Age 30-39', session.num_finished_age3039)
    elif participant.age in list(range(40, 50)):
        session.num_finished_age4049 += 1
        print('Nr. Age 40-49', session.num_finished_age4049)
    elif participant.age in list(range(50, 60)):
        session.num_finished_age5059 += 1
        print('Nr.Age 50-59', session.num_finished_age5059)
    elif participant.age in list(range(60, 70)):
        session.num_finished_age6069 += 1
        print('Nr. Age 60-69', session.num_finished_age6069)

    player.num_participants_finished_east = session.num_participants_finished_east
    player.num_participants_finished_west = session.num_participants_finished_west
    player.num_fin = session.num_fin
    player.num_finished_male = session.num_finished_male
    player.num_finished_female = session.num_finished_female
    player.num_finished_age1829 = session.num_finished_age1829
    player.num_finished_age3039 = session.num_finished_age3039
    player.num_finished_age4049 = session.num_finished_age4049
    player.num_finished_age5059 = session.num_finished_age5059
    player.num_finished_age6069 = session.num_finished_age6069





# PAGES
class PS2 (Page):
    form_model = 'player'
    form_fields = ['redpref']

    @staticmethod
    def before_next_page(player, timeout_happened):
        gen_seed2(player)


class PS3(Page):
    form_model = 'player'
    # randomise field order
    def get_form_fields(player):
        import random
        fields = ['redpref_state',
                  'redpref_tax']
        random.seed(player.seed_cust2)
        random.shuffle(fields)
        return fields

class PS4(Page):
    form_model = 'player'
    form_fields = ['man_check',
                   'man_check2']

class PS5(Page):
    form_model = 'player'
    form_fields = ['attcheck1',
                   'attcheck2',
                   'attcheck3']


class PS12(Page):
    form_model = 'player'
    form_fields = ['state_edu']

class PS13(Page):
    form_model = 'player'
    form_fields = ['edu']



class PS14(Page):
    form_model = 'player'
    form_fields = ['occupation']

class PS15(Page):
    form_model = 'player'
    form_fields = ['soc_statfam']

class PS16(Page):
    form_model = 'player'
    form_fields = ['ruralurban']

class PS17(Page):
    form_model = 'player'
    form_fields = ['ethnic_min']

class PS18(Page):
    form_model = 'player'
    form_fields = ['income',
                   'comment']

class Thanks(Page):
    form_model = 'player'
    form_fields = ['consent2']

    @staticmethod
    def before_next_page(player,timeout_happened):
        quota_full(player)

class Redirect(Page):
    form_model = 'player'

page_sequence = [PS2,PS3,PS4,PS5,PS12,PS13,PS14,PS15,PS16,PS17,PS18,Thanks,Redirect]
