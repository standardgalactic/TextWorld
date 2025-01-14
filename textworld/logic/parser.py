#!/usr/bin/env python

# CAVEAT UTILITOR
#
# This file was automatically generated by TatSu.
#
#    https://pypi.python.org/pypi/tatsu/
#
# Any changes you make to it will be overwritten the next time
# the file is generated.

from __future__ import annotations

import sys

from tatsu.buffering import Buffer
from tatsu.parsing import Parser
from tatsu.parsing import tatsumasu
from tatsu.parsing import leftrec, nomemo, isname # noqa
from tatsu.infos import ParserConfig
from tatsu.util import re, generic_main  # noqa


KEYWORDS = {}  # type: ignore


class GameLogicBuffer(Buffer):
    def __init__(self, text, /, config: ParserConfig = None, **settings):
        config = ParserConfig.new(
            config,
            owner=self,
            whitespace=None,
            nameguard=None,
            comments_re=None,
            eol_comments_re='#.*?$',
            ignorecase=False,
            namechars='',
            parseinfo=False,
        )
        config = config.replace(**settings)
        super().__init__(text, config=config)


class GameLogicParser(Parser):
    def __init__(self, /, config: ParserConfig = None, **settings):
        config = ParserConfig.new(
            config,
            owner=self,
            whitespace=None,
            nameguard=None,
            comments_re=None,
            eol_comments_re='#.*?$',
            ignorecase=False,
            namechars='',
            parseinfo=False,
            keywords=KEYWORDS,
            start='start',
        )
        config = config.replace(**settings)
        super().__init__(config=config)

    @tatsumasu()
    def _start_(self):  # noqa
        self._document_()

    @tatsumasu()
    def _str_(self):  # noqa
        self._pattern('"[^"]*"')

    @tatsumasu()
    def _strBlock_(self):  # noqa
        self._pattern('"""(?:.|\\n)*?"""')

    @tatsumasu()
    def _name_(self):  # noqa
        self._pattern('\\w+')

    @tatsumasu()
    def _phName_(self):  # noqa
        self._pattern("[\\w']+")

    @tatsumasu()
    def _predName_(self):  # noqa
        self._pattern('[\\w/]+')

    @tatsumasu()
    def _ruleName_(self):  # noqa
        self._pattern('[\\w/]+')

    @tatsumasu('VariableNode')
    def _variable_(self):  # noqa
        self._name_()
        self.name_last_node('name')
        with self._optional():
            self._token(':')
            self._name_()
            self.name_last_node('type')

            self._define(
                ['type'],
                []
            )

        self._define(
            ['name', 'type'],
            []
        )

    @tatsumasu('SignatureNode')
    def _signature_(self):  # noqa
        self._predName_()
        self.name_last_node('name')
        self._token('(')

        def sep2():
            self._token(',')

        def block2():
            self._name_()
        self._gather(block2, sep2)
        self.name_last_node('types')
        self._token(')')

        self._define(
            ['name', 'types'],
            []
        )

    @tatsumasu('PropositionNode')
    def _proposition_(self):  # noqa
        self._predName_()
        self.name_last_node('name')
        self._token('(')

        def sep2():
            self._token(',')

        def block2():
            self._variable_()
        self._gather(block2, sep2)
        self.name_last_node('arguments')
        self._token(')')

        self._define(
            ['arguments', 'name'],
            []
        )

    @tatsumasu('ActionPreconditionNode')
    def _actionPrecondition_(self):  # noqa
        with self._optional():
            self._token('$')
        self.name_last_node('preserve')
        self._proposition_()
        self.name_last_node('condition')

        self._define(
            ['condition', 'preserve'],
            []
        )

    @tatsumasu('ActionNode')
    def _action_(self):  # noqa
        self._ruleName_()
        self.name_last_node('name')
        self._token('::')

        def sep2():
            self._token('&')

        def block2():
            self._actionPrecondition_()
        self._positive_gather(block2, sep2)
        self.name_last_node('preconditions')
        self._token('->')

        def sep4():
            self._token('&')

        def block4():
            self._proposition_()
        self._positive_gather(block4, sep4)
        self.name_last_node('postconditions')

        self._define(
            ['name', 'postconditions', 'preconditions'],
            []
        )

    @tatsumasu('PlaceholderNode')
    def _placeholder_(self):  # noqa
        self._phName_()
        self.name_last_node('name')
        with self._optional():
            self._token(':')
            self._name_()
            self.name_last_node('type')

            self._define(
                ['type'],
                []
            )

        self._define(
            ['name', 'type'],
            []
        )

    @tatsumasu('PredicateNode')
    def _predicate_(self):  # noqa
        self._predName_()
        self.name_last_node('name')
        self._token('(')

        def sep2():
            self._token(',')

        def block2():
            self._placeholder_()
        self._gather(block2, sep2)
        self.name_last_node('parameters')
        self._token(')')

        self._define(
            ['name', 'parameters'],
            []
        )

    @tatsumasu('RulePreconditionNode')
    def _rulePrecondition_(self):  # noqa
        with self._optional():
            self._token('$')
        self.name_last_node('preserve')
        self._predicate_()
        self.name_last_node('condition')

        self._define(
            ['condition', 'preserve'],
            []
        )

    @tatsumasu('RuleNode')
    def _rule_(self):  # noqa
        self._ruleName_()
        self.name_last_node('name')
        self._token('::')

        def sep2():
            self._token('&')

        def block2():
            self._rulePrecondition_()
        self._positive_gather(block2, sep2)
        self.name_last_node('preconditions')
        self._token('->')

        def sep4():
            self._token('&')

        def block4():
            self._predicate_()
        self._positive_gather(block4, sep4)
        self.name_last_node('postconditions')

        self._define(
            ['name', 'postconditions', 'preconditions'],
            []
        )

    @tatsumasu('AliasNode')
    def _alias_(self):  # noqa
        self._predicate_()
        self.name_last_node('lhs')
        self._token('=')

        def sep2():
            self._token('&')

        def block2():
            self._predicate_()
        self._positive_gather(block2, sep2)
        self.name_last_node('rhs')

        self._define(
            ['lhs', 'rhs'],
            []
        )

    @tatsumasu()
    def _signatureOrAlias_(self):  # noqa
        with self._choice():
            with self._option():
                self._alias_()
            with self._option():
                self._signature_()
            self._error(
                'expecting one of: '
                '<alias> <predName> <predicate>'
                '<signature> [\\w/]+'
            )

    @tatsumasu('ReverseRuleNode')
    def _reverseRule_(self):  # noqa
        self._ruleName_()
        self.name_last_node('lhs')
        self._token('::')
        self._ruleName_()
        self.name_last_node('rhs')

        self._define(
            ['lhs', 'rhs'],
            []
        )

    @tatsumasu()
    def _predicateDecls_(self):  # noqa

        def block0():
            self._signatureOrAlias_()
            self.add_last_node_to_name('@')
            self._token(';')
        self._closure(block0)

    @tatsumasu('PredicatesNode')
    def _predicates_(self):  # noqa
        self._token('predicates')
        self._token('{')
        self._predicateDecls_()
        self.name_last_node('predicates')
        self._token('}')

        self._define(
            ['predicates'],
            []
        )

    @tatsumasu()
    def _ruleDecls_(self):  # noqa

        def block0():
            self._rule_()
            self.add_last_node_to_name('@')
            self._token(';')
        self._closure(block0)

    @tatsumasu('RulesNode')
    def _rules_(self):  # noqa
        self._token('rules')
        self._token('{')
        self._ruleDecls_()
        self.name_last_node('rules')
        self._token('}')

        self._define(
            ['rules'],
            []
        )

    @tatsumasu()
    def _reverseRuleDecls_(self):  # noqa

        def block0():
            self._reverseRule_()
            self.add_last_node_to_name('@')
            self._token(';')
        self._closure(block0)

    @tatsumasu('ReverseRulesNode')
    def _reverseRules_(self):  # noqa
        self._token('reverse_rules')
        self._token('{')
        self._reverseRuleDecls_()
        self.name_last_node('reverse_rules')
        self._token('}')

        self._define(
            ['reverse_rules'],
            []
        )

    @tatsumasu('ConstraintsNode')
    def _constraints_(self):  # noqa
        self._token('constraints')
        self._token('{')
        self._ruleDecls_()
        self.name_last_node('constraints')
        self._token('}')

        self._define(
            ['constraints'],
            []
        )

    @tatsumasu('Inform7TypeNode')
    def _inform7Type_(self):  # noqa
        self._token('type')
        self._token('{')
        self._token('kind')
        self._token('::')
        self._str_()
        self.name_last_node('kind')
        self._token(';')
        with self._optional():
            self._token('definition')
            self._token('::')
            self._str_()
            self.name_last_node('definition')
            self._token(';')

            self._define(
                ['definition'],
                []
            )
        self._token('}')

        self._define(
            ['definition', 'kind'],
            []
        )

    @tatsumasu('Inform7PredicateNode')
    def _inform7Predicate_(self):  # noqa
        self._predicate_()
        self.name_last_node('predicate')
        self._token('::')
        self._str_()
        self.name_last_node('source')
        self._token(';')

        self._define(
            ['predicate', 'source'],
            []
        )

    @tatsumasu('Inform7PredicatesNode')
    def _inform7Predicates_(self):  # noqa
        self._token('predicates')
        self._token('{')

        def block1():
            self._inform7Predicate_()
        self._closure(block1)
        self.name_last_node('predicates')
        self._token('}')

        self._define(
            ['predicates'],
            []
        )

    @tatsumasu('Inform7CommandNode')
    def _inform7Command_(self):  # noqa
        self._ruleName_()
        self.name_last_node('rule')
        self._token('::')
        self._str_()
        self.name_last_node('command')
        self._token('::')
        self._str_()
        self.name_last_node('event')
        self._token(';')

        self._define(
            ['command', 'event', 'rule'],
            []
        )

    @tatsumasu('Inform7CommandsNode')
    def _inform7Commands_(self):  # noqa
        self._token('commands')
        self._token('{')

        def block1():
            self._inform7Command_()
        self._closure(block1)
        self.name_last_node('commands')
        self._token('}')

        self._define(
            ['commands'],
            []
        )

    @tatsumasu('Inform7CodeNode')
    def _inform7Code_(self):  # noqa
        self._token('code')
        self._token('::')
        self._strBlock_()
        self.name_last_node('code')
        self._token(';')

        self._define(
            ['code'],
            []
        )

    @tatsumasu()
    def _inform7Part_(self):  # noqa
        with self._choice():
            with self._option():
                self._inform7Type_()
            with self._option():
                self._inform7Predicates_()
            with self._option():
                self._inform7Commands_()
            with self._option():
                self._inform7Code_()
            self._error(
                'expecting one of: '
                "'code' 'commands' 'predicates' 'type'"
                '<inform7Code> <inform7Commands>'
                '<inform7Predicates> <inform7Type>'
            )

    @tatsumasu('Inform7Node')
    def _inform7_(self):  # noqa
        self._token('inform7')
        self._token('{')

        def block1():
            self._inform7Part_()
        self._closure(block1)
        self.name_last_node('parts')
        self._token('}')

        self._define(
            ['parts'],
            []
        )

    @tatsumasu()
    def _typePart_(self):  # noqa
        with self._choice():
            with self._option():
                self._predicates_()
            with self._option():
                self._rules_()
            with self._option():
                self._reverseRules_()
            with self._option():
                self._constraints_()
            with self._option():
                self._inform7_()
            self._error(
                'expecting one of: '
                "'constraints' 'inform7' 'predicates'"
                "'reverse_rules' 'rules' <reverseRules>"
            )

    @tatsumasu('TypeNode')
    def _type_(self):  # noqa
        self._token('type')
        self._name_()
        self.name_last_node('name')
        with self._optional():
            self._token(':')

            def sep2():
                self._token(',')

            def block2():
                self._name_()
            self._positive_gather(block2, sep2)
            self.name_last_node('supertypes')

            self._define(
                ['supertypes'],
                []
            )
        self._token('{')

        def block4():
            self._typePart_()
        self._closure(block4)
        self.name_last_node('parts')
        self._token('}')

        self._define(
            ['name', 'parts', 'supertypes'],
            []
        )

    @tatsumasu('DocumentNode')
    def _document_(self):  # noqa

        def block1():
            self._type_()
        self._closure(block1)
        self.name_last_node('types')
        self._check_eof()

        self._define(
            ['types'],
            []
        )

    @tatsumasu()
    def _onlyVariable_(self):  # noqa
        self._variable_()
        self.name_last_node('@')
        self._check_eof()

    @tatsumasu()
    def _onlySignature_(self):  # noqa
        self._signature_()
        self.name_last_node('@')
        self._check_eof()

    @tatsumasu()
    def _onlyProposition_(self):  # noqa
        self._proposition_()
        self.name_last_node('@')
        self._check_eof()

    @tatsumasu()
    def _onlyPlaceholder_(self):  # noqa
        self._placeholder_()
        self.name_last_node('@')
        self._check_eof()

    @tatsumasu()
    def _onlyPredicate_(self):  # noqa
        self._predicate_()
        self.name_last_node('@')
        self._check_eof()

    @tatsumasu()
    def _onlyAction_(self):  # noqa
        self._action_()
        self.name_last_node('@')
        self._check_eof()

    @tatsumasu()
    def _onlyRule_(self):  # noqa
        self._rule_()
        self.name_last_node('@')
        self._check_eof()


