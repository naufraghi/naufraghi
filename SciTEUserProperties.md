Save this file in `~/.SciTEUser.properties`

```
# Window
position.left=5
position.top=22
position.width=1024
position.height=900

# Indentation
tabsize=4
indent.size=4
use.tabs=0

# Find
find.files=$(find.files) *.py *.sip

# Source files
source.files=$(source.files=),*.sip,*.TXT

# Save filters
strip.trailing.spaces=1
ensure.consistent.line.ends=1

# Buffer handling
split.vertical=0
buffers=100
buffers.zorder.switching=1
tabbar.multiline=1
reload.preserves.undo=1
line.margin.visible=1
line.margin.width=3+

# All monospace
font.base=$(font.monospace)
font.small=$(font.monospace)
font.comment=$(font.monospace)
font.text=$(font.monospace)
font.text.comment=$(font.monospace)
font.embedded.base=$(font.monospace)
font.embedded.comment=$(font.monospace)
font.vbs=$(font.monospace)

# Dark background
style.*.*=fore:#FFFFFF;back:#000000
style.*.32=$(font.base),back:#000000,fore:#ffffff
caret.fore=#FFFFFF
selection.alpha=90
selection.back=#FFFFFF

# Give symbolic names to the set of colours used in the standard styles.
colour.code.comment.box=fore:#FF7FFF
colour.code.comment.line=fore:#FF7FFF
colour.code.comment.doc=fore:#3F703F
colour.text.comment=fore:#FFFF00,back:#D0F0D0
colour.other.comment=fore:#007F00
colour.embedded.comment=back:#E0EE00
colour.embedded.js=back:#F0F000
colour.notused=back:#555500
colour.number=fore:#007F7F
colour.keyword=fore:#00007F
colour.string=fore:#7F7FAA
colour.char=fore:#7F7FAA
colour.operator=fore:#AAAAAA
colour.preproc=fore:#7F7F00
colour.error=fore:#FFFF00,back:#FF0000


# Python styles
# White space
style.python.0=fore:#DDDDDD
# Comment
style.python.1=fore:#007F00,$(font.comment)
# Number
style.python.2=fore:#007F7F
# String
style.python.3=$(colour.string),$(font.monospace)
# Single quoted string
style.python.4=$(colour.string),$(font.monospace)
# Keyword
style.python.5=fore:$(colour.keyword),bold
# Triple quotes
style.python.6=fore:#7F0000
# Triple double quotes
style.python.7=fore:#7F0000
# Class name definition
style.python.8=fore:#0000FF,bold
# Function or method name definition
style.python.9=fore:#667F7F,bold
# Operators
style.python.10=$(colour.operator)
# Identifiers
style.python.11=
# Comment-blocks
style.python.12=fore:#7F7F7F
# End of line where string is not closed
style.python.13=fore:#000000,$(font.monospace),back:#E0C0E0,eolfilled
# Highlighted identifiers
style.python.14=fore:#90D0F0
# Decorators
style.python.15=fore:#F09000
# Matched Operators
style.python.34=fore:#0000FF,bold
style.python.35=fore:#FF0000,bold
# Braces are only matched in operator style
braces.python.style=10
```
