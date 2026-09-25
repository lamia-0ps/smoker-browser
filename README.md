# Smoker Browser

Smoker Browser is an Android web browser with automation as a first-class feature rather than an add-on. You get a normal, visible, fully interactive browser — and the same page exposes a scripting surface that can read source, drive native gestures, clear sessions, and pull streams down to storage.

It is meant for people who script the web from a phone: repetitive form entry, scheduled lookups, multi-site data collection, or QA passes when a laptop isn't around.

```
Android 5.0+ · ~6 MB · no accounts · no telemetry
```

---

## Why this exists

Most mobile automation gives you two bad options. Either you tether to a desktop driver and lose the phone entirely, or you run a headless stack that never quite renders what a real user sees.

Smoker Browser takes a third route: keep a real WebView that a human can also use, and hand the same page to JavaScript with a bridge into the Android layer. If a task needs a tap at a specific coordinate, a scroll past a lazy-loaded block, or a file pulled out of a blob URL, the script can do it directly.

---

## Install

Build from source (below) and sideload the resulting APK, or grab a build from the repository's **Releases** page.

Android will ask you to allow installation from an unknown source the first time. There is no Play Store listing; the app needs the broad permissions that automation requires.

---

## Quick start

1. Launch the app and let the start page load.
2. Open the **⋮** menu and choose the bot tool you need.
3. Paste or edit your script, then run it.
4. Scripts persist between launches, so a workflow you set up once is there next time.

A minimal example — pull the page source and hand it to your own logic:

```js
var html = Code.Bot();
console.log(html.length + " characters");
Bot.search("low poly models");
```

A slightly more useful one — wait for a list to render, then scroll it:

```js
setTimeout(function () {
  AppBot.scrollDown(600);   // move a real finger, not a synthetic event
}, 2500);
```

---

## Scripting surface

The browser injects a set of helpers into every page. Calls are marshalled into Java and executed natively, so they behave the same whether the page is quiescent or mid-navigation.

| Call | What it does |
| --- | --- |
| `Code.Bot()` | Returns the current document source as a string |
| `Cleaner.Bot()` | Wipes cookies and site storage to start from a clean session |
| `Bot.search(query)` | Runs a search through the native path instead of the omnibox |
| `AppBot.*` | Dispatches real touch input — clicks, swipes, scrolls — at the OS level |

Because `AppBot` goes through `dispatchTouchEvent`, it works on pages that ignore synthetic JavaScript events: canvas widgets, gesture handlers, and anything gated behind a trusted-input check.

---

## Browser features

- **Search-or-URL bar** with a clear button, plus pull-to-refresh and a thin load indicator.
- **Ad and popup filtering**, on by default. Overlay and redirect popups are suppressed before they take over the screen, and a single menu toggle turns filtering off for a site that misbehaves under it.
- **Stream capture.** When a page produces a download through a blob or data URL, the payload is intercepted, converted, and handed to Android's download manager instead of being dropped.
- **Persistent injection.** The automation hooks stay attached across navigation rather than firing once on load.
- **Desktop site, zoom, and refresh controls** in the same menu.
- **Picture-in-picture**, so a long-running page keeps rendering while you do something else.

---

## Building

Requirements:

- JDK 17
- Android SDK 34 (`platforms;android-34`, `build-tools;34.0.0`)
- Gradle 8.9 or newer

Point Gradle at your SDK and build:

```bash
echo "sdk.dir=$ANDROID_HOME" > local.properties
gradle assembleDebug
```

The APK lands in `app/build/outputs/apk/debug/`. Open the project in Android Studio if you prefer; the Gradle setup works unmodified.

Launcher icons are generated rather than committed by hand:

```bash
pip install pillow
python scripts/make_icon.py
```

---

## Project layout

```
app/src/main/
  AndroidManifest.xml            permissions, activities, browser intent filters
  java/com/smoke/browser/
    MainActivity.java            browser surface, menus, all bot bridge objects
    SmokeBrowser.java            Application entry point and crash capture
    DebugActivity.java           crash report viewer
    AppUtil.java                 UI helpers
    FileUtil.java                file, bitmap and content-URI utilities
  res/
    layout/main.xml              app shell: toolbar, progress bar, WebView
    values/                      strings, smoke/ember palette, theme
    mipmap-*/                    generated launcher icons
    drawable/                    adaptive icon layers
scripts/make_icon.py             icon generator
```

---

## Notes and limits

- Automation changes what a site sees. That does not change what the site's terms allow — check them before you point this at someone's service.
- `AppBot` runs on the main thread, so long gesture sequences are best spaced out.
- Filtering is heuristic, not a full content-blocking engine. Some first-party interstitials will still get through.

---

## License

GPL-3.0 — see [LICENSE](LICENSE).

This project is a modified distribution of an upstream work under the same license: it has been rebranded, re-namespaced to `com.smoke.browser`, and given a new interface and build configuration.