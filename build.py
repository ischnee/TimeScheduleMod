# Builds TimeScheduleMod (TSMod): Ben Marwick's Time Schedule Viz plus snapshots, a TA estimate and other changes,
# from Ben's minified file.
# The dashboard's own script lives inside a template literal in that file, so every addition below is plain JS/HTML/CSS
# that tmpl() escapes for the template (backslashes, backticks, ${, newlines) before inserting it at a unique anchor.
# Usage: python3 build.py   (reads ben-original.js next to it and writes bookmarklet-timeschedulemod.js)
# ben-original.js is Ben Marwick's bookmarklet-time-schedule-viz-generic.js as of Sept 29, 2026 (his commit d2c3fd6).
# To pick up a newer version of Ben's, replace ben-original.js; the build stops if an anchor it needs has changed.
import os, sys

here = os.path.dirname(os.path.abspath(__file__))
src = sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, 'ben-original.js')
out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(here, 'bookmarklet-timeschedulemod.js')
s = open(src, encoding='utf-8').read()


def tmpl(code):
    return code.replace('\\', '\\\\').replace('`', '\\`').replace('${', '\\${').replace('\n', '\\n')


def insert(anchor, code, where='before', replace=False):
    global s
    a = anchor.replace('\n', '\\n')
    assert s.count(a) == 1, (s.count(a), anchor[:70])
    if replace:
        s = s.replace(a, tmpl(code))
    elif where == 'before':
        s = s.replace(a, tmpl(code) + a)
    else:
        s = s.replace(a, a + tmpl(code))


ICON = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M8 2v8M4.5 6.5 8 10l3.5-3.5M2.5 13.5h11"/></svg>'

