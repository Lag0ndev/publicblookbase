# Blookbase Firebase (chat)

## Important: the web config is NOT a secret

The Firebase `apiKey`, `projectId`, `appId`, etc. are **meant to be public** in any website.
Hiding them in a private GitHub folder does **not** stop someone from reading them from the browser.

**Real security = Security Rules** (this folder) + optionally Firebase Auth later.

## Never commit these

- Service account JSON (`*firebase-adminsdk*.json`)
- Private keys
- Server-only secrets

Only commit rules, indexes, and `firebase.json` / `.firebaserc`.

## Deploy rules (from this folder)

```bash
npm i -g firebase-tools
firebase login
firebase use blookbase
firebase deploy --only firestore:rules
```

In [Firebase Console](https://console.firebase.google.com/) → **Firestore Database**:
1. Create database (production mode is fine — rules below will open chat safely).
2. Deploy the rules in `firestore.rules`.

## What the rules allow

| Action | Allowed? |
|--------|----------|
| Read chat messages | Yes (public) |
| Send a new message | Yes, if text ≤ 300 chars, name ≤ 24, valid timestamp |
| Edit / delete messages | **No** (clients blocked) |
| Any other collection | **No** |

## Optional hardening later

- Firebase Anonymous Auth + `request.auth != null`
- Cloud Functions rate limiting
- Admin SDK moderation tools

