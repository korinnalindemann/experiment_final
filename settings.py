from os import environ

SESSION_CONFIGS = [
     dict(
         name='cap_betteropp',
         app_sequence=['screening',
                       'real_effort',
                       'vote_rules',
                       'postgame_survey'

],
         num_demo_participants= 10,
         display_name= 'Study',
         use_browser_bots=False,

     ),

#    dict(
#        name = 'cap_worseopp',
#        app_sequence=['postgame_survey'
#                      ],
#        num_demo_participants = 4,
#        display_name = 'Capitalism - Worse Opponents',
#    ),#

#     dict(
#         name='red_betteropp',
#         app_sequence=[#'screening',
#                       'vote_rules',
#                       #'real_effort'
#],
#         num_demo_participants= 10,
#         display_name= 'Redistribution - Better Opponents',######

 #    ),
#
#    dict(
#        name = 'red_worseopp',
#        app_sequence=['screening'
#                      ],
#        num_demo_participants = 10,
#        display_name = 'Redistribution - Worse Opponents',#
#
#    ),

]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

ROOMS = [
    dict(
        name='umfrage_s2',
        display_name='Session_BilendiRespondi',
     #   participant_label_file='_rooms/econ101.txt',
      #  use_secure_urls=True
    ),
]
SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

PARTICIPANT_FIELDS = ['is_dropout', 'treat','prime','redistribution','better_opp','diff_player_opp', 'num_redi', 'num_capi',
                      'state_now', 'gender', 'age']
SESSION_FIELDS = ['params', 'num_participants_finished_east','num_participants_finished_west',
                  'num_finished_female', 'num_finished_male', 'num_finished_divers',
                  'num_finished_age1829', 'num_finished_age3039', 'num_finished_age4049', 'num_finished_age5059',
                  'num_finished_age6069',  'num_fin',
                  'num_participants_red', 'num_participants_cap']

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'de'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'EUR'
USE_POINTS = True

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '6593783526314'



# generating session configs for all varieties of features
#import sys


#if sys.argv[1] == 'test':
#    MAX_ITERATIONS = 5
#    FREEZE_TIME = 0.1
#    TRIAL_PAUSE = 0.2
#    TRIAL_TIMEOUT = 0.3

 #   SESSION_CONFIGS = [
    #    dict(
    #        name=f"testing_sliders",
    #        num_demo_participants=1,
    #        app_sequence=['sliders'],
    #        trial_delay=TRIAL_PAUSE,
    #        retry_delay=FREEZE_TIME,
    #        num_sliders=3,
    #        attempts_per_slider=3,
    #   ),
  #      ]
#for task in ['decoding', 'matrix', 'transcription']:
#    SESSION_CONFIGS.extend(
#        [
#            dict(
#                name=f"testing_{task}_defaults",
#                num_demo_participants=1,
#                app_sequence=['real_effort'],
#            #    puzzle_delay=TRIAL_PAUSE,
            #    retry_delay=FREEZE_TIME,
#                ),
#            dict(
#                name=f"testing_{task}_retrying",
#                num_demo_participants=1,
#                app_sequence=['real_effort'],
            #   puzzle_delay=TRIAL_PAUSE,
            #    retry_delay=FREEZE_TIME,
#                attempts_per_puzzle=5,
#                ),
#            dict(
#                name=f"testing_{task}_limited",
#                num_demo_participants=1,
#                app_sequence=['real_effort'],
            #    puzzle_delay=TRIAL_PAUSE,
            #    retry_delay=FREEZE_TIME,
             #   max_iterations=MAX_ITERATIONS,
#                ),
#            ]
#        )
