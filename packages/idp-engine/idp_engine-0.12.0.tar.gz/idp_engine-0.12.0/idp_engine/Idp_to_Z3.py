# Copyright 2019-2023 Ingmar Dasseville, Pierre Carbonnelle
#
# This file is part of IDP-Z3.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""

Translates AST tree to Z3

TODO: vocabulary

"""

from __future__ import annotations

from copy import copy
from fractions import Fraction
from typing import TYPE_CHECKING, List, Callable
from z3 import (
    Z3Exception,
    Datatype,
    DatatypeRef,
    ExprRef,
    Function,
    RecFunction,
    Const,
    FreshConst,
    BoolSort,
    IntSort,
    RealSort,
    Or,
    Not,
    And,
    ForAll,
    Exists,
    Sum,
    If,
    BoolVal,
    RatVal,
    IntVal,
    RecAddDefinition,
    AtMost,
    AtLeast,
    Distinct
)

import idp_engine.Parse as Parse
import idp_engine.Expression as Expr
from .utils import (
    BOOL,
    INT,
    REAL,
    DATE,
    GOAL_SYMBOL,
    RELEVANT,
    RESERVED_SYMBOLS,
    Semantics,
    AggType,
)
from math import floor, ceil

if TYPE_CHECKING:
    from .Theory import Theory


# class TypeDeclaration  ###########################################################


def translate_typedeclaration(self, problem: Theory) -> ExprRef:
    out = problem.z3.get(self.name, None)
    if out is None:
        if self.name == BOOL:
            out = BoolSort(problem.ctx)
            problem.z3[self.constructors[0].name] = BoolVal(True, problem.ctx)
            problem.z3[self.constructors[1].name] = BoolVal(False, problem.ctx)
            self.constructors[0].py_value = True
            self.constructors[1].py_value = False
        elif self.name == INT:
            out = IntSort(problem.ctx)
        elif self.name == REAL:
            out = RealSort(problem.ctx)
        elif self.name == DATE:
            out = IntSort(problem.ctx)
        elif self.super_set:
            out = self.super_sets[0].translate(problem)
        elif self.constructors:
            sort = Datatype(self.name, ctx=problem.ctx)
            for c in self.constructors:
                sort.declare(
                    c.name,
                    *[
                        (
                            a.decl.name,
                            a.decl.codomain.translate(problem)
                            if a.decl.codomain.name != self.name
                            else sort,
                        )  # recursive data type
                        for a in c.args
                    ],
                )
            out = sort.create()

            for c in self.constructors:
                c.py_value = out.__dict__[c.name]
                problem.z3[c.name] = c.py_value
                if c.tester:
                    problem.z3[c.tester.name] = out.__dict__[f"is_{c.name}"]
                for a in c.args:
                    problem.z3[a.decl.name] = out.__dict__[a.accessor]
                if not c.domains:
                    self.map[str(c)] = Expr.UnappliedSymbol.construct(c)
                elif c.range:
                    for e in c.range:
                        self.map[str(e)] = e
        else:  # empty type --> don't care
            out = IntSort(problem.ctx)
        problem.z3[self.name] = out
    return out


# class SymbolDeclaration  ###########################################################


def translate_symboldeclaration(self, problem: Theory) -> ExprRef:
    out = problem.z3.get(self.name, None)
    if out is None:
        recursive = any(
            self in def_.clarks
            for _, def_ in problem.def_constraints.keys()
            if def_.mode == Semantics.RECDATA
        )
        if self.arity == 0:
            out = Const(self.name, self.codomain.root_set[0].decl.translate(problem))
        else:
            types = [x.root_set[0].translate(problem) for x in self.sorts] + [
                self.sort_.root_set[0].translate(problem)
            ]
            out = (
                Function(self.name, types)
                if not recursive
                else RecFunction(self.name, types)
            )
        problem.z3[self.name] = out
    return out


# class TupleIDP  ###########################################################


def translate_tupleidp(self, problem: Theory) -> ExprRef:
    return [arg.translate(problem) for arg in self.args]


# class Constructor  ###########################################################


def translate_constructor(self, problem: Theory) -> ExprRef:
    return problem.z3[self.name]


# class Expression  ###########################################################


def translate_expression(self, problem: Theory, vars={}) -> ExprRef:
    """Converts the syntax tree to a Z3 expression, with lookup in problem.z3

    Args:
        problem (Theory): holds the context for the translation (e.g. a cache of translations).

        vars (dict[id, ExprRef], optional): mapping from Variable's id to Z3 translation.
            Filled in by AQuantifier.  Defaults to {}.

    Returns:
        ExprRef: Z3 expression
    """
    out = problem.z3.get(self.str, None)
    if out is None:
        out = self.translate1(problem, vars)
        if not vars:
            problem.z3[self.str] = out
    return out


def reified_expression(self, problem: Theory) -> DatatypeRef:
    str = b"*" + self.code.encode()
    out = problem.z3.get(str, None)
    if out is None:
        out = Const(str, BoolSort(problem.ctx))
        problem.z3[str] = out
    return out


# class SetName  ###############################################################


def translate_setname(self, problem: Theory, vars={}) -> ExprRef:
    if self == Expr.BOOL_SETNAME:
        return BoolSort(problem.ctx)
    elif self == Expr.INT_SETNAME:
        return IntSort(problem.ctx)
    elif self == Expr.REAL_SETNAME:
        return RealSort(problem.ctx)
    else:
        return self.decl.translate(
            problem,
        )


# Class AIfExpr  ###############################################################


def translate1_aifexpr(self, problem: Theory, vars={}) -> ExprRef:
    """Converts the syntax tree to a Z3 expression, without lookup in problem.z3

    A lookup is wasteful when `self` is a subformula of a formula that is not in `problem.z3`.

    Args:
        problem (Theory): holds the context for the translation (e.g. a cache of translations).

        vars (dict[id, ExprRef], optional): mapping from Variable's id to Z3 translation.
            Filled in by AQuantifier.  Defaults to {}.

    Returns:
        ExprRef: Z3 expression
    """
    return If(
        self.sub_exprs[Expr.AIfExpr.IF].translate(problem, vars),
        self.sub_exprs[Expr.AIfExpr.THEN].translate(problem, vars),
        self.sub_exprs[Expr.AIfExpr.ELSE].translate(problem, vars),
    )


# Class Quantee  ######################################################


def translate_quantee(self, problem: Theory, vars={}) -> ExprRef:
    out = {}
    for vars in self.vars:
        for v in vars:
            translated = FreshConst(v.type.root_set[0].decl.translate(problem))
            out[v.str] = translated
    return out


# Class AQuantification  ######################################################


def translate1_aquantification(self, problem: Theory, vars={}) -> ExprRef:
    local_vars = {}
    for q in self.quantees:
        local_vars.update(q.translate(problem, vars))
    all_vars = copy(vars)
    all_vars.update(local_vars)
    forms = [f.translate(problem, all_vars) for f in self.sub_exprs]

    if self.q == "∀":
        forms = (
            And(forms)
            if 1 < len(forms)
            else forms[0]
            if 1 == len(forms)
            else BoolVal(True, problem.ctx)
        )
        if local_vars:
            forms = ForAll(list(local_vars.values()), forms)
    else:
        forms = (
            Or(forms)
            if 1 < len(forms)
            else forms[0]
            if 1 == len(forms)
            else BoolVal(False, problem.ctx)
        )
        if local_vars:
            forms = Exists(list(local_vars.values()), forms)
    return forms


# Class Operator  #######################################################

Operator_MAP: dict[str, Callable] = {
    "∧": lambda x, y: And(x, y),
    "∨": lambda x, y: Or(x, y),
    "⇒": lambda x, y: Or(Not(x), y),
    "⇐": lambda x, y: Or(x, Not(y)),
    "⇔": lambda x, y: x == y,
    "+": lambda x, y: x + y,
    "-": lambda x, y: x - y,
    "⨯": lambda x, y: x * y,
    "/": lambda x, y: x / y,
    "%": lambda x, y: x % y,
    "^": lambda x, y: x**y,
    "=": lambda x, y: x == y,
    "<": lambda x, y: x < y,
    ">": lambda x, y: x > y,
    "≤": lambda x, y: x <= y,
    "≥": lambda x, y: x >= y,
    "≠": lambda x, y: x != y,
}


def translate1_operator(self, problem: Theory, vars={}) -> ExprRef:
    out = self.sub_exprs[0].translate(problem, vars)

    for i in range(1, len(self.sub_exprs)):
        function = Expr.Operator.MAP[self.operator[i - 1]]
        try:
            out = function(out, self.sub_exprs[i].translate(problem, vars))
        except Exception as e:
            raise e
    return out


# Class ADisjunction  #######################################################


def translate1_adisjunction(self, problem: Theory, vars={}) -> ExprRef:
    if len(self.sub_exprs) == 1:
        out = self.sub_exprs[0].translate(problem, vars)
    else:
        out = Or([e.translate(problem, vars) for e in self.sub_exprs])
    return out


# Class AConjunction  #######################################################


def translate1_aconjunction(self, problem: Theory, vars={}) -> ExprRef:
    if len(self.sub_exprs) == 1:
        out = self.sub_exprs[0].translate(problem, vars)
    else:
        out = And([e.translate(problem, vars) for e in self.sub_exprs])
    return out


# Class AComparison  #######################################################

Comparison_invert = {"=": "=", "≠": "≠", "<": ">", "≤": "≥", ">": "<", "≥": "≤"}


def translate_acomparison_optimum(
    self,
    problem: Theory,
    lhs: Expr.Expression,
    op: Expr.Expression,
    rhs: Expr.Expression,
    vars={},
) -> ExprRef:
    """
    Optimized translation method for _very_ specific circumstances in which one
    child is a count and the other child is a literal int (or a symbol
    interpreted as one). This allows us to use Z3's AtLeast and AtMost
    (https://z3prover.github.io/api/html/namespacez3py.html#a0369f15ecdb913e47fc7bb645fcfcf08)
    instead of converting the aggregate to a sum of ite's.
    """
    # Agg/literal can either be left-right or right-left children, this
    # ensures we grab the right one. In the case of right-left, we also invert
    # the operator so we can assume it's always left-right.
    (agg, operator, num) = (
        (lhs, op, rhs)
        if isinstance(lhs, Expr.AAggregate)
        else (rhs, Comparison_invert[op], lhs)
    )
    sub_exprs = [x.sub_exprs[0].translate(problem, vars) for x in agg.sub_exprs]

    if num.is_int():
        num = int(num.number)  # TODO: should Number have method for this?
    else:
        num = float(num.number)  # We round these later, depending on operator

    out = None
    # TODO: replace by match statement once p3.9 is dropped
    if operator == ">":
        out = AtLeast(*sub_exprs, ceil(num) + 1)
    elif operator == "≥":
        out = AtLeast(*sub_exprs, ceil(num))
    elif operator == "<":
        out = AtMost(*sub_exprs, floor(num) - 1)
    elif operator == "≤":
        out = AtMost(*sub_exprs, floor(num))
    elif operator == "=":
        out = And(AtMost(*sub_exprs, floor(num)), AtLeast(*sub_exprs, ceil(num)))
    else:
        raise Exception("Internal error")
    return out


def at_most_at_least_possible(
    lhs: Expr.Expression, operator: str, rhs: Expr.Expression
):
    """
    Verifies whether an optimized Z3 encoding using "AtMost" or "AtLeast" is
    possible for two children of an AComparison. This is the case when one
    child is a cardinality, while the other child is a literal int.
    See: https://gitlab.com/krr/IDP-Z3/-/issues/362
    """
    return (
        operator in "≤<>≥="
        and any(
            (
                (isinstance(x, Expr.AAggregate) and x.aggtype == AggType.CARD)
                for x in (lhs, rhs)
            )
        )
        and any((isinstance(x, Expr.Number) for x in (lhs, rhs)))
    )


def translate1_acomparison(self: Expr.AComparison, problem: Theory, vars={}) -> ExprRef:
    assert not any(x == "≠" for x in self.operator), f"Internal error: {self}"

    out: List[ExprRef] = []
    # AComparison can have multiple children in the case of chained
    # comparisons. This loop iterates over each subsequent pairs of children
    # (i.e., 0-1, 1-2, ...) and translates them accordingly, to group them in a
    # big conjunction.
    for lhs, op, rhs in zip(self.sub_exprs, self.operator, self.sub_exprs[1:]):
        # Check if an optimized translation is possible.
        if at_most_at_least_possible(lhs, op, rhs):
            out.append(self.translate_acomparison_optimum(problem, lhs, op, rhs, vars))
        else:
            x = lhs.translate(problem, vars)
            assert x is not None, f"Internal error: {x} is None"
            function = Expr.Operator.MAP[op]
            y = rhs.translate(problem, vars)
            assert y is not None, f"Internal error: {y} is None"
            try:
                out.append(function(x, y))
            except Z3Exception as e:
                self.check(False, "{}:{}{}{}".format(str(e), str(x), op, str(y)))
    if 1 < len(out):
        return And(out)
    else:
        return out[0]


# Class AUnary  #######################################################

AUnary_MAP = {"-": lambda x: 0 - x, "¬": lambda x: Not(x)}


def translate1_aunary(self, problem: Theory, vars={}) -> ExprRef:
    out = self.sub_exprs[0].translate(problem, vars)
    function = Expr.AUnary.MAP[self.operator]
    try:
        return function(out)
    except:
        self.check(False, f"Incorrect syntax {self}")


# Class AAggregate  #######################################################


def translate1_aaggregate(self, problem: Theory, vars={}) -> ExprRef:
    assert self.annotated and not self.quantees, f"Cannot expand {self.code}"
    if self.aggtype in [AggType.CARD, AggType.SUM]:
        return Sum([f.translate(problem, vars) for f in self.sub_exprs])
    elif self.aggtype == AggType.DISTINCT:
        return Distinct([f.translate(problem, vars) for f in self.sub_exprs])
    else:
        assert True, "Unreachable code, please report"


# Class AExtAggregate  #######################################################


def translate1_extaggregate(self, problem: Theory, vars={}) -> ExprRef:
    assert self.annotated, "Internal error"
    # TODO: Replace by match once support for p3.9 is dropped
    if self.aggtype == AggType.CARD:
        return len(self.sub_exprs)
    elif self.aggtype == AggType.SUM:
        return Sum([f.translate(problem, vars) for f in self.sub_exprs])
    elif self.aggtype == AggType.DISTINCT:
        return Distinct([f.translate(problem, vars) for f in self.sub_exprs])
    else:
        assert True, "Unreachable code, please report"


# Class AppliedSymbol  #######################################################


def translate1_appliedsymbol(self, problem: Theory, vars={}) -> ExprRef:
    if self.as_disjunction:
        return self.as_disjunction.translate(problem, vars)
    self.check(
        self.decl,
        f"Unknown symbol: {self.symbol}.\n"
        f"Possible fix: introduce a variable "
        f"(e.g., !x in Concept: x=... => $(x)(..))",
    )
    self.check(not self.is_enumerated, f"{self.decl.name} is not enumerated")
    self.check(not self.in_enumeration, f"Internal error")
    if self.decl.name in [GOAL_SYMBOL, RELEVANT]:
        return Expr.TRUE.translate(problem, vars)
    if self.decl.name == "abs":
        arg = self.sub_exprs[0].translate(problem, vars)
        return If(arg >= 0, arg, -arg, problem.ctx)
    if self.decl.name in [BOOL, INT, REAL, DATE]:
        return problem.z3["true"]  # already type-checked
    self.check(
        len(self.sub_exprs) == self.decl.arity,
        f"Incorrect number of arguments for {self}",
    )
    if len(self.sub_exprs) == 0:
        return self.decl.translate(problem)
    elif type(self.symbol.decl) == Parse.TypeDeclaration:
        return (
            self.sub_exprs[0]
            .type.has_element(self.sub_exprs[0], problem.extensions)
            .translate(problem)
        )
    else:
        arg = [x.translate(problem, vars) for x in self.sub_exprs]
        # assert  all(a != None for a in arg)
        try:
            return (self.decl.translate(problem))(arg)
        except Exception as e:
            if self.original.code.startswith("$"):
                msg = f"$()() expression is not properly guarded: {self.original.code}"
            else:
                msg = f"Incorrect symbol application: {self}"
            self.check(False, f"{msg} ({str(e)})")


def reified_appliedsymbol(self, problem: Theory, vars={}) -> DatatypeRef:
    if self.is_reified():
        str = b"*" + self.code.encode()
        out = problem.z3.get(str, None)
        if out is None:
            sort = (
                BoolSort(problem.ctx)
                if self.in_enumeration or self.is_enumerated
                else self.decl.codomain.root_set[0].decl.translate(problem)
            )
            out = Const(str, sort)
            problem.z3[str] = out
    else:
        out = self.translate(problem)
    return out


# Class UnappliedSymbol  #######################################################


def translate1_unappliedsymbol(self, problem: Theory, vars={}) -> ExprRef:
    return problem.z3[self.name]


# Class Variable  #######################################################


def translate_variable(self, problem: Theory, vars={}) -> ExprRef:
    return vars[self.str]


# Class Number  #######################################################


def translate_number(self, problem: Theory, vars={}) -> ExprRef:
    out = problem.z3.get(self.str, None)
    if out is None:
        out = (
            RatVal(self.py_value.numerator, self.py_value.denominator, problem.ctx)
            if isinstance(self.py_value, Fraction)
            else IntVal(self.py_value, problem.ctx)
        )
        problem.z3[self.str] = out
    return out


# Class Date  #######################################################


def translate_date(self, problem: Theory, vars={}) -> ExprRef:
    out = problem.z3.get(self.str, None)
    if out is None:
        out = IntVal(self.py_value, problem.ctx)
        problem.z3[self.str] = self.py_value
    return out


# Class Brackets  #######################################################


def translate1_brackets(self, problem: Theory, vars={}) -> ExprRef:
    return self.sub_exprs[0].translate(problem, vars)


# Class RecDef  #######################################################


def translate1_recdef(self, problem: Theory, vars={}) -> ExprRef:
    local_vars = {}
    for v in self.vars:
        translated = FreshConst(v.type.root_set[0].decl.translate(problem))
        local_vars[v.str] = translated
    all_vars = copy(vars)
    all_vars.update(local_vars)
    decl = problem.declarations[self.name]
    func = decl.translate(problem)
    # add definition to context
    RecAddDefinition(
        func, list(local_vars.values()), self.sub_exprs[0].translate(problem, all_vars)
    )
    return Expr.TRUE.translate(problem)
