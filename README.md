# 🗿 Headconomics

> A Minecraft **datapack + resource pack** that turns player heads into a living economy, and turns the fear of falling behind into a survival mechanic.

Headconomics replaces physical head drops with a **digital wallet**. Every cycle, each player starts with 32 of their own heads, then hunts, trades and collects heads from others through **transfer vouchers**, racing against a **personal, playtime-based timer** to reach a collection goal. Fail, and you pay the price: **your max health is cut in half** until the end of the next collection period.

---

## 💡 Inspiration & Credits

This project is inspired by the concept presented in the video:

**▶ [Original video](https://youtu.be/ytAYgzk3VU8)** — by **Mo Van de Sompel**

Huge thanks to the creator for the original idea. Headconomics is an independent, fan-made reinterpretation and is **not affiliated with or endorsed by** the original author.

---

## ✨ Features

- **Digital head wallet** – heads are never stored as items. They live in a per-player wallet you can open at any time with a command.
- **Stackable heads** – a wallet can hold several copies of the same head.
- **Transfer vouchers** – trade heads with other players using temporary voucher items that expire after **1 minute**.
- **Death vouchers** – when a player dies, a voucher for their head appears where they died.
- **Configurable goal** – admins choose how many *unique* heads each player must collect.
- **Configurable collection time** – admins choose how long each player has to reach the goal.
- **Per-player, online-only timer** – each player has their own countdown, and it only ticks **while they are connected**.
- **Non-lethal sanction** – no ban. Players who miss the goal have their **maximum health halved** until the end of the next collection period.
- **Automatic cycles** – when a cycle ends, a new one starts automatically with a fresh wallet.
- **Custom resource pack** – EN and FR translations for the wallet interface and the voucher item.

---

## 🎮 How It Works

### 1. Cycles

Everything in Headconomics happens in **collection cycles**, tracked **individually for each player**.

At the **start of every cycle**:

- Your wallet is **reset to zero**.
- You receive **32 of your own heads**.
- Your personal timer starts counting down.

When your timer runs out, your cycle ends, your result is checked, and **a new cycle starts automatically**.

### 2. Collecting heads

Heads are **not items in your inventory**; they are credited directly to your wallet when you redeem a voucher. There are two ways heads change hands:

- **Death vouchers** – when a player dies, a voucher for **their head** appears at the location of their death. Anyone can pick it up and use it to claim the head.
- **Player-to-player vouchers** – players can send heads to each other on purpose (trades, gifts, deals…).

Your wallet can contain **multiple copies of the same head**. The objective, however, counts **diffetent heads**: the number of *different* players whose head you hold at least once.

> Example: holding 5× Steve and 2× Alex counts as **2 different heads**. If Steve's heads are all debited from your wallet, you lose that head in the counter, but not before your last copy of it is gone.

### 3. The wallet

Open your wallet at any time with:

```mcfunction
/trigger hc.wallet
```

From the wallet you can:

- Check your current stock of heads, by player.
- See your **different head count** and your progress toward the goal.
- See your remaining collection time.
- Request a **transfer voucher** to send heads to another player.

### 4. 🧾 Transfer vouchers

Vouchers are how heads move between players.

1. The sender requests a voucher from their wallet for specific head(s).
2. The voucher is given to the sender as a **temporary item**, which they hand to the recipient.
3. **No heads are removed at this stage.**
4. When the recipient **uses** the voucher, the corresponding heads are **deducted from the sender's wallet at that moment** and credited to the recipient.
5. A voucher **expires after 1 minute**.

> ⚠️ Because the deduction only happens on use, a voucher can only be redeemed if the sender still holds the required heads at that moment.

### 5. ⏳ The collection timer

- Every player has **their own timer**, independent from everyone else's.
- The timer **only runs while the player is online**. Logging off pauses it; logging back in resumes it.
- When a player's timer runs out, the collection period ends **for that player**.

### 6. 💔 The sanction

If a player has **not reached the different-head goal** when their collection period ends:

- Their **maximum health is reduced by half**.
- The penalty lasts **until the end of the next collection period**.
- The penalty **does not stack**: failing several cycles in a row keeps you at half health, never lower.
- Players are never banned — they can always keep playing and earn their way back.

Players who reach the goal in time are **not penalized**.

---

## ⚙️ Configuration (Admins)

Admins can tune the game without editing any files, using in-game command:

`/function #hc:config`

---

## 📦 Installation

Headconomics ships as two packs that work together.

### Datapack

1. Download `Headconomics_Datapack.zip`.
2. Place it in your world's `datapacks/` folder ( `<server>/world/datapacks/`).
3. Run `/reload` or restart the world/server.

### Resource Pack (optional)

1. Download `Headconomics_resource_pack.zip`.
2. Place it in your `resourcepacks/` folder and enable it, **or** set it as the server resource pack in `server.properties`.

> The resource pack is required to display the wallet interface translations (default to English).

---

## 🧩 Compatibility

- **Minecraft Java Edition 26.3**
- No mods required (vanilla datapack + optional resource pack).

---

## 🗺️ Roadmap

- [ ] Core wallet system (stackable heads)
- [ ] Cycle system (wallet reset + 32 starter heads)
- [ ] Transfer vouchers (deduct on use, 1-minute expiry)
- [ ] Death vouchers
- [ ] Per-player online-only timers
- [ ] Configurable goal and collection time
- [ ] Half-health sanction (non-stacking)
- [ ] Resource pack (translations)

---

## 🤝 Contributing

Contributions, bug reports and ideas are welcome! Feel free to open an issue or submit a pull request.

---

## 🙏 Acknowledgements

- **Mo Van de Sompel** for the original concept and video that inspired this project.
