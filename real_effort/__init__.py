import time

from otree import settings
from otree.api import *
from otree.models import player

from .image_utils import encode_image

doc = """
Real-effort tasks. The different tasks are available in task_matrix.py, task_transcription.py, etc.
You can delete the ones you don't need. 
"""


def get_task_module(player):
    """
    This function is only needed for demo mode, to demonstrate all the different versions.
    You can simplify it if you want.
    """
    from . import task_matrix, task_transcription, task_decoding

    session = player.session
    # task = session.config.get("task")
    if player.round_number == 1:
        return task_transcription
    if player.round_number == 2:
        return task_matrix
    if player.round_number == 3:
        return task_decoding

    # default
    # return task_matrix


class Constants(BaseConstants):
    name_in_url = "transcription"
    players_per_group = None
    num_rounds = 3

    instructions_template = __name__ + "/instructions_old.html"
    captcha_length = 3


class Subsession(BaseSubsession):
    pass


def creating_session(subsession: Subsession):
    session = subsession.session
    defaults = dict(
        retry_delay=1.0, puzzle_delay=1.0, attempts_per_puzzle=1, max_iterations=None
    )
    session.params = {}
    for param in defaults:
        session.params[param] = session.config.get(param, defaults[param])



class Group(BaseGroup):
    pass


class Player(BasePlayer):
    iteration = models.IntegerField(initial=0)
    num_trials = models.IntegerField(initial=0)
    num_correct = models.IntegerField(initial=0)
    num_failed = models.IntegerField(initial=0)
    score_task = models.IntegerField(initial=0)
    score_total = models.IntegerField(initial=0)
    score_task_opp1 = models.IntegerField(initial=0)
    score_task_opp2 = models.IntegerField(initial=0)
    tot_rscore_opp1 = models.IntegerField(initial=0)
    tot_rscore_opp2 = models.IntegerField(initial=0)
    sum_group = models.IntegerField(initial=0)
    sum_group_third = models.FloatField(initial=0)
    seed_cust = models.IntegerField
    red_amount = models.FloatField(initial=0)
    red_amount_opp1 = models.FloatField(initial=0)
    red_amount_opp2 = models.FloatField(initial=0)
    red_amount_tot = models.FloatField(initial=0)
    red_amount_tot_opp1 = models.FloatField(initial=0)
    red_amount_tot_opp2 = models.FloatField(initial=0)
    sum_group_third_tod= models.FloatField(initial=0)
    diff_red = models.FloatField(initial =0)



# puzzle-specific stuff


class Puzzle(ExtraModel):
    """A model to keep record of all generated puzzles"""
    player = models.Link(Player)
    iteration = models.IntegerField(initial=0)
    attempts = models.IntegerField(initial=0)
    timestamp = models.FloatField(initial=0)
    # can be either simple text, or a json-encoded definition of the puzzle, etc.
    text = models.LongStringField()
    # solution may be the same as text, if it's simply a transcription task
    solution = models.LongStringField()
    response = models.LongStringField()
    response_timestamp = models.FloatField()
    is_correct = models.BooleanField()


def generate_puzzle(player: Player) -> Puzzle:
    """Create new puzzle for a player"""
    task_module = get_task_module(player)
    fields = task_module.generate_puzzle_fields()
    player.iteration += 1
    return Puzzle.create(
        player=player, iteration=player.iteration, timestamp=time.time(), **fields
    )


def get_current_puzzle(player):
    puzzles = Puzzle.filter(player=player, iteration=player.iteration)
    if puzzles:
        [puzzle] = puzzles
        return puzzle


def encode_puzzle(puzzle: Puzzle):
    """Create data describing puzzle to send to client"""
    task_module = get_task_module(puzzle.player)  # noqa
    # generate image for the puzzle
    image = task_module.render_image(puzzle)
    data = encode_image(image)
    return dict(image=data)


def get_progress(player: Player):
    """Return current player progress"""
    return dict(
        num_trials=player.num_trials,
        num_correct=player.num_correct,
        num_incorrect=player.num_failed,
        iteration=player.iteration,
    )


