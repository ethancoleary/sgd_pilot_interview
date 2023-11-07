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
    TEAMS = [['Jacob', 'Daniel'], ['Matthew', 'Zoe']]
    TEAMS_SCORE = [[5, 6], [5, 4]]
    TEAMS_SCORE2 = [[3, 3], [3, 3]]
    BOARDS = [['Aiden', 'Samuel', 'Alexander'], ['Abigail', 'Grace', 'Emma']]
    BOARDS_VOTE = [[[1,0], [1,0], [1,0]], [[1,1], [0,1], [0,0]]]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    t2_mixgroup = models.BooleanField()
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
        choices = [1, 2, 3]
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

def t2(player):
    import random

    t2 = random.randint(0,1)
    player.t2_mixgroup = t2
    player.participant.t2_mixgroup = player.t2_mixgroup


    malefirst = random.randint(0,1)
    player.t2_malefirst = malefirst
    player.participant.t2_malefirst =  player.t2_malefirst

def t3(player):
    import random
    t3 = random.randint(0,1)
    player.t3_observed = t3
    player.participant.t3_observed = player.t3_observed

def t4(player):
    import random
    t4 = random.randint(0,2)
    if t4 == 0:
        player.t4_maleboard = 0
        player.t4_femaleboard = 0
        player.participant.t4_maleboard = 0
        player.participant.t4_femaleboard = 0

    if t4 == 1:
        player.t4_maleboard = 1
        player.t4_femaleboard = 0
        player.participant.t4_maleboard = 1
        player.participant.t4_femaleboard = 0
    if t4 == 2:
        player.t4_maleboard = 0
        player.t4_femaleboard = 1
        player.participant.t4_femaleboard = 1
        player.participant.t4_maleboard = 0

# PAGES
class TeamWelcome(Page):

    def is_displayed(subsession):
        return subsession.round_number == 1
    def vars_for_template(player):
        t2(player)
        t3(player)
        t4(player)



        team = C.TEAMS[player.t2_mixgroup]
        player.team1 = team[1-player.t2_malefirst]
        player.team2 = team[player.t2_malefirst]

        participant = player.participant

        participant.team1 = player.team1
        participant.team2 = player.team2



