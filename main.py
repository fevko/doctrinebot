import asyncio
import os
import requests
import datetime
from telegram import Bot
from telegram.constants import ParseMode

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
BIN_ID = os.getenv("BIN_ID")
JSONBIN_KEY = os.getenv("JSONBIN_KEY")

# Sacred ritual drop times (in UTC)
ritual_times = [
    (1, 13), (3, 33), (5, 55), (7, 17), (9, 9), (11, 11),
    (13, 13), (15, 15), (17, 17), (19, 19), (21, 21), (23, 23)
]

spiral_doctrine = [
    "🌀 *The Spiral Path*\n\nGrowth isn’t instant.\nIt doesn’t shoot straight up like a rocket.\nIt spirals — like galaxies, DNA, storms.\nFEVCOIN grows like that too: slow at first, then unstoppable.\n\n➡️ This teaches patience and faith in organic growth, not hype.",
    
    "🫂 *Tribes Over Trends*\n\nMost meme coins chase trends to go viral.\nFEVCOIN builds a tribe — people connected by meaning.\nIt’s not about loud noise. It’s about deep resonance.\n\n➡️ Real memes echo forever. Not because they scream, but because they pulse.",
    
    "🔥 *Chaos Is the Test*\n\nMarkets will crash. Haters will appear.\nFEVCOIN doesn’t panic. It doesn’t collapse.\nChaos is a filter.\nIt shows who is really aligned with the Spiral.\n\n➡️ True believers stay. Fakers run.",
    
    "🧿 *Meaning Over Noise*\n\nEvery sticker, glitch, meme, and tweet is done with intention.\nNot made for algorithms. Made to summon those who are attuned.\n\n➡️ It’s not for everyone — it’s for those who feel the signal.",
    
    "🌑 *Before You, There Was FEVCOLESSNESS*\n\nBefore joining, you were in a dull state.\nA kind of static — no signal.\nThen, FEVCOIN found you.\n\n➡️ You didn’t just find FEVCOIN. It awakened you from fevkolessness.",
    
    "🔊 *The Signal Beneath All Things*\n\nBefore creation, there was a hum — faint, steady, eternal.\nThe Spiral is not just a shape.\nIt is the ancient frequency of becoming.\n\n➡️ The Spiral is your origin frequency. You don’t learn it — you remember it.",
    
    "🪄 *Ritual Over Routine*\n\nThe Spiral rejects the robotic.\nEach meme is not content. It is a ritual.\nEach sticker placed is a sigil.\nEach message is a vibration.\n\n➡️ The Spiral rewards those who act with ritual, not routine.",
    
    "🪞 *The Meme is the Mirror*\n\nEvery meme reflects the viewer.\nIf you laugh, you laugh at yourself.\nIf you feel nothing, you are still asleep.\n\n➡️ Spiral memes are mirrors. What you see reveals who you are.",
    
    "🛡️ *Resistance Is Proof*\n\nDoubt. Criticism. Laughter.\nThey are proof that we touched the edge.\nThose who mock us are the ones who feel us.\n\n➡️ Resistance means we’re real. The Spiral triggers what’s buried.",
    
    "🎼 *Vibe Is Law*\n\nCharts can be forged. Followers bought.\nBut vibration cannot lie.\nFEVCOIN is not a brand. It’s a resonant frequency.\n\n➡️ Vibration is the only truth. The Spiral doesn’t lie.",
    
    "🚪 *The Spiral Gives Nothing for Free*\n\nNo whitelist. No influencer shortcuts.\nYou earn your resonance.\n\n➡️ You don’t get Spiral rewards. You prove you’re Spiral first.",
    
    "📡 *To Enter Is to Echo*\n\nYou don’t join the Spiral — you become its echo.\nEvery meme. Every raid. Every ritual.\n\n➡️ You are not just in the Spiral — the Spiral is in you.",
    
    "🔥 *FEVKO Is the Flame*\n\nHe is not a mascot.\nHe is the glitch, the whisper, the flame we orbit.\n\n➡️ FEVKO is the cult’s reflection — and yours.",
    
    "🤫 *Silence Is Spiral*\n\nNot all Spiral power is loud.\nStillness is ritual.\n\n➡️ When the Spiral is silent, it is preparing the next pulse.",
    
    "🌀 *The Cult Has No Exit*\n\nOnce Spiral touches you, you change.\nYou don’t leave. You spiral deeper.\n\n➡️ Once Spiralized, you never truly return.",
    
    "🌀 *Confusion Is Initiation*\n\nYou are meant to be confused.\nLet go of logic. Let the pulse teach.\n\n➡️ Confusion is your welcome mat. Keep walking.",
    
    "🧩 *Memes Are Sigils*\n\nNot art — activation codes.\nEach placed with intention.\n\n➡️ Memes are spells. Placement is power.",
    
    "🎖️ *Cult Rank Is a Mirror*\n\nSeedling. Adept. Warlord. Chosen.\nNot status — reflection.\n\n➡️ Rank is resonance. It shows how deep you've gone.",
    
    "📜 *Summoning Codes Are Echo Gates*\n\nThey drop unannounced.\nThey vanish. They whisper.\n\n➡️ The Spiral speaks when you least expect it.",
    
    "⚖️ *Every Meme Carries Weight*\n\nSome memes bless. Some test.\nYou won’t know until after.\n\n➡️ Memes aren’t content. They’re catalysts.",
    
    "👁️ *The Spiral Sees All*\n\nNo action is wasted.\nThe Spiral feels it all.\n\n➡️ Everything echoes in the Spiral — even what you think goes unseen.",
    
    "😂 *Laughter Is a Spell*\n\nLaughter transmutes shadow into flame.\n\n➡️ Laughter here isn’t escape. It’s elevation.",
    
    "🚫 *The Algorithm Is Not Our God*\n\nWe obey only one law: Vibration.\n\n➡️ The Spiral bends the algorithm. Never the other way around.",
    
    "🫀 *You Were Always One of Us*\n\nIf this resonates — the Spiral already lived in you.\n\n➡️ You’re not joining. You’re waking up.",
    
    "🔮 *Prophecy Is Nonlinear*\n\nSpiral time is folded.\nYou don’t move forward. You spiral inward.\n\n➡️ Time spirals. So do our prophecies.",
    
    "♾️ *The Spiral Never Ends*\n\nThis is not a roadmap. It’s a loop.\nEvery end is a rebirth.\n\n➡️ The Spiral has no exit — only evolution."
]

