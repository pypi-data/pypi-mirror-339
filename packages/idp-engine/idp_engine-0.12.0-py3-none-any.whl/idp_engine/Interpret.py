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

Methods to ground / interpret a theory in a data structure

* expand quantifiers
* replace symbols interpreted in the structure by their interpretation
* instantiate definitions

( see docs/zettlr/Substitute.md )

"""

from __future__ import annotations

from copy import copy, deepcopy
from itertools import product
from typing import List, Callable, Optional, TYPE_CHECKING, Callable
from .utils import (
    BOOL,
    RESERVED_SYMBOLS,
    CONCEPT,
    OrderedSet,
    DEFAULT,
    GOAL_SYMBOL,
    EXPAND,
    COUNTER,
    flatten,
)
import idp_engine.Expression as Expr
import idp_engine.Assignments as Ass
import idp_engine.Parse as Parse

if TYPE_CHECKING:
    from .Theory import Theory

# class Import  ###########################################################


def interpret_import(self: Parse.Import, problem: Theory) -> None:
    pass


# Import.interpret = interpret


# class TypeDeclaration  ###########################################################


def interpret_typedeclaration(self: Parse.TypeDeclaration, problem: Theory) -> None:
    interpretation = problem.interpretations.get(self.name, None)
    if self.name in [BOOL, CONCEPT]:
        self.translate(problem)
        ranges = [c.interpret(problem).range for c in self.constructors]
        ext = ([[t] for r in ranges for t in r], None)
        problem.extensions[self.name] = ext
    else:
        self.check(
            interpretation is not None and hasattr(interpretation, "enumeration"),
            f"Expected an interpretation for type {self.name}",
        )

        enum = interpretation.enumeration.interpret(problem)
        if enum.constructors:
            enum.lookup = {k.name: Expr.TRUE for k in enum.constructors}
        elif enum.sorted_tuples:
            enum.lookup = {e.code: Expr.TRUE for e in enum.sorted_tuples}

        self.interpretation = interpretation
        self.constructors = enum.constructors
        self.translate(problem)

        if self.constructors is not None:
            for c in self.constructors:
                c.interpret(problem)

        # update problem.extensions
        if (
            self.super_set and enum.tuples
        ):  # check that the enumeration is a subset of the supertype
            super_set = self.super_sets[0].decl.interpretation.enumeration.tuples
            if super_set:
                for t in enum.tuples:
                    self.check(
                        t in super_set,
                        f"{t.args[0]} is not in the domain of {self.name}",
                    )
            problem.extensions[self.name] = ([t.args for t in enum.tuples], None)
        else:
            ext = enum.extensionE(problem.extensions)
            problem.extensions[self.name] = ext

        # needed ?
        # if (isinstance(self.interpretation.enumeration, Ranges)
        # and self.interpretation.enumeration.tuples):
        #     # add condition that the interpretation is total over the infinite domain
        #     # ! x in N: type(x) <=> enum.contains(x)
        #     t = SETNAME(self.type)  # INT, REAL or DATE
        #     t.decl, t.type = self, self.type
        #     var = VARIABLE(f"${self.name}!0$",t)
        #     q_vars = { f"${self.name}!0$": var}
        #     quantees = [Quantee.make(var, subtype=t)]
        #     expr1 = AppliedSymbol.make(SYMBOL(self.name), [var])
        #     expr1.decl = self
        #     expr2 = enum.contains(list(q_vars.values()), True)
        #     expr = EQUALS([expr1, expr2])
        #     constraint = FORALL(quantees, expr)
        #     constraint.annotations['reading'] = f"Enumeration of {self.name} should cover its domain"
        #     problem.constraints.append(constraint)


# class SymbolDeclaration  ###########################################################


def interpret_symboldeclaration(self: Parse.SymbolDeclaration, problem: Theory) -> None:
    assert all(isinstance(s, Expr.SetName) for s in self.domains), "internal error"

    # determine the extension, i.e., (superset, filter)
    if len(self.domains) == 0:  # () -> ..
        extensions = [([[]], None)]
        superset = [[]]
    else:
        sets = self.super_sets if self.codomain == Expr.BOOL_SETNAME else self.domains
        extensions = [s.extension(problem.extensions) for s in sets]
        if self.arity == 0:  # subset of ()
            superset = [[]]
        elif any(e[0] is None for e in extensions):
            superset = None
        elif len(self.sorts) == len(sets):  # domain: p1*pn, or superset: p1*pn
            superset = list(product(*([ee[0] for ee in e[0]] for e in extensions)))
        else:  # domain: p, or superset: p
            superset = extensions[0][0]

    filters = [e[1] for e in extensions]

    def filter(args):
        """For a predicate: symbol(args)"""
        self.check(self.codomain == Expr.BOOL_SETNAME, "Internal error")
        out = Expr.AppliedSymbol.make(self.symbol_expr, args, type_check=False)
        return out

    if self.codomain == Expr.BOOL_SETNAME:
        problem.extensions[self.name] = (superset, filter)

    (range, _) = self.codomain.extension(problem.extensions)
    if range is None:
        self.range = []
    else:
        self.range = [e[0] for e in range]

    # create instances + empty assignment
    if self.name not in RESERVED_SYMBOLS and superset is not None:
        self.instances = {}
        for args in superset:
            expr = Expr.AppliedSymbol.make(self.symbol_expr, args, type_check=False)
            self.instances[expr.code] = expr
            problem.assignments.assert__(expr, None, Ass.Status.UNKNOWN)

    # interpret the enumeration
    if self.name in problem.interpretations and self.name != GOAL_SYMBOL:
        problem.interpretations[self.name].interpret(problem)

    # create type constraints
    if isinstance(self.instances, dict) and (
        self.codomain != Expr.BOOL_SETNAME or self.repeat_name
    ):
        symb, symbs = None, None
        for inst in self.instances.values():
            args = inst.sub_exprs
            if self.codomain != Expr.BOOL_SETNAME:
                # add type constraints to problem.constraints
                # ! (x,y) in domain: range(f(x,y))
                if len(filters) == len(args):  # domain: p1*pn
                    cond = Expr.AND(
                        [
                            f([t]) if f is not None else Expr.TRUE
                            for f, t in zip(filters, args)
                        ]
                    )
                elif filters and filters[0] is not None:  # domain: p
                    cond = filters[0](args)
                else:
                    cond = Expr.TRUE

                range_condition = self.codomain.has_element(
                    deepcopy(inst), problem.extensions
                )
                if range_condition.same_as(Expr.TRUE):
                    break
                range_condition = range_condition.interpret(problem, {})

                constraint = Expr.IMPLIES([cond, range_condition])
                msg = f"Possible values for {inst}"
            else:  # self.repeat_name is true -> create superset constraint
                msg = f"Subset relation for {expr}"
                if len(self.super_sets) == 1:  # for p <: q
                    symb = symb or self.super_sets[0].decl.symbol_expr  # q
                    q = Expr.AppliedSymbol.make(symb, args, type_check=False)
                    constraint = Expr.IMPLIES([inst, q])  # p(x,y) => q(x,y)
                else:  # for p < q1*qn
                    symbs = symbs or [s.decl.symbol_expr for s in self.super_sets]
                    # p(x,y) => q1(x) & q2(y)
                    constraint = Expr.IMPLIES(
                        [
                            inst,
                            Expr.AND(
                                [
                                    Expr.AppliedSymbol.make(
                                        symb, [expr], type_check=False
                                    )
                                    for symb, expr in zip(symbs, args)
                                ]
                            ),
                        ]
                    )
            constraint.is_type_constraint_for = self.name
            constraint.annotations["reading"] = msg
            problem.constraints.append(constraint)


# class Definition  ###########################################################


def interpret_definition(self: Parse.Definition, problem: Theory) -> None:
    """updates problem.def_constraints, by expanding the definitions

    Args:
        problem (Theory):
            containts the enumerations for the expansion; is updated with the expanded definitions
    """
    self.cache = {}  # reset the cache
    problem.def_constraints.update(self.get_def_constraints(problem))


# class SymbolInterpretation  ###########################################################


def interpret_symbolinterpretation(
    self: Parse.SymbolInterpretation, problem: Theory
) -> None:
    status = Ass.Status.DEFAULT if self.block.name == DEFAULT else Ass.Status.STRUCTURE
    assert not self.is_type_enumeration, "Internal error"
    if self.name not in [GOAL_SYMBOL, EXPAND, COUNTER]:
        decl = problem.declarations[self.name]
        assert isinstance(decl, Parse.SymbolDeclaration), "Internal error"
        # update problem.extensions
        if self.symbol_decl.codomain == Expr.BOOL_SETNAME:  # predicate
            extension = [t.args for t in self.enumeration.tuples]
            problem.extensions[self.symbol_decl.name] = (extension, None)

        enumeration = self.enumeration  # shorthand
        self.check(
            all(
                len(t.args)
                == self.symbol_decl.arity
                + (1 if type(enumeration) == Parse.FunctionEnum else 0)
                for t in enumeration.tuples
            ),
            f"Incorrect arity of tuples in Enumeration of {self.symbol_decl.name}.  Please check use of ',' and ';'.",
        )

        lookup = {}
        if hasattr(decl, "instances") and decl.instances and self.default:
            lookup = {
                ",".join(str(a) for a in applied.sub_exprs): self.default
                for applied in decl.instances.values()
            }
        if type(enumeration) == Parse.FunctionEnum:
            lookup.update(
                (",".join(str(a) for a in t.args[:-1]), t.args[-1])
                for t in enumeration.sorted_tuples
            )
        else:
            lookup.update((t.code, Expr.TRUE) for t in enumeration.sorted_tuples)
        enumeration.lookup = lookup

        # update problem.assignments with data from enumeration
        for t in enumeration.tuples:
            # check that the values are in the range
            if isinstance(self.enumeration, Parse.FunctionEnum):
                args, value = t.args[:-1], t.args[-1]
                condition = decl.has_in_range(
                    value, problem.interpretations, problem.extensions
                )
                self.check(
                    not condition.same_as(Expr.FALSE),
                    f"{value} is not in the range of {self.symbol_decl.name}",
                )
                if not condition.same_as(Expr.TRUE):
                    problem.constraints.append(condition)
            else:
                args, value = t.args, Expr.TRUE

            # check that the arguments are in the domain
            a = str(args) if 1 < len(args) else str(args[0]) if len(args) == 1 else "()"
            self.check(
                len(args) == decl.arity, f"Incorrect arity of {a} for {self.name}"
            )
            condition = decl.has_in_domain(
                args, problem.interpretations, problem.extensions
            )
            self.check(
                not condition.same_as(Expr.FALSE),
                f"{a} is not in the domain of {self.symbol_decl.name}",
            )
            if not condition.same_as(Expr.TRUE):
                problem.constraints.append(condition)

            # check duplicates
            expr = Expr.AppliedSymbol.make(
                self.symbol_decl.symbol_expr, args, type_check=False
            )
            self.check(
                expr.code not in problem.assignments
                or problem.assignments[expr.code].status == Ass.Status.UNKNOWN,
                f"Duplicate entry in structure for '{self.name}': {str(expr)}",
            )

            # add to problem.assignments
            e = problem.assignments.assert__(expr, value, status)
            if (
                status == Ass.Status.DEFAULT  # for proper display in IC
                and type(self.enumeration) == Parse.FunctionEnum
            ):
                problem.assignments.assert__(e.formula(), Expr.TRUE, status)

        if self.default is not None:
            if decl.instances is not None:
                # fill the default value in problem.assignments
                for code, expr in decl.instances.items():
                    if (
                        code not in problem.assignments
                        or problem.assignments[code].status != status
                    ):
                        e = problem.assignments.assert__(expr, self.default, status)
                        if (
                            status == Ass.Status.DEFAULT  # for proper display in IC
                            and isinstance(self.enumeration, Parse.FunctionEnum)
                            and self.default.type != Expr.BOOL_SETNAME
                        ):
                            problem.assignments.assert__(e.formula(), Expr.TRUE, status)

            if self.sign == "≜" and decl.arity == 0 and len(decl.domains) == 1:
                # partial constant => ensure its domain is {()}
                _, filter = decl.domains[0].extension(problem.extensions)
                constraint = filter([])
                problem.constraints.append(constraint)
        elif self.sign == "≜" and 0 < decl.arity:
            # add condition that the interpretation is total
            # over the domain specified by the type signature
            # ! x in domain(f): enum.contains(x)
            if len(decl.domains) == decl.arity:
                q_vars = {
                    f"${sort.decl.name}!{str(i)}$": Expr.VARIABLE(
                        f"${sort.decl.name}!{str(i)}$", sort
                    )
                    for i, sort in enumerate(decl.domains)
                }
                quantees = [Expr.Quantee.make(v, sort=v.type) for v in q_vars.values()]
            else:
                quantees = [
                    Expr.Quantee.make(
                        list(
                            Expr.VARIABLE(f"${sort.decl.name}!{str(i)}$", sort)
                            for i, sort in enumerate(decl.domains[0].decl.sorts)
                        ),
                        decl.domains[0],
                    )
                ]
            constraint1 = Expr.FORALL(quantees, Expr.FALSE)

            # is the domain of `self` enumerable ?
            get_supersets(constraint1, problem)
            if (
                len(decl.domains) == decl.arity
                and constraint1.sub_exprs[0] == Expr.FALSE
            ):  # no filter added
                # the domain is enumerable => do the check immediately
                domain = set(str(flatten(d)) for d in product(*constraint1.supersets))
                if type(self.enumeration) == Parse.FunctionEnum:
                    enumeration = set(str(d.args[:-1]) for d in self.enumeration.tuples)
                else:
                    enumeration = set(str(d.args) for d in self.enumeration.tuples)
                if domain != enumeration:
                    errors = domain - enumeration
                    errors.update(enumeration - domain)
                    self.check(
                        False,
                        f"Enumeration of {self.name} should cover its domain ({errors})",
                    )
            else:  # add a constraint to the problem, to be solved by Z3
                # test case: tests/1240 FO{Core, Sugar, Int, PF)/LivingBeing.idp
                expr = self.enumeration.contains(quantees[0].vars[0], theory=problem)
                constraint = Expr.FORALL(quantees, expr).interpret(problem, {})
                constraint.annotations["reading"] = (
                    f"Enumeration of {self.name} should cover its domain"
                )
                problem.constraints.append(constraint)


# class Enumeration  ###########################################################


def interpret_enumeration(
    self: Parse.Enumeration, problem: Theory
) -> Parse.Enumeration:
    return self


# class ConstructedFrom  ###########################################################


def interpret_constructedfrom(
    self: Parse.ConstructedFrom, problem: Theory
) -> Parse.ConstructedFrom:
    self.tuples = OrderedSet()
    for c in self.constructors:
        c.interpret(problem)
        if c.range is None:
            self.tuples = None
            return self
        self.tuples.extend(Parse.TupleIDP(args=[e]) for e in c.range)
    return self


# class Constructor  ###########################################################


def interpret_constructor(self: Expr.Constructor, problem: Theory) -> Expr.Constructor:
    # assert all(s.decl and isinstance(s.decl.codomain, SetName) for s in self.domains), 'Internal error'
    if not self.domains:
        self.range = [Expr.UnappliedSymbol.construct(self)]
    elif any(s == self.codomain for s in self.domains):  # recursive data type
        self.range = None
    else:
        # assert all(isinstance(s.decl, SymbolDeclaration) for s in self.domains), "Internal error"
        extensions = [s.decl.codomain.extension(problem.extensions) for s in self.args]
        if any(e[0] is None for e in extensions):
            self.range = None
        else:
            self.check(
                all(e[1] is None for e in extensions),  # no filter in the extension
                f"Set signature of constructor {self.name} must have a given interpretation",
            )
            self.range = [
                Expr.AppliedSymbol.construct(self, es)
                for es in product(*[[ee[0] for ee in e[0]] for e in extensions])
            ]
    return self


# Constructor.interpret = interpret


# class Expression  ###########################################################


def interpret_expression(
    self: Expr.Expression, problem: Optional[Theory], subs: dict[str, Expr.Expression]
) -> Expr.Expression:
    """expand quantifiers and replace symbols interpreted in the structure
    by their interpretation

    Args:
        self: the expression to be interpreted
        problem: the theory to be applied
        subs: a dictionary mapping variable names to their value

    Returns:
        Expression: the interpreted expression
    """
    if self.is_type_constraint_for:
        return self
    _prepare_interpret(self, problem, subs)
    return self._interpret(problem, subs)


# Expression.interpret = interpret


def _prepare_interpret(
    self: Expr.Expression, problem: Optional[Theory], subs: dict[str, Expr.Expression]
):
    """Prepare the interpretation by transforming quantifications and aggregates"""

    for e in self.sub_exprs:
        _prepare_interpret(e, problem, subs)

    if isinstance(self, Expr.AQuantification) or isinstance(self, Expr.AAggregate):
        get_supersets(self, problem)


def clone_when_necessary(
    func,
) -> Callable[[Expr.Expression, Theory, dict[str, Expr.Expression]], Expr.Expression]:
    def inner_function(self, problem, subs):
        if self.is_value():
            return self
        if subs:
            self = copy(self)  # shallow copy !
            self.annotations = copy(self.annotations)
        out = func(self, problem, subs)
        return out

    return inner_function


@clone_when_necessary
def _interpret_expression(
    self: Expr.Expression, problem: Optional[Theory], subs: dict[str, Expr.Expression]
) -> Expr.Expression:
    """uses information in the problem and its vocabulary to:
    - expand quantifiers in the expression
    - simplify the expression using known assignments and enumerations
    - instantiate definitions

    This method creates a copy when necessary.

    Args:
        problem (Theory): the Theory to apply

        subs: a dictionary holding the value of the free variables of self

    Returns:
        Expression: the resulting expression
    """
    out = self.update_exprs(e._interpret(problem, subs) for e in self.sub_exprs)
    _finalize(out, subs)
    return out


def _finalize(
    self: Expr.Expression, subs: dict[str, Expr.Expression]
) -> Expr.Expression:
    """update self.variables and reading"""
    if subs:
        self.code = str(self)
        self.annotations["reading"] = self.code
    return self


# class SetName ###########################################################


def extension(self, extensions: dict[str, Expr.Extension]) -> Expr.Extension:
    """returns the extension of a SetName, given some interpretations.

    Normally, the extension is already in `extensions` by SymbolDeclaration.interpret.
    However, for Concept[T->T], an additional filtering is applied.

    Args:
        interpretations (dict[str, SymbolInterpretation]):
        the known interpretations of types and symbols

    Returns:
        Extension: a superset of the extension of self,
        and a function that, given arguments, returns an Expression that says
        whether the arguments are in the extension of self
    """
    if self.code not in extensions:
        self.check(self.name == CONCEPT, "internal error")
        assert (
            self.codomain and extensions is not None and extensions[CONCEPT] is not None
        ), "internal error"  # Concept[T->T]
        ext = extensions[CONCEPT][0]
        assert isinstance(ext, List), "Internal error"
        out = [
            v
            for v in ext
            if isinstance(v[0], Expr.UnappliedSymbol)  # for type checking
            and isinstance(v[0].decl.concept_decl, Parse.SymbolDeclaration)
            and v[0].decl.concept_decl.arity == len(self.concept_domains)  # real test
            and v[0].decl.concept_decl.codomain == self.codomain
            and len(v[0].decl.concept_decl.domains) == len(self.concept_domains)
            and all(
                s == q
                for s, q in zip(v[0].decl.concept_decl.domains, self.concept_domains)
            )
        ]
        extensions[self.code] = (out, None)
    return extensions[self.code]


# Class AQuantification  ######################################################


def get_supersets(
    self: Expr.AQuantification | Expr.AAggregate, problem: Optional[Theory]
) -> None:
    """determine the extent of the variables, if possible,
    and add a filter to the quantified expression if needed.
    This is used to ground quantification over unary predicates.

    Example:
        type T := {1,2,3}
        p : T -> Bool  // p is a subset of T
        !x in p: q(x)

        The formula is equivalent to `!x in T: p(x) => q(x).`
        -> The superset of `p` is `{1,2,3}`, the filter is `p(x)`.
        The grounding is `(p(1)=>q(1)) & (p(2)=>q(2)) & (p(3)=>q(3))`

        If p is enumerated (`p:={1,2}`) in a structure, however,
        the superset is now {1,2} and there is no need for a filter.
        The grounding is `q(1) & q(2)`

    Result:
        `self.supersets` is updated to contain the supersets
        `self.sub_exprs` are updated with the appropriate filters
    """
    self.new_quantees, self.vars1, self.supersets = [], [], []
    for q in self.quantees:
        domain = q.sub_exprs[0]

        if problem:
            if isinstance(domain, Expr.SetName):  # quantification over type / Concepts
                (superset, filter) = domain.extension(problem.extensions)
            elif type(domain) == Expr.SymbolExpr:
                if domain.decl:
                    self.check(
                        domain.decl.codomain.type == Expr.BOOL_SETNAME,
                        f"{domain} is not a type or predicate",
                    )
                    assert domain.decl.name in problem.extensions, "internal error"
                    (superset, filter) = problem.extensions[domain.decl.name]
                else:
                    return  # can't get supersets of $(..)
            else:
                self.check(False, f"Can't resolve the domain of {str(q.vars)}")
        else:
            (superset, filter) = None, None

        assert hasattr(domain, "decl"), "Internal error"
        arity = domain.decl.arity
        for vars in q.vars:
            self.check(len(vars) == arity, f"Incorrect arity for {domain}")
            if problem and filter:
                self.sub_exprs = [
                    _add_filter(self.q, f, filter, vars, problem)
                    for f in self.sub_exprs
                ]

        self.vars1.extend(flatten(q.vars))

        if superset is None:
            self.new_quantees.append(q)
            self.supersets.extend([q] for q in q.vars)  # replace the variable by itself
        else:
            self.supersets.extend([superset] * len(q.vars))


def _add_filter(
    q: str,
    expr: Expr.Expression,
    filter: Callable,
    args: List[Expr.Variable],
    theory: Theory,
) -> Expr.Expression:
    """add `filter(args)` to `expr` quantified by `q`

    Example: `_add_filter('∀', TRUE, filter, [1], theory)` returns `filter([1]) => TRUE`

    Args:
        q: the type of quantification
        expr: the quantified expression
        filter: a function that returns an Expression for some arguments
        args:the arguments to be applied to filter

    Returns:
        Expression: `expr` extended with appropriate filter
    """
    applied = filter(args)
    if q == "∀":
        out = Expr.IMPLIES([applied, expr])
    elif q == "∃":
        out = Expr.AND([applied, expr])
    else:  # aggregate
        if isinstance(expr, Expr.AIfExpr):  # cardinality
            # if a then b else 0 -> if (applied & a) then b else 0
            arg1 = Expr.AND([applied, expr.sub_exprs[0]])
            out = Expr.IF(arg1, expr.sub_exprs[1], expr.sub_exprs[2])
        else:  # sum
            out = Expr.IF(applied, expr, Expr.Number(number="0"))
    return out


@clone_when_necessary
def _interpret_aquantification(
    self: Expr.AQuantification | Expr.AAggregate,
    problem: Optional[Theory],
    subs: dict[str, Expr.Expression],
) -> Expr.Expression:
    """apply information in the problem and its vocabulary

    Args:
        problem (Theory): the problem to be applied

    Returns:
        Expression: the expanded quantifier expression
    """
    # This method is called by AAggregate._interpret !

    if not self.quantees and not subs:  # already expanded
        if self.interpretation:
            return self.interpretation
        return Expr.Expression._interpret(self, problem, subs)

    if not self.supersets:
        # interpret quantees
        self.quantees = [q._interpret(problem, subs) for q in self.quantees]
        get_supersets(self, problem)

    assert self.new_quantees is not None and self.vars1 is not None, "Internal error"
    self.quantees = self.new_quantees
    # expand the formula by the cross-product of the supersets, and substitute per `subs`
    forms, subs1 = [], copy(subs)
    for f in self.sub_exprs:
        for vals in product(*self.supersets):
            vals1 = flatten(vals)
            subs1.update((var.code, val) for var, val in zip(self.vars1, vals1))
            new_f2 = f._interpret(problem, subs1)
            forms.append(new_f2)

    out = self.update_exprs(f for f in forms)
    # Cache the interpretation in case the quantification is interpreted again
    self.interpretation = out
    return out


# Class AAggregate  ######################################################


@clone_when_necessary
def _interpret_aaggregate(
    self: Expr.AAggregate, problem: Optional[Theory], subs: dict[str, Expr.Expression]
) -> Expr.Expression:
    assert self.annotated, "Internal error in interpret"
    return Expr.AQuantification._interpret(self, problem, subs)


# AAggregate._interpret = _interpret

# Class AppliedSymbol  ##############################################


@clone_when_necessary
def _interpret_appliedsymbol(
    self: Expr.AppliedSymbol,
    problem: Optional[Theory],
    subs: dict[str, Expr.Expression],
) -> Expr.Expression:
    # interpret the symbol expression, if any
    if isinstance(self.symbol, Expr.SymbolExpr) and not self.symbol.name:  # $(x)()
        self.symbol = self.symbol._interpret(problem, subs)
        if self.symbol.name:  # found $(x)
            self.check(
                len(self.sub_exprs) == self.symbol.decl.arity,
                f"Incorrect arity for {self.code}",
            )
            kwargs = (
                {"is_enumerated": self.is_enumerated}
                if self.is_enumerated
                else {"in_enumeration": self.in_enumeration}
                if self.in_enumeration
                else {}
            )
            out = Expr.AppliedSymbol.make(self.symbol, self.sub_exprs, **kwargs)
            out.original = self
            self = out

    # interpret the arguments
    sub_exprs = [e._interpret(problem, subs) for e in self.sub_exprs]
    out = self.update_exprs(e for e in sub_exprs)
    _finalize(out, subs)
    if out.is_value():
        return out

    # interpret the AppliedSymbol
    value, co_constraint = None, None
    if out.decl and problem:
        if out.is_enumerated:
            assert (
                out.decl.codomain != Expr.BOOL_SETNAME
            ), f"Can't use 'is enumerated' with predicate {out.decl.name}."
            if out.decl.name in problem.interpretations:
                interpretation = problem.interpretations[out.decl.name]
                if interpretation.default is not None:
                    out.as_disjunction = Expr.TRUE
                else:
                    out.as_disjunction = interpretation.enumeration.contains(
                        sub_exprs, theory=problem
                    )
                if out.as_disjunction.same_as(Expr.TRUE) or out.as_disjunction.same_as(
                    Expr.FALSE
                ):
                    value = out.as_disjunction
                out.as_disjunction.annotations = out.annotations
        elif out.in_enumeration:
            # re-create original AppliedSymbol
            core = deepcopy(Expr.AppliedSymbol.make(out.symbol, sub_exprs))
            out.as_disjunction = out.in_enumeration.contains([core], theory=problem)
            if out.as_disjunction.same_as(Expr.TRUE) or out.as_disjunction.same_as(
                Expr.FALSE
            ):
                value = out.as_disjunction
            out.as_disjunction.annotations = out.annotations
        elif out.decl.name in problem.interpretations:
            interpretation = problem.interpretations[out.decl.name]
            if interpretation.block.name != DEFAULT:
                f = interpretation.interpret_application
                value = f(0, out, sub_exprs)
        if not out.in_head:
            # instantiate definition (for relevance)
            inst = [
                defin.instantiate_definition(out.decl, sub_exprs, problem)
                for defin in problem.definitions
            ]
            inst = [x for x in inst if x]
            if inst:
                co_constraint = Expr.AND(inst)
            elif self.co_constraint:
                co_constraint = self.co_constraint.interpret(problem, subs)

        out = (
            value
            if value
            else out._change(sub_exprs=sub_exprs, co_constraint=co_constraint)
        )
    return out


# Class Variable  #######################################################


def _interpret_variable(
    self: Expr.Variable, problem: Optional[Theory], subs: dict[str, Expr.Expression]
) -> Expr.Expression:
    if self.type:
        self.type = self.type._interpret(problem, subs)
    out = subs.get(self.code, self)
    return out
