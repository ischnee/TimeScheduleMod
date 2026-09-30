# TimeScheduleMod (TSMod)

A version of Ben Marwick's **Time Schedule Viz** bookmarklet ([uw-anthro-web-helpers](https://github.com/benmarwick/uw-anthro-web-helpers)) for the UW Time Schedule. It adds registration snapshots and a TA estimate. Everything else works as in Ben's dashboard, and his README explains how to use it.

**Status: private, in testing.**

## What TSMod adds

- **Snapshots of registration.**
  - **Why:** UW's archive keeps only each quarter's final numbers, which can differ a lot from how the quarter started.
  - **Save snapshot** in the header writes the dashboard, with its numbers as they are now, to one HTML file. It asks for:
    - a note, such as *First day of classes* or *10th day*
    - whether to reload the numbers first, so the time is exact
    - whether to include 10 years of history
  - **Where it saves:** in Chrome, you choose the folder, and Chrome remembers it for next time. Other browsers save to Downloads.
  - **Reopening:** the file works like the dashboard (filters, charts, table, Time Series if history was saved). It never contacts the Time Schedule. A gold **SNAPSHOT** bar shows the note and when the numbers are from.
- **TA estimate.** A **TAs (est.)** card estimates TAs from the quiz sections under the lecture sections counted:
  - **Named TAs:** a name on a quiz section counts as a TA. The exception is the lecture's own instructor, who is often listed on quiz sections until TAs are assigned.
  - **Load:** a TA's load is the number of quiz sections they lead across everything loaded. Each course uses its TAs' most common load.
  - **Sections with students but no TA** (blank, STAFF, TBA, or only the instructor) go first to named TAs below their course's usual load. The rest need new TAs at that load.
  - **Empty sections** (no students) aren't counted: departments usually cancel them, or open and staff them later.
  - **By course** opens every quiz section with the arithmetic course by course. Each section links to its Time Schedule page.
- **TA names are never kept.** As each page loads, TA names become TA1, TA2, and so on. Only these labels are shown and saved.
- **% Full dots** are drawn instead of emoji, so sections over capacity can be dark green.

## Install

1. Download `TimeScheduleMod.html` from this repository.
2. In Chrome, open **Bookmarks → Bookmark Manager**, then the **⋮** menu at the top right of that page, then **Import bookmarks**, and pick the file.
3. A **TimeScheduleMod** bookmark appears. To update later, delete it and import a newer file.

## How to use

1. Sign in to the [UW Time Schedule](https://www.washington.edu/students/timeschd/) and open a quarter, e.g. `/timeschd/AUT2026/`.
2. Click **TimeScheduleMod**. The dashboard opens in a new tab.
3. Type the course prefixes you want (e.g. `PHIL, CLAS`).
4. To keep today's numbers, click **Save snapshot**, add a note, and save.

## Privacy

- **No student data.** TSMod reads only the Time Schedule's section listings: courses, instructors of record, and enrollment counts.
- **TAs appear only as TA1, TA2…,** on screen and in saved files.
- **Keep snapshots inside UW.** Snapshots hold section counts and instructors of record. The Time Schedule is behind a UW sign-in, so keep snapshots in a UW-shared folder.

## Cautions

- **The TA estimate is only an estimate.** It counts TAs who lead a quiz section. It misses graders and lab sections, and appointment percentages aren't on the Time Schedule. Use **By course** to check it against what you know.
- **Snapshot numbers are from when the prefix was loaded,** or reloaded, as the SNAPSHOT bar says.

## For maintainers

- **How it's built.**
  - **`build.py`** takes Ben's file, `ben-original.js`, and adds TSMod's changes. It writes `bookmarklet-timeschedulemod.js`.
  - **Why a build step:** Ben's file is minified, and the dashboard's script sits inside it as an escaped string. So the changes are kept in `build.py` as readable code and inserted at fixed points in his file.
  - **`make-import.js`** writes `TimeScheduleMod.html` from the built file.
- **After any change:**
  ```
  python3 build.py && node make-import.js
  node --experimental-websocket test/run.js
  ```
  The tests need Google Chrome and Node 20 or later. They run the dashboard in headless Chrome against a fake PHIL Time Schedule (`test/fake-time-schedule.js`), in which every name and number is invented.
- **Taking Ben's updates:** replace `ben-original.js` with his latest `bookmarklet-time-schedule-viz-generic.js`, then rebuild and test. `build.py` stops with an error if a place it changes has moved.

## Credit and license

TimeScheduleMod is built on **Time Schedule Viz** by [Ben Marwick](https://faculty.washington.edu/bmarwick/) (UW Anthropology), used under the MIT license. See [LICENSE](LICENSE), which keeps his copyright and permission notice.