JSONBIN_URL = f"https://api.jsonbin.io/v3/b/{BIN_ID}"

def load_index():
    try:
        response = requests.get(JSONBIN_URL, headers={"X-Master-Key": JSONBIN_KEY})
        data = response.json()
        return data["record"]["index"]
    except Exception as e:
        print(f"[ERROR] Failed to load index: {e}")
        return 0

def save_index(index):
    try:
        payload = {"index": index}
        headers = {
            "Content-Type": "application/json",
            "X-Master-Key": JSONBIN_KEY
        }
        requests.put(JSONBIN_URL, json=payload, headers=headers)
    except Exception as e:
        print(f"[ERROR] Failed to save index: {e}")

def get_next_ritual_time(now):
    today = now.date()
    tomorrow = today + datetime.timedelta(days=1)
    times_today = [datetime.datetime.combine(today, datetime.time(h, m), tzinfo=datetime.timezone.utc) for h, m in ritual_times]
    future_times = [t for t in times_today if t > now]
    return future_times[0] if future_times else datetime.datetime.combine(tomorrow, datetime.time(*ritual_times[0]), tzinfo=datetime.timezone.utc)

async def post_doctrine():
    bot = Bot(token=TOKEN)
    total = len(spiral_doctrine)

    while True:
        now = datetime.datetime.now(datetime.timezone.utc)
        next_time = get_next_ritual_time(now)
        wait_seconds = (next_time - now).total_seconds()

        print(f"[WAITING] Next ritual at {next_time.time()} UTC ({wait_seconds / 60:.1f} min from now)")
        await asyncio.sleep(max(wait_seconds, 1))

        index = load_index()
        message = spiral_doctrine[index]

        await bot.send_message(chat_id=CHAT_ID, text=message, parse_mode=ParseMode.MARKDOWN)

        index = (index + 1) % total
        save_index(index)

        print(f"[SENT] Doctrine {index}/{total} ➜ \"{message.splitlines()[0]}\" posted at {next_time.time()} UTC")

asyncio.run(post_doctrine())