def play_game(player: Player, message: dict):
    """Main game workflow
    Implemented as reactive scheme: receive message from vrowser, react, respond.

    Generic game workflow, from server point of view:
    - receive: {'type': 'load'} -- empty message means page loaded
    - check if it's game start or page refresh midgame
    - respond: {'type': 'status', 'progress': ...}
    - respond: {'type': 'status', 'progress': ..., 'puzzle': data} -- in case of midgame page reload

    - receive: {'type': 'next'} -- request for a next/first puzzle
    - generate new puzzle
    - respond: {'type': 'puzzle', 'puzzle': data}

    - receive: {'type': 'answer', 'answer': ...} -- user answered the puzzle
    - check if the answer is correct
    - respond: {'type': 'feedback', 'is_correct': true|false, 'retries_left': ...} -- feedback to the answer

    If allowed by config `attempts_pre_puzzle`, client can send more 'answer' messages
    When done solving, client should explicitely request next puzzle by sending 'next' message

    Field 'progress' is added to all server responses to indicate it on page.

    To indicate max_iteration exhausted in response to 'next' server returns 'status' message with iterations_left=0
    """
    session = player.session
    my_id = player.id_in_group
    params = session.params
    task_module = get_task_module(player)

    now = time.time()
    # the current puzzle or none
    current = get_current_puzzle(player)

    message_type = message['type']

    # page loaded
    if message_type == 'load':
        p = get_progress(player)
        if current:
            return {
                my_id: dict(type='status', progress=p, puzzle=encode_puzzle(current))
            }
        else:
            return {my_id: dict(type='status', progress=p)}

    if message_type == "cheat" and settings.DEBUG:
        return {my_id: dict(type='solution', solution=current.solution)}

    # client requested new puzzle
    if message_type == "next":
        if current is not None:
            if current.response is None:
                raise RuntimeError("trying to skip over unsolved puzzle")
            if now < current.timestamp + params["puzzle_delay"]:
                raise RuntimeError("retrying too fast")
            if current.iteration == params['max_iterations']:
                return {
                    my_id: dict(
                        type='status', progress=get_progress(player), iterations_left=0
                    )
                }
        # generate new puzzle
        z = generate_puzzle(player)
        p = get_progress(player)
        return {my_id: dict(type='puzzle', puzzle=encode_puzzle(z), progress=p)}

    # client gives an answer to current puzzle
    if message_type == "answer":
        if current is None:
            raise RuntimeError("trying to answer no puzzle")

        if current.response is not None:  # it's a retry
            if current.attempts >= params["attempts_per_puzzle"]:
                raise RuntimeError("no more attempts allowed")
            if now < current.response_timestamp + params["retry_delay"]:
                raise RuntimeError("retrying too fast")

            # undo last updation of player progress
            player.num_trials -= 1
            if current.is_correct:
                player.num_correct -= 1
            else:
                player.num_failed -= 1

        # check answer
        answer = message["answer"]

        if answer == "" or answer is None:
            raise ValueError("bogus answer")

        current.response = answer
        current.is_correct = task_module.is_correct(answer, current)
        current.response_timestamp = now
        current.attempts += 1

        # update player progress
        if current.is_correct:
            player.num_correct += 1
        else:
            player.num_failed += 1
        player.num_trials += 1

        retries_left = params["attempts_per_puzzle"] - current.attempts
        p = get_progress(player)
        return {
            my_id: dict(
                type='feedback',
                is_correct=current.is_correct,
                retries_left=retries_left,
                progress=p,
            )
        }

    raise RuntimeError("unrecognized message from client")

# generate random seed
def gen_seed(player):
    import random
    p = player
    p.seed_cust = random.randrange(1,1000)
    print(p.seed_cust)
    return p.seed_cust

