# TimeScheduleMod (TSMod)

A version of Ben Marwick's **Time Schedule Viz** bookmarklet ([uw-anthro-web-helpers](https://github.com/benmarwick/uw-anthro-web-helpers)) for the UW Time Schedule. It adds registration snapshots, a TA estimate, and views of a whole year, a decade and ten summers. Everything else works as in Ben's dashboard, and his README explains how to use it.

**Status: in testing.**

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
- **Views:** buttons in the header switch between **Quarter** (Ben's dashboard for the quarter you opened), **Year**, **Decade**, **AY time series**, **Summers** and **Summer time series**.
  - **Year:** one academic year (Autumn, Winter, Spring). It shows cards for the year, then a column per quarter with its own cards and Enrolled vs Capacity chart. A menu picks the year.
  - **Decade:** the last ten academic years, one per row. Each quarter's cell shows enrolled, seats, % full, sections and TAs, shaded by fullness, with the year's totals in the last column. Click a cell or year to open it in Year.
  - **Summers:** the last ten summers, which are never part of a year. Click one to see its cards and chart.
  - **AY time series:** chosen courses quarter by quarter over ten years, Autumn, Winter and Spring only. The picker lists every course offered in those years, as whole courses, with "last taught" for one not offered lately. To follow one instructor, click **Clear** above the instructor list, then check that instructor.
  - **Summer time series:** the same, for the last ten summers.
  - **Where the numbers come from:** once a prefix is loaded, TSMod reads the other quarters' Time Schedule pages in the background (about a minute for a decade). A progress bar appears only if you open a view before its pages are read. Past quarters show the numbers UW's archive keeps, the quarter's final ones.
  - **TAs for a year** are TA-quarters: each quarter's estimate added up, so a TA working all three quarters counts 3.
- **Filters carry over:** Gen Ed, "Count only" a level, and the instructors unchecked apply in every view. Unchecking single sections changes only the quarter you opened, because sections differ every quarter.
- **Courses excluded everywhere,** for independent study and the like:
  - **Excluding:** uncheck every section of a course in the Quarter view, and that course number (e.g. PHIL 484) is left out of every quarter, view and total, including % full.
  - **The Excluded bar** under the prefixes lists these courses; × brings one back. TSMod remembers them in your browser, and snapshots keep them.
  - **Suggestions:** TSMod suggests courses whose sections all meet "to be arranged" with variable credits, the usual signs of independent study. One click excludes them.

## Install

A [bookmarklet](https://en.wikipedia.org/wiki/Bookmarklet) is a bookmark stored in your web browser that contains JavaScript commands that make the browser do useful work. This one only works on the UW Time Schedule, which requires UW credentials.

1. In Chrome, open **Bookmarks → Bookmark Manager**.
2. Click the **⋮** menu at the very top right of that page (not the one beside your profile icon), then **Add new bookmark**.
3. For the name, use `TimeScheduleMod`.
4. Paste the script below into the URL field, then click **Save**.

#### Script for the bookmarklet:

```
javascript:(function(){
  var s = document.createElement('script');
  s.src = 'https://cdn.jsdelivr.net/gh/ischnee/TimeScheduleMod@main/bookmarklet-timeschedulemod.js?t=' + Date.now();
  s.onload = function() { console.log('[Bookmarklet] Script loaded'); };
  s.onerror = function() { console.error('[Bookmarklet] Failed to load script'); };
  document.body.appendChild(s);
})();
```

This short script loads the latest TimeScheduleMod from this repository each time you click it, so you never need to reinstall it to get updates.

**Prefer a fixed copy that doesn't update itself?**
1. Download `TimeScheduleMod.html` from this repository.
2. Import it in Chrome: Bookmark Manager → **⋮** → **Import bookmarks**.
3. To update later, delete that bookmark and import a newer copy.

## How to use

1. Sign in to the [UW Time Schedule](https://www.washington.edu/students/timeschd/) and open a quarter, e.g. `/timeschd/AUT2026/`.
2. Click **TimeScheduleMod**. The dashboard opens in a new tab.
3. Type the course prefixes you want (e.g. `PHIL, CLAS`). If you clicked TimeScheduleMod on a department's page (e.g. `/timeschd/AUT2026/phil.html`), that prefix is already loaded.
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
  The tests need Google Chrome and Node 20 or later. They run the dashboard in headless Chrome against a fake Time Schedule (`test/fake-time-schedule.js`), in which every name and number is invented: a PHIL department for one quarter's details, and a CLAS department with pages from 2016 to 2026 for Year, Decade and Summers.
- **Every push reaches every user.** Everyone using the loader runs whatever is on `main` the next time they click. Keep write access to people who need it, and protect those GitHub accounts with two-factor authentication.
- **Send updates out right away.** jsDelivr keeps a copy of the file on its servers for up to 12 hours. About a minute after pushing, open `https://purge.jsdelivr.net/gh/ischnee/TimeScheduleMod@main/bookmarklet-timeschedulemod.js` once, and everyone gets the new version on their next click.
  - Wait the minute: purging in the first seconds after a push can put the old version straight back, before GitHub reports the new one.
  - The loader's timestamp (`?t=…`) stops browsers from reusing an old copy.
- **Taking Ben's updates:** replace `ben-original.js` with his latest `bookmarklet-time-schedule-viz-generic.js`, then rebuild and test. `build.py` stops with an error if a place it changes has moved.

## Credit and license

TimeScheduleMod is built on **Time Schedule Viz** by [Ben Marwick](https://faculty.washington.edu/bmarwick/) (UW Anthropology), used under the MIT license. See [LICENSE](LICENSE), which keeps his copyright and permission notice.
