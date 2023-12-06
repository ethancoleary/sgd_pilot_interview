from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'manager'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 25
    PAYMENT_PER_CORRECT_ANSWER = 0.15
    COMMISSION_PER_CORRECT_ANSWER = 0.2
    COMPETITORS = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    GROUP_TYPE = [1, 2, 3]
    PAIR = [[
        [0, 8], [1, 5], [2, 7], [3, 4]],
        [[1,8], [0,6], [2,5]],
        [[1, 6], [2, 8], [3, 5]]
    ]
    WORKER_NAMES = [
        "Zoe",
        "Chloe D",
        "Chloe T",
        "Emma",
        "Alexander",
        "Daniel",
        "Jacob M",
        "Jacob R",
        "Harvey"]
    WORKER_ROUND1_SCORES = [
        3,
        4,
        5,
        7,
        8,
        5,
        3,
        6,
        4,
    ]
    WORKER_ROUND2_SCORES = [
        4,
        4,
        0,
        4,
        4,
        7,
        3,
        4,
        5,
    ]

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    t2_group_type = models.IntegerField()
    t2_malefirst = models.BooleanField()
    t3_observed = models.BooleanField()
    t4_maleboard = models.BooleanField(initial=0)
    t4_femaleboard = models.BooleanField(initial=0)
    team1 = models.StringField()
    team1_score = models.IntegerField()
    team1_score2 = models.IntegerField()
    team2 = models.StringField()
    team2_score = models.IntegerField()
    team2_score2 = models.IntegerField()
    number_entered = models.IntegerField()
    correct_answer = models.IntegerField()
    score = models.IntegerField(initial=0)
    belief_absolute = models.IntegerField()
    belief_relative = models.IntegerField(
        widget=widgets.RadioSelect,
        choices=[
            [1, '1st place'],
            [2, '2nd place'],
            [3, '3rd place'],
        ],
        initial=0
    )
    round1_performance_payment = models.CurrencyField()
    round2_performance_payment = models.CurrencyField()
    belief_absolute_payoff = models.CurrencyField(initial=0)
    belief_relative_payoff = models.CurrencyField(initial=0)
    player_positions = models.IntegerField(initial=2)
    tie = models.BooleanField(initial=False)
    display_counter = models.IntegerField(initial=0)
    board1 = models.StringField()
    board2 = models.StringField()
    board3 = models.StringField()
    workerA_team1 = models.BooleanField()
    total_rounds_payoff = models.CurrencyField()
    commission = models.CurrencyField()
    workerA_score = models.IntegerField()

timer_text = 'Time left in this round'
def get_timeout_seconds(player):
    participant = player.participant
    import time
    return participant.expiry - time.time()

def team(player):
    import random
    participant = player.participant

    player.t2_group_type = random.randint(0,2)
    participant.t2_type = player.t2_group_type

    teams = C.PAIR[player.t2_group_type]
    participant.team = teams[0] #Here I've set it all to the one where x =4

    malefirst = random.randint(0, 1)
    player.t2_malefirst = malefirst
    participant.t2_malefirst = malefirst

    if malefirst == 1 :

        participant.team.reverse()

    player.team1 = C.WORKER_NAMES[participant.team[0]]
    participant.team1 = player.team1
    player.team2 = C.WORKER_NAMES[participant.team[1]]
    participant.team2 = player.team2

def t3(player):
    import random
    participant = player.participant

    t3 = random.randint(0,1)
    player.t3_observed = t3
    participant.t3_observed = t3


# PAGES
class TeamWelcome(Page):

    def is_displayed(subsession):
        return subsession.round_number == 1
    def vars_for_template(player):
        team(player)
        t3(player)

        participant = player.participant

        participant.team1 = player.team1
        participant.team2 = player.team2



