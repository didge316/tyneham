# Tyneham Village — Contact Form Setup

**Service:** [Web3Forms](https://web3forms.com)  
**Account:** log in at web3forms.com to find the access key and manage submissions

## How it works

A JavaScript `fetch` call POSTs to `https://api.web3forms.com/submit` as JSON, including the access key, a custom subject line ("New Contact Form Message - Tyneham Village"), and the reply-to address. On success the user is sent to `thank-you.html`. On failure an inline error appears and the button is re-enabled.

## Files

- `contact.html` — the form
- `thank-you.html` — the success page (set to `noindex`)

## Spam protection

Honeypot `botcheck` field (hidden checkbox), plus Web3Forms' built-in spam filtering.
