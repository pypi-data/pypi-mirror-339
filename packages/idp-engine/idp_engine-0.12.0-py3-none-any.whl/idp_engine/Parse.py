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

Classes to parse an IDP-Z3 theory.

"""

from __future__ import annotations

from copy import copy, deepcopy
from datetime import date
from enum import Enum
from itertools import groupby
from os import path
from sys import intern
from textx import metamodel_from_file
from typing import Tuple, List, Union, Optional, TYPE_CHECKING


from .Assignments import Assignments
from .Expression import (
    Annotations,
    Annotation,
    ASTNode,
    Constructor,
    CONSTRUCTOR,
    Accessor,
    SymbolExpr,
    Expression,
    AGenExist,
    AIfExpr,
    IF,
    AQuantification,
    split_quantees,
    SetName,
    SETNAME,
    Quantee,
    ARImplication,
    AEquivalence,
    AImplication,
    ADisjunction,
    AConjunction,
    AComparison,
    ASumMinus,
    AMultDiv,
    APower,
    AUnary,
    AAggregate,
    AExtAggregate,
    AppliedSymbol,
    UnappliedSymbol,
    Number,
    Brackets,
    Date,
    Extension,
    Identifier,
    Variable,
    TRUEC,
    FALSEC,
    TRUE,
    FALSE,
    EQUALS,
    AND,
    OR,
    BOOL_SETNAME,
    INT_SETNAME,
    REAL_SETNAME,
    DATE_SETNAME,
)
from .utils import (
    RESERVED_SYMBOLS,
    OrderedSet,
    NEWL,
    BOOL,
    INT,
    REAL,
    DATE,
    CONCEPT,
    GOAL_SYMBOL,
    EXPAND,
    RELEVANT,
    ABS,
    COUNTER,
    IDPZ3Error,
    MAX_QUANTIFIER_EXPANSION,
    Semantics as S,
    flatten,
    split_prefix,
)

if TYPE_CHECKING:
    from .Theory import Theory


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
    if type_.decl is None:
        assert type_ == BOOL_SETNAME, "Internal error"
        out = (
            TRUE
            if val_string in [TRUE, "True"]
            else FALSE
            if val_string in [FALSE, "False"]
            else None
        )
        if out is None:
            raise IDPZ3Error(f"wrong boolean value: {val_string}")
    elif (
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
        assert type(type_.decl.interpretation) == SymbolInterpretation, "Internal error"
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
            if type(type_.decl) == TypeDeclaration
            else type_.decl.codomain.name
        )

        if type_ == BOOL_SETNAME or enum_type == BOOL:
            out = (
                TRUE
                if val_string in [TRUE, "True"]
                else FALSE
                if val_string in [FALSE, "False"]
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


class ViewType(Enum):
    HIDDEN = "hidden"
    NORMAL = "normal"
    EXPANDED = "expanded"


class IDP(ASTNode):
    """The class of AST nodes representing an IDP-Z3 program."""

    """ do not display this info in the API
    Attributes:
        code (str): source code of the IDP program

        vocabularies (dict[str, Vocabulary]): list of vocabulary blocks, by name

        theories (dict[str, TheoryBlock]): list of theory blocks, by name

        structures (dict[str, Structure]): list of structure blocks, by name

        procedures (dict[str, Procedure]): list of procedure blocks, by name

        display (Display, Optional): display block, if any

        warnings (Exceptions): list of warnings
    """

    from .EN import EN_idp as EN

    def __init__(self, **kwargs):
        # log("parsing done")
        self.code = None
        self.vocabularies = self.dedup_nodes(kwargs, "vocabularies")
        self.theories = self.dedup_nodes(kwargs, "theories")
        self.structures = self.dedup_nodes(kwargs, "structures")
        displays = kwargs.pop("displays")
        self.procedures = self.dedup_nodes(kwargs, "procedures")

        # If a global prefix has been declared, pass it on to the vocabularies.
        self.prefixes = {
            name: pref.uri
            for (name, pref) in self.dedup_nodes(kwargs, "prefixes").items()
        }
        for name, voc in self.vocabularies.items():
            for k, v in self.prefixes.items():
                self.check(
                    k not in voc.declared_prefixes or voc.declared_prefixes[k] == v,
                    f"Conflicting prefix: {k}",
                )
                voc.declared_prefixes[k] = v

        assert len(displays) <= 1, "Too many display blocks"
        self.display = displays[0] if len(displays) == 1 else None

        for voc in self.vocabularies.values():
            voc.annotate_block(self)
        self.warnings = flatten(t.annotate_block(self) for t in self.theories.values())
        for struct in self.structures.values():
            struct.annotate_block(self)

        # determine default vocabulary, theory, before annotating display
        self.vocabulary = next(iter(self.vocabularies.values()))
        self.theory = next(iter(self.theories.values()))
        if self.display is None:
            self.display = Display(constraints=[], interpretations=[])

    @classmethod
    def from_file(cls, file: str) -> "IDP":
        """parse an IDP program from file

        Args:
            file (str): path to the source file

        Returns:
            IDP: the result of parsing the IDP program
        """
        assert path.exists(file), f"Can't find {file}"
        with open(file, "r", encoding="utf-8") as source:
            code = source.read()
            return cls.from_str(code)

    @classmethod
    def from_str(cls, code: str) -> "IDP":
        """parse an IDP program

        Args:
            code (str): source code to be parsed

        Returns:
            IDP: the result of parsing the IDP program
        """
        out = idpparser.model_from_str(code)
        out.code = code
        return out

    @classmethod
    def parse(cls, file_or_string: str) -> "IDP":
        """DEPRECATED: parse an IDP program

        Args:
            file_or_string (str): path to the source file, or the source code itself

        Returns:
            IDP: the result of parsing the IDP program
        """
        print("IDP.parse() is deprecated. Use `from_file` or `from_str` instead")
        code = file_or_string
        if path.exists(file_or_string):
            with open(file_or_string, "r", encoding="utf-8") as source:
                code = source.read()
        out = idpparser.model_from_str(code)
        out.code = code
        return out

    def get_blocks(self, blocks: List[str] | str) -> List[ASTNode]:
        """returns the AST nodes for the blocks whose names are given

        Args:
            blocks (List[str]): list of names of the blocks to retrieve

        Returns:
            List[Union[Vocabulary, TheoryBlock, Structure, Procedure, Display]]:
                list of AST nodes
        """
        names = blocks.split(",") if type(blocks) is str else blocks
        out = []
        for name in names:
            name = name.strip()  # remove spaces
            out.append(
                self.vocabularies[name]
                if name in self.vocabularies
                else self.theories[name]
                if name in self.theories
                else self.structures[name]
                if name in self.structures
                else self.procedures[name]
                if name in self.procedures
                else self.display
                if name == "Display"
                else ""
            )
        return out

    def execute(self) -> None:
        raise IDPZ3Error("Internal error")  # monkey-patched


################################ Vocabulary  ##############################


class Vocabulary(ASTNode):
    """The class of AST nodes representing a vocabulary block."""

    from .Annotate import annotate_block_voc as annotate_block

    def __init__(
        self,
        parent: ASTNode,
        name: str,
        prefixes,
        declarations: List[Union[Declaration, VarDeclaration, Import]],
    ):
        self.name = name
        self.idp: Optional[IDP] = None  # parent object
        self.symbol_decls: dict[
            str, Union[Declaration, VarDeclaration, Constructor]
        ] = {}

        self.name = "V" if not self.name else self.name
        # self.voc = self
        self.prefix = split_prefix(self.name)

        # Keep track of prefixes declared inside of the vocabulary or at
        # the top-level (the latter are added in IDP.__init__).
        self.declared_prefixes = {pref.name: pref.uri for pref in prefixes}

        # expand multi-symbol declarations
        temp = []
        for decl in declarations:
            if isinstance(decl, SymbolDeclaration):
                for symbol in decl.symbols:
                    new = copy(decl)  # shallow copy !

                    if new.partiality == "partial" and decl.domains == decl.sorts:
                        # partial function without domain declaration --> create a domain symbol
                        name = f"dom_{symbol}"
                        dom = SymbolDeclaration(
                            parent=parent,
                            annotations=None,
                            sorts=new.domains,
                            sort_=BOOL_SETNAME,
                            name=name,
                        )
                        temp.append(dom)
                        set_name = SetName(parent=parent, name=name)
                        new.domains = [set_name]
                    new.name = intern(symbol)
                    new.private = new.name.startswith("_")
                    new.symbols = None
                    temp.append(new)
            else:
                temp.append(decl)
        self.declarations = temp

        # define built-in types: Bool, Int, Real, Symbols
        self.declarations = [
            TypeDeclaration(self, name=BOOL, constructors=[TRUEC, FALSEC]),
            TypeDeclaration(self, name=INT, enumeration=IntRange()),
            TypeDeclaration(self, name=REAL, enumeration=RealRange()),
            TypeDeclaration(self, name=DATE, enumeration=DateRange()),
            TypeDeclaration(self, name=CONCEPT, constructors=[]),
            SymbolDeclaration.make(
                self,
                name=GOAL_SYMBOL,
                sorts=[SETNAME(CONCEPT, ins=[], out=SETNAME(BOOL))],
                sort_=SETNAME(BOOL),
            ),
            SymbolDeclaration.make(
                self,
                name=RELEVANT,
                sorts=[SETNAME(CONCEPT, ins=[], out=SETNAME(BOOL))],
                sort_=SETNAME(BOOL),
            ),
            SymbolDeclaration.make(
                self, name=ABS, sorts=[INT_SETNAME], sort_=INT_SETNAME
            ),
        ] + self.declarations

    def __str__(self):
        return (
            f"vocabulary {{{NEWL}"
            f"    {f'{NEWL}    '.join(str(i) for i in self.declarations)}"
            f"{NEWL}}}{NEWL}"
        ).replace("    \n", "")

    def add_voc_to_block(self, block):
        """adds the enumerations in a vocabulary to a theory or structure block

        Args:
            block (Theory): the block to be updated
        """
        for s in self.declarations:
            block.check(
                s.name not in block.declarations,
                f"Duplicate declaration of {self.name} "
                f"in vocabulary and block {block.name}",
            )
            block.declarations[s.name] = s
            if type(s) == TypeDeclaration and s.interpretation and self.name != BOOL:
                block.check(
                    s.name not in block.interpretations,
                    f"Duplicate enumeration of {self.name} "
                    f"in vocabulary and block {block.name}",
                )
                block.interpretations[s.name] = s.interpretation


class Import(ASTNode):
    from .Interpret import interpret_import as interpret

    def __init__(self, **kwargs):
        self.name = kwargs.pop("name")

    def __str__(self):
        return f"Import {self.name}"


class TypeDeclaration(ASTNode):
    """AST node to represent `type <symbol> := <enumeration>`

    Args:
        name (string): name of the type

        arity (int): the number of arguments

        domains (List[SetName]): a singleton list with a set having the type's name

        codomain (SetName): the Boolean type

        super_sets(List[SetName]): super-type

        constructors ([Constructor]): list of constructors in the enumeration

        interpretation (SymbolInterpretation): the symbol interpretation

        map (dict[string, Expression]): a mapping from code to Expression in range

        block (Vocabulary): the vocabulary block that contains it

        symbol_expr (SymbolExpr): the symbol expression for the type

        prefix (Optional[str]): the type's prefix
    """

    from .Annotate import annotate_declaration_typedeclaration as annotate_declaration
    from .Idp_to_Z3 import translate_typedeclaration as translate
    from .Interpret import interpret_typedeclaration as interpret

    def __init__(
        self,
        parent,
        name: str,
        constructors: Optional[List[Constructor]] = None,
        enumeration: Optional[Enumeration] = None,
        super_set: Optional[SetName] = None,
    ):
        self.name = name
        self.constructors = constructors if constructors else []
        enumeration = enumeration
        self.super_set = super_set

        self.arity: int = 1
        self.domains: List[SetName] = [SetName(None, self.name)]
        self.codomain: SetName = BOOL_SETNAME
        self.super_sets: List[SetName] = [super_set] if super_set else self.domains
        self.block: Optional[Block] = None
        self.symbol_expr: Optional[SymbolExpr] = None

        self.map: dict[str, Expression] = {}

        self.interpretation: Optional[SymbolInterpretation] = None
        if enumeration:
            self.interpretation = SymbolInterpretation(
                parent=None,
                name=UnappliedSymbol(None, self.name),
                sign="≜",
                enumeration=enumeration,
                default=FALSE,
            )
            self.interpretation.block = parent

        # Capture the prefix if there is one.
        self.prefix = split_prefix(self.name)

    def __str__(self):
        if self.name in RESERVED_SYMBOLS:
            return ""
        enumeration = (
            self.enumeration
            if hasattr(self, "enumeration") and self.enumeration
            else ""
        )
        constructors = enumeration.constructors if enumeration else None
        constructed = (
            ""
            if not bool(constructors) or all(0 == len(c.domains) for c in constructors)
            else "constructed from "
        )
        enumeration = (
            f"{constructed}{{{', '.join(str(c) for c in constructors)}}}"
            if constructors
            else f"{self.interpretation}"
            if self.interpretation
            else f"{enumeration}"
        )
        return f"type {self.name} {'' if not enumeration else ':= ' + enumeration}"

    def contains_element(
        self, term: Expression, extensions: dict[str, Extension]
    ) -> Expression:
        """returns an Expression that is TRUE when `term` is in the type"""
        if self.name == CONCEPT:
            comparisons = [
                EQUALS([term, UnappliedSymbol.construct(c)]) for c in self.constructors
            ]
            return OR(comparisons)
        elif self.name in [BOOL, INT, REAL, DATE]:
            return TRUE
        else:
            (superset, filter) = extensions[self.name]
            if superset is not None:
                # superset.sort(key=lambda t: str(t))
                if term.is_value():
                    comparisons = (
                        TRUE if any(term.same_as(t[0]) for t in superset) else FALSE
                    )
                else:
                    comparisons = OR([EQUALS([term, t[0]]) for t in superset])
                out = (
                    comparisons
                    if filter is None
                    else AND([filter([term]), comparisons])
                )
            elif filter is not None:
                out = filter([term])
            else:
                out = TRUE
            return out


class SymbolDeclaration(ASTNode):
    """The class of AST nodes representing an entry in the vocabulary,
    declaring one or more symbols.
    Multi-symbols declaration are replaced by single-symbol declarations
    before the annotate() stage.

    Attributes:
        annotations : the annotations given by the expert.

            `annotations['reading']` is the annotation
            giving the intended meaning of the expression (in English).

        symbols ([str]): the symbols being defined, before expansion

        name (string): the identifier of the symbol, after expansion of the node

        arity (int): the number of arguments

        sorts (List[SetName]): the types of the arguments

        out (SetName): the type of the symbol applied to arguments

        domains (List[SetName]): the domain of the symbol (as a cross-product)

        codomain (SetName): the codomain of the symbol

        super_sets (List[SetName]): for predicates: immediate superset of the interpretation.

        symbol_expr (SymbolExpr, Optional): symbol expression of the same name

        instances (dict[string, Expression]):
            a mapping from the code of a symbol applied to a tuple of
            arguments to its parsed AST

        range (List[Expression]): the list of possible values

        private (Bool): True if the symbol name starts with '_' (for use in IC)

        block: the vocabulary where it is defined

        unit (str):
            the unit of the symbol, such as m (meters)

        heading (str):
            the heading that the symbol should belong to

        optimizable (bool):
            whether this symbol should get optimize buttons in the IC

        counter (bool):
            whether this symbol should get a number counter in the IC

        by_z3 (Bool): True if the symbol is created by z3 (testers and accessors of constructors)
    """

    from .Annotate import annotate_declaration_symboldeclaration as annotate_declaration
    from .Idp_to_Z3 import translate_symboldeclaration as translate
    from .Interpret import interpret_symboldeclaration as interpret

    def __init__(
        self,
        parent,
        annotations: Optional[Annotations],
        sorts: List[SetName],
        sort_: SetName,
        symbols: Optional[List[str]] = None,
        name: Optional[str] = None,
        partiality: Optional[str] = None,
        repeat_name: Optional[str] = None,
        domains: Optional[List[SetName]] = None,
        codomain: Optional[SetName] = None,
        super_sets: Optional[List[SetName]] = None,
    ):
        self.annotations: Annotation = annotations.annotations if annotations else {}
        self.symbols: Optional[List[str]] = symbols
        self.name: Optional[str] = name
        self.sorts = sorts
        self.sort_ = sort_
        self.domains = domains or sorts
        self.codomain = codomain or sort_
        self.super_sets = super_sets or sorts
        self.partiality = partiality
        self.repeat_name = repeat_name

        self.symbol_expr: Optional[SymbolExpr] = None
        self.arity = None
        self.private = None
        self.unit: Optional[str] = None
        self.heading: Optional[str] = None
        self.optimizable: bool = True
        self.counter: bool = False

        self.range: Optional[List[AppliedSymbol]] = (
            None  # all possible terms.  Used in get_range and IO.py
        )
        self.instances: Optional[dict[str, AppliedSymbol]] = (
            None  # not starting with '_'
        )
        self.block: Optional[ASTNode] = None  # vocabulary where it is declared
        self.view = ViewType.NORMAL  # "hidden" | "normal" | "expanded" whether the symbol box should show atoms that contain that symbol, by default
        self.by_z3 = False

        # Capture the prefix if there is one.
        self.prefix = split_prefix(self.name)

    @classmethod
    def make(cls, parent, name, sorts, sort_):
        o = cls(parent=parent, name=name, sorts=sorts, sort_=sort_, annotations=None)
        o.arity = len(o.sorts)
        return o

    def __str__(self):
        if self.name in RESERVED_SYMBOLS:
            return ""
        args = "⨯".join(map(str, self.domains)) if 0 < len(self.domains) else ""
        return (
            f"{self.name}: "
            f"{ '('+args+')' if args else '()'}"
            f" → {self.codomain.name}"
        )

    def __repr__(self):
        return str(self)

    def has_in_domain(
        self,
        args: List[Expression],
        interpretations: dict[str, "SymbolInterpretation"],
        extensions: dict[str, Extension],
    ) -> Expression:
        """Returns an expression that is TRUE when `args` are in the domain of the symbol.

        Arguments:
            args (List[Expression]): the list of arguments to be checked, e.g. `[1, 2]`

        Returns:
            Expression: whether `(1,2)` is in the domain of the symbol
        """
        assert self.arity == len(
            args
        ), f"Incorrect arity of {str(args)} for {self.name}"
        if len(self.domains) == self.arity:
            return AND(
                [
                    typ.has_element(term, extensions)
                    for typ, term in zip(self.domains, args)
                ]
            )
        else:
            return AppliedSymbol.make(self.domains[0].decl.symbol_expr, args)

    def has_in_range(
        self,
        value: Expression,
        interpretations: dict[str, "SymbolInterpretation"],
        extensions: dict[str, Extension],
    ) -> Expression:
        """Returns an expression that says whether `value` is in the range of the symbol."""
        return self.codomain.has_element(value, extensions)

    def contains_element(
        self, term: Expression, extensions: dict[str, Extension]
    ) -> Expression:
        """returns an Expression that is TRUE when `term` satisfies the predicate"""
        assert self.codomain == BOOL_SETNAME and self.name is not None, "Internal error"
        (superset, filter) = extensions[self.name]
        if superset is not None:
            # superset.sort(key=lambda t: str(t))
            comparisons = [EQUALS([term, t[0]]) for t in superset]
            out = (
                OR(comparisons)
                if filter is None
                else AND([filter([term]), OR(comparisons)])
            )
        elif filter is not None:
            out = filter([term])
        else:
            out = TRUE
        return out


class VarDeclaration(ASTNode):
    """represents a declaration of variable (IEP 24)

    Attributes:
        name (str): name of the variable

        subtype (SetName): type of the variable

        prefix (str, Optional): prefix of the variable
    """

    from .Annotate import annotate_declaration_vardeclaration as annotate_declaration

    def __init__(self, **kwargs):
        self.name = kwargs.pop("name")
        self.subtype = kwargs.pop("subtype")
        self.prefix = None

    def __str__(self):
        return f"var {self.name} ∈ {self.subtype}"


Declaration = Union[TypeDeclaration, SymbolDeclaration]


################################ TheoryBlock  ###############################


class TheoryBlock(ASTNode):
    """The class of AST nodes representing a theory block."""

    from .Annotate import annotate_block_theory as annotate_block

    def __init__(self, **kwargs):
        self.name = kwargs.pop("name")
        self.vocab_name = kwargs.pop("vocab_name")
        constraints: List[Expression] = kwargs.pop("constraints")
        self.definitions = kwargs.pop("definitions")
        self.interpretations = self.dedup_nodes(kwargs, "interpretations")

        self.name = "T" if not self.name else self.name
        self.vocab_name = "V" if not self.vocab_name else self.vocab_name

        self.prefix = split_prefix(self.name)

        self.declarations = {}
        self.def_constraints = {}  # {(Declaration, Definition): List[Expression]}
        self.assignments = Assignments()

        self.constraints = OrderedSet()
        for c in constraints:
            if c.annotations is not None:
                c.expr.annotations = c.annotations.annotations
            self.constraints.append(c.expr)
        for definition in self.definitions:
            for rule in definition.rules:
                rule.block = self
        self.voc = None

    def __str__(self):
        return self.name


class Definition(Expression):
    """The class of AST nodes representing an inductive definition.

    Attributes:
        id (num): unique identifier for each definition

        rules ([Rule]):
            set of rules for the definition, e.g., `!x: p(x) <- q(x)`

        renamed (dict[Declaration, List[Rule]]):
            rules with normalized body for each defined symbol,
            e.g., `!x: p(x) <- q(p1_)`
            (quantees and head are unchanged)

        canonicals (dict[Declaration, List[Rule]]):
            normalized rule for each defined symbol,
            e.g., `! p1_: p(p1_) <- q(p1_)`

        clarks (dict[Declaration, Transformed Rule]):
            normalized rule for each defined symbol (used to be Clark completion)
            e.g., `! p1_: p(p1_) <=> q(p1_)`

        def_vars (dict[String, dict[String, Variable]]):
            Fresh variables for arguments and result

        inductive (set[SymbolDeclaration])
            set of SymbolDeclaration with an inductive definition

        cache (dict[SymbolDeclaration, str, Expression]):
            cache of instantiation of the definition

        inst_def_level (int): depth of recursion during instantiation

    """

    definition_id = (
        0  # intentional static variable so that no two definitions get the same ID
    )

    from .Annotate import annotate_definition as annotate
    from .Definition import get_def_constraints
    from .Definition import instantiate_definition_def as instantiate_definition
    from .EN import EN_definition as EN
    from .Interpret import interpret_definition as interpret

    def __init__(self, parent, annotations: Optional[Annotations], mode, rules):
        Definition.definition_id += 1
        self.id = Definition.definition_id
        self.mode = (
            S.WELLFOUNDED
            if mode is None or "well-founded" in mode
            else S.COMPLETION
            if "completion" in mode
            else S.KRIPKEKLEENE
            if "Kripke-Kleene" in mode
            else S.COINDUCTION
            if "co-induction" in mode
            else S.STABLE
            if "stable" in mode
            else S.RECDATA
            if "recursive" in mode
            else mode
        )
        assert type(self.mode) == S, f"Unsupported mode: {mode}"
        self.annotations: Annotation = annotations.annotations if annotations else {}
        self.rules: List[Rule] = rules
        self.renamed: dict[SymbolDeclaration, List[Rule]] = {}
        self.clarks: dict[SymbolDeclaration, Rule] = {}
        self.canonicals: dict[SymbolDeclaration, List[Rule]] = {}
        self.def_vars: dict[str, Variable] = {}
        self.inductive: set[SymbolDeclaration] = set()
        self.cache: dict[
            Tuple[Declaration, str], Expression
        ] = {}  # {decl, str: Expression}
        self.inst_def_level = 0

    def __str__(self):
        return (
            "Definition "
            + str(self.id)
            + " of "
            + ",".join([k.name for k in self.canonicals.keys()])
        )

    def __repr__(self):
        out = []
        for rule in self.clarks.values():
            out.append(repr(rule))
        return NEWL.join(out)

    def __eq__(self, another):
        return self.id == another.id

    def __hash__(self):
        return hash(self.id)

    def __deepcopy__(self, memo):
        cls = self.__class__  # Extract the Definition class
        out = cls.__new__(cls)  # Create a new instance of Definition
        memo[id(self)] = out
        out.__dict__.update(self.__dict__)

        out.rules = [deepcopy(x, memo) for x in self.rules]
        out.annotations = deepcopy(self.annotations, memo)
        out.canonicals = {x: deepcopy(y) for x, y in self.canonicals.items()}
        out.clarks = {x: deepcopy(y) for x, y in self.clarks.items()}
        out.mode = self.mode
        return out


class Rule(Expression):
    from .Annotate import annotate_rule as annotate
    from .Definition import instantiate_definition_rule as instantiate_definition
    from .EN import EN_rule as EN

    def __init__(
        self,
        parent,
        annotations: Annotations,
        quantees: List[Quantee],
        definiendum: AppliedSymbol,
        out: Expression,
        body: Expression,
    ):
        self.annotations: Annotation = (
            annotations.annotations if annotations else {"reading": str(self)}
        )
        self.quantees = quantees
        self.definiendum = definiendum
        self.out = out
        self.body = body
        self.has_finite_domain = None  # Bool
        self.block = None  # theory where it occurs

        split_quantees(self)

        if self.body is None:
            self.body = TRUE
        self.original: Optional[Rule] = None
        self.implication: Optional[Expression] = None  # rule in immlication form
        self.WDF: Optional[Expression] = None

    def __repr__(self):
        quant = (
            ""
            if not self.quantees
            else f"∀ {','.join(str(q) for q in self.quantees)}: "
        )
        return (
            f"{quant}{self.definiendum} "
            f"{(' = ' + str(self.out)) if self.out else ''}"
            f"← {str(self.body)}"
        )

    def __str__(self):
        return repr(self)

    def __deepcopy__(self, memo):
        cls = self.__class__  # Extract the class of the object
        out = cls.__new__(
            cls
        )  # Create a new instance of the object based on extracted class
        memo[id(self)] = out
        out.__dict__.update(self.__dict__)

        out.definiendum = deepcopy(self.definiendum)
        out.definiendum.sub_exprs = [deepcopy(e) for e in self.definiendum.sub_exprs]
        out.out = deepcopy(self.out)
        out.body = deepcopy(self.body)
        return out


# Expressions : see Expression.py

################################ Structure  ###############################


class Structure(ASTNode):
    """
    The class of AST nodes representing an structure block.
    """

    from .Annotate import annotate_block_struc as annotate_block

    def __init__(self, **kwargs):
        """
        The textx parser creates the Structure object. All information used in
        this method directly comes from text.
        """
        self.name = kwargs.pop("name")
        self.vocab_name = kwargs.pop("vocab_name")
        self.interpretations = self.dedup_nodes(kwargs, "interpretations")

        self.name = "S" if not self.name else self.name
        self.vocab_name = "V" if not self.vocab_name else self.vocab_name

        self.prefix = split_prefix(self.name)

        self.voc = None
        self.declarations = {}
        self.assignments = Assignments()

    def __str__(self):
        return self.name


class SymbolInterpretation(Expression):
    """
    AST node representing `<symbol> := { <identifiers*> } else <default>.`

    Attributes:
        name (string): name of the symbol being enumerated.

        symbol_decl (SymbolDeclaration): symbol being enumerated

        enumeration ([Enumeration]): enumeration.

        default (Expression): default value (for function enumeration).

        is_type_enumeration (Bool): True if the enumeration is for a type symbol.

    """

    from .Annotate import annotate_symbolinterpretation as annotate
    from .Interpret import interpret_symbolinterpretation as interpret

    def __init__(
        self,
        parent,
        name: UnappliedSymbol,
        sign: str,
        enumeration: Enumeration,
        default: Optional[Expression],
    ):
        self.name = name.name
        self.sign = sign
        self.enumeration = enumeration
        self.default = default

        self.prefix = split_prefix(self.name)

        if not self.enumeration:
            self.enumeration = Enumeration(parent=self, tuples=[])

        self.sign = (
            "⊇" if self.sign == ":>" else "≜" if self.sign == ":=" else self.sign
        )
        self.check(
            self.sign == "≜"
            or (type(self.enumeration) == FunctionEnum and self.default is None),
            "'⊇' can only be used with a functional enumeration ('→') without else clause",
        )

        self.symbol_decl: Optional[SymbolDeclaration] = None
        self.is_type_enumeration = None
        self.block = None

    def __repr__(self):
        return f"{self.name} {self.sign} {self.enumeration}"

    def interpret_application(self, rank, applied, args, tuples=None):
        """returns an expression equivalent to `self.symbol` applied to `args`,
        simplified by the interpretation of `self.symbol`.

        This is a recursive function.

        Example: assume `f:>{(1,2)->A, (1, 3)->B, (2,1)->C}` and `args=[g(1),2)]`.
        The returned expression is:
        ```
        if g(1) = 1 then A
        else if g(1)=2 then f(g(1),2)
        else f(g(1),2)
        ```

        Args:
            rank (Int): iteration number (from 0)

            applied (AppliedSymbol): template to create new AppliedSymbol
                (ex: `g(1),a()`, before interpretation)

            args (List(Expression)): interpreted arguments applied to the symbol (ex: `g(1),2`)

            tuples (OrderedSet[TupleIDP], optional): relevant tuples for this iteration.
                Initialized with `[[1,2,A], [1,3,B], [2,1,C]]`

        Returns:
            Expression: Grounded interpretation of self.symbol applied to args
        """
        if tuples == None:
            tuples = self.enumeration.sorted_tuples
            if all(a.is_value() for a in args):  # use lookup
                key = ",".join(a.code for a in args)
                if key in self.enumeration.lookup:
                    return self.enumeration.lookup[key]
                elif self.sign == "≜":  # can use default
                    return self.default

        if rank == self.symbol_decl.arity:  # valid tuple -> return a value
            if not type(self.enumeration) == FunctionEnum:
                return TRUE if tuples else self.default
            else:
                self.check(
                    len(tuples) <= 1,
                    f"Duplicate values in structure "
                    f"for {str(self.name)}{str(tuples[0])}",
                )
                return (
                    self.default
                    if not tuples
                    # enumeration of constant
                    else tuples[0].args[rank]
                )
        else:  # constructs If-then-else recursively
            out = (
                self.default
                if self.default is not None
                else applied._change(sub_exprs=args)
            )
            groups = groupby(tuples, key=lambda t: str(t.args[rank]))

            if args[rank].is_value():
                for val, tuples2 in groups:  # try to resolve
                    if str(args[rank]) == val:
                        out = self.interpret_application(
                            rank + 1, applied, args, list(tuples2)
                        )
            else:
                for val, tuples2 in groups:
                    tuples = list(tuples2)
                    out = IF(
                        EQUALS([args[rank], tuples[0].args[rank]]),
                        self.interpret_application(rank + 1, applied, args, tuples),
                        out,
                    )
            return out


class Enumeration(Expression):
    """Represents an enumeration of tuples of expressions.
    Used for predicates, or types without n-ary constructors.

    Attributes:
        tuples (OrderedSet[TupleIDP]): OrderedSet of TupleIDP of Expression

        sorted_tuples: a sorted list of tuples

        lookup: dictionary from arguments to values

        constructors (List[Constructor], optional): List of Constructor
    """

    from .Annotate import annotate_enumeration as annotate
    from .Interpret import interpret_enumeration as interpret

    def __init__(self, parent: ASTNode, tuples: List[TupleIDP]):
        self.sorted_tuples = sorted(
            tuples, key=lambda t: t.code
        )  # do not change dropdown order
        self.tuples: Optional[OrderedSet] = OrderedSet(tuples)

        self.lookup: dict[str, Expression] = {}
        self.constructors: Optional[List[Constructor]]
        if all(
            len(c.args) == 1 and type(c.args[0]) == UnappliedSymbol for c in self.tuples
        ):
            self.constructors = [CONSTRUCTOR(c.args[0].name) for c in self.tuples]
        else:
            self.constructors = None

    def __repr__(self):
        return (
            f'{{{", ".join([repr(t) for t in self.tuples])}}}'
            if self.tuples
            else f'{{{", ".join([repr(t) for t in self.constructors])}}}'
        )

    def contains(
        self,
        args,
        arity: Optional[int] = None,
        rank: int = 0,
        tuples: Optional[List[TupleIDP]] = None,
        theory: Optional[Theory] = None,
    ) -> Expression:
        """returns an Expression that says whether Tuple args is in the enumeration"""

        if arity is None:
            arity = len(args)
        if rank == arity:  # valid tuple
            return TRUE
        if tuples is None:
            tuples = self.sorted_tuples

        # constructs If-then-else recursively
        groups = groupby(tuples, key=lambda t: str(t.args[rank]))
        if args[rank].is_value():
            for val, tuples2 in groups:  # try to resolve
                if str(args[rank]) == val:
                    return self.contains(
                        args, arity, rank + 1, list(tuples2), theory=theory
                    )
            return FALSE
        else:
            if rank + 1 == arity:  # use OR
                equalities = [EQUALS([args[rank], t.args[rank]]) for t in tuples]
                out = OR(equalities)
                out.enumerated = ", ".join(str(c) for c in tuples)
                return out
            out = FALSE
            for val, tuples2 in groups:
                tuples = list(tuples2)
                out = IF(
                    EQUALS([args[rank], tuples[0].args[rank]]),
                    self.contains(args, arity, rank + 1, tuples, theory),
                    out,
                )
            return out

    def extensionE(
        self, extensions: Optional[dict[str, Extension]] = None
    ) -> Extension:
        """computes the extension of an enumeration, i.e., a set of tuples and a filter

        Args:
            interpretations (dict[str, &quot;SymbolInterpretation&quot;], optional): _description_. Defaults to None.
            extensions (dict[str, Extension], optional): _description_. Defaults to None.

        Returns:
            Extension: _description_
        """
        # assert all(c.range is not None for c in self.constructors)
        ranges = [c.range for c in self.constructors]
        return ([[t] for r in ranges for t in r], None)


class FunctionEnum(Enumeration):
    def extensionE(
        self, extensions: Optional[dict[str, Extension]] = None
    ) -> Extension:
        self.check(
            False,
            f"Can't use function enumeration for type declaration or quantification",
        )
        return (None, None)  # dead code


class CSVEnumeration(Enumeration):
    pass


class ConstructedFrom(Enumeration):
    """Represents a 'constructed from' enumeration of constructors

    Attributes:
        tuples (OrderedSet[TupleIDP], Optional): OrderedSet of tuples of Expression

        constructors (List[Constructor]): List of Constructor

        accessors (dict[str, int]): index of the accessor in the constructors
    """

    from .Annotate import annotate_constructedfrom as annotate
    from .Interpret import interpret_constructedfrom as interpret

    def __init__(
        self,
        parent: Optional[ASTNode],
        constructed: str,
        constructors: List[Constructor],
    ):
        self.constructed = constructed
        self.constructors = constructors
        self.tuples: Optional[OrderedSet] = None
        self.accessors: dict[str, int] = dict()

    def contains(
        self,
        args,
        arity: Optional[int] = None,
        rank: int = 0,
        tuples: Optional[List[TupleIDP]] = None,
        theory: Optional[Theory] = None,
    ) -> Expression:
        """returns True if args belong to the type enumeration"""
        # args must satisfy the tester of one of the constructors
        # TODO add tests
        assert len(args) == 1, f"Incorrect arity in {self.parent.name}{args}"
        if type(args[0].decl) == Constructor:  # try to simplify it
            self.check(
                self.parent.name == args[0].decl.codomain,
                f"Incorrect type of {args[0]} for {self.parent.name}",
            )
            self.check(
                len(args[0].sub_exprs) == len(args[0].decl.domains), f"Incorrect arity"
            )
            return AND(
                [
                    t.decl.codomain.has_element(e, theory.extensions)
                    for e, t in zip(args[0].sub_exprs, args[0].decl.domains)
                ]
            )
        out = [
            AppliedSymbol.construct(constructor.tester, args)
            for constructor in self.constructors
        ]
        return OR(out)

    def extensionE(
        self, extensions: Optional[dict[str, Extension]] = None
    ) -> Extension:
        def filter(args):
            if (
                type(args[0]) != Variable and type(args[0].decl) == Constructor
            ):  # try to simplify it
                # TODO add tests
                self.check(
                    self.parent.name == args[0].decl.codomain.name,
                    f"Incorrect type of {args[0]} for {self.parent.name}",
                )
                self.check(
                    len(args[0].sub_exprs) == len(args[0].decl.domains),
                    f"Incorrect arity",
                )
                return AND(
                    [
                        t.decl.domains[0].has_element(e, extensions)
                        for e, t in zip(args[0].sub_exprs, args[0].decl.domains)
                    ]
                )
            out = [
                AppliedSymbol.construct(constructor.tester, args)
                for constructor in self.constructors
            ]
            return OR(out)  # return of filter()

        return ([t.args for t in self.tuples], None) if self.tuples else (None, filter)


class TupleIDP(Expression):
    from .Annotate import annotate_tupleidp as annotate
    from .Idp_to_Z3 import translate_tupleidp as translate

    def __init__(self, **kwargs):
        self.args: List[Identifier] = kwargs.pop("args")
        self.code = intern(",".join([str(a) for a in self.args]))

    def __str__(self):
        return self.code

    def __repr__(self):
        return f"({self.code})" if 1 < len(self.args) else self.code


class FunctionTuple(TupleIDP):
    def __init__(self, **kwargs):
        self.args = kwargs.pop("args")
        if not isinstance(self.args, list):
            self.args = [self.args]
        self.value = kwargs.pop("value")
        self.args.append(self.value)
        self.code = intern(",".join([str(a) for a in self.args]))


class CSVTuple(TupleIDP):
    pass


class Ranges(Enumeration):
    def __init__(self, parent: ASTNode, **kwargs):
        self.elements = kwargs.pop("elements")

        tuples: List[TupleIDP] = []
        self.type: Optional[SetName] = None
        if self.elements:
            self.type = self.elements[0].fromI.type
            for x in self.elements:
                if x.fromI.type != self.type:
                    if self.type in [INT_SETNAME, REAL_SETNAME] and x.fromI.type in [
                        INT_SETNAME,
                        REAL_SETNAME,
                    ]:
                        self.type = REAL_SETNAME  # convert to REAL
                        tuples = [TupleIDP(args=[n.args[0].real()]) for n in tuples]
                    else:
                        self.check(False, f"incorrect value {x.fromI} for {self.type}")

                if x.toI is None:
                    tuples.append(TupleIDP(args=[x.fromI]))
                elif (
                    self.type == INT_SETNAME
                    and x.fromI.type == INT_SETNAME
                    and x.toI.type == INT_SETNAME
                ):
                    for i in range(x.fromI.py_value, x.toI.py_value + 1):
                        tuples.append(TupleIDP(args=[Number(number=str(i))]))
                elif (
                    self.type == REAL_SETNAME
                    and x.fromI.type == INT_SETNAME
                    and x.toI.type == INT_SETNAME
                ):
                    for i in range(x.fromI.py_value, x.toI.py_value + 1):
                        tuples.append(TupleIDP(args=[Number(number=str(float(i)))]))
                elif self.type == REAL_SETNAME:
                    self.check(
                        False, f"Can't have a range over real: {x.fromI}..{x.toI}"
                    )
                elif (
                    self.type == DATE_SETNAME
                    and x.fromI.type == DATE_SETNAME
                    and x.toI.type == DATE_SETNAME
                ):
                    for i in range(x.fromI.py_value, x.toI.py_value + 1):
                        d = Date(iso=f"#{date.fromordinal(i).isoformat()}")
                        tuples.append(TupleIDP(args=[d]))
                else:
                    self.check(False, f"Incorrect value {x.toI} for {self.type}")
        Enumeration.__init__(self, parent=parent, tuples=tuples)

    def contains(
        self,
        args,
        arity: Optional[int] = None,
        rank: int = 0,
        tuples: Optional[List[TupleIDP]] = None,
        theory: Optional[Theory] = None,
    ) -> Expression:
        var = args[0]
        if not self.elements:
            return TRUE
        if self.tuples and len(self.tuples) < MAX_QUANTIFIER_EXPANSION:
            es = [EQUALS([var, c.args[0]]) for c in self.tuples]
            e = OR(es)
            return e
        sub_exprs = []
        for x in self.elements:
            if x.toI is None:
                e = EQUALS([var, x.fromI])
            else:
                e = AComparison.make("≤", [x.fromI, var, x.toI])
            sub_exprs.append(e)
        return OR(sub_exprs)

    def extensionE(
        self, extensions: Optional[dict[str, Extension]] = None
    ) -> Extension:
        if not self.elements:
            return (None, None)
        if self.tuples is not None:  # and len(self.tuples) < MAX_QUANTIFIER_EXPANSION:
            return ([t.args for t in self.tuples], None)

        def filter(args):
            sub_exprs = []
            for x in self.elements:
                if x.toI is None:
                    e = EQUALS([args[0], x.fromI])
                else:
                    e = AComparison.make("≤", [x.fromI, args[0], x.toI])
                sub_exprs.append(e)
            return OR(sub_exprs)

        return (None, filter)


class RangeElement(Expression):
    def __init__(self, **kwargs):
        self.fromI = kwargs.pop("fromI")
        self.toI = kwargs.pop("toI")


class IntRange(Ranges):
    def __init__(self):
        Ranges.__init__(self, parent=self, elements=[])
        self.type = INT_SETNAME
        self.tuples = None

    def extensionE(
        self, extensions: Optional[dict[str, Extension]] = None
    ) -> Extension:
        return (None, None)


class RealRange(Ranges):
    def __init__(self):
        Ranges.__init__(self, parent=self, elements=[])
        self.type = REAL_SETNAME
        self.tuples = None

    def extensionE(
        self, extensions: Optional[dict[str, Extension]] = None
    ) -> Extension:
        return (None, None)


class DateRange(Ranges):
    def __init__(self):
        Ranges.__init__(self, parent=self, elements=[])
        self.type = DATE_SETNAME
        self.tuples = None

    def extensionE(
        self, extensions: Optional[dict[str, Extension]] = None
    ) -> Extension:
        return (None, None)


################################ Display  ###############################


class Display(ASTNode):
    from .Annotate import annotate_block_display as annotate_block

    def __init__(self, **kwargs):
        self.constraints = kwargs.pop("constraints")
        self.interpretations = self.dedup_nodes(kwargs, "interpretations")
        self.moveSymbols = False
        self.optionalPropagation = False
        self.manualPropagation = False
        self.optionalRelevance = False
        self.manualRelevance = False
        self.introduction: str = ""
        self.name = "display"
        self.voc = None

    def run(self, idp):
        """Apply the display block to the idp theory"""

        def base_symbols(name, concepts) -> list[SymbolDeclaration]:
            """Verify that concepts is a list of concepts.
            Returns the list of symbol declarations."""
            symbols = []
            # All concepts should be concepts, except for the first
            # argument of 'unit' and 'heading'. 'introduction' can also be
            # ignored, as it always contains text.
            for i, symbol in enumerate(concepts):
                if name in ["unit", "heading"] and i == 0:
                    continue
                elif name == "introduction":
                    continue
                self.check(
                    symbol.name.startswith("`"),
                    f"arg '{symbol.name}' of {name}'" f" must begin with a tick '`'",
                )
                self.check(
                    symbol.name[1:] in self.voc.symbol_decls,
                    f"argument '{symbol.name}' of '{name}'" f" must be a concept",
                )
                symbols.append(self.voc.symbol_decls[symbol.name[1:]])
            return symbols

        for k, interpretation in self.interpretations.items():
            symbols = base_symbols(
                interpretation.name,
                [t.args[0] for t in interpretation.enumeration.tuples],
            )
            if interpretation.name == EXPAND:
                for symbol in symbols:
                    self.voc.symbol_decls[symbol.name].view = ViewType.EXPANDED
            elif interpretation.name == GOAL_SYMBOL:
                idp.theory.interpretations[k] = interpretation
            elif interpretation.name == COUNTER:
                for symbol in symbols:
                    self.voc.symbol_decls[symbol.name].counter = True
            else:
                raise IDPZ3Error(f"Unknown enumeration in display: {interpretation}")
        for constraint in self.constraints:
            if type(constraint) == AppliedSymbol:
                self.check(
                    constraint.symbol.name, f"Invalid syntax: {constraint}"
                )  # SymbolExpr $()
                name = constraint.symbol.name
                symbols = base_symbols(name, constraint.sub_exprs)

                if name == "hide":  # e.g. hide(Length, Angle)
                    for symbol in symbols:
                        self.voc.symbol_decls[symbol.name].view = ViewType.HIDDEN
                elif name in [GOAL_SYMBOL, EXPAND]:  # e.g. goal_symbol(`tax_amount`)
                    self.check(False, f"Please use an enumeration for {name}")
                elif name == "unit":  # e.g. unit('m', `length):
                    for symbol in symbols:
                        symbol.unit = str(constraint.sub_exprs[0])
                elif name == "heading":
                    # e.g. heading('Shape', `type).
                    for symbol in symbols:
                        symbol.heading = str(constraint.sub_exprs[0])
                elif name == "noOptimization":  # e.g., noOptimization(`temp)
                    for symbol in symbols:
                        symbol.optimizable = False
                elif name == "moveSymbols":
                    self.moveSymbols = True
                elif name == "optionalPropagation":
                    self.optionalPropagation = True
                elif name == "manualPropagation":
                    self.manualPropagation = True
                elif name == "optionalRelevance":
                    self.optionalRelevance = True
                elif name == "manualRelevance":
                    self.manualRelevance = True
                elif name == "introduction":
                    self.introduction = str(constraint.sub_exprs[0])
                else:
                    raise IDPZ3Error(f"Unknown display axiom:" f" {constraint}")
            elif type(constraint) == AComparison:  # e.g. view = normal
                self.check(constraint.is_assignment(), "Internal error")
                self.check(
                    constraint.sub_exprs[0].symbol.name, f"Invalid syntax: {constraint}"
                )
                if constraint.sub_exprs[0].symbol.name == "view":
                    if constraint.sub_exprs[1].name == "expanded":
                        for s in self.voc.symbol_decls.values():
                            if (
                                type(s) == SymbolDeclaration
                                and s.view == ViewType.NORMAL
                            ):
                                s.view = (
                                    ViewType.EXPANDED
                                )  # don't change hidden symbols
                    else:
                        self.check(
                            constraint.sub_exprs[1].name == "normal",
                            f"Unknown display axiom: {constraint}",
                        )
            else:
                raise IDPZ3Error(f"Unknown display axiom: {constraint}")


################################ Main  ##################################


class Procedure(ASTNode):
    def __init__(self, **kwargs):
        self.name = kwargs.pop("name")
        self.args = kwargs.pop("args")
        self.pystatements = kwargs.pop("pystatements")

    def __str__(self):
        return f"{NEWL.join(str(s) for s in self.pystatements)}"


class Call1(ASTNode):
    def __init__(self, **kwargs):
        self.name = kwargs.pop("name")
        self.par = kwargs.pop("par") if "par" in kwargs else None
        self.args = kwargs.pop("args")
        self.kwargs = kwargs.pop("kwargs")
        self.post = kwargs.pop("post")

    def __str__(self):
        kwargs = (
            ""
            if len(self.kwargs) == 0
            else f"{',' if self.args else ''}{','.join(str(a) for a in self.kwargs)}"
        )
        args = (
            "" if not self.par else f"({','.join(str(a) for a in self.args)}{kwargs})"
        )
        return f"{self.name}{args}" f"{'' if self.post is None else '.'+str(self.post)}"


class String(ASTNode):
    def __init__(self, **kwargs):
        self.literal = kwargs.pop("literal")

    def __str__(self):
        return f"{self.literal}"


class PyList(ASTNode):
    def __init__(self, **kwargs):
        self.elements = kwargs.pop("elements")

    def __str__(self):
        return f"[{','.join(str(e) for e in self.elements)}]"


class PyAssignment(ASTNode):
    def __init__(self, **kwargs):
        self.var = kwargs.pop("var")
        self.val = kwargs.pop("val")

    def __str__(self):
        return f"{self.var} = {self.val}"


########################################################################

Block = Union[Vocabulary, TheoryBlock, Structure, Display]

dslFile = path.join(path.dirname(__file__), "Idp.tx")

idpparser = metamodel_from_file(
    dslFile,
    memoization=True,
    classes=[
        IDP,
        Annotations,
        Vocabulary,
        Import,
        VarDeclaration,
        TypeDeclaration,
        Accessor,
        SetName,
        SymbolDeclaration,
        SymbolExpr,
        TheoryBlock,
        Definition,
        Rule,
        AIfExpr,
        AGenExist,
        AQuantification,
        Quantee,
        ARImplication,
        AEquivalence,
        AImplication,
        ADisjunction,
        AConjunction,
        AComparison,
        ASumMinus,
        AMultDiv,
        APower,
        AUnary,
        AAggregate,
        AExtAggregate,
        AppliedSymbol,
        UnappliedSymbol,
        Number,
        Brackets,
        Date,
        Variable,
        Structure,
        SymbolInterpretation,
        Enumeration,
        FunctionEnum,
        CSVEnumeration,
        TupleIDP,
        FunctionTuple,
        CSVTuple,
        ConstructedFrom,
        Constructor,
        Ranges,
        RangeElement,
        Display,
        Procedure,
        Call1,
        String,
        PyList,
        PyAssignment,
    ],
)
