import re
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo


# Format timestamps to ISO 8601 format
def format_timestamp(timestamp_str, user_timezone='UTC'):
    if not timestamp_str:
        return None
    try:
        local_dt = datetime.strptime(timestamp_str, '%Y-%m-%dT%H:%M')
        local_tz = ZoneInfo(user_timezone)
        local_dt = local_dt.replace(tzinfo=local_tz)
        utc_dt = local_dt.astimezone(ZoneInfo('UTC'))
        # Format with millisecond precision
        return utc_dt.isoformat(timespec='milliseconds')
    except ValueError:
        return None


# Get the current time and the time exactly 7 days ago
# Timestamps must be included with deep search requests
def get_timestamps():
    # Create a search window of 7 days
    current_time = datetime.now(timezone.utc)
    seven_days_ago = current_time - timedelta(days=7)

    # Convert both times to ISO 8601 format with millisecond precision
    # Example: 2021-07-01T00:00:00.000+00:00
    # Eagle Eye Networks API requires timestamps to be in this format
    current_time_iso = current_time.isoformat(timespec='milliseconds')
    seven_days_ago_iso = seven_days_ago.isoformat(timespec='milliseconds')

    return current_time_iso, seven_days_ago_iso


# Convert a camelCase string to a title case string
# This is useful for converting event names into a more readable format
def camel_to_title(camel_str, acronyms=['pos', 'lpr']):
    """
    Convert a camelCase string to a title case string.
    :param camel_str: The camelCase string to convert.
    :param acronyms: A list of acronyms to capitalize in the title.
    :return: The title case string.
    """

    title_str = re.sub(r'([a-z])([A-Z])', r'\1 \2', camel_str).title()
    for acronym in acronyms:
        title_str = re.sub(
            fr'\b({acronym})\b',
            acronym.upper(),
            title_str,
            flags=re.IGNORECASE
        )

    return title_str
