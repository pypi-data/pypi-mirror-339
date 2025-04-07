# subdomain-permut
Subdomain permutation tool

## this vs [alterx](https://github.com/projectdiscovery/alterx)
Alterx is good, but manually generating permutations file is kinda tedious. Moreover, when working with large files, alterx doesn't write anything for *days*(it has happened to me). So, I am releasing this simple tool for subdomain permutation

## Usage
You can simply run this command, and it will do most of the thigs automatically
```bash
python3 main.py -l subdomains.txt -d site.com
```

```
usage: main.py [-h] --list LIST --domain DOMAIN [--level LEVEL] [--output OUTPUT] [--enrich ENRICH] [--verbose]

Subdomain permutation tool

optional arguments:
  -h, --help            show this help message and exit
  --list LIST, -l LIST  Subdomains list
  --domain DOMAIN, -d DOMAIN
                        Domain name for the target
  --level LEVEL         Number of iterations to run through (default=2)
  --output OUTPUT, -o OUTPUT
                        Output file name (default=permut.txt)
  --enrich ENRICH, -e ENRICH
                        Enrich using given wordlist
  --verbose, -v         Verbose output
  ```