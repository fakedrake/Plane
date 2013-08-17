"""
Any flow should be able to work with any plane if we are talking
about the same type.
"""

class BFSSeparator(object):
    """
    This is a placeholder to separate in the bfs queue the different
    levels. This could be replaced by a simple None but I find it is
    more readable this way.
    """

    def __init__(self, depth):
        self.depth = depth

class PlaneBFS(object):
    """
    A plane abstraction to feed me visible nodes without asking many
    questions. This is also a callibrator. A stateful machine. Each
    pour has a different bfs.
    """


    def __init__(self, plane, max_iterations=10, max_depth=3):
        """
        Given a plane and a reference to the contents..
        """
        self.plane = plane
        self.iterations = 0
        self.parents = [BFSSeparator(0)]
        self.active = False
        self.parent_it = None
        self.max_iterations = max_iterations
        self.max_depth = max_depth
        self.depth = 0

    def extend_visibility(self, node):
        """
        Extend visibility to node, that is queue it's first order neighbors.
        """
        self.parents.append(node)

    def skip(self):
        """
        Skip if we are out of iterations.
        """

        return self.iterations > self.max_iterations

    def __nonzero__(self):
        return (self.active or bool(self.parents)) \
            and self.depth < self.max_depth

    def pop(self, force_skip=False):
        """
        Pop a node if it is not insignificant and respecting the maximum
        per level iterations. This does not do depth first search, it
        iterates over the visible area. You need to
        `extend_visibility'. Force_skip will stop looking into the
        current parent node.
        """

        self.active = True

        if self.skip() or force_skip or self.parent_it is None:
            if not self.parents or self.depth >= self.max_depth:
                self.active = False
                return None

            self.iterations = 0
            self.parent = self.parents.pop(0)

            # When we encounter a level separator push a new one
            if type(self.parent) is BFSSeparator:
                self.parents.append(BFSSeparator(depth=self.depth+1))
                self.depth = self.parent.depth
                return self.pop(force_skip=True)

            self.parent_it = self.plane.neighbours(self.parent)

        try:
            ret = next(self.parent_it)
            self.iterations += 1
            return ret
        except StopIteration:
            return self.pop(force_skip=True)



class Flow(object):
    """
    Flow through the abstract graph to highlight the closeness of
    concepts.
    """

    def __init__(self, plane, valve, node_type=None, min_content=0.1, bfs_class=PlaneBFS, default_content=0, predicate=None):
        """
        Arguments:

        - Valve: callable with 2 argments that retusrs how much flow
          is allowed 0-1.

        - Node_type: the class of the nodes that go into the
          valve. This may be None but best provide it

        - min_content: minimum content that is visible

        - bfs_class: PlaneBFS is quite abstract but you always may
          need something strange.
        """

        self.valve = valve
        self.node_type = node_type
        self.plane = plane
        self.min_content = min_content
        self.bfs_class = bfs_class
        self.default_content = default_content
        self.predicate = predicate

        self.nodes = dict()     # use d.get(key, default)


    def pour(self, node, content):
        """
        Pour through a node with original content. We may want to avoid
        the way we came. For that provide the from. If no content is
        provided tha current node content is assumed.

        There will be nodes that contain no notable flow. These are
        saved but are not recursed.
        """
        ncontent = lambda x: self.nodes.get(x, self.default_content)

        if node not in self.nodes:
            self.nodes[node] = content

        bfs = self.bfs_class(self.plane)
        bfs.extend_visibility(node)

        while bfs:
            dest = bfs.pop()
            if dest is None:
                continue

            source = bfs.parent

            dest_cont = ncontent(dest) + self.valve(source, dest) * ncontent(source)

            self.nodes[dest] = dest_cont

            # If dest_cont is trivial dont go down that path
            if dest_cont > self.min_content:
                bfs.extend_visibility(dest)


class Plane(object):
    """
    An abstract place where all our objects are. You look into it for
    the objects.
    """
    def __init__(self, neighbour_gen):
        self.neighbours = neighbour_gen


def flowFactory():

    def skip3(n):
        """
        Yield multiples of 3 of the number.
        """
        ret = n
        while 1:
            ret += 3*n
            yield ret

    def valve(s,d):
        return min(s,d)/max(s,d)

    plane = Plane(neighbour_gen=skip3)
    flow = Flow(plane, valve)
    bfs = PlaneBFS(plane)
    bfs.extend_visibility(10)
    return bfs
