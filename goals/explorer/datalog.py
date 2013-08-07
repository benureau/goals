from pubsub import pub


class DataLog(object):

    def __init__(self, guide):
        self.guide = guide

        pub.subscribe(self.feedback, 'guide.feedback')
        pub.subscribe(self.next_action, 'guide.next_action')

        self.orders, self.goals, self.predictions, self.effects = [], [], [], []
        self.paths = 4*[0]

    @property
    def order_count(self):
        return self.paths[0] + self.paths[1] + self.paths[2]

    @property
    def goal_count(self):
        return self.paths[3]

    def feedback(self, guide, action, result):
        if guide == self.guide:
            order, prediction, effect = result
            goal = action.payload if action.type == 'goal' else None
            self.orders.append(self._tupleize(order))
            self.goals.append(self._tupleize(goal))
            self.effects.append(self._tupleize(effect))
            self.predictions.append(self._tupleize(prediction))

    def next_action(self, guide, action, path):
        if guide == self.guide:
            self.paths[path] += 1

    def _tupleize(self, t):
        if t is not None and type(t) != tuple:
            return tuple(t)
        else:
            return t

    def manual_feedback(self, effect, goal = None, prediction = None):
        self.effects.append(self._tupleize(effect))
        self.goals.append(self._tupleize(goal))
        self.predictions.append(self._tupleize(prediction))

    def package_history(self):
        return tuple((o, g, p, e) for o, g, p, e in
                     zip(self.orders, self.goals, self.predictions, self.effects))