CSS = """.snap-tools{margin-left:auto;display:flex;align-items:center;gap:12px}.snap-tools+.ts-toggle-container{margin-left:12px}
.snap-asof{font-size:12px;color:#e8e3d3;white-space:nowrap}
.snap-btn{display:inline-flex;align-items:center;gap:7px;background:#fff;color:#4b2e83;border:0;border-radius:16px;padding:6px 14px;font:600 13px 'Open Sans',Arial,sans-serif;cursor:pointer;box-shadow:0 1px 2px rgba(0,0,0,.2)}
.snap-btn:hover{background:#f0ebfa}.snap-btn:disabled{opacity:.55;cursor:default}.snap-btn svg,.snap-save svg{width:15px;height:15px;flex:none}
.snap-shade{position:fixed;inset:0;background:rgba(30,16,60,.35);z-index:1000;display:flex;justify-content:center;align-items:flex-start;padding-top:90px}
.snap-dlg{width:min(600px,calc(100vw - 40px));background:#fff;border-radius:10px;box-shadow:0 18px 50px rgba(0,0,0,.35);overflow:hidden;color:#222}
.snap-dlg h2{margin:0;background:#4b2e83;color:#fff;font-size:15px;font-weight:600;padding:8px 12px 8px 20px;display:flex;justify-content:space-between;align-items:center}
.snap-x{background:none;border:0;color:#fff;font-size:20px;line-height:1;cursor:pointer;opacity:.75;padding:2px 7px;border-radius:4px}.snap-x:hover{opacity:1;background:rgba(255,255,255,.15)}
.snap-body{padding:16px 22px 4px;font-size:13px}
.snap-row{display:grid;grid-template-columns:92px 1fr;gap:10px;align-items:start;margin-bottom:14px}
.snap-row>b{color:#4b2e83;font-size:12px;text-transform:uppercase;letter-spacing:.5px;padding-top:6px}
.snap-note{width:100%;box-sizing:border-box;border:2px solid #b7a57a;border-radius:6px;padding:8px 10px;font:15px 'Open Sans',Arial,sans-serif}.snap-note:focus{outline:none;border-color:#4b2e83}
.snap-picks{display:flex;flex-wrap:wrap;gap:6px;margin-top:7px}
.snap-picks button{border:1px solid #4b2e83;background:#fff;color:#4b2e83;border-radius:14px;padding:2px 10px;font:600 12px 'Open Sans',Arial,sans-serif;cursor:pointer}.snap-picks button:hover{background:#e8e3d3}.snap-picks button.on{background:#4b2e83;color:#fff}
.snap-val{padding-top:5px;line-height:1.55}.snap-val .dim,.snap-check .dim{color:#777;font-size:12px}
.snap-check{display:block;margin-top:5px;color:#333;cursor:pointer}.snap-check input{margin:0 6px 0 0;vertical-align:-2px}
.snap-file{font-family:Menlo,Consolas,monospace;font-size:12px;background:#f4f6f8;border-radius:5px;padding:6px 9px;margin-top:3px;overflow-wrap:anywhere}
.snap-status{min-height:18px;font-size:12px;font-weight:600;color:#4b2e83;margin:-4px 0 4px}.snap-status.err{color:#b91c1c}
.snap-foot{display:flex;justify-content:flex-end;gap:10px;padding:8px 22px 18px}
.snap-foot button{font:600 13px 'Open Sans',Arial,sans-serif;border-radius:16px;padding:7px 16px;cursor:pointer;display:inline-flex;align-items:center;gap:6px}
.snap-cancel{background:#fff;border:1px solid #bbb;color:#444}.snap-save{background:#4b2e83;border:0;color:#fff}.snap-foot button:disabled,.snap-picks button:disabled{opacity:.6;cursor:default}
.snap-banner{display:flex;align-items:center;gap:14px;flex-wrap:wrap;background:#fbf6e6;border-bottom:1px solid #e6d9b0;padding:9px 25px;font-size:14px;color:#3d2f0e}
.snap-tag{background:#85754d;color:#fff;font-size:11px;font-weight:700;letter-spacing:.08em;border-radius:4px;padding:3px 8px}
.snap-note-text{font-weight:700;font-size:15px;color:#2e1a5c}.snap-meta{color:#6b5a2a}.snap-right{margin-left:auto;font-size:12px;color:#85754d;cursor:help}
.snap-lock{color:#666;font-size:13px}.tsv-snapshot .snap-tools,.tsv-snapshot .chip-remove{display:none}
.snap-nohist{font-size:13px;color:#6b5a2a;background:#fbf6e6;border-radius:5px;padding:6px 10px}
.snap-toast{position:fixed;left:50%;bottom:24px;transform:translateX(-50%);background:#2e1a5c;color:#fff;padding:10px 18px;border-radius:8px;font-size:13px;box-shadow:0 6px 20px rgba(0,0,0,.3);z-index:1001}
.fill-dot{display:inline-block;width:12px;height:12px;border-radius:50%;margin-right:6px;vertical-align:-1px}.fill-dot.low{background:#e0453c}.fill-dot.mid{background:#f59a1b}.fill-dot.full{background:#6fb14f}.fill-dot.over{background:#2d6a2e}
.stat-card .stat-sub{font-size:12px;color:#777;margin-top:6px}.stat-card h3 .nc,.stat-card h3 .est{text-transform:none}.stat-card h3 .est{font-weight:normal;color:#888}#ta-card{cursor:help}
.ta-open{display:none;margin-top:8px;border:1px solid #4b2e83;background:#fff;color:#4b2e83;border-radius:12px;padding:2px 11px;font:600 12px 'Open Sans',Arial,sans-serif;cursor:pointer}.ta-open:hover{background:#e8e3d3}
.ta-shade{padding-top:40px}.ta-dlg{width:min(1180px,calc(100vw - 40px));font-size:13px}.ta-body{padding:12px 20px 12px;max-height:calc(100vh - 150px);overflow:auto}
.ta-loads{color:#555;display:flex;gap:6px 14px;flex-wrap:wrap;margin-bottom:8px}.ta-loads b{color:#4b2e83}
.ta-table{width:100%;border-collapse:collapse}.ta-table th{text-align:left;font-size:12px;color:#4b2e83;border-bottom:2px solid #ddd;padding:5px 8px;vertical-align:bottom;cursor:default}
.ta-table td{border-bottom:1px solid #eee;padding:6px 8px;vertical-align:top}.ta-table .n{text-align:right;width:52px}.ta-table td.c{font-weight:700;white-space:nowrap;width:80px}.ta-table td.m{white-space:nowrap;width:190px}
.ta-table tfoot td{border-bottom:none;border-top:2px solid #ddd;font-weight:600}.ta-table .dim{color:#888;font-weight:normal;font-size:12px}
.qz-lec{display:flex;flex-wrap:wrap;gap:4px;align-items:center;margin:1px 0}.qz-l{width:16px;color:#888;font-size:11px;font-weight:700}
.qz{display:inline-flex;align-items:center;gap:5px;border-radius:11px;padding:1px 8px;font-size:12px;border:1px solid #b9a9e0;background:#fff;color:#2e1a5c;text-decoration:none}.qz:hover{box-shadow:0 0 0 2px rgba(75,46,131,.25)}
.qz b{color:#888;font-weight:600;font-size:11px}.qz em{font-style:normal;color:#888;font-size:11px}.qz i{font-style:normal;color:#4b2e83;font-weight:700}
.qz.need{background:#fdecc8;border-color:#e9b949;color:#7a4b00}.qz.empty{border:1px dashed #bbb;color:#999;background:#fafafa}
.ta-note{margin:8px 0 0;font-size:12px;color:#777}"""

# The page's source, captured before anything changes it; a saved snapshot carries its data in #tsv-snapshot.
START = """
    /* Snapshots: the page's own source, captured before anything changes it, so "Save snapshot" can write a copy of
       this dashboard with its data inside. A saved snapshot carries that data in #tsv-snapshot and never fetches. */
    const PAGE_SOURCE = "<!DOCTYPE html>\\n" + document.documentElement.outerHTML;
    const snapshotEl = document.getElementById("tsv-snapshot");
    const SNAPSHOT = snapshotEl ? JSON.parse(snapshotEl.textContent) : null;"""

