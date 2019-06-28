from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from rasa_core.featurizers import (MaxHistoryTrackerFeaturizer,
                                   BinarySingleStateFeaturizer)

featurizer = MaxHistoryTrackerFeaturizer(BinarySingleStateFeaturizer(),
                                         max_history=5)

from rasa_core.policies import FallbackPolicy, KerasPolicy, MemoizationPolicy
from rasa_core.agent import Agent
fallback = FallbackPolicy(fallback_action_name="utter_error_scope_message",
                        core_threshold=0.5,
                        nlu_threshold=0.8)

from rasa_core import config as policy_config
policies = policy_config.load("policies.yml")


agent = Agent("subset_flightdomain.yml", policies=policies)
training_data = agent.load_data('stories.md')
agent.train(training_data)

agent.persist('models/dialogue_subset')
