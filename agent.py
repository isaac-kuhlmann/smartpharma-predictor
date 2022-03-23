from time import sleep
import csv

from weekly_state import weekly_state
import random

class agent:
    """
    Agent can perform 2 actions
    1. Order more stock
    2. Do nothing
    """
    def __init__(self):
        self.q_map = [[0 for x in range(100)] for y in range(100)]
        self.actions = [x for x in range(100)]
        self.gamma = 0.8
        self.num_states = 100
        self.avg_weekly_usage = 10000
        self.doses_per_order = 100
        self.unit_price = 1000
        self.environment = weekly_state(self.avg_weekly_usage, self.doses_per_order)
        self.verbose = False

    def best_action(self, state):
        # FIND MAX INDEX
        # best_index = 1
        best_q = 0
        # min action
        min_action = int(self.avg_weekly_usage / 100 * 0.85)
        best_index = min_action

        for i in range(min_action, self.num_states):
            if state + i >= self.num_states:
                break
            if self.q_map[state][i] >= best_q:
                best_q = self.q_map[state][i]
                best_index = i
            
        return best_index
        

    def max_reward(self, state):
        return max(self.q_map[state])

    def q_learning(self):
        """
        Randomly choose action (do nothing or make an order of some size)
        """
        running_order_avg = 0
        running_stock_avg = 0
        running_untreated = 0
        running_spent = 0
        with open('data.csv', 'w', newline='') as datafile:
            data_writer = csv.writer(datafile)
            for i in range(100000000000):
                init_stock = self.environment.stock
                init_state = int(init_stock / self.environment.order_unit_doses)

                action = self.best_action(init_state)
                # action = random.choice(self.actions)

                reward = self.environment.perform_action(action)

                # out of order from normal algorithm. the state progresses before the max reward is found
                next_stock = self.environment.stock
                next_state = int(next_stock / self.environment.order_unit_doses)

                max_next_reward = self.max_reward(next_state)
                self.q_map[init_state][next_state] = reward + (self.gamma * max_next_reward)

                running_order_avg += action
                running_stock_avg += self.environment.stock
                running_untreated += self.environment.untreated
                running_spent     += (action * self.unit_price)
                if i % 10 == 0:      
                    print('\nWeek', i)  
                    if self.verbose:
                        self.print_episode(init_stock, next_stock, action, reward)
                    order_avg = running_order_avg / 10
                    spent_avg = running_spent / 10
                    stock_avg = running_stock_avg / 10
                    print('10-Week Average Units Ordered:', order_avg, '(', self.doses_per_order, 'doses per unit )')
                    print(f'10-Week Average Spent: ${spent_avg}')
                    print('Untreated Patients over 10 weeks:', running_untreated)
                    print('Average Held In Stock over 10 weeks: ', stock_avg / 10)
                    data_writer.writerow([i, int(spent_avg), running_untreated])
                # print('Average Reward:', running_avg, '\n')
                    running_order_avg = 0
                    running_stock_avg = 0
                    running_untreated = 0
                    running_spent = 0
                # sleep()


    def print_episode(self, stock1, stock2, action, reward):
        print('Last Week Stock:', stock1)
        print('Patients Treated:', self.environment.treated)
        print('Patients Untreated:', self.environment.untreated)
        if action == 0:
            print('NO ORDER PLACED')
        else:
            print('ORDER PLACED:', action, 'Units Ordered(', self.environment.order_unit_doses ,'doses per unit )')

        print('Current Stock:', stock2)
        print('Reward:', reward)



a = agent()

a.q_learning()