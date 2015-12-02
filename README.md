# computing4liberalarts.py
A working repository for ideas for a course

This repository currently contains a bare minimum that I could distill from internet resources to access the [Twitter search API](https://dev.twitter.com/rest/public/search).  We could use this for investigating the feasibility to include twitter data in the course "Computing in Liberal Arts".  

##Install

This is a Python package, in order to install clone this repository using `git` (and [`git-crypt`](https://github.com/AGWA/git-crypt):

```sh
git clone https://github.com/davidavdav/computing4liberalarts.py.git
cd computing4liberalarts
git-crypt unlock
```

The last command is necessary to unlock an [encrypted file](twitter/secret.py) containing the credentials for accessing the twitter search API from an [application only authentication](https://dev.twitter.com/oauth/application-only) perspective. 

If you drop me a line with your gpg public key, I can add you to the `git-crypt unlock` users.  

## Using the search API

With this package in the search path, you can do a twitter search in Python, e.g., for `"ucu"`
```python
import twitter
result = twitter.search("ucu")

import json
print json.dumps(result, indent=4)
```
The `result` is a Python structure (from the twitter API json result) containing tweets related to the search.  In my experience, I get 15 tweets at the time, and the results are quite structured.  There probably are ways to specify the query in a way that we ge more results, or filtered by language or time period etc.   One of the things we could ask the students to do, is to collect particular items from the structure, and print them to a plain text table (csv), that can then be analysed in R. 

## Python twitter API

There are many.  It is very well possible that this can be done in just a few lines using a standard package.  However, I could not find anythong that could use the "application only authentication".

