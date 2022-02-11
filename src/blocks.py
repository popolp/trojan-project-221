"""
This file contains templates for messages is Slack.
Currently uses only the plain text template.
"""

def plain_text(metadata):
    return [
        {
            "type": "section",
            "text": {
                "type": "plain_text",
                "text": metadata,
            },
        }
    ]
