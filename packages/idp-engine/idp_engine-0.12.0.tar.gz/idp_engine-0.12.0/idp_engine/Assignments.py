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

Classes to store assignments of values to questions

"""

from __future__ import annotations

__all__ = ["Status", "Assignment", "Assignments"]


from collections import defaultdict
from copy import copy, deepcopy
from datetime import date
from enum import Enum, auto
from typing import Optional, Tuple, List, TYPE_CHECKING
from z3 import BoolRef

from .Expression import (
    Expression,
    TRUE,
    FALSE,
    AND,
    NOT,
    EQUALS,
    AppliedSymbol,
    SetName,
    BOOL_SETNAME,
    DATE_SETNAME,
    INT_SETNAME,
    REAL_SETNAME,
    Number,
)
from .utils import NEWL, BOOL, INT, REAL, DATE

if TYPE_CHECKING:
    from .Parse import SymbolDeclaration, Enumeration
    from .Theory import Theory


class Status(Enum):
    """Describes how the value of a question was obtained"""

    UNKNOWN = auto()
    # fixed values:
    STRUCTURE = auto()
    UNIVERSAL = auto()
    CONSEQUENCE = auto()
    ENV_CONSQ = auto()
    # choices:
    EXPANDED = auto()
    DEFAULT = auto()
    GIVEN = auto()


def str_to_IDP(
    val_string: str,
    type_: SetName,
) -> Expression:
    """recursive function to decode a val_string in set `type_`

    Args:
        type_ (SetName): set containing the value
        val_string (str): a string containing a value

    Raises:
        IDPZ3Error: if wrong value

    Returns:
        Expression: the internal representation of the value
    """
    if (
        hasattr(type_.root_set[0].decl, "map")
        and val_string in type_.root_set[0].decl.map
    ):  # constructor
        out = type_.root_set[0].decl.map[val_string]
    elif 1 < len(val_string.split("(")):  # e.g., pos(0,0)
        assert hasattr(type_.decl, "interpretation"), "Internal error"

        # find constructor name and its arguments in val_string
        stack: List[int] = []
        args: List[str] = []
        for i, c in enumerate(val_string):
            if c == "(":
                name: str = val_string[:i].strip() if len(stack) == 0 else name
                stack.append(i + 1)
            elif c == "," and len(stack) == 1:
                start = stack.pop()
                args.append(val_string[start:i])
                stack.append(i + 2)
            elif c == ")":
                start = stack.pop()
                if len(stack) == 0:
                    args.append(
                        val_string[start:i]
                    )  # TODO construct the AppliedSymbol here, rather than later

        # find the constructor
        constructor = None
        assert (
            type(type_.decl.interpretation) == "SymbolInterpretation"
        ), "Internal error"
        for cons in type_.decl.interpretation.enumeration.constructors:
            if cons.name == name:
                constructor = cons
        assert constructor is not None, f"wrong constructor name '{name}' for {type_}"

        new_args = []
        for a, s in zip(args, constructor.domains):
            assert s.decl is not None, "Internal error"
            new_args.append(str_to_IDP(a, s))

        out = AppliedSymbol.construct(constructor, new_args)
    else:
        interp = getattr(type_.root_set[0].decl, "interpretation", None)
        enum_type = (
            interp.enumeration.type.name
            if interp
            else type_.decl.name
            if type(type_.decl) == "TypeDeclaration"
            else type_.decl.codomain.name
        )

        if type_ == BOOL_SETNAME or enum_type == BOOL:
            out = (
                TRUE
                if val_string == "True"
                else FALSE
                if val_string == "False"
                else None
            )
            if out is None:
                raise IDPZ3Error(f"wrong boolean value: {val_string}")
        elif type_ == DATE_SETNAME or enum_type == DATE:
            d = (
                date.fromordinal(eval(val_string))
                if not val_string.startswith("#")
                else date.fromisoformat(val_string[1:])
            )
            out = Date(iso=f"#{d.isoformat()}")
        elif type_ == REAL_SETNAME or enum_type == REAL:
            out = Number(
                number=val_string
                if "/" in val_string
                else str(float(eval(val_string.replace("?", ""))))
            )
        elif type_ == INT_SETNAME or enum_type == INT:
            out = Number(number=str(eval(val_string)))
        else:
            raise IDPZ3Error(f"unknown type for: {val_string}: {type_.decl}")
    return out


class Assignment(object):
    """Represent the assignment of a value to a question.
    Questions can be:

    * predicates and functions applied to arguments,
    * comparisons,
    * outermost quantified expressions

    A value is a rigid term.

    An assignment also has a reference to the symbol under which it should be
    displayed.

    Attributes:
        sentence (Expression): the question to be assigned a value

        value (Expression, optional): a rigid term

        status (Status, optional): qualifies how the value was obtained

        is_certainly_undefined (bool): True for functions applied to arguments certainly outside of its domain

        relevant (bool, optional): states whether the sentence is relevant

        symbol_decl (SymbolDeclaration): declaration of the symbol under which
        it should be displayed in the IC.
    """

    def __init__(
        self,
        sentence: Expression,
        value: Optional[Expression],
        status: Optional[Status],
        relevant: Optional[bool] = True,
    ):
        self.sentence: Expression = sentence
        self.value: Optional[Expression] = value
        self.status: Optional[Status] = status
        self.is_certainly_undefined = False
        self.relevant: Optional[bool] = relevant

        # First symbol in the sentence, preferably not starting with '_':
        # if no public symbol (not starting with '_') is found, the first
        # private one is used.
        self.symbol_decl: Optional[SymbolDeclaration] = None
        default = None
        self.symbols: dict[str, SymbolDeclaration] = sentence.collect_symbols(
            co_constraints=False
        ).values()
        for d in self.symbols:
            if not d.name.startswith("_"):
                if not d.by_z3:  # ignore accessors and testers
                    self.symbol_decl = d
                    break
            elif default is None:
                default = d
        if not self.symbol_decl:  # use the '_' symbol (to allow relevance computation)
            self.symbol_decl = default

    def copy(self, shallow: Optional[bool] = False) -> Assignment:
        out = copy(self)
        if not shallow:
            out.sentence = deepcopy(out.sentence)
        return out

    def __str__(self) -> str:
        pre, post = "", ""
        if self.value is None:
            pre = "? "
        elif self.value.same_as(TRUE):
            pre = ""
        elif self.value.same_as(FALSE):
            pre = "Not "
        else:
            post = f" -> {str(self.value)}"
        return f"{pre}{self.sentence.annotations['reading']}{post}"

    def __repr__(self) -> str:
        return self.__str__()

    def __log__(self) -> Optional[Expression]:
        return self.value

    def same_as(self, other: Assignment) -> bool:
        """returns True if self has the same sentence and truth value as other.

        Args:
            other (Assignment): an assignment

        Returns:
            bool: True if self has the same sentence and truth value as other.
        """
        return self.sentence.same_as(other.sentence) and (
            (self.value is None and other.value is None)
            or (
                self.value is not None
                and other.value is not None
                and self.value.same_as(other.value)
            )
        )

    def to_json(self) -> str:  # for GUI
        return str(self)

    def formula(self) -> Expression:
        if self.value is None:
            raise Exception("can't translate unknown value")
        if self.sentence.type == BOOL_SETNAME:
            out = self.sentence if self.value.same_as(TRUE) else NOT(self.sentence)
        else:
            out = EQUALS([self.sentence, self.value])
        return out

    def negate(self) -> Assignment:
        """returns an Assignment for the same sentence, but an opposite truth value.

        Raises:
            AssertionError: Cannot negate a non-boolean assignment

        Returns:
            [type]: returns an Assignment for the same sentence, but an opposite truth value.
        """
        assert (
            self.sentence.type == BOOL_SETNAME
        ), "Cannot negate a non-boolean assignment"
        assert self.value is not None, "Cannot negate an assignment without value"
        value = FALSE if self.value.same_as(TRUE) else TRUE
        return Assignment(self.sentence, value, self.status, self.relevant)

    def translate(self, problem: Theory) -> BoolRef:
        # called when the fact is true or false --> it must be defined too.
        out = self.formula()
        out.fill_WDF()
        out = AND([out.WDF, out])
        return out.translate(problem)

    def as_set_condition(
        self,
    ) -> Tuple[Optional[AppliedSymbol], Optional[bool], Optional[Enumeration]]:
        """returns an equivalent set condition, or None

        Returns:
            Tuple[Optional[AppliedSymbol], Optional[bool], Optional[Enumeration]]: meaning "appSymb is (not) in enumeration"
        """
        (x, y, z) = self.sentence.as_set_condition()
        assert self.value is not None, "Internal error"
        if x:
            return (x, y if self.value.same_as(TRUE) else not y, z)
        return (None, None, None)

    def unset(self) -> None:
        """Unsets the value of an assignment.

        Returns:
            None
        """
        self.value = None
        self.status = Status.UNKNOWN


class Assignments(dict):
    """Contains a set of Assignment"""

    def __init__(self, *arg, **kw):
        super(Assignments, self).__init__(*arg, **kw)
        self.symbols: dict[str, SymbolDeclaration] = {}
        for a in self.values():
            if a.symbol_decl:
                self.symbols[a.symbol_decl.name] = a.symbol_decl

    def copy(self, shallow: bool = False) -> "Assignments":
        return Assignments({k: v.copy(shallow) for k, v in self.items()})

    def assert__(
        self,
        sentence: Expression,
        value: Optional[Expression],
        status: Optional[Status],
    ) -> Assignment:
        if sentence.code in self:
            out = self[sentence.code].copy(shallow=True)
            if out.status in [
                Status.GIVEN,
                Status.EXPANDED,
                Status.DEFAULT,
            ] and status in [Status.CONSEQUENCE, Status.ENV_CONSQ, Status.UNIVERSAL]:
                assert out.value.same_as(
                    value
                ), "System should not override given choices with different consequences, please report this bug."
            else:
                if not (
                    out.status == Status.ENV_CONSQ and status == Status.CONSEQUENCE
                ):
                    # do not change an env consequence to a decision consequence
                    out.value = value
                    out.status = status
        else:
            out = Assignment(sentence, value, status)
        if out.symbol_decl:  # ignore comparisons of constructors
            self[sentence.code] = out
            self.symbols[out.symbol_decl.name] = out.symbol_decl
        return out

    def __str__(self) -> str:
        """Print the assignments in the same format as a model.

        Most symbols are printed as `name := {(val1, ..., val} -> valx, ...}.`
        with the exception of nullary symbols, which are printed as
        `name := value`.
        """
        out: dict[SymbolDeclaration, dict[str, str]] = {}  # ordered set of strings
        enumerated: dict[SymbolDeclaration, bool] = defaultdict(lambda: True)
        nullary = set()
        for a in self.values():
            if type(a.sentence) == AppliedSymbol:
                if a.status not in [Status.DEFAULT, Status.STRUCTURE]:
                    enumerated[a.symbol_decl] = False
                args = ", ".join(str(e) for e in a.sentence.sub_exprs)
                args = f"({args})" if 1 < len(a.sentence.sub_exprs) else args

                c = None
                if a.symbol_decl.arity == 0:
                    # Symbol is a proposition or constant.
                    c = f"{str(a.value)}" if a.value is not None else "*"
                    nullary.add(a.symbol_decl)
                elif a.value == FALSE:
                    # make sure we have an entry for `a` in `out`
                    if a.symbol_decl not in out:
                        out[a.symbol_decl] = {}
                elif a.value == TRUE:
                    # Symbol is a predicate.
                    c = f"{args}"
                elif a.value is not None:
                    # Symbol is a function.
                    c = f"{args} -> {str(a.value)}"

                if c:
                    enum = out.get(a.symbol_decl, dict())
                    enum[c] = c
                    out[a.symbol_decl] = enum

        model_str = ""
        for k, enum in out.items():
            if k in nullary:  # do not use {...}
                val = f"{k.name} := {list(enum)[0]}.{NEWL}"
                if "*" in val:
                    val = f"// {val}"
            else:
                sign = ":=" if k.instances or k.codomain == BOOL_SETNAME else ":>"
                # TODO improve sign detection (using root_set/extension, interpretation)
                # needs access to the theory !
                finite_domain = all(s.name not in [INT, REAL, DATE] for s in k.domains)
                sign = ":=" if finite_domain or k.codomain == BOOL_SETNAME else ":>"
                val = f"{k.name} {sign} {{{ ', '.join(s for s in enum) }}}.{NEWL}"
                val = f"{k.name} {sign} {{{ ', '.join(s for s in enum) }}}.{NEWL}"
            if not enumerated[k]:
                model_str += val
        return model_str
