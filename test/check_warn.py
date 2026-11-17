r"""Check that \eq warns exactly for the non-equation keys in warn-body.tex."""
import re, sys

EXPECTED = {'the section', 'other section name', 'a figure', 'table in a p column'}
NO_CLEVEREF_ONLY = {'figure via ltx label'}
ok = True
for log in sys.argv[1:]:
    text = re.sub(r'\n\(mermin\)\s*', ' ', open(log, errors='replace').read())
    warned = set(re.findall(r"Package mermin Warning: `(.*?)' is not an equation label", text))
    expected = EXPECTED | (set() if 'cleveref' in log else NO_CLEVEREF_ONLY)
    if warned != expected:
        print(f'{log}: warned for {sorted(warned)}, expected {sorted(expected)}')
        ok = False
if ok:
    print('\\eq warning checks pass')
sys.exit(0 if ok else 1)