FUNCTIONS = r"""    /* ---- TA estimate ----
       From the quiz sections (QZ) of the lecture sections counted above; quiz sections AA, AB... belong to lecture A.
       - Who leads a quiz section is kept only as a label: TA1, TA2... for a "Last,First" name other than that lecture's
         own instructor ("instructor": often listed on quiz sections until TAs are assigned); otherwise STAFF, TBA or "blank"
         (a blank instructor parses as the section's status, "Open"). TA names are replaced as each page loads, so they are
         never shown or saved. The labels are this session's own, numbered in the order TAs appear.
       - A TA's load: how many quiz sections they lead in everything loaded (a TA can lead sections in two courses).
         The usual load is the most common one; each course has its own (its named TAs' most common load).
       - Needs a TA: a quiz section with students but no TA. In each course, named TAs with fewer sections than the
         course's usual load take these first; the rest need new TAs at that load (4 at a load of 2 = 2 more TAs).
       - Empty quiz sections (no students) aren't counted: departments usually cancel them, or open and staff them later.
       TAs who don't lead a section of their own (graders, for example) aren't on the Time Schedule. */
    const taLabels = {};
    let taCount = 0, taFiltered = [];
    function lectureKey(d){ return d.prefix + "|" + d.number + "|" + d.section.charAt(0); }
    function labelQuizLeaders(lectures, quizzes){
        const lectureOf = {};
        lectures.forEach(function(d){ lectureOf[lectureKey(d)] = d; });
        quizzes.forEach(function(q){
            const name = String(q.instructor || "").trim(), lec = lectureOf[lectureKey(q)];
            q.leader = /,/.test(name) ? (lec && lec.instructor === name ? "instructor" : taLabels[name] || (taLabels[name] = "TA" + (++taCount)))
                : /^(STAFF|TBA)$/i.test(name) ? name.toUpperCase() : "blank";
            delete q.instructor;
        });
    }
    function isTa(leader){ return /^TA\d+$/.test(leader); }
    function byTaNumber(a, b){ return a.slice(2) - b.slice(2); }
    /* The most common value; a tie goes to the value nearest `prefer`, then to the larger. */
    function mostCommon(values, prefer){
        const n = {};
        values.forEach(function(v){ n[v] = (n[v] || 0) + 1; });
        return Object.keys(n).map(Number).sort(function(a, b){ return n[b] - n[a] || Math.abs(a - prefer) - Math.abs(b - prefer) || b - a; })[0];
    }
    function taEstimate(filtered){
        const lectureOf = {}, counted = {}, load = {}, coursesOf = {};
        rawData.forEach(function(d){ lectureOf[lectureKey(d)] = d; });
        filtered.forEach(function(d){ counted[lectureKey(d)] = true; });
        quizData.forEach(function(q){ if(isTa(q.leader)){ load[q.leader] = (load[q.leader] || 0) + 1; (coursesOf[q.leader] = coursesOf[q.leader] || {})[q.prefix + " " + q.number] = true; } });
        const loads = Object.keys(load).map(function(k){ return load[k]; });
        const usual = loads.length ? mostCommon(loads, 2) : 2;
        const courses = {}, named = {};
        quizData.filter(function(q){ return counted[lectureKey(q)]; }).forEach(function(q){
            const k = q.prefix + " " + q.number, c = courses[k] || (courses[k] = { count: 0, list: [], tas: {}, needs: 0, empty: 0, openSeats: 0, lectures: {} });
            c.count++;
            c.list.push(q);
            if(isTa(q.leader)){ c.tas[q.leader] = true; named[q.leader] = true; }
            else if(q.enrl > 0) c.needs++;
            else c.empty++;
            const lec = lectureOf[lectureKey(q)];
            if(lec && !c.lectures[lec.section]){ c.lectures[lec.section] = true; c.openSeats += Math.max(0, lec.lim - lec.enrl); }
        });
        const t = { sections: 0, named: Object.keys(named).length, more: 0, needs: 0, taken: 0, empty: 0, usual: usual, load: load, coursesOf: coursesOf, courses: courses };
        Object.keys(courses).forEach(function(k){
            const c = courses[k], tas = Object.keys(c.tas).sort(byTaNumber);
            c.load = tas.length ? mostCommon(tas.map(function(n){ return load[n]; }), usual) : usual;
            c.spareTas = tas.filter(function(n){ return load[n] < c.load; });
            c.taken = Math.min(c.needs, c.spareTas.reduce(function(sum, n){ return sum + c.load - load[n]; }, 0));
            c.more = Math.ceil((c.needs - c.taken) / c.load);
            t.sections += c.count; t.more += c.more; t.needs += c.needs; t.taken += c.taken; t.empty += c.empty;
        });
        return t;
    }
    function plural(n, one, many){ return n + " " + (n === 1 ? one : (many || one + "s")); }
    function renderTaCard(filtered){
        taFiltered = filtered;
        const t = taEstimate(filtered);
        $("#stat-ta").text(t.more ? "≈" + (t.named + t.more) : t.named);
        $("#stat-ta-sub").html(!t.sections ? "no quiz sections" : snapEsc(t.named + " named" + (t.more ? " + ≈" + t.more + " more" : "")) + "<br>"
            + snapEsc((t.needs ? plural(t.needs, "section") + " without a TA" : "every section with students has a TA") + (t.empty ? " · " + t.empty + " empty" : "")));
        $("#ta-open").toggle(t.sections > 0);
        const lines = ["Estimated from the quiz sections of the lecture sections counted."];
        if(t.sections){
            lines.push("", "Named: " + plural(t.named, "TA") + " (a name on a quiz section, other than the course's own instructor).");
            lines.push("Usual load: " + plural(t.usual, "quiz section") + " per TA.");
            if(t.needs) lines.push("Without a TA: " + plural(t.needs, "quiz section") + " with students but no TA (blank, STAFF, TBA, or only the course's instructor). "
                + (t.taken ? (t.taken === 1 ? "1 can go to a named TA who has" : t.taken + " can go to named TAs who have") + " fewer sections than usual; " + (t.needs - t.taken === 1 ? "the other needs" : "the rest need") : "They need")
                + " about " + plural(t.more, "more TA") + ", at each course's usual load.");
            if(t.empty) lines.push("Not counted: " + plural(t.empty, "empty quiz section") + " (no students yet). Departments usually cancel these, or open and staff them if enrollment grows.");
            lines.push("TAs who don't lead a section, such as graders, aren't on the Time Schedule.", "", "By course shows every quiz section and how this adds up.");
        }
        $("#ta-card").attr("title", lines.join("\n"));
    }
    /* A quiz section as a chip: section, who leads it, students. It opens the section on the Time Schedule. */
    function taChip(q, t){
        const ta = isTa(q.leader), course = q.prefix + " " + q.number;
        const also = ta ? Object.keys(t.coursesOf[q.leader]).filter(function(k){ return k !== course; }) : [];
        const tip = (ta ? q.leader + " leads " + plural(t.load[q.leader], "quiz section") + " in all" + (also.length ? ", also in " + also.join(", ") : "")
            : q.enrl > 0 ? "Students but no TA: counted as needing one" : "No students yet: not counted") + ". Click to open this section on the Time Schedule.";
        return "<a class='qz " + (ta ? "ta" : q.enrl > 0 ? "need" : "empty") + "' target='_blank' rel='noopener' title='" + snapEsc(tip) + "' href='https://sdb.admin.uw.edu/timeschd/uwnetid/sln.asp?QTRYR="
            + qtrYrStr + "&SLN=" + snapEsc(q.sln) + "'><b>" + snapEsc(q.section) + "</b>" + snapEsc(q.leader) + (also.length ? "<i>↔</i>" : "") + "<em>" + q.enrl + "</em></a>";
    }
    function openTaBreakdown(){
        $("#ta-dialog").remove();
        const t = taEstimate(taFiltered), byLoad = {}, inCourses = {};
        Object.keys(t.load).forEach(function(n){ (byLoad[t.load[n]] = byLoad[t.load[n]] || []).push(n); });
        const loads = Object.keys(byLoad).map(Number).sort(function(a, b){ return byLoad[b].length - byLoad[a].length || a - b; })
            .map(function(l){ return "<span><b>" + l + " each:</b> " + byLoad[l].sort(byTaNumber).join(" ") + "</span>"; }).join("");
        const rows = Object.keys(t.courses).sort().map(function(k){
            const c = t.courses[k], tas = Object.keys(c.tas), lecs = {}, rest = c.needs - c.taken;
            tas.forEach(function(n){ inCourses[n] = (inCourses[n] || 0) + 1; });
            c.list.forEach(function(q){ (lecs[q.section.charAt(0)] = lecs[q.section.charAt(0)] || []).push(q); });
            const chips = Object.keys(lecs).sort().map(function(l){
                return "<div class='qz-lec'><span class='qz-l'>" + snapEsc(l) + "</span>" + lecs[l].sort(function(a, b){ return a.section.localeCompare(b.section); }).map(function(q){ return taChip(q, t); }).join("") + "</div>";
            }).join("");
            const math = !c.needs ? "<span class='dim'>0</span>" : (c.taken ? c.taken + " to " + c.spareTas.join(", ") + "; " : "") + (rest ? rest + " ÷ " + c.load + " = <b>+" + c.more + "</b>" : "<b>+0</b>");
            return "<tr><td class='c'>" + snapEsc(k) + "</td><td>" + chips + "</td><td class='n'>" + tas.length + "</td><td class='n'>" + c.load + "</td><td class='n'>" + c.needs
                + (c.empty ? "<div class='dim'" + (c.openSeats ? " title='The lecture has " + plural(c.openSeats, "open seat") + ", so these may still open'" : "") + ">" + c.empty + " empty</div>" : "") + "</td><td class='m'>" + math + "</td></tr>";
        }).join("");
        const shared = Object.keys(inCourses).filter(function(n){ return inCourses[n] > 1; }).sort(byTaNumber);
        const dlg = $("<div id='ta-dialog' class='snap-shade ta-shade'></div>").html("<div class='snap-dlg ta-dlg' role='dialog' aria-modal='true' aria-labelledby='ta-title'>"
            + "<h2><span id='ta-title'>TAs by course</span><button type='button' class='snap-x' aria-label='Close'>×</button></h2><div class='ta-body'>"
            + "<div class='ta-loads'><span>Usual load <b>" + t.usual + "</b> quiz sections per TA" + (loads ? " ·" : "") + "</span>" + loads + "</div>"
            + "<table class='ta-table'><thead><tr><th>Course</th><th>Quiz sections <span class='dim'>(section · who leads · students)</span></th><th class='n'>TAs<br>named</th><th class='n'>Usual<br>load</th><th class='n'>Need<br>a TA</th><th>More TAs</th></tr></thead>"
            + "<tbody>" + rows + "</tbody><tfoot><tr><td class='c'>Total</td><td class='dim'>" + (shared.length ? snapEsc(shared.join(", ") + (shared.length === 1 ? " leads" : " lead") + " sections in more than one course, counted once") : "") + "</td>"
            + "<td class='n'>" + t.named + "</td><td></td><td class='n'>" + t.needs + (t.empty ? "<div class='dim'>" + t.empty + " empty</div>" : "") + "</td><td class='m'><b>+" + t.more + "</b> → " + (t.more ? "≈" : "") + plural(t.named + t.more, "TA") + "</td></tr></tfoot></table>"
            + "<p class='ta-note'>TA names are replaced with TA1, TA2… as each page loads, and snapshots keep only these labels. Each section opens on the Time Schedule.</p></div></div>").appendTo("body");
        const close = function(){ dlg.remove(); $(document).off("keydown.ta"); };
        dlg.on("click", function(e){ if(e.target === this) close(); });
        dlg.find(".snap-x").on("click", close).focus();
        $(document).on("keydown.ta", function(e){ if(e.key === "Escape") close(); });
    }

    /* ---- Snapshots ---- */
    const DOWNLOAD_ICON = '""" + ICON + r"""';
    const QTR_NAME = { WIN: "Winter", SPR: "Spring", SUM: "Summer", AUT: "Autumn" };
    function quarterName(id){ return (QTR_NAME[id.slice(0, 3)] || id.slice(0, 3)) + " " + id.slice(3); }
    function snapEsc(v){ return String(v).replace(/[&<>"']/g, function(c){ return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }
    function fmtWhen(iso, withDate){
        const d = new Date(iso), time = d.toLocaleTimeString("en-US", { hour: "numeric", minute: "2-digit" });
        return withDate ? d.toLocaleDateString("en-US", { weekday: "short", month: "short", day: "numeric", year: "numeric" }) + ", " + time : time;
    }
    function sameDay(a, b){ return new Date(a).toDateString() === new Date(b).toDateString(); }
    /* The data's time: when the earliest of the prefixes shown was loaded from the Time Schedule. */
    function dataAsOf(){
        const times = activePrefixes.map(function(p){ return fetchedAt[p]; }).filter(Boolean).sort();
        return times.length ? times[0] : null;
    }
    function updateAsOf(){
        if(SNAPSHOT) return;
        const t = dataAsOf();
        $("#snap-asof").text(t ? "Data as of " + fmtWhen(t, !sameDay(t, new Date())) : "")
            .attr("title", t ? "When these numbers were loaded from the Time Schedule" + (activePrefixes.length > 1 ? " (the earliest of your prefixes)" : "") : "");
        $("#snap-save").prop("disabled", activePrefixes.length === 0)
            .attr("title", activePrefixes.length ? "Save this dashboard, with its numbers as of now, as a file you can reopen any time" : "Load a prefix first");
    }
    /* Loads a prefix's page again, replacing its rows only if the new page has sections (a signed-out page has none). */
    async function refetchPrefix(p){
        const res = await fetch(baseUrl + prefixLookup[p]);
        if(!res.ok) throw new Error("Couldn't reload " + p + " (the Time Schedule answered " + res.status + ").");
        const added = parseUWTimeSchedule(await res.text(), true);
        if(!added.length && rawData.some(function(d){ return d.src === p; })) throw new Error("The Time Schedule sent no sections for " + p + ". You may need to sign in again.");
        added.forEach(function(d){ d.src = p; });
        added.quiz.forEach(function(d){ d.src = p; });
        labelQuizLeaders(added, added.quiz);
        rawData = rawData.filter(function(d){ return d.src !== p; }).concat(added);
        quizData = quizData.filter(function(d){ return d.src !== p; }).concat(added.quiz);
        fetchedAt[p] = new Date().toISOString();
        tsDataCache[currQuarterId + "_" + p] = rawData.filter(function(d){ return d.prefix === p; });
    }
    function historyTasks(prefixes){
        const tasks = [];
        prefixes.forEach(function(p){ histQuarters.forEach(function(hq){ const key = hq.str + "_" + p; if(hq.str !== currQuarterId && !tsDataCache[key]) tasks.push({ hq: hq, p: p, key: key }); }); });
        return tasks;
    }
    /* The same pages Time Series fetches; quarters already fetched there aren't fetched again. */
    async function fetchHistory(prefixes, progress){
        const tasks = historyTasks(prefixes);
        for(let i = 0; i < tasks.length; i++){
            const t = tasks[i];
            progress("Fetching history: " + t.hq.str + " " + t.p + " (" + (i + 1) + " of " + tasks.length + ")");
            try {
                const res = await fetch("https://www.washington.edu/students/timeschd/" + t.hq.str + "/" + prefixLookup[t.p]);
                tsDataCache[t.key] = res.ok ? parseUWTimeSchedule(await res.text()) : [];
            } catch(e){ tsDataCache[t.key] = []; }
        }
    }
    function snapshotFileName(note, iso){
        const d = new Date(iso || Date.now()), pad = function(n){ return String(n).padStart(2, "0"); };
        const stamp = d.getFullYear() + "-" + pad(d.getMonth() + 1) + "-" + pad(d.getDate()) + " " + pad(d.getHours()) + pad(d.getMinutes());
        const ps = activePrefixes.length > 4 ? activePrefixes.slice(0, 3).join(" ") + " +" + (activePrefixes.length - 3) : activePrefixes.join(" ");
        return ("Time Schedule " + currQuarterId + " " + ps + " " + stamp + (note ? " " + note : "")).replace(/[\\/:*?"<>|]+/g, "-").replace(/\s+/g, " ").trim().slice(0, 150) + ".html";
    }
    /* Everything the dashboard needs to reopen as it is now: the rows, the filters and selections, and (if asked) history. */
    function snapshotData(note, withHistory){
        const shown = function(d){ return activePrefixes.indexOf(d.src) !== -1; };
        let history = null;
        if(withHistory){
            history = {};
            Object.keys(tsDataCache).forEach(function(k){ const p = k.slice(k.indexOf("_") + 1); if(activePrefixes.indexOf(p) !== -1 && k.indexOf(currQuarterId + "_") !== 0) history[k] = tsDataCache[k]; });
        }
        const times = {};
        activePrefixes.forEach(function(p){ times[p] = fetchedAt[p]; });
        return { version: 1, note: note, quarter: currQuarterId, dataAsOf: dataAsOf(), savedAt: new Date().toISOString(), prefixes: activePrefixes.slice(), fetchedAt: times,
            rawData: rawData.filter(shown), quizData: quizData.filter(shown), history: history,
            ui: { genEds: $(".gened-filter:checked").map(function(){ return this.value; }).get(), excludedSections: excludedSections.slice(), excludedInstructors: excludedInstructors.slice(),
                table: dataTable ? { order: dataTable.order(), search: dataTable.search(), length: dataTable.page.len() } : null,
                timeSeries: $("#ts-toggle").is(":checked"), tsSelected: $("#ts-course-select").val() || [], tsExcludedInstructors: tsExcludedInstructors.slice() } };
    }
    /* The snapshot file: this page's own source with the data in #tsv-snapshot, and its suggested file name. */
    function snapshotFile(note, withHistory){
        const snap = snapshotData(note, withHistory);
        const tag = "<script id=\"tsv-snapshot\" type=\"application/json\">" + JSON.stringify(snap).replace(/</g, "\\u003c") + "<\/script>";
        return { blob: new Blob([PAGE_SOURCE.replace("<body>", function(){ return "<body>" + tag; })], { type: "text/html" }), name: snapshotFileName(note, snap.dataAsOf) };
    }
    /* Browsers without a Save As dialog for pages (Safari, Firefox) get an ordinary download. */
    function downloadFile(file){
        const url = URL.createObjectURL(file.blob), a = document.createElement("a");
        a.href = url; a.download = file.name; document.body.appendChild(a); a.click(); a.remove();
        setTimeout(function(){ URL.revokeObjectURL(url); }, 60000);
    }
    function snapToast(text){
        const t = $("<div class='snap-toast' role='status'></div>").text(text).appendTo("body");
        setTimeout(function(){ t.fadeOut(400, function(){ t.remove(); }); }, 6000);
    }
    function openSaveDialog(){
        if(!activePrefixes.length) return;
        $("#snap-dialog").remove();
        const picks = ["First day of classes", "10th day", "Last day to add", "End of quarter"];
        const dlg = $("<div id='snap-dialog' class='snap-shade'></div>").html(
            "<div class='snap-dlg' role='dialog' aria-modal='true' aria-labelledby='snap-title'><h2><span id='snap-title'>Save a snapshot</span><button type='button' class='snap-x' aria-label='Close'>×</button></h2><div class='snap-body'>"
            + "<div class='snap-row'><b>Note</b><div><input class='snap-note' id='snap-note' maxlength='80' placeholder='e.g. First day of classes' aria-label='Note'><div class='snap-picks'>"
            + picks.map(function(p){ return "<button type='button'>" + p + "</button>"; }).join("") + "</div></div></div>"
            + "<div class='snap-row'><b>Data as of</b><div class='snap-val'><span id='snap-when'></span><label class='snap-check'><input type='checkbox' id='snap-reload' checked>Reload from the Time Schedule first, so the time is exact</label></div></div>"
            + "<div class='snap-row'><b>Includes</b><div class='snap-val'><span id='snap-includes'></span><label class='snap-check'><input type='checkbox' id='snap-history'>Also save 10 years of history, so Time Series works in the file <span class='dim' id='snap-hist-cost'></span></label></div></div>"
            + "<div class='snap-row'><b>File</b><div class='snap-file' id='snap-file'></div></div>"
            + "<div class='snap-status' id='snap-status' role='status'></div>"
            + "</div><div class='snap-foot'><button type='button' class='snap-cancel'>Cancel</button><button type='button' class='snap-save'>" + DOWNLOAD_ICON + (window.showSaveFilePicker ? "Save file…" : "Save file") + "</button></div></div>").appendTo("body");
        const asOf = dataAsOf(), n = rawData.filter(function(d){ return activePrefixes.indexOf(d.src) !== -1; }).length, missing = historyTasks(activePrefixes).length;
        $("#snap-when").html(snapEsc(fmtWhen(asOf, true)) + " <span class='dim'>(" + (activePrefixes.length === 1 ? "when " + snapEsc(activePrefixes[0]) + " was loaded" : "the earliest of your " + activePrefixes.length + " prefixes") + ")</span>");
        $("#snap-includes").text(activePrefixes.join(", ") + " · " + n + " sections, with your current filters and selections");
        $("#snap-hist-cost").text(missing ? "(fetches " + missing + " past quarter" + (missing === 1 ? "" : "s") + ")" : "(already loaded)");
        let saving = false;
        const refresh = function(){ $("#snap-file").text(snapshotFileName($("#snap-note").val().trim(), $("#snap-reload").is(":checked") ? null : asOf)); };
        const close = function(){ if(!saving){ dlg.remove(); $(document).off("keydown.snap"); } };
        dlg.on("click", function(e){ if(e.target === this) close(); });
        dlg.find(".snap-x, .snap-cancel").on("click", close);
        $(document).on("keydown.snap", function(e){ if(e.key === "Escape") close(); });
        dlg.find(".snap-picks button").on("click", function(){ $("#snap-note").val($(this).text()); dlg.find(".snap-picks button").removeClass("on"); $(this).addClass("on"); refresh(); });
        $("#snap-note").on("input", function(){ const v = this.value; dlg.find(".snap-picks button").each(function(){ $(this).toggleClass("on", $(this).text() === v); }); refresh(); })
            .on("keydown", function(e){
                /* Tab in an empty note takes the placeholder's suggestion ("First day of classes"); after that, Tab moves on. */
                if(e.key === "Tab" && !e.shiftKey && !this.value.trim()){ e.preventDefault(); this.value = this.placeholder.replace(/^e\.g\.\s*/i, ""); $(this).trigger("input"); }
                else if(e.key === "Enter") dlg.find(".snap-save").click();
            });
        $("#snap-reload").on("change", refresh);
        /* Chrome's Save As dialog comes first, while the click still counts as the person's (Chrome requires that); it opens
           in the folder last used for snapshots. Reloading and fetching history happen after a place is chosen. */
        dlg.find(".snap-save").on("click", async function(){
            const note = $("#snap-note").val().trim(), status = function(t, err){ $("#snap-status").text(t).toggleClass("err", !!err); };
            const reload = $("#snap-reload").is(":checked"), withHistory = $("#snap-history").is(":checked");
            let handle = null;
            if(window.showSaveFilePicker){
                try {
                    handle = await window.showSaveFilePicker({ id: "tsv-snapshots", startIn: "documents", suggestedName: snapshotFileName(note, reload ? null : dataAsOf()),
                        types: [{ description: "Web page", accept: { "text/html": [".html"] } }] });
                } catch(e){
                    if(e.name === "AbortError") return;   /* Save As was cancelled: back to this dialog */
                    handle = null;                        /* no Save As here after all: download instead */
                }
            }
            saving = true;
            dlg.find("button, input").prop("disabled", true);
            try {
                if(reload){
                    for(const p of activePrefixes){ status("Reloading " + p + " from the Time Schedule…"); await refetchPrefix(p); }
                    renderChips();
                    renderDashboard();
                }
                if(withHistory) await fetchHistory(activePrefixes.slice(), status);
                status("Saving…");
                const file = snapshotFile(note, withHistory);
                if(handle){
                    const out = await handle.createWritable();
                    await out.write(file.blob);
                    await out.close();
                } else downloadFile(file);
                saving = false;
                close();
                snapToast(handle ? "Snapshot saved as “" + handle.name + "”" : "Snapshot saved to your Downloads folder: " + file.name);
            } catch(e){
                saving = false;
                /* Save As may already have made an empty file; remove it so a failed save leaves nothing behind. */
                if(handle && handle.remove) try { await handle.remove(); } catch(err){}
                status(e.message + " Nothing was saved.", true);
                dlg.find("button, input").prop("disabled", false);
            }
        });
        refresh();
        $("#snap-note").focus();
    }
    /* Opening a saved snapshot: its data and settings replace the empty start, and prefixes can't be added. */
    function applySnapshot(){
        const s = SNAPSHOT, ui = s.ui || {};
        rawData = s.rawData || [];
        quizData = s.quizData || [];
        activePrefixes = s.prefixes.slice();
        loadedPrefixes = s.prefixes.slice();
        Object.assign(fetchedAt, s.fetchedAt || {});
        excludedSections = ui.excludedSections || [];
        excludedInstructors = ui.excludedInstructors || [];
        tsExcludedInstructors = ui.tsExcludedInstructors || [];
        if(ui.genEds) $(".gened-filter").each(function(){ this.checked = ui.genEds.indexOf(this.value) !== -1; });
        activePrefixes.forEach(function(p){
            tsDataCache[currQuarterId + "_" + p] = rawData.filter(function(d){ return d.prefix === p; });
            histQuarters.forEach(function(hq){ const key = hq.str + "_" + p; if(hq.str !== currQuarterId) tsDataCache[key] = s.history ? (s.history[key] || []) : []; });
        });
        document.body.classList.add("tsv-snapshot");
        document.title = "Snapshot " + s.quarter + " " + s.prefixes.join(" ") + (s.note ? " · " + s.note : "");
        $(".dashboard-header p").text(s.quarter + " | Excludes 500+ level, 99s, and Honors.");
        $("#prefix-input").hide();
        $("#prefix-hint").removeClass("warning").html("<span class='snap-lock'>🔒 " + snapEsc(s.prefixes.join(", ")) + ", as saved</span>");
        $(".dashboard-header").after("<div class='snap-banner'><span class='snap-tag'>SNAPSHOT</span>" + (s.note ? "<span class='snap-note-text'>" + snapEsc(s.note) + "</span>" : "")
            + "<span class='snap-meta'>" + quarterName(s.quarter) + (s.dataAsOf ? " · data as of " + snapEsc(fmtWhen(s.dataAsOf, true)) : "") + "</span>"
            + "<span class='snap-right' title='This file keeps the numbers from when it was saved. Open the Time Schedule for today’s numbers.'>Saved " + snapEsc(fmtWhen(s.savedAt, !s.dataAsOf || !sameDay(s.savedAt, s.dataAsOf))) + " · numbers don’t update</span></div>");
        if(!s.history) $(".ts-controls").prepend("<div class='snap-nohist'>This snapshot didn’t save the 10-year history, so Time Series shows " + snapEsc(quarterName(s.quarter)) + " only.</div>");
    }
    /* After the table exists: its sort, search and page length, then the Time Series view if it was open. */
    function applySnapshotAfter(){
        const ui = SNAPSHOT.ui || {};
        if(dataTable && ui.table) dataTable.order(ui.table.order || []).search(ui.table.search || "").page.len(ui.table.length || 25).draw();
        if(ui.timeSeries){
            $("#ts-toggle").prop("checked", true).trigger("change");
            if(ui.tsSelected && ui.tsSelected.length) $("#ts-course-select").val(ui.tsSelected).trigger("change");
        }
    }
"""

