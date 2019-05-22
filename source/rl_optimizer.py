#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from tetris_RLenv import *
from time import *
from random import *
# import tensorflow as tf


class RLOptimizer:

    def __init__(self, width=10, height=22, base_blocks_bag=CLASSIC_BLOCK_BAG,
                 update_rate=0.1, learning_rate=0.1,
                 exploration_rate_min=0, exploration_rate_max=1,
                 replay_memory_size=5000, batch_size=10,
                 update_period=10, max_epochs=10):
        self.width = width
        self.height = height

        self.base_blocks_bag = base_blocks_bag

        self.update_rate = update_rate
        self.learning_rate = learning_rate
        self.exploration_rate_min = exploration_rate_min
        self.exploration_rate_max = exploration_rate_max
        self.replay_memory_size = replay_memory_size
        self.batch_size = batch_size
        self.update_period = update_period
        self.max_epochs = max_epochs

        self.env = TetrisEnv(width=self.width, height=self.height,
                             base_blocks_bag=self.base_blocks_bag)

    def initReplayMemory(self):
        self.replay_memory = []
        t = 0
        self.env.reset()
        while t < self.replay_memory_size:
            self.env.render()
            sleep(1)

            s0 = self.env.getState()
            a = self.env.sampleAction()
            self.env.step(a)
            r = self.env.reward
            s1 = self.env.getState()
            self.replay_memory.append([s0, a, r, s1])

            if self.env.done:
                self.env.reset()
            t += 1

    def addToReplayMemory(self, s0, a, r, s1):
        del self.replay_memory[0]
        self.replay_memory.append([s0, a, r, s1])

    def sampleFromReplayMemory(self):
        return sample(self.replay_memory, self.batch_size)


if __name__ == "__main__":
    optimizer = RLOptimizer(
        width=3, height=3, base_blocks_bag=DOMINO_BLOCK_BAG,
        replay_memory_size=100)
    optimizer.initReplayMemory()
    print(optimizer.replay_memory)
    input("End")
