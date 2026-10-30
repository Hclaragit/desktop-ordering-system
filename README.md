# Desktop Ordering & Management System (Prototype)

A desktop ordering application with separate customer and manager workflows, built with Python and CustomTkinter. It stores its data in a Google Sheet through the Google Sheets API.

This is an individual project for IB Computer Science (Internal Assessment). It is an educational prototype, not a production system. See [Limitations](#limitations-and-known-issues) before reading the code.

## Status

> **Needs your own setup to run.** The code expects a Google Sheet, OAuth credentials and (optionally) a Gmail app password, none of which are included. They are read from environment variables (see `.env.example`).

## What it does

Customer side:
- Login and sign-up screen, with a password-change option using a security answer
- Menu pages for beverages, desserts and foods, with a cart
- Checkout with a payment choice and optional use of loyalty points (1 point earned per 10 dollars spent; 1 point reduces the total by 1 dollar)
- A purchase summary pop-up and a confirmation email sent through Gmail SMTP
- "My page" for leaving a rating and a comment on a menu item, and a feedback pop-up

Manager side:
- Manager login
- A list of pending orders, with a button to mark an order as finished
- Order history page
- Page to view ratings and comments, filtered by menu type and item

Menu items, users, points, orders and ratings are all stored in Google Sheets tabs (`login screen`, `menu page`, `manager page`, `order history page`, `Rating&comments`).

## Tech stack

- Python 3
- CustomTkinter / Tkinter for the GUI
- Google Sheets API (`google-api-python-client`, `google-auth-oauthlib`) as the data store
- `smtplib` for email notifications

## Project structure

| File | Role |
| --- | --- |
| `loginscreen.py` | Entry point. Login, sign-up and change-password windows |
| `mainpage.py` | Customer home page (category buttons) |
| `menupage.py` | Menu list, cart, checkout, points, email |
| `mypage.py` | Customer rating and comment page |
| `managerpage.py` | Manager order list and "finish order" action |
| `orderhistorypage.py` | Order history view |
| `ratingcommentspage.py` | Manager view of ratings and comments |
| `csiagooglesheet.py` | Google Sheets authentication and data loading helpers |
| `Archive.zip` | Older archive containing copies of the same eight files (not needed to run) |

## Setup (what would be required)

1. Python 3 with Tk support. Install the dependencies:
   ```
   pip install -r requirements.txt
   ```
2. A Google Cloud OAuth client file (`credentials.json`) with the Google Sheets API enabled. Put it in the working directory or point `GOOGLE_CREDENTIALS_FILE` at it. The first run opens a browser to authorise and writes `token.json` to the working directory.
3. A Google Sheet with the tabs and cell layout listed above, with its ID in the `SPREADSHEET_ID` environment variable. The original sheet is private and is not part of this repository, so the exact column layout can only be inferred from the code.
4. Optional, for confirmation emails: a Gmail account and app password in `SHOP_EMAIL` and `SHOP_EMAIL_APP_PASSWORD`. If they are not set, the app skips sending. `.env.example` lists the variables, but the code does not load a `.env` file, so export them in your shell first.
5. Run:
   ```
   python loginscreen.py
   ```

## Limitations and known issues

- **Authentication is a simulation.** Passwords and security answers are stored and compared as plain text in the spreadsheet, and the manager password is read from the sheet as well. There is no hashing, rate limiting or session handling. Do not reuse real passwords.
- **Configuration is read from environment variables only.** There is no `.env` loader, and startup fails with an error if `SPREADSHEET_ID` is missing.
- **Network calls happen at import time.** Most modules call `csiagooglesheet.main()` when imported, so each page needs a working Google connection just to load.
- **Concurrency is not handled.** Orders and points are written back to the sheet with plain reads and writes, so two users at the same time could overwrite each other.
- **Error handling is minimal.** Email failures are only printed to the console.
- **No automated tests.** Behaviour has not been verified in this repository.
- Some UI text contains typos and some identifiers are misspelled (for example `upadate_DB`). These were left as they are.

## Credits

Individual project. Design diagrams (class diagrams, flowcharts, UI sketches) from the original IA exist outside this folder and are not included here.
