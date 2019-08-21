import argparse as arg
from collections import namedtuple
from enum import Enum, auto
from itertools import islice, dropwhile
from functools import wraps
import re

import sympy as sp
from sympy.abc import v


parser = arg.ArgumentParser(
    description="Produce the dotfile and probability equation for a tree of given size.")
parser.add_argument(
    "n", type=int, help="The number of nodes already in the map when inserting.")
args = parser.parse_args()
N = args.n


def debug(f):
    @wraps(f)
    def g(*args, **kwargs):
        res = f(*args, **kwargs)
        print(res)
        return res
    return g


class ColType(Enum):
    Collision = auto()
    NoCollision = auto()


Pair = namedtuple("Pair", ["col", "no_col"])


class Node():
    collisions = 0
    no_collisions = 0

    """Node in the tree
    Attributes:
        ctype :: ColType : Collision type of node
        n :: int : "level" of node - how many elements the hashmap already contains when this is added
        parent :: Node : whatever node is one level up in the tree
        children :: Pair : The nodes below this one
    """

    def __init__(self, ctype, n, parent=None):
        if ctype == ColType.Collision:
            self.id = self.__class__.collisions
            self.__class__.collisions += 1
        else:
            self.id = self.__class__.no_collisions
            self.__class__.no_collisions += 1
        self.ctype = ctype
        self.n = n
        self.parent = parent
        self.children = None

    def __str__(self):
        if self.ctype == ColType.Collision:
            return f"c{self.id}"
        else:
            return f"nc{self.id}"
    __repr__ = __str__

    @property
    def k(self):
        """The value k in the terms (v-k)/v and k/v"""
        if self.parent is None:
            return 1
        else:
            if self.parent.ctype == ColType.Collision or self.parent.parent is None:
                return self.parent.k
            else:
                return self.parent.k + 1

    @property
    def term(self):
        if self.parent is None:
            return 1
        elif self.ctype == ColType.Collision:
            return self.k / v
        else:
            return (v - self.k) / v

    @property
    def probability(self):
        if self.parent is None:
            return self.term
        else:
            return self.term * self.parent.probability

    def levelorder(self):
        yield self
        if self.children is not None:
            for (l, r) in zip(*map(Node.levelorder, self.children)):
                yield l
                yield r

    def rev_levelorder(self):
        """Traverse in levelorder but start with the nocollision child"""
        yield self
        if self.children is not None:
            for (l, r) in zip(*map(Node.rev_levelorder, self.children)):
                yield r
                yield l


root = Node(ColType.NoCollision, 0)
Node.collisions += 1

cur_nodes = [root]
for n in range(1, N+1):
    new_cur = []
    for old in cur_nodes:
        col = Node(ColType.Collision, n, old)
        no_col = Node(ColType.NoCollision, n, old)
        old.children = Pair(col, no_col)
        new_cur.extend([col, no_col])
    cur_nodes = new_cur


def to_dot(root):
    """Generate a dot file from the root downwards"""
    buf = ["""
digraph Program {
    rankdir = BT
"""]

    for node in root.rev_levelorder():
        if node.ctype == ColType.Collision:
            buf.append(f'    {node}[label="c"]')
        else:
            buf.append(f'    {node}[label="nc"]')

    buf.append("\n\n")

    for node in islice(root.levelorder(), 1, None):
        buf.append(f'    {node.parent}->{node} [label="{node.term}"]')

    buf.append("}\n")
    return buf


buf = to_dot(root)

with open("out.dot", "w") as f:
    f.write("\n".join(buf))

# find equation
last_cols = filter(lambda n: n.ctype == ColType.Collision,
                   dropwhile(lambda n: n.n != N, root.levelorder()))
collision_p = 0
for node in last_cols:  # both sum and reduce fail here - no idea why.
    collision_p += node.probability

eq = collision_p


def to_wolfram(s):
    """Convert a python string to the wolfram alpha equivalent string"""
    return s.replace("**", "^").replace("[", "(").replace("]", ")")


def to_latex(s):
    """Convert a python string to a equivalent latex code"""
    def fractionizer(
        m): return f"\\frac{'{'}{m.group(1)}{'}{'}{m.group(2)}{'}'}"
    return re.sub(r"(\([^\/\(\)]*\)) *\/ *([^\/\(\)]*)", fractionizer,
                  re.sub(r"(\([^\/\(\)]*\)) *\/ *(\([^\/\(\)]*\))",
                         fractionizer, s.replace("**", "^").replace("*", " \cdot ").replace("[", "(").replace("]", ")")))


print()
sp.pprint(eq)
simp_eq = sp.simplify(eq)

print()
sp.pprint(simp_eq)

print()
equation = str(simp_eq)
print(f"Python string: {equation}")
print(f"Wolfram alpha code: {to_wolfram(equation)}")
print(f"Latex code: {to_latex(equation)}")
