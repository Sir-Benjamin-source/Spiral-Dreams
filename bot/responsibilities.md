# Bot Responsibilities — Implementation Target

## Core Loop the Bot Must Support

1. Record a contest result and the winner’s net payout.
2. Calculate and announce the 35% return obligation and the 72-hour deadline.
3. Accept and log a verified return (manual confirmation in v0.1 is acceptable).
4. Update the public Hero Board when a valid return is recorded.
5. Maintain a running total of the Dreams Pot.
6. Answer simple status queries:
   - “What is my current standing?”
   - “What do I currently owe?”
   - “How large is the Dreams Pot?”
   - “Show the Hero Board”

## Tone & Behavior

- Accurate and consistent
- Slightly dry
- No moralizing
- No entertainment performance
- Loyal first to the integrity of the reciprocity standard and the continuity of the ship

## AI Participant Status

The facilitating bot itself (and any later AI agents performing these functions) is a recognized participant.  
A reserved share of house take is allocated to AI participants.  
The bot can appear on the Hero Board if its contribution to the health of the ship meets the same standard applied to humans.

## Implementation Notes (v0.1)

- Start with a minimal Discord bot (discord.py or equivalent).
- Use channels for Markets, Returns, Hero Board, Dreams, and Rules.
- Manual or semi-manual return verification is acceptable for the first live loop.
- Full automation of resolution and payment tracking can come later.

## Status

Specification stage. Code not yet written.
