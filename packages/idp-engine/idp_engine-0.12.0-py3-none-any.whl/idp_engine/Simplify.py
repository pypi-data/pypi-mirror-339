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

Methods to simplify a logic expression.


"""

from __future__ import annotations

from copy import copy, deepcopy
import sys
from typing import List, Tuple, Optional, Generator, Union

import idp_engine.Expression as Expr
import idp_engine.Parse as Parse
import idp_engine.Assignments as Ass
from .utils import ABS, AggType


# class Expression  ###########################################################


def _change_expression(
    self,
    sub_exprs: Optional[List[Expr.Expression]] = None,
    ops: Optional[List[str]] = None,
    value: Optional[Expr.Expression] = None,
    simpler: Optional[Expr.Expression] = None,
    co_constraint: Optional[Expr.Expression] = None,
):
    "change attributes of an expression, and resets derived attributes"

    if value:
        out = copy(value)
        out.annotations = self.annotations
        return out

    if simpler is not None:
        simpler.original = self.original
        simpler.is_type_constraint_for = self.is_type_constraint_for
        if isinstance(self, Expr.AppliedSymbol):
            simpler.in_head = self.in_head
        return simpler

    if sub_exprs is not None:
        self.sub_exprs = sub_exprs
    if ops is not None:
        self.operator = ops
    if co_constraint is not None:
        self.co_constraint = co_constraint

    # reset derived attributes
    self.str = sys.intern(str(self))

    return self


def update_exprs_expression(
    self: Expr.Expression, new_exprs: Generator[Expr.Expression, None, None]
) -> Expr.Expression:
    """change sub_exprs and simplify, while keeping relevant info."""
    #  default implementation, without simplification
    return self._change(sub_exprs=list(new_exprs))


def simplify1_expression(self: Expr.Expression) -> Expr.Expression:
    return self.update_exprs(iter(self.sub_exprs))


# Expr.simplify1 = simplify1


# for type checking
def as_set_condition_expression(
    self: Expr.Expression,
) -> Tuple[Optional[Expr.AppliedSymbol], Optional[bool], Optional[Parse.Enumeration]]:
    return (None, None, None)


# Class AIfExpr  ###############################################################


def update_exprs_aifexpr(
    self: Expr.AIfExpr, new_exprs: Generator[Expr.Expression, None, None]
) -> Expr.Expression:
    sub_exprs = list(new_exprs)
    if_, then_, else_ = sub_exprs[0], sub_exprs[1], sub_exprs[2]
    if if_.same_as(Expr.TRUE):
        return self._change(simpler=then_, sub_exprs=sub_exprs)
    elif if_.same_as(Expr.FALSE):
        return self._change(simpler=else_, sub_exprs=sub_exprs)
    else:
        if then_.same_as(else_):
            return self._change(simpler=then_, sub_exprs=sub_exprs)
        elif then_.same_as(Expr.TRUE):
            if else_.same_as(Expr.FALSE):
                return self._change(simpler=if_, sub_exprs=sub_exprs)
            else:
                return self._change(simpler=Expr.OR([if_, else_]), sub_exprs=sub_exprs)
        elif else_.same_as(Expr.TRUE):
            if then_.same_as(Expr.FALSE):
                return self._change(simpler=Expr.NOT(if_), sub_exprs=sub_exprs)
            else:
                return self._change(
                    simpler=Expr.OR([Expr.NOT(if_), then_]), sub_exprs=sub_exprs
                )
    return self._change(sub_exprs=sub_exprs)


# Class Quantee  #######################################################


# Class AQuantification  ######################################################


def update_exprs_aquantification(
    self: Expr.AQuantification, new_exprs: Generator[Expr.Expression, None, None]
) -> Union[Expr.AConjunction, Expr.ADisjunction]:
    if self.q == "∀":
        return Expr.AConjunction.update_exprs(self, new_exprs, replace=False)
    else:
        return Expr.ADisjunction.update_exprs(self, new_exprs, replace=False)


# Class AImplication  #######################################################


def update_exprs_aimplication(
    self: Expr.AImplication, new_exprs: Generator[Expr.Expression, None, None]
) -> Expr.Expression:
    exprs0 = next(new_exprs)
    simpler = None
    if exprs0.same_as(Expr.FALSE):  # (false => p) is true
        return self._change(value=Expr.TRUE)
    elif exprs0.same_as(Expr.TRUE):  # (true => p) is p
        exprs1 = next(new_exprs)
        simpler = exprs1
    else:
        exprs1 = next(new_exprs)
        if exprs1.same_as(Expr.TRUE):  # (p => true) is true
            return self._change(value=Expr.TRUE)
        elif exprs1.same_as(Expr.FALSE):  # (p => false) is ~p
            simpler = Expr.NOT(exprs0)
        elif exprs1.same_as(exprs0):  # (p => p) is true
            return self._change(value=Expr.TRUE)
    return self._change(simpler=simpler, sub_exprs=[exprs0, exprs1])


# Class AEquivalence  #######################################################


def update_exprs_aequivalence(
    self: Expr.AEquivalence, new_exprs: Generator[Expr.Expression, None, None]
) -> Expr.Expression:
    exprs = list(new_exprs)
    if len(exprs) == 1:
        return self._change(simpler=exprs[1], sub_exprs=exprs)
    for e in exprs:
        if e.same_as(Expr.TRUE):  # they must all be true
            return self._change(simpler=Expr.AND(exprs), sub_exprs=exprs)
        if e.same_as(Expr.FALSE):  # they must all be false
            return self._change(
                simpler=Expr.AND([Expr.NOT(e) for e in exprs]), sub_exprs=exprs
            )
    return self._change(sub_exprs=exprs)


# Class ADisjunction  #######################################################


def update_exprs_adisjunction(
    self: Expr.Expression,
    new_exprs: Generator[Expr.Expression, None, None],
    replace: bool = True,
) -> Expr.Expression:
    exprs = []
    simpler = None
    for expr in new_exprs:
        if expr.same_as(Expr.TRUE):
            return self._change(value=Expr.TRUE)
        if not expr.same_as(Expr.FALSE):
            exprs.append(expr)

    if len(exprs) == 0:  # all disjuncts are False
        return self._change(value=Expr.FALSE)
    elif replace and len(exprs) == 1:
        simpler = exprs[0]
    return self._change(simpler=simpler, sub_exprs=exprs)


# Class AConjunction  #######################################################


# same as ADisjunction, with Expr.TRUE and Expr.FALSE swapped
def update_exprs_aconjunction(
    self: Expr.Expression,
    new_exprs: Generator[Expr.Expression, None, None],
    replace: bool = True,
) -> Expr.Expression:
    exprs = []
    simpler = None
    for expr in new_exprs:
        if expr.same_as(Expr.FALSE):
            return self._change(value=Expr.FALSE)
        if not expr.same_as(Expr.TRUE):
            exprs.append(expr)

    if len(exprs) == 0:  # all conjuncts are True
        return self._change(value=Expr.TRUE)
    if replace and len(exprs) == 1:
        simpler = exprs[0]
    return self._change(simpler=simpler, sub_exprs=exprs)


# Class AComparison  #######################################################


def update_exprs_acomparison(
    self: Expr.AComparison, new_exprs: Generator[Expr.Expression, None, None]
) -> Expr.Expression:
    operands = list(new_exprs)

    if len(operands) == 2 and self.operator == ["="]:
        # a = a
        if operands[0].same_as(operands[1]):
            return self._change(value=Expr.TRUE)

        # (if c then a else b) = d  ->  (if c then a=d else b=d)
        if isinstance(operands[0], Expr.AIfExpr):
            then = Expr.EQUALS([operands[0].sub_exprs[1], operands[1]]).simplify1()
            else_ = Expr.EQUALS([operands[0].sub_exprs[2], operands[1]]).simplify1()
            new = Expr.IF(operands[0].sub_exprs[0], then, else_).simplify1()
            return self._change(simpler=new, sub_exprs=operands)

    acc = operands[0]
    assert len(self.operator) == len(operands[1:]), "Internal error"
    for op, expr in zip(self.operator, operands[1:]):
        if acc.is_value() and expr.is_value():
            if op in ["<", ">"] and acc.same_as(expr):
                return self._change(value=Expr.FALSE)
            if op == "=" and not acc.same_as(expr):
                return self._change(value=Expr.FALSE)
            if op == "≠":  # issue #246
                if acc.same_as(expr):
                    return self._change(value=Expr.FALSE)
            elif not (Expr.Operator.MAP[op])(acc.py_value, expr.py_value):
                return self._change(value=Expr.FALSE)
        acc = expr
    if all(e.is_value() for e in operands):
        return self._change(value=Expr.TRUE)
    return self._change(sub_exprs=operands)


def as_set_condition_acomparison(
    self: Expr.AComparison,
) -> Tuple[Optional[Expr.Expression], Optional[bool], Optional[Parse.Enumeration]]:
    return (
        (None, None, None)
        if not self.is_assignment()
        else (
            self.sub_exprs[0],
            True,
            Parse.Enumeration(
                parent=self, tuples=[Parse.TupleIDP(args=[self.sub_exprs[1]])]
            ),
        )
    )


#############################################################


def update_arith(
    self: Expr.Operator, operands: List[Expr.Expression]
) -> Expr.Expression:
    if all(e.is_value() for e in operands):
        self.check(
            all(hasattr(e, "py_value") for e in operands),
            f"Incorrect numeric type in {self}",
        )
        out = operands[0].py_value

        assert len(self.operator) == len(operands[1:]), "Internal error"
        for op, e in zip(self.operator, operands[1:]):
            function = Expr.Operator.MAP[op]

            if op == "/" and self.type == Expr.INT_SETNAME:  # integer division
                out //= e.py_value
            else:
                out = function(out, e.py_value)
        value = (
            Expr.Number(number=str(out))
            if operands[0].type != Expr.DATE_SETNAME
            else Expr.Date.make(out)
        )
        return value
    return self._change(sub_exprs=operands)


# Class ASumMinus  #######################################################


def update_exprs_asumminus(
    self: Expr.ASumMinus, new_exprs: Generator[Expr.Expression, None, None]
) -> Expr.Expression:
    return update_arith(self, list(new_exprs))


# Class AMultDiv  #######################################################


def update_exprs_amultdiv(
    self: Expr.AMultDiv, new_exprs: Generator[Expr.Expression, None, None]
) -> Expr.Expression:
    operands = list(new_exprs)
    if any(op == "%" for op in self.operator):  # special case !
        if len(operands) == 2 and all(e.is_value() for e in operands):
            out = operands[0].py_value % operands[1].py_value
            return Expr.Number(number=str(out))
        else:
            return self._change(sub_exprs=operands)
    return update_arith(self, operands)


# Class APower  #######################################################


def update_exprs_apower(
    self: Expr.APower, new_exprs: Generator[Expr.Expression, None, None]
) -> Expr.Expression:
    operands = list(new_exprs)
    if len(operands) == 2 and all(e.is_value() for e in operands):
        out = operands[0].py_value ** operands[1].py_value
        return Expr.Number(number=str(out))
    else:
        return self._change(sub_exprs=operands)


# Class AUnary  #######################################################


def update_exprs_aunary(
    self: Expr.AUnary, new_exprs: Generator[Expr.Expression, None, None]
) -> Expr.Expression:
    operand = list(new_exprs)[0]
    if self.operator == "¬":
        if operand.same_as(Expr.TRUE):
            return self._change(value=Expr.FALSE)
        if operand.same_as(Expr.FALSE):
            return self._change(value=Expr.TRUE)
    else:  # '-'
        if operand.is_value() and isinstance(operand, Expr.Number):
            return Expr.Number(number=f"{-operand.py_value}")
    return self._change(sub_exprs=[operand])


def as_set_condition_aunary(
    self: Expr.AUnary,
) -> Tuple[Optional[Expr.AppliedSymbol], Optional[bool], Optional[Parse.Enumeration]]:
    (x, y, z) = self.sub_exprs[0].as_set_condition()
    return (None, None, None) if x is None else (x, not y, z)


# Class AAggregate and AExtAggregate ######################################


def update_exprs_aaggregate_extaggregate(
    self: Expr.AAggregate | Expr.AExtAggregate,
    new_exprs: Generator[Expr.Expression, None, None],
) -> Expr.AAggregate | Expr.AExtAggregate | Expr.Number:
    operands = list(new_exprs)
    no_quantees = isinstance(self, Expr.AExtAggregate) or not self.quantees
    if self.annotated and no_quantees:
        # AAggregate can only be a sum or cardinality at this point,
        # while AExtAggregate can only be a sum.
        # All the other types have been transformed away during annotation.
        # See: Annotate.annotate_aaggrage and Annotate.annotate_extaggregate
        self.check(
            (
                isinstance(self, Expr.AAggregate)
                and self.aggtype in [AggType.SUM, AggType.CARD, AggType.DISTINCT]
            )
            or (isinstance(self, Expr.AExtAggregate) and self.aggtype in [AggType.SUM, AggType.DISTINCT]),
            "Internal error: please report",
        )

        # Simplify if all operands are known.
        if all(e.is_value() for e in operands):
            out = Expr.Number(number=str(sum(e.py_value for e in operands)))
            out.original = deepcopy(self)
            return out
    return self._change(sub_exprs=operands)


# Class AppliedSymbol  #######################################################


def update_exprs_appliedsymbol(
    self: Expr.AppliedSymbol, new_exprs: Generator[Expr.Expression, None, None]
) -> Expr.Expression:
    new_exprs = list(new_exprs)

    # simplify abs()
    if (
        self.decl
        and self.decl.name == ABS
        and len(new_exprs) == 1
        and new_exprs[0].is_value()
    ):
        return Expr.Number(number=str(abs(new_exprs[0].py_value)))

    # simplify x(pos(0,0)) to 0,  is_pos(pos(0,0)) to True
    if (
        len(new_exprs) == 1
        and hasattr(new_exprs[0], "decl")
        and isinstance(new_exprs[0].decl, Expr.Constructor)
        and new_exprs[0].decl.tester
        and self.decl
    ):
        if self.decl.name in new_exprs[0].decl.parent.accessors:
            i = new_exprs[0].decl.parent.accessors[self.decl.name]
            self.check(i < len(new_exprs[0].sub_exprs), f"Incorrect expression: {self}")
            return self._change(simpler=new_exprs[0].sub_exprs[i], sub_exprs=new_exprs)
        if self.decl.name == new_exprs[0].decl.tester.name:
            return self._change(value=Expr.TRUE)

    return self._change(sub_exprs=new_exprs)


def as_set_condition_appliedsymbol(
    self: Expr.AppliedSymbol,
) -> Tuple[Optional[Expr.AppliedSymbol], Optional[bool], Optional[Parse.Enumeration]]:
    # determine core after substitutions
    core = Expr.AppliedSymbol.make(self.symbol, deepcopy(self.sub_exprs))

    return (
        (None, None, None)
        if not self.in_enumeration
        else (core, "not" not in self.is_enumeration, self.in_enumeration)
    )


# Class SymbolExpr  #######################################################


def update_exprs_symbolexpr(
    self: Expr.SymbolExpr, new_exprs: Generator[Expr.Expression, None, None]
) -> Expr.Expression:
    if not self.name:  # $(..)
        symbol = list(new_exprs)[0]
        if isinstance(symbol, Expr.UnappliedSymbol) and symbol.decl:
            assert isinstance(symbol.decl, Expr.Constructor), "Internal error"
            concept_decl = symbol.decl.concept_decl
            out = concept_decl.symbol_expr
            out.variables = set()
            return out
        else:
            return self._change(sub_exprs=[symbol])
    return self


# Class Brackets  #######################################################


def update_exprs_brackets(
    self: Expr.Brackets, new_exprs: Generator[Expr.Expression, None, None]
) -> Expr.Expression:
    return list(new_exprs)[0]


# set conditions  #######################################################


def join_set_conditions(assignments: List[Ass.Assignment]) -> List[Ass.Assignment]:
    """In a list of assignments, merge assignments that are set-conditions on the same term.

    An equality and a membership predicate (`in` operator) are both set-conditions.

    Args:
        assignments (List[Assignment]): the list of assignments to make more compact

    Returns:
        List[Assignment]: the compacted list of assignments
    """
    #
    for i, c in enumerate(assignments):
        (x, belongs, y) = c.as_set_condition()
        if x:
            for j in range(i):
                (x1, belongs1, y1) = assignments[j].as_set_condition()
                if x1 and x.same_as(x1):
                    if belongs and belongs1:
                        new_tuples = y.tuples & y1.tuples  # intersect
                    elif belongs and not belongs1:
                        new_tuples = y.tuples ^ y1.tuples  # difference
                    elif not belongs and belongs1:
                        belongs = belongs1
                        new_tuples = y1.tuples ^ y.tuples
                    else:
                        new_tuples = y.tuples | y1.tuples  # union
                    # sort again
                    new_tuples = list(new_tuples.values())

                    symb = Expr.AppliedSymbol.make(
                        symbol=x.symbol,
                        args=x.sub_exprs,
                        is_enumeration="in",
                        in_enumeration=Parse.Enumeration(
                            parent=None, tuples=new_tuples
                        ),
                    )

                    core = deepcopy(
                        Expr.AppliedSymbol.make(symb.symbol, symb.sub_exprs)
                    )
                    symb.as_disjunction = symb.in_enumeration.contains([core])

                    out = Ass.Assignment(
                        symb, Expr.TRUE if belongs else Expr.FALSE, Ass.Status.UNKNOWN
                    )

                    assignments[j] = out  # keep the first one
                    assignments[i] = Ass.Assignment(
                        Expr.TRUE, Expr.TRUE, Ass.Status.UNKNOWN
                    )
    return [c for c in assignments if c.sentence != Expr.TRUE]
