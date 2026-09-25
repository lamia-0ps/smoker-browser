# 🔥 Smoker Browser

A fast, open-source **Android automation browser** with a persistent bot engine — run tasks, scrape data, and manage custom bots straight from your phone.

## ✨ Key features

* 🤖 **Immortal Bot engine** — run automation on multiple websites simultaneously with no performance drop
* ⚡ **Native JS bridge** — deep, direct control of the browser session from your scripts
* 🔓 **Open source** — transparent, ad-free and secure, licensed under GPL-3.0

## 🛠️ Bot bridge API

* `Code.Bot()` — read the raw page source directly inside your automation script
* `Cleaner.Bot()` — clear cookies and session data programmatically for fresh instances
* `Bot.search()` — native search execution bridge built for high-speed bot queries
* `AppBot()` — trigger Android system-level actions: clicks, swipes, scrolls

## 📦 Building

Open the project in **Android Studio** (JDK 17) with Android SDK 34, or build from the CLI with Gradle 8.x:

```bash
gradle assembleRelease
```

## 📜 License & legal

This project is licensed under the **GPL-3.0 License** — see the [LICENSE](LICENSE) file.
It is a modified version of an upstream GPL-3.0 licensed work (rebranding, new package id, refreshed UI).

*Disclaimer: Smoker Browser is intended for legitimate web automation, testing, and scraping. Please respect the Terms of Service of the websites you automate.*
