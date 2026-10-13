# Deutsch Daily 🇩🇪

A mobile-friendly A2–B1 German vocabulary flashcard website.

## Website

After enabling GitHub Pages, the site will be available at:

https://shub0893820-byte.github.io/learn-German/

## Features
- Tap-to-flip vocabulary cards with meanings, noun grammar, examples and translations
- Daily quiz and a lesson archive
- Local browser progress tracking
- Daily lesson archive updates via GitHub Actions at 08:30 Europe/Berlin
- Responsive layout, no frontend framework or paid hosting required

## Enable GitHub Pages
1. Open Settings → Pages in this repository.
2. Under Build and deployment, choose Deploy from a branch.
3. Select branch master and folder /(root), then save.
4. Open Actions and ensure workflows are allowed.
5. The daily workflow checks both possible UTC offsets for Berlin daylight-saving time. It only publishes during Berlin's 08:00 hour.

## Daily vocabulary workflow
The scheduled workflow chooses 25 entries from the curated vocabulary bank, adds them to data/lessons.json, and commits the archive. It doesn't require an API key. The current bank is finite, so words can repeat after the bank cycles; extend data/vocabulary-bank.json to reduce repeats.

## Progress
Progress is saved in the current browser's local storage. It doesn't sync between devices yet.
