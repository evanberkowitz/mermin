% A stand-in for IOP's iopart.cls, which TeX Live does not ship: like the
% real class, it defines equation*, which conflicts with amsmath.
\ProvidesClass{iopart}[2026/11/17 test stand-in]
\LoadClass{article}
\expandafter\def\csname equation*\endcsname{\[}
\expandafter\def\csname endequation*\endcsname{\]}
