from pydantic import BaseModel


class GrammarIssue(BaseModel):
    original:str
    issue:str
    suggestion:str


class WeakVerbIssue(BaseModel):
    original:str
    weak_word:str
    suggestion:str


class SuggestionIssue(BaseModel):
    issue:str
    suggestion:str


class LackingIssue(BaseModel):
    issue:str
    suggestion:str


class PremiumSummary(BaseModel):
    grammar_count:int
    weak_verbs_count:int
    suggestion_count:int
    lacking_count:int


class PremiumAssessment(BaseModel):

    summary:PremiumSummary

    grammar:list[GrammarIssue]

    weak_verbs:list[WeakVerbIssue]

    suggestions:list[SuggestionIssue]

    lacking:list[LackingIssue]