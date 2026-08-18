#!/usr/bin/env python3
"""
WellSnax curriculum quiz validator.

Usage:  python3 validate_quizzes.py [path-to-repo]   (default: current directory)
Exit code 0 = clean, 1 = defects found. Safe for CI / pre-push.

Checks structural faults only. It cannot tell you whether an answer is
scientifically correct, it tells you whether the page is internally coherent.
"""
import re, sys, glob, os
from collections import defaultdict

TAG = re.compile(r'<.*?>')
def txt(s): return re.sub(r'\s+', ' ', TAG.sub('', s)).strip()

def parse(path):
    h = open(path, encoding='utf-8').read()
    out = []
    for blk in re.findall(r'<div class="quiz-question">(.*?)</ul>', h, re.S):
        qm = re.search(r'<p class="q">(.*?)</p>', blk, re.S)
        if not qm:
            continue
        opts = []
        for li in re.findall(r'<li\b(.*?)</li>', blk, re.S):
            lm = re.search(r'<span class="letter">([A-Z])\.</span>(.*)$', li, re.S)
            if not lm:
                continue
            is_correct = 'class="correct"' in li.split('>', 1)[0]
            opts.append((is_correct, lm.group(1), txt(lm.group(2)).replace(' Correct', '')))
        out.append({"q": txt(qm.group(1)), "opts": opts})
    return out

def num(q):
    m = re.match(r'^(\d+)[.)]', q)
    return int(m.group(1)) if m else None

def check(path):
    d = []
    def bad(rule, q, msg): d.append((os.path.basename(path), rule, q[:70], msg))
    qs = parse(path)
    if not qs:
        return d
    seen_nums = []
    for i, item in enumerate(qs):
        q, opts = item["q"], item["opts"]
        labels = [o[2] for o in opts]
        letters = [o[1] for o in opts]
        n_correct = sum(1 for o in opts if o[0])
        is_tf = set(labels) == {"True", "False"}
        orphan = bool(re.match(r'^\d+[.)]\s*(True|False)\s*$', q)) or (len(opts) == 1 and len(q) < 30)

        # R1 exactly one correct answer
        if not orphan and n_correct != 1:
            bad("R1-answer-count", q, f"{n_correct} options marked correct, expected 1")
        # R2 orphan / fragment blocks
        if orphan:
            bad("R2-orphan-block", q, f"question text looks like an option fragment; opts={labels}")
        # R3 option count
        if not orphan:
            if len(opts) == 0:
                bad("R3-no-options", q, "option list is empty")
            elif is_tf and len(opts) != 2:
                bad("R3-option-count", q, f"true/false item has {len(opts)} options")
            elif not is_tf and len(opts) != 4:
                bad("R3-option-count", q, f"multiple choice item has {len(opts)} options, expected 4")
        # R4 letter sequence
        if opts and not orphan:
            expect = [chr(ord('A') + i) for i in range(len(opts))]
            if letters != expect:
                bad("R4-letter-sequence", q, f"letters {''.join(letters)} expected {''.join(expect)}")
        # R5 true/false order
        if is_tf and len(opts) == 2 and labels != ["True", "False"]:
            bad("R5-tf-order", q, f"order is {labels}, expected ['True','False']")
        # R6 truncated or empty option text
        for _, L, t in opts:
            if not t:
                bad("R6-empty-option", q, f"option {L} has no text")
            elif re.search(r'\b(of|the|a|an|in|to|for|with|and|or|is|are|vitamin|than)$', t, re.I):
                bad("R6-truncated-option", q, f"option {L} ends on a dangling word: ...{t[-45:]!r}")
        # R7 answer leaked into question text
        if re.search(r'\bAnswer:\s*(True|False|[A-D])\b', q):
            bad("R7-answer-leaked", q, "correct answer appears inside the question text")
        # R8 stem contains the T/F prompt as trailing text with no options
        if re.search(r'(True\s*/\s*False|TRUE or FALSE)\s*$', q) and len(opts) == 0:
            bad("R8-tf-absorbed", q, "True/False prompt absorbed into stem, options dropped")
        if not orphan and num(q):
            seen_nums.append(num(q))
    # R9 numbering continuity
    if seen_nums:
        expect = list(range(1, len(seen_nums) + 1))
        if seen_nums != expect:
            dupes = [n for n in set(seen_nums) if seen_nums.count(n) > 1]
            d.append((os.path.basename(path), "R9-numbering", "(file level)",
                      f"question numbers {seen_nums} not sequential"
                      + (f"; repeated {sorted(dupes)}" if dupes else "")))
    return d

def main():
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    files = sorted(glob.glob(os.path.join(root, "*.html")))
    if not files:
        print(f"no html files found in {root}"); return 2
    allf = []
    for f in files:
        allf += check(f)
    by_rule = defaultdict(list)
    for f, r, q, m in allf:
        by_rule[r].append((f, q, m))
    print(f"Scanned {len(files)} files. {len(allf)} defects across {len(by_rule)} rules.\n")
    for rule in sorted(by_rule):
        items = by_rule[rule]
        print(f"{rule}  ({len(items)})")
        for f, q, m in items[:60]:
            print(f"    {f:14} {q[:62]:62} {m}")
        if len(items) > 60:
            print(f"    ... and {len(items)-60} more")
        print()
    return 1 if allf else 0

if __name__ == "__main__":
    sys.exit(main())
