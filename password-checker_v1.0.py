# ==========================================================
# Author: Lemarc Wincher
# Project: Password Strength Checker (CLI)
# Version: 1.0
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

# Color codes (ANSI) to be used later in prompt messages
RED    = "\033[31m"
GREEN  = "\033[32m"
YELLOW = "\033[33m"
RESET  = "\033[0m"

# Optional: color support on older Windows setups (safe to ignore if missing)
try:
    import colorama
    colorama.init()
except Exception:
    pass

# Friendly opening message to greet the user
print(GREEN + "====================================" + RESET)
print(GREEN + "🔐  Welcome to Lemarc's Password Checker!  🔐" + RESET)
print(GREEN + "====================================\n" + RESET)

# Prompts user to enter password until password is strong enough (exceeds parameters)
attempts = 0  # Counts how many tries the user takes

while True:
    # Uses getpass to hide user password to avoid shoulder-surfing (with fallback if terminal doesn't support hidden input)
    while True:
        try:
            password = getpass.getpass("Please enter your password to continue: ")
            break
        except (EOFError, KeyboardInterrupt):
            print(RED + "\n(Interrupted) Please type your password." + RESET)
        except Exception:
            # Fallback option, switches to input incase getpass fails
            print(YELLOW + "(Secure input not supported here; switching to visible input.)" + RESET)
            try:
                password = input("Please enter your password to continue: ")
                break
            except (EOFError, KeyboardInterrupt):
                print(RED + "\n(Interrupted) Please type your password." + RESET)

    # Edge case: empty input (user just hits Enter)
    if not password.strip():
        print(RED + "❌ Empty input! Please type a password (not just Enter)." + RESET)
        continue  # Go back to the start of the loop without counting an attempt

    attempts += 1  # Each time a password is entered, attempts go up one
    print(YELLOW + "\nChecking password strength...\n" + RESET)

    # Tiny spinner animation (ASCII) so it feels responsive
    frames = "-\\|/"  # Frames for the spinning animation
    start = time.time()
    duration = 1.2
    fps = 14
    sys.stdout.write(YELLOW + "Analyzing password... " + RESET)
    sys.stdout.flush()
    i = 0
    while time.time() - start < duration:
        sys.stdout.write(frames[i % len(frames)])
        sys.stdout.flush()
        time.sleep(1 / fps)  # 1 fraction of a second pause for each frame to ensure it is seen
        sys.stdout.write("\b")  # Backspace so the next frame replaces the last one, creates the spin animation
        i += 1
    sys.stdout.write("✓\n")
    sys.stdout.flush()

    # Checks password strength using regex
    if len(password) < 8:  # Ensures at least 8 characters
        print(RED + "❌ Oops, too short! Password must be at least 8 characters." + RESET)
    elif not re.search(r"[A-Z]", password):  # Ensures at least one uppercase letter
        print(RED + "❌ Not quite strong enough! Add at least one uppercase letter." + RESET)
    elif not re.search(r"[a-z]", password):  # Ensures at least one lowercase letter
        print(RED + "❌ Try again! Your password needs at least one lowercase letter." + RESET)
    elif not re.search(r"[0-9]", password):  # Ensures at least one number
        print(RED + "❌ Drat! You forgot to add at least one number." + RESET)
    elif not re.search(r"[@$!%*?&]", password):  # Ensures at least one special character
        print(RED + "❌ Haste makes waste! Please add at least one special character (@, $, !, %, *, ?, &)." + RESET)
    else:
        # Creates score to calculate password strength based on parameters met
        score = 0
        if len(password) >= 8:
            score += 1
        if re.search(r"[A-Z]", password):
            score += 1
        if re.search(r"[a-z]", password):
            score += 1
        if re.search(r"[0-9]", password):
            score += 1
        if re.search(r"[@$!%*?&]", password):
            score += 1

        # Displays strength rating
        if score < 3:
            print(YELLOW + f"⚠️ Password score: {score}/5 → Weak" + RESET)
        elif score in (3, 4):
            print(YELLOW + f"⚠️ Password score: {score}/5 → Medium" + RESET)
        else:
            print(GREEN + f"🔥 Password score: {score}/5 → Strong" + RESET)

        # Validates password if it passes regex check
        # NOTE: pass = at least 8, has upper, lower, digit, symbol (already ensured above)
        print(GREEN + f"✅ Hurray! You created a strong password in {attempts} attempt(s)! You’re good to go." + RESET)

        # Creates/updates a log entry in Documents/PasswordChecker/password_log.txt
        documents_path = os.path.join(os.path.expanduser("~"), "Documents", "PasswordChecker")
        os.makedirs(documents_path, exist_ok=True)  # Create folder if it doesn't exist
        logfile_path = os.path.join(documents_path, "password_log.txt")
        with open(logfile_path, "a", encoding="utf-8") as f:
            f.write(f"{datetime.now().isoformat()} | attempts={attempts} | score={score}/5 | rating="
                    f"{'Strong' if score == 5 else ('Medium' if score >= 3 else 'Weak')}\n")
        print(YELLOW + f"(Log saved to {os.path.abspath(logfile_path)})" + RESET)

        # Friendly wrap-up message
        print(GREEN + "✅ All done! Thanks for checking your password with me." + RESET)
        break  # Exits loop upon success

    # If we got here, one of the checks failed → show score/rating too (helpful feedback)
    # Creates score to calculate password strength based on parameters met (fail path)
    score = 0
    if len(password) >= 8:
        score += 1
    if re.search(r"[A-Z]", password):
        score += 1
    if re.search(r"[a-z]", password):
        score += 1
    if re.search(r"[0-9]", password):
        score += 1
    if re.search(r"[@$!%*?&]", password):
        score += 1

    # Displays strength rating on failure paths
    if score < 3:
        print(YELLOW + f"⚠️ Password score: {score}/5 → Weak" + RESET)
    elif score in (3, 4):
        print(YELLOW + f"⚠️ Password score: {score}/5 → Medium" + RESET)
    else:
        print(GREEN + f"🔥 Password score: {score}/5 → Strong" + RESET)

    # Prompts user to try again if regex check failed
    # Strict boolean to ensure invalid input is interpreted properly
    while True:
        retry = input(YELLOW + "\nPassword not strong enough! Would you like to try again? (y/n): " + RESET).strip().lower()  # Ensures input is clean
        if retry in ("y", "yes"):
            print()  # Formatted spacing
            break  # try again → go back to while True (outer)
        if retry in ("n", "no"):  # If the user did not say yes, thank them and close program
            print(GREEN + "✅ All done! Thanks for checking your password with me." + RESET)
            print(GREEN + f"\nThank you for using my password checker! Attempts made: {attempts}. Have a great day!" + RESET)

            # Also log the last attempt (even on exit) to keep history complete
            documents_path = os.path.join(os.path.expanduser("~"), "Documents", "PasswordChecker")
            os.makedirs(documents_path, exist_ok=True)
            logfile_path = os.path.join(documents_path, "password_log.txt")
            with open(logfile_path, "a", encoding="utf-8") as f:
                f.write(f"{datetime.now().isoformat()} | attempts={attempts} | score={score}/5 | rating="
                        f"{'Strong' if score == 5 else ('Medium' if score >= 3 else 'Weak')}\n")
            print(YELLOW + f"(Log saved to {os.path.abspath(logfile_path)})" + RESET)
            raise SystemExit(0)
        print(RED + "Hey! That's not a yes or no. Please type y/n (or yes/no)." + RESET)
