# Auto ML in folder rules #

With a few rules procmail can dispatch automatically a ML message in a specific ML folder.


# Details #

```

# Auto ML
:0
* ^List-Id: <\/[^@\.]+
.ML.`echo $MATCH | sed -e 's/[^a-zA-Z\n0-9-]/_/g'`/

:0
* ^X-Mailing-List: <\/[^@\.]+
.ML.`echo $MATCH | sed -e 's/[^a-zA-Z\n0-9-]/_/g'`/

:0
* ^List-Id: \/[^\ ]+
.ML.`echo $MATCH | sed -e 's/[^a-zA-Z\n0-9-]/_/g'`/

# all the rest goes to the root folder
:0
./

```