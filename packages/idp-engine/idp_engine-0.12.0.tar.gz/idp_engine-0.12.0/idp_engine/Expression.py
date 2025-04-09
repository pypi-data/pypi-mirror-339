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

This module contains the ASTNode classes for expressions.
Note that many methods are imported from other modules, as done at the top
of each class.

"""

from __future__ import annotations

from copy import copy, deepcopy
from collections import ChainMap
from datetime import date
from dateutil.relativedelta import *
from fractions import Fraction
from re import findall
from sys import intern
from textx import get_location
from typing import Optional, List, Union, Tuple, Set, Callable, TYPE_CHECKING, Any, Dict

if TYPE_CHECKING:
    from .Theory import Theory
    from .Parse import Vocabulary, Declaration, SymbolDeclaration, Enumeration, ASTNode

from .utils import (
    unquote,
    OrderedSet,
    BOOL,
    INT,
    REAL,
    DATE,
    CONCEPT,
    RESERVED_SYMBOLS,
    IDPZ3Error,
    split_prefix,
    AggType,
)


class ASTNode(object):
    """superclass of all AST nodes"""

    from .EN import EN_astnode as EN

    def location(self):
        try:
            location = get_location(self)
            location["end"] = location["col"] + (
                len(self.code) if hasattr(self, "code") else 0
            )
            return location
        except:
            return {"line": 1, "col": 1, "end": 1}

    def check(self, condition: bool, msg: str):
        """raises an exception if `condition` is not True

        Args:
            condition (Bool): condition to be satisfied
            msg (str): error message

        Raises:
            IDPZ3Error: when `condition` is not met
        """
        if not condition:
            raise IDPZ3Error(msg, self)

    def SCA_Check(self, detections):
        raise IDPZ3Error("Internal error")  # monkey-patched

    def dedup_nodes(
        self, kwargs: dict[str, List[ASTNode]], arg_name: str
    ) -> dict[str, ASTNode]:
        """pops `arg_name` from kwargs as a list of named items
        and returns a mapping from name to items

        Args:
            kwargs: dictionary mapping named arguments to list of ASTNodes

            arg_name: name of the kwargs argument, e.g. "interpretations"

        Returns:
            dict[str, ASTNode]: mapping from `name` to AST nodes

        Raises:
            AssertionError: in case of duplicate name
        """
        ast_nodes = kwargs.pop(arg_name)
        out = {}
        for i in ast_nodes:
            # can't get location here
            assert hasattr(i, "name"), "internal error"
            assert i.name not in out, f"Duplicate '{i.name}' in {arg_name}"
            out[i.name] = i
        return out

    def interpret(self, problem: Optional[Theory]) -> ASTNode:
        return self


Annotation = Dict[str, Union[str, Dict[str, Any]]]


class Annotations(ASTNode):
    def __init__(self, parent, annotations: List[str]):
        self.annotations: Annotation = {}
        v: Union[str, dict[str, Any]]
        for s in annotations:
            p = s.split(":", 1)
            if len(p) == 2:
                if p[0] != "slider":
                    k, v = (p[0], p[1])
                else:
                    # slider:(lower_sym, upper_sym) in (lower_bound, upper_bound)
                    pat = r"\(((.*?), (.*?))\)"
                    arg = findall(pat, p[1])
                    l_symb = arg[0][1]
                    u_symb = arg[0][2]
                    l_bound = arg[1][1]
                    u_bound = arg[1][2]
                    slider_arg = {
                        "lower_symbol": l_symb,
                        "upper_symbol": u_symb,
                        "lower_bound": l_bound,
                        "upper_bound": u_bound,
                    }
                    k, v = ("slider", slider_arg)
            else:
                k, v = ("reading", p[0])
            self.check(k not in self.annotations, f"Duplicate annotation: [{k}: {v}]")
            self.annotations[k] = v


class Accessor(ASTNode):
    """represents an accessor and a type

    Attributes:
        accessor (str, Optional): name of accessor function

        codomain (SetName): name of the output type of the accessor

        decl (SymbolDeclaration): declaration of the accessor function
    """

    def __init__(self, parent, out: SetName, accessor: Optional[str] = None):
        self.accessor = accessor
        self.codomain = out
        self.decl: Optional[SymbolDeclaration] = None

    def __str__(self):
        return (
            self.codomain.name
            if not self.accessor
            else f"{self.accessor}: {self.codomain.name}"
        )


class Expression(ASTNode):
    """The abstract class of AST nodes representing (sub-)expressions.

    Attributes:
        code (string):
            Textual representation of the expression.  Often used as a key.

            It is generated from the sub-tree.

        str (string)
            Textual representation of the simplified expression.

        sub_exprs (List[Expression]):
            The children of the AST node.

            The list may be reduced by simplification.

        type (SetName, Optional):
            The type of the expression, e.g., ``bool``.

        co_constraint (Expression, optional):
            A constraint attached to the node.

            For example, the co_constraint of ``square(length(top()))`` is
            ``square(length(top())) = length(top())*length(top()).``,
            assuming ``square`` is appropriately defined.

            The co_constraint of a defined symbol applied to arguments
            is the instantiation of the definition for those arguments.
            This is useful for definitions over infinite domains,
            as well as to compute relevant questions.

        annotations (dict[str, str]):
            The set of annotations given by the expert in the IDP-Z3 program.

            ``annotations['reading']`` is the annotation
            giving the intended meaning of the expression (in English).

        original (Expression):
            The original expression, before propagation and simplification.

        variables (Set(string)):
            The set of names of the variables in the expression, before interpretation.

        is_type_constraint_for (string):
            name of the symbol for which the expression is a type constraint

        WDF (Expression, optional):
            a formula that is true only when `self` is well-defined (for partial functions)

    """

    from .Annotate import annotate_expression as annotate
    from .Annotate import (
        fill_attributes_and_check_expression as fill_attributes_and_check,
    )
    from .Definition import add_level_mapping_expression as add_level_mapping
    from .Definition import collect_nested_symbols_expression as collect_nested_symbols
    from .Idp_to_Z3 import translate_expression as translate
    from .Idp_to_Z3 import reified_expression as reified
    from .Interpret import interpret_expression as interpret
    from .Interpret import _interpret_expression as _interpret
    from .Simplify import as_set_condition_expression as as_set_condition
    from .Simplify import _change_expression as _change
    from .Simplify import simplify1_expression as simplify1
    from .Simplify import update_exprs_expression as update_exprs
    from .SymbolicPropagate import propagate1_expression as propagate1
    from .SymbolicPropagate import simplify_with
    from .SymbolicPropagate import substitute_expression as substitute
    from .SymbolicPropagate import symbolic_propagate_expression as symbolic_propagate
    from .WDF import fill_WDF_expression as fill_WDF
    from .WDF import merge_WDFs_expression as merge_WDFs

    def __init__(
        self,
        parent: Optional[ASTNode] = None,
        annotations: Optional[Annotations] = None,
    ):
        if parent:
            self.parent = parent
        self.sub_exprs: List[Expression]

        self.code: str = intern(str(self))
        self.annotations: Annotation = (
            annotations.annotations if annotations else {"reading": self.code}
        )
        self.original: Optional[Expression] = self

        self.str: str = self.code
        self.block: Optional[ASTNode] = None
        self.variables: Optional[Set[str]] = None
        self.type: Optional[SetName] = None
        self.is_type_constraint_for: Optional[str] = None
        self.co_constraint: Optional[Expression] = None
        self.WDF: Optional[Expression] = None
        self.in_head: bool
        self.py_value: Union[int, float]

        # attributes of the top node of a (co-)constraint
        self.questions: Optional[OrderedSet] = None
        self.relevant: Optional[bool] = None

    def __deepcopy__(self, memo):
        cls = self.__class__  # Extract the class of the object
        out = cls.__new__(
            cls
        )  # Create a new instance of the object based on extracted class
        memo[id(self)] = out
        out.__dict__.update(self.__dict__)

        out.sub_exprs = [deepcopy(e, memo) for e in self.sub_exprs]
        out.variables = deepcopy(self.variables, memo)
        out.co_constraint = deepcopy(self.co_constraint, memo)
        out.WDF = None  # do not copy WDF
        out.questions = deepcopy(self.questions, memo)
        return out

    def same_as(self, other: Expression):
        # symmetric
        if self.str == other.str:  # and type(self) == type(other):
            return True

        if type(self) in [Number, Date] and type(other) in [Number, Date]:
            return float(self.py_value) == float(other.py_value)

        return False

    def __repr__(self):
        return str(self)

    def __log__(self):  # for debugWithYamlLog
        return {
            "class": type(self).__name__,
            "code": self.code,
            "str": self.str,
            "co_constraint": self.co_constraint,
        }

    def has_variables(self) -> bool:
        return any(e.has_variables() for e in self.sub_exprs)

    def collect(
        self, questions: OrderedSet, all_: bool = True, co_constraints: bool = True
    ):
        """collects the questions in self.

        `questions` is an OrderedSet of Expression
        Questions are the terms and the simplest sub-formula that
        can be evaluated.

        all_=False : ignore expanded formulas
        and AppliedSymbol interpreted in a structure

        co_constraints=False : ignore co_constraints

        default implementation for UnappliedSymbol, AIfExpr, AUnary, Variable,
        Number_constant, Brackets
        """
        for e in self.sub_exprs:
            e.collect(questions, all_, co_constraints)

    def collect_symbols(
        self,
        symbols: Optional[dict[str, SymbolDeclaration]] = None,
        co_constraints: bool = True,
    ) -> dict[str, SymbolDeclaration]:
        """returns the list of symbols occurring in self,
        ignoring type constraints and symbols created by aggregates
        """
        symbols = {} if symbols == None else symbols
        assert symbols is not None, "Internal error"
        if self.is_type_constraint_for is None:  # ignore type constraints
            if (
                hasattr(self, "decl")
                and self.decl
                and self.decl.__class__.__name__ == "SymbolDeclaration"
                and not self.decl.name in RESERVED_SYMBOLS
                and not self.decl.name.startswith("__")
            ):  # min/max aggregates
                symbols[self.decl.name] = self.decl
            for e in self.sub_exprs:
                e.collect_symbols(symbols, co_constraints)
        return symbols

    def generate_constructors(self, constructors: dict[str, List[Constructor]]):
        """fills the list `constructors` with all constructors belonging to
        open types.
        """
        for e in self.sub_exprs:
            e.generate_constructors(constructors)

    def collect_co_constraints(self, co_constraints: OrderedSet, recursive=True):
        """collects the constraints attached to AST nodes, e.g. instantiated
        definitions

        Args:
            recursive: if True, collect co_constraints of co_constraints too
        """
        if self.co_constraint is not None and self.co_constraint not in co_constraints:
            co_constraints.append(self.co_constraint)
            if recursive:
                self.co_constraint.collect_co_constraints(co_constraints, recursive)
        for e in self.sub_exprs:
            e.collect_co_constraints(co_constraints, recursive)

    def is_value(self) -> bool:
        """True for numerals, date, identifiers,
        and constructors applied to values.

        Synomym: "is ground", "is rigid"

        Returns:
            bool: True if `self` represents a value.
        """
        return False

    def is_reified(self) -> bool:
        """False for values and for symbols applied to values.

        Returns:
            bool: True if `self` has to be reified to obtain its value in a Z3 model.
        """
        return True

    def is_assignment(self) -> bool:
        """

        Returns:
            bool: True if `self` assigns a rigid term to a rigid function application
        """
        return False

    def has_decision(self) -> bool:
        # returns true if it contains a variable declared in decision
        # vocabulary
        return any(e.has_decision() for e in self.sub_exprs)

    def type_inference(self, voc: Vocabulary) -> dict[str, SetName]:
        return {}
        try:
            return dict(ChainMap(*(e.type_inference(voc) for e in self.sub_exprs)))
        except AttributeError as e:
            if "has no attribute 'sorts'" in str(e):
                msg = f"Incorrect arity for {self}"
            else:
                msg = f"Unknown error for {self}"
            self.check(False, msg)
            return {}  # dead code

    def __str__(self) -> str:
        # TODO: where is this monkey patched? This seems incorrect?
        raise IDPZ3Error("Internal error")  # monkey-patched

    def as_set_condition(
        self,
    ) -> Tuple[Optional[AppliedSymbol], Optional[bool], Optional[Enumeration]]:
        """Returns an equivalent expression of the type "x in y", or None

        Returns:
            Tuple[Optional[AppliedSymbol], Optional[bool], Optional[Enumeration]]: meaning "expr is (not) in enumeration"
        """
        return (None, None, None)

    def split_equivalences(self) -> Expression:
        """Returns an equivalent expression where equivalences are replaced by
        implications

        Returns:
            Expression
        """
        out = self.update_exprs(e.split_equivalences() for e in self.sub_exprs)
        return out

    def get_type(self):
        return self.type


class Constructor(ASTNode):
    """Constructor declaration

    Attributes:
        name (string): name of the constructor

        args (List[Accessor])

        sorts (List[SetName]): types of the arguments of the constructor

        out (SetName): type that contains this constructor

        arity (Int): number of arguments of the constructor

        tester (SymbolDeclaration, Optional): function to test if the constructor
        has been applied to some arguments (e.g., is_rgb)

        concept_decl (SymbolDeclaration, Optional): declaration with name[1:],
        only for Concept constructors.

        range: the list of identifiers

        prefix (str, Optional): the constructor's prefix
    """

    from .Annotate import annotate_constructor as annotate
    from .Idp_to_Z3 import translate_constructor as translate
    from .Interpret import interpret_constructor as interpret

    def __init__(
        self,
        parent: Optional[ASTNode],
        name: str,
        args: Optional[List[Accessor]] = None,
    ):
        self.name: str = name
        self.args = (
            args if args else []
        )  # TODO avoid self.args by defining Accessor as subclass of SetName
        self.domains = [a.codomain for a in self.args]

        self.arity = len(self.domains)

        self.codomain: Optional[SetName] = None
        self.concept_decl: Optional[SymbolDeclaration] = None
        self.tester: Optional[SymbolDeclaration] = None
        self.range: Optional[List[Expression]] = None
        self.prefix: Optional[str] = split_prefix(self.name)
        self.block = None
        self.annotations = {}

    def __str__(self):
        return (
            self.name
            if not self.args
            else f"{self.name}({', '.join((str(a) for a in self.args))})"
        )


def CONSTRUCTOR(name: str, args=None) -> Constructor:
    return Constructor(None, name, args)


class SetName(Expression):
    """ASTNode representing a (sub-)type or a `Concept[aSignature]`, e.g., `Concept[T*T->Bool]`

    Inherits from Expression

    Args:
        name (str): name of the concept

        concept_domains (List[SetName], Optional): domain of the Concept signature, e.g., `[T, T]`

        codomain (SetName, Optional): range of the Concept signature, e.g., `Bool`

        decl (Declaration, Optional): declaration of the type

        root_set (List[SetName]): cross-product of root sets that include this set.
            Used for type checking.
    """

    from .Annotate import annotate_setname as annotate
    from .Idp_to_Z3 import translate_setname as translate
    from .Interpret import extension

    def __init__(
        self,
        parent,
        name: str,
        ins: Optional[List[SetName]] = None,
        out: Optional[SetName] = None,
    ):
        self.name = unquote(name)
        self.concept_domains = ins
        self.codomain = out
        self.sub_exprs = []
        self.decl: Declaration = None
        self.root_set: List[SetName] = None
        super().__init__(parent)

    def __str__(self):
        return self.name + (
            ""
            if not self.codomain
            else f"[{'*'.join(str(s) for s in self.concept_domains)}->{self.codomain}]"
        )

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        self.check(
            self.name != CONCEPT or self.codomain,
            f"`Concept` must be qualified with a type signature",
        )
        return (
            other
            and self.name == other.name
            and (
                not self.codomain
                or (
                    self.codomain == other.codomain
                    and len(self.concept_domains) == len(other.concept_domains)
                    and all(
                        s == o
                        for s, o in zip(self.concept_domains, other.concept_domains)
                    )
                )
            )
        )

    def is_value(self):
        return True

    def has_element(
        self, term: Expression, extensions: dict[str, Extension]
    ) -> Expression:
        """Returns an Expression that says whether `term` is in the type/predicate denoted by `self`.

        Args:
            term (Expression): the argument to be checked

        Returns:
            Expression: whether `term` `term` is in the type denoted by `self`.
        """
        if self.name == CONCEPT:
            extension = self.extension(extensions)[0]
            assert extension is not None, "Internal error"
            comparisons = [EQUALS([term, c[0]]) for c in extension]
            return OR(comparisons)
        else:
            assert self.decl is not None, "Internal error"
            self.check(self.decl.codomain == BOOL_SETNAME, "internal error")
            return self.decl.contains_element(term, extensions)


def SETNAME(name: str, ins=None, out=None) -> SetName:
    return SetName(None, name, ins, out)


BOOL_SETNAME = SETNAME(BOOL)
INT_SETNAME = SETNAME(INT)
REAL_SETNAME = SETNAME(REAL)
DATE_SETNAME = SETNAME(DATE)


class AIfExpr(Expression):
    PRECEDENCE = 10
    IF = 0
    THEN = 1
    ELSE = 2

    from .Annotate import fill_attributes_and_check_aifexpr as fill_attributes_and_check
    from .Definition import collect_nested_symbols_aifexpr as collect_nested_symbols
    from .EN import EN_aifexpr as EN
    from .Idp_to_Z3 import translate1_aifexpr as translate1
    from .Simplify import update_exprs_aifexpr as update_exprs
    from .WDF import merge_WDFs_aifexpr as merge_WDFs

    def __init__(
        self, parent, if_f: Expression, then_f: Expression, else_f: Expression
    ):
        self.if_f = if_f
        self.then_f = then_f
        self.else_f = else_f

        self.sub_exprs = [self.if_f, self.then_f, self.else_f]
        super().__init__()

    @classmethod
    def make(
        cls, if_f: Expression, then_f: Expression, else_f: Expression
    ) -> "AIfExpr":
        out = (cls)(None, if_f=if_f, then_f=then_f, else_f=else_f)
        return out.fill_attributes_and_check().simplify1()

    def __str__(self):
        return (
            f"if {self.sub_exprs[AIfExpr.IF  ].str}"
            f" then {self.sub_exprs[AIfExpr.THEN].str}"
            f" else {self.sub_exprs[AIfExpr.ELSE].str}"
        )


def IF(IF: Expression, THEN: Expression, ELSE: Expression, annotations=None) -> AIfExpr:
    return AIfExpr.make(IF, THEN, ELSE)


class Quantee(Expression):
    """represents the description of quantification, e.g., `x in T` or `(x,y) in P`
    The `Concept` type may be qualified, e.g. `Concept[Color->Bool]`

    Attributes:
        vars (List[List[Variable]]): the (tuples of) variables being quantified

        subtype (SetName, Optional): a literal SetName to quantify over, e.g., `Color` or `Concept[Color->Bool]`.

        sort (SymbolExpr, Optional): a dereferencing expression, e.g.,. `$(i)`.

        sub_exprs (List[SymbolExpr], Optional): the (unqualified) type or predicate to quantify over,
        e.g., `[Color], [Concept] or [$(i)]`.

        arity (int): the length of the tuple of variables

        decl (SymbolDeclaration, Optional): the (unqualified) Declaration to quantify over, after resolution of `$(i)`.
        e.g., the declaration of `Color`
    """

    from .Annotate import annotate_quantee
    from .Annotate import fill_attributes_and_check_quantee as fill_attributes_and_check
    from .EN import EN_quantee as EN
    from .Idp_to_Z3 import translate_quantee as translate

    def __init__(
        self,
        parent,
        vars: Union[List[Variable], List[List[Variable]]],
        subtype: Optional[SetName] = None,
        sort: Optional[SymbolExpr] = None,
    ):
        self.subtype = subtype
        if self.subtype:
            self.check(
                self.subtype.name == CONCEPT or self.subtype.codomain is None,
                f"Can't use signature after predicate {self.subtype.name}",
            )

        self.sub_exprs = [sort] if sort else [self.subtype] if self.subtype else []
        self.arity = None
        self.vars: List[List[Variable]] = []
        for i, v in enumerate(vars):
            if isinstance(v, Variable):
                self.vars.append([v])
                self.arity = 1 if self.arity == None else self.arity
            elif hasattr(v, "vars"):  # varTuple
                self.check(
                    1 < len(v.vars), f"Can't have singleton in binary quantification"
                )
                self.vars.append(v.vars)
                self.arity = len(v.vars) if self.arity == None else self.arity
            else:  # List of variables
                self.vars = vars
                self.arity = len(vars[0]) if self.arity == None else self.arity

        super().__init__()
        self.decl = None

        self.check(
            all(len(v) == self.arity for v in self.vars),
            f"Inconsistent tuples in {self}",
        )

    @classmethod
    def make(
        cls,
        var: Union[Variable, List[Variable]],
        subtype: Optional[SetName] = None,
        sort: Optional[SymbolExpr] = None,
    ) -> "Quantee":
        out = (cls)(None, [var], subtype=subtype, sort=sort)
        return out.fill_attributes_and_check()

    def __str__(self):
        signature = (
            ""
            if len(self.sub_exprs) <= 1
            else f"[{','.join(t.str for t in self.sub_exprs[1:-1])}->{self.sub_exprs[-1]}]"
        )
        return (
            f"{','.join(str(v) for vs in self.vars for v in vs)}"
            f"{f' ∈ {self.sub_exprs[0]}' if self.sub_exprs else ''}"
            f"{signature}"
        )


def split_quantees(self):
    """replaces an untyped quantee `x,y,z` into 3 quantees,
    so that each variable can have its own sort

    Args:
        self: either a AQuantification, AAggregate or Rule"""
    if len(self.quantees) == 1 and not self.quantees[0].sub_exprs:
        # separate untyped variables, so that they can be typed separately
        q = self.quantees.pop()
        for vars in q.vars:
            for var in vars:
                self.quantees.append(Quantee.make(var, sort=None))


class AQuantification(Expression):
    """ASTNode representing a quantified formula

    Args:
        annotations (dict[str, str]):
            The set of annotations given by the expert in the IDP-Z3 program.

            ``annotations['reading']`` is the annotation
            giving the intended meaning of the expression (in English).

        q (str): either '∀' or '∃'

        quantees (List[Quantee]): list of variable declarations

        f (Expression): the formula being quantified

        supersets, new_quantees, vars1: attributes used in `interpret`
    """

    PRECEDENCE = 20
    from .Annotate import annotate_aquantification as annotate
    from .Annotate import (
        fill_attributes_and_check_aquantification as fill_attributes_and_check,
    )
    from .EN import EN_aquantification as EN
    from .Idp_to_Z3 import translate1_aquantification as translate1
    from .Interpret import _interpret_aquantification as _interpret
    from .Simplify import update_exprs_aquantification as update_exprs
    from .SymbolicPropagate import symbolic_propagate_aquantification
    from .WDF import merge_WDFs_aquantification_aaggregate as merge_WDFs

    def __init__(
        self,
        parent: Optional[ASTNode],
        annotations: Optional[Annotations],
        q: str,
        quantees: List[Quantee],
        f: Expression,
    ):
        self.q = q
        self.quantees = quantees
        self.f = f

        self.q = (
            "∀"
            if self.q in ["!", "forall"]
            else "∃"
            if self.q in ["?", "thereisa"]
            else self.q
        )
        split_quantees(self)

        self.sub_exprs = [self.f]
        super().__init__(annotations=annotations)

        self.type = BOOL_SETNAME
        self.supersets: Optional[List[List[List[Union[Identifier, Variable]]]]] = None
        self.new_quantees: Optional[List[Quantee]] = None
        self.vars1: Optional[List[Variable]] = None
        self.interpretation = None

    @classmethod
    def make(
        cls,
        q: str,
        quantees: List[Quantee],
        f: Expression,
        annotations: Optional[Annotation] = None,
    ) -> "AQuantification":
        "make and annotate a quantified formula"
        out = cls(None, None, q, quantees, f)
        if annotations:
            out.annotations = annotations
        return out.fill_attributes_and_check()

    def __str__(self):
        if len(self.sub_exprs) == 0:
            body = TRUE.str if self.q == "∀" else FALSE.str
        elif len(self.sub_exprs) == 1:
            body = self.sub_exprs[0].str
        else:
            connective = "∧" if self.q == "∀" else "∨"
            body = connective.join("(" + e.str + ")" for e in self.sub_exprs)

        if self.quantees:
            vars = ",".join([f"{q}" for q in self.quantees])
            return f"{self.q} {vars}: {body}"
        else:
            return body

    def __deepcopy__(self, memo):
        out = super().__deepcopy__(memo)
        out.quantees = [deepcopy(q, memo) for q in self.quantees]
        return out

    def collect(self, questions, all_=True, co_constraints=True):
        questions.append(self)
        if all_:
            Expression.collect(self, questions, all_, co_constraints)
            for q in self.quantees:
                q.collect(questions, all_, co_constraints)

    def collect_symbols(self, symbols=None, co_constraints=True):
        symbols = Expression.collect_symbols(self, symbols, co_constraints)
        for q in self.quantees:
            q.collect_symbols(symbols, co_constraints)
        return symbols


def FORALL(qs, expr, annotations=None):
    return AQuantification.make("∀", qs, expr, annotations)


def EXISTS(qs, expr, annotations=None):
    return AQuantification.make("∃", qs, expr, annotations)


class AGenExist(Expression):
    """
    Represents a generalised existential quantification of the form
    "∃ OP INT quantor: f", with OP a comparison operator and INT an integer
    literal.  It represents a shorthand for a cardinality, "#{OP: f} OP INT".
    For example, "∃=1 c in Country: color_of(c) = Blue" states that there must
    be exactly one country that is assigned blue.
    """

    from .Annotate import annotate_agenexist as annotate
    from .EN import EN_agenexist as EN

    def __init__(self, parent, annotations, q, operator, number, quantees, f):
        # Init can be left bare-bones as AGenExist is transformed away during
        # annotation step.
        self.operator = (
            Operator.NORMAL[operator] if operator in Operator.NORMAL else operator
        )
        super().__init__(annotations=annotations)
        self.sub_exprs = []

    def __str__(self):
        vars_ = ",".join([f"{q}" for q in self.quantees])
        return f"∃{self.operator}{self.number}{vars_}: {self.f}."


class Operator(Expression):
    PRECEDENCE = 0  # monkey-patched # TODO: this is never monkey-patched?
    NORMAL = {
        "is strictly less than": "<",
        "is less than": "≤",
        "=<": "≤",
        "is greater than": "≥",
        "is strictly greater than": ">",
        ">=": "≥",
        "is not": "≠",
        "~=": "≠",
        "<=>": "⇔",
        "is the same as": "⇔",
        "are necessary and sufficient conditions for": "⇔",
        "<=": "⇐",
        "are necessary conditions for": "⇐",
        "=>": "⇒",
        "then": "⇒",
        "are sufficient conditions for": "⇒",
        "|": "∨",
        "or": "∨",
        "&": "∧",
        "and": "∧",
        "*": "⨯",
        "is": "=",
    }
    # EN_map: Optional[dict[str, str]] = None

    from .Annotate import (
        fill_attributes_and_check_operator as fill_attributes_and_check,
    )
    from .Definition import collect_nested_symbols_operator as collect_nested_symbols
    from .EN import EN_operator as EN
    from .EN import operator_EN_map as EN_map
    from .Idp_to_Z3 import Operator_MAP as MAP
    from .Idp_to_Z3 import translate1_operator as translate1

    def __init__(
        self, parent, operator, sub_exprs, annotations: Optional[Annotations] = None
    ):
        self.operator = operator
        self.sub_exprs = sub_exprs

        self.operator = list(map(lambda op: Operator.NORMAL.get(op, op), self.operator))

        super().__init__(parent, annotations=annotations)

        self.type = (
            BOOL_SETNAME
            if self.operator[0] in "&|∧∨⇒⇐⇔"
            else BOOL_SETNAME
            if self.operator[0] in "=<>≤≥≠"
            else None
        )

    @classmethod
    def make(
        cls,
        ops: Union[str, List[str]],
        operands: List[Expression],
        annotations: Optional[Annotation] = None,
        parent=None,
    ) -> Expression:
        """creates a BinaryOp
        beware: cls must be specific for ops !
        """
        if len(operands) == 0:
            if cls == AConjunction:
                out = copy(TRUE)
            elif cls == ADisjunction:
                out = copy(FALSE)
            else:
                assert False, "Internal error"
        elif len(operands) == 1:
            return operands[0]
        else:
            if isinstance(ops, str):
                ops = [ops] * (len(operands) - 1)
            out = (cls)(parent, ops, operands)
        if annotations:
            out.annotations = annotations

        if parent:  # for error messages
            out._tx_position = parent._tx_position
            out._tx_position_end = parent._tx_position_end
        return out.fill_attributes_and_check().simplify1()

    def __str__(self):
        def parenthesis(precedence, x):
            return f"({x.str})" if type(x).PRECEDENCE <= precedence else f"{x.str}"

        precedence = type(self).PRECEDENCE
        temp = parenthesis(precedence, self.sub_exprs[0])
        for i in range(1, len(self.sub_exprs)):
            temp += (
                f" {self.operator[i-1]} {parenthesis(precedence, self.sub_exprs[i])}"
            )
        return temp

    def collect(self, questions, all_=True, co_constraints=True):
        if self.operator[0] in "=<>≤≥≠":
            questions.append(self)
        for e in self.sub_exprs:
            e.collect(questions, all_, co_constraints)


class AImplication(Operator):
    PRECEDENCE = 50

    from .Annotate import (
        fill_attributes_and_check_aimplication as fill_attributes_and_check,
    )
    from .Definition import add_level_mapping_aimplication as add_level_mapping
    from .EN import EN_aimplication as EN
    from .Simplify import update_exprs_aimplication as update_exprs
    from .WDF import merge_WDFs_aimplication_aconjunction as merge_WDFs


def IMPLIES(exprs, annotations=None):
    return AImplication.make("⇒", exprs, annotations)


class AEquivalence(Operator):
    PRECEDENCE = 40

    from .Annotate import (
        fill_attributes_and_check_aequivalence as fill_attributes_and_check,
    )
    from .Simplify import update_exprs_aequivalence as update_exprs

    # NOTE: also used to split rules into positive implication and negative implication. Please don't change.
    def split(self):
        posimpl = IMPLIES([self.sub_exprs[0], self.sub_exprs[1]])
        negimpl = RIMPLIES(deepcopy([self.sub_exprs[0], self.sub_exprs[1]]))
        return AND([posimpl, negimpl])

    def split_equivalences(self):
        out = self.update_exprs(e.split_equivalences() for e in self.sub_exprs)
        return out.split()


def EQUIV(exprs, annotations=None):
    return AEquivalence.make("⇔", exprs, annotations)


class ARImplication(Operator):
    PRECEDENCE = 30

    from .Annotate import annotate_arimplication as annotate
    from .Definition import add_level_mapping_arimplication as add_level_mapping


def RIMPLIES(exprs, annotations):
    return ARImplication.make("⇐", exprs, annotations)


class ADisjunction(Operator):
    PRECEDENCE = 60

    from .Annotate import (
        fill_attributes_and_check_aconjunction_adisjunction as fill_attributes_and_check,
    )
    from .Idp_to_Z3 import translate1_adisjunction as translate1
    from .Simplify import update_exprs_adisjunction as update_exprs
    from .SymbolicPropagate import propagate1_adisjunction
    from .WDF import merge_WDFs_adisjunction as merge_WDFs

    def __str__(self):
        if not hasattr(self, "enumerated"):
            return super().__str__()
        return f"{self.sub_exprs[0].sub_exprs[0].code} in {{{self.enumerated}}}"


def OR(exprs):
    return ADisjunction.make("∨", exprs)


class AConjunction(Operator):
    PRECEDENCE = 70

    from .Annotate import (
        fill_attributes_and_check_aconjunction_adisjunction as fill_attributes_and_check,
    )
    from .Idp_to_Z3 import translate1_aconjunction as translate1
    from .Simplify import update_exprs_aconjunction as update_exprs
    from .SymbolicPropagate import propagate1_aconjunction as propagate1
    from .WDF import merge_WDFs_aimplication_aconjunction as merge_WDFs


def AND(exprs):
    return AConjunction.make("∧", exprs)


class AComparison(Operator):
    PRECEDENCE = 80

    from .Annotate import annotate_acomparison as annotate
    from .Annotate import (
        fill_attributes_and_check_acomparison as fill_attributes_and_check,
    )
    from .Idp_to_Z3 import translate1_acomparison as translate1
    from .Idp_to_Z3 import translate_acomparison_optimum
    from .Simplify import as_set_condition_acomparison as as_set_condition
    from .Simplify import update_exprs_acomparison as update_exprs
    from .SymbolicPropagate import propagate1_acomparison as propagate1

    def is_assignment(self):
        # f(x)=y
        return (
            len(self.sub_exprs) == 2
            and self.operator in [["="], ["≠"]]
            and isinstance(self.sub_exprs[0], AppliedSymbol)
            and not self.sub_exprs[0].is_reified()
            and self.sub_exprs[1].is_value()
        )


def EQUALS(exprs):
    return AComparison.make("=", exprs)


class ASumMinus(Operator):
    PRECEDENCE = 90

    from .Annotate import (
        fill_attributes_and_check_asumminus as fill_attributes_and_check,
    )
    from .Simplify import update_exprs_asumminus as update_exprs


class AMultDiv(Operator):
    PRECEDENCE = 100

    from .Annotate import (
        fill_attributes_and_check_amultdiv as fill_attributes_and_check,
    )
    from .Simplify import update_exprs_amultdiv as update_exprs
    from .WDF import merge_WDFs_amultdiv as merge_WDFs


class APower(Operator):
    PRECEDENCE = 110

    from .Annotate import fill_attributes_and_check_apower as fill_attributes_and_check
    from .Simplify import update_exprs_apower as update_exprs


class AUnary(Expression):
    PRECEDENCE = 120

    from .Annotate import fill_attributes_and_check_aunary as fill_attributes_and_check
    from .Definition import add_level_mapping_unary as add_level_mapping
    from .EN import EN_aunary as EN
    from .Idp_to_Z3 import AUnary_MAP as MAP
    from .Idp_to_Z3 import translate1_aunary as translate1
    from .Simplify import as_set_condition_aunary as as_set_condition
    from .Simplify import update_exprs_aunary as update_exprs
    from .SymbolicPropagate import propagate1_aunary as propagate1

    def __init__(self, parent, operators: List[str], f: Expression):
        self.operators = operators
        self.f = f
        self.operators = ["¬" if c in ["~", "not"] else c for c in self.operators]
        self.operator = self.operators[0]
        self.check(
            all([c == self.operator for c in self.operators]),
            "Incorrect mix of unary operators",
        )

        self.sub_exprs = [self.f]
        super().__init__()

    @classmethod
    def make(cls, op: str, expr: Expression) -> AUnary:
        out = AUnary(None, operators=[op], f=expr)
        return out.fill_attributes_and_check().simplify1()

    def __str__(self):
        return f"{self.operator}({self.sub_exprs[0].str})"


def NOT(expr):
    return AUnary.make("¬", expr)


class AAggregate(Expression):
    PRECEDENCE = 130

    from .Annotate import annotate_aaggregate as annotate
    from .Annotate import (
        fill_attributes_and_check_aquantification as fill_attributes_and_check,
    )
    from .Definition import collect_nested_symbols_aaggregate as collect_nested_symbols
    from .EN import EN_aaggregate as EN
    from .Idp_to_Z3 import translate1_aaggregate as translate1
    from .Interpret import _interpret_aaggregate as _interpret
    from .Simplify import update_exprs_aaggregate_extaggregate as update_exprs
    from .WDF import merge_WDFs_aquantification_aaggregate as merge_WDFs

    def __init__(
        self,
        parent: Optional[Expression],
        aggtype: str,
        quantees: List[Quantee],
        term: Optional[Expression] = None,
        condition: Optional[Expression] = None,
    ):
        self.quantees: List[Quantee] = quantees
        self.parent = parent

        # TODO: replace by match once p3.9 is dropped.
        if aggtype in ["#", "card"]:
            self.aggtype = AggType.CARD
        elif aggtype in ["min"]:
            self.aggtype = AggType.MIN
        elif aggtype in ["max"]:
            self.aggtype = AggType.MAX
        elif aggtype in ["sum"]:
            self.aggtype = AggType.SUM
        elif aggtype in ["distinct"]:
            self.aggtype = AggType.DISTINCT
        else:
            raise AssertionError("Internal error, please report")
        split_quantees(self)
        self.term = Number(number="1") if self.aggtype == AggType.CARD else term
        self.condition = TRUE if condition is None else condition
        self.sub_exprs = [self.term, self.condition]  # later: expressions to be summed
        self.annotated = (
            False  # cannot test q_vars, because aggregate may not have quantee
        )
        self.q = ""
        self.supersets, self.new_quantees, self.vars1 = None, None, None
        self.interpretation = None
        super().__init__()

    @classmethod
    def make(
        self,
        parent: Optional[Expression],
        aggtype: str,
        quantees: List[Quantee],
        term: Optional[Expression] = None,
        condition: Optional[Expression] = None,
    ):
        return AAggregate(
            parent=parent,
            aggtype=aggtype,
            quantees=quantees,
            term=term,
            condition=condition,
        ).fill_attributes_and_check()

    def __str__(self):
        # aggregates are over finite domains, and cannot have partial expansion
        if not self.annotated:
            assert len(self.sub_exprs) <= 2, "Internal error"
            vars = ",".join([f"{q}" for q in self.quantees])
            if self.aggtype == AggType.CARD:
                out = f"{self.aggtype}{{{vars}: {self.condition}}}"
            else:
                out = f"{self.aggtype}{{{self.term} | {vars}: {self.condition}}}"
        else:
            out = f"{self.aggtype}{{" f"{','.join(e.str for e in self.sub_exprs)}" f"}}"
        return out

    def __deepcopy__(self, memo):
        out = super().__deepcopy__(memo)
        out.quantees = [deepcopy(q, memo) for q in self.quantees]
        return out

    def collect(self, questions, all_=True, co_constraints=True):
        if all_ or len(self.quantees) == 0:
            Expression.collect(self, questions, all_, co_constraints)
            for q in self.quantees:
                q.collect(questions, all_, co_constraints)

    def collect_symbols(self, symbols=None, co_constraints=True):
        return AQuantification.collect_symbols(self, symbols, co_constraints)


class AExtAggregate(Expression):
    """Represents an aggregate over extension.

    This is an aggregate for which the set is manually enumerated, e.g.,
    sum{{A(), B(), C()}}.

    Args:
        aggtype (utils.AggType): the type
    """

    PRECEDENCE = 130

    from .Annotate import annotate_extaggregate as annotate
    from .Definition import collect_nested_symbols_aaggregate as collect_nested_symbols
    from .EN import EN_extaggregate as EN
    from .Idp_to_Z3 import translate1_extaggregate as translate1
    from .Simplify import update_exprs_aaggregate_extaggregate as update_exprs

    def __init__(self, parent: Optional[Expression], aggtype: str, symbols):
        # TODO: replace by match once p3.9 is dropped.
        if aggtype in ["#", "card"]:
            self.aggtype = AggType.CARD
        elif aggtype in ["min"]:
            self.aggtype = AggType.MIN
        elif aggtype in ["max"]:
            self.aggtype = AggType.MAX
        elif aggtype in ["sum"]:
            self.aggtype = AggType.SUM
        elif aggtype in ["distinct"]:
            self.aggtype = AggType.DISTINCT
        else:
            raise AssertionError("Internal error, please report")
        self.sub_exprs = symbols
        self.annotated = False
        super().__init__()

    def __str__(self):
        sub_exprs = (str(x) for x in self.sub_exprs)
        if self.aggtype == AggType.CARD:
            return f"#{{{", ".join(sub_exprs)}}}"
        else:
            return f"{self.aggtype}{{{{{", ".join(sub_exprs)}}}}}"


class AppliedSymbol(Expression):
    """Represents a symbol applied to arguments

    Args:
        symbol (SymbolExpr): the symbol to be applied to arguments

        is_enumerated (string): '' or 'is enumerated'

        is_enumeration (string): '' or 'in'

        in_enumeration (Enumeration): the enumeration following 'in'

        as_disjunction (Optional[Expression]):
            the translation of 'is_enumerated' and 'in_enumeration' as a disjunction

        decl (Declaration): the declaration of the symbol, if known

        in_head (Bool): True if the AppliedSymbol occurs in the head of a rule

        prefix (Optional[str]): the prefix of the symbol
    """

    PRECEDENCE = 200

    from .Annotate import annotate_appliedsymbol as annotate
    from .Annotate import (
        fill_attributes_and_check_appliedsymbol as fill_attributes_and_check,
    )
    from .Definition import add_level_mapping_appliedsymbol as add_level_mapping
    from .Definition import (
        collect_nested_symbols_appliedsymbol as collect_nested_symbols,
    )
    from .EN import EN_appliedsymbol as EN
    from .Idp_to_Z3 import translate1_appliedsymbol as translate1
    from .Idp_to_Z3 import reified_appliedsymbol as reified
    from .Interpret import _interpret_appliedsymbol as _interpret
    from .Simplify import as_set_condition_appliedsymbol as as_set_condition
    from .Simplify import update_exprs_appliedsymbol as update_exprs
    from .SymbolicPropagate import propagate1_appliedsymbol as propagate1
    from .SymbolicPropagate import substitute_appliedsymbol as substitute
    from .WDF import merge_WDFs_appliedsymbol as merge_WDFs

    def __init__(
        self,
        parent,
        symbol,
        sub_exprs,
        annotations: Optional[Annotations] = None,
        is_enumerated="",
        is_enumeration="",
        in_enumeration="",
    ):
        self.symbol: SymbolExpr = symbol
        self.sub_exprs = sub_exprs
        self.is_enumerated = is_enumerated
        self.is_enumeration = is_enumeration
        if self.is_enumeration == "∉":
            self.is_enumeration = "not"
        self.in_enumeration = in_enumeration

        super().__init__(annotations=annotations)

        self.as_disjunction = None
        self.decl: Optional[Declaration] = None
        self.in_head = False
        self.prefix = split_prefix(self.symbol.name)

    @classmethod
    def make(
        cls,
        symbol: SymbolExpr,
        args: List[Expression],
        type_: Optional[SetName] = None,
        annotations: Optional[Annotations] = None,
        is_enumerated="",
        is_enumeration="",
        in_enumeration="",
        type_check=True,
    ) -> AppliedSymbol:
        out = cls(
            None,
            symbol,
            args,
            annotations,
            is_enumerated,
            is_enumeration,
            in_enumeration,
        )
        out.sub_exprs = args
        # annotate
        out.decl = symbol.decl
        out.type = type_
        return out.fill_attributes_and_check(type_check)

    @classmethod
    def construct(cls, constructor, args):
        out = cls.make(SymbolExpr.make(constructor), args)
        out.decl = constructor
        out.type = constructor.codomain
        out.variables = set()
        return out

    def __str__(self):
        out = f"{self.symbol}({', '.join([x.str for x in self.sub_exprs])})"
        if self.in_enumeration:
            enum = f"{', '.join(str(e) for e in self.in_enumeration.tuples)}"
        return (
            f"{out}"
            f"{ ' '+self.is_enumerated if self.is_enumerated else ''}"
            f"{ f' {self.is_enumeration} {{{enum}}}' if self.in_enumeration else ''}"
        )

    def __deepcopy__(self, memo):
        out = super().__deepcopy__(memo)
        out.symbol = deepcopy(self.symbol, memo)
        out.as_disjunction = deepcopy(self.as_disjunction, memo)
        return out

    def collect(self, questions, all_=True, co_constraints=True):
        if self.decl and self.decl.name not in RESERVED_SYMBOLS:
            questions.append(self)
            if self.is_enumerated or self.in_enumeration:
                app = AppliedSymbol.make(self.symbol, self.sub_exprs)
                questions.append(app)
        self.symbol.collect(questions, all_, co_constraints)
        for e in self.sub_exprs:
            e.collect(questions, all_, co_constraints)
        if co_constraints and self.co_constraint is not None:
            self.co_constraint.collect(questions, all_, co_constraints)

    def collect_symbols(self, symbols=None, co_constraints=True):
        symbols = Expression.collect_symbols(self, symbols, co_constraints)
        self.symbol.collect_symbols(symbols, co_constraints)
        return symbols

    def has_decision(self):
        return (
            self.decl.block is not None and not self.decl.block.name == "environment"
        ) or any(e.has_decision() for e in self.sub_exprs)

    def type_inference(self, voc: Vocabulary):
        return {}
        decl = (
            voc.symbol_decls.get(self.symbol.name, None)
            if voc and hasattr(voc, "symbol_decls")
            else None
        )
        if decl:
            self.check(
                decl.arity == len(self.sub_exprs),
                f"Incorrect number of arguments in {self}: " f"should be {decl.arity}",
            )
        # try:
        out = {}
        for i, e in enumerate(self.sub_exprs):
            if decl and type(e) in [Variable, UnappliedSymbol]:
                if len(decl.domains) == len(self.sub_exprs):  # domain: p1*pn
                    out[e.name] = decl.domains[i]
                elif decl.domains[0] is not None:  # domain: p  -> use type signature
                    out[e.name] = decl.domains[0].decl.sorts[i]
            else:
                out.update(e.type_inference(voc))
        return out

    def is_value(self) -> bool:
        # independent of is_enumeration and in_enumeration !
        return type(self.decl) == Constructor and all(
            e.is_value() for e in self.sub_exprs
        )

    def is_reified(self):
        return (
            self.in_enumeration
            or self.is_enumerated
            or not all(e.is_value() for e in self.sub_exprs)
        )

    def generate_constructors(self, constructors: dict):
        assert self.symbol.name, "Can't use concepts here"
        symbol = self.symbol.name
        if symbol in ["unit", "heading", "introduction"]:
            assert type(self.sub_exprs[0]) == UnappliedSymbol, "Internal error"
            constructor = CONSTRUCTOR(self.sub_exprs[0].name)
            constructors[symbol].append(constructor)

    def simplified_code(self) -> str:
        """
        The simplified code for a symbol is the equivalent code in which every
        interpreted symbol has been simplified. For example, if `bar := a`, 
        then the simplified code for `foo(bar())` would be `foo(a)`.
        """
        return f"{self.symbol}({', '.join([x.str for x in self.sub_exprs])})"



class SymbolExpr(Expression):
    """represents either a type name, a symbol name
    or a `$(..)` expression evaluating to a type or symbol name

    Attributes:

        name (Optional[str]): name of the type or symbol, or None

        eval (Optional[str]): `$` or None

        s (Optional[Expression]): argument of the `$`.

        decl (Optional[Declaration]): the declaration of the symbol

    Either `name` and `decl`are not None, or `eval` and `s` are not None.
    When `eval` is None, `s` is None too.
    """

    from .Annotate import annotate_symbolexpr as annotate
    from .Simplify import update_exprs_symbolexpr as update_exprs

    def __init__(
        self, parent, name: Optional[str], eval: Optional[str], s: Optional[Expression]
    ):
        self.name = unquote(name) if name else name
        self.eval = eval
        self.s = s
        self.sub_exprs = [s] if s is not None else []
        self.decl: Optional[Declaration] = None
        super().__init__()

    @classmethod
    def make(cls, decl: Declaration) -> SymbolExpr:
        out = (cls)(None, decl.name, None, None)
        out.decl = decl
        return out

    def __str__(self):
        return f"$({self.sub_exprs[0]})" if self.eval else f"{self.name}"


class UnappliedSymbol(Expression):
    """The result of parsing a symbol not applied to arguments.
    Can be a constructor or a quantified variable.

    Variables are converted to Variable() by annotate().
    """

    PRECEDENCE = 200

    from .Annotate import annotate_unappliedsymbol as annotate
    from .Idp_to_Z3 import translate1_unappliedsymbol as translate1

    def __init__(self, parent: Optional[ASTNode], name: str):
        self.name = unquote(name)

        Expression.__init__(self)

        self.sub_exprs = []
        self.decl = None
        self.is_enumerated = None
        self.is_enumeration = None
        self.in_enumeration = None
        self.prefix = split_prefix(self.name)

    @classmethod
    def construct(cls, constructor: Constructor):
        """Create an UnappliedSymbol from a constructor"""
        out = (cls)(None, name=constructor.name)
        out.decl = constructor
        out.type = constructor.codomain
        out.variables = set()
        return out

    def is_value(self):
        return True

    def is_reified(self):
        return False

    def __str__(self):
        return self.name


TRUEC = CONSTRUCTOR("true")
FALSEC = CONSTRUCTOR("false")

TRUE = UnappliedSymbol.construct(TRUEC)
TRUE.type = BOOL_SETNAME
FALSE = UnappliedSymbol.construct(FALSEC)
FALSE.type = BOOL_SETNAME


class Variable(Expression):
    """AST node for a variable in a quantification or aggregate

    Args:
        name (str): name of the variable

        type (Optional[Union[SetName]]): sort of the variable, if known
    """

    PRECEDENCE = 200

    from .Annotate import annotate_variable as annotate
    from .Idp_to_Z3 import translate_variable as translate
    from .Interpret import _interpret_variable as _interpret
    from .SymbolicPropagate import substitute_variable as substitute

    def __init__(self, parent, name: str, type: Optional[SetName] = None):
        self.name = name
        assert type is None or isinstance(type, SetName), f"Internal error: {self}"

        super().__init__()

        self.type = type
        self.sub_exprs = []
        self.variables = set([self.name])

    def __str__(self):
        return self.name

    def __deepcopy__(self, memo):
        return self

    def fill_attributes_and_check(self: Expression) -> Expression:
        return self

    def has_variables(self) -> bool:
        return True


def VARIABLE(name: str, type: SetName):
    return Variable(None, name, type)


class Number(Expression):
    PRECEDENCE = 200

    from .Annotate import annotate_number as annotate
    from .Idp_to_Z3 import translate_number as translate

    def __init__(self, **kwargs):
        self.number = kwargs.pop("number")

        super().__init__()

        self.sub_exprs = []
        self.variables = set()
        self.py_value = 0  # to get the type

        ops = self.number.split("/")
        if len(ops) == 2:  # possible with z3_to_idp for rational value
            self.py_value = Fraction(self.number)
            self.type = REAL_SETNAME
        elif "." in self.number:
            self.py_value = Fraction(
                self.number if not self.number.endswith("?") else self.number[:-1]
            )
            self.type = REAL_SETNAME
        else:
            self.py_value = int(self.number)
            self.type = INT_SETNAME
        self.decl = None

    def __str__(self):
        return self.number

    def real(self):
        """converts the INT number to REAL"""
        self.check(
            self.type in [INT_SETNAME, REAL_SETNAME], f"Can't convert {self} to {REAL}"
        )
        return Number(number=str(float(self.py_value)))

    def is_value(self):
        return True

    def is_reified(self):
        return False

    def is_int(self):
        return self.type == INT_SETNAME


ZERO = Number(number="0")
ONE = Number(number="1")


class Date(Expression):
    PRECEDENCE = 200

    from .Idp_to_Z3 import translate_date as translate

    def __init__(self, **kwargs):
        self.iso = kwargs.pop("iso")

        dt = date.today() if self.iso == "#TODAY" else date.fromisoformat(self.iso[1:])
        if "y" in kwargs:
            y = int(kwargs.pop("y"))
            m = int(kwargs.pop("m"))
            d = int(kwargs.pop("d"))
            dt = dt + relativedelta(years=y, months=m, days=d)
        self.date = dt

        super().__init__()

        self.sub_exprs = []
        self.variables = set()

        self.py_value = int(self.date.toordinal())
        self.type = DATE_SETNAME

    @classmethod
    def make(cls, value: int) -> Date:
        return cls(iso=f"#{date.fromordinal(value).isoformat()}")

    def __str__(self):
        return f"#{self.date.isoformat()}"

    def is_value(self):
        return True

    def is_reified(self):
        return False


class Brackets(Expression):
    PRECEDENCE = 200

    from .Annotate import (
        fill_attributes_and_check_brackets as fill_attributes_and_check,
    )
    from .EN import EN_brackets as EN
    from .Idp_to_Z3 import translate1_brackets as translate1
    from .Simplify import update_exprs_brackets as update_exprs
    from .SymbolicPropagate import symbolic_propagate_brackets as symbolic_propagate

    def __init__(self, parent, f, annotations: Optional[Annotations] = None):
        self.f = f
        self.sub_exprs = [self.f]

        super().__init__()
        self.annotations = (
            annotations.annotations
            if annotations
            else {"reading": self.f.annotations["reading"]}
        )

    # don't @use_value, to have parenthesis
    def __str__(self):
        return f"({self.sub_exprs[0].str})"


class RecDef(Expression):
    """represents a recursive definition"""

    from .Idp_to_Z3 import translate1_recdef as translate1

    def __init__(self, parent, name, vars, expr):
        self.parent = parent
        self.name = name
        self.vars = vars
        self.sub_exprs = [expr]

        Expression.__init__(self)

        if parent:  # for error messages
            self._tx_position = parent._tx_position
            self._tx_position_end = parent._tx_position_end

    def __str__(self):
        return (
            f"{self.name}("
            f"{', '.join(str(v) for v in self.vars)}"
            f") = {self.sub_exprs[0]}."
        )


Identifier = Union[AppliedSymbol, UnappliedSymbol, Number, Date]
Extension = Tuple[
    Optional[List[List[Identifier]]],  # None if the extension is infinite (e.g., Int)
    Optional[Callable],
]  # None if filtering is not required