class Round1Intro(Page):

    def is_displayed(subsession):
        return subsession.round_number == 1

    def vars_for_template(player):
        grid_numbers = [1, 0, 1,
                     0, 0, 0,
                     1, 0, 0]

        return {
            'grid_numbers': grid_numbers,
        }



    @staticmethod
    def before_next_page(player, timeout_happened):
        participant = player.participant
        import time

        # remember to add 'expiry' to PARTICIPANT_FIELDS.
        participant.expiry = time.time() + 20

class Round1(Page):
    form_model = 'player'
    form_fields = ['number_entered']
    import random

    get_timeout_seconds = get_timeout_seconds

    @staticmethod
    def is_displayed(player):
        return get_timeout_seconds(player) >= 0

    def vars_for_template(player):
        import random
        # Generate a list of 25 random integers, each either 0 or 1
        ones = random.randint(1, 9)
        grid_numbers = [0, 0, 0,
                        0, 0, 0,
                        0, 0, 0]
        for i in range(9):
            if i < ones:
                grid_numbers[i] = 1
        random.shuffle(grid_numbers)
        player.correct_answer = ones

        return {
            'grid_numbers': grid_numbers
        }

    def before_next_page(player, timeout_happened):
        participant = player.participant
        if player.correct_answer == player.number_entered:
            player.score = 1
            player.payoff = C.PAYMENT_PER_CORRECT_ANSWER




class Belief(Page):
    form_model = 'player'
    form_fields = ['belief_absolute', 'belief_relative']
    def is_displayed(player):
        participant = player.participant
        return get_timeout_seconds(player) <= 0
    def vars_for_template(player):
        all_players = player.in_all_rounds()
        total_score = sum([p.score for p in all_players])
        player.round1_performance_payment = sum([p.payoff for p in all_players])

        participant = player.participant
        participant.round1_score = total_score
        player.round1_performance_payment = total_score * C.PAYMENT_PER_CORRECT_ANSWER

        player.display_counter = player.round_number


    def before_next_page(player, timeout_happened):
        participant = player.participant
        if participant.round1_score == player.belief_absolute:
            player.belief_absolute_payoff = 0.5




class Round1Results(Page):

    def is_displayed(player):
        participant = player.participant
        return get_timeout_seconds(player) <= 0

    def vars_for_template(player):
        participant = player.participant

        player.team1_score = C.WORKER_ROUND1_SCORES[participant.team[0]]

        player.team2_score = C.WORKER_ROUND1_SCORES[participant.team[1]]


        round1_scores = [participant.round1_score, player.team1_score, player.team2_score]
        if participant.round1_score == min(round1_scores):
            player.player_positions = 3
            if participant.round1_score == min(player.team1_score, player.team2_score):
                player.tie = True

        if participant.round1_score == max(round1_scores):
            player.player_positions = 1
            if participant.round1_score == max(player.team1_score, player.team2_score):
                player.tie = True


        if player.tie == 0 :
            if player.player_positions == player.belief_relative:
                player.belief_relative_payoff = cu(0.5)
        if player.tie == 1 :
            if player.belief_relative == 2:
                player.belief_relative_payoff = cu(0.5)
            if player.player_positions ==2 and player.belief_relative == 3:
                player.belief_relative_payoff = cu(0.5)
            if player.player_positions ==1 and player.belief_relative == 1:
                player.belief_relative_payoff = cu(0.5)

        participant.total_round1_payoff = cu(player.round1_performance_payment + player.belief_relative_payoff + player.belief_absolute_payoff)



class Round2Intro(Page):

    def is_displayed(player):
        participant = player.participant
        return get_timeout_seconds(player) <= 0

    def vars_for_template(player):
        import random
        ones = random.randint(8, 36)
        grid_numbers = [0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0]
        for i in range(36):
            if i < ones:
                grid_numbers[i] = 1
        random.shuffle(grid_numbers)
        player.correct_answer = ones

        participant = player.participant

        if participant.t3_observed == 0:
            player.board1 = ""
            player.board2 = ""
            player.board3 = ""
        if participant.t3_observed == 1:
            participant.board_names = ["Mason", "Alexander", "Daniel"]
            player.board1 = participant.board_names[0]
            player.board2 = participant.board_names[1]
            player.board3 = participant.board_names[2]

        return {
            'grid_numbers': grid_numbers
        }




