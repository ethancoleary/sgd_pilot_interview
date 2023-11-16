from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'interview'
    PLAYERS_PER_GROUP = 5
    NUM_ROUNDS = 25
    PAYMENT_PER_CORRECT_ANSWER = 0.1
    USE_POINTS = True


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    trial_task = models.IntegerField()
    trial_answer = models.IntegerField()
    number_entered = models.IntegerField()
    correct_answer = models.IntegerField()
    score = models.IntegerField(initial=0)

    quota = models.BooleanField()
    compete = models.BooleanField()
    belief_relative = models.IntegerField(
        widget=widgets.RadioSelect,
        choices=[
            [1, '1st place'],
            [2, '2nd place'],
            [3, '3rd place'],
            [4, '4th place'],
        ],
        initial=0
    )
    belief_absolute = models.IntegerField(initial = 0)
    combined_payoff = models.CurrencyField(initial=0)
    belief_absolute_payoff = models.CurrencyField(initial=0)
    belief_relative_payoff = models.CurrencyField(initial=0)
    interview_total_payoff = models.CurrencyField(initial=0)
    worker_1_id = models.IntegerField()
    worker_2_id = models.IntegerField()
    worker_3_id = models.IntegerField()
    worker_1_score = models.IntegerField()
    worker_2_score = models.IntegerField()
    worker_3_score = models.IntegerField()
    position = models.IntegerField()


def quota(player):
    import random
    treatment = random.randint(0,1)
    player.quota = treatment
    player.participant.quota = player.quota

    if player.participant.male == 1:
        player.participant.quota = 0


timer_text = 'Time left in interview task'
def get_timeout_seconds(player):
    participant = player.participant
    import time
    return participant.expiry - time.time()

def is_displayed1(player: Player):
    """only returns True if there is time left."""
    return get_timeout_seconds1(player) > 0

# PAGES
class Structure(Page):

    def is_displayed(subsession):
        return subsession.round_number == 1
    def vars_for_template(player):
        quota(player)

class IntroToInterview(Page):
    def is_displayed(subsession):
        return subsession.round_number == 1

class TrialTask(Page):
    form_model = 'player'
    form_fields = ['trial_task']

    def is_displayed(subsession):
        return subsession.round_number == 1


    def vars_for_template(player):
        import random
        # Generate a list of 16 random integers, each either 0 or 1
        grid_numbers = [random.randint(0, 1) for _ in range(9)]
        player.trial_answer = sum(grid_numbers)

        return {
            'grid_numbers': grid_numbers
        }

    @staticmethod
    def error_message(player: Player, values):
        solutions = dict(trial_task = player.trial_answer)

        if values != solutions:
            return "Answer is incorrect, try again."


class Decision(Page):
    form_model = 'player'
    form_fields = ['compete']

    def is_displayed(subsession):
        return subsession.round_number == 1

    @staticmethod
    def before_next_page(player, timeout_happened):
        participant = player.participant
        participant.compete = player.compete
        import time

        # remember to add 'expiry' to PARTICIPANT_FIELDS.
        participant.expiry = time.time() + 30



class Task(Page):
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
        grid_numbers = [random.randint(0, 1) for _ in range(9)]
        player.correct_answer = sum(grid_numbers)

        return {
            'grid_numbers': grid_numbers
        }

    def before_next_page(player, timeout_happened):
        participant = player.participant
        if player.correct_answer == player.number_entered:
            player.score = 1
            if participant.compete == 0:
                player.payoff = C.PAYMENT_PER_CORRECT_ANSWER
        else:
            player.score = 0
        participant.manager = 0


