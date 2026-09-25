#!/usr/bin/env python3
"""Smoker feature pack: renames bot menu, adds Smoker Bots manager, smokey tools icon."""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAIN = os.path.join(ROOT, "app/src/main/java/com/smoke/browser/MainActivity.java")
LAYOUT = os.path.join(ROOT, "app/src/main/res/layout/main.xml")
GRADLE = os.path.join(ROOT, "app/build.gradle")

FEATURE_METHODS = r'''
    // 🔥 Smoker Bots: named, savable automation bots
    private static final String SMOKER_BOTS_KEY = "smoker_bots_json";
    private static final String SMOKER_BOTS_SEEDED = "smoker_bots_seeded_v1";

    private org.json.JSONArray getSavedBots() {
        String raw = getSharedPreferences("BotPrefs", 0).getString(SMOKER_BOTS_KEY, "[]");
        try { return new org.json.JSONArray(raw); } catch (Exception e) { return new org.json.JSONArray(); }
    }

    private void persistBots(org.json.JSONArray bots) {
        getSharedPreferences("BotPrefs", 0).edit().putString(SMOKER_BOTS_KEY, bots.toString()).apply();
    }

    private void seedPresetBots() {
        android.content.SharedPreferences p = getSharedPreferences("BotPrefs", 0);
        if (p.getBoolean(SMOKER_BOTS_SEEDED, false)) return;
        org.json.JSONArray bots = getSavedBots();
        String[][] presets = {
            {"🌙 Dark Mode", "document.querySelectorAll('img,video').forEach(function(m){m.style.filter='invert(1) hue-rotate(180deg)';});document.documentElement.style.filter='invert(1) hue-rotate(180deg)';document.body.style.background='#111';"},
            {"🚫 Ad Nuker", "var s=['iframe','ins','.ad','.ads','.advert','[id*=ad-]','[class*=sponsor]'];s.forEach(function(q){document.querySelectorAll(q).forEach(function(e){e.remove();});});"},
            {"📜 Auto Scroll", "if(window.__smokerScroll){clearInterval(window.__smokerScroll);window.__smokerScroll=null;}else{window.__smokerScroll=setInterval(function(){window.scrollBy(0,2);},30);}"},
            {"📖 Reader Mode", "var b=document.body;b.style.background='#faf7f2';b.style.color='#222';b.style.fontFamily='Georgia,serif';b.style.fontSize='19px';b.style.lineHeight='1.7';b.style.maxWidth='680px';b.style.margin='24px auto';b.style.padding='0 16px';document.querySelectorAll('nav,header,footer,aside,iframe,form,button').forEach(function(e){e.remove();});"},
            {"🛡 Popup Blocker", "window.open=function(){return null;};window.alert=function(){};window.confirm=function(){return true;};window.prompt=function(){return null;};document.querySelectorAll('[class*=popup],[class*=modal],[id*=popup],[id*=modal],[class*=overlay]').forEach(function(e){e.style.display='none';});"}
        };
        try {
            for (String[] pr : presets) {
                org.json.JSONObject o = new org.json.JSONObject();
                o.put("name", pr[0]);
                o.put("code", pr[1]);
                bots.put(o);
            }
        } catch (Exception ignored) {}
        persistBots(bots);
        p.edit().putBoolean(SMOKER_BOTS_SEEDED, true).apply();
    }

    private void runSmokerBot(final android.webkit.WebView webView, String name, String code) {
        getSharedPreferences("BotPrefs", 0).edit().putString(BOT_CODE_KEY, code).apply();
        webView.evaluateJavascript("(function(){ try{" + code + "}catch(e){console.log('SmokerBot: '+e.message);} })();", null);
        isBotRunning = true;
        showStatus("🔥 " + name + " is working!");
    }

    private void showSmokerBotsDialog(final android.webkit.WebView webView) {
        seedPresetBots();
        final android.app.Dialog dialog = new android.app.Dialog(this);
        android.widget.LinearLayout root = new android.widget.LinearLayout(this);
        root.setOrientation(android.widget.LinearLayout.VERTICAL);
        root.setPadding(40, 40, 40, 40);
        android.graphics.drawable.GradientDrawable bg = new android.graphics.drawable.GradientDrawable();
        bg.setCornerRadius(35f);
        bg.setColor(0xFF1A1F24);
        root.setBackground(bg);

        android.widget.TextView header = new android.widget.TextView(this);
        header.setText("🔥 Work with Smoker");
        header.setTextSize(22);
        header.setTextColor(0xFFFF7043);
        header.setTypeface(null, android.graphics.Typeface.BOLD);
        header.setPadding(0, 0, 0, 10);
        root.addView(header);

        android.widget.TextView sub = new android.widget.TextView(this);
        sub.setText("Your saved bots — tap one to run it on this page");
        sub.setTextSize(13);
        sub.setTextColor(0xFFB0BEC5);
        sub.setPadding(0, 0, 0, 25);
        root.addView(sub);

        final android.widget.LinearLayout botList = new android.widget.LinearLayout(this);
        botList.setOrientation(android.widget.LinearLayout.VERTICAL);
        android.widget.ScrollView scroll = new android.widget.ScrollView(this);
        scroll.setLayoutParams(new android.widget.LinearLayout.LayoutParams(-1, 0, 1.0f));
        scroll.addView(botList);
        root.addView(scroll);

        final org.json.JSONArray bots = getSavedBots();
        for (int i = 0; i < bots.length(); i++) {
            final int idx = i;
            org.json.JSONObject bot = bots.optJSONObject(i);
            if (bot == null) continue;
            final String name = bot.optString("name", "Bot");
            final String code = bot.optString("code", "");
            android.widget.LinearLayout row = new android.widget.LinearLayout(this);
            row.setOrientation(android.widget.LinearLayout.HORIZONTAL);
            row.setGravity(android.view.Gravity.CENTER_VERTICAL);
            row.setPadding(20, 18, 20, 18);
            android.graphics.drawable.GradientDrawable rowBg = new android.graphics.drawable.GradientDrawable();
            rowBg.setCornerRadius(18f);
            rowBg.setColor(0xFF263238);
            row.setBackground(rowBg);
            android.widget.LinearLayout.LayoutParams rowLp = new android.widget.LinearLayout.LayoutParams(-1, -2);
            rowLp.setMargins(0, 0, 0, 14);
            row.setLayoutParams(rowLp);

            android.widget.TextView label = new android.widget.TextView(this);
            label.setText(name);
            label.setTextColor(0xFFFFFFFF);
            label.setTextSize(15);
            label.setLayoutParams(new android.widget.LinearLayout.LayoutParams(0, -2, 1.0f));
            row.addView(label);

            android.widget.TextView run = new android.widget.TextView(this);
            run.setText("▶ Run");
            run.setTextColor(0xFFFF7043);
            run.setTextSize(14);
            run.setTypeface(null, android.graphics.Typeface.BOLD);
            run.setPadding(24, 6, 12, 6);
            row.addView(run);

            android.widget.TextView del = new android.widget.TextView(this);
            del.setText("🗑");
            del.setTextSize(15);
            del.setPadding(18, 6, 6, 6);
            row.addView(del);

            run.setOnClickListener(v -> { runSmokerBot(webView, name, code); dialog.dismiss(); });
            label.setOnClickListener(v -> { runSmokerBot(webView, name, code); dialog.dismiss(); });
            del.setOnClickListener(v -> {
                org.json.JSONArray cur = getSavedBots();
                org.json.JSONArray next = new org.json.JSONArray();
                for (int j = 0; j < cur.length(); j++) {
                    if (j != idx) { try { next.put(cur.get(j)); } catch (Exception ignored) {} }
                }
                persistBots(next);
                dialog.dismiss();
                showSmokerBotsDialog(webView);
            });
            botList.addView(row);
        }

        androidx.cardview.widget.CardView newBtn = createCardButton("＋ NEW BOT", 0xFFFF7043, 0xFFFFFFFF, false, false);
        androidx.cardview.widget.CardView quickBtn = createCardButton("⚡ QUICK RUN (one-off code)", 0xFF263238, 0xFFFFB74D, false, false);
        root.addView(newBtn);
        root.addView(quickBtn);
        newBtn.setOnClickListener(v -> { dialog.dismiss(); showBotCreateDialog(webView); });
        quickBtn.setOnClickListener(v -> { dialog.dismiss(); showBotEditor(webView); });

        dialog.setContentView(root);
        if (dialog.getWindow() != null) {
            dialog.getWindow().setBackgroundDrawable(new android.graphics.drawable.ColorDrawable(android.graphics.Color.TRANSPARENT));
            int width = (int)(getResources().getDisplayMetrics().widthPixels * 0.90);
            dialog.getWindow().setLayout(width, android.view.ViewGroup.LayoutParams.WRAP_CONTENT);
        }
        dialog.show();
    }

    private void showBotCreateDialog(final android.webkit.WebView webView) {
        final android.app.Dialog dialog = new android.app.Dialog(this);
        android.widget.LinearLayout root = new android.widget.LinearLayout(this);
        root.setOrientation(android.widget.LinearLayout.VERTICAL);
        root.setPadding(40, 40, 40, 40);
        android.graphics.drawable.GradientDrawable bg = new android.graphics.drawable.GradientDrawable();
        bg.setCornerRadius(35f);
        bg.setColor(0xFF1A1F24);
        root.setBackground(bg);

        android.widget.TextView header = new android.widget.TextView(this);
        header.setText("🔥 Create Smoker Bot");
        header.setTextSize(20);
        header.setTextColor(0xFFFF7043);
        header.setTypeface(null, android.graphics.Typeface.BOLD);
        header.setPadding(0, 0, 0, 25);
        root.addView(header);

        final android.widget.EditText nameIn = new android.widget.EditText(this);
        nameIn.setHint("Bot name (e.g. Night Reader)");
        nameIn.setTextColor(0xFFFFFFFF);
        nameIn.setHintTextColor(0xFF78909C);
        nameIn.setSingleLine(true);
        nameIn.setBackgroundResource(android.R.drawable.editbox_background_normal);
        root.addView(nameIn);

        final android.widget.EditText codeIn = new android.widget.EditText(this);
        codeIn.setHint("JavaScript code...");
        codeIn.setTextColor(0xFFFFFFFF);
        codeIn.setHintTextColor(0xFF78909C);
        codeIn.setGravity(android.view.Gravity.TOP);
        codeIn.setMinLines(5);
        codeIn.setTypeface(android.graphics.Typeface.MONOSPACE);
        codeIn.setBackgroundResource(android.R.drawable.editbox_background_normal);
        android.widget.LinearLayout.LayoutParams codeLp = new android.widget.LinearLayout.LayoutParams(-1, 0, 1.0f);
        codeLp.setMargins(0, 20, 0, 0);
        codeIn.setLayoutParams(codeLp);
        root.addView(codeIn);

        android.widget.LinearLayout btnRow = new android.widget.LinearLayout(this);
        btnRow.setOrientation(android.widget.LinearLayout.HORIZONTAL);
        btnRow.setGravity(android.view.Gravity.RIGHT);
        btnRow.setPadding(0, 25, 0, 0);
        androidx.cardview.widget.CardView cancel = createCardButton("Cancel", 0xFF263238, 0xFFB0BEC5, false, false);
        androidx.cardview.widget.CardView save = createCardButton("💾 Save Bot", 0xFFFF7043, 0xFFFFFFFF, false, false);
        btnRow.addView(cancel);
        btnRow.addView(save);
        root.addView(btnRow);

        cancel.setOnClickListener(v -> dialog.dismiss());
        save.setOnClickListener(v -> {
            String name = nameIn.getText().toString().trim();
            String code = codeIn.getText().toString().trim();
            if (name.isEmpty() || code.isEmpty()) { showStatus("Name and code required"); return; }
            org.json.JSONArray bots2 = getSavedBots();
            try {
                org.json.JSONObject o = new org.json.JSONObject();
                o.put("name", name);
                o.put("code", code);
                bots2.put(o);
                persistBots(bots2);
                showStatus("💾 Bot '" + name + "' saved!");
                dialog.dismiss();
                showSmokerBotsDialog(webView);
            } catch (Exception e) { showStatus("Save failed"); }
        });

        dialog.setContentView(root);
        if (dialog.getWindow() != null) {
            dialog.getWindow().setBackgroundDrawable(new android.graphics.drawable.ColorDrawable(android.graphics.Color.TRANSPARENT));
            int width = (int)(getResources().getDisplayMetrics().widthPixels * 0.90);
            dialog.getWindow().setLayout(width, android.view.ViewGroup.LayoutParams.WRAP_CONTENT);
        }
        dialog.show();
    }
'''

