# Lemarc’s Password Strength Checker
A command-line tool written in Python that checks the strength of a password in real time. Built as a personal project to improve my regex, input handling, and file I/O skills.

## What It Does
- Prompts the user to enter a password securely (hidden input using `getpass`)
- Validates the password with regex for:
  - Minimum length (8+)
  - Uppercase & lowercase letters
  - Numbers
  - Special characters (`@ $ ! % * ? &`)
- Gives **color-coded feedback** on each attempt
- Tracks how many tries it took to create a strong password
- Displays a small **spinner animation** while checking
- Logs each session’s results to: Documents/PasswordChecker/password_log.txt

*(no passwords are stored — just timestamps, scores, and ratings)*

## Technologies Used
- **Python 3**
- Built-in modules: `re`, `getpass`, `datetime`, `sys`, `time`, `os`
- **Colorama** for cross-platform terminal color support

## Example Output

Please enter your password to continue:
Checking password strength...

❌ Not quite strong enough! Add at least one uppercase letter.
⚠️ Password score: 3/5 → Medium

Password not strong enough! Would you like to try again? (y/n): y

✅ Hurray! You created a strong password in 2 attempt(s)! You’re good to go.
🔥 Password score: 5/5 → Strong
(Log saved to C:\Users\Lemarc\Documents\PasswordChecker\password_log.txt)
✅ All done! Thanks for checking your password with me.


## What I Learned
- How to design input loops with **regex-based validation**
- How to use `getpass` to prevent **shoulder-surfing**
- How to **handle exceptions** gracefully
- How to add basic **terminal animations** for user experience
- How to log safely without saving sensitive data

## 📚 Version History
- **v1.0** → single-file version (manual structure, learning build)
- **v2.0** → refactored version with methods, spinner, and structured logging

## About Me
I’m **Lemarc Wincher**, a CIS junior at **Texas State University (McCoy College of Business)**. I build small tools like this to strengthen my understanding of IT, cybersecurity, and automation fundamentals — always aiming to grow one project at a time.

📫 **Contact:**  
- Email: [lemwincher@gmail.com](mailto:lemwincher@gmail.com)  
- LinkedIn: [linkedin.com/in/lemarc-wincher](https://linkedin.com/in/lemarc-wincher)

> *"Every project starts small — what matters is that it gets finished."*
