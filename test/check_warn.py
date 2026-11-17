r"""Check that \eq warns exactly for the non-equation keys in warn-body.tex."""
import re, sys

EXPECTED = {'the section', 'other section name', 'a figure'}
ok = True
for log in sys.argv[1:]:
    text = re.sub(r'\n\(mermin\)\s*', ' ', open(log, errors='replace').read())
    warned = set(re.findall(r"Package mermin Warning: `(.*?)' is not an equation label", text))
    if warned != EXPECTED:
        print(f'{log}: warned for {sorted(warned)}, expected {sorted(EXPECTED)}')
        ok = False
if ok:
    print('\\eq warning checks pass')
sys.exit(0 if ok else 1)
