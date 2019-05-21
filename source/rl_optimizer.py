#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from tetris_RLenv import *
from time import *
# import tensorflow as tf

env = TetrisEnv()
width = env.board.width
height = env.board.height + 2

# X = tf.placeholder(tf.int8, [None, width, height], name="board")


class RLOptimizer:

    def __init__(self, update_rate=0.1, learning_rate=0.1,
                 exploration_rate_min=0, exploration_rate_max=1,
                 replay_memory_size=5000, batch_size=10,
                 update_period=10, max_epochs=10):
        self.update_rate = update_rate
        self.learning_rate = learning_rate
        self.exploration_rate_min = exploration_rate_min
        self.exploration_rate_max = exploration_rate_max
        self.replay_memory_size = replay_memory_size
        self.batch_size = batch_size
        self.update_period = update_period
        self.max_epochs = max_epochs

        self.env = TetrisEnv()

    def initReplayMemory(self):
        self.replay_memory = []
        t = 0
        self.env.reset()
        while t < self.replay_memory_size:
            self.env.render()
            sleep(0)

            s0 = self.env.getState
            a = self.env.sampleAction()
            self.env.step(a)
            r = self.env.reward
            s1 = self.env.getState()
            self.replay_memory.append([s0, a, r, s1])

            if self.env.done:
                self.env.reset()
            t += 1


if __name__ == "__main__":
    optimizer = RLOptimizer()
    optimizer.initReplayMemory()
    input("End")
