from datetime import datetime
from typing import Optional, Any

def parse_date(date_value: Any) -> Optional[datetime]:
    if isinstance(date_value, list) and len(date_value) >= 9:
        try:
            # New format has [year, month, day, hour, minute, second, microsecond, _, _]
            return datetime.strptime(
                f"{date_value[0]} {date_value[1]}",
                "%Y %j",
            )
        except (ValueError, IndexError):
            return None
    return None 