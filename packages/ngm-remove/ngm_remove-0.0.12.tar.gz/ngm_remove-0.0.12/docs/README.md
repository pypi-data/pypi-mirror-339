### Remove

- removes files
- prints out filepath
- logs filepath to syslog/sqlite

### Motivation

- being able to clean up folders deep inside tree, like: `remove **/node_nodules`
- have some persistent logging on what being removed: in journald/syslog and in sqlite database
- get list of files to remove: from file
- get list of files to remove: from command

### Alternative: `rm -rf **/node_nodules`

- Yes
- However we would not see what entries being removed

### Alternative: `rm -rfv **/node_nodules`

- Yes
- But `rm` would log each file (inside `node_modules`) in this case.
- For a large `node_modules` - the output is overwhelming. I just need to see which node_modules being removed and keep the output log readable.

### Alternative:`find` and `xargs`

- Yes
- But we will end up with rather longer command for a `trivial` task

### Alternative: `find . -type d -name node_modules -prune -print -exec rm -fr {} \;`

- Yes, it does work!
- Again, explaining commands like this would take some effort.
- Or, running commands like this, without fully understanding it - is a risky habit

### Example

```bash
pip install ngm-remove

cd projects

remove **/node_nodules

journalctl -t remove -r
```

### Use in scripts

- In scripts, you might need to use `shopt -s globstar` to enable `**` globs

```bash
shopt -s globstar # feature available since bash 4.0, released in 2009
remove **/node_modules
```

### Remove files of certain type

```bash
find . -type f -exec file {} \; | grep -i --color=never avif > files.txt
remove --input files.txt
```

### Options

```bash
remove file1 file2              # Remove file1 and file2
remove --help                   # Show help
remove --version                # Show version
remove --input list.txt         # Get paths from list.txt and remove those
remove --cmd 'cat list.txt'     # Get paths from running command and remove those
```
