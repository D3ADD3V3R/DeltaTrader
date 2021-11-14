import numpy as np
import pandas as pd
import sqlite3

from TradingEnvironment import TradingEnvironment

TYPE = 'KLINES_15M'
SYMBOL = 'ETHUSDT'


#
# For KI purposes https://pypi.org/project/deepevolution/
#

class MainClass:
    def Random_games(self, env, train_episodes=50, training_batch_size=500):
        average_net_worth = 0
        for episode in range(train_episodes):
            state = env.reset(env_steps_size=training_batch_size)

            while True:
                env.render()

                action = np.random.randint(3, size=1)[0]

                state, reward, done = env.step(action)

                if env.current_step == env.end_step:
                    average_net_worth += env.net_worth
                    print("net_worth:", env.net_worth)
                    break

        print("average_net_worth:", average_net_worth / train_episodes)

    def main(self):
        conn = sqlite3.connect('kline_data.db')
        conn.row_factory = sqlite3.Row

        dataset = list(conn.execute(f"SELECT * FROM {TYPE} WHERE SYMBOL = '{SYMBOL}'"))

        lookback_window_size = 50
        train_df = dataset[: -lookback_window_size]
        test_df = dataset[-lookback_window_size:]  # 30 days

        train_env = TradingEnvironment('FirstBot', train_df, lookback_window_size=lookback_window_size)
        test_env = TradingEnvironment('FirstBot', test_df, lookback_window_size=lookback_window_size)

        self.Random_games(train_env, 10, 500)


if __name__ == '__main__':
    MainClass().main()
