# Copyright 2017 reinforce.io. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import unittest

import numpy as np
from six.moves import xrange

from tensorforce import Configuration
from tensorforce.agents import PPOAgent
from tensorforce.core.networks import layered_network_builder
from tensorforce.execution import Runner
from tensorforce.contrib.openai_gym import OpenAIGym


class TestQuickstartExample(unittest.TestCase):

    def test_example(self):
        passed = 0

        for _ in xrange(3):
            # Create an OpenAIgym environment
            env = OpenAIGym('CartPole-v0')

            # Create a Trust Region Policy Optimization agent
            agent = PPOAgent(config=Configuration(
                log_level='info',
                batch_size=256,

                memory=dict(
                    type='prioritized_replay',
                ),
                update_frequency=256,
                first_update=512,

                learning_rate=0.0001,
                optimizer_batch_size=64,
                normalize_rewards=False,
                gae_rewards=False,
                baseline=dict(
                    type="mlp",
                    sizes=[32, 32],
                    epochs=1,
                    update_batch_size=64,
                    learning_rate=0.001
                ),
                states=env.states,
                actions=env.actions,
                network=layered_network_builder([
                    dict(type='dense', size=32, activation='tanh'),
                    dict(type='dense', size=32, activation='tanh')
                ])
            ))
            runner = Runner(agent=agent, environment=env)

            def episode_finished(r):
                # Test if mean reward over 50 should ensure that learning took off
                avg_reward = np.mean(r.episode_rewards[-50:])
                return r.episode < 100 or avg_reward < 50.0

            runner.run(episodes=2000, max_timesteps=200, episode_finished=episode_finished)

            if runner.episode < 2000:
                passed += 1

        print('Quick start example passed = {}'.format(passed))
        self.assertTrue(passed >= 2)
