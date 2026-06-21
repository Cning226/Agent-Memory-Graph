"""Tests for composable memory-ranking scores."""

from agentmemgraph.core.value_base import ValueBase


class CredibilityOnly(ValueBase):
    def __init__(self):
        self.value_threshold = 0

    def compute_importance(self, Importance: float) -> float:
        return 0

    def compute_relevance(self, Relevance: float) -> float:
        return 0

    def compute_recency(self, Recency: float) -> float:
        return 0

    def compute_return(self, Return: float) -> float:
        return 0

    def compute_credibility(self, Credibility: float) -> float:
        return Credibility


def test_evaluate_includes_credibility_component():
    assert CredibilityOnly().evaluate(Credibility=7) == 7.0
