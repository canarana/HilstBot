"""wp-go-archiver archives Wikipedia:Goings-on"""

import datetime
import re
import sys
import pywikibot

WP_GO_TITLE = "Wikipedia:Goings-on"
DATE_REGEX = r"\[\[(\w+ \d{1,2})\]\], \[\[(\d{4})\]\]"
CURRENT_ITEM = r"\*\s?.+?\([ \w]+?\)\n"
ADVERTISEMENT = " ([[Wikipedia:Bots/Requests for approval/HilstBot|Bot]])"

print("Starting wp-go-archiver at " + datetime.datetime.now(datetime.UTC).isoformat())

site = pywikibot.Site("en", "wikipedia")
site.login()

wp_go = pywikibot.Page(site, WP_GO_TITLE)
current_text = wp_go.get()

# Obtain the next date to appear on WP:GO
new_date = datetime.datetime.today()
while new_date.weekday() != 6:
    new_date += datetime.timedelta(1)

# Verify that the archive hasn't been done yet
date_on_page = re.search(DATE_REGEX, current_text).group(1)
if date_on_page == new_date.strftime("%B %-d"):
    print("Archive has already been done! Exiting.")
    sys.exit(0)

# Archive the current page
previous_date = ", ".join(re.search(DATE_REGEX, current_text).groups())
archive_title = WP_GO_TITLE + "/" + previous_date
print(f"Archiving to {archive_title}")
wp_go.save(summary="Stripping hatnote before archival" + ADVERTISEMENT)
wp_go.move(archive_title, reason="Archive" + ADVERTISEMENT, movetalk=False)

# Create a new page with the updated text
new_text = current_text
new_date_text = new_date.strftime("[[%B %-d]], [[%Y]]")
new_text = re.sub(DATE_REGEX, new_date_text, new_text)
new_text = re.sub(CURRENT_ITEM, "", new_text)

wp_go.text = new_text
wp_go.save(summary="New week" + ADVERTISEMENT)
