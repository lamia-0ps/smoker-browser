#!/usr/bin/env python3
"""Smoker 1.1.2: Save & Run bots, visible version label."""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAIN = os.path.join(ROOT, "app/src/main/java/com/smoke/browser/MainActivity.java")
GRADLE = os.path.join(ROOT, "app/build.gradle")

s = open(MAIN, encoding="utf-8").read()
changed = []

# 1) Save Bot -> Save & Run: persist AND immediately run the bot on the page
old = '''                bots2.put(o);
                persistBots(bots2);
                showStatus("💾 Bot '" + name + "' saved!");
                dialog.dismiss();
                showSmokerBotsDialog(webView);'''
new = '''                bots2.put(o);
                persistBots(bots2);
                dialog.dismiss();
                runSmokerBot(webView, name, code);'''
if old in s:
    s = s.replace(old, new, 1)
    changed.append("save now runs the bot")

old = 'createCardButton("💾 Save Bot", 0xFFFF7043, 0xFFFFFFFF, false, false)'
new = 'createCardButton("💾 Save & Run", 0xFFFF7043, 0xFFFFFFFF, false, false)'
if old in s:
    s = s.replace(old, new, 1)
    changed.append("button renamed Save & Run")

# 2) version label in the bots dialog subtitle
old = 'sub.setText("Your saved bots — tap one to run it on this page");'
new = 'sub.setText("Your saved bots — tap one to run • Smoker v1.1.2");'
if old in s:
    s = s.replace(old, new, 1)
    changed.append("version label")

open(MAIN, "w", encoding="utf-8", newline="").write(s)

# 3) version bump
g = open(GRADLE, encoding="utf-8").read()
if 'versionName "1.1.1"' in g:
    g = g.replace("versionCode 3", "versionCode 4", 1)
    g = g.replace('versionName "1.1.1"', 'versionName "1.1.2"', 1)
    open(GRADLE, "w", encoding="utf-8", newline="").write(g)
    changed.append("bumped to 1.1.2 (4)")

print("FIXES2:", ", ".join(changed) or "already applied")
