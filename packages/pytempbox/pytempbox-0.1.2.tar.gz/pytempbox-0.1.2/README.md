# PyTempBox - Python Temporary Email Service

[![PyPI version](https://img.shields.io/pypi/v/pytempbox.svg)](https://pypi.org/project/pytempbox/)
[![Python versions](https://img.shields.io/pypi/pyversions/pytempbox.svg)](https://pypi.org/project/pytempbox/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

PyTempBox is a lightweight Python library for generating and managing temporary email addresses. Perfect for testing, automation, and protecting your privacy when interacting with online services.

## ✨ Features

With this service, you can instantly create temporary email addresses 🚀. Once the email address is generated, you can fetch incoming messages in real-time 📩. The service is designed to be lightweight ⚡, requiring minimal dependencies. Additionally, the API follows best practices in Python programming, making it user-friendly 🐍. Security is a top priority, as all connections are made through secure HTTPS 🔒. You can also retrieve the full content of each message received 📝.

## 📦 Installation

To install the package, simply run the following command in your terminal:

```bash
pip install pytempbox
```

Please note that this package requires Python version 3.9 or higher to work properly.

## 🚀 Quick Start

```python
"""
🔥 PyTempBox Quickstart: Temporary Emails in 3 Steps 🔥

1. Create → 2. Receive → 3. Read
"""

from pytempbox import PyTempBox

# 1️⃣ CREATE - Instant email generator
temp_mail = PyTempBox()
email_address = temp_mail.generate_email()
print(f"📧 Your shiny new temp email: {email_address}")

# 2️⃣ RECEIVE - Smart email checker (auto-retries)
print("\n🕵️ Checking inbox...")
inbox = temp_mail.get_messages(email_address)

if not inbox:
    print("✨ Inbox is empty (try sending a test email first!)")
else:
    # 3️⃣ READ - Clean message display
    print(f"\n📬 Found {len(inbox)} message(s):")
    
    for i, message in enumerate(inbox, 1):
        print(f"\n━━━━ Message #{i} ━━━━")
        print(f"From: {message['from']}")
        print(f"Subject: {message['subject']}")
        print(f"\n{message['body_text'][:200]}...")  # Preview first 200 chars
        print("━━━━━━━━━━━━━━━━━━━━")
```

## 📚 Documentation

### Core Methods

The package offers several useful functions to manage temporary emails. First, you can use `generate_email(min_length=10, max_length=15)` to create a new temporary email address with a specified minimum and maximum length 🆕✉️. To retrieve messages sent to that email, you can call `get_messages(email, timeout=300, interval=10)`, which checks for incoming messages within a set timeout and interval ⏳📥. If you want to see the full content of a specific message, you can use `get_message_content(email, message_id)` to get all the details of that message 📜. Lastly, the function `get_available_domains()` will list all the email domains you can use for generating temporary addresses 🌐.

### Advanced Usage

```python
# Customize email generation
email = client.generate_email(min_length=8, max_length=12)

# Get specific message details
message = client.get_message_content(
    email="your_temp@example.com",
    message_id="12345"
)
```

## 📜 License

This package is distributed under the MIT License, which means you can use, modify, and distribute it freely. For more details about the license, please refer to the [LICENSE](LICENSE) file. 📄✨
