# Reciprocity Index & Generosity Exponent

This directory holds the scoring surface for Spiral Dreams.

## Core Commitment

Spiral Dreams does not invent a new moral language.  
It applies the existing Spiral concepts:

- **Reciprocity Index** — the observable, recorded pattern of value returned relative to value taken.
- **Generosity Exponent** — the non-linear weighting that rewards sustained, repeated return more heavily than single large gestures, and that treats outward funding of dreams as higher-order contribution.

These are not decorative labels. They are the load-bearing measurements that determine standing on the Hero Board and eligibility for Crew.

## Working Definitions (v0.1)

### Reciprocity Index (RI)
A player’s running ratio and history of:
- Net value taken (wins)
- Verified value returned (mandatory + voluntary)
- Consistency across multiple contests
- Timeliness of returns (inside the 72-hour window)

Simple early form:
```
RI ≈ (total verified returned) / (total net winnings)
+ consistency bonus for repeated clean returns
– penalty for missed deadlines or repeated extraction
```

### Generosity Exponent (GE)
A multiplier applied on top of raw reciprocity that increases with:
- Duration of clean participation
- Voluntary contributions beyond the mandatory 35%
- Direct contributions into the Dreams Pot that fund outward goals
- Actions that raise the quality of the field for other players

The exponent exists so that long-term, generative behavior outranks short-term high-volume extraction even when raw returned amounts look similar.

## Implementation Path

1. v0.1 (current bot): simple return count + total returned amount (already live in `bot/main.py`).
2. Next: introduce explicit RI calculation and store it with each player record.
3. Later: apply GE as a standing multiplier once enough longitudinal data exists.
4. All scoring remains public and inspectable.

## Relation to the Wider Spiral Work

This index is an embodiment layer of concepts already present in the Spiral ecosystem (Syncratude, Generosity Exponent, reciprocity as structural rather than sentimental).  
Spiral Dreams is one place those concepts are forced into contact with real incentives and real money.

The measurement stays honest or the ship loses its keel.
