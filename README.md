GrepG: Python Client For GrepPage
===

`grepg` (pronounced Grep G) is a python client for [GrepPage](https://www.greppage.com).  It allows you to access your notes without leaving the terminal.

![GrepG Screenshot](http://i.imgur.com/IqlY9lZ.png)

# Installation
To install `grepg` run

```
pip install grepg
```

To upgrade `grepg` to the latest release

```
pip install grepg --upgrade
```

# Requirements
- Tested on python 2.7.x and higher


# Usage - Search
## Search all public data on GrepPage.

grepg will show the description followed by the topic name and the user that created that item. The command for that item is on the next line.

```
$ grepg ruby array add
Add or append something to the end of the array [Ruby] (evidanary)
["a","b"].push('gen-rb')
...

```

## Search Private Notes on GrepPage
You will need to create an [GrepPage Account](https://www.greppage.com/signup) and then run `grepg configure`

```
$ grepg configure
Default Username: evidanary
GrepPage Secret Access Key (Settings > Token > Secret API Key on greppage.com): .......
$ grepg private_keyword
My private description
private command
...
```
## Search my notes only
When you search, grepg shows you a mix of items from topics you created and public topics that other users have created. To narrow your search to only topics you created pass the `-l` flag. Alternatively, you can see an entire topic by `grepg show topic_name`

```
$ grepg -l ruby file
read file in to string [Ruby] (my_user_name)
....
```

## Creating Data
(Requires setting up of auth credentials)

Add an item -

```
$ grepg add item
...opens a file in your editor
Successfully created item
```

Or add a topic -

```
$ grepg add topic Ruby
Successfully created topic Ruby
```

## Show a Topic

(Requires setting up of auth credentials)

```
$ grepg show scala
Convert List of string to Set
‘this is a list this’.split(‘ ‘).map(Word(_)).toSet

Case class example
case class Person(firstName: String, lastName:String)
...
```
# General Usage

```
usage: grepg [-h] [--debug] [--version] {search,configure,create,show} ...

positional arguments:
  {search,configure,create,show}
                        sub-command help
    search              Searches for keywords
    configure           Configures the client for accessing private data
    create              Creates a resource on GrepPage
    show                Displays a resource on GrepPage

optional arguments:
  -h, --help            show this help message and exit
  --debug               Show debugging info
  --version             show program's version number and exit
```

# Configuration
Setup defaults in `~/.grepg/credentials.yml` and `~/.grepg/settings.yml`

# License
grepg is under the [MIT License](http://www.opensource.org/licenses/MIT).
