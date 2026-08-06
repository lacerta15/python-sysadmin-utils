"""Send plain-text email alerts over SMTP."""
from __future__ import annotations

import smtplib
from email.message import EmailMessage


def send(host: str, sender: str, recipients, subject: str, body: str,
         port: int = 25, user: str | None = None, password: str | None = None,
         use_tls: bool = False) -> None:
    """Send a simple text email. ``recipients`` may be a str or list."""
    if isinstance(recipients, str):
        recipients = [recipients]
    msg = EmailMessage()
    msg["From"] = sender
    msg["To"] = ", ".join(recipients)
    msg["Subject"] = subject
    msg.set_content(body)

    with smtplib.SMTP(host, port, timeout=15) as smtp:
        if use_tls:
            smtp.starttls()
        if user and password:
            smtp.login(user, password)
        smtp.send_message(msg)
