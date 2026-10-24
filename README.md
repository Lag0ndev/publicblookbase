# Blookbase

**Blookbase** is a free fan-made website for the educational game **Blooket**. It helps players and teachers track seasons, countdowns, packs, gamemodes, leaks, and update history in one place.

**Live site:** [https://blookbase.vercel.app](https://blookbase.vercel.app)

> **Not affiliated with, endorsed by, or connected to Blooket or its owners.** All Blooket names, art, and assets belong to their respective owners. This is an independent fan project by [Lag0n](https://www.youtube.com/@Lag0n4/).

## What is Blookbase?

Blooket is a classroom quiz game with collectible characters called **Blooks**, **packs**, seasonal events, and many **gamemodes**. Official info is spread across help pages, the market, and social posts. Blookbase organizes that information for fans:

| Feature | What it does |
|--------|----------------|
| **Home** | Hub for the site |
| **Countdown** | Timers for seasons and events (e.g. Spooktober, Season 9, holidays) |
| **What's New** | Recent product / season highlights |
| **Leaks** | Fan tracking of unreleased or rare Blooks, uniques, mysticals, and gamemode status |
| **Update Tracker** | Chronological feed of Blooket updates (seasons, packs, gamemodes, UI) |
| **Videos** | Blooket-related YouTube content |
| **Gamemodes** | Overview of host and solo modes with logos and details |
| **Packs / Market** | Pack contents, rarities, and odds reference |
| **Pack Calculator** | Tools related to pack opens |
| **Banners** | Banner-related reference |
| **About** | Credits and disclaimer |

## Who is it for?

- Students and players who collect Blooks and follow new seasons
- Teachers who use Blooket in class and want a clear season/event overview
- Fans who follow leaks, update history, and community videos

## Tech

- Static front end (HTML / CSS / JS), hosted on [Vercel](https://vercel.com)
- Optional Firebase for public chat (locked down with Firestore security rules)
- GitHub Actions probes Blooket CDN assets about every **5 minutes** (GitHub's minimum schedule interval) and updates `data/last-check.json`

## Pages (URLs)

- `/` — Home
- `/countdown` — Seasonal countdowns
- `/whatsnew` — What's New
- `/leaks` — Leaks & unreleased content
- `/tracker` — Update tracker
- `/videos` — Videos
- `/gamemodes` — Gamemodes
- `/packs` — Packs (market reference)
- `/about` — About

## Deploy

Import this repository on [Vercel](https://vercel.com). `vercel.json` rewrites app routes to `index.html`.

## Disclaimer

Blookbase is **fan-made and unofficial**. It is not a Blooket product. Game data and images may change when Blooket updates their servers; the tracker helps notice asset changes but is not guaranteed to be complete or official.

---

Made by **[Lag0n](https://www.youtube.com/@Lag0n4/)** · Repo: [Lag0ndev/blookbase](https://github.com/Lag0ndev/blookbase)
