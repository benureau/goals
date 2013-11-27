"""A guide class balance motor and sensory exploration."""

import random
from collections import namedtuple
from pubsub import pub


from explorer import datalog
from explorer import motor
from explorer import effect

Action = namedtuple('Action', ['type', 'payload'])

import treedict

defaultcfg = treedict.TreeDict()

defaultcfg.motor.explorer  = motor.MotorBabble
defaultcfg.effect.explorer = effect.RandomExplorer
defaultcfg.effect.filter   = False

defaultcfg.guide.min_orderbabble   = 10
defaultcfg.guide.ratio_orderbabble = 0.05

class Guide(object):

    @classmethod
    def from_robot(cls, robot, cfg, goalexplorer = None, motorbabble = None):
        return cls(robot.m_feats, robot.s_feats, robot.m_bounds, cfg, goalexplorer = goalexplorer, motorbabble = motorbabble)

    def __init__(self, m_feats, s_feats, m_bounds, cfg, goalexplorer = None, motorbabble = None):
        """
        @param effect     a Motorbabble instance. It will be checked for compability.
        @param effect     a EffectExplorer instance. It will be checked for compability.
        """

        self.m_feats  = tuple(m_feats)
        self.s_feats  = tuple(s_feats)
        self.m_bounds = tuple(m_bounds)

        self.history   = []
        self.latest    = None # action proposed, but with no result yet

        self.datalog = datalog.DataLog(self)

        self.cfg = cfg
        self.cfg.update(defaultcfg, overwrite = False, protect_structure = True)

        if motorbabble is not None:
            self.babble = motorbabble
        else:
            self.babble = cfg.motor.explorer(self.m_feats, self.m_bounds, self.cfg)

        if goalexplorer is not None:
            self.goalexplorer = goalexplorer
        else:
            self.goalexplorer = cfg.effect.explorer(self.s_feats, self.cfg)
            if self.cfg.effect.filter:
                self.goalexplorer = effect.EffectFilter(self.goalexplorer, self.cfg.effect.filtered_values)

        self.t = 0 # number of actions

    def next_action(self):
        """The core of the guiding"""

        if not self.babble.finished or len(self.goalexplorer) < self.cfg.guide.min_orderbabble:
            babbling = self.babble.babble(self.t)
            action = Action(type = 'order', payload = babbling)
            path = 0
        else:
            if random.random() < self.cfg.guide.ratio_orderbabble:
                babbling = self.babble.babble(self.t)
                action = Action(type = 'order', payload = babbling)
                path = 1
            else:
                goal = self.goalexplorer.next_goal()
                if goal is None:
                    babbling = self.babble.babble(self.t)
                    action = Action(type = 'order', payload = babbling)
                    path = 2
                else:
                    action = Action(type = 'goal', payload = goal)
                    path = 3

        pub.sendMessage('guide.next_action', guide = self, action = action, path = path)
        self.latest = action
        return action

    def feedback(self, action, result):
        """
        @param action  the action followed that produced result
        @param result  the result, as a pair (order, effect)
        """
        self.t += 1
        pub.sendMessage('guide.feedback', guide = self, action = action, result = result)

        if action != self.latest:
            print('warning: the returned action {} is not the last one, {}'.format(action, self.latest))
        self.history.append((action, result))

        order, prediction, effect  = result
        self.babble.add_order(order, effect = effect)

        if action.type == 'order':
            self.goalexplorer.add_effect(effect, prediction = prediction)
        elif action.type == 'goal':
            self.goalexplorer.add_effect(effect, goal = action.payload, prediction = prediction)
        else:
            raise ValueError('Action type {} not recognized'.format(action.type))
