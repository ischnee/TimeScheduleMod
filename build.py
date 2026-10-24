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


def insert(anchor, code, where='before', replace=False, raw=False):
    """raw: code goes in as written, for the bookmarklet's own code outside the template, or for template text that must
    keep a ${...} placeholder."""
    global s
    a = anchor.replace('\n', '\\n')
    assert s.count(a) == 1, (s.count(a), anchor[:70])
    c = code if raw else tmpl(code)
    if replace:
        s = s.replace(a, c)
    elif where == 'before':
        s = s.replace(a, c + a)
    else:
        s = s.replace(a, a + c)


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
.stat-card .stat-sub{font-size:12px;color:#777;margin-top:6px}.stat-card h3 .nc,.stat-card h3 .est{text-transform:none}.stat-card h3 .est{font-weight:normal;color:#888}#ta-card{cursor:help}#denied-card{cursor:help}.sq-chips{display:flex;flex-wrap:wrap;align-items:center;gap:6px;margin-bottom:10px}.sq-chip{border:1px solid #c9bfe3;background:#fff;color:#4b2e83;border-radius:14px;padding:4px 12px;font:600 13px 'Open Sans',Arial,sans-serif;cursor:pointer}.sq-chip:hover{border-color:#4b2e83}.sq-chip.on{background:#4b2e83;color:#fff;border-color:#4b2e83}.sq-chip.found{border-style:dashed}.sq-add{border-style:dashed;border-color:#d9c48a;color:#85754d}.sq-del{border:0;background:none;color:#999;font-size:16px;line-height:1;cursor:pointer;margin-left:-6px;padding:0 4px}.sq-del:hover{color:#b42318}.sq-form{display:flex;flex-wrap:wrap;align-items:center;gap:8px;margin:0 0 12px;font-size:13px}.sq-form[hidden]{display:none}.sq-form input{padding:5px 9px;font:inherit;border:1px solid #ccc;border-radius:5px}.sq-err{color:#b42318}.sq-strip{display:flex;align-items:stretch;gap:6px;overflow-x:auto;padding:2px 2px 8px;margin-bottom:12px}.sq-tile{flex:1 1 0;min-width:138px;background:#fff;border-radius:8px;box-shadow:0 1px 3px rgba(0,0,0,.06);border-top:4px solid #4b2e83;padding:10px 12px;font-size:12px;color:#555}.sq-tile.sq-total{border-top-color:#b7a57a;background:#fdfbf4}.sq-c{font-weight:700;color:#2e1a5c;font-size:14px}.sq-t{color:#777;min-height:2.7em;line-height:1.35}.sq-n b{font-size:22px;color:#2e1a5c}.sq-n.sq-none{color:#999;font-size:12px}.sq-d{font-weight:700;margin-top:2px}.sq-d.up{color:#1a7f37}.sq-d.down{color:#b42318}.sq-s{margin-top:2px}.sq-s span{color:#999}.sq-spark{display:block;margin:5px 0 1px}.sq-arrow{align-self:center;color:#8f7bc4;font-size:20px;font-weight:700}.sq-gap{flex:0 0 8px}.sq-table thead th{vertical-align:bottom}.sq-table thead th span{display:block;font-size:10px;text-transform:none;letter-spacing:0;color:#888;font-weight:normal;white-space:normal;max-width:150px}.sq-cell{cursor:default;height:auto;padding:8px 11px;line-height:1.35}.sq-cell .pc-big b{font-size:18px}.sq-q{font-size:11px;color:#666;white-space:nowrap}.sq-as{font-style:italic;color:#85754d;font-size:11px}.dn-get{margin-top:8px;border:1px solid #4b2e83;background:#fff;color:#4b2e83;border-radius:12px;padding:2px 11px;font:600 12px 'Open Sans',Arial,sans-serif;cursor:pointer}.pv-dn{color:#8a3a12}
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
CSS += """
.dashboard-header{row-gap:8px}.view-seg{margin-left:auto;display:inline-flex;background:rgba(255,255,255,.12);border-radius:18px;padding:3px;gap:2px}
.view-seg button{border:0;background:none;color:#e8e3d3;font:600 13px 'Open Sans',Arial,sans-serif;padding:5px 13px;border-radius:15px;cursor:pointer;white-space:nowrap}.view-seg button:hover{color:#fff;background:rgba(255,255,255,.12)}
.view-seg button.on{background:#fff;color:#4b2e83}.view-seg .caret{margin-left:6px;font-size:11px}
.pv-yearmenu{position:fixed;z-index:50;background:#fff;border-radius:8px;box-shadow:0 10px 30px rgba(0,0,0,.25);padding:6px;display:flex;flex-direction:column;min-width:120px}
.pv-yearmenu button{border:0;background:none;text-align:left;font:600 13px 'Open Sans',Arial,sans-serif;color:#2e1a5c;padding:6px 12px;border-radius:5px;cursor:pointer}.pv-yearmenu button:hover,.pv-yearmenu button:focus{background:#f0ebfa;outline:none}.pv-yearmenu button.on{background:#4b2e83;color:#fff}.snap-tools{flex-basis:100%;justify-content:flex-end;margin-left:0}.snap-btn .snap-asof{color:#85754d;font-weight:normal;font-size:12px}
.excl-bar{flex-wrap:wrap;align-items:center;gap:6px 10px;margin:8px 25px 0;padding:8px 14px;background:#fff;border-radius:6px;box-shadow:0 1px 3px rgba(0,0,0,.05);font-size:13px}.excl-bar[style*=block]{display:flex !important}
.excl-bar strong{color:#4b2e83;font-size:12px;text-transform:uppercase;letter-spacing:.5px;cursor:help}
.excl-chip{display:inline-flex;align-items:center;gap:4px;border:1px solid #b9a9e0;border-radius:12px;padding:1px 4px 1px 10px;color:#2e1a5c;font-weight:600}
.excl-chip button{border:0;background:none;color:#888;font-size:15px;line-height:1;cursor:pointer;padding:0 4px;border-radius:8px}.excl-chip button:hover{color:#b91c1c;background:#f4f0fb}
.excl-sugg{color:#6b5a2a;background:#fbf6e6;border-radius:12px;padding:3px 6px 3px 12px;cursor:help}.excl-sugg b{color:#3d2f0e}
.excl-sugg button{margin-left:8px;border:1px solid #85754d;background:#fff;color:#3d2f0e;border-radius:12px;padding:1px 9px;font:600 12px 'Open Sans',Arial,sans-serif;cursor:pointer}.excl-sugg .excl-no{border-color:transparent;background:none;color:#85754d;margin-left:2px}
#period-view{display:none;margin:15px 25px 25px}.pv-on #period-view{display:block}.pv-on #current-quarter-view .stats-row,.pv-on #current-quarter-view .charts-column,.pv-on #current-quarter-view .table-container{display:none}
.pv-head{display:flex;align-items:center;gap:16px;flex-wrap:wrap;margin-bottom:12px}.pv-head label{font-weight:600;color:#4b2e83;display:flex;align-items:center;gap:8px}.pv-head select{font:inherit;padding:4px 8px;border:1px solid #ccc;border-radius:5px}
.pv-hint{font-size:13px;color:#777}#bg-progress{display:none;align-items:center;gap:12px;margin:12px 25px 0;font-size:12px;color:#4b2e83}
.pv-bar{width:240px;height:8px;background:#e8e3f3;border-radius:4px;overflow:hidden}.pv-fill{height:100%;width:0;background:#4b2e83;transition:width .2s}
.pv-year,.pv-col{background:#fff;border-radius:6px;box-shadow:0 1px 3px rgba(0,0,0,.05);padding:12px 16px}.pv-year{margin-bottom:15px}
.pv-year h2,.pv-col h2{margin:0 0 10px;font-size:16px;color:#4b2e83;display:flex;align-items:center;gap:10px}.pv-this{font-size:11px;font-weight:600;color:#85754d;background:#fbf6e6;border-radius:10px;padding:2px 8px;cursor:help}
.pv-cards{display:grid;grid-template-columns:repeat(5,1fr);gap:8px}.pv-cols .pv-cards,.pv-sdetail .pv-cards{grid-template-columns:repeat(3,1fr)}
.pv-card{border:1px solid #eee;border-radius:6px;padding:7px 10px}.pv-card h3{margin:0;font-size:11px;color:#777;text-transform:uppercase;letter-spacing:.4px;font-weight:600}.pv-card h3 .nc,.pv-card h3 .est{text-transform:none}.pv-card h3 .est{font-weight:normal;color:#999}
.pv-v{font-size:22px;font-weight:700;color:#4b2e83;margin-top:2px}.pv-cols{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:15px}.pv-col.pv-focus{box-shadow:0 0 0 3px #b9a9e0}
.pv-chart{height:300px;margin-top:8px}.pv-na{color:#999;font-size:13px}.pv-big-na{padding:30px 0;text-align:center}
.pv-table{width:100%;border-collapse:separate;border-spacing:6px}.pv-table thead th{text-align:left;color:#4b2e83;font-size:12px;text-transform:uppercase;letter-spacing:.5px;padding:2px 10px}
.pv-table th.pv-yr{text-align:left;color:#2e1a5c;font-size:15px;white-space:nowrap;background:#fff;border-radius:6px;padding:10px 14px;cursor:pointer;box-shadow:0 1px 3px rgba(0,0,0,.05)}.pv-table th.pv-yr span{display:block;font-size:11px;font-weight:normal;color:#85754d}
.pv-cell{background:#fff;border-radius:6px;padding:12px 14px;font-size:13px;line-height:1.6;color:#333;vertical-align:top;cursor:pointer;box-shadow:0 1px 3px rgba(0,0,0,.05);height:78px}
.pv-cell:hover,.pv-table th.pv-yr:hover{box-shadow:0 0 0 2px #b9a9e0}.pv-cell.pv-na{color:#aaa;vertical-align:middle;cursor:default;background:#fafafa}.pc-big b{font-size:20px;color:#2e1a5c}.pv-cell b{color:#2e1a5c}
.pv-table .pv-tot{border-left:3px solid #e6d9b0}.pv-table tbody td:last-child{box-shadow:inset 3px 0 0 #e6d9b0,0 1px 3px rgba(0,0,0,.05)}.pv-stable tbody td:last-child{box-shadow:0 1px 3px rgba(0,0,0,.05)}
.pv-summers{display:grid;grid-template-columns:minmax(320px,420px) 1fr;gap:15px;align-items:start}.pv-stable tr.pv-sel .pv-cell,.pv-stable tr.pv-sel th{box-shadow:0 0 0 3px #b9a9e0}
@media (max-width:1100px){.pv-cols,.pv-summers{grid-template-columns:1fr}.pv-cards{grid-template-columns:repeat(3,1fr)}}"""

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
    /* For the quarter shown by default; Year, Decade and Summers pass another quarter's lectures and quiz sections. */
    function taEstimate(filtered, lectures, quizzes){
        lectures = lectures || rawData; quizzes = quizzes || quizData;
        const lectureOf = {}, counted = {}, load = {}, coursesOf = {};
        lectures.forEach(function(d){ lectureOf[lectureKey(d)] = d; });
        filtered.forEach(function(d){ counted[lectureKey(d)] = true; });
        quizzes.forEach(function(q){ if(isTa(q.leader)){ load[q.leader] = (load[q.leader] || 0) + 1; (coursesOf[q.leader] = coursesOf[q.leader] || {})[q.prefix + " " + q.number] = true; } });
        const loads = Object.keys(load).map(function(k){ return load[k]; });
        const usual = loads.length ? mostCommon(loads, 2) : 2;
        const courses = {}, named = {};
        quizzes.filter(function(q){ return counted[lectureKey(q)]; }).forEach(function(q){
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
    /* The page TSMod was opened on, for its own prefix (see startPrefix), if it loaded within 10 minutes. */
    let openerPage = null;
    try {
        const o = window.opener, loadedAt = o && o.performance ? o.performance.timeOrigin : 0;
        if(o && startPage && o.location.pathname.toLowerCase().endsWith("/" + startPage.toLowerCase()) && o.location.pathname.toUpperCase().indexOf("/" + currQuarterId + "/") !== -1
            && Date.now() - loadedAt < 10 * 60 * 1000) openerPage = { file: startPage.toLowerCase(), html: "<!DOCTYPE html>\n" + o.document.documentElement.outerHTML, at: new Date(loadedAt).toISOString() };
    } catch(e){ openerPage = null; }
    const usedOpener = {};
    function fetchFirstPage(p){
        if(openerPage && prefixLookup[p].toLowerCase() === openerPage.file && !usedOpener[p]){
            usedOpener[p] = openerPage.at;
            const html = openerPage.html;
            return Promise.resolve({ ok: true, status: 200, text: function(){ return Promise.resolve(html); } });
        }
        return fetch(baseUrl + prefixLookup[p]);
    }
    function pageTime(p){ return usedOpener[p] || new Date().toISOString(); }
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
        $("#snap-asof").text(t ? " · as of " + fmtWhen(t, !sameDay(t, new Date())) : "")
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
                if(res.ok) storeHistoryPage(t.key, await res.text()); else { tsDataCache[t.key] = []; tsQuizCache[t.key] = []; }
            } catch(e){ tsDataCache[t.key] = []; tsQuizCache[t.key] = []; }
        }
    }
    function snapshotFileName(note, iso){
        const d = new Date(iso || Date.now()), pad = function(n){ return String(n).padStart(2, "0"); };
        const stamp = d.getFullYear() + "-" + pad(d.getMonth() + 1) + "-" + pad(d.getDate()) + " " + pad(d.getHours()) + pad(d.getMinutes());
        const ps = activePrefixes.length > 4 ? activePrefixes.slice(0, 3).join(" ") + " +" + (activePrefixes.length - 3) : activePrefixes.join(" ");
        return ("Time Schedule " + currQuarterId + " " + ps + " " + stamp + (note ? " " + note : "")).replace(/[\\/:*?"<>|]+/g, "-").replace(/\s+/g, " ").trim().slice(0, 150) + ".html";
    }
    /* Everything the dashboard needs to reopen as it is now: the rows, the filters and selections, and (if asked) history. */
    /* ---- Enrollment Summary: denied requests and room size (Oct 2026) ----
       The Time Schedule's Enrollment Summary (sdb.admin.uw.edu .../tsstat.asp) adds, for each section, the room's capacity and
       how many registration requests were denied. Its site doesn't let other sites read it, so Get them opens it in a tab; the
       user clicks the TimeScheduleMod bookmark there, which reads that page and the same page for the dashboard's other 39
       quarters (same site) and posts the numbers back here (see tsmSummary in the bookmarklet's own code). Kept in this
       browser by quarter and prefix ("AUT2026_PHIL": { at, secs: { SLN: [room, denied, withdrawn] } }), and in snapshots.
       Withdrawn sections don't count. */
    const SUMMARY_URL = "https://sdb.admin.uw.edu/timeschd/uwnetid/tsstat.asp", SUMMARY_ORIGIN = new URL(SUMMARY_URL).origin;
    let enrollSummary = {};
    try { enrollSummary = SNAPSHOT ? (SNAPSHOT.summary || {}) : JSON.parse(localStorage.getItem("tsmod-enrollment-summary") || "{}") || {}; } catch(e){ enrollSummary = {}; }
    function saveSummary(){ if(SNAPSHOT) return; try { localStorage.setItem("tsmod-enrollment-summary", JSON.stringify(enrollSummary)); } catch(e){} }
    function summaryOf(q, d){ const s = enrollSummary[q + "_" + d.prefix]; return s && s.secs && s.secs[d.sln] ? s.secs[d.sln] : null; }
    function hasSummary(q){ return activePrefixes.length > 0 && activePrefixes.every(function(p){ return !!enrollSummary[q + "_" + p]; }); }
    function summaryAsOf(q){ return activePrefixes.map(function(p){ return (enrollSummary[q + "_" + p] || {}).at || ""; }).filter(Boolean).sort()[0] || ""; }
    /* For one quarter's counted lecture sections (and their quiz sections): requests denied, and seats the rooms could still
       hold where students were turned away (no more than were denied). null until that quarter's summary is in. */
    function demand(q, rows, quiz){
        if(!hasSummary(q)) return null;
        const out = { denied: 0, quizDenied: 0, grow: 0, withdrawn: 0, top: [] };
        rows.forEach(function(d){
            const s = summaryOf(q, d);
            if(!s) return;
            if(s[2]){ out.withdrawn++; return; }
            out.denied += s[1];
            if(s[1] > 0){ const room = s[0] > d.lim ? s[0] - d.lim : 0; out.grow += Math.min(room, s[1]); out.top.push({ d: d, room: s[0], denied: s[1] }); }
        });
        (quiz || []).forEach(function(d){ const s = summaryOf(q, d); if(s && !s[2]) out.quizDenied += s[1]; });
        out.top.sort(function(a, b){ return b.denied - a.denied || (a.d.prefix + a.d.number + a.d.section).localeCompare(b.d.prefix + b.d.number + b.d.section); });
        return out;
    }
    function demandLines(dm){
        return dm.top.slice(0, 15).map(function(t){ return t.d.prefix + " " + t.d.number + " " + t.d.section + ": " + plural(t.denied, "denied", "denied") + " · " + t.d.enrl + " of " + t.d.lim + " seats"
            + (t.room > 0 ? " · room holds " + t.room : ""); }).concat(dm.top.length > 15 ? ["…and " + plural(dm.top.length - 15, "more section")] : []);
    }
    function renderDeniedCard(filtered){
        const counted = {};
        filtered.forEach(function(d){ counted[lectureKey(d)] = true; });
        const dm = demand(currQuarterId, filtered, quizData.filter(function(q){ return counted[lectureKey(q)]; }));
        $("#dn-get").toggle(!SNAPSHOT).text(dm ? "Update" : "Get them");
        if(!dm){
            $("#stat-denied").text("–");
            $("#stat-denied-sub").text(SNAPSHOT ? "Not in this snapshot" : "From the Enrollment Summary");
            $("#denied-card").attr("title", "Registration requests turned away, and room sizes, come from the Time Schedule's Enrollment Summary.\nGet them opens it in a new tab: click your TimeScheduleMod bookmark there, and it sends this quarter's and the past ten years' numbers back here.");
            return;
        }
        $("#stat-denied").text(fmtN(dm.denied));
        $("#stat-denied-sub").html(snapEsc(dm.top.length ? "at " + plural(dm.top.length, "section") + (dm.grow ? " · room for " + fmtN(dm.grow) + " more" : "") : "no section turned students away")
            + (dm.quizDenied ? "<br>" + snapEsc("+ " + fmtN(dm.quizDenied) + " at quiz sections") : ""));
        $("#denied-card").attr("title", ["Registration requests denied for the lecture sections counted, from the Enrollment Summary" + (summaryAsOf(currQuarterId) ? " (" + new Date(summaryAsOf(currQuarterId)).toLocaleString() + ")" : "") + "."]
            .concat(dm.grow ? ["Rooms hold " + fmtN(dm.grow) + " more students in those sections (up to the number denied)."] : [])
            .concat(dm.quizDenied ? ["Quiz sections: " + fmtN(dm.quizDenied) + " more denied."] : [])
            .concat(dm.withdrawn ? [plural(dm.withdrawn, "withdrawn section") + " not counted."] : [])
            .concat(dm.top.length ? ["", "Most denied:"].concat(demandLines(dm)) : []).join("\n"));
    }
    /* Get them: the Enrollment Summary for the first prefix, with what to fetch (prefixes, quarters, where to send) in its address's #. */
    function openSummary(){
        if(!activePrefixes.length || SNAPSHOT) return;
        const req = { p: activePrefixes.slice(), q: histQuarters.map(function(h){ return h.str; }), o: location.origin };
        const url = SUMMARY_URL + "?QTRYR=" + currQuarterId.slice(0, 3) + "+" + currQuarterId.slice(3) + "&CURRIC=" + encodeURIComponent(activePrefixes[0]).replace(/%20/g, "+")
            + "#tsmod=" + encodeURIComponent(JSON.stringify(req));
        if(!window.open(url, "_blank")) $("#stat-denied-sub").text("Pop-up blocked: allow pop-ups for this page, then Get them again");
        else $("#stat-denied-sub").text("In the new tab, click your TimeScheduleMod bookmark");
    }
    window.addEventListener("message", function(e){
        if(SNAPSHOT || e.origin !== SUMMARY_ORIGIN || !e.data || e.data.type !== "tsmod-enrollment-summary") return;
        const num = function(v){ v = parseInt(v, 10); return isNaN(v) || v < 0 ? 0 : v; };
        (e.data.pages || []).forEach(function(pg){
            if(!pg || !/^[A-Z]{3}\d{4}$/.test(pg.q) || typeof pg.prefix !== "string" || !pg.secs || typeof pg.secs !== "object") return;
            const secs = {};
            Object.keys(pg.secs).forEach(function(sln){ const v = pg.secs[sln]; if(/^\d{4,5}$/.test(sln) && Array.isArray(v)) secs[sln] = [num(v[0]), num(v[1]), v[2] ? 1 : 0]; });
            enrollSummary[pg.q + "_" + pg.prefix.toUpperCase()] = { at: String(pg.at || ""), secs: secs };
        });
        saveSummary();
        renderDashboard();
        if(isPeriodView()) renderPeriod();
    });
    function snapshotSummary(){
        const out = {};
        Object.keys(enrollSummary).forEach(function(k){ if(activePrefixes.indexOf(k.slice(k.indexOf("_") + 1)) !== -1) out[k] = enrollSummary[k]; });
        return out;
    }
    function snapshotData(note, withHistory){
        const shown = function(d){ return activePrefixes.indexOf(d.src) !== -1; };
        let history = null, quizHistory = null;
        if(withHistory){
            history = {}; quizHistory = {};
            Object.keys(tsDataCache).forEach(function(k){ const p = k.slice(k.indexOf("_") + 1); if(activePrefixes.indexOf(p) !== -1 && k.indexOf(currQuarterId + "_") !== 0){ history[k] = tsDataCache[k]; if(tsQuizCache[k]) quizHistory[k] = tsQuizCache[k]; } });
        }
        const times = {};
        activePrefixes.forEach(function(p){ times[p] = fetchedAt[p]; });
        return { version: 1, note: note, quarter: currQuarterId, dataAsOf: dataAsOf(), savedAt: new Date().toISOString(), prefixes: activePrefixes.slice(), fetchedAt: times,
            rawData: rawData.filter(shown), quizData: quizData.filter(shown), history: history, quizHistory: quizHistory, summary: snapshotSummary(),
            ui: { genEds: $(".gened-filter:checked").map(function(){ return this.value; }).get(), excludedSections: excludedSections.slice(), excludedInstructors: excludedInstructors.slice(),
                table: dataTable ? { order: dataTable.order(), search: dataTable.search(), length: dataTable.page.len() } : null,
                timeSeries: $("#ts-toggle").is(":checked"), tsSelected: $("#ts-course-select").val() || [], tsExcludedInstructors: tsExcludedInstructors.slice(),
                excludedCourses: excludedCourses.slice(), view: viewMode, year: pvYear, summer: pvSummer, tsMode: tsMode, sequences: customSeqs, seq: pvSeq } };
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
        excludedCourses = ui.excludedCourses || [];
        if(ui.year) pvYear = ui.year;
        if(ui.summer) pvSummer = ui.summer;
        if(ui.seq) pvSeq = ui.seq;
        Object.assign(tsQuizCache, s.quizHistory || {});
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
            setView(ui.tsMode === "summer" ? "sumseries" : "ayseries");
            if(ui.tsSelected && ui.tsSelected.length) $("#ts-course-select").val(ui.tsSelected).trigger("change");
        } else if(ui.view && ui.view !== "quarter") setView(ui.view);
    }
"""

PERIOD = r"""    /* ---- Year, Decade and Summers ----
       Other quarters, from the same Time Schedule pages Time Series reads (one shared cache): one academic year (Autumn,
       Winter, Spring), the last ten academic years, and the last ten summers. Summer is never part of a year; it has its own
       view. Past quarters show the numbers the Time Schedule archive keeps for them.
       Each quarter is counted with the Quarter view's filters, generalized: Gen Ed, the level picked under "Count only",
       the instructors unchecked, and the courses excluded everywhere (excludedCourses). Unchecking single sections changes
       only the Quarter view's own quarter, since section codes change every quarter. */
    const tsQuizCache = {};
    let viewMode = "quarter", pvYear = null, pvFocus = null, pvScrollOnce = false, pvSummer = null, tsMode = "ay";
    const QN3 = { WIN: 0, SPR: 1, SUM: 2, AUT: 3 }, YEAR_QTRS = ["AUT", "WIN", "SPR"];
    function qIndex(id){ return +id.slice(3) * 4 + QN3[id.slice(0, 3)]; }
    function qOfYear(q, ay){ return q + (q === "AUT" ? ay : ay + 1); }
    function ayLabel(ay){ return ay + "–" + String(ay + 1).slice(2); }
    /* The newest academic year and summer to show: the page's own, and from Summer on, the coming Autumn's year. */
    const NEWEST_AY = (function(){ const q = currQuarterId.slice(0, 3), y = +currQuarterId.slice(3); return q === "AUT" || q === "SUM" ? y : y - 1; })();
    const NEWEST_SUMMER = (function(){ const q = currQuarterId.slice(0, 3), y = +currQuarterId.slice(3); return q === "WIN" ? y - 1 : y; })();
    pvYear = NEWEST_AY;
    function fmtN(n){ return Number(n).toLocaleString("en-US"); }
    /* A history page: its lecture rows (for Time Series and these views) and its quiz rows, with TA names replaced. */
    function storeHistoryPage(key, html){
        const rows = parseUWTimeSchedule(html, true);
        labelQuizLeaders(rows, rows.quiz);
        tsQuizCache[key] = rows.quiz;
        tsDataCache[key] = rows;
        return rows;
    }

    /* Courses excluded everywhere, by prefix and number (e.g. "PHIL 484"): unchecking every section of a course in the
       Quarter view adds it; × in the Excluded bar, or checking one of its sections again, removes it. Kept in this browser
       (and in snapshots), so independent-study courses stay out of every quarter's numbers. Suggested: courses whose
       sections all meet "to be arranged" with variable credits, the Time Schedule's signs of independent study. */
    function courseKey(d){ return d.prefix + " " + d.number; }
    function loadList(k){ if(SNAPSHOT) return []; try { return JSON.parse(localStorage.getItem(k) || "[]") || []; } catch(e){ return []; } }
    function saveList(k, v){ if(SNAPSHOT) return; try { localStorage.setItem(k, JSON.stringify(v)); } catch(e){} }
    let excludedCourses = loadList("tsmod-excluded-courses"), dismissedSuggestions = loadList("tsmod-excl-dismissed");
    function saveExcludedCourses(){ saveList("tsmod-excluded-courses", excludedCourses); }
    function applyCourseExclusions(){
        rawData.forEach(function(d){ const k = sectionKey(d); if(excludedCourses.indexOf(courseKey(d)) !== -1 && excludedSections.indexOf(k) === -1) excludedSections.push(k); });
    }
    function exclusionSuggestions(){
        const by = {};
        rawData.filter(function(d){ return activePrefixes.indexOf(d.prefix) !== -1; }).forEach(function(d){ (by[courseKey(d)] = by[courseKey(d)] || []).push(d); });
        return Object.keys(by).filter(function(k){
            return excludedCourses.indexOf(k) === -1 && dismissedSuggestions.indexOf(k) === -1
                && by[k].every(function(d){ return d.tba; }) && by[k].some(function(d){ return d.varCredits; });
        }).sort();
    }
    function renderExclBar(){
        const shown = excludedCourses.filter(function(k){ return activePrefixes.some(function(p){ return k.indexOf(p + " ") === 0; }); }).sort();
        const sugg = SNAPSHOT ? [] : exclusionSuggestions();
        const bar = $("#excl-bar");
        if(!shown.length && !sugg.length){ bar.hide().empty(); return; }
        bar.html((shown.length ? "<strong title='Left out of every quarter and every view, and remembered in this browser. To add a course, uncheck all of its sections in the table; × brings it back.'>Excluded everywhere:</strong>"
                + shown.map(function(k){ return "<span class='excl-chip'>" + snapEsc(k) + (SNAPSHOT ? "" : "<button type='button' data-course='" + snapEsc(k) + "' aria-label='Include " + snapEsc(k) + " again'>×</button>") + "</span>"; }).join("") : "")
            + (sugg.length ? "<span class='excl-sugg' title='Every section meets “to be arranged”, with variable credits: the usual signs of independent study'>Look like independent study: <b>" + snapEsc(sugg.join(", ")) + "</b>"
                + "<button type='button' class='excl-yes'>Exclude " + (sugg.length === 1 ? "it" : "them") + "</button><button type='button' class='excl-no'>Not now</button></span>" : "")).show();
    }
    $(document).on("click", "#excl-bar [data-course]", function(){
        const k = $(this).attr("data-course"), keys = rawData.filter(function(d){ return courseKey(d) === k; }).map(sectionKey);
        excludedCourses = excludedCourses.filter(function(x){ return x !== k; });
        excludedSections = excludedSections.filter(function(x){ return keys.indexOf(x) === -1; });
        saveExcludedCourses();
        renderDashboard();
    });
    $(document).on("click", "#excl-bar .excl-yes", function(){
        exclusionSuggestions().forEach(function(k){ if(excludedCourses.indexOf(k) === -1) excludedCourses.push(k); });
        saveExcludedCourses();
        renderDashboard();
    });
    $(document).on("click", "#excl-bar .excl-no", function(){
        dismissedSuggestions = dismissedSuggestions.concat(exclusionSuggestions());
        saveList("tsmod-excl-dismissed", dismissedSuggestions);
        renderExclBar();
    });

    /* The Quarter view's level under "Count only", when one level is picked. */
    function chosenLevel(){ const b = $(".level-btn.active"); return b.length && b.attr("data-level") !== "all" ? b.attr("data-level") : null; }
    function genEdOk(d, genEds){ return (d.genEd.length === 0 && genEds.indexOf("None") !== -1) || d.genEd.some(function(g){ return genEds.indexOf(g) !== -1; }); }
    /* One quarter's numbers, with the generalized filters. The page's own quarter uses the Quarter view's exact choices. */
    function quarterStats(id){
        const genEds = $(".gened-filter:checked").map(function(){ return this.value; }).get(), level = chosenLevel(), own = id === currQuarterId;
        let all = [], quiz = [], loaded = true, any = false;
        activePrefixes.forEach(function(p){
            const key = id + "_" + p;
            if(own){ all = all.concat(rawData.filter(function(d){ return d.prefix === p; })); quiz = quiz.concat(quizData.filter(function(q){ return q.prefix === p; })); any = true; return; }
            if(!(key in tsDataCache)){ if(!SNAPSHOT) loaded = false; return; }
            const rows = tsDataCache[key].filter(function(d){ return d.prefix === p; });
            if(rows.length) any = true;
            all = all.concat(rows);
            quiz = quiz.concat((tsQuizCache[key] || []).filter(function(q){ return q.prefix === p; }));
        });
        const rows = all.filter(function(d){
            if(!genEdOk(d, genEds) || excludedInstructors.indexOf(d.instructor) !== -1 || excludedCourses.indexOf(courseKey(d)) !== -1) return false;
            return own ? excludedSections.indexOf(sectionKey(d)) === -1 : !level || d.level === level;
        });
        const enrl = rows.reduce(function(n, d){ return n + d.enrl; }, 0), lim = rows.reduce(function(n, d){ return n + d.lim; }, 0), t = taEstimate(rows, all, quiz);
        const counted = {};
        rows.forEach(function(d){ counted[lectureKey(d)] = true; });
        const dm = demand(id, rows, quiz.filter(function(q){ return counted[lectureKey(q)]; }));
        return { id: id, dm: dm, rows: rows, sections: rows.length, enrl: enrl, lim: lim, pct: lim ? enrl / lim * 100 : null, tas: t.named + t.more, approx: t.more > 0, quiz: t.sections,
            state: !loaded ? "loading" : any ? "ok" : qIndex(id) > qIndex(currQuarterId) ? "future" : "none" };
    }
    function sumStats(list){
        const ok = list.filter(function(st){ return st.state === "ok"; }), enrl = ok.reduce(function(n, st){ return n + st.enrl; }, 0), lim = ok.reduce(function(n, st){ return n + st.lim; }, 0);
        const withDm = ok.filter(function(st){ return st.dm; }), dm = withDm.length ? { denied: withDm.reduce(function(n, st){ return n + st.dm.denied; }, 0), grow: withDm.reduce(function(n, st){ return n + st.dm.grow; }, 0), parts: withDm.length } : null;
        return { dm: dm, sections: ok.reduce(function(n, st){ return n + st.sections; }, 0), enrl: enrl, lim: lim, pct: lim ? enrl / lim * 100 : null, tas: ok.reduce(function(n, st){ return n + st.tas; }, 0),
            approx: ok.some(function(st){ return st.approx; }), parts: ok.length, state: ok.length ? "ok" : list.some(function(st){ return st.state === "loading"; }) ? "loading" : "none" };
    }
    function stateText(st){
        if(st.state === "loading") return "Loading…";
        if(st.state === "future") return "Not published yet";
        if(SNAPSHOT && st.id && st.id !== currQuarterId && !Object.keys(SNAPSHOT.history || {}).some(function(k){ return k.indexOf(st.id + "_") === 0; })) return "Not in this snapshot";
        return "No sections";
    }
    function cardsHtml(st, taTitle){
        const card = function(h, v, extra){ return "<div class='pv-card'" + (extra || "") + "><h3>" + h + "</h3><div class='pv-v'>" + v + "</div></div>"; };
        return "<div class='pv-cards'>" + card("Sections", fmtN(st.sections)) + card("Enrolled", fmtN(st.enrl)) + card("Capacity", fmtN(st.lim))
            + card("Fullness", st.pct === null ? "–" : st.pct.toFixed(1) + "%")
            + card("<span class='nc'>TAs</span> <span class='est'>(est.)</span>", (st.approx ? "≈" : "") + st.tas, taTitle ? " title='" + snapEsc(taTitle) + "'" : "")
            + (st.dm ? card("Denied", fmtN(st.dm.denied), " title='" + snapEsc("Registration requests denied, from the Enrollment Summary" + (st.dm.grow ? "; rooms hold " + fmtN(st.dm.grow) + " more where students were turned away" : "")
                + (st.dm.top && st.dm.top.length ? "\n\n" + demandLines(st.dm).join("\n") : "")) + "'") : "") + "</div>";
    }
    /* Shading by fullness: lavender to deeper purple, and dark green when over capacity, as in the % Full dots. */
    function shade(pct){ return pct === null ? "" : pct > 100 ? "background:rgba(45,106,46,.16)" : "background:rgba(75,46,131," + (0.03 + 0.2 * Math.min(pct, 100) / 100).toFixed(3) + ")"; }
    function cellHtml(st, attrs, ta){
        if(st.state !== "ok") return "<td class='pv-cell pv-na'" + attrs + ">" + snapEsc(stateText(st)) + "</td>";
        return "<td class='pv-cell'" + attrs + " style='" + shade(st.pct) + "'><div class='pc-big'><b>" + fmtN(st.enrl) + "</b> enrolled</div>"
            + "<div>of " + fmtN(st.lim) + " seats · <b>" + (st.pct === null ? "–" : st.pct.toFixed(1) + "%") + "</b> full</div>"
            + "<div>" + plural(st.sections, "section") + " · " + (st.approx ? "≈" : "") + st.tas + " " + (ta || (st.tas === 1 ? "TA" : "TAs")) + "</div>"
            + (st.dm ? "<div class='pv-dn'>" + fmtN(st.dm.denied) + " denied" + (st.dm.grow ? " · room for " + fmtN(st.dm.grow) : "") + "</div>" : "") + "</td>";
    }
    function scatterTraces(rows){
        const traces = [];
        activePrefixes.forEach(function(prefix){
            const pr = rows.filter(function(d){ return d.prefix === prefix && d.lim > 0; });
            if(!pr.length) return;
            traces.push({ x: pr.map(function(d){ return d.lim; }), y: pr.map(function(d){ return d.enrl; }), mode: "markers", type: "scatter", name: prefix,
                marker: { size: 11, color: colorFor(prefix), opacity: 0.85, line: { color: "#ffffff", width: 1 } },
                text: pr.map(function(d){ return d.prefix + " " + d.number + " " + d.section + "<br>" + d.name + "<br>" + d.instructor + "<br>Enrl: " + d.enrl + "/" + d.lim; }), hoverinfo: "text" });
        });
        const max = Math.max.apply(null, rows.map(function(d){ return d.lim; }).concat([10]));
        traces.push({ x: [0, max], y: [0, max], mode: "lines", type: "scatter", name: "100% Full", line: { dash: "dash", color: "#e41a1c", width: 1.5 }, hoverinfo: "none" });
        return traces;
    }
    function drawScatter(id, rows){
        Plotly.react(id, scatterTraces(rows), { xaxis: { title: "Capacity" }, yaxis: { title: "Enrolled" }, showlegend: activePrefixes.length > 1, legend: { orientation: "h", y: -0.28 },
            autosize: true, height: 300, margin: { t: 12, l: 48, r: 10, b: 44 } }, { responsive: true, displayModeBar: false });
    }
    function quarterBlock(st, chartId){
        return "<h2>" + snapEsc(quarterName(st.id)) + (st.id === currQuarterId ? " <span class='pv-this' title='The Quarter view’s quarter: its own section choices apply'>this quarter</span>" : "") + "</h2>"
            + (st.state === "ok" ? cardsHtml(st) + "<div class='pv-chart' id='" + chartId + "'></div>" : "<div class='pv-na pv-big-na'>" + snapEsc(stateText(st)) + "</div>");
    }
    function drawYear(){
        const stats = YEAR_QTRS.map(function(q){ return quarterStats(qOfYear(q, pvYear)); }), year = sumStats(stats);
        $("#period-view").html("<div class='pv-year'><h2>" + ayLabel(pvYear) + (year.parts && year.parts < 3 ? " <span class='pv-this'>" + year.parts + " of 3 quarters</span>" : "") + "</h2>"
            + (year.state === "ok" ? cardsHtml(year, "TA-quarters: each quarter’s estimate, added up (a TA in all three quarters counts 3)") : "<div class='pv-na pv-big-na'>" + (year.state === "loading" ? "Loading…" : "No sections") + "</div>") + "</div>"
            + "<div class='pv-cols'>" + stats.map(function(st, i){ return "<div class='pv-col" + (pvFocus === st.id ? " pv-focus" : "") + "' data-q='" + st.id + "'>" + quarterBlock(st, "pv-chart-" + i) + "</div>"; }).join("") + "</div>");
        stats.forEach(function(st, i){ if(st.state === "ok") drawScatter("pv-chart-" + i, st.rows); });
        if(pvFocus && pvScrollOnce){ const el = document.querySelector(".pv-col.pv-focus"); if(el){ el.scrollIntoView({ block: "nearest" }); pvScrollOnce = false; } }
    }
    function drawDecade(){
        let body = "";
        for(let ay = NEWEST_AY; ay > NEWEST_AY - 10; ay--){
            const stats = YEAR_QTRS.map(function(q){ return quarterStats(qOfYear(q, ay)); }), year = sumStats(stats);
            body += "<tr><th class='pv-yr' data-year='" + ay + "' title='Open " + ayLabel(ay) + " in Year'>" + ayLabel(ay) + (year.parts && year.parts < 3 ? "<span>" + year.parts + " of 3 quarters</span>" : "") + "</th>"
                + stats.map(function(st){ return cellHtml(st, " data-year='" + ay + "' data-q='" + st.id + "' title='Open " + quarterName(st.id) + " in Year'"); }).join("")
                + cellHtml(Object.assign({ id: "" }, year), " data-year='" + ay + "' title='Open " + ayLabel(ay) + " in Year. TAs are TA-quarters: each quarter’s estimate, added up.'", year.tas === 1 ? "TA-quarter" : "TA-quarters") + "</tr>";
        }
        $("#period-view").html("<div class='pv-head'><span class='pv-hint'>The last ten academic years. Click a year or quarter to open it in Year.</span></div>"
            + "<table class='pv-table'><thead><tr><th>Academic year</th><th>Autumn</th><th>Winter</th><th>Spring</th><th class='pv-tot'>Year</th></tr></thead><tbody>" + body + "</tbody></table>");
    }
    function drawSummers(){
        const list = [];
        for(let y = NEWEST_SUMMER; y > NEWEST_SUMMER - 10; y--) list.push(quarterStats("SUM" + y));
        if(pvSummer === null || !list.some(function(st){ return st.id === "SUM" + pvSummer && st.state === "ok"; })){ const first = list.filter(function(st){ return st.state === "ok"; })[0]; if(first) pvSummer = +first.id.slice(3); }
        const sel = list.filter(function(st){ return st.id === "SUM" + pvSummer; })[0];
        $("#period-view").html("<div class='pv-head'><span class='pv-hint'>The last ten summers. Click one to see it beside the list.</span></div><div class='pv-summers'><table class='pv-table pv-stable'><thead><tr><th>Summer</th><th>All terms</th></tr></thead><tbody>"
            + list.map(function(st){ return "<tr class='" + (sel && st.id === sel.id ? "pv-sel" : "") + "'><th class='pv-yr' data-summer='" + st.id.slice(3) + "'>" + st.id.slice(3) + "</th>" + cellHtml(st, " data-summer='" + st.id.slice(3) + "'") + "</tr>"; }).join("")
            + "</tbody></table><div class='pv-col pv-sdetail'>" + (sel && sel.state === "ok" ? quarterBlock(sel, "pv-chart-sum") : "<div class='pv-na pv-big-na'>" + (list.some(function(st){ return st.state === "loading"; }) ? "Loading…" : "No summer sections") + "</div>") + "</div></div>");
        if(sel && sel.state === "ok") drawScatter("pv-chart-sum", sel.rows);
    }
    function neededQuarters(){
        const ids = [];
        if(viewMode === "year") YEAR_QTRS.forEach(function(q){ ids.push(qOfYear(q, pvYear)); });
        if(viewMode === "decade") for(let ay = NEWEST_AY; ay > NEWEST_AY - 10; ay--) YEAR_QTRS.forEach(function(q){ ids.push(qOfYear(q, ay)); });
        if(viewMode === "summers") for(let y = NEWEST_SUMMER; y > NEWEST_SUMMER - 10; y--) ids.push("SUM" + y);
        return ids;
    }
    function isPeriodView(){ return viewMode === "year" || viewMode === "decade" || viewMode === "summers" || viewMode === "sequences"; }
    function drawPeriod(){
        if(!activePrefixes.length){ $("#period-view").html("<div class='pv-na pv-big-na'>Add a prefix above to see " + (viewMode === "summers" ? "its summers" : viewMode === "year" ? "a year" : viewMode === "sequences" ? "its course sequences" : "a decade") + ".</div>"); return; }
        if(viewMode === "year") drawYear(); else if(viewMode === "decade") drawDecade(); else if(viewMode === "summers") drawSummers(); else if(viewMode === "sequences") drawSequences();
    }
    /* ---- Sequences (Oct 2026) ----
       A department's course sequences, academic year by academic year: the courses in order (MATH 120 → 124 → 125 …), each
       year's students per course (Autumn · Winter · Spring), and an executive strip on top: the latest full year against the
       oldest year shown, with the largest section then and now. Built in for MATH: the pathways and watch-lists from Andy
       Loveless's pathway chart and section-capacity report (Oct 2026), with its renumbered courses joined (207 was 307, …).
       Any department: sequences found from course titles (one title at one level, numbered I, II, III…, e.g. ELEMENTARY
       SPANISH 101-103), the courses whose largest section grew most, and sequences the user adds (kept in this browser).
       Counts are lecture sections' enrollment and limits as the Time Schedule shows them, unfiltered: the Quarter view's
       filters and exclusions don't apply here. Summer is left out, as in Year and Decade. */
    const SEQ_PRESETS = {
        MATH: { source: "MATH’s pathways and watch-lists, from Andy Loveless’s pathway chart and section-capacity report",
            alias: { "307": "207", "308": "208", "324": "224", "310": "300" }, lists: [
            { name: "Calculus", flow: true, courses: ["120", "124", "125", "126", "207", "208"], note: "The main STEM pipeline, Precalculus through Linear Algebra" },
            { name: "Non-calculus", flow: true, courses: ["111", "112"], note: "For business, the social sciences, education and quantitative literacy" },
            { name: "Remediation", flow: true, courses: ["102", "103", "120"], note: "Pre-algebra and elementary functions, on to Precalculus" },
            { name: "High demand", courses: ["207", "208", "224"], note: "Where section sizes grew most" },
            { name: "Upper division", courses: ["300", "381", "394", "403", "407"], note: "The fastest-growing 300- and 400-level courses" }] }
    };
    let pvSeq = null;
    let customSeqs = (function(){ if(SNAPSHOT) return ((SNAPSHOT.ui || {}).sequences) || {}; try { return JSON.parse(localStorage.getItem("tsmod-sequences") || "{}") || {}; } catch(e){ return {}; } })();
    function saveSeqs(){ if(SNAPSHOT) return; try { localStorage.setItem("tsmod-sequences", JSON.stringify(customSeqs)); } catch(e){} }
    function seqYears(){ const out = []; for(let ay = NEWEST_AY; ay > NEWEST_AY - 10; ay--) out.push(ay); return out; }
    function titleCase(t){ return String(t).toLowerCase().replace(/(^|\s)([a-z])/g, function(m, a, b){ return a + b.toUpperCase(); }).replace(/\s(And|Of|In|With|For|To|The)\b/g, function(m){ return m.toLowerCase(); })
        .replace(/\b(Ii|Iii|Iv|Vi|Vii)\b/g, function(m){ return m.toUpperCase(); }); }
    /* One prefix's lecture (or quiz) rows for a quarter; null while its page isn't read yet. */
    function seqRows(q, p, quiz){
        if(q === currQuarterId) return (quiz ? quizData : rawData).filter(function(d){ return d.prefix === p; });
        const key = q + "_" + p;
        if(!(key in tsDataCache)) return null;
        return quiz ? (tsQuizCache[key] || []) : tsDataCache[key].filter(function(d){ return d.prefix === p; });
    }
    /* One course in one quarter, under its old number if it was renumbered (when the new number isn't offered then). */
    function seqCourse(p, num, q, alias){
        if(qIndex(q) > qIndex(currQuarterId)) return { state: "future" };
        const rows = seqRows(q, p);
        if(rows === null) return { state: "loading" };
        let lec = rows.filter(function(d){ return d.number === num; });
        if(!lec.length && alias){ const old = Object.keys(alias).filter(function(k){ return alias[k] === num; }); lec = rows.filter(function(d){ return old.indexOf(d.number) !== -1; }); }
        if(!lec.length) return { state: "none" };
        const keys = {};
        lec.forEach(function(d){ keys[lectureKey(d)] = true; });
        const quiz = (seqRows(q, p, true) || []).filter(function(d){ return keys[lectureKey(d)]; });
        return { state: "ok", q: q, enrl: lec.reduce(function(n, d){ return n + d.enrl; }, 0), lim: lec.reduce(function(n, d){ return n + d.lim; }, 0), sections: lec.length,
            maxLec: Math.max.apply(null, lec.map(function(d){ return d.lim; })), maxQuiz: quiz.length ? Math.max.apply(null, quiz.map(function(d){ return d.lim; })) : 0, quizzes: quiz.length,
            name: lec[0].name, from: lec[0].number };
    }
    /* One course in one academic year (Autumn, Winter, Spring). full: all three quarters are published. */
    function seqYear(p, num, ay, alias){
        const qs = YEAR_QTRS.map(function(q){ return seqCourse(p, num, qOfYear(q, ay), alias); }), ok = qs.filter(function(c){ return c.state === "ok"; });
        const old = ok.filter(function(c){ return c.from !== num; })[0];
        return { ay: ay, qs: qs, enrl: ok.reduce(function(n, c){ return n + c.enrl; }, 0), lim: ok.reduce(function(n, c){ return n + c.lim; }, 0), offered: ok.length,
            maxLec: ok.length ? Math.max.apply(null, ok.map(function(c){ return c.maxLec; })) : 0, maxQuiz: ok.length ? Math.max.apply(null, ok.map(function(c){ return c.maxQuiz; })) : 0,
            loading: qs.some(function(c){ return c.state === "loading"; }), full: qs.every(function(c){ return c.state === "ok" || c.state === "none"; }),
            name: ok.length ? ok[ok.length - 1].name : "", from: old ? old.from : null };
    }
    /* Sequences found from course titles, and the courses whose largest section grew most. */
    function detectSeqs(p){
        const pre = SEQ_PRESETS[p], titles = {}, total = {};
        seqYears().forEach(function(ay){ YEAR_QTRS.forEach(function(q){ (seqRows(qOfYear(q, ay), p) || []).forEach(function(d){ titles[d.number] = d.name; total[d.number] = (total[d.number] || 0) + d.enrl; }); }); });
        const groups = {}, out = [];
        Object.keys(titles).forEach(function(num){
            const m = String(titles[num]).toUpperCase().match(/^(.*?\S)[\s,:-]+(I{1,3}|IV|VI{0,3}|[1-6]|[A-D])$/);
            if(m) (groups[num.charAt(0) + "|" + m[1]] = groups[num.charAt(0) + "|" + m[1]] || []).push(num);
        });
        Object.keys(groups).forEach(function(k){
            const nums = groups[k].sort();
            if(nums.length < 2 || (pre && pre.lists.some(function(l){ return l.flow && nums.every(function(n){ return l.courses.indexOf(n) !== -1; }); }))) return;
            out.push({ name: titleCase(k.split("|")[1]), flow: true, courses: nums, total: nums.reduce(function(t, n){ return t + (total[n] || 0); }, 0), note: "Found from course titles: " + k.split("|")[1] + " I, II…" });
        });
        out.sort(function(a, b){ return b.total - a.total; });
        const years = seqYears(), grew = [];
        Object.keys(titles).forEach(function(num){
            const ys = years.map(function(ay){ return seqYear(p, num, ay, pre ? pre.alias : null); }).filter(function(y){ return y.offered && y.full; });
            if(ys.length < 2) return;
            const now = ys[0].maxLec, then = ys[ys.length - 1].maxLec;
            if(now > then && then > 0) grew.push({ num: num, by: now - then });
        });
        grew.sort(function(a, b){ return b.by - a.by || a.num.localeCompare(b.num); });
        const lists = out.slice(0, 6);
        if(grew.length) lists.push({ name: "Section-size growth", courses: grew.slice(0, 5).map(function(g){ return g.num; }).sort(), note: "The courses whose largest lecture section grew most over the years shown" });
        return lists;
    }
    function seqLists(){
        const out = [];
        activePrefixes.forEach(function(p){
            const pre = SEQ_PRESETS[p], alias = pre ? pre.alias : null;
            if(pre) pre.lists.forEach(function(l, i){ out.push(Object.assign({ id: p + ":built-in:" + i, prefix: p, kind: "built-in", alias: alias, source: pre.source }, l)); });
            detectSeqs(p).forEach(function(l){ out.push(Object.assign({ id: p + ":found:" + l.name + ":" + l.courses.join("-"), prefix: p, kind: "found", alias: alias }, l)); });
            (customSeqs[p] || []).forEach(function(l, i){ out.push({ id: p + ":mine:" + i, prefix: p, kind: "mine", index: i, name: l.name, flow: true, courses: l.courses, alias: alias, note: "Yours, kept in this browser" }); });
        });
        return out;
    }
    function spark(vals){
        const pts = vals.filter(function(v){ return v !== null; });
        if(pts.length < 2) return "";
        const max = Math.max.apply(null, pts), min = Math.min.apply(null, pts), w = 120, h = 26, n = vals.length;
        const xy = [];
        vals.forEach(function(v, i){ if(v !== null) xy.push([(i / (n - 1)) * (w - 6) + 3, h - 3 - (max === min ? 0.5 : (v - min) / (max - min)) * (h - 6)]); });
        const last = xy[xy.length - 1];
        return "<svg class='sq-spark' width='" + w + "' height='" + h + "' viewBox='0 0 " + w + " " + h + "' aria-hidden='true'><polyline fill='none' stroke='#8f7bc4' stroke-width='1.6' points='"
            + xy.map(function(c){ return c[0].toFixed(1) + "," + c[1].toFixed(1); }).join(" ") + "'/><circle cx='" + last[0].toFixed(1) + "' cy='" + last[1].toFixed(1) + "' r='2.6' fill='#4b2e83'/></svg>";
    }
    function pctChange(now, then){ if(!then) return null; return Math.round((now / then - 1) * 100); }
    function drawSequences(){
        const lists = seqLists();
        const cur = lists.filter(function(l){ return l.id === pvSeq; })[0] || lists[0];
        if(!cur){ $("#period-view").html("<div class='pv-na pv-big-na'>No sequences yet for " + snapEsc(activePrefixes.join(", ")) + ": add one with + Add a sequence.</div>" + seqChips([], null)); return; }
        pvSeq = cur.id;
        const years = seqYears(), many = activePrefixes.length > 1;
        const cols = cur.courses.map(function(num){ return { num: num, ys: years.map(function(ay){ return seqYear(cur.prefix, num, ay, cur.alias); }) }; });
        /* The latest full year, and the oldest year shown with the course in it (also full). */
        const latestIdx = years.findIndex(function(ay, i){ return cols.some(function(c){ return c.ys[i].full && c.ys[i].offered; }); });
        const tiles = cols.map(function(c){
            const now = latestIdx === -1 ? null : c.ys[latestIdx], base = c.ys.slice().reverse().filter(function(y){ return y.full && y.offered; })[0];
            const name = (c.ys.filter(function(y){ return y.name; })[0] || {}).name || "";
            const ch = now && base && base.ay !== now.ay ? pctChange(now.enrl, base.enrl) : null;
            return "<div class='sq-tile'><div class='sq-c'>" + snapEsc(cur.prefix + " " + c.num) + "</div><div class='sq-t'>" + snapEsc(titleCase(name)) + "</div>"
                + (now && now.offered ? "<div class='sq-n'><b>" + fmtN(now.enrl) + "</b> students</div>" : "<div class='sq-n sq-none'>Not offered in " + (latestIdx === -1 ? "these years" : ayLabel(years[latestIdx])) + "</div>")
                + (ch === null ? (base || !now || !now.offered ? "" : "<div class='sq-d'>New</div>") : "<div class='sq-d " + (ch > 0 ? "up" : ch < 0 ? "down" : "") + "'>" + (ch > 0 ? "+" : "") + ch + "% since " + ayLabel(base.ay) + "</div>")
                + spark(c.ys.slice().reverse().map(function(y){ return y.full && y.offered ? y.enrl : null; }))
                + (now && now.offered ? "<div class='sq-s'>Largest section " + now.maxLec + (base && base.ay !== now.ay && base.maxLec !== now.maxLec ? " <span>(was " + base.maxLec + ")</span>" : "") + "</div>" : "") + "</div>";
        });
        const totNow = latestIdx === -1 ? 0 : cols.reduce(function(n, c){ return n + c.ys[latestIdx].enrl; }, 0);
        const baseIdx = (function(){ for(let i = years.length - 1; i > latestIdx; i--) if(cols.every(function(c){ return c.ys[i].full; }) && cols.some(function(c){ return c.ys[i].offered; })) return i; return -1; })();
        const totThen = baseIdx === -1 ? 0 : cols.reduce(function(n, c){ return n + c.ys[baseIdx].enrl; }, 0), totCh = baseIdx === -1 ? null : pctChange(totNow, totThen);
        const total = "<div class='sq-tile sq-total'><div class='sq-c'>All " + cols.length + " courses</div><div class='sq-t'>" + (latestIdx === -1 ? "" : ayLabel(years[latestIdx])) + "</div><div class='sq-n'><b>" + fmtN(totNow) + "</b> students</div>"
            + (totCh === null ? "" : "<div class='sq-d " + (totCh > 0 ? "up" : totCh < 0 ? "down" : "") + "'>" + (totCh > 0 ? "+" : "") + totCh + "% since " + ayLabel(years[baseIdx]) + "</div>")
            + spark(years.slice().reverse().map(function(ay, j){ const i = years.length - 1 - j; return cols.every(function(c){ return c.ys[i].full; }) ? cols.reduce(function(n, c){ return n + c.ys[i].enrl; }, 0) : null; })) + "</div>";
        const strip = "<div class='sq-strip'>" + tiles.join(cur.flow ? "<span class='sq-arrow' aria-hidden='true'>→</span>" : "") + "<span class='sq-gap'></span>" + total + "</div>";
        /* The grid: a row per academic year, a column per course, shaded against that course's own ten years. */
        const maxOf = cols.map(function(c){ return Math.max.apply(null, c.ys.map(function(y){ return y.enrl; }).concat([1])); });
            const cell = function(y, i){
            if(y.loading && !y.offered) return "<td class='pv-cell pv-na'>Loading…</td>";
            if(!y.offered) return "<td class='pv-cell pv-na'>" + (y.qs.every(function(c){ return c.state === "future"; }) ? "Not published yet" : "Not offered") + "</td>";
            const tip = y.qs.map(function(c, k){ const q = qOfYear(YEAR_QTRS[k], y.ay);
                return quarterName(q) + ": " + (c.state === "ok" ? fmtN(c.enrl) + " enrolled of " + fmtN(c.lim) + " seats, " + plural(c.sections, "section") + ", largest " + c.maxLec + (c.quizzes ? "; " + plural(c.quizzes, "quiz section") + ", up to " + c.maxQuiz : "") + (c.from !== cols[i].num ? " (as " + cur.prefix + " " + c.from + ")" : "")
                    : c.state === "future" ? "not published yet" : c.state === "loading" ? "loading" : "not offered"); }).join("\n");
            return "<td class='pv-cell sq-cell' title='" + snapEsc(tip) + "' style='background:rgba(75,46,131," + (0.03 + 0.2 * y.enrl / maxOf[i]).toFixed(3) + ")'><div class='pc-big'><b>" + fmtN(y.enrl) + "</b> students</div>"
                + "<div class='sq-q'>" + y.qs.map(function(c){ return c.state === "ok" ? fmtN(c.enrl) : "–"; }).join(" · ") + "</div>"
                + "<div class='sq-q'>max " + y.maxLec + (y.maxQuiz ? " · quiz " + y.maxQuiz : "") + "</div>" + (y.from ? "<div class='sq-as'>as " + snapEsc(cur.prefix + " " + y.from) + "</div>" : "") + "</td>";
        };
        let body = "";
        years.forEach(function(ay, r){
            const parts = Math.max.apply(null, cols.map(function(c){ return c.ys[r].qs.filter(function(q){ return q.state === "ok"; }).length; }));
            const sum = cols.reduce(function(n, c){ return n + c.ys[r].enrl; }, 0), anyLoading = cols.some(function(c){ return c.ys[r].loading; });
            body += "<tr><th class='pv-yr' data-year='" + ay + "' title='Open " + ayLabel(ay) + " in Year'>" + ayLabel(ay) + (parts && parts < 3 && cols.some(function(c){ return c.ys[r].qs.some(function(q){ return q.state === "future"; }); }) ? "<span>" + parts + " of 3 quarters</span>" : "") + "</th>"
                + cols.map(function(c, i){ return cell(c.ys[r], i); }).join("")
                + (anyLoading && !sum ? "<td class='pv-cell pv-na'>Loading…</td>" : "<td class='pv-cell sq-cell'><div class='pc-big'><b>" + fmtN(sum) + "</b> students</div></td>") + "</tr>";
        });
        $("#period-view").html(seqChips(lists, cur)
            + "<div class='pv-head'><span class='pv-hint'>" + snapEsc((cur.note ? cur.note + ". " : "") + (cur.kind === "built-in" ? "From " + cur.source + "." : cur.kind === "found" ? "" : "") + " The tiles compare the latest full year with the oldest shown. Lecture sections’ students, as the Time Schedule shows them; summer left out.") + "</span></div>"
            + strip
            + "<table class='pv-table sq-table'><thead><tr><th>Academic year<span>Students in the year, then Aut · Win · Spr; the largest lecture and quiz section</span></th>" + cols.map(function(c){ const nm = (c.ys.filter(function(y){ return y.name; })[0] || {}).name || "";
                return "<th title='" + snapEsc(titleCase(nm)) + "'>" + snapEsc(cur.prefix + " " + c.num) + "<span>" + snapEsc(titleCase(nm)) + "</span></th>"; }).join("") + "<th class='pv-tot'>" + (cur.flow ? "Sequence" : "All") + "</th></tr></thead><tbody>" + body + "</tbody></table>");
    }
    function seqChips(lists, cur){
        const many = activePrefixes.length > 1;
        return "<div class='sq-chips' role='group' aria-label='Sequences'>" + lists.map(function(l){
            return "<button type='button' class='sq-chip" + (cur && l.id === cur.id ? " on" : "") + (l.kind === "found" ? " found" : l.kind === "mine" ? " mine" : "") + "' data-seq='" + snapEsc(l.id) + "' aria-pressed='" + String(!!(cur && l.id === cur.id)) + "' title='"
                + snapEsc((l.note || "") + (l.kind === "found" ? " (found automatically)" : "")) + "'>" + snapEsc((many ? l.prefix + " · " : "") + l.name) + "</button>"
                + (l.kind === "mine" && !SNAPSHOT ? "<button type='button' class='sq-del' data-del='" + l.index + "' data-p='" + snapEsc(l.prefix) + "' title='Remove " + snapEsc(l.name) + "' aria-label='Remove " + snapEsc(l.name) + "'>×</button>" : "");
        }).join("") + (SNAPSHOT ? "" : "<button type='button' class='sq-chip sq-add' aria-expanded='false'>+ Add a sequence</button>") + "</div>"
            + (SNAPSHOT ? "" : "<form class='sq-form' hidden><input id='sq-name' placeholder='Name (e.g. Logic)' aria-label='Name'><input id='sq-courses' size='34' placeholder='Courses in order, e.g. " + snapEsc((activePrefixes[0] || "PHIL") + " 120, 470") + "' aria-label='Courses in order'>"
                + "<button type='submit' class='sq-chip on'>Save</button><button type='button' class='sq-chip sq-cancel'>Cancel</button><span class='sq-err'></span></form>");
    }
    $(document).on("click", ".sq-chip[data-seq]", function(){ pvSeq = $(this).attr("data-seq"); drawSequences(); });
    $(document).on("click", ".sq-add", function(){ $(".sq-form").prop("hidden", false); $(this).attr("aria-expanded", "true"); $("#sq-courses").focus(); });
    $(document).on("click", ".sq-cancel", function(){ $(".sq-form").prop("hidden", true); $(".sq-add").attr("aria-expanded", "false"); });
    $(document).on("click", ".sq-del", function(){
        const p = $(this).attr("data-p"), i = +$(this).attr("data-del");
        (customSeqs[p] || []).splice(i, 1);
        saveSeqs();
        pvSeq = null;
        drawSequences();
    });
    $(document).on("submit", ".sq-form", function(e){
        e.preventDefault();
        let p = activePrefixes[0];
        const nums = [];
        String($("#sq-courses").val() || "").toUpperCase().split(/[\s,;→>]+/).forEach(function(t){
            if(/^\d{3}$/.test(t)) nums.push(t);
            else if(activePrefixes.indexOf(t) !== -1 && !nums.length) p = t;
        });
        if(nums.length < 1){ $(".sq-err").text("Type course numbers in order, e.g. " + p + " 120, 470"); return; }
        (customSeqs[p] = customSeqs[p] || []).push({ name: String($("#sq-name").val() || "").trim() || p + " " + nums.join("–"), courses: nums });
        saveSeqs();
        pvSeq = p + ":mine:" + (customSeqs[p].length - 1);
        drawSequences();
    });
    /* ---- Reading the other quarters in the background ----
       Once a prefix is loaded, every page these views and the time series use is read in the background, three at a time,
       newest academic years first: the last ten academic years, the last ten summers, and Time Series' 40 quarters (one
       shared cache). The progress bar shows only when the view on screen needs pages not read yet. A saved snapshot never
       fetches.
       So that it never makes the page lag (Oct 2026: the user saw jerky scrolling): it starts a couple of seconds after the
       dashboard last redrew, reads two pages at a time, reads each page only when the browser is idle and nobody has
       scrolled or typed for 400 ms, and a view redraws once, when all its pages are in. */
    const bgQueued = {};
    const bg = { queue: [], total: 0, done: 0, running: 0 };
    function wantedQuarters(){
        const ids = [];
        for(let ay = NEWEST_AY; ay > NEWEST_AY - 10; ay--) YEAR_QTRS.forEach(function(q){ ids.push(qOfYear(q, ay)); });
        for(let y = NEWEST_SUMMER; y > NEWEST_SUMMER - 10; y--) ids.push("SUM" + y);
        histQuarters.slice().reverse().forEach(function(hq){ ids.push(hq.str); });
        return ids.filter(function(id, i){ return id !== currQuarterId && ids.indexOf(id) === i; });
    }
    function tsQuarterIds(){ return histQuarters.filter(inTsMode).map(function(hq){ return hq.str; }); }
    /* The quarters the view on screen needs. */
    function neededQuarters(){
        const ids = [];
        if(viewMode === "year") YEAR_QTRS.forEach(function(q){ ids.push(qOfYear(q, pvYear)); });
        if(viewMode === "decade" || viewMode === "sequences") for(let ay = NEWEST_AY; ay > NEWEST_AY - 10; ay--) YEAR_QTRS.forEach(function(q){ ids.push(qOfYear(q, ay)); });
        if(viewMode === "summers") for(let y = NEWEST_SUMMER; y > NEWEST_SUMMER - 10; y--) ids.push("SUM" + y);
        if(isSeriesView()) return tsQuarterIds();
        return ids;
    }
    function missingFor(ids){
        const out = [];
        ids.forEach(function(id){ if(id === currQuarterId) return; activePrefixes.forEach(function(p){ if(!((id + "_" + p) in tsDataCache)) out.push(id + "_" + p); }); });
        return out;
    }
    function startBackground(){
        if(SNAPSHOT) return;
        wantedQuarters().forEach(function(id){
            activePrefixes.forEach(function(p){
                const key = id + "_" + p;
                if(key in tsDataCache || bgQueued[key]) return;
                bgQueued[key] = true;
                bg.queue.push({ id: id, p: p, key: key });
                bg.total++;
            });
        });
        while(bg.running < 2 && bg.queue.length) runBackground();
    }
    let bgTimer = null, lastActivity = 0;
    ["scroll", "wheel", "touchmove", "keydown", "mousedown"].forEach(function(ev){ window.addEventListener(ev, function(){ lastActivity = Date.now(); }, { passive: true, capture: true }); });
    function scheduleBackground(){ if(SNAPSHOT) return; clearTimeout(bgTimer); bgTimer = setTimeout(startBackground, 2000); }
    function whenCalm(){
        return new Promise(function(done){
            (function wait(){
                const quiet = Date.now() - lastActivity;
                if(quiet < 400) return setTimeout(wait, 410 - quiet);
                if(window.requestIdleCallback) requestIdleCallback(function(){ done(); }, { timeout: 1500 }); else setTimeout(done, 0);
            })();
        });
    }
    async function runBackground(){
        bg.running++;
        while(bg.queue.length){
            const t = bg.queue.shift();
            if(!(t.key in tsDataCache)){
                try {
                    const res = await fetch("https://www.washington.edu/students/timeschd/" + t.id + "/" + prefixLookup[t.p]);
                    const html = res.ok ? await res.text() : null;
                    await whenCalm();
                    if(html !== null && !(t.key in tsDataCache)) storeHistoryPage(t.key, html); else if(!(t.key in tsDataCache)){ tsDataCache[t.key] = []; tsQuizCache[t.key] = []; }
                } catch(e){ tsDataCache[t.key] = []; tsQuizCache[t.key] = []; }
            }
            bg.done++;
            afterBackgroundPage();
        }
        bg.running--;
    }
    /* After each page: the progress bar, if the view on screen is waiting; and that view, once it has what it needs. */
    let needsWereMet = true;
    function afterBackgroundPage(){
        const waiting = missingFor(neededQuarters()).length;
        if(waiting) showProgress(); else $("#bg-progress").hide();
        if(!waiting && !needsWereMet){ if(isPeriodView()) drawPeriod(); if(isSeriesView()) seriesReady(); }
        needsWereMet = !waiting;
    }
    function showProgress(){
        $("#bg-progress").css("display", "flex").find(".pv-fill").css("width", (bg.total ? bg.done / bg.total * 100 : 0) + "%");
        $("#bg-status").text("Reading the last ten years from the Time Schedule: " + bg.done + " of " + bg.total + " pages");
    }
    function renderPeriod(){
        const waiting = !SNAPSHOT && missingFor(neededQuarters()).length > 0;
        needsWereMet = !waiting;
        if(waiting){ startBackground(); showProgress(); } else $("#bg-progress").hide();
        if(isPeriodView()) drawPeriod();
        if(isSeriesView()){ if(waiting) $("#ts-course-select").prop("disabled", true); else seriesReady(); }
    }

    /* ---- AY and summer time series ----
       Ben's Time Series, in two modes: the academic year's quarters only (summer left out), and summers only. The course
       picker lists every course offered in the loaded prefixes over those quarters, whole courses only (the instructor
       checkboxes follow one instructor), with when it was last taught if that wasn't the latest quarter. Courses excluded
       everywhere aren't listed. */
    function isSeriesView(){ return viewMode === "ayseries" || viewMode === "sumseries"; }
    function inTsMode(hq){ return tsMode === "summer" ? hq.q === "SUM" : hq.q !== "SUM"; }
    /* Ben's plot and instructor list walk histQuarters; for each call it holds only this mode's quarters. */
    function withTsQuarters(fn){
        return function(){
            const all = histQuarters.slice();
            histQuarters.length = 0;
            Array.prototype.push.apply(histQuarters, all.filter(inTsMode));
            try { return fn.apply(this, arguments); }
            finally { histQuarters.length = 0; Array.prototype.push.apply(histQuarters, all); }
        };
    }
    plotTimeSeries = withTsQuarters(plotTimeSeries);
    renderTsInstructorFilters = withTsQuarters(renderTsInstructorFilters);
    loadTimeSeriesData = withTsQuarters(loadTimeSeriesData);   /* its list of pages to fetch is made before its first wait */
    function seriesReady(){
        const sel = $("#ts-course-select");
        sel.prop("disabled", false);
        if(!sel.data("select2")) return;
        const courses = {};
        let newest = -1;
        histQuarters.filter(inTsMode).forEach(function(hq){
            activePrefixes.forEach(function(p){
                const rows = hq.str === currQuarterId ? rawData.filter(function(d){ return d.prefix === p; }) : (tsDataCache[hq.str + "_" + p] || []).filter(function(d){ return d.prefix === p; });
                rows.forEach(function(d){
                    const k = d.prefix + "|" + d.number, idx = qIndex(hq.str), c = courses[k] || (courses[k] = { p: d.prefix, n: d.number, name: d.name, last: -1, lastId: "" });
                    if(idx >= c.last){ c.last = idx; c.lastId = hq.str; c.name = d.name; }
                    if(idx > newest) newest = idx;
                });
            });
        });
        const keys = Object.keys(courses).filter(function(k){ return excludedCourses.indexOf(k.replace("|", " ")) === -1; }).sort(function(a, b){ return a.localeCompare(b, "en", { numeric: true }); });
        const kept = (sel.val() || []).filter(function(v){ return keys.indexOf(v) !== -1; });
        sel.empty().append(keys.map(function(k){
            const c = courses[k], when = c.last < newest ? " · last taught " + c.lastId.slice(0, 1) + c.lastId.slice(1, 3).toLowerCase() + " " + c.lastId.slice(3) : "";
            return $("<option></option>").val(k).text(c.p + " " + c.n + " - " + c.name + when);
        }));
        sel.val(kept).trigger("change");
    }
    /* The Year button shows the year on screen, with a caret: clicked again, it opens a menu of the ten years. */
    function updateYearChip(){
        const b = $(".view-seg [data-view=year]");
        if(viewMode === "year") b.html(snapEsc(ayLabel(pvYear)) + "<span class='caret' aria-hidden='true'>▾</span>").attr({ "aria-haspopup": "menu", title: "Autumn, Winter and Spring of " + ayLabel(pvYear) + ". Click to pick another academic year." });
        else b.text("Year").removeAttr("aria-haspopup").attr("title", "Autumn, Winter and Spring of one academic year");
    }
    function closeYearMenu(){ $("#pv-yearmenu").remove(); $(".view-seg [data-view=year]").attr("aria-expanded", "false"); }
    function openYearMenu(){
        closeYearMenu();
        const b = $(".view-seg [data-view=year]"), r = b[0].getBoundingClientRect();
        let items = "";
        for(let ay = NEWEST_AY; ay > NEWEST_AY - 10; ay--) items += "<button type='button' role='menuitemradio' aria-checked='" + (ay === pvYear) + "' data-year='" + ay + "'" + (ay === pvYear ? " class='on'" : "") + ">" + ayLabel(ay) + "</button>";
        $("<div id='pv-yearmenu' class='pv-yearmenu' role='menu' aria-label='Academic year'></div>").html(items).css({ top: r.bottom + 6, left: r.left }).appendTo("body");
        b.attr("aria-expanded", "true");
        $("#pv-yearmenu .on").focus();
    }
    $(document).on("click", "#pv-yearmenu [data-year]", function(){ pvYear = +$(this).attr("data-year"); pvFocus = null; closeYearMenu(); updateYearChip(); renderPeriod(); });
    $(document).on("pointerdown", function(e){ if($("#pv-yearmenu").length && !$(e.target).closest("#pv-yearmenu, .view-seg [data-view=year]").length) closeYearMenu(); });
    $(document).on("keydown", function(e){
        const menu = $("#pv-yearmenu");
        if(!menu.length) return;
        if(e.key === "Escape"){ closeYearMenu(); $(".view-seg [data-view=year]").focus(); }
        if(e.key === "ArrowDown" || e.key === "ArrowUp"){ e.preventDefault(); const items = menu.find("button"), i = items.index(document.activeElement); items.eq(Math.max(0, Math.min(items.length - 1, i + (e.key === "ArrowDown" ? 1 : -1)))).focus(); }
    });
    function setView(v){
        viewMode = v;
        closeYearMenu();
        $(".view-seg button").each(function(){ const on = $(this).attr("data-view") === v; $(this).toggleClass("on", on).attr("aria-pressed", String(on)); });
        updateYearChip();
        const series = isSeriesView();
        if(series) tsMode = v === "sumseries" ? "summer" : "ay";
        if($("#ts-toggle").is(":checked") !== series) $("#ts-toggle").prop("checked", series).trigger("change");
        document.body.classList.toggle("pv-on", isPeriodView());
        renderPeriod();
    }
    $(document).on("click", ".view-seg button", function(){
        const v = $(this).attr("data-view");
        if(v === "year" && viewMode === "year") return $("#pv-yearmenu").length ? closeYearMenu() : openYearMenu();
        setView(v);
    });
    $(document).on("click", ".pv-table [data-year]", function(){ pvYear = +$(this).attr("data-year"); pvFocus = $(this).attr("data-q") || null; pvScrollOnce = true; setView("year"); });
    $(document).on("click", ".pv-stable [data-summer]", function(){ pvSummer = +$(this).attr("data-summer"); drawSummers(); });
    /* Every redraw of the Quarter view also refreshes the Excluded bar and, when one is showing, the other views. */
    const benRenderDashboard = renderDashboard;
    renderDashboard = function(opts){ applyCourseExclusions(); benRenderDashboard(opts); renderExclBar(); scheduleBackground(); if(isPeriodView() || isSeriesView()) renderPeriod(); };
"""

insert('(async function(){\n', START, where='after')
# Parser: quiz sections were skipped; keep them apart (for the TA estimate) instead.
insert('function parseUWTimeSchedule(html){', 'function parseUWTimeSchedule(html, withQuiz){', replace=True)
insert('const results = [];', 'const results = []; results.quiz = [];', replace=True)
insert('if(line.includes("QZ")) continue;', 'const isQuiz = line.includes("QZ");\n                if(isQuiz && !withQuiz) continue;', replace=True)
insert('const added = parseUWTimeSchedule(await res.text());', 'const added = parseUWTimeSchedule(await res.text(), true);', replace=True)
insert('results.push({', 'if(isQuiz){ results.quiz.push({ sln: sln, prefix: currentCourse.prefix, number: currentCourse.number, section: section, instructor: instructor, enrl: enrl, lim: lim }); continue; }\n                ')
insert('let rawData = [];', '\n    let quizData = [];\n    const fetchedAt = {};', where='after')
insert('rawData = rawData.concat(added);', 'added.forEach(function(d){ d.src = p; });\n                added.quiz.forEach(function(d){ d.src = p; });\n                labelQuizLeaders(added, added.quiz);\n                quizData = quizData.concat(added.quiz);\n                fetchedAt[p] = pageTime(p);\n                ')
# Header: data time and the Save snapshot button, left of the Current / Time Series switch.
# TSMod's own message box instead of Ben's alerts, as in MyGradMod: shown inside the page, headed so a first-time user knows
# the bookmarklet is installed and working, with the steps (and a button to the Time Schedule). A browser can silence alerts.
insert('javascript:!function(){', r"""function tsmNotice(m,k){var o=document.getElementById("tsmod-notice");o&&o.remove();var s=document.createElement("div");s.id="tsmod-notice";s.style.cssText="position:fixed;inset:0;z-index:2147483647;background:rgba(30,16,60,.28);display:flex;justify-content:center;align-items:flex-start;padding-top:32vh";s.innerHTML="<div role='alertdialog' aria-labelledby='tsmod-notice-head' style='width:min(440px,calc(100vw - 40px));background:#fff;border-radius:10px;box-shadow:0 12px 40px rgba(0,0,0,.35);overflow:hidden;font:15px/1.45 -apple-system,BlinkMacSystemFont,Segoe UI,Roboto,sans-serif;color:#222;text-align:left'><div id='tsmod-notice-head' style='background:#4b2e83;color:#fff;font-size:12px;font-weight:600;letter-spacing:.04em;padding:8px 16px'>TimeScheduleMod successfully installed</div><div class='msg' style='padding:16px 18px 4px'></div><div style='padding:10px 18px 16px;display:flex;justify-content:flex-end;align-items:center;gap:10px'><a class='go' style='display:none;color:#4b2e83;border:1px solid #4b2e83;border-radius:16px;padding:5px 16px;font-weight:600;text-decoration:none'></a><button type='button' style='background:#4b2e83;color:#fff;border:0;border-radius:16px;padding:6px 20px;font:inherit;font-weight:600;cursor:pointer'>OK</button></div></div>";s.querySelector(".msg").textContent=m;if(k){var a=s.querySelector(".go");a.href=k.href;a.textContent=k.label;a.style.display="inline-block"}var y=function(e){"Escape"!==e.key&&"Enter"!==e.key||(e.preventDefault(),c())},c=function(){s.remove(),document.removeEventListener("keydown",y,!0)};s.addEventListener("click",function(e){e.target!==s&&"BUTTON"!==e.target.tagName||c()});document.addEventListener("keydown",y,!0);document.body.appendChild(s);s.querySelector("button").focus()}""", where='after', raw=True)
insert('if(!e)return void alert("Please click this bookmarklet while on a UW Time Schedule page (e.g., /timeschd/SPR2026/).");',
    r"""if(!e)return void(/\/timeschd\/?(index\.html?)?$/i.test(window.location.pathname)?tsmNotice("Pick a quarter on this page, then click TimeScheduleMod again."):tsmNotice("Open the UW Time Schedule: sign in with your UW NetID, pick any quarter (for example Autumn 2026), then click TimeScheduleMod again.",{href:"https://www.washington.edu/students/timeschd/",label:"Open the Time Schedule"}));""", replace=True, raw=True)
insert('if(!l)return void alert("Popup blocked! Please allow popups for washington.edu to generate the dashboard.");',
    'if(!l)return void tsmNotice("Pop-up blocked! Allow pop-ups for this site, then click TimeScheduleMod again.");', replace=True, raw=True)
# Opened from a department's page (e.g. .../AUT2026/phil.html), the dashboard starts with that department's prefix: the
# bookmarklet passes the page's file name, and each file belongs to exactly one prefix in prefixLookup.
insert('r="https://www.washington.edu/students/timeschd/"+t+"/"', ',o=(window.location.pathname.match(/\\/([^\\/]+\\.html?)$/i)||[])[1]||""', where='after', raw=True)
insert('const currQuarterId = "${t}";', '\\n    const startPage = "${o}";', where='after', raw=True)
# The preset prefix's page is the one TSMod was opened on: if that page loaded in the last 10 minutes, its HTML is used
# instead of fetching it again, and the data's time is when it loaded.
insert('loadedPrefixes.push(p);\n        try {\n            const res = await fetch(baseUrl + prefixLookup[p]);', 'loadedPrefixes.push(p);\n        try {\n            const res = await fetchFirstPage(p);', replace=True)
# Header: the All Departments and CAS Curriculum Policies links go; a row of view buttons replaces the Current / Time
# Series switch (its checkbox stays, hidden, since Ben's code shows and hides Time Series by it); Save snapshot, with the
# data's time inside it, gets a second row.
insert('<div class="dashboard-links"><a href="${r}" target="_blank">All Departments ↗</a><a href="https://admin.artsci.washington.edu/curriculum/curriculum-planning-general-information" target="_blank">CAS Curriculum Policies ↗</a></div>', '', replace=True)
insert('<div class="ts-toggle-container"><span>Current</span><label class="switch"><input type="checkbox" id="ts-toggle"><span class="slider"></span></label><span>Time Series</span></div>',
    '<div class="view-seg" role="group" aria-label="View">'
    + '<button type="button" data-view="quarter" class="on" aria-pressed="true" title="This quarter, section by section">Quarter</button>'
    + '<button type="button" data-view="year" aria-pressed="false" title="Autumn, Winter and Spring of one academic year">Year</button>'
    + '<button type="button" data-view="decade" aria-pressed="false" title="The last ten academic years, quarter by quarter">Decade</button>'
    + '<button type="button" data-view="sequences" aria-pressed="false" title="Course sequences, year by year: built in for MATH, found from course titles elsewhere, or your own">Sequences</button>'
    + '<button type="button" data-view="ayseries" aria-pressed="false" title="Chosen courses over ten years, Autumn, Winter and Spring">AY time series</button>'
    + '<button type="button" data-view="summers" aria-pressed="false" title="The last ten summers">Summers</button>'
    + '<button type="button" data-view="sumseries" aria-pressed="false" title="Chosen courses over the last ten summers">Summer time series</button>'
    + '<input type="checkbox" id="ts-toggle" hidden></div>'
    + '<div class="snap-tools"><button type="button" id="snap-save" class="snap-btn" disabled title="Load a prefix first">' + ICON + 'Save snapshot<span id="snap-asof" class="snap-asof"></span></button></div>', replace=True)
# Ben's section-row pattern, ^(?:[A-Za-z]+\s*)*..., can split a run of letters in exponentially many ways, so a long line
# of plain text (a course note: MATH's pages have them) froze the page with no error (Oct 2026). Each word now has to be
# taken whole; it matches the same lines.
insert(r"line.match(/^(?:[A-Za-z]+\\s*)*>?", r"line.match(/^(?:[A-Za-z]+(?![A-Za-z])\\s*)*>?", replace=True, raw=True)
insert('<div id="active-prefix-chips"></div>', '<div id="excl-bar" class="excl-bar" style="display:none"></div>', where='after')
insert('<div class="stats-row">', '<div id="period-view"></div>')
insert('<div id="current-quarter-view">', '<div id="bg-progress"><div class="pv-bar"><div class="pv-fill"></div></div><span id="bg-status"></span></div>')
# Time series: whole courses only (see seriesReady), and full-size summer points in the summer time series.
insert('pref + " " + num + " (all sections)"', 'pref + " " + num', replace=True)
insert('placeholder: "Select courses or sections to compare...",', 'placeholder: "Select courses to compare...",', replace=True)
insert('if(hq.q === "SUM")', 'if(hq.q === "SUM" && tsMode !== "summer")', replace=True)
# Parser: a section's "to be arranged" meeting and variable credits, the signs of independent study.
insert('const section = slnMatch[2];', r'''
                const credTok = (line.slice(line.indexOf(slnMatch[0]) + slnMatch[0].length).trim().split(/\s+/)[0] || "");
                const tba = /to be arranged/i.test(line), varCredits = /^(VAR|\d+-\d*)$/i.test(credTok);''', where='after')
insert('pct: lim > 0 ? (enrl / lim) * 100 : 0', ', tba: tba, varCredits: varCredits', where='after')
# A "to be arranged" meeting can run into the instructor's name ("to be arranged Smith,Ann"); keep just the name.
insert(r'instructor = instructor.replace(/\\s+(Open|Closed|Restr|Full-term)$/ig, "").trim();', r'''
                instructor = instructor.replace(/^to be arranged\s*/i, "") || "TBA";''', where='after')
# Time Series keeps each page's quiz rows too, for the TA estimate in the other views.
insert('tsDataCache[task.key] = parseUWTimeSchedule(await res.text());', 'storeHistoryPage(task.key, await res.text());', replace=True)
# Before Ben's own handler: a section checkbox can exclude or bring back its whole course (see excludedCourses).
insert('$("#course-table").on("change", ".sec-toggle"', r'''$("#course-table").on("change", ".sec-toggle", function(){
        const key = $(this).attr("data-key"), d = rawData.filter(function(x){ return sectionKey(x) === key; })[0];
        if(!d) return;
        const ck = courseKey(d);
        if(this.checked){ if(excludedCourses.indexOf(ck) !== -1){ excludedCourses = excludedCourses.filter(function(x){ return x !== ck; }); saveExcludedCourses(); } return; }
        const others = rawData.filter(function(x){ return courseKey(x) === ck && sectionKey(x) !== key; });
        if(excludedCourses.indexOf(ck) === -1 && others.every(function(x){ return excludedSections.indexOf(sectionKey(x)) !== -1; })){ excludedCourses.push(ck); saveExcludedCourses(); }
    });
    ''')
# A fifth card: TAs, estimated.
insert('<div class="stat-card"><h3>Fullness</h3><div class="value" id="stat-pct">0%</div></div>', '<div class="stat-card" id="ta-card"><h3><span class="nc">TAs</span> <span class="est">(est.)</span></h3><div class="value" id="stat-ta">0</div><div class="stat-sub" id="stat-ta-sub"></div><button type="button" id="ta-open" class="ta-open" title="Every quiz section, and how the estimate adds up">By course</button></div>', where='after')
insert('$("#stat-pct").text(totalLim > 0 ? ((totalEnrl / totalLim) * 100).toFixed(1) + "%" : "0%");', '\n        renderTaCard(filteredData);\n        updateAsOf();', where='after')
# The Enrollment Summary's numbers (Oct 2026): a Denied requests card after the TA card, drawn with it, and Get them.
insert('title="Every quiz section, and how the estimate adds up">By course</button></div>', '<div class="stat-card" id="denied-card"><h3>Denied requests</h3><div class="value" id="stat-denied">–</div><div class="stat-sub" id="stat-denied-sub"></div><button type="button" id="dn-get" class="dn-get">Get them</button></div>', where='after')
insert('renderTaCard(filteredData);', '\n        renderDeniedCard(filteredData);', where='after')
insert('window.addEventListener("resize"', '$("#dn-get").on("click", openSummary);\n    ')
# On the Enrollment Summary itself, the bookmarklet reads the page and the same page for the quarters and prefixes the
# dashboard asked for (in the address after #tsmod=), and posts them to the dashboard that opened the tab.
insert('s.querySelector("button").focus()}', r"""function tsmSummaryRows(h){var d=new DOMParser().parseFromString(h,"text/html"),t=[].filter.call(d.querySelectorAll("table"),function(x){return/Denied\s*Requests/i.test(x.textContent)})[0],o={};if(!t)return null;[].forEach.call(t.querySelectorAll("tr"),function(r){var c=[].map.call(r.querySelectorAll("td"),function(x){return x.textContent.replace(/\s+/g," ").trim()}),L=c.length,n=function(v){v=parseInt(v,10);return isNaN(v)?0:v};if(L<8||!/^\d{4,5}$/.test(c[0]))return;o[c[0]]=[n(c[L-4]),n(c[L-2]),/withdrawn/i.test(c[L-1])?1:0]});return o}function tsmSummary(){var q=null,w=window.opener;try{q=JSON.parse(decodeURIComponent((location.hash.match(/#tsmod=(.+)$/)||[])[1]||""))}catch(x){}if(!q||!q.p||!q.q||!q.o||!/^https:\/\/([a-z0-9-]+\.)*(washington|uw)\.edu$|^http:\/\/(127\.0\.0\.1|localhost)(:\d+)?$/.test(q.o))return void tsmNotice("This is the Time Schedule's Enrollment Summary. To add its denied requests and room sizes to TimeScheduleMod, click Get them on the dashboard's Denied requests card, then click TimeScheduleMod on the tab it opens.");if(!w||w.closed)return void tsmNotice("This tab lost its link to the TimeScheduleMod dashboard (signing in can do that). Close it, click Get them on the dashboard again, then click TimeScheduleMod on the new tab.");var j=[],g=[],k=0;q.p.forEach(function(p){q.q.forEach(function(r){/^[A-Z]{3}\d{4}$/.test(r)&&j.push({p:String(p),q:r})})});var u=function(){var m=document.querySelector("#tsmod-notice .msg");m&&(m.textContent="Reading the Enrollment Summary: "+k+" of "+j.length+" pages…")};tsmNotice("Reading the Enrollment Summary…");u();var f=function(){if(!j.length)return Promise.resolve();var a=j.shift();return fetch(location.pathname+"?QTRYR="+a.q.slice(0,3)+"+"+a.q.slice(3)+"&CURRIC="+encodeURIComponent(a.p).replace(/%20/g,"+"),{credentials:"include"}).then(function(r){return r.ok?r.text():""}).then(function(h){var o=h?tsmSummaryRows(h):null;o&&g.push({q:a.q,prefix:a.p,at:(new Date).toISOString(),secs:o})},function(){}).then(function(){k++,u()}).then(f)};Promise.all([f(),f(),f()]).then(function(){try{w.postMessage({type:"tsmod-enrollment-summary",pages:g},q.o),tsmNotice("Sent "+g.length+" pages of the Enrollment Summary to TimeScheduleMod. You can close this tab.")}catch(x){tsmNotice("Couldn't reach the TimeScheduleMod dashboard. Is it still open?")}})}if(/\/timeschd\/uwnetid\/tsstat\.asp/i.test(window.location.pathname))return void tsmSummary();""", where='after', raw=True)
insert('</style>', CSS.replace('\n', ''))
insert('<h1>UW Time Schedule Analytics</h1>', '<h1>TimeScheduleMod</h1>', replace=True)
# The first card counts the sections still checked after every filter; "Filtered Sections" read as the ones filtered out.
insert('<h3>Filtered Sections</h3>', '<h3 title="Lecture sections counted: checked, and matching the Gen Ed, level and instructor filters">Sections counted</h3>', replace=True)
insert('UW Time Schedule Dashboard</title>', 'TimeScheduleMod</title>', replace=True)
# % Full: drawn dots instead of emoji, so over-capacity sections can be a darker green (there is no dark green circle emoji).
insert('''let emoji = (data >= 75 && data <= 100) ? "🟢" : (data > 100 || (data >= 50 && data < 75)) ? "🟠" : "🔴";
                            return emoji + " " + data.toFixed(1) + "%";''', '''const band = data > 100 ? ["over", "Over capacity"] : data >= 75 ? ["full", "75–100% full"] : data >= 50 ? ["mid", "50–75% full"] : ["low", "Under 50% full"];
                            return (type === "display" ? "<span class='fill-dot " + band[0] + "' title='" + band[1] + "'></span>" : "") + data.toFixed(1) + "%";''', replace=True)
insert('let isFetchingTS = false;', FUNCTIONS + PERIOD + '    ')
insert('renderDashboard();\n    renderChips();\n', 'if(SNAPSHOT) applySnapshot();\n    ')
insert('window.addEventListener("resize"', '$("#snap-save").on("click", openSaveDialog);\n    $("#ta-open").on("click", openTaBreakdown);\n    if(SNAPSHOT) applySnapshotAfter();\n    ')
insert('window.addEventListener("resize"', r'''const startPrefix = Object.keys(prefixLookup).filter(function(p){ return prefixLookup[p].toLowerCase() === startPage.toLowerCase(); })[0];
    if(startPrefix && !SNAPSHOT){ $("#prefix-input").val(startPrefix); parsePrefixInput(); }
    ''')

open(out, 'w', encoding='utf-8').write(s)
print('wrote', out, len(s), 'chars')
