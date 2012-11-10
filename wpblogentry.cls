%
%  wpblogentry.cls - Document Class for WordPress Blog post
%
%  (c) 2010 Eric Finster
%

% The class we are providing
\ProvidesClass{Latex/Classes/wpblogentry}[2010/01/27 v1 WordPress Blog Entry]

% Set up the base class as "article"
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{article}}
\ProcessOptions\relax
\LoadClass[10pt]{article}

% These declarations give us variables for tags and categories
\def\tags#1{\gdef\@tags{#1}}
\def\category#1{\gdef\@category{#1}}

\renewcommand{\maketitle}{
  \begin{center}
    \vskip 2em
    { \LARGE \@title \par }
    \vskip 1.5em
    { \large Tags: \@tags \par }
    \vskip 1.5em
    { \large Posted In: \@category }
  \end{center}
  \par
  \vskip 1.5em
}


