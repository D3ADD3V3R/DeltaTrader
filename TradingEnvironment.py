import numpy as np
import random
from collections import deque


class TradingEnvironment:
    # A custom Bitcoin trading environment
    def __init__(self, botname, df, initial_balance=1000, lookback_window_size=50):
        # Define action space and state size and other custom parameters
        self.df = df
        self.df_total_steps = len(self.df) - 1
        self.initial_balance = initial_balance
        self.lookback_window_size = lookback_window_size
        self.botname = botname

        # Action space from 0 to 3, 0 is hold, 1 is buy, 2 is sell
        self.action_space = np.array([0, 1, 2])

        # Orders history contains the balance, net_worth, crypto_bought, crypto_sold, crypto_held values for the last lookback_window_size steps
        self.orders_history = deque(maxlen=self.lookback_window_size)

        # Market history contains the OHCL values for the last lookback_window_size prices
        self.market_history = deque(maxlen=self.lookback_window_size)

        # State size contains Market+Orders history for the last lookback_window_size steps
        self.state_size = (self.lookback_window_size, 10)

    # Reset the state of the environment to an initial state
    def reset(self, env_steps_size=0):
        self.balance = self.initial_balance
        self.net_worth = self.initial_balance
        self.prev_net_worth = self.initial_balance
        self.crypto_held = 0
        self.crypto_sold = 0
        self.crypto_bought = 0
        if env_steps_size > 0:  # used for training dataset
            self.start_step = random.randint(self.lookback_window_size, self.df_total_steps - env_steps_size) if (self.lookback_window_size < env_steps_size) else 0
            self.end_step = self.start_step + env_steps_size
        else:  # used for testing dataset
            self.start_step = self.lookback_window_size
            self.end_step = self.df_total_steps

        self.current_step = self.start_step

        for i in reversed(range(self.lookback_window_size)):
            current_step = self.current_step - i
            self.orders_history.append(
                [self.balance, self.net_worth, self.crypto_bought, self.crypto_sold, self.crypto_held])
            self.market_history.append([self.df[current_step]['OPEN'],
                                        self.df[current_step]['HIGH'],
                                        self.df[current_step]['LOW'],
                                        self.df[current_step]['CLOSE'],
                                        self.df[current_step]['VOLUME']
                                        ])

        state = np.concatenate((self.market_history, self.orders_history), axis=1)
        return state

    # Execute one time step within the environment
    def step(self, action):
        self.crypto_bought = 0
        self.crypto_sold = 0


        # Set the current price to a random price between open and close
        current_price = random.uniform(
            self.df[self.current_step]['OPEN'],
            self.df[self.current_step]['CLOSE'])

        if action == 0:  # Hold
            pass

        elif action == 1 and self.balance > 0:
            # Buy with 100% of current balance
            self.crypto_bought = self.balance / current_price
            self.balance -= self.crypto_bought * current_price
            self.crypto_held += self.crypto_bought

        elif action == 2 and self.crypto_held > 0:
            # Sell 100% of current crypto held
            self.crypto_sold = self.crypto_held
            self.balance += self.crypto_sold * current_price
            self.crypto_held -= self.crypto_sold

        self.prev_net_worth = self.net_worth
        self.net_worth = self.balance + self.crypto_held * current_price

        self.orders_history.append(
            [self.balance, self.net_worth, self.crypto_bought, self.crypto_sold, self.crypto_held])

        # Calculate reward
        reward = self.net_worth - self.prev_net_worth

        if self.net_worth <= self.initial_balance / 2:
            done = True
        else:
            done = False

        obs = self._next_observation()

        self.current_step += 1
        return obs, reward, done

    # Get the data points for the given current_step
    def _next_observation(self):
        self.market_history.append([self.df[self.current_step]['OPEN'],
                                    self.df[self.current_step]['HIGH'],
                                    self.df[self.current_step]['LOW'],
                                    self.df[self.current_step]['CLOSE'],
                                    self.df[self.current_step]['VOLUME']
                                    ])
        obs = np.concatenate((self.market_history, self.orders_history), axis=1)
        return obs

    # render environment
    def render(self):
        print(f'[{self.botname}]\tStep: {self.current_step}, Net Worth: {self.net_worth}')