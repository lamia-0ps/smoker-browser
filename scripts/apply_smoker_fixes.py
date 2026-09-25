#!/usr/bin/env python3
"""Smoker 1.1.1 fixes: visible input fields, visible bot list, no preset bots."""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAIN = os.path.join(ROOT, "app/src/main/java/com/smoke/browser/MainActivity.java")
GRADLE = os.path.join(ROOT, "app/build.gradle")

s = open(MAIN, encoding="utf-8").read()
changed = []

# 1) Bot list ScrollView: 0dp+weight collapses to zero height in a wrap-content dialog
old = "scroll.setLayoutParams(new android.widget.LinearLayout.LayoutParams(-1, 0, 1.0f));"
new = "scroll.setLayoutParams(new android.widget.LinearLayout.LayoutParams(-1, (int)(getResources().getDisplayMetrics().heightPixels * 0.45)));"
if old in s:
    s = s.replace(old, new, 1)
    changed.append("bot list fixed height")

# 2) No preset bots: remove the seeding call, the seeder method, and its constant
if "        seedPresetBots();\n" in s:
    s = s.replace("        seedPresetBots();\n", "", 1)
    changed.append("removed seed call")
m = re.search(r'\n    private static final String SMOKER_BOTS_SEEDED = "smoker_bots_seeded_v1";\n', s)
if m:
    s = s[:m.start()] + "\n" + s[m.end():]
    changed.append("removed SEEDED constant")
m = re.search(r"\n    private void seedPresetBots\(\) \{.*?\n    \}\n", s, re.S)
if m:
    s = s[:m.start()] + "\n" + s[m.end():]
    changed.append("removed seeder method")

# 3) Create-bot fields: dark rounded background so the white text is actually visible
old_name = "        nameIn.setBackgroundResource(android.R.drawable.editbox_background_normal);"
new_name = ("        android.graphics.drawable.GradientDrawable nameBg = new android.graphics.drawable.GradientDrawable();\n"
            "        nameBg.setCornerRadius(14f);\n"
            "        nameBg.setColor(0xFF263238);\n"
            "        nameIn.setBackground(nameBg);\n"
            "        nameIn.setPadding(24, 18, 24, 18);")
if old_name in s:
    s = s.replace(old_name, new_name, 1)
    changed.append("name field visible")

old_code = "        codeIn.setBackgroundResource(android.R.drawable.editbox_background_normal);"
new_code = ("        android.graphics.drawable.GradientDrawable codeBg = new android.graphics.drawable.GradientDrawable();\n"
            "        codeBg.setCornerRadius(14f);\n"
            "        codeBg.setColor(0xFF263238);\n"
            "        codeIn.setBackground(codeBg);\n"
            "        codeIn.setPadding(24, 18, 24, 18);")
if old_code in s:
    s = s.replace(old_code, new_code, 1)
    changed.append("code field visible")

# 4) Empty-state hint when no bots exist yet
anchor = '        androidx.cardview.widget.CardView newBtn = createCardButton("＋ NEW BOT"'
empty_block = '''        if (bots.length() == 0) {
            android.widget.TextView empty = new android.widget.TextView(this);
            empty.setText("No saved bots yet.\\nTap ＋ NEW BOT to create your first one.");
            empty.setTextColor(0xFF78909C);
            empty.setTextSize(14);
            empty.setGravity(android.view.Gravity.CENTER);
            empty.setPadding(0, 60, 0, 60);
            botList.addView(empty);
        }

'''
if anchor in s and "No saved bots yet" not in s:
    s = s.replace(anchor, empty_block + anchor, 1)
    changed.append("empty-state hint")

open(MAIN, "w", encoding="utf-8", newline="").write(s)

# 5) version bump
g = open(GRADLE, encoding="utf-8").read()
if 'versionName "1.1.0"' in g:
    g = g.replace("versionCode 2", "versionCode 3", 1)
    g = g.replace('versionName "1.1.0"', 'versionName "1.1.1"', 1)
    open(GRADLE, "w", encoding="utf-8", newline="").write(g)
    changed.append("bumped to 1.1.1 (3)")

print("FIXES:", ", ".join(changed) or "already applied")
