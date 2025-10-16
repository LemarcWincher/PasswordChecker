# ==========================================================
# Author: Lemarc Wincher
# Project: Password Strength Checker (CLI)
# Version: 2.0
# Last Updated: October 16th, 2025
# Description:
#   A command-line password strength checker that scores 
#   passwords using regex checks, color-coded feedback, 
#   and a spinner animation. Logs attempts securely to 
#   ~/Documents/PasswordChecker/password_log.txt.
# ==========================================================

import re       # Introduces regex pattern matching
import sys      # Used for writing spinner frames
import time     # Used to pace spinner frames
import os       # Used for log file location
import getpass  # Ensures password is hidden when typed to avoid shoulder-surfing
from datetime import datetime  # Timestamp for logging

# === COLORS ===
RESET = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"

# color support on older Windows setups
try:
    import colorama
    colorama.init()
except Exception:
    pass


# === PASSWORD LOGIC ===

def score_password(password: str, min_len: int = 8, symbols_pat: str = r"[@$!%*?&]") -> int: # Sets parameters for method to pull from
    """scores password 0–5 based on regex checks"""
    score = 0
    if len(password) >= min_len: score += 1
    if re.search(r"[A-Z]", password): score += 1
    if re.search(r"[a-z]", password): score += 1
    if re.search(r"[0-9]", password): score += 1
    if re.search(symbols_pat, password): score += 1
    return score


def rating_from_score(score: int) -> str: # Translates integer score to a proper category how good password protection is
    """translates numeric score into strength label"""
    if score == 5: return "Strong"
    if score >= 3: return "Medium"
    return "Weak"


def log_attempt(attempts: int, score: int, rating: str, logfile: str = "password_log.txt"): # Creates a log with time date, etc according to each password checked
    """writes attempts + rating info to file (no password stored)"""
    import os
    # Make sure the PasswordChecker folder exists inside Documents
    documents_path = os.path.join(os.path.expanduser("~"), "Documents", "PasswordChecker")
    os.makedirs(documents_path, exist_ok=True)  # Create folder if it doesn't exist

    logfile_path = os.path.join(documents_path, logfile)
    with open(logfile_path, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now().isoformat()} | attempts={attempts} | score={score}/5 | rating={rating}\n")

    # Confirmation message showing exact file path where log was saved
    print(YELLOW + f"(Log saved to {os.path.abspath(logfile_path)})" + RESET)


# === INPUT HANDLERS ===

def safe_getpass(prompt: str) -> str: # Ensures getpass works and if it doesn't, switches to input
    """handles password input safely; falls back if getpass breaks"""
    while True:
        try:
            return getpass.getpass(prompt)
        except (EOFError, KeyboardInterrupt):
            print(RED + "\n(Interrupted) Try again." + RESET)
        except Exception:
            print(YELLOW + "(secure input not supported here; switching to visible input)" + RESET) # Fallback option, switches to input incase getpass fails
            try:
                return input(prompt)
            except (EOFError, KeyboardInterrupt):
                print(RED + "\n(Interrupted) Try again." + RESET)


def ask_yes_no(prompt: str) -> bool: # Strict boolean to ensure invalid input is interpreted properly
    """forces y/yes or n/no before continuing"""
    valid_yes = {"y", "yes"}
    valid_no = {"n", "no"}
    while True:
        try:
            ans = input(prompt)
        except (EOFError, KeyboardInterrupt):
            print(RED + "\n(Interrupted) Type y/n or yes/no." + RESET)
            continue

        ans_norm = (ans or "").strip().lower() # Normalizes the answer despite the input for consistent interpretation
        if ans_norm in valid_yes: return True
        if ans_norm in valid_no: return False
        print(RED + "That’s not a yes or no. Try again." + RESET)


def spinner(message="Checking password strength", duration=1.4, fps=14):
    """Lil ASCII spinner next to `message` for `duration`—overwrites in place"""
    frames = "-\\|/" # Frames for the spinning animation
    sys.stdout.write(YELLOW + message + "... " + RESET)
    sys.stdout.flush()
    start = time.time()
    i = 0
    while time.time() - start < duration:
        sys.stdout.write(frames[i % len(frames)])
        sys.stdout.flush()
        time.sleep(1 / fps) # 1 fraction of a second pause for each frame to ensure it is seen
        sys.stdout.write("\b") # Backspace so the next frame replaces the last one, creates the spin animation
        i += 1
    sys.stdout.write("✓\n")
    sys.stdout.flush()


# === MAIN CHECKER ===

def run_password_check():
    """one full password check session"""
    attempts = 0
    while True:
        password = safe_getpass("Please enter your password to continue: ") # Uses getpass to avoid shoulder-surfing

        # Skips if user just hits Enter
        if not password.strip():
            print(RED + "❌ Empty input! Please type a password (not just Enter)." + RESET)
            continue

        attempts += 1
        print(YELLOW + "\nChecking password strength...\n" + RESET)
        spinner("Analyzing password")

        # Step-by-step feedback
        if len(password) < 8:
            print(RED + "❌ Oops, too short! Password must be at least 8 characters." + RESET)
        elif not re.search(r"[A-Z]", password):
            print(RED + "❌ Not quite strong enough! Add at least one uppercase letter." + RESET)
        elif not re.search(r"[a-z]", password):
            print(RED + "❌ Try again! Your password needs at least one lowercase letter." + RESET)
        elif not re.search(r"[0-9]", password):
            print(RED + "❌ Drat! You forgot to add at least one number." + RESET)
        elif not re.search(r"[@$!%*?&]", password):
            print(RED + "❌ Haste makes waste! Please add at least one special character (@, $, !, %, *, ?, &)." + RESET)
        else:
            # All good
            score = score_password(password)
            rating = rating_from_score(score)
            print(GREEN + f"✅ Hurray! You created a strong password in {attempts} attempt(s)! You’re good to go." + RESET)
            print(GREEN + f"🔥 Password score: {score}/5 → {rating}" + RESET)
            log_attempt(attempts, score, rating)
            print(GREEN + "✅ All done! Thanks for checking your password with me." + RESET)
            break

        # Show rating even when it fails
        score = score_password(password)
        rating = rating_from_score(score)
        print(YELLOW + f"⚠️ Password score: {score}/5 → {rating}" + RESET)

        # Ask to retry
        retry_yes = ask_yes_no(YELLOW + "\nPassword not strong enough! Would you like to try again? (y/n): " + RESET)
        if not retry_yes:
            print(GREEN + "✅ All done! Thanks for checking your password with me." + RESET)
            print(GREEN + f"\nThank you for using my password checker! Attempts made: {attempts}. Have a great day!" + RESET)
            log_attempt(attempts, score, rating)
            return  # Exits this run
        print()  # Space before next round


# === MAIN PROGRAM ===

def main():
    print(GREEN + "====================================" + RESET)
    print(GREEN + "🔐  Welcome to Lemarc's Password Checker!  🔐" + RESET)
    print(GREEN + "====================================\n" + RESET)

    while True:
        run_password_check()

        # Ask to do another full check
        another = ask_yes_no(YELLOW + "\nNice job! Would you like to check another password? (y/n): " + RESET)
        if not another:
            print(GREEN + "\nThanks for using my checker! Stay secure out there 🔒" + RESET)
            break
        print()  # Spacing for next run


# === RUN ===
if __name__ == "__main__":
    main()