insert('(async function(){\n', START, where='after')
# Parser: quiz sections were skipped; keep them apart (for the TA estimate) instead.
insert('function parseUWTimeSchedule(html){', 'function parseUWTimeSchedule(html, withQuiz){', replace=True)
insert('const results = [];', 'const results = []; results.quiz = [];', replace=True)
insert('if(line.includes("QZ")) continue;', 'const isQuiz = line.includes("QZ");\n                if(isQuiz && !withQuiz) continue;', replace=True)
insert('const added = parseUWTimeSchedule(await res.text());', 'const added = parseUWTimeSchedule(await res.text(), true);', replace=True)
insert('results.push({', 'if(isQuiz){ results.quiz.push({ sln: sln, prefix: currentCourse.prefix, number: currentCourse.number, section: section, instructor: instructor, enrl: enrl, lim: lim }); continue; }\n                ')
insert('let rawData = [];', '\n    let quizData = [];\n    const fetchedAt = {};', where='after')
insert('rawData = rawData.concat(added);', 'added.forEach(function(d){ d.src = p; });\n                added.quiz.forEach(function(d){ d.src = p; });\n                labelQuizLeaders(added, added.quiz);\n                quizData = quizData.concat(added.quiz);\n                fetchedAt[p] = new Date().toISOString();\n                ')
# Header: data time and the Save snapshot button, left of the Current / Time Series switch.
insert('<div class="ts-toggle-container">', '<div class="snap-tools"><span id="snap-asof" class="snap-asof"></span><button type="button" id="snap-save" class="snap-btn" disabled title="Load a prefix first">' + ICON + 'Save snapshot</button></div>')
# A fifth card: TAs, estimated.
insert('<div class="stat-card"><h3>Fullness</h3><div class="value" id="stat-pct">0%</div></div>', '<div class="stat-card" id="ta-card"><h3><span class="nc">TAs</span> <span class="est">(est.)</span></h3><div class="value" id="stat-ta">0</div><div class="stat-sub" id="stat-ta-sub"></div><button type="button" id="ta-open" class="ta-open" title="Every quiz section, and how the estimate adds up">By course</button></div>', where='after')
insert('$("#stat-pct").text(totalLim > 0 ? ((totalEnrl / totalLim) * 100).toFixed(1) + "%" : "0%");', '\n        renderTaCard(filteredData);\n        updateAsOf();', where='after')
insert('</style>', CSS.replace('\n', ''))
insert('<h1>UW Time Schedule Analytics</h1>', '<h1>TimeScheduleMod</h1>', replace=True)
insert('UW Time Schedule Dashboard</title>', 'TimeScheduleMod</title>', replace=True)
# % Full: drawn dots instead of emoji, so over-capacity sections can be a darker green (there is no dark green circle emoji).
insert('''let emoji = (data >= 75 && data <= 100) ? "🟢" : (data > 100 || (data >= 50 && data < 75)) ? "🟠" : "🔴";
                            return emoji + " " + data.toFixed(1) + "%";''', '''const band = data > 100 ? ["over", "Over capacity"] : data >= 75 ? ["full", "75–100% full"] : data >= 50 ? ["mid", "50–75% full"] : ["low", "Under 50% full"];
                            return (type === "display" ? "<span class='fill-dot " + band[0] + "' title='" + band[1] + "'></span>" : "") + data.toFixed(1) + "%";''', replace=True)
insert('let isFetchingTS = false;', FUNCTIONS + '    ')
insert('renderDashboard();\n    renderChips();\n', 'if(SNAPSHOT) applySnapshot();\n    ')
insert('window.addEventListener("resize"', '$("#snap-save").on("click", openSaveDialog);\n    $("#ta-open").on("click", openTaBreakdown);\n    if(SNAPSHOT) applySnapshotAfter();\n    ')

open(out, 'w', encoding='utf-8').write(s)
print('wrote', out, len(s), 'chars')
