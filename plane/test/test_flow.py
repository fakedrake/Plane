import unittest
from plane.flow import Plane, Flow

def skip3(n):
    """
    Yield multiples of 3 of the number.
    """
    ret = 0
    while 1:
        ret += 3*n
        yield ret

def valve(s,d):
    # Here is how to avoid the valve of things
    if d > 100:
        return 0

    return float(min(s,d))/float(max(s,d))


class TestFlow(unittest.TestCase):
    def setUp(self):
        self.plane = Plane(neighbour_gen=skip3)
        self.flow = Flow(self.plane, valve)

    def test_pour(self):
        self.flow.pour(1, 3)
        expected = [(1, 3), (3, 1.0), (6, 0.5), (9, 0.6666666666666666), (12, 0.25), (15, 0.2), (18, 0.5), (21, 0.14285714285714285), (24, 0.125), (27, 0.6666666666666666), (30, 0.1), (33, 0.09090909090909091), (36, 0.25), (45, 0.13333333333333333), (54, 0.8333333333333333), (63, 0.09523809523809523), (72, 0.16666666666666666), (81, 1.0), (90, 0.1), (99, 0.030303030303030304)]
        result = list(self.flow.nodes.iteritems())

        for i in expected:
            self.assertIn(i,result)
