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

Methods to compute the Well-definedness condition of an Expression.

"""

from __future__ import annotations
from copy import copy
from typing import List, TYPE_CHECKING
from z3 import Solver, unsat

import idp_engine.Parse as Parse
import idp_engine.Expression as Expr

# from .Parse import TypeDeclaration, SymbolDeclaration, VarDeclaration
# from .Expression import (Expression, SetName, AIfExpr, IF,
#                          AQuantification, Quantee, AImplication,
#                          AConjunction, ADisjunction,
#                          Operator, AMultDiv, AUnary,
#                          AAggregate, AppliedSymbol, Number, NOT,
#                          EQUALS, AND, OR, TRUE, FALSE, ZERO, FORALL, IMPLIES,
#                          INT_SETNAME, REAL_SETNAME, DATE_SETNAME)
from .utils import CONCEPT, OrderedSet, flatten, IDPZ3Error

if TYPE_CHECKING:
    from .Theory import Theory


def is_subset_of(
    e: Expr.Expression, s1: Expr.SetName, s2: Expr.SetName
) -> Expr.Expression:
    """Returns a formula that is true when Expression e (of type s1) is necessarily in the set s2.

    Essentially, it goes up the hierarchy of s1 until s2 is found.
    It raises an error if the formula is FALSE.
    """
    if s1 == s2:
        return Expr.TRUE
    msg = f"Not in domain: {e} (of type {s1.name}) is not in {s2.name}"
    e.check(
        all(r1 == r2 for r1, r2 in zip(s1.root_set, s2.root_set)), msg
    )  # not disjoint
    if len(s1.root_set) == 0:  #  --> s2(), i.e., () is in s2
        symbol = s2.decl.symbol_expr
        assert symbol is not None
        app = Expr.AppliedSymbol.make(symbol, []).fill_WDF()
        return And([app.WDF, app])
    if isinstance(s1.decl, Parse.TypeDeclaration):
        if (
            isinstance(e, Expr.Number)
            and hasattr(s2.decl, "enumeration")
            and s2.decl.enumeration is not None
        ):  # check that e is in s2
            return s2.decl.enumeration.contains([e])  # resolve to TRUE or FALSE
        if s1.decl.super_sets[0] and s1.decl.super_sets[0] != s1:
            return is_subset_of(e, s1.decl.super_sets[0], s2)
        #  --> s2(e), i.e., e is in s2
        symbol = s2.decl.symbol_expr
        assert symbol is not None
        app = Expr.AppliedSymbol.make(symbol, [e]).fill_WDF()
        return And([app.WDF, app])
    if s1.name == CONCEPT:  # Concept[sig] <: Concept
        assert s2.concept_domains is not None
        e.check(s2.name == CONCEPT and len(s2.concept_domains) == 0, msg)
        return Expr.TRUE
    e.check(len(s1.decl.super_sets) > 0, msg)  # s1 = {()} = s2 = {()}
    # go up the hierarchy
    if len(s1.decl.super_sets) == 1 and s1.decl.super_sets[0] != s1:
        return is_subset_of(e, s1.decl.super_sets[0], s2)
    s1.check(False, "can't compare cross-product of sets")
    return Expr.FALSE  # dead code for mypy


def check_WDFs(theory: Theory, wdfs: List[Expr.Expression]) -> None:
    """Raises an error if a WDF in the list is not a tautology."""
    if any(not w.same_as(Expr.TRUE) for w in wdfs):
        solver = Solver(ctx=theory.ctx)
        for decl in theory.declarations.values():
            if not isinstance(decl, Parse.VarDeclaration):
                decl.interpret(theory)
                if hasattr(decl, "enumeration") and decl.enumeration is not None:
                    decl.enumeration.interpret(theory)
                decl.translate(theory)
        th = [c for c in theory.constraints if c.is_type_constraint_for is not None]

        for w in wdfs:
            if w.same_as(Expr.FALSE):
                raise IDPZ3Error("Domain error")
            if not w.same_as(Expr.TRUE):
                solver.push()
                c = w.interpret(theory, {})
                tautology = Expr.IMPLIES([Expr.AND(th), c]) if th else c
                solver.add(Expr.NOT(tautology).translate(theory))
                if solver.check() != unsat:
                    raise IDPZ3Error(
                        f"Domain error: {w} is not a tautology."
                        " Please add appropriate guards."
                    )
                solver.pop()
    return


# WDF constructors  #######################################################


def If(
    if_: Expr.Expression, then_: Expr.Expression, else_: Expr.Expression
) -> Expr.Expression:
    """Create a simplified If"""
    out = Expr.IF(if_, then_, else_)
    if isinstance(out, Expr.ADisjunction):
        return Or(out.sub_exprs)
    return out


def And(sub_exprs: List[Expr.Expression]) -> Expr.Expression:
    """Create a simplified conjunction"""
    out = OrderedSet()  # remove duplicates
    for e in sub_exprs:
        if isinstance(e, Expr.AConjunction):  # flatten p & (q & r)
            for ee in e.sub_exprs:
                out.append(ee)
        else:
            out.append(e)
    return Expr.AND([e for e in out.values()])


def Or(sub_exprs: List[Expr.Expression]) -> Expr.Expression:
    """Create a simplified disjunction"""
    exprs = OrderedSet()  # remove duplicates
    if isinstance(sub_exprs[-1], Expr.AConjunction):  # a|(b&c) -> (a|b) & (a|c)
        return And(Or(sub_exprs[:-1] + [e]) for e in sub_exprs[-1].sub_exprs)
    for e in sub_exprs:
        if isinstance(e, Expr.ADisjunction):  # flatten p | (q | r)
            for ee in e.sub_exprs:
                exprs.append(ee)
        else:
            exprs.append(e)
    # remove p | ~p
    positive, negative = set(), set()
    for e in exprs.values():
        if isinstance(e, Expr.AUnary):
            negative.add(e.sub_exprs[0].code)
        else:
            positive.add(e.code)
    exclude = positive.intersection(negative)
    if exclude:
        return Expr.TRUE
    else:
        out = Expr.OR(
            [
                e
                for e in exprs.values()
                if not (
                    e.code in exclude
                    or (isinstance(e, Expr.AUnary) and e.sub_exprs[0].code in exclude)
                )
            ]
        )
        return out


def Forall(qs: List[Expr.Quantee], expr: Expr.Expression) -> Expr.Expression:
    """Create a simplified Forall"""
    # move quantifications upward
    # !x: a&(!y:b)&c   --> !x: !y: a&b&..
    if isinstance(expr, Expr.Operator):
        for i, e in enumerate(expr.sub_exprs):
            if isinstance(e, Expr.AQuantification) and e.q == "∀":  # e = (!y:b)
                inner_vars = set(*flatten((q.vars for q in e.quantees)))
                if inner_vars.isdisjoint(expr.variables):  # x != y
                    new_expr = copy(expr.sub_exprs)  # new_exprs = a&b&c
                    new_expr[i] = e.sub_exprs[0]
                    if isinstance(expr, Expr.AConjunction):
                        new_expr = And(new_expr)
                    elif isinstance(expr, Expr.ADisjunction):
                        new_expr = Or(new_expr)
                    expr = Forall(e.quantees, new_expr)  # !y: a&b&c
                    break
    # ! (x,y) in p: phi  --> !(x,y) in p : p(x,y) => phi  (because no type inference)
    for q in qs:
        if 1 < q.arity:
            for var in q.vars:
                cond = Expr.AppliedSymbol.make(q.sub_exprs[0], var)  # p(x,y)
                expr = Or([Not(cond), expr])
                decl = q.sub_exprs[0].decl
                while (
                    decl and len(decl.super_sets) == 1
                ):  # also add the n-ary supersets of p
                    decl = decl.super_sets[0].decl
                    cond = Expr.AppliedSymbol.make(decl.symbol_expr, var)  # p(x,y)
                    expr = Or([Not(cond), expr])

    return Expr.FORALL(qs, expr).simplify1()


def Not(e: Expr.Expression) -> Expr.Expression:
    """Create a simplified negation"""
    if isinstance(e, Expr.AConjunction):  # ~(p & q)  -->  ~p | ~q
        return Or([Not(ee) for ee in e.sub_exprs])
    if isinstance(e, Expr.ADisjunction):  # ~(p | q)  -->  ~p & ~q
        return And([Not(ee) for ee in e.sub_exprs])
    if isinstance(e, Expr.AUnary):  # ~(~p))  -->  p
        return e.sub_exprs[0]
    return Expr.NOT(e)


# Class Expression  #######################################################


def fill_WDF_expression(self: Expr.Expression) -> Expr.Expression:
    """Compute the Well-definedness condition of an Expression"""
    for e in self.sub_exprs:
        e.fill_WDF()
    return self.merge_WDFs()


def merge_WDFs_expression(self: Expr.Expression) -> Expr.Expression:
    """Combine the WDF of the sub-expressions of self"""
    wdfs = [e.WDF if e.WDF else Expr.TRUE for e in self.sub_exprs]
    self.WDF = And(wdfs)
    return self


# Class AIfExpr  #######################################################


def merge_WDFs_aifexpr(self):
    # WDF(if(a,b,c)) is WDF(a) & if(a, WDF(b), WDF(c))
    if all(e.WDF for e in self.sub_exprs):
        self.WDF = And(
            [
                self.sub_exprs[0].WDF,
                If(self.sub_exprs[0], self.sub_exprs[1].WDF, self.sub_exprs[2].WDF),
            ]
        )
    else:
        self.WDF = None
    return self


# Class AQuantification, AAggregate  #######################################################


def merge_WDFs_aquantification_aaggregate(self):
    if len(self.sub_exprs) == 1:  # not a min/max aggregate
        # WDF(!x in p: phi)  = WDF(p) & !x in p: WDF(phi)
        if self.sub_exprs[0].WDF:
            forall = Forall(self.quantees, self.sub_exprs[0].WDF)
            self.WDF = And([q.WDF for q in self.quantees] + [forall])
        else:
            self.WDF = None
    else:
        # WDF(min{f|x in p: phi}) = WDF(p) & !x in p: WDF(phi) & (~phi | WDF(f))
        wdfs = [e.WDF if e.WDF else Expr.TRUE for e in self.sub_exprs]
        condition = And([wdfs[1], Or([Not(self.sub_exprs[1]), wdfs[0]])])
        forall = Forall(self.quantees, condition)
        self.WDF = And([q.WDF for q in self.quantees] + [forall])
    return self


# Class ADisjunction  #######################################################


def merge_WDFs_adisjunction(self):
    # WDF(p | q) = (WDF(p) & p) | (WDF(p) & WDF(q))
    # if WDF(q) is true, this becomes WDF(p)
    out, testing = Expr.TRUE, False
    for e in reversed(self.sub_exprs):
        if not e.WDF:
            continue
        if not testing:
            if e.WDF.same_as(Expr.TRUE):
                continue
            else:
                out, testing = e.WDF, True
        else:
            out = Or([And([e.WDF, e]), And([e.WDF, out])])
    self.WDF = out
    return self


# Class AImplication, AConjunction  #######################################################


def merge_WDFs_aimplication_aconjunction(self):
    # WDF(p & q) = (WDF(p) & ~p) | (WDF(p) & WDF(q))
    # if WDF(q) is true, this becomes WDF(p)
    out, testing = Expr.TRUE, False
    for e in reversed(self.sub_exprs):
        if not e.WDF:
            continue
        if not testing:
            if e.WDF.same_as(Expr.TRUE):
                continue
            else:
                out, testing = e.WDF, True
        else:
            out = Or([And([e.WDF, Not(e)]), And([e.WDF, out])])  #
    self.WDF = out
    return self


# Class AMultDiv  #######################################################


def merge_WDFs_amultdiv(self):
    # WDF(f*g/h) = WDF(f) & WDF(g) & WDF(h) & h ~= 0
    wdfs = [e.WDF if e.WDF else Expr.TRUE for e in self.sub_exprs]
    self.WDF = And(wdfs)
    for i, op in enumerate(self.operator):
        self.check(
            op != "/" or i == len(self.sub_exprs) - 2,
            f"Division must be the last operation in {self.code}",
        )
    if self.operator[-1] == "/":
        self.WDF = And(
            [Expr.NOT(Expr.EQUALS([self.sub_exprs[-1], Expr.ZERO])), self.WDF]
        )
    return self


# Class AppliedSymbol  #######################################################


def merge_WDFs_appliedsymbol(self):
    # WDF(p(a, b)) = WDF(p) & WDF(a) & WDF(b) & dom(p)(a,b)
    wdfs = [e.WDF or Expr.TRUE for e in self.sub_exprs]
    wdf1 = self.symbol.WDF or Expr.TRUE

    #  wdf2 = WDF for the domain of self
    if self.symbol.decl:  # known symbol
        domains = self.symbol.decl.domains
    elif self.symbol.eval == "$":  # $(..)
        domains = self.symbol.sub_exprs[0].type.concept_domains
    else:
        self.check(False, f"Unknown symbol: {self.symbol}")
    if not self.symbol.decl or isinstance(self.symbol.decl, Parse.SymbolDeclaration):
        if self.sub_exprs and len(self.sub_exprs) == len(domains):
            wdf2 = And(
                [is_subset_of(e, e.type, d) for e, d in zip(self.sub_exprs, domains)]
            )
        elif domains:  #  partial constant or n-ary domain
            symbol = domains[0].decl.symbol_expr
            wdf2 = Expr.AppliedSymbol.make(symbol, self.sub_exprs)
        else:  # constant c()
            wdf2 = Expr.TRUE
    else:
        wdf2 = Expr.TRUE
    self.WDF = Expr.AND([wdf1, wdf2] + wdfs)
    return self
