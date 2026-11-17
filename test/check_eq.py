r"""Check the text that \eq prints in each eq-*.pdf given on the command line."""
import subprocess, sys, unicodedata

WANT = [
    'T1: the anomaly condition (1) holds',
    'T2: the Pythagorean condition (1) holds',
    'T3: the shift relation (2) holds',
    'T4: the Γ action (3) holds',
    'T5: the Schrödinger equation (4) holds',
    'T6: the Γ dual (5) holds',
]
ok = True
for pdf in sys.argv[1:]:
    text = subprocess.run(['pdftotext', pdf, '-'], capture_output=True, text=True, check=True).stdout
    # pdftotext writes accents from OT1 fonts as base letter + combining mark.
    text = unicodedata.normalize('NFC', ' '.join(text.split()))
    for want in WANT:
        if want not in text:
            print(f'{pdf}: missing {want!r}')
            ok = False
    # A citation in a section title must survive the trip through the .toc.
    t7 = 'T7: the anomaly condition (1) again'
    if text.count(t7) != 2:
        print(f'{pdf}: {t7!r} appears {text.count(t7)} times, not twice (heading and contents)')
        ok = False
if ok:
    print('\\eq checks pass')
sys.exit(0 if ok else 1)