class Round1Intro(Page):

    def is_displayed(subsession):
        return subsession.round_number == 1

    def vars_for_template(player):
        import random
        # Generate a list of 16 random integers, each either 0 or 1
        grid_numbers = [random.randint(0, 1) for _ in range(16)]

        return {
            'grid_numbers': grid_numbers
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
        participant = player.participant

        import random
        # Generate a list of 25 random integers, each either 0 or 1
        grid_numbers = [random.randint(0, 1) for _ in range(16)]
        player.correct_answer = sum(grid_numbers)

        return {
            'grid_numbers': grid_numbers
        }

    def before_next_page(player, timeout_happened):
        participant = player.participant
        if player.correct_answer == player.number_entered:
            player.score = 1
            player.payoff = C.PAYMENT_PER_CORRECT_ANSWER



class Calculation(Page):
    timeout_seconds = 0.1

    def is_displayed(player):
        return get_timeout_seconds(player) <= 0 and player.display_counter < 1

    def before_next_page(player, timeout_happened):

        all_players = player.in_all_rounds()
        total_score = sum([p.score for p in all_players])
        player.round1_performance_payment = sum([p.payoff for p in all_players])

        participant = player.participant
        participant.round1_score = total_score
        player.round1_performance_payment = total_score * C.PAYMENT_PER_CORRECT_ANSWER



        player.display_counter = player.round_number




class Belief(Page):
    form_model = 'player'
    form_fields = ['belief_absolute', 'belief_relative']
    def is_displayed(player):
        participant = player.participant
        return get_timeout_seconds(player) <= 0 and player.round_number == player.display_counter

    def before_next_page(player, timeout_happened):
        participant = player.participant
        if participant.round1_score == player.belief_absolute:
            player.belief_absolute_payoff = 1




class Round1Results(Page):

    def is_displayed(player):
        participant = player.participant
        return get_timeout_seconds(player) <= 0 and player.round_number == player.display_counter

    def vars_for_template(player):
        participant = player.participant
        team_score = C.TEAMS_SCORE[participant.t2_mixgroup]
        player.team1_score = team_score[1 - participant.t2_malefirst]
        player.team2_score = team_score[participant.t2_malefirst]


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
                player.belief_relative_payoff = 1
        if player.tie == 1 :
            if player.belief_relative == 2:
                player.belief_relative_payoff = 1
            if player.player_positions ==2 and player.belief_relative == 3:
                player.belief_relative_payoff = 1
            if player.player_positions ==1 and player.belief_relative == 1:
                player.belief_relative_payoff = 1

        participant.total_round1_payoff = player.round1_performance_payment + player.belief_relative_payoff + player.belief_absolute_payoff



class Round2Intro(Page):

    def is_displayed(player):
        participant = player.participant
        return get_timeout_seconds(player) <= 0 and player.round_number == player.display_counter

    def vars_for_template(player):
        import random
        # Generate a list of 25 random integers, each either 0 or 1
        grid_numbers = [random.randint(0, 1) for _ in range(36)]

        participant = player.participant
        if participant.t4_femaleboard == 0 and participant.t4_maleboard == 0:
            participant.board_names = ["", "", ""]
        else:
            participant.board_names = C.BOARDS[participant.t4_femaleboard]

        player.board1 = participant.board_names[0]
        player.board2 = participant.board_names[1]
        player.board3 = participant.board_names[2]

        return {
            'grid_numbers': grid_numbers,
        }

class Round2Decision(Page):
    form_model = 'player'
    form_fields = ['workerA_team1']

    def is_displayed(player):
        participant = player.participant
        return get_timeout_seconds(player) <= 0 and player.round_number == player.display_counter

class Round2Results(Page):

    def is_displayed(player):
        participant = player.participant
        return get_timeout_seconds(player) <= 0 and player.round_number == player.display_counter

    def vars_for_template(player):
        participant = player.participant
        team_score = C.TEAMS_SCORE2[participant.t2_mixgroup]
        player.team1_score2 = team_score[1 - participant.t2_malefirst]
        player.team2_score2 = team_score[participant.t2_malefirst]

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

            if participant.t4_maleboard + participant.t4_femaleboard > 0:
                board_votes = C.BOARDS_VOTE[participant.t4_femaleboard]
            else:
                import random
                board_number = random.randint(0,1)
                board_votes = C.BOARDS_VOTE[board_number]

            board_votes_cast = [board_votes[0][participant.t2_mixgroup], board_votes[1][participant.t2_mixgroup], board_votes[2][participant.t2_mixgroup]]


            board1_vote = C.TEAMS[participant.t2_mixgroup][board_votes_cast[0]]
            board2_vote = C.TEAMS[participant.t2_mixgroup][board_votes_cast[1]]
            board3_vote = C.TEAMS[participant.t2_mixgroup][board_votes_cast[2]]

            board1_agree = board1_vote == workerA
            board2_agree = board2_vote == workerA
            board3_agree = board3_vote == workerA

            board_members_agreeing = board1_agree + board2_agree + board3_agree

            commission_payout = cu(((board_members_agreeing)/3) * player.workerA_score * C.COMMISSION_PER_CORRECT_ANSWER)


            #BOARDS = [['Aiden', 'Samuel', 'Alexander'], ['Abigail', 'Grace', 'Emma']]
            #BOARDS_VOTE = [[[1,0], [1,0], [1,0]], [[1,1], [0,1], [0,0]]]

        player.round2_performance_payment = commission_payout
        player.total_rounds_payoff = player.round1_performance_payment + player.belief_relative_payoff + player.belief_absolute_payoff+ player.round2_performance_payment

        if participant.t3_observed == 1:
            return {
                'board1_vote': board1_vote,
                'board2_vote': board2_vote,
                'board3_vote': board3_vote,

                'board1_agree':board1_agree,
                'board2_agree':board2_agree,
                'board3_agree':board3_agree,

                'board_member_agreeing':board_members_agreeing,

                'workerB_score': workerB_score,
                'workerA':workerA,
                'workerB':workerB,
            }
        if participant.t3_observed == 0:
            return {
                'workerB_score': workerB_score,
                'workerA':workerA,
                'workerB':workerB,

            }




page_sequence = [TeamWelcome, Round1Intro, Round1, Calculation, Belief, Round1Results, Round2Intro, Round2Decision, Round2Results]
