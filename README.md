# rc2resource-website
RC2 grant website for DK099810 and DK114785

# generating "pretty" structures
I used a pretty hacky method since there weren't many compounds:
1) Copy out structure to fresh chemdraw
2) Save as png
3) Run make-pretty-structure bash script (requires imagemagick)
Why --> chemdraw lines have annoying gaps at joins (bad miter joints). Scaling png export appears to fix.
