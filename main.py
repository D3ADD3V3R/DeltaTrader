import sys

import numpy as np
import sqlite3
import argparse

from PyQt5.QtWidgets import QApplication

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Flatten, Dense
from deepevolution import wrap_keras

from ApplicationDashboard import ApplicationDashboard
from TradingEnvironment import TradingEnvironment

TYPE = 'KLINES_15M'
SYMBOL = 'ETHUSDT'


#
# For KI purposes https://pypi.org/project/deepevolution/
#

def Random_games(dashboard, env, train_episodes=50, training_batch_size=500):
    average_net_worth = 0
    for episode in range(train_episodes):
        state = env.reset(env_steps_size=training_batch_size)

        while True:

            action = np.random.randint(3, size=1)[0]
            state, reward, done = env.step(action)

            env.render()

            if env.current_step == env.end_step:
                average_net_worth += env.net_worth
                print("net_worth:", env.net_worth)
                break

    print("average_net_worth:", average_net_worth / train_episodes)


class MainClass:
    def __init__(self):
        self.lookback_window_size = 50

    def main(self, args):
        conn = sqlite3.connect(args.data)
        conn.row_factory = sqlite3.Row

        dataset = list(conn.execute(f"SELECT * FROM {args.table} WHERE SYMBOL = '{args.symbol}'"))

        train_df = dataset[: -self.lookback_window_size]
        test_df = dataset[-self.lookback_window_size:]  # 30 days

        train_env = TradingEnvironment('FirstBot', train_df, lookback_window_size=self.lookback_window_size)
        test_env = TradingEnvironment('FirstBot', test_df, lookback_window_size=self.lookback_window_size)

        app = QApplication([])
        dashboard = ApplicationDashboard()

        if args.train:
            dashboard.show()
            app.setStyle('Fusion')
            app.exec()

        if args.test:
            if not args.nogui:
                Random_games(dashboard, test_env, 10, 500)
            else:
                Random_games(None, test_env, 1, 50)

        if args.trade:
            pass

    def train(self, dashboard, train_data, generations=10, polulation=10):
        wrap_keras()

        # Create the Model
        kiModel = Sequential([
            Flatten(input_shape=(50, 6)),
            Dense(512, activation='relu'),
            Dense(512),
            Dense(128),
            Dense(3)
        ])




if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Deltatrader for Evolution Trading')
    parser.add_argument('-d', '--data', default='kline_data.db', help='Path to the sqlite database')
    parser.add_argument('-t', '--table', default=TYPE, help='The Type of Data User (Tablename)')
    parser.add_argument('-s', '--symbol', default=SYMBOL, help='The Symbol to use')
    parser.add_argument('-g', '--nogui', action='store_true', help='Disables the Dashboard')
    parser.add_argument('--train', action='store_true', help='Train the evolution ki')
    parser.add_argument('--test', action='store_true', help='Trade with the given broker')
    parser.add_argument('--trade', action='store_true', help='Test the evolution ki (or do random actions)')
    parser.add_argument('-f', '--file', required='--trade' in sys.argv, help='JSON-File with the broker data')

    args = parser.parse_args()

    MainClass().main(args)
