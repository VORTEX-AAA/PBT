from datetime import datetime
from zoneinfo import ZoneInfo

chennai = ZoneInfo("Asia/Kolkata")
now = datetime.now(chennai)

print("Chennai, India")
print("Date:", now.strftime("%Y-%m-%d"))
print("Time:", now.strftime("%H:%M:%S"))
print("Day:", now.strftime("%A"))
print("Timezone:", now.tzname())