# score calculation of results #######
def get_score(player: Player):
    participant = player.participant
    p = player
    ## generate opponent values (different seeds per subsession so not always the same numbers)
    import random
    if p.round_number == 1:
        random.seed(p.seed_cust)
    elif p.round_number == 2:
        random.seed(p.seed_cust)
    else:
        random.seed(p.seed_cust)
    p.score_task = p.num_correct - p.num_failed
    print(p.score_task)
    from math import ceil
    if (p.score_task >= 0 and p.score_task <= 1) or (p.score_task <=0 and p.score_task >= -1):
        number_list = [1, 2]
    if (p.score_task > 1 and p.score_task <= 7) or (p.score_task < -1 and p.score_task >= -7):
        number_list = [0.5, 0.6, 0.7, 0.8, 0.9]

    if (p.score_task > 7 and p.score_task <=9) or (p.score_task < -7 and p.score_task >= -9):
        number_list = [0.5, 0.6, 0.7]

    if (p.score_task > 9 and p.score_task <=14) or (p.score_task < -9 and p.score_task >= -14):
        number_list = [0.4, 0.5]

    if (p.score_task > 14 or p.score_task < -14):
        number_list = [0.3, 0.4]

    if participant.better_opp == 1:
        if p.score_task > 0:
            p.score_task_opp1 = ceil(p.score_task + (p.score_task* (random.choice(number_list))))
            p.score_task_opp2 = ceil(p.score_task + (p.score_task* (random.choice(number_list))))

        elif p.score_task < 0:
            p.score_task_opp1 = ceil(p.score_task + (-p.score_task * (random.choice(number_list))))
            p.score_task_opp2 = ceil(p.score_task + (-p.score_task * (random.choice(number_list))))

        elif p.score_task == 0:
            p.score_task_opp1 = ceil(p.score_task + random.choice(number_list))
            p.score_task_opp2 = ceil(p.score_task + random.choice(number_list))

    elif participant.better_opp == 0:
        if p.score_task > 0:
            p.score_task_opp1 = ceil(p.score_task - (p.score_task * (random.choice(number_list))))
            p.score_task_opp2 = ceil(p.score_task - (p.score_task * (random.choice(number_list))))

        elif p.score_task < 0:
            p.score_task_opp1 = ceil(p.score_task - (-p.score_task * (random.choice(number_list))))
            p.score_task_opp2 = ceil(p.score_task - (-p.score_task * (random.choice(number_list))))

        elif p.score_task == 0:
            p.score_task_opp1 = ceil(p.score_task - random.choice(number_list))
            p.score_task_opp2 = ceil(p.score_task - random.choice(number_list))


    p.sum_group = p.score_task + p.score_task_opp1 + p.score_task_opp2
    p.sum_group_third = round((p.sum_group / 3),1)




 #   if p.score_task < 0:
 #       if participant.better_opp == 1:
 #           p.sum_group = int((p.score_task + (p.score_task * (-participant.diff_player_opp)))*3)
 #       else:
 #           p.sum_group = int((p.score_task - (p.score_task * (-participant.diff_player_opp)))*3)





 #   if p.score_task == 0:
 #       if participant.better_opp == 1:
 #           p.sum_group = int(participant.diff_player_opp*10)
 #       else:
 #           p.sum_group = (int(participant.diff_player_opp*10)*(-1))
 #   print(p.sum_group)

#    p.max_opp1 = int(p.sum_group - (3 * p.score_task))
#    print('Maximum for opp. bett is', p.max_opp1)
    # ranges min-max for better opp:
#    p.max_opp1_bet = p.score_task + p.max_opp1 - 1
#    p.min_opp1_bet = p.score_task + 1

    # ranges min-max for worse opp:
#    p.max_opp1_worse = p.score_task - 1
#    p.min_opp1_worse = p.score_task + p.max_opp1 + 1
#    print('Minimum for opp. worse is', p.min_opp1_worse)

 #   ## generate opponent values (different seeds per subsession so not always the same numbers)
 #   import random
 #   if p.round_number == 1:
#        random.seed(10)
 #   elif p.round_number == 2:
 #       random.seed(11)
 #   else:
 #       random.seed(12)
  #  if participant.better_opp == 1:
        # maximum is a function that the max is the difference between the group sum and 3 * the players score - 1,
        # so that group member 1 and group member 2 are both better than the player
  #      if p.max_opp1_bet > p.min_opp1_bet:
  #          p.score_task_opp1 = random.randint(p.min_opp1_bet, p.max_opp1_bet)