class Round2Decision(Page):
    form_model = 'player'
    form_fields = ['workerA_team1']

    def is_displayed(player):
        participant = player.participant
        return get_timeout_seconds(player) <= 0 and player.round_number == player.display_counter


class Calculation(Page):
    timeout_seconds = 2


    def is_displayed(player):
        return get_timeout_seconds(player) <= 0 and player.round_number == player.display_counter


class Round2Results(Page):

    def is_displayed(player):
        participant = player.participant
        return get_timeout_seconds(player) <= 0 and player.round_number == player.display_counter

    def vars_for_template(player):
        participant = player.participant

        player.team1_score2 = C.WORKER_ROUND2_SCORES[participant.team[0]]

        player.team2_score2 = C.WORKER_ROUND2_SCORES[participant.team[1]]

        if player.workerA_team1 == True:
            workerA = participant.team1
            workerB = participant.team2
            player.workerA_score = player.team1_score2
            workerB_score = player.team2_score2

        if player.workerA_team1 == False:
            workerA = participant.team2
            workerB = participant.team1
            player.workerA_score = player.team2_score2
            workerB_score = player.team1_score2

        player.commission = cu(player.workerA_score * C.COMMISSION_PER_CORRECT_ANSWER)
        commission_payout = player.commission

        if participant.t3_observed == 1:
            import random

            if participant.t2_type == 0 or participant.t2_type == 2:
                board_votes = [1,1,1]
            if participant.t2_type == 1:
                board_votes = [random.randint(0, 1), random.randint(0, 1), random.randint(0, 1)]

            board1_agree = board_votes[0]
            board2_agree = board_votes[1]
            board3_agree = board_votes[2]
            board_members_agreeing = sum(board_votes)

            commission_payout = cu(((board_members_agreeing)/3) * player.commission)

            #BOARDS = [['Aiden', 'Samuel', 'Alexander'], ['Abigail', 'Grace', 'Emma']]
            #BOARDS_VOTE = [[[1,0], [1,0], [1,0]], [[1,1], [0,1], [0,0]]]

        player.round2_performance_payment = cu(commission_payout)
        participant.total_round2_payoff = player.round2_performance_payment

        import random
        round_draw = random.randint(1, 2)

        if round_draw == 1:
            participant.stage2_payoff = participant.total_round1_payoff
        if round_draw == 2:
            participant.stage2_payoff = participant.total_round2_payoff

        participant.board = 0
        #participant.board = participant.total_round1_payoff + participant.total_round2_payoff >= 5

        if participant.t3_observed == 1:
            return {

                'board1_agree':board1_agree,
                'board2_agree':board2_agree,
                'board3_agree':board3_agree,

                'board_member_agreeing':board_members_agreeing,

                'workerB_score': workerB_score,
                'workerA':workerA,
                'workerB':workerB,
                'round_draw':round_draw,
            }

        if participant.t3_observed == 0:
            return {
                'workerB_score': workerB_score,
                'workerA':workerA,
                'workerB':workerB,
                'round_draw': round_draw,

            }

    @staticmethod
    def app_after_this_page(player, upcoming_apps):
        participant = player.participant
        return upcoming_apps[0]


        #if get_timeout_seconds(player) <= 0 and player.round_number == player.display_counter and participant.board == 1:
            #return upcoming_apps[0]
        #if participant.board == 0:
            #return upcoming_apps[-1]


page_sequence = [TeamWelcome, Round1Intro, Round1, Belief, Round1Results, Round2Intro, Round2Decision, Calculation, Round2Results]
