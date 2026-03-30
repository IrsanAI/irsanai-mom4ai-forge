from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List


@dataclass
class ResonanceScore:
    score: float
    connection: float
    coordination: float
    interaction_count: int
    classification: str


def _clamp01(value: float) -> float:
    return max(0.0, min(1.0, value))


def score_interactions(interactions: Iterable[Dict]) -> ResonanceScore:
    """
    Berechnet Resonanz aus echten Interaktionen.

    Erwartete Felder pro Event (0.0 bis 1.0):
      - intent_match
      - context_match
      - tone_match
      - reliability
      - coordination
    """
    rows: List[Dict] = list(interactions)
    if not rows:
        return ResonanceScore(
            score=0.0,
            connection=0.0,
            coordination=0.0,
            interaction_count=0,
            classification="no_data",
        )

    def avg(key: str, default: float = 0.0) -> float:
        return _clamp01(sum(float(r.get(key, default)) for r in rows) / len(rows))

    connection = _clamp01(
        0.35 * avg("intent_match")
        + 0.35 * avg("context_match")
        + 0.30 * avg("tone_match")
    )
    coordination = _clamp01(
        0.55 * avg("coordination")
        + 0.45 * avg("reliability")
    )
    score = _clamp01(0.5 * connection + 0.5 * coordination)
    classification = classify_resonance(score, len(rows))
    return ResonanceScore(
        score=score,
        connection=connection,
        coordination=coordination,
        interaction_count=len(rows),
        classification=classification,
    )


def classify_resonance(score: float, interaction_count: int) -> str:
    if interaction_count < 3:
        return "insufficient_data"
    if score >= 0.75:
        return "resonant"
    if score >= 0.55:
        return "emerging"
    if score >= 0.35:
        return "neutral"
    return "non_resonant"

