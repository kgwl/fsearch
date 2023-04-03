# fsearch

Recursively search for a pattern in many files and directories. The default output is a table with statistics of the files.


Example usage:

#### Search pattern in bar.txt file:
```
python3 fs.py -p pattern -d foo/bar.txt
```

#### Search for many patterns in a wordlist in a directory:
```
python3 fs.py -w wordlist.txt -d /foo/bar/
```

##### Search for many patterns in a wordlist in a directory and print all lines that contain a word from the wordlist.
```
python3 fs.py -w wordlist.txt -d /foo/bar/ -m full
```
