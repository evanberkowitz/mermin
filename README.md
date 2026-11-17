# mermin

LaTeX tools for writing equations the way N. David Mermin asks in
"What's Wrong with These Equations?", *Physics Today* **42**(10), 9 (October 1989),
[doi:10.1063/1.2811173](https://doi.org/10.1063/1.2811173).

## Mermin's rules

1. **Fisher's rule.** Number *every* displayed equation, whether or not the
   text refers to it now. Readers, referees and later papers will.
2. **The Good Samaritan rule.** When citing an equation, identify it by a
   phrase as well as a number: "the anomaly condition (3)", never a bare
   "(3)" or "Eq. (3) shows". An equation number is a locator, never a noun.
   The same holds for citation numbers: "Berkowitz, Cherman, and Jacobson [1]"
   or "Ref. [1]", not "of [1]".
3. **The math-is-prose rule.** A display is part of its sentence: punctuate
   it with commas and periods so the paragraph reads straight through.

## `\alsolabel`

The Good Samaritan rule asks for a noun phrase at every citation, and the
right phrase changes with context. The same line can be "the anomaly
condition" in one paragraph and "the 3450 condition" in another. amsmath
allows one `\label` per numbered line. `\alsolabel{key}` adds more labels to
the same line:

```latex
\usepackage{mermin}
...
\begin{equation}
  L_1^2 + L_2^2 = R_1^2 + R_2^2
  \label{eq:anomaly}
  \alsolabel{eq:3450 condition}
\end{equation}
... the anomaly condition~\eqref{eq:anomaly} ...
... the 3450 condition~\eqref{eq:3450 condition} ...
```

- Use it any number of times per line, before or after `\label`, or with no
  `\label` at all.
- Every key gets the same number and hyperref anchor; `\ref`, `\eqref` and
  `\cref` all work.
- Works in `equation`, `align`, `gather`, `multline`, `split`,
  `subequations` and `empheq`, with hyperref and cleveref, loaded in any
  order. Outside a display it is plain `\label`.
- `\label` is unchanged: two `\label`s on one line are still an error.

## Tests

`make -C test` builds four package configurations and checks that every key
in `test/alsolabel-body.tex` resolves to its line's number and anchor.
