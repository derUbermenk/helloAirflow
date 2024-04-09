FROM python:3.10-slim

COPY sender_requirements.txt /tmp/sender_requirements.txt
COPY scripts/send_emails.py /usr/local/bin/send_emails
RUN python -m pip install -r /tmp/sender_requirements.txt


RUN chmod +x /usr/local/bin/send_emails

ENV PATH="/usr/local/bin:${PATH}"