"""Check that every key gN-x in an .aux resolves to the same label data as its group, and groups differ."""
import re, sys, collections, pathlib
ok = True
body = (pathlib.Path(__file__).parent / 'alsolabel-body.tex').read_text()
expected_keys = set(re.findall(r'(?:label|alsolabel)\{(g\d+-[a-z])\}', body))
for aux in sys.argv[1:]:
    text = open(aux).read()
    labels = {}
    for m in re.finditer(r'\\newlabel\{(g\d+-[a-z])\}\{(.*)\}\s*$', text, re.M):
        labels[m.group(1)] = m.group(2)
    missing = expected_keys - set(labels)
    if missing:
        print(f'{aux}: MISSING {sorted(missing)}'); ok = False
    groups = collections.defaultdict(dict)
    for k, v in labels.items():
        groups[k.split('-')[0]][k] = re.sub(r'\{[^{}]*\}\{\}$', '', v)  # ignore trailing extra field
    nums = {}
    for g, ks in sorted(groups.items(), key=lambda x: int(x[0][1:])):
        vals = set(ks.values())
        num = re.match(r'\{\{?([^{}]*)', next(iter(vals))).group(1)
        status = 'ok' if len(vals) == 1 else 'MISMATCH'
        if len(vals) != 1: ok = False
        nums[g] = num
        print(f'{aux:20} {g:4} {sorted(ks)} -> {num} {status}')
    # Every display line has its own number; g18 and g19 label a section
    # and a figure, whose counters are separate.
    shown = {g: n for g, n in nums.items() if g not in ('g18', 'g19')}
    if len(set(shown.values())) != len(shown):
        print(f'{aux}: two display groups share a number: {shown}'); ok = False
    expected = 20
    if len(groups) != expected:
        print(f'{aux}: expected {expected} groups, got {sorted(groups)}'); ok = False
sys.exit(0 if ok else 1)
