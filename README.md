# mermin

Tools for writing equations the way N. David Mermin asks in
"What's Wrong with These Equations?", *Physics Today* **42**(10), 9 (1989),
[doi:10.1063/1.2811173](https://doi.org/10.1063/1.2811173).

Version 0.1, 2026/11/16.

## Description

Mermin's Good Samaritan rule asks that every equation be cited by a noun
phrase as well as its number: "the anomaly condition (3)", never a bare
"(3)". This package makes the phrase the label. `\alsolabel{phrase}` gives
an equation, or one line of an `align`, as many phrases as the prose needs,
and `\eq{phrase}` cites it by one of them, printing the phrase and the
linked number:

```latex
\usepackage{mermin}
...
\begin{equation}
  L_1^2+L_2^2=R_1^2+R_2^2.
  \label{anomaly condition}
  \alsolabel{Pythagorean condition}
\end{equation}
The 3450 model satisfies the \eq{anomaly condition}.
Read as a statement about integers, the same line is
the \eq{Pythagorean condition}.
```

prints "the anomaly condition (1)" and "the Pythagorean condition (1)".

`\alsolabel` may come before or after `\label`, any number of times, or
replace it entirely. Every key gets the line's number and hyperref anchor,
and `\ref`, `\eqref`, `\pageref`, and `\cref` all work. It supports the
amsmath displays (`equation`, `align`, `gather`, `multline`, `split`,
`subequations`) and `empheq`, with hyperref and cleveref loaded in any
order. `\label` itself is unchanged.

`\eq{phrase}` falls back to the label `eq:phrase`, so existing `eq:` labels
need no change. A phrase that cannot be a key, such as one with math, is
given once where the label is defined, `\alsolabel[$\Gamma$ action]{Gamma action}`,
and cited as `\eq{Gamma action}`, which prints "Γ action (n)". `\eq` is for
equations only and warns when its key names a section, figure, or anything
else.

The full documentation, including Mermin's three rules and the
annotated implementation, is `mermin.pdf`.

## Files

| File         | Contents                                                     |
|--------------|--------------------------------------------------------------|
| `mermin.dtx` | Documented source: user manual and implementation            |
| `mermin.ins` | Installer: generates `mermin.sty` from `mermin.dtx`          |
| `mermin.sty` | The package (generated; not in the repository)               |
| `mermin.pdf` | The manual (generated; not in the repository)                |
| `test/`      | Test suite for `\alsolabel`                                  |

## Installation

```sh
make            # tex mermin.ins, then pdflatex mermin.dtx with its indexes
```

Then either copy `mermin.sty` to `$(kpsewhich -var-value TEXMFHOME)/tex/latex/mermin/`,
or point a paper's build at this directory with `TEXINPUTS=/path/to/mermin:`.
Without make, run `tex mermin.ins` for the package and `pdflatex mermin.dtx`
twice for the manual.

Requires a LaTeX format from 2020-10-01 or later, and amsmath.

## Testing

```sh
make test
```

typesets every supported environment, with the keys in every order, in four
package configurations (amsmath alone; with hyperref; with hyperref and
cleveref; and with mermin loaded first), and checks that every key in each
`.aux` file resolves to its line's number and anchor. It also checks the
text `\eq` prints, for phrase keys, `eq:` keys, typeset phrases given to
`\alsolabel`, and non-ASCII phrases, and that `\eq` warns exactly when it
cites something other than an equation.

## License

Copyright (C) 2026 Evan Berkowitz.

This work may be distributed and/or modified under the conditions of the
LaTeX Project Public License, version 1.3c or later
(<https://www.latex-project.org/lppl.txt>), which is part of all
distributions of LaTeX from 2008 on. It has the LPPL maintenance
status "maintained"; the Current Maintainer is Evan Berkowitz.
