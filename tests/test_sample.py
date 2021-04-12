# content of test_sample.py
def bowler_extras(self):
    """Output the bowlers extras."""
    extras = self.wides + self.no_balls
    return str('{0}'.format(extras))


def economy(runs, overs):
    """Workout the economy."""
    econ = float(runs) / float(overs)
    return format(econ, '.2f')


def test_answer1():
    assert economy(4, 2) == '2.00'
