# Time & Energy Audit Tracker

A CLI-style time tracking application inspired by Dan Martell's Time & Energy Audit method.

**Copyright © 2026 Arty McLabin**

## How It Works

1. **Run the script** - Double-click `time_tracker.pyw` (no console window) or `time_tracker.py`
2. **Every 15 minutes** - The window pops to the foreground once and reminds you to log
3. **Enter your activity** - Type in the single-line format shown below
4. **Press Enter** - Saves immediately and shows confirmation with timestamp
5. **Timer resets** - 15 minutes countdown starts from your last submission

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

- ✅ **Single timer** - No timer duplication, clean countdown display
- ✅ **One entry at a time** - Fast, simple Enter-to-save workflow
- ✅ **Instant feedback** - Status label shows timestamp of saved entry
- ✅ **No dialogs** - No popup interruptions, just inline confirmation
- ✅ **Excel in script folder** - All data saved alongside the script
- ✅ **No quit confirmation** - Just close when you want to quit
- ✅ **Pops up once** - Non-intrusive reminder every 15 minutes
- ✅ **Active window** - Runs until you close it manually

## Running the App

**Double-click `time_tracker.pyw`** - runs without showing a console window

Or from command line:
```bash
python time_tracker.py
```

## Output

All entries are saved to `time_audit.xlsx` in the same folder with:
- **Date** (format: `01jan2026`)
- **Time** (format: `14:05`)
- **Energy** level (Green/Red/White)
- **Value** ($-$$$$)
- **Activity** description
- Color-coded rows matching your input

## Notes

- The window stays active until you manually close it
- You can ignore the reminder if you're focused - it won't nag you again
- Multiple entries per reminder are encouraged
- The timer always resets based on your last submission
