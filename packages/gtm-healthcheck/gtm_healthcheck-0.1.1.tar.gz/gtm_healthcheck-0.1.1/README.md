# GTM Healthcheck

**GTM Healthcheck** is a command-line tool that analyzes a Google Tag Manager (GTM) container export (`.json` file) and calculates the size (in KB) of each **tag**, **trigger**, and **variable**.

This helps marketers, analysts, and developers clean up their containers by identifying old, bloated, or unused elements — and freeing up space for new tags with just one command.

---

## 🚨 Problem It Solves

**Current process:**
- You pause or delete a tag/trigger/variable manually in a dummy container and publish the container.
- Check if the container size decreased in version history.
- Repeat over and over — very time-consuming, takes upto 3-4 hrs or more depending upon container size.

**With GTM Healthcheck:**
- Just install and run our automation.
- It gives you a complete CSV report of how much space each element takes.
- Done in **under a minute** — no guesswork.

---

## 📦 Installation

Install the tool using below command:

```bash
pip install gtm-healthcheck
```

---

## 🚀 Usage

### 1. Export your container from GTM
- Go to **Admin > Export Container** in your GTM account.
- Save the `.json` file locally (e.g., `container.json`).

### 2. Run the tool

```bash
healthcheck <container.json>
```
Replace `<container.json>` with actual gtm container filename which you have downloaded

This generates a CSV report in the current directory (default: `healthcheck.csv`)

---

## 📊 Output Format

The output CSV includes:

| Type     | Name                    | Size (KB) |% Occupied |   
|----------|-------------------------|-----------|-----------|
| Tag      | GA4 - Pageview          | 2.87      |3.5%       |
| Trigger  | Click - All Buttons     | 1.25      |1.2%       |
| Variable | Custom JavaScript Helper| 3.14      |0.6%       |

This allows you to:
- Identify heavy tags or unused variables
- Sort/filter by size or type
- Share with your team or agency

---

## ✅ When Should You Use This?

- Before publishing large GTM changes
- When you're hitting GTM container size limits
- To audit old containers for optimization
- During migration/cleanup projects
- As part of your QA process

---

## 🔐 Data Privacy

This tool works **locally on your machine** and does **not send any data externally**. Your GTM export stays secure and private.

---

## ❤️ Built For

Marketers • Analysts • Developers  
To save time, simplify GTM audits, and make container management efficient.

---

## Legal Notice

This tool is an **internal property** of **WebEngage** and is strictly for **auditing purposes**. It is owned by **Nipun Patel (Copyright)** and any misuse, unauthorized distribution, or external sharing will lead to **legal consequences**.

---

© WebEngage. All rights reserved.
