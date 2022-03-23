from random import random

class weekly_state:
    """
    The weekly state for a single drug
    usage: the average weekly usage
    doses: the number of doses in a single unit involved in an order

    Includes:
    - Current In Stock Amount
    - Patients Treated This Week
    - Patients Untreated This Week
    """
    def __init__(self, usage, doses):
        self.stock = 0
        self.treated = 0
        self.untreated = 0
        self.avg_usage = usage
        self.order_unit_doses = doses
        # # orders go bad after a certain point
        # self.shelf_life = 4 # weeks
        # self.batches = []


    def new_week(self):
        rand = random()
        if (rand * 10) % 2 == 0:
            sign = 1
        else:
            sign = -1
        
        rand /= 5
        usage = int(self.avg_usage * (1+rand*sign))
        
        if self.stock > usage:
            self.stock -= usage
            self.treated = usage
            self.untreated = 0
        else:
            self.treated = self.stock
            self.untreated = usage - self.stock
            self.stock = 0

    def perform_action(self, action):
        """
        Possible actions
        0: do nothing
        1+: order more (the number is the size)

        return: the reward for the action (as well as progresses to the next week)
        """
        reward = 0
        if self.stock < 500:
            reward -= (100 * (500-self.stock))
        if self.stock > 1000:
            reward -= (100 * (self.stock-1000))
        if action >= 1:
            self.stock += (action * self.order_unit_doses)
            reward -= (1000 * action)   


        self.new_week()

        # reward += (1 * self.treated)
        reward -= (10000 * self.untreated)

        return reward
