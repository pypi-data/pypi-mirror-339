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

Methods to show a Theory in plain English.

"""

from __future__ import annotations
from typing import TYPE_CHECKING

from copy import copy

from .utils import NEWL, AggType

import idp_engine.Expression as Expr
import idp_engine.Parse as Parse

if TYPE_CHECKING:
    # from .Parse import IDP
    # from .Parse import TypeDeclaration, Definition, Rule
    from .Theory import Theory


def EN_idp(self: Parse.IDP) -> str:
    out = "\n".join(
        f"Theory {name}:\n{Theory(th).EN()}\n" for name, th in self.theories.items()
    )
    return out


def EN_astnode(self: Expr.ASTNode) -> str:
    return str(self)


def EN_definition(self: Parse.Definition) -> str:
    rules = "\n".join(f"    {r.original.EN()}." for r in self.rules)
    return "Definition:\n" + rules


def EN_rule(self: Parse.Rule) -> str:
    # TODO len(self.quantees) > self.definiendum.symbol.decl.arity
    vars = ",".join([f"{q}" for q in self.quantees])
    quant = f"for each {','.join(str(q) for q in self.quantees)}, " if vars else ""
    return (
        f"{quant}"
        f"{self.definiendum.EN()} "
        f"{(' is ' + str(self.out.EN())) if self.out else ''}"
        f" if {str(self.body.EN())}"
    ).replace("  ", " ")


def EN_aifexpr(self: Expr.AIfExpr) -> str:
    return (
        f"if {self.sub_exprs[Expr.AIfExpr.IF].EN()}"
        f" then {self.sub_exprs[Expr.AIfExpr.THEN].EN()}"
        f" else {self.sub_exprs[Expr.AIfExpr.ELSE].EN()}"
    )


def EN_quantee(self: Expr.Quantee) -> str:
    signature = (
        ""
        if len(self.sub_exprs) <= 1
        else f"[{','.join(t.EN() for t in self.sub_exprs[1:-1])}->{self.sub_exprs[-1].EN()}]"
    )
    return (
        f"{','.join(str(v) for vs in self.vars for v in vs)}"
        f"{f' in {self.sub_exprs[0]}' if self.sub_exprs else ''}"
        f"{signature}"
    )


def EN_aquantification(self: Expr.AQuantification) -> str:
    self = self.original
    vars = ",".join([f"{q.EN()}" for q in self.quantees])
    if not vars:
        return self.sub_exprs[0].EN()
    elif self.q == "∀":
        return f"for every {vars}, it is true that {self.sub_exprs[0].EN()}"
    elif self.q == "∃":
        return f"there is a {vars} such that {self.sub_exprs[0].EN()}"
    self.check(False, "Internal error")


def original(x: Expr.Expression) -> Expr.Expression:
    return x.original if x.original else x


def EN_aaggregate(self: Expr.AAggregate) -> str:
    self = original(self)
    vars = ",".join([f"{q.EN()}" for q in self.quantees])
    if self.aggtype in [AggType.SUM, AggType.MIN, AggType.MAX]:
        return (
            f"the {self.aggtype} of "
            f"{self.sub_exprs[0].EN()} "
            f"for all {vars}"
            f"{f' such that {self.sub_exprs[1].EN()}' if len(self.sub_exprs) == 2 else ''}"
        )
    else:  #  #
        return f"the number of {vars} such that " f"{self.sub_exprs[0].EN()}"


def EN_extaggregate(self: Expr.AExtAggregate) -> str:
    self = original(self)
    sub_exprs_en = ", ".join((x.EN() for x in self.sub_exprs))
    if self.aggtype in [AggType.SUM, AggType.MIN, AggType.MAX]:
        return f"the {self.aggtype} of ({sub_exprs_en})"
    elif self.aggtype == AggType.DISTINCT:
        return f"({sub_exprs_en}) have distinct values"
    else:
        return f"the number of items in ({sub_exprs_en})"

    return ""


operator_EN_map = {
    "∧": " and ",
    "∨": " or ",
    "⇒": " are sufficient conditions for ",
    "⇐": " are necessary conditions for ",
    "⇔": " if and only if ",
    "=": " is ",
    "≠": " is not ",
}


def EN_operator(self: Expr.Operator) -> str:
    def parenthesis(precedence, x):
        return f"({x.EN()})" if type(x).PRECEDENCE <= precedence else f"{x.EN()}"

    precedence = type(self).PRECEDENCE
    temp = parenthesis(precedence, self.sub_exprs[0])
    for i in range(1, len(self.sub_exprs)):
        op = Expr.Operator.EN_map.get(self.operator[i - 1], self.operator[i - 1])
        temp += f" {op} {parenthesis(precedence, self.sub_exprs[i])}"
    return temp


def EN_aimplication(self: Expr.AImplication) -> str:
    if 2 < len(self.sub_exprs):
        return Expr.Operator.EN(self)
    elif isinstance(self.original, Expr.ARImplication):
        return Expr.Operator.EN(self.original)
    return f"if {self.sub_exprs[0].EN()}, then {self.sub_exprs[1].EN()}"


def EN_aunary(self: Expr.AUnary) -> str:
    if (
        isinstance(self.sub_exprs[0], Expr.AComparison)
        and len(self.sub_exprs[0].sub_exprs) == 2
        and self.sub_exprs[0].operator[0] == "="
    ):
        # ~(a=b)
        new_expr = copy(self.sub_exprs[0])
        new_expr.operator[0] = "≠"
        return new_expr.EN()
    op = "not" if self.operator == "¬" else self.operator
    return f"{op}({self.sub_exprs[0].EN()})"


def EN_appliedsymbol(self: Expr.AppliedSymbol) -> str:
    if isinstance(self.decl, Parse.TypeDeclaration):
        out = f"{self.symbol}({', '.join([x.EN() for x in self.sub_exprs])})"
    elif self.symbol.decl:
        en = self.symbol.decl.annotations.get("EN", None)
        if en:
            out = en.format("", *(e.EN() for e in self.sub_exprs))
        else:
            out = f"{self.symbol}({', '.join([x.EN() for x in self.sub_exprs])})"
    elif self.symbol.eval == "$":  # $(..)
        out = f"concept {self.symbol.sub_exprs[0]} applied to ({', '.join([x.EN() for x in self.sub_exprs])})"
    else:
        self.check(False, f"Unknown symbol: {self.symbol}")
    if self.in_enumeration:
        enum = f"{', '.join(str(e) for e in self.in_enumeration.tuples)}"
    return (
        f"{out}"
        f"{ ' '+self.is_enumerated if self.is_enumerated else ''}"
        f"{ f' {self.is_enumeration} {{{enum}}}' if self.in_enumeration else ''}"
    )


def EN_brackets(self: Expr.Brackets) -> str:
    return f"({self.sub_exprs[0].EN()})"


EN_comp_map = {
    "<": "more than",
    "≤": "at least",
    "≥": "at most",
    ">": "less than",
    "≠": "exactly not",
    "=": "exactly",
}


def EN_agenexist(self: Expr.AGenExist):
    operator = EN_comp_map[self.operator]
    vars_ = ",".join([f"{q.EN()}" for q in self.quantees])
    return f"There exist {operator} {self.number} {vars_} such that {self.f.EN()}"


def EN_theory(self: Theory) -> str:
    """returns a string containing the Theory in controlled English"""

    def annot(c):
        return (
            f"[{c.annotations['reading']}]{NEWL}    "
            if c.annotations["reading"]
            else ""
        )

    constraints = "\n".join(
        f"- {annot(c)}" f"{c.original.EN()}."
        for c in self.constraints.values()
        if not c.is_type_constraint_for
        and (not isinstance(c, Expr.AppliedSymbol) or c.symbol.decl.name != "relevant")
    ).replace("  ", " ")
    definitions = "\n".join(f"- {d.EN()}" for d in self.definitions)
    return definitions + ("\n" if definitions else "") + constraints
