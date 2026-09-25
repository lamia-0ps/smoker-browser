package com.smoke.browser;

import android.app.Activity;
import android.os.Bundle;
import android.widget.ScrollView;
import android.widget.TextView;

/** Crash reporter screen referenced by SmokeBrowser. */
public class DebugActivity extends Activity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        ScrollView sv = new ScrollView(this);
        TextView tv = new TextView(this);
        tv.setTextIsSelectable(true);
        tv.setPadding(48, 48, 48, 48);
        tv.setTextSize(13f);
        String err = getIntent() != null ? getIntent().getStringExtra("error") : null;
        tv.setText(err != null && !err.isEmpty() ? err : "No error details.");
        sv.addView(tv);
        setContentView(sv);
    }
}
