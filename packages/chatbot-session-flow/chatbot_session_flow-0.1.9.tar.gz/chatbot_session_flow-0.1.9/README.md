# WhatsApp Chatbot Session Flow

## Overview

This package provides a **Django-based** session management system for building a WhatsApp chatbot. It enables:

- **Dynamic page-based navigation**
- **Session tracking**
- **Dynamic method execution** for custom tasks (e.g., adding to cart)
- **Middleware support**
- **Admin integration**

## Installation

Install the package via pip:

```bash
pip install chatbot_session_flow
```

### Environment Variables

Set the following environment variables in your shell or a `.env` file:

```bash
export pub_key=""
export secret=""
export SECRET_KEY="xx56r_@x_jb8(rqiw5+xw^+@l#m(=%9h+!98k1o$ex3_zogx"
export MODE=dev
export DEBUG=True
export DB_NAME=<dbname>
export DB_USER=<db connection user>
export DB_PASSWORD=<database password>
export DB_HOST="<database connection host>"
export DB_PORT=<database running port>
export NGUMZO_API_KEY=<your api key if using ngumzo APIs>
export DYNAMIC_METHOD_VIEWS="<your_app.dynamic_methods>"
```

### Django Settings

Add it to your `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    ...,
    'chatbot_session_flow',
]
```

Add middleware to enable session handling:

```python
MIDDLEWARE = [
    ...,
    'chatbot_session_flow.middleware.WhatsappSessionMiddleware',
]
```

### Migrations

Run the migrations:

```bash
python manage.py makemigrations chatbot_session_flow
python manage.py migrate chatbot_session_flow
```

## Internal Logic

The chatbot flow is managed through a sequence of `Page` instances. Each page can reference the next, allowing dynamic navigation.
Sessions are tied to users via the `Session` and `Stepper` models.

### Dynamic Methods

Custom tasks such as saving data, calling APIs, or formatting messages are handled by dynamic methods specified in a dynamic file defined by `DYNAMIC_METHOD_VIEWS`. These include:

- `sendWhatsappMessage(session, phoneNumber, message)` – your logic to send messages.
- `formatRequest(request)` – used by middleware to shape incoming data.
- Any task-specific functions (e.g., `add_to_cart`) that can be dynamically executed.

### Dynamic Method Example

```python
# your_app/dynamic_methods.py

def add_to_cart(session, page, message, *args, **kwargs):
    print(f"Adding product to cart for user {session.user.phoneNumber}")
    return "Item added to cart"
```

Call it dynamically:

```python
from chatbot_session_flow.views import perform_dynamic_action

response = perform_dynamic_action(session, page, "Item name")
```

## Dynamic Message Templating

Use collected data within page content dynamically:

```text
Hello {firstName}, your order has been placed!
```

The values in `{}` are replaced by corresponding session or user data.

## Models

### Profile

Handles user identity:

```python
from chatbot_session_flow.models import Profile

profile = Profile.objects.create(
    firstName="John",
    lastName="Doe",
    phoneNumber="+1234567890",
    email="john@example.com"
)
```

### Session

Tracks the user’s chatbot session:

```python
session = Session.objects.create(user=profile, isValidSession=True)
print(session.is_session_expired())
```

### Page

Each page drives a single step in the conversation:

```python
page = Page.objects.create(title="Welcome", pageType="text", content="Hello {firstName}")
```


## Common Issues & Fixes

### No Migrations Detected

- Ensure your environment is correct.
- Use `pip install -e .` if developing locally.
- Run:
  ```bash
  python manage.py makemigrations chatbot_session_flow
  python manage.py migrate
  ```

### Dynamic Methods Not Found or Not Executing

- Confirm the file path in `DYNAMIC_METHOD_VIEWS` is correct.
- Check that the function name matches the `task` attribute in your `Page`.
- Ensure the function signature accepts dynamic args/kwargs:
  ```python
  def custom_task(session, page, message, *args, **kwargs):
      ...
  ```

## known Issues

- As of yet there are no knows issues but you are encouragedd to test and create github issues for any issues faced in your development.
- Feel free to reachout To me via email ```kamadennis05@gmail.com```

## Conclusion

This package offers a powerful framework for building WhatsApp-based conversational flows with dynamic logic and session handling.
Feel free to contribute or extend the package to fit your business logic!