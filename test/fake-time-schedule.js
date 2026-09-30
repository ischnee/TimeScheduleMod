// A made-up PHIL department's Time Schedule page, in the real page's format, for the tests. Every name and number is invented.
// page(quarter, shift) returns the page; shift nudges lecture enrollments so past quarters differ.
const fs = require('fs');
const courses = [
  ['100', 'INTRODUCTION TO PHILOSOPHY', '(A&H/SSc)', [[180, 200], [96, 100]]],
  ['102', 'CONTEMPORARY MORAL PROBLEMS', '(A&H/SSc)', [[141, 150], [48, 60]]],
  ['114', 'PHILOSOPHICAL ISSUES IN THE LAW', '(A&H/SSc)', [[117, 120]]],
  ['115', 'PRACTICAL REASONING', '(SSc)', [[88, 120]]],
  ['118', 'PHILOSOPHY OF RELIGION', '(A&H)', [[55, 60]]],
  ['120', 'INTRODUCTION TO LOGIC', '(NSc)', [[172, 180], [60, 60]]],
  ['160', 'SOME MAJOR FIGURES IN PHILOSOPHY', '(A&H)', [[42, 50]]],
  ['207', 'HISTORY OF MODERN PHILOSOPHY', '(A&H)', [[38, 45]]],
  ['240', 'INTRODUCTION TO ETHICS', '(A&H/SSc)', [[119, 120], [45, 50]]],
  ['241', 'TOPICS IN ETHICS', '(A&H/SSc)', [[30, 40]]],
  ['242', 'INTRODUCTION TO MEDICAL ETHICS', '(A&H/SSc)', [[149, 150]]],
  ['243', 'ENVIRONMENTAL ETHICS', '(A&H/SSc)', [[70, 80]]],
  ['267', 'INTRODUCTION TO PHILOSOPHY OF RELIGION', '(A&H)', [[31, 40]]],
  ['320', 'HISTORY OF ANCIENT PHILOSOPHY', '(A&H)', [[36, 40]]],
  ['322', 'MODERN PHILOSOPHY', '(A&H)', [[24, 40]]],
  ['338', 'PHILOSOPHY OF HUMAN RIGHTS', '(A&H/SSc)', [[40, 40]]],
  ['345', 'MORAL PSYCHOLOGY', '(A&H)', [[33, 30]]],
  ['360', 'INTRODUCTION TO SYMBOLIC LOGIC', '(NSc)', [[33, 40]]],
  ['401', 'PHILOSOPHICAL WRITING', '', [[12, 20]]],
  ['411', 'KANT', '(A&H)', [[18, 25]]],
  ['440', 'TOPICS IN POLITICAL PHILOSOPHY', '(A&H/SSc)', [[22, 25]]],
  ['450', 'EPISTEMOLOGY', '(A&H)', [[16, 25]]],
  ['460', 'PHILOSOPHY OF SCIENCE', '(A&H/NSc)', [[20, 25]]],
];
const names = ['Alpha', 'Beta', 'Gamma', 'Delta', 'Epsilon', 'Zeta', 'Eta', 'Theta', 'Iota', 'Kappa', 'Lambda', 'Mu', 'Nu', 'Xi', 'Omicron', 'Pi'];
// Quiz sections per lecture: [leader, enrolled]. leader is a TA's name, 'STAFF', 'TBA' (no meeting time or name),
// '' (blank) or 'PROF' (the lecture's own instructor). Worked out by hand, all courses: 12 named TAs; usual load 2
// (7 TAs lead 2, 3 lead 3, 1 leads 4, 1 leads 1); 16 sections with students but no TA, 1 of them taken by Kale
// (1 section, in a course where the usual is 2); ≈8 more TAs; 3 empty sections not counted; 47 quiz sections. ≈20 TAs.
const QUIZ = {
  '100 A': [['Aster', 24], ['Aster', 25], ['Birch', 23], ['Birch', 25], ['Cedar', 22], ['Cedar', 24], ['STAFF', 20], ['', 18]],
  '100 B': [['Dahlia', 24], ['Dahlia', 25], ['STAFF', 21], ['PROF', 19]],
  '102 A': [['Elm', 25], ['Elm', 24], ['Elm', 23], ['Fern', 22], ['Fern', 25], ['Fern', 24]],
  '120 A': [['Ginkgo', 25], ['Ginkgo', 24], ['Ginkgo', 23], ['Laurel', 25], ['Laurel', 22], ['Laurel', 21], ['Laurel', 20], ['STAFF', 22], ['STAFF', 12], ['', 9]],
  '240 A': [['Hazel', 25], ['Hazel', 24], ['STAFF', 0], ['STAFF', 0]],
  '242 A': [['Iris', 25], ['Iris', 25], ['Juniper', 24], ['TBA', 23], ['PROF', 22], ['', 0]],
  '115 A': [['Juniper', 22], ['Kale', 21], ['STAFF', 23], ['STAFF', 22]],
  '114 A': [['STAFF', 24], ['STAFF', 24], ['STAFF', 23], ['', 23], ['TBA', 23]],
};
function page(quarter, shift) {
  let sln = 20100, out = `<html><head><title>PHIL ${quarter}</title></head><body><h1>PHILOSOPHY</h1>`;
  courses.forEach(([num, name, gened, secs], ci) => {
    out += `<br><table><tr><td><A NAME=phil${num}>PHIL&nbsp;&nbsp; ${num} </A>&nbsp;<A HREF=/course>${name}</A> ${gened}</td></tr></table>`;
    secs.forEach(([enrl0, lim], si) => {
      const enrl = Math.max(0, Math.min(lim + 5, enrl0 + shift * ((ci + si) % 3 - 1)));
      const sec = String.fromCharCode(65 + si), who = 'Instructor,' + names[(ci * 3 + si) % names.length];
      out += `<table><tr><td><pre><A HREF=/sln>${sln++}</A> ${sec}  5       MWF    1030-1120  SAV  264      ${who.padEnd(20)} Open     ${String(enrl).padStart(3)}/ ${lim}                      ${gened.replace(/[()]/g, '')}</pre></td></tr></table>`;
      (QUIZ[num + ' ' + sec] || []).forEach(([leader, qe], q) => {
        const id = sec + String.fromCharCode(65 + q);
        const meets = leader === 'TBA' ? 'to be arranged           ' : 'TTh    0930-1020  SAV  132';
        const person = leader === 'PROF' ? who : leader === 'STAFF' ? 'STAFF' : leader && leader !== 'TBA' ? 'Assistant,' + leader : '';
        out += `<table><tr><td><pre><A HREF=/sln>${sln++}</A> ${id} QZ      ${meets}      ${person.padEnd(20)} Open      ${String(qe).padStart(2)}/ 25</pre></td></tr></table>`;
      });
    });
  });
  return out + '</body></html>';
}
page.QUIZ = QUIZ; page.courses = courses; page.names = names;
module.exports = page;
