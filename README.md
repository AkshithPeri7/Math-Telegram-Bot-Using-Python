# Math Telegram Bot Using Python 🤖➗

A Python-powered Telegram bot that makes common mathematical calculations and number-based utilities accessible through a simple chat interface.

This project is associated with the research paper **“MATH TELEGRAM BOT USING PYTHON”**, published in the *Journal of Emerging Technologies and Innovative Research (JETIR)* in July 2025.

## ✨ Features

The research publication lists these mathematical utilities:

- Factorial
- Prime number check
- Armstrong number check
- Palindrome check
- Fibonacci sequence
- Greatest Common Divisor (GCD)
- Least Common Multiple (LCM)
- Digit sum and digit count
- Interactive Telegram bot interface and inline keyboards

> Feature availability depends on the version of the code in this repository.

## 🛠️ Technologies

- **Python** — core programming language
- **Telegram Bot API** — messaging interface
- **python-telegram-bot** — Python library for Telegram bot development

## 🚀 Getting Started

### Prerequisites

- Python 3 installed
- A Telegram account
- A bot token created using Telegram's **@BotFather**

### Installation

1. Clone this repository:

   ```bash
   git clone <YOUR_REPOSITORY_URL>
   cd <YOUR_REPOSITORY_FOLDER>
   ```

2. Install dependencies. If the repository has a `requirements.txt` file, run:

   ```bash
   pip install -r requirements.txt
   ```

   Otherwise, install the Telegram library (and any other dependencies required by the source code):

   ```bash
   pip install python-telegram-bot
   ```

3. Configure your bot token securely. For example, set an environment variable:

   **Windows PowerShell:**
   ```powershell
   $env:TELEGRAM_BOT_TOKEN="YOUR_BOT_TOKEN"
   ```

   **macOS / Linux:**
   ```bash
   export TELEGRAM_BOT_TOKEN="YOUR_BOT_TOKEN"
   ```

   Ensure the bot's source code reads the token from `TELEGRAM_BOT_TOKEN`, or adapt its existing configuration accordingly. **Never commit your token to GitHub.**

4. Run the bot using the actual entry-point filename in this repository. For example, if the main script is named `main.py`:

   ```bash
   python main.py
   ```

## 💬 How to Use

1. Open your bot in Telegram.
2. Send `/start` to begin, if supported by your implementation.
3. Choose a mathematical utility from the available menu or follow the bot's prompts.
4. Enter the requested number(s) and view the result.

## 📄 Research Publication

| Detail | Information |
| --- | --- |
| **Paper** | MATH TELEGRAM BOT USING PYTHON |
| **Journal** | Journal of Emerging Technologies and Innovative Research (JETIR) |
| **Publication date** | July 2025 |
| **Volume / Issue** | 12 / 7 |
| **Paper ID** | JETIR2507096 |
| **Pages** | a929–a941 |
| **ISSN** | 2349-5162 |

**Authors:** Akshith Peri, Anup Kabra, Chirag D Bedre, Choyan Paul, Dr. Nirmala S.

📖 [View published research paper](https://www.jetir.org/view?paper=JETIR2507096)  
📥 [Read the research paper (PDF)](https://www.jetir.org/papers/JETIR2507096.pdf)

### Citation

> Akshith Peri, Anup Kabra, Chirag D Bedre, Choyan Paul, and Dr. Nirmala S., “MATH TELEGRAM BOT USING PYTHON,” *Journal of Emerging Technologies and Innovative Research*, vol. 12, no. 7, pp. a929–a941, July 2025. Paper ID: JETIR2507096.

## 🔮 Future Improvements

Potential enhancements include more mathematical functions, improved input validation, better error handling, and expanded interactive menus.

## 🤝 Contributions

Suggestions and improvements are welcome. Open an issue or submit a pull request.

---

**Note:** The installation and execution commands above are templates because the repository source files have not been provided. Update the repository URL, folder name, entry-point script, and dependency instructions to match the actual code.