class Calculation(Page):
    timeout_seconds = 0.1

    def is_displayed(player):
        return get_timeout_seconds(player) <= 0

    def before_next_page(player, timeout_happened):

        all_players = player.in_all_rounds()
        total_score = sum([p.score for p in all_players])

        participant = player.participant
        participant.interview_score = total_score


        if participant.compete == 0:
            player.combined_payoff = participant.interview_score * C.PAYMENT_PER_CORRECT_ANSWER
            participant.combined_payoff = player.combined_payoff

        male_pool = {
            1: 1,
            2: 1,
            3: 1,
            4: 1,
            5: 1,
            6: 1,
            7: 1,
            8: 1,
            9: 1,
            10: 1,
            11: 1,
        }

        female_pool = {
            20: 1,
            21: 1,
            23: 1,
            24: 1,
            25: 1,
            26: 1,
            27: 1,
            28: 1,
            29: 1,
            30: 1,
            31: 1,
        }

        import random

        if participant.compete == 1:
        ## Worker 1 and 2 are always of opposite gender. Worker 3 is own gender.
            if participant.male == 1:
                player.worker_1_id, player.worker_1_score = random.choice(list(female_pool.items()))
                player.worker_2_id, player.worker_2_score = random.choice(list(female_pool.items()))
                while player.worker_2_id == player.worker_1_id:
                    player.worker_2_id, player.worker_2_score = random.choice(list(female_pool.items()))

                player.worker_3_id, player.worker_3_score = random.choice(list(male_pool.items()))

                others_scores = [player.worker_1_score, player.worker_2_score, player.worker_3_score]
                others_scores.sort()

                if participant.interview_score >= others_scores[0]:
                    player.position = 1
                if participant.interview_score < others_scores[0] and participant.interview_score >= others_scores[1]:
                    player.position = 2
                if participant.interview_score < others_scores[1] and participant.interview_score >= others_scores[2]:
                    player.position = 3
                if participant.interview_score < others_scores[2]:
                    player.position = 4

                if participant.interview_score > others_scores[1]:
                    player.combined_payoff = 2
                    participant.manager = 1

                if participant.interview_score == others_scores[1]:
                    roll = random.randint(0,1)
                    if roll == 1:
                        player.combined_payoff = 2
                        participant.manager = 1
                    else:
                        player.combined_payoff = 0
                        participant.manager = 0

                if participant.interview_score < others_scores[1]:
                    player.combined_payoff = 0
                    participant.manager = 0

            if participant.female == 1:
                player.worker_1_id, player.worker_1_score = random.choice(list(male_pool.items()))
                player.worker_2_id, player.worker_2_score = random.choice(list(male_pool.items()))
                while player.worker_2_id == player.worker_1_id:
                    player.worker_2_id, player.worker_2_score = random.choice(list(male_pool.items()))

                player.worker_3_id, player.worker_3_score = random.choice(list(female_pool.items()))

                others_scores = [player.worker_1_score, player.worker_2_score, player.worker_3_score]
                others_scores.sort()

                if participant.interview_score >= others_scores[0]:
                    player.position = 1
                if participant.interview_score < others_scores[0] and participant.interview_score >= others_scores[1]:
                    player.position = 2
                if participant.interview_score < others_scores[1] and participant.interview_score >= others_scores[2]:
                    player.position = 3
                if participant.interview_score < others_scores[2]:
                    player.position = 4

                if participant.quota == 1:

                    if player.worker_1_score >= player.worker_2_score:
                        top_male_score = player.worker_1_score
                    else:
                        top_male_score = player.worker_2_score

                    if participant.interview_score > top_male_score or participant.interview_score > player.worker_3_score:
                        player.combined_payoff = 2
                        participant.manager = 1

                    if participant.interview_score == top_male_score or participant.interview_score == player.worker_3_score:
                        roll = random.randint(0, 1)
                        if roll == 1:
                            player.combined_payoff = 2
                            participant.manager = 1
                        else:
                            player.combined_payoff = 0
                            participant.manager = 0
                    else:
                        player.combined_payoff = 0
                        participant.manager = 0

                if participant.quota == 0:



                    if participant.interview_score > others_scores[1]:
                        player.combined_payoff = 2
                        participant.manager = 1

                    if participant.interview_score == others_scores[1]:
                        roll = random.randint(0, 1)
                        if roll == 1:
                            player.combined_payoff = 2
                            participant.manager = 1
                        else:
                            player.combined_payoff = 0
                            participant.manager = 0

                    if participant.interview_score < others_scores[1]:
                        player.combined_payoff = 0
                        participant.manager = 0


        if participant.compete == 0:
            participant.die_roll = random.randint(1, 6)
            if participant.die_roll <3:
                participant.manager = 1
            else:
                participant.manager = 0

class Belief(Page):
    form_model = 'player'
    form_fields = ['belief_absolute', 'belief_relative']
    def is_displayed(player):
        participant = player.participant
        return participant.manager == 1 and participant.compete == 1 and get_timeout_seconds(player) <= 0


    def before_next_page(player, timeout_happened):
        participant = player.participant
        if participant.interview_score == player.belief_absolute:
            player.belief_absolute_payoff = 1


class Belief_die(Page):
    form_model = 'player'
    form_fields = ['belief_absolute']
    def is_displayed(player):
        participant = player.participant
        return participant.manager == 1 and participant.compete == 0 and get_timeout_seconds(player) <= 0


    def before_next_page(player, timeout_happened):
        participant = player.participant
        if participant.interview_score == player.belief_absolute:
            player.belief_absolute_payoff = 1

class Outcome(Page):

    def is_displayed(player):
        return get_timeout_seconds(player) <= 0

    def vars_for_template(player):

        participant = player.participant

        player.belief_relative_payoff = player.position == player.belief_relative

        if player.position == 1 :
            relative = "1st"

        if player.position == 2:
            relative = "2nd"

        if player.position == 3:
            relative = "3rd"

        if player.position == 4:
            relative = "4th"

        if player.belief_relative == 1 :
            belief_relative = "1st"

        if player.belief_relative == 2:
            belief_relative = "2nd"

        if player.belief_relative == 3:
            belief_relative = "3rd"

        if player.belief_relative == 4:
            belief_relative = "4th"

        payoff_relative = cu(player.belief_relative_payoff)
        if participant.compete == 1:
            if participant.manager == 1:
                participant.interview_payoff = cu(player.belief_relative_payoff+player.belief_absolute_payoff+2)
            if participant.manager == 0:
                participant.interview_payoff = 0

        if participant.compete == 0:
            participant.interview_payoff = cu(player.belief_relative_payoff + player.belief_absolute_payoff + participant.interview_score*C.PAYMENT_PER_CORRECT_ANSWER)


        return {
            'belief_relative':belief_relative,
            'relative':relative,
            'payoff_relative':payoff_relative
        }




    @staticmethod
    def app_after_this_page(player, upcoming_apps):
        participant = player.participant
        if get_timeout_seconds(player) <= 0 and participant.manager == 1:
            return upcoming_apps[0]
        if participant.manager == 0:
            return upcoming_apps[-1]


page_sequence = [Structure, IntroToInterview, TrialTask, Decision, Task, Calculation, Belief, Belief_die, Outcome]

