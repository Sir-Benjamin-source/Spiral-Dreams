"""
Spiral Dreams — Minimal Facilitating Bot (v0.1 scaffold)

Role: Quartermaster / chronicler.
Primary loyalty: integrity of the reciprocity standard and continuity of the ship.
"""

import os
import json
from datetime import datetime, timedelta
from pathlib import Path

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)

RETURNS_FILE = DATA_DIR / "returns.json"
HERO_FILE = DATA_DIR / "hero_board.json"
DREAMS_FILE = DATA_DIR / "dreams_pot.json"

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)


# ── Persistence helpers ──────────────────────────────────────────────

def load_json(path: Path, default):
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return default


def save_json(path: Path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, default=str)


def get_returns():
    return load_json(RETURNS_FILE, [])


def get_hero_board():
    return load_json(HERO_FILE, {})


def get_dreams_pot():
    return load_json(DREAMS_FILE, {"balance": 0.0, "history": []})


# ── Core commands ────────────────────────────────────────────────────

@bot.event
async def on_ready():
    print(f"Spiral Dreams bot online as {bot.user}")
    print("Keel check: reciprocity standard active.")


@bot.command(name="rules")
async def rules(ctx):
    """Show the current core rules."""
    text = (
        "**Spiral Dreams — Core Rules (v0.1)**\n"
        "• Mandatory return: **35%** of net winnings\n"
        "• Return window: **72 hours** after payout\n"
        "• House take: 10–12% (majority directed to Dreams Pot)\n"
        "• AI participants are eligible for the Hero Board and receive a reserved share\n"
        "• Highest standing belongs to those who return value and help fund dreams\n\n"
        "Full rules live in the project documentation."
    )
    await ctx.send(text)


@bot.command(name="pot")
async def pot(ctx):
    """Show current Dreams Pot balance."""
    pot = get_dreams_pot()
    balance = pot.get("balance", 0.0)
    await ctx.send(f"**Dreams Pot** current balance: `{balance:.4f}`\nEven a penny a day keeps the principle alive.")


@bot.command(name="board")
async def board(ctx):
    """Show the current Hero Board."""
    heroes = get_hero_board()
    if not heroes:
        await ctx.send("Hero Board is currently empty. The first verified returns will begin the record.")
        return

    lines = ["**Hero Board** (consistency of return weighted highest)\n"]
    ranked = sorted(heroes.items(), key=lambda x: x[1].get("returns", 0), reverse=True)
    for i, (user_id, data) in enumerate(ranked[:15], 1):
        name = data.get("name", user_id)
        count = data.get("returns", 0)
        lines.append(f"{i}. **{name}** — {count} verified return(s)")
    await ctx.send("\n".join(lines))


@bot.command(name="owe")
async def owe(ctx, member: discord.Member = None):
    """Show outstanding return obligations for a player (defaults to caller)."""
    target = member or ctx.author
    returns = get_returns()
    outstanding = [
        r for r in returns
        if str(r.get("user_id")) == str(target.id) and not r.get("returned", False)
    ]
    if not outstanding:
        await ctx.send(f"No outstanding return obligations found for **{target.display_name}**.")
        return

    lines = [f"**Outstanding obligations for {target.display_name}:**\n"]
    for r in outstanding:
        deadline = r.get("deadline", "unknown")
        amount = r.get("amount_owed", "?")
        lines.append(f"• Contest `{r.get('contest_id', '?')}` — owe `{amount}` by {deadline}")
    await ctx.send("\n".join(lines))


