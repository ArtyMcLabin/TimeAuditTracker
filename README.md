# Time & Energy Audit Tracker

A CLI-style time tracking application inspired by Dan Martell's Time & Energy Audit method.

**Copyright © 2026 Arty McLabin**

## How It Works

1. **Run the script** - Double-click `time_tracker.pyw` (no console window) or `time_tracker.py`
2. **Every 15 minutes** - The window pops to the foreground and reminds you to log
3. **Enter your activities** - One per line in the format shown below
4. **Submit** - Click "Submit Entries" or press Ctrl+Enter
5. **Timer resets** - 15 minutes start from your last submission

## Entry Format

```
green $$ activity description
red $$$ another activity
white $ low value task
```

**Color codes:**
- `green` = Energizing tasks (things you enjoy)
- `red` = Draining tasks (things that drain your energy)
- `white` = Neutral tasks

**Dollar signs ($):**
- `$` = ~$10/hour tasks (low value)
- `$$` = ~$50/hour tasks
- `$$$` = ~$250/hour tasks
- `$$$$` = $500+/hour tasks (high value strategic work)

## Examples

```
green $$$$ strategic planning for Q1
red $ responding to emails
white $$ team meeting
green $$$ coding new feature
```

## Features

- ✅ Pops up every 15 minutes (non-intrusive - only once)
- ✅ Enter multiple activities at once
- ✅ Timer resets from last submission
- ✅ Saves to Excel with color coding
- ✅ Tracks date/time of each entry
- ✅ Active window (runs until you close it)
- ✅ No nagging - patiently waits for your input

## Running the App

**Double-click `time_tracker.pyw`** - runs without showing a console window

Or from command line:
```bash
python time_tracker.py
```

## Output

All entries are saved to `time_audit.xlsx` in the same folder with:
- Date & Time
- Energy level (Green/Red/White)
- Value ($-$$$$)
- Activity description
- Color-coded rows matching your input

## Notes

- The window stays active until you manually close it
- You can ignore the reminder if you're focused - it won't nag you again
- Multiple entries per reminder are encouraged
- The timer always resets based on your last submission
