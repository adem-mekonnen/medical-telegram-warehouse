import os
import json
import logging

logger = logging.getLogger(__name__)

def write_channel_messages_json(base_path, date_str, channel_name, messages):
    """Saves a list of message dicts to a JSON file."""
    directory = os.path.join(base_path, "raw", "telegram_messages", date_str)
    os.makedirs(directory, exist_ok=True)
    
    filepath = os.path.join(directory, f"{channel_name}.json")
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(messages, f, ensure_ascii=False, indent=2)
        logger.info(f"Saved {len(messages)} messages to {filepath}")
    except Exception as e:
        logger.error(f"Failed to save JSON for {channel_name}: {e}")

def write_manifest(base_path, date_str, channel_message_counts):
    """Saves a summary of what was scraped."""
    directory = os.path.join(base_path, "raw", "manifests")
    os.makedirs(directory, exist_ok=True)
    
    filepath = os.path.join(directory, f"manifest_{date_str}.json")
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(channel_message_counts, f, indent=2)
    except Exception as e:
        logger.error(f"Failed to save manifest: {e}")