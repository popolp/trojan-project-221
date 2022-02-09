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