def patch_main_activity():
    s = open(MAIN, encoding="utf-8").read()
    changed = []

    if "WORK WITH SMOKER" not in s:
        old = 'createCardButton("WORK WITH BOT", 0xFFFFFFFF, 0xFF2196F3, false, false)'
        new = 'createCardButton("🔥 WORK WITH SMOKER", 0xFFFFFFFF, 0xFFFF7043, false, false)'
        assert old in s, "menu button anchor missing"
        s = s.replace(old, new, 1)
        changed.append("renamed menu button")

    if "showSmokerBotsDialog(myBrowser)" not in s:
        old = "m1.setOnClickListener(v12 -> { menuDlg.dismiss(); showBotEditor(myBrowser); });"
        new = "m1.setOnClickListener(v12 -> { menuDlg.dismiss(); showSmokerBotsDialog(myBrowser); });"
        assert old in s, "menu click anchor missing"
        s = s.replace(old, new, 1)
        changed.append("wired smoker bots dialog")

    if "final android.view.View btnMenu" not in s:
        old = "final android.widget.TextView btnMenu = findViewById(R.id.btn_menu);"
        new = "final android.view.View btnMenu = findViewById(R.id.btn_menu);"
        assert old in s, "btnMenu declaration anchor missing"
        s = s.replace(old, new, 1)
        changed.append("btnMenu typed as View")

    if "showSmokerBotsDialog(final android.webkit.WebView webView)" not in s:
        anchor = s.rstrip()
        assert anchor.endswith("}"), "unexpected file end"
        # insert before the final class-closing brace
        pos = anchor.rfind("\n}")
        assert pos != -1
        s = anchor[:pos] + "\n" + FEATURE_METHODS.rstrip() + "\n" + anchor[pos:] + "\n"
        changed.append("injected smoker bots manager")

    open(MAIN, "w", encoding="utf-8", newline="").write(s)
    print("MainActivity.java:", ", ".join(changed) or "already patched")