#        else:
#            p.score_task_opp1 = random.randint(p.score_task + 1, p.score_task + 2)
#        print(p.score_task_opp1)
#    if participant.better_opp == 0:
#        if p.min_opp1_worse > p.max_opp1_worse:
#            p.score_task_opp1 = random.randint(p.max_opp1_worse, p.min_opp1_worse)
#        else:
#            p.score_task_opp1 = random.randint(p.score_task - 2, p.score_task - 1)
#    p.score_task_opp2 = int(p.sum_group - p.score_task - p.score_task_opp1)
     # calculate total score of player and opponents / group members

    if p.round_number == 1:
        p.score_total = p.score_task
        p.tot_rscore_opp1 = p.score_task_opp1
        p.tot_rscore_opp2 = p.score_task_opp2
    else:
        prev_player = p.in_round(player.round_number - 1)
        p.score_total = prev_player.score_total + p.score_task
        p.tot_rscore_opp1 = prev_player.tot_rscore_opp1 + p.score_task_opp1
        p.tot_rscore_opp2 = prev_player.tot_rscore_opp2 + p.score_task_opp2
        from statistics import mean




    ## redistribution variables
    if participant.redistribution == 1:
        p.red_amount = round(p.sum_group_third - p.score_task, 1)
        p.red_amount_opp1 = round(p.sum_group_third - p.score_task_opp1,1)
        p.red_amount_opp2 = round(p.sum_group_third - p.score_task_opp2,1)

    else:
        p.red_amount = 0
        p.red_amount_opp1 = 0
        p.red_amount_opp2 = 0

    if p.round_number == 1:
        p.red_amount_tot = round(p.red_amount,1)
        p.red_amount_tot_opp1 = round(p.red_amount_opp1,1)
        p.red_amount_tot_opp2 = round(p.red_amount_opp2,1)
        p.sum_group_third_tod = round(p.sum_group_third, 1)


    else: # something is wrong in round 3... (only adds those
        prev_player = p.in_round(player.round_number - 1)
        p.red_amount_tot = round(prev_player.red_amount_tot + p.red_amount,1)
        p.red_amount_tot_opp1 = round(prev_player.red_amount_tot_opp1 + p.red_amount_opp1,1)
        p.red_amount_tot_opp2 = round(prev_player.red_amount_tot_opp2 + p.red_amount_opp2,1)
        p.sum_group_third_tod = round(prev_player.sum_group_third_tod + p.sum_group_third, 1)
    print(p.sum_group_third_tod)
    # doesn't work if 0.
    if p.score_task != 0 and (p.score_task < p.sum_group_third):
        p.diff_red = (p.sum_group_third_tod / p.score_total) - 1

    elif p.score_task != 0 and (p.score_task > p.sum_group_third):
        p.diff_red = (p.sum_group_third_tod / p.score_total)
    else:
        p.diff_red = p.sum_group_third_tod
    print('Percentage Diff. tot in', p.round_number, p.diff_red)




    print(p.red_amount_tot)


####### PAGES #######################################################################

class instr(Page):
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def before_next_page(player, timeout_happened):
        gen_seed(player)



class Instructions1(Page):
    pass


class Game(Page):
    timeout_seconds = 45
    timer_text = 'Verbleibende Zeit:'
    live_method = play_game

    @staticmethod
    def js_vars(player: Player):
        return dict(params=player.session.params)

    @staticmethod
    def vars_for_template(player: Player):
        task_module = get_task_module(player)
        return dict(DEBUG=settings.DEBUG,
                    input_type=task_module.INPUT_TYPE,
                    placeholder=task_module.INPUT_HINT)

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if not timeout_happened and not player.session.params['max_iterations']:
            raise RuntimeError("malicious page submission")





class Results_Round(Page):
    @staticmethod
    def vars_for_template(player: Player):
        get_score(player)
        return dict()



class Results_Cap(Page):

        def is_displayed(player: Player):
            participant = player.participant
            return participant.redistribution is False



class Results_Red(Page):
    def is_displayed(player: Player):
        participant = player.participant
        return participant.redistribution is True




page_sequence = [instr, Instructions1, Game, Results_Round, Results_Cap, Results_Red]


## See VL 5 for adjusting the templates
