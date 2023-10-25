from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'interview'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    trial_task = models.IntegerField()
    trial_answer = models.IntegerField()
    blind = models.BooleanField()
    compete = models.BooleanField()
    belief_relative = models.FloatField()
    belief_absolute = models.IntegerField()


def blind(player):
    import random
    treatment = random.randint(0,1)
    player.blind = treatment
    player.participant.blind = player.blind


# PAGES
class Structure(Page):

    def vars_for_template(player):
        blind(player)

class IntroToInterview(Page):
    pass

class TrialTask(Page):
    form_model = 'player'
    form_fields = ['trial_task']

    def is_displayed(subsession):
        return subsession.round_number == 1


    def vars_for_template(player):
        import random
        # Generate a list of 16 random integers, each either 0 or 1
        grid_numbers = [random.randint(0, 1) for _ in range(16)]
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


class Task(Page):
    pass

class Belief(Page):
    pass

class Outcome(Page):
    pass


page_sequence = [Structure, IntroToInterview, TrialTask, Decision, Task, Outcome]
