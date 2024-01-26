# Note utility for linux command line

Personal project for taking timestamped, tagged notes while working in the field and not really able to
easily switch away from the terminal or use wifi.

Build with `setup.py` and install globally.

## Usage
#### Add a note to default notebook
```
$ note A note about something that happened
```

#### Add a note to specific notebook
```
$ note a note for a special notebook -n the_notebook
```

#### Tag a note
```
$ note A note about something that happened -t tag1 tag2
```
#### List notebooks
```
$ note --notebooks
Notebooks:
	general
	field_notes*
```

#### Create notebook
```
$ note -c a_new_notebook
```

#### Set default
```
$ note --set-default field_notes
```

#### Print notes
```
$ python note.py --notes
2024-01-16 09:54:34-08:00: test
2024-01-16 09:55:24-08:00: no internet on h11, no fuel pumping on h13... going back to hotel until mechanical gets here
2024-01-16 12:11:46-08:00: okay we replaced fuel pump and filter but harv still sputters
```

#### Tag and view tagged notes
```
$ note a general note
Note saved to demo_notebook notebook
$ note a tagged note -t tag1
Note saved to demo_notebook notebook
$ note --notes
2024-01-25 16:21:04-08:00: a general note
2024-01-25 16:21:13-08:00: a tagged note
$ note --notes -t tag1
2024-01-25 16:21:13-08:00: a tagged note
```