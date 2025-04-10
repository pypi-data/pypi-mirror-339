# Streamlit Session Manager

A simple session management library for Streamlit applications that allows easy access to user session data from cookies.

## Installation

```bash
pip install 5x-streamlit-session-manager
```

## Usage

```python
import streamlit as st
from streamlit_session_manager import SessionManager

# Initialize the session manager
session = SessionManager()

# Get user details
user = session.get_user()
if user:
    email = user.get('email')
    first_name = user.get('first_name')
    last_name = user.get('last_name')

# Or get just the email
email = session.get_email()

# Or get the full name
full_name = session.get_full_name()
```

## Features

- Easy access to user session data
- Get email address from session
- Get user's full name
- Get complete user details
- Error handling and type safety

## Requirements

- Python 3.7+
- Streamlit 1.0.0+
- extra-streamlit-components 0.1.0+

## License

This project is licensed under the MIT License - see the LICENSE file for details.