class GameLogicSemantics:
    def start(self, ast):  # noqa
        return ast

    def str(self, ast):  # noqa
        return ast

    def strBlock(self, ast):  # noqa
        return ast

    def name(self, ast):  # noqa
        return ast

    def phName(self, ast):  # noqa
        return ast

    def predName(self, ast):  # noqa
        return ast

    def ruleName(self, ast):  # noqa
        return ast

    def variable(self, ast):  # noqa
        return ast

    def signature(self, ast):  # noqa
        return ast

    def proposition(self, ast):  # noqa
        return ast

    def actionPrecondition(self, ast):  # noqa
        return ast

    def action(self, ast):  # noqa
        return ast

    def placeholder(self, ast):  # noqa
        return ast

    def predicate(self, ast):  # noqa
        return ast

    def rulePrecondition(self, ast):  # noqa
        return ast

    def rule(self, ast):  # noqa
        return ast

    def alias(self, ast):  # noqa
        return ast

    def signatureOrAlias(self, ast):  # noqa
        return ast

    def reverseRule(self, ast):  # noqa
        return ast

    def predicateDecls(self, ast):  # noqa
        return ast

    def predicates(self, ast):  # noqa
        return ast

    def ruleDecls(self, ast):  # noqa
        return ast

    def rules(self, ast):  # noqa
        return ast

    def reverseRuleDecls(self, ast):  # noqa
        return ast

    def reverseRules(self, ast):  # noqa
        return ast

    def constraints(self, ast):  # noqa
        return ast

    def inform7Type(self, ast):  # noqa
        return ast

    def inform7Predicate(self, ast):  # noqa
        return ast

    def inform7Predicates(self, ast):  # noqa
        return ast

    def inform7Command(self, ast):  # noqa
        return ast

    def inform7Commands(self, ast):  # noqa
        return ast

    def inform7Code(self, ast):  # noqa
        return ast

    def inform7Part(self, ast):  # noqa
        return ast

    def inform7(self, ast):  # noqa
        return ast

    def typePart(self, ast):  # noqa
        return ast

    def type(self, ast):  # noqa
        return ast

    def document(self, ast):  # noqa
        return ast

    def onlyVariable(self, ast):  # noqa
        return ast

    def onlySignature(self, ast):  # noqa
        return ast

    def onlyProposition(self, ast):  # noqa
        return ast

    def onlyPlaceholder(self, ast):  # noqa
        return ast

    def onlyPredicate(self, ast):  # noqa
        return ast

    def onlyAction(self, ast):  # noqa
        return ast

    def onlyRule(self, ast):  # noqa
        return ast


def main(filename, **kwargs):
    if not filename or filename == '-':
        text = sys.stdin.read()
    else:
        with open(filename) as f:
            text = f.read()
    parser = GameLogicParser()
    return parser.parse(
        text,
        filename=filename,
        **kwargs
    )


if __name__ == '__main__':
    import json
    from tatsu.util import asjson

    ast = generic_main(main, GameLogicParser, name='GameLogic')
    data = asjson(ast)
    print(json.dumps(data, indent=2))
