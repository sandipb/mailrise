"""
Tests for the SMTP server functionality.
"""

import email.policy
from email.message import EmailMessage
from email.parser import BytesParser
from pathlib import Path

import apprise
from aiosmtpd.smtp import Envelope

from mailrise.smtp import _parsemessage


def test_parsemessage() -> None:
    """Tests for email message parsing."""
    msg = EmailMessage()
    msg.set_content('Hello, World!')
    msg['From'] = ''
    msg['Subject'] = 'Test Message'
    notification = _parsemessage(msg, Envelope())
    assert notification.subject == 'Test Message'
    assert notification.body == 'Hello, World!'
    assert notification.body_format == apprise.NotifyFormat.TEXT

    msg = EmailMessage()
    msg.set_content('Hello, World!')
    msg.add_alternative('Hello, <strong>World!</strong>', subtype='html')
    notification = _parsemessage(msg, Envelope())
    assert notification.subject == '[no subject]'
    assert notification.from_ == '[no sender]'
    assert notification.body == 'Hello, <strong>World!</strong>'
    assert notification.body_format == apprise.NotifyFormat.HTML


def test_multipart() -> None:
    """Tests for email message parsing with multipart components."""
    img_name = 'bridge.jpg'
    with open(Path(__file__).parent/img_name, 'rb') as file:
        img_data = file.read()
    msg = EmailMessage()
    msg.add_related('Hello, World!')
    msg.add_related(img_data, maintype='image', subtype='jpeg')
    msg['From'] = ''
    msg['Subject'] = 'Test Message'
    notification = _parsemessage(msg, Envelope())
    assert notification.subject == 'Test Message'
    assert notification.body == 'Hello, World!'
    assert notification.body_format == apprise.NotifyFormat.TEXT

    msg = EmailMessage()
    msg.add_alternative('Hello, World!', subtype='plain')
    msg.add_alternative('<strong>Hello, World!</strong>', subtype='html')
    msg['From'] = ''
    msg['Subject'] = 'Test Message'
    notification = _parsemessage(msg, Envelope())
    assert notification.subject == 'Test Message'
    assert notification.body == '<strong>Hello, World!</strong>'
    assert notification.body_format == apprise.NotifyFormat.HTML


def test_parseattachments() -> None:
    """Tests for email message parsing with attachments."""
    img_name = 'bridge.jpg'
    with open(Path(__file__).parent/img_name, 'rb') as file:
        img_data = file.read()

    msg = EmailMessage()
    msg.set_content('Hello, World!')
    msg['From'] = 'sender@example.com'
    msg['Subject'] = 'Now With Images'
    msg.add_attachment(
        img_data,
        maintype='image',
        subtype='jpeg',
        filename=img_name
    )
    notification = _parsemessage(msg, Envelope())
    assert notification.subject == 'Now With Images'
    assert notification.from_ == 'sender@example.com'
    assert notification.body == 'Hello, World!'
    assert notification.body_format == apprise.NotifyFormat.TEXT
    assert len(notification.attachments) == 1
    assert notification.attachments[0].data == img_data
    assert notification.attachments[0].filename == img_name

    msg = EmailMessage()
    msg.set_content('Hello, World!')
    msg['From'] = 'sender@example.com'
    msg['Subject'] = 'Now With Images'
    msg.add_attachment(
        img_data,
        maintype='image',
        subtype='jpeg',
        filename=f'1_{img_name}'
    )
    msg.add_attachment(
        img_data,
        maintype='image',
        subtype='jpeg',
        filename=f'2_{img_name}'
    )
    notification = _parsemessage(msg, Envelope())
    assert notification.subject == 'Now With Images'
    assert notification.from_ == 'sender@example.com'
    assert notification.body == 'Hello, World!'
    assert notification.body_format == apprise.NotifyFormat.TEXT
    assert len(notification.attachments) == 2
    for attach in notification.attachments:
        assert attach.data == img_data
    assert notification.attachments[0].filename == f'1_{img_name}'
    assert notification.attachments[1].filename == f'2_{img_name}'


def test_parseattachment_text() -> None:
    """Tests that a text attachment is parsed into its original bytes.

    The email library decodes text parts into strings, but an attachment must
    be uploaded as the bytes that the sender transmitted.
    """
    msg = BytesParser(policy=email.policy.default).parsebytes(
        b'From: sender@example.com\r\n'
        b'Subject: Now With Notes\r\n'
        b'Content-Type: multipart/mixed; boundary=notes\r\n'
        b'\r\n'
        b'--notes\r\n'
        b'Content-Type: text/plain\r\n'
        b'\r\n'
        b'Hello, World!\r\n'
        b'--notes\r\n'
        b'Content-Type: text/plain; charset="utf-8"\r\n'
        b'Content-Disposition: attachment; filename="notes.txt"\r\n'
        b'\r\n'
        b'Hello, attached world!\r\n'
        b'--notes--\r\n'
    )
    notification = _parsemessage(msg, Envelope())
    assert notification.body == 'Hello, World!'
    assert notification.attachments[0].filename == 'notes.txt'
    assert notification.attachments[0].data == b'Hello, attached world!'


def test_parseattachment_nested_message() -> None:
    """Tests that a nested message attachment is parsed into bytes.

    A delivery-status notification carries the returned message as a
    `message/rfc822` part, which the email library parses into an
    `EmailMessage` object rather than bytes.
    """
    msg = BytesParser(policy=email.policy.default).parsebytes(
        b'From: MAILER-DAEMON@example.com\r\n'
        b'To: bounce@mailrise.example.com\r\n'
        b'Subject: Undelivered Mail Returned to Sender\r\n'
        b'Content-Type: multipart/report; report-type=delivery-status; '
        b'boundary=bounce\r\n'
        b'\r\n'
        b'--bounce\r\n'
        b'Content-Type: text/plain\r\n'
        b'\r\n'
        b'Delivery failed.\r\n'
        b'--bounce\r\n'
        b'Content-Type: message/delivery-status\r\n'
        b'\r\n'
        b'Final-Recipient: rfc822; nobody@example.com\r\n'
        b'Action: failed\r\n'
        b'\r\n'
        b'--bounce\r\n'
        b'Content-Type: message/rfc822\r\n'
        b'\r\n'
        b'From: sender@example.com\r\n'
        b'Subject: Returned message\r\n'
        b'\r\n'
        b'Original message body\r\n'
        b'--bounce--\r\n'
    )
    notification = _parsemessage(msg, Envelope())

    assert notification.body == 'Delivery failed.'
    assert len(notification.attachments) == 2

    report, returned = notification.attachments
    assert b'Final-Recipient: rfc822; nobody@example.com' in report.data
    assert b'Subject: Returned message' in returned.data
    assert b'Original message body' in returned.data