NEW_BTN_MENU = (
    '\t\t<ImageView\r\n'
    '\t\t\tandroid:id="@+id/btn_menu"\r\n'
    '\t\t\tandroid:layout_width="45dp"\r\n'
    '\t\t\tandroid:layout_height="45dp"\r\n'
    '\t\t\tandroid:background="?attr/selectableItemBackgroundBorderless"\r\n'
    '\t\t\tandroid:padding="9dp"\r\n'
    '\t\t\tandroid:scaleType="centerInside"\r\n'
    '\t\t\tandroid:src="@drawable/tools_icon"\r\n'
    '\t\t\tandroid:focusable="true" />'
)

def patch_layout():
    s = open(LAYOUT, encoding="utf-8").read()
    if 'android:src="@drawable/tools_icon"' in s:
        print("main.xml: already patched")
        return
    pat = re.compile(r'\t\t<TextView\r?\n\t\t\tandroid:id="@\+id/btn_menu".*?/>', re.S)
    m = pat.search(s)
    assert m, "btn_menu block not found in main.xml"
    s = s[:m.start()] + NEW_BTN_MENU + s[m.end():]
    open(LAYOUT, "w", encoding="utf-8", newline="").write(s)
    print("main.xml: btn_menu is now the smokey tools icon")

def patch_gradle():
    s = open(GRADLE, encoding="utf-8").read()
    if 'versionName "1.1.0"' in s:
        print("build.gradle: already at 1.1.0")
        return
    s = s.replace("versionCode 1", "versionCode 2", 1)
    s = s.replace('versionName "1.0.0"', 'versionName "1.1.0"', 1)
    open(GRADLE, "w", encoding="utf-8", newline="").write(s)
    print("build.gradle: bumped to 1.1.0 (2)")

patch_main_activity()
patch_layout()
patch_gradle()
print("SMOKER_PACK_OK")
