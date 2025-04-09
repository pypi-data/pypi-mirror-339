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
This module contains methods and functions for the handling of definitions
"""

from __future__ import annotations

from copy import deepcopy
from typing import Set, Tuple, List, Optional, TYPE_CHECKING

from .utils import RESERVED_SYMBOLS, Semantics, CO_CONSTR_RECURSION_DEPTH, REAL
import idp_engine.Expression as Expr
import idp_engine.Parse as Parse

if TYPE_CHECKING:
    from Theory import Theory

# class Definition  ###########################################################


def get_def_constraints(
    self: Parse.Definition, problem: Theory, for_explain: bool = False
) -> dict[Tuple[Parse.SymbolDeclaration, Parse.Definition], List[Expr.Expression]]:
    """returns the constraints for this definition.

    The `instantiables` (of the definition) are expanded in `problem`.

    Args:
        problem (Theory):
            contains the structure for the expansion/interpretation of the constraints

        for_explain (Bool):
            Use implications instead of equivalence, for rule-specific explanations

    Return:
        dict[SymbolDeclaration, Definition, List[Expression]]:
            a mapping from (SymbolDeclaration, Definition) to the list of constraints
    """
    if self.mode == Semantics.RECDATA:
        out = {}
        for decl in self.renamed:
            # expr = nested if expression, for each rule
            decl.check(
                decl.codomain in [Expr.INT_SETNAME, Expr.BOOL_SETNAME],
                f"Recursive functions of type {decl.codomain} are not supported yet",
            )
            expr = (
                Expr.ZERO
                if decl.codomain == Expr.INT_SETNAME
                else Expr.FALSE
                if decl.codomain == Expr.BOOL_SETNAME
                else Expr.FALSE
            )  # todo: pick a value in type enumeration
            for rule in self.renamed[decl]:
                val = rule.out if rule.out is not None else Expr.TRUE
                expr = Expr.IF(rule.body, val, expr)

            vars = sorted(list(self.def_vars[decl.name].values()), key=lambda v: v.name)
            vars = vars[:-1] if decl.codomain != Expr.BOOL_SETNAME else vars
            expr = Expr.RecDef(self, decl.name, vars, expr.interpret(problem, {}))
            out[decl, self] = [expr]
        return out

    # compute level symbols
    level_symbols: dict[Parse.SymbolDeclaration, Expr.SetName] = {}
    for key in self.inductive:
        symbdec = Parse.SymbolDeclaration.make(
            self, "_" + str(self.id) + "lvl_" + key.name, key.domains, Expr.REAL_SETNAME
        )
        level_symbols[key] = Expr.SETNAME(symbdec.name)
        level_symbols[key].decl = symbdec

    # add level mappings
    instantiables = {}
    for decl, rules in self.canonicals.items():
        rule = rules[0]
        rule.has_finite_domain = all(
            s.extension(problem.extensions)[0] is not None
            for s in rule.definiendum.decl.domains
        )

        if rule.has_finite_domain or decl in self.inductive:
            # add a constraint containing the definition over the full domain
            if rule.out:
                expr = Expr.AppliedSymbol.make(
                    rule.definiendum.symbol, rule.definiendum.sub_exprs
                )
                expr.in_head = True
                head = Expr.EQUALS([expr, rule.out])
            else:
                head = Expr.AppliedSymbol.make(
                    rule.definiendum.symbol, rule.definiendum.sub_exprs
                )
                head.in_head = True

            # determine reverse implications, if any
            bodies, implications = [], []
            for r in rules:
                if not decl in self.inductive:
                    bodies.append(r.body)
                    if for_explain and 1 < len(
                        rules
                    ):  # not simplified -> no need to make copies
                        implications.append(Expr.IMPLIES([r.body, head], r.annotations))
                else:
                    new = r.body.split_equivalences()
                    bodies.append(new)
                    if for_explain:
                        new = deepcopy(new).add_level_mapping(
                            level_symbols, rule.definiendum, False, False, self.mode
                        )
                        implications.append(Expr.IMPLIES([new, head], r.annotations))

            all_bodies = Expr.OR(bodies)
            if not decl in self.inductive:  # i.e., function with finite domain
                if implications:  # already contains reverse implications
                    implications.append(
                        Expr.IMPLIES([head, all_bodies], self.annotations)
                    )
                else:
                    implications = [Expr.EQUIV([head, all_bodies], self.annotations)]
            else:  # i.e., predicate
                if not implications:  # no reverse implication
                    new = deepcopy(all_bodies).add_level_mapping(
                        level_symbols, rule.definiendum, False, False, self.mode
                    )
                    implications = [
                        Expr.IMPLIES([new, deepcopy(head)], self.annotations)
                    ]
                all_bodies = deepcopy(all_bodies).add_level_mapping(
                    level_symbols, rule.definiendum, True, True, self.mode
                )
                implications.append(Expr.IMPLIES([head, all_bodies], self.annotations))
            instantiables[decl] = implications

    out = {}
    for decl, bodies in instantiables.items():
        quantees = self.canonicals[decl][
            0
        ].quantees  # take quantee from 1st renamed rule
        expr = [
            Expr.FORALL(quantees, e, e.annotations).interpret(problem, {})
            for e in bodies
        ]
        out[decl, self] = expr
    return out


def instantiate_definition_def(
    self: Parse.Definition,
    decl: Parse.SymbolDeclaration,
    new_args: List[Expr.Expression],
    theory: Theory,
) -> Optional[Expr.Expression]:
    rule = self.clarks.get(decl, None)
    # exclude inductive and recursive definitions, unless they do not have variable arguments
    if (
        rule
        and self.mode != Semantics.RECDATA
        and (decl not in self.inductive or all(not a.has_variables() for a in new_args))
    ):
        instantiable = all(  # finite domain or not a variable
            s.extension(theory.extensions)[0] is not None or not v.has_variables()
            for s, v in zip(rule.definiendum.decl.domains, new_args)
        )

        if not instantiable:
            return None

        key = str(new_args)
        if (decl, key) in self.cache:
            return self.cache[decl, key]

        if self.inst_def_level + 1 > CO_CONSTR_RECURSION_DEPTH:
            return None
        self.inst_def_level += 1
        self.cache[decl, key] = None

        out = rule.instantiate_definition(new_args, theory)

        self.cache[decl, key] = out
        self.inst_def_level -= 1
        return out
    return None


# class Rule  ###########################################################


def instantiate_definition_rule(
    self: Parse.Rule, new_args: List[Expr.Expression], theory: Theory
) -> Expr.Expression:
    """Create an instance of the definition for new_args, and interpret it for theory.

    Args:
        new_args ([Expression]): tuple of arguments to be applied to the defined symbol
        theory (Theory): the context for the interpretation

    Returns:
        Expression: a boolean expression
    """
    out = self.body  # in case there are no arguments
    instance = Expr.AppliedSymbol.make(self.definiendum.symbol, new_args)
    instance.in_head = True
    self.check(len(self.definiendum.sub_exprs) == len(new_args), "Internal error")
    subs = dict(zip([e.name for e in self.definiendum.sub_exprs], new_args))

    if self.definiendum.type == Expr.BOOL_SETNAME:  # a predicate
        out = Expr.EQUIV([instance, out])
    else:
        subs[self.out.name] = instance
    out = out.interpret(theory, subs)
    out.block = self.block
    return out


## collect_nested_symbols ####################################################


# Expression
def collect_nested_symbols_expression(
    self: Expr.Expression, symbols: Set[Parse.SymbolDeclaration], is_nested: bool
) -> Set[Parse.SymbolDeclaration]:
    """returns the set of symbol declarations that occur (in)directly
    under an aggregate or some nested term, where is_nested is flipped
    to True the moment we reach such an expression

    returns {Parse.SymbolDeclaration}
    """
    for e in self.sub_exprs:
        e.collect_nested_symbols(symbols, is_nested)
    return symbols


# AIfExpr
def collect_nested_symbols_aifexpr(
    self: Expr.AIfExpr, symbols: Set[Parse.SymbolDeclaration], is_nested: bool
) -> Set[Parse.SymbolDeclaration]:
    return Expr.Expression.collect_nested_symbols(self, symbols, True)


# Operator
def collect_nested_symbols_operator(
    self: Expr.Operator, symbols: Set[Parse.SymbolDeclaration], is_nested: bool
):
    return Expr.Expression.collect_nested_symbols(
        self,
        symbols,
        is_nested if self.operator[0] in ["∧", "∨", "⇒", "⇐", "⇔"] else True,
    )


# AAggregate
def collect_nested_symbols_aaggregate(
    self: Expr.AAggregate, symbols: Set[Parse.SymbolDeclaration], is_nested: bool
) -> Set[Parse.SymbolDeclaration]:
    return Expr.Expression.collect_nested_symbols(self, symbols, True)


# AppliedSymbol
def collect_nested_symbols_appliedsymbol(
    self: Expr.AppliedSymbol, symbols: Set[Parse.SymbolDeclaration], is_nested: bool
):
    if is_nested and (
        hasattr(self, "decl")
        and self.decl
        and not isinstance(self.decl, Expr.Constructor)
        and self.decl.name not in RESERVED_SYMBOLS
    ):
        symbols.add(self.decl)
    for e in self.sub_exprs:
        e.collect_nested_symbols(symbols, True)
    return symbols


## add_level_mapping ####################################################


# Expression
def add_level_mapping_expression(
    self: Expr.Expression,
    level_symbols: dict[Parse.SymbolDeclaration, Expr.SetName],
    head: Expr.AppliedSymbol,
    pos_justification: bool,
    polarity: bool,
    mode: Semantics,
) -> Expr.Expression:
    """Returns an expression where level mapping atoms (e.g., lvl_p > lvl_q)
        are added to atoms containing recursive symbols.

    Arguments:
        - level_symbols (dict[SymbolDeclaration, SetName]): the level mapping
            symbols as well as their corresponding recursive symbols
        - head (AppliedSymbol): head of the rule we are adding level mapping
            symbols to.
        - pos_justification (Bool): whether we are adding symbols to the
            direct positive justification (e.g., head => body) or direct
            negative justification (e.g., body => head) part of the rule.
        - polarity (Bool): whether the current expression occurs under
            negation.
    """
    return self.update_exprs(
        (
            e.add_level_mapping(level_symbols, head, pos_justification, polarity, mode)
            for e in self.sub_exprs
        )
    ).fill_attributes_and_check()  # update .variables


# AImplication
def add_level_mapping_aimplication(
    self: Expr.Expression,
    level_symbols: dict[Parse.SymbolDeclaration, Expr.SetName],
    head: Expr.AppliedSymbol,
    pos_justification: bool,
    polarity: bool,
    mode: Semantics,
) -> Expr.Expression:
    sub_exprs = [
        self.sub_exprs[0].add_level_mapping(
            level_symbols, head, pos_justification, not polarity, mode
        ),
        self.sub_exprs[1].add_level_mapping(
            level_symbols, head, pos_justification, polarity, mode
        ),
    ]
    return self.update_exprs(sub_exprs).fill_attributes_and_check()


# ARimplication
def add_level_mapping_arimplication(
    self: Expr.ARimplication,
    level_symbols: dict[Parse.SymbolDeclaration, Expr.SetName],
    head: Expr.AppliedSymbol,
    pos_justification: bool,
    polarity: bool,
    mode: Semantics,
) -> Expr.Expression:
    sub_exprs = [
        self.sub_exprs[0].add_level_mapping(
            level_symbols, head, pos_justification, polarity, mode
        ),
        self.sub_exprs[1].add_level_mapping(
            level_symbols, head, pos_justification, not polarity, mode
        ),
    ]
    return self.update_exprs(sub_exprs).fill_attributes_and_check()


# AUnary
def add_level_mapping_unary(
    self: Expr.AUnary,
    level_symbols: dict[Parse.SymbolDeclaration, Expr.SetName],
    head: Expr.AppliedSymbol,
    pos_justification: bool,
    polarity: bool,
    mode: Semantics,
) -> Expr.Expression:
    sub_exprs = (
        e.add_level_mapping(
            level_symbols,
            head,
            pos_justification,
            not polarity if self.operator == "¬" else polarity,
            mode,
        )
        for e in self.sub_exprs
    )
    return self.update_exprs(sub_exprs).fill_attributes_and_check()


# AppliedSymbol
def add_level_mapping_appliedsymbol(
    self: Expr.AppliedSymbol,
    level_symbols: dict[Parse.SymbolDeclaration, Expr.SetName],
    head: Expr.AppliedSymbol,
    pos_justification: bool,
    polarity: bool,
    mode: Semantics,
) -> Expr.Expression:
    assert head.symbol.decl in level_symbols, f"Internal error in level mapping: {self}"
    if (
        self.symbol.decl not in level_symbols
        or self.in_head
        or mode in [Semantics.RECDATA, Semantics.COMPLETION]
        or (mode == Semantics.STABLE and pos_justification != polarity)
    ):
        return self
    else:
        if mode in [Semantics.WELLFOUNDED, Semantics.STABLE]:
            op = (
                (">" if pos_justification else "≥")
                if polarity
                else ("≤" if pos_justification else "<")
            )
        elif mode == Semantics.KRIPKEKLEENE:
            op = ">" if polarity else "≤"
        else:
            assert mode == Semantics.COINDUCTION, f"Internal error: {mode}"
            op = (
                ("≥" if pos_justification else ">")
                if polarity
                else ("<" if pos_justification else "≤")
            )
        comp = Expr.AComparison.make(
            op,
            [
                Expr.AppliedSymbol.make(
                    level_symbols[head.symbol.decl],
                    head.sub_exprs,
                    type_=Expr.REAL_SETNAME,
                ),
                Expr.AppliedSymbol.make(
                    level_symbols[self.symbol.decl],
                    self.sub_exprs,
                    type_=Expr.REAL_SETNAME,
                ),
            ],
        )
        if polarity:
            return Expr.AND([comp, self])
        else:
            return Expr.OR([comp, self])