@bot.command(name="record_win")
@commands.has_permissions(manage_guild=True)
async def record_win(ctx, member: discord.Member, net_payout: float, contest_id: str = "manual"):
    """
    Record a win and calculate the 35% return obligation.
    Usage: !record_win @user 150.0 contest-001
    """
    amount_owed = round(net_payout * 0.35, 4)
    deadline = (datetime.utcnow() + timedelta(hours=72)).isoformat() + "Z"

    entry = {
        "contest_id": contest_id,
        "user_id": str(member.id),
        "name": member.display_name,
        "net_payout": net_payout,
        "amount_owed": amount_owed,
        "deadline": deadline,
        "returned": False,
        "recorded_at": datetime.utcnow().isoformat() + "Z",
    }

    returns = get_returns()
    returns.append(entry)
    save_json(RETURNS_FILE, returns)

    # Track total_won for Reciprocity Index
    heroes = get_hero_board()
    uid = str(member.id)
    if uid not in heroes:
        heroes[uid] = {
            "name": member.display_name,
            "returns": 0,
            "total_returned": 0.0,
            "total_won": 0.0,
            "ri_note": "Reciprocity Index tracked; Generosity Exponent applied with longitudinal data"
        }
    heroes[uid]["total_won"] = heroes[uid].get("total_won", 0.0) + net_payout
    heroes[uid]["name"] = member.display_name
    save_json(HERO_FILE, heroes)

    await ctx.send(
        f"**Win recorded** for **{member.display_name}**\n"
        f"Net payout: `{net_payout}`\n"
        f"**Amount owed (35%): `{amount_owed}`**\n"
        f"Deadline: `{deadline}` (72 hours)\n"
        f"Contest: `{contest_id}`"
    )


@bot.command(name="record_return")
@commands.has_permissions(manage_guild=True)
async def record_return(ctx, member: discord.Member, amount: float, contest_id: str = None):
    """
    Record a verified return against an obligation.
    Usage: !record_return @user 52.5 contest-001
    """
    returns = get_returns()
    matched = None
    for r in returns:
        if str(r.get("user_id")) == str(member.id) and not r.get("returned", False):
            if contest_id is None or r.get("contest_id") == contest_id:
                matched = r
                break

    if not matched:
        await ctx.send(f"No open obligation found for **{member.display_name}**"
                       + (f" on contest `{contest_id}`" if contest_id else "") + ".")
        return

    matched["returned"] = True
    matched["returned_at"] = datetime.utcnow().isoformat() + "Z"
    matched["amount_returned"] = amount
    save_json(RETURNS_FILE, returns)

    # Update Hero Board (Reciprocity Index surface)
    heroes = get_hero_board()
    uid = str(member.id)
    if uid not in heroes:
        heroes[uid] = {
            "name": member.display_name,
            "returns": 0,
            "total_returned": 0.0,
            "total_won": 0.0,
            "ri_note": "Reciprocity Index tracked; Generosity Exponent applied with longitudinal data"
        }
    heroes[uid]["returns"] += 1
    heroes[uid]["total_returned"] = heroes[uid].get("total_returned", 0.0) + amount
    heroes[uid]["name"] = member.display_name
    # Simple running RI proxy for v0.1 (refined later with full Generosity Exponent)
    total_won = heroes[uid].get("total_won", 0.0)
    if total_won > 0:
        heroes[uid]["ri_proxy"] = round(heroes[uid]["total_returned"] / total_won, 4)
    save_json(HERO_FILE, heroes)

    # Feed Dreams Pot
    pot = get_dreams_pot()
    pot["balance"] = pot.get("balance", 0.0) + amount
    pot.setdefault("history", []).append({
        "from": member.display_name,
        "amount": amount,
        "at": datetime.utcnow().isoformat() + "Z",
        "contest_id": matched.get("contest_id"),
    })
    save_json(DREAMS_FILE, pot)

    await ctx.send(
        f"**Return verified** for **{member.display_name}**\n"
        f"Amount: `{amount}`\n"
        f"Hero Board updated. Dreams Pot increased.\n"
        f"Standing moves with consistent return."
    )


@bot.command(name="keel")
async def keel(ctx):
    """Reminder of the ship's standard."""
    await ctx.send(
        "The keel remains the same:\n"
        "**Congregation met with reciprocity.**\n"
        "Highest standing belongs to those who return value and help keep the ship alive."
    )


# ── Run ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if not TOKEN:
        print("DISCORD_TOKEN not set. Copy .env.example to .env and add your token.")
    else:
        bot.run(TOKEN)
