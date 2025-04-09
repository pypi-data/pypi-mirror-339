import sys
from .Parse import IDP

from .Run import model_check, model_expand, model_propagate, execute, decision_table
from .Theory import Propagation, Theory
from .Assignments import Status, Assignment, Assignments

from z3 import z3

z3.Z3_DEBUG = False

# For some theories with large structures, we need more recursion depth to
# handle the grounding process. The max recursion depth is machine-specific,
# but if we set a value that is too high we will encounter an error anyway.
# Hence, we pick a ridiculously large number.
sys.setrecursionlimit(
    15000
)  # https://docs.python.org/3/library/sys.html#sys.setrecursionlimit
