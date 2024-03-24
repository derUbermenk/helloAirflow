FROM python:3.10-slim

COPY formatter_requirements.txt /tmp/formatter_requirements.txt
COPY scripts/format_emails.py /usr/local/bin/format_emails
RUN python -m pip install -r formatter_requirements.txt

RUN chmod +x /usr/local/bin/format_emails

ENV PATH="/usr/local/bin:${PATH}"