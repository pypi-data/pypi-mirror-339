# SimpleLogin API Client

A Python client for interacting with the SimpleLogin API.

## Features

*   List aliases
*   List mailboxes
*   Create custom aliases
*   Create random aliases

## Installation

Requires the `requests` library:

```bash
pip install requests
```

## Usage

### Initialization

First, import the client and initialize it with your SimpleLogin [API](https://app.simplelogin.io/dashboard/api_key) key.

````python
from simplelogin import SimpleLoginClient, AliasMode

api_key = "YOUR_API_KEY"  # Replace with your actual API key
client = SimpleLoginClient(api_key)

# List all aliases (first page)
aliases = client.list_aliases()
if aliases:
    for alias in aliases:
        print(alias['email'])

# List pinned aliases
pinned_aliases = client.list_aliases(pinned=True)

# Search for aliases containing 'example'
search_results = client.list_aliases(query="example")

mailboxes = client.list_mailboxes()
if mailboxes:
    for mailbox in mailboxes:
        print(f"ID: {mailbox['id']}, Email: {mailbox['email']}")

# Get available mailboxes first (needed for mailbox_ids)
mailboxes = client.list_mailboxes()
if mailboxes:
    mailbox_ids = [m['id'] for m in mailboxes] # Use IDs of mailboxes to receive emails

    new_alias = client.create_custom_alias(
        prefix="my_custom_prefix",
        mailbox_ids=mailbox_ids,
        suffix="@yourdomain.com", # Optional: Uses the first available suffix if None
        name="My Alias Name",      # Optional
        note="Alias for testing"   # Optional
    )

    if new_alias:
        print(f"Created alias: {new_alias['email']}")
    else:
        print("Failed to create custom alias.")
else:
    print("Could not fetch mailboxes.")

# Create a random alias using words (default)
random_alias_word = client.create_random_alias(note="Random word alias")
if random_alias_word:
    print(f"Created random word alias: {random_alias_word['email']}")

# Create a random alias using UUID
random_alias_uuid = client.create_random_alias(mode=AliasMode.UUID, note="Random UUID alias")
if random_alias_uuid:
    print(f"Created random UUID alias: {random_alias_uuid['email']}")
