#!/usr/bin/env python3
"""
WellSnax structural fixes. Run from the repo root:  python3 apply_structural_fixes.py .
Edits HTML in place. Every change is logged to fix-log.txt.

Scope: structural defects and answer restorations only.
Nothing here rewrites question wording or invents an answer.
"""
import re, os, sys, glob

REPO = sys.argv[1] if len(sys.argv) > 1 else "."
log = []

def L(msg): log.append(msg); print(msg)

# ---------------------------------------------------------------- 1. orphans
ORPHAN = re.compile(
    r'\s*<div class="quiz-question">\s*'
    r'<p class="q">\d+\.\s*(?:True|False)\s*</p>\s*'
    r'<ul class="options">.*?</ul>\s*</div>',
    re.S)

removed = 0
for path in sorted(glob.glob(os.path.join(REPO, "*.html"))):
    h = open(path, encoding='utf-8').read()
    new, n = ORPHAN.subn("", h)
    if n:
        open(path, 'w', encoding='utf-8').write(new)
        removed += n
        L(f"[orphan]  {os.path.basename(path)}: removed {n} stray option-fragment block(s)")
L(f"[orphan]  TOTAL removed: {removed}")

# ------------------------------------------------- 2. restore missing answers
# Source of truth: Alexis's answer keys, which spell True/False as words for
# these items, so there is no letter-to-position ambiguity.
RESTORE = {
    "hs-2-4.html": {11: "True", 12: "False", 13: "True", 14: "True", 15: "True"},
    "hs-1-2.html": {2: "False", 4: "False", 7: "False", 10: "False", 13: "True"},
}

TF_BLOCK = ('<ul class="options">\n'
            '            <li{a}><span class="letter">A.</span> True{ba}</li>\n'
            '            <li{b}><span class="letter">B.</span> False{bb}</li>\n'
            '          </ul>')
CORRECT = ' class="correct"'
BADGE = ' <span class="correct-badge">Correct</span>'

def build(ans):
    t = ans == "True"
    return TF_BLOCK.format(
        a=CORRECT if t else "", ba=BADGE if t else "",
        b="" if t else CORRECT, bb="" if t else BADGE)

for fname, answers in RESTORE.items():
    path = os.path.join(REPO, fname)
    if not os.path.exists(path):
        L(f"[restore] {fname}: FILE NOT FOUND, skipped"); continue
    h = open(path, encoding='utf-8').read()
    for qn, ans in sorted(answers.items()):
        pat = re.compile(
            r'(<p class="q">' + str(qn) + r'\.\s.*?</p>\s*)<ul class="options">(.*?)</ul>', re.S)
        m = pat.search(h)
        if not m:
            L(f"[restore] {fname} Q{qn}: question block not found, skipped"); continue
        if 'class="correct"' in m.group(2):
            L(f"[restore] {fname} Q{qn}: already has an answer, left alone"); continue
        stem = m.group(1)
        # strip a trailing "True / False" that was absorbed into the stem
        stem_clean = re.sub(r'\s*(True\s*/\s*False|TRUE or FALSE)\s*(</p>)', r'\2', stem)
        h = h[:m.start()] + stem_clean + build(ans) + h[m.end():]
        L(f"[restore] {fname} Q{qn}: answer set to {ans} (from Alexis's key)")
    open(path, 'w', encoding='utf-8').write(h)

# ------------------------------------------------ 3. correct inverted T/F keys
# These nine were reported by Derek and are wrong on the page. Each is a
# plain factual call, not a matter of interpretation. Flagged for sign-off.
INVERT = [
    ("hs-3-2.html", 4,  "True",  "Carbohydrates do help athletes maintain energy during intense exercise"),
    ("hs-3-2.html", 10, "True",  "Balanced macronutrients do help maintain steady energy"),
    ("hs-3-3.html", 11, "True",  "Several low %DV foods can leave daily iron needs unmet"),
    ("hs-4-1.html", 12, "False", "Skipping meals is not recommended by dietary guidelines"),
    ("hs-4-4.html", 11, "True",  "Variety across food groups is the definition of a balanced plate"),
    ("hs-4-6.html", 11, "True",  "Celiac disease requires strict avoidance of wheat, barley and rye"),
    ("hs-6-1.html", 10, "True",  "Adequate protein supports recovery and reduces soreness"),
    ("hs-6-2.html", 7,  "True",  "Low energy availability reduces bone density and raises injury risk"),
    ("hs-6-3.html", 14, "False", "Thirst lags fluid loss, so athletes should not rely on it alone"),
]

for fname, qn, ans, why in INVERT:
    path = os.path.join(REPO, fname)
    if not os.path.exists(path):
        L(f"[invert]  {fname}: FILE NOT FOUND, skipped"); continue
    h = open(path, encoding='utf-8').read()
    pat = re.compile(r'(<p class="q">' + str(qn) + r'\.\s.*?</p>\s*)<ul class="options">(.*?)</ul>', re.S)
    m = pat.search(h)
    if not m:
        L(f"[invert]  {fname} Q{qn}: not found, skipped"); continue
    body = m.group(2)
    if not re.search(r'>\s*True\s*<|>\s*True\b', body) or "False" not in body:
        L(f"[invert]  {fname} Q{qn}: not a true/false item, skipped"); continue
    cur = "True" if re.search(r'class="correct"[^>]*>\s*<span class="letter">[A-Z]\.</span>\s*True', body) else "False"
    if cur == ans:
        L(f"[invert]  {fname} Q{qn}: already {ans}, left alone"); continue
    h = h[:m.start()] + m.group(1) + build(ans) + h[m.end():]
    open(path, 'w', encoding='utf-8').write(h)
    L(f"[invert]  {fname} Q{qn}: {cur} -> {ans}  ({why})  ** REVIEW **")

open(os.path.join(REPO, "fix-log.txt"), "w").write("\n".join(log) + "\n")
print(f"\nDone. {len(log)} actions written to fix-log.txt")
