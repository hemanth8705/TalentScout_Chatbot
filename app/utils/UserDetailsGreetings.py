def greet_initial() -> str:
    """Return the initial greeting message."""
    return "Hi! I'm GPT. Let's get started. What's your name?"

def greet_user(name: str) -> str:
    """Return a personalized greeting for the user name."""
    return f"Nice to meet you, {name}!"

def acknowledge_email(email: str) -> str:
    """Return a message acknowledging the email."""
    return f"Great, I’ll reach out to you at {email} if needed."

def acknowledge_phone() -> str:
    """Return a message acknowledging the phone number."""
    return "Phone number noted."

def comment_on_experience(years: int) -> str:
    """Return a comment on the years of experience."""
    return f"Awesome! {years} years is solid."

def acknowledge_frameworks(frameworks: list) -> str:
    """Return a message acknowledging provided frameworks."""
    return "Thanks for sharing your frameworks."