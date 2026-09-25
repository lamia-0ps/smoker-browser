#!/usr/bin/env python3
"""Smoker 1.1.3: bot engine self-test + visible JS errors."""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAIN = os.path.join(ROOT, "app/src/main/java/com/smoke/browser/MainActivity.java")
GRADLE = os.path.join(ROOT, "app/build.gradle")

s = open(MAIN, encoding="utf-8").read()
changed = []

# 1) runSmokerBot: report the real result/error as a toast instead of hiding it
old = '''        webView.evaluateJavascript("(function(){ try{" + code + "}catch(e){console.log('SmokerBot: '+e.message);} })();", null);
        isBotRunning = true;
        showStatus("🔥 " + name + " is working!");'''
new = '''        webView.evaluateJavascript("(function(){ try{" + code + "; return 'OK';}catch(e){return 'ERROR: '+e.message;} })();", r -> showStatus("🔥 " + name + ": " + r));
        isBotRunning = true;'''
if old in s:
    s = s.replace(old, new, 1)
    changed.append("saved-bot errors visible")

# 2) quick run: same — surface result/error via toast
old = '''webview.evaluateJavascript("(function(){ try{"+code+"}catch(e){alert(e.message);} })();", null);'''
new = '''webview.evaluateJavascript("(function(){ try{"+code+"; return 'OK';}catch(e){return 'ERROR: '+e.message;} })();", r -> showStatus("⚡ Quick Run: " + r));'''
if old in s:
    s = s.replace(old, new, 1)
    changed.append("quick-run errors visible")

# 3) TEST BOT ENGINE button in the Smoker Bots dialog
anchor = '''        newBtn.setOnClickListener(v -> { dialog.dismiss(); showBotCreateDialog(webView); });
        quickBtn.setOnClickListener(v -> { dialog.dismiss(); showBotEditor(webView); });'''
inject = anchor + '''

        androidx.cardview.widget.CardView testBtn = createCardButton("🧪 TEST BOT ENGINE", 0xFF263238, 0xFF80DEEA, false, false);
        root.addView(testBtn);
        testBtn.setOnClickListener(v -> {
            dialog.dismiss();
            webView.evaluateJavascript("(function(){try{document.documentElement.style.boxShadow='inset 0 0 0 12px #76FF03';document.title='SMOKER OK';return 'ENGINE OK — lime border = bots work';}catch(e){return 'ERROR: '+e.message;}})()", r -> showStatus("🧪 " + r));
        });'''
if anchor in s and "TEST BOT ENGINE" not in s:
    s = s.replace(anchor, inject, 1)
    changed.append("engine test button")

# 4) version label
old = 'sub.setText("Your saved bots — tap one to run • Smoker v1.1.2");'
new = 'sub.setText("Your saved bots — tap one to run • Smoker v1.1.3");'
if old in s:
    s = s.replace(old, new, 1)
    changed.append("version label")

open(MAIN, "w", encoding="utf-8", newline="").write(s)

# 5) version bump
g = open(GRADLE, encoding="utf-8").read()
if 'versionName "1.1.2"' in g:
    g = g.replace("versionCode 4", "versionCode 5", 1)
    g = g.replace('versionName "1.1.2"', 'versionName "1.1.3"', 1)
    open(GRADLE, "w", encoding="utf-8", newline="").write(g)
    changed.append("bumped to 1.1.3 (5)")

print("FIXES3:", ", ".join(changed) or "already applied")
