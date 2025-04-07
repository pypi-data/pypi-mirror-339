# Tgpdc Mailer

[![PyPI version](https://badge.fury.io/py/ms-template-mailer.svg)](https://badge.fury.io/py/ms-template-mailer)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)

> A simple Python package for sending templated emails using Microsoft Graph API.

## 📋 Table of Contents

- [Features](#-features)
- [Installation](#-installation)
- [Prerequisites](#-prerequisites)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [Examples](#-examples)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

## ✨ Features

- 📧 Send HTML templated emails using Microsoft Graph API
- 🔄 Simple template variable substitution
- 👥 Support for multiple recipients, CC, and BCC
- ⚙️ Environment variable configuration support
- 🚀 Easy-to-use API

## 📥 Installation

```bash
pip tgpdc-mailer
```

## 📝 Prerequisites

1. Microsoft Azure Account
2. Registered Application in Azure AD with permissions:
   - `Mail.Send`
   - `Mail.Send.Shared`

## ⚙️ Configuration

### Environment Variables

Create a `.env` file:

```env
TENANT_ID=your_tenant_id
CLIENT_ID=your_client_id
CLIENT_SECRET=your_client_secret
SENDER_EMAIL=your_sender_email@domain.com
```

### Direct Initialization

```python
from tgpdc_mailer import Mailer

mailer = Mailer(
    tenant_id="your_tenant_id",
    client_id="your_client_id",
    client_secret="your_client_secret",
    sender_email="your_sender_email@domain.com"
)
```

## 🚀 Usage

### Basic Example

```python
from tgpdc_mailer import Mailer

# Initialize the mailer
mailer = Mailer()

# Send email
result = mailer.send_email(
    to_emails="recipient@example.com",
    subject="Welcome Email",
    template_path="templates/welcome.html",
    template_context={
        "name": "John Doe",
        "company": "ACME Corp"
    }
)
```

## 📝 Examples

### Template Structure

```html
<!DOCTYPE html>
<html>
<body>
    <h1>Welcome {{ name }}!</h1>
    <p>Thank you for joining {{ company }}.</p>
</body>
</html>
```

### Multiple Recipients

```python
result = mailer.send_email(
    to_emails=[
        "recipient1@example.com",
        "recipient2@example.com"
    ],
    subject="Team Update",
    template_path="templates/update.html",
    template_context={
        "update_text": "New project starting next week"
    },
    cc_emails=["manager@example.com"],
    bcc_emails=["archive@example.com"]
)
```

### Error Handling

```python
result = mailer.send_email(
    to_emails="recipient@example.com",
    subject="Test Email",
    template_path="templates/notification.html",
    template_context={"message": "Hello World!"}
)

if result['success']:
    print("Email sent successfully!")
else:
    print(f"Failed to send email: {result['message']}")
```

## 🔧 Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| Authentication Failed | Check Azure AD credentials and permissions |
| Template Not Found | Verify template path and file existence |
| Invalid Recipients | Validate email address format |


## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.


## 🙏 Acknowledgments

- Microsoft Graph API
- Python Requests Library
- Python-dotenv

## 📝 Version History

| Version | Changes |
|---------|---------|
| 0.1.1   | Initial Release |
