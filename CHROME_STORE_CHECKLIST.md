# Chrome Web Store Submission & Readiness Checklist — Blockium

This document contains the exact text, justifications, and specifications required when publishing or updating Blockium on the **[Chrome Developer Dashboard](https://chrome.google.com/webstore/devconsole)**.

---

## 1. Single Purpose Policy Statement
> **Official Chrome Policy Requirement:** An extension must have a single purpose that is clear to users and contributes to a cohesive user experience.

### Ready-to-Paste Single Purpose Justification:
```text
Blockium has a single, unified purpose: to provide users with a clean, fast, and privacy-protected web browsing experience by blocking intrusive advertisements, cross-site tracking beacons, disruptive video interruptions, and cookie consent overlays directly on their device without collecting personal data.
```

---

## 2. Permissions Justification Table (Manifest V3)

Copy and paste these exact explanations into the **Privacy Practices** tab of your Chrome Web Store listing for each permission declared in `manifest.json`:

| Permission | Justification Text for Chrome Web Store Reviewers |
|:---|:---|
| **`declarativeNetRequest`** | Required to evaluate network requests directly against local ad, tracker, and malware filter lists using Chrome's native C++ engine without intercepting or reading user browsing data. |
| **`declarativeNetRequestWithHostAccess`** | Required to apply domain-specific cosmetic element-hiding rules and scriptlets on websites specified by filter lists or customized by the user. |
| **`storage`** | Required to persist user preferences locally on their machine, including active theme selection, whitelisted domains, custom Element Zapper rules, and aggregate local statistics. |
| **`tabs`** | Required solely to update the extension action badge with the count of blocked requests on the active tab and reset tab-specific counters upon navigation. |
| **`webNavigation`** | Used to detect top-level page commit events to cleanly reinitialize tab-level metrics and execute timing-critical content scriptlets before ads render. |
| **`alarms`** | Required to schedule periodic, low-frequency background checks to download updated open-source filter lists (e.g., EasyList). |
| **`notifications`** | Used exclusively to display optional local desktop alerts when high-risk deceptive phishing domains or malware URLs are blocked. |
| **`<all_urls>` (Host Permission)** | Required so content scriptlets can inject cosmetic hiding CSS, suppress video ad pre-rolls (e.g. on YouTube), and dismiss cookie consent dialogs across any website the user visits. |

---

## 3. Privacy Practices Tab Declarations

* **User Data Collection:** Check **"No"** to all data collection categories.
  - Personal Information: **None**
  - Health / Financial: **None**
  - Authentication: **None**
  - Personal Communications: **None**
  - Location: **None**
  - Web History: **None** (Filter rules match locally; URLs are never transmitted).
  - User Activity: **None**
  - Website Content: **None**
* **Certification:** Check the box certifying that you do not sell user data, use data for creditworthiness/lending, or transfer data for purposes unrelated to the extension's core functionality.

---

## 4. Store Listing Assets & Copy

* **Title (≤ 45 chars):**
  `Blockium Ad Blocker — Fast Adblock & Privacy`
* **Short Description (≤ 132 chars):**
  `Block video ads, intrusive trackers, cookie consent popups, and malicious domains with zero telemetry and 0ms latency.`
* **Official Website URL:**
  `https://blockium.pages.dev`
* **Official Privacy Policy URL:**
  `https://blockium.pages.dev/privacy`
* **Official Terms of Service URL:**
  `https://blockium.pages.dev/terms`
* **Support Email:**
  `blockiumapps@gmail.com`
* **Category:**
  `Tools` or `Productivity`

---

## 5. Required Graphical Assets

| Asset | Size | Status in `assets/` |
|:---|:---|:---|
| **Extension Icon** | 128 × 128 px | ✅ `assets/logo.png` |
| **Small Promo Tile** | 440 × 280 px | ✅ `assets/small_promo_440x280.jpg` |
| **Marquee Promo Banner** | 1400 × 560 px | ✅ `assets/marquee_promo_1400x560.jpg` |
| **Store Screenshot 1** | 1280 × 800 px | ✅ `assets/1_simple_popup_1280x800.jpg` |
| **Store Screenshot 2** | 1280 × 800 px | ✅ `assets/2_advanced_popup_1280x800.jpg` |
| **Store Screenshot 3** | 1280 × 800 px | ✅ `assets/3_dashboard_1280x800.jpg` |
| **Store Screenshot 4** | 1280 × 800 px | ✅ `assets/4_command_center_1280x800.jpg` |
| **Store Screenshot 5** | 1280 × 800 px | ✅ `assets/5_live_feed_1280x800.jpg` |

---

## 6. Automated Verification Audit
Run the automated test suite before any store submission:
```bash
cd /Users/krishan/Documents/antigravity/adblocker && node tests/verify-extension.js
```
* Status: **489 tests passing, 0 failures, 0 eval() calls, 0 remote code vulnerabilities.**
