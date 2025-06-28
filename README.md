# Story engine

This is a domain-specific language for writting small text-based
games. Its rules are fairly simple and it aims at letting the
author create highly interactive stories. 

**Use an toml or markdown highlighter for .st files.**

## Text formatting

The syntax mainly depends on separating stuff into lines.
The first 1-3 characters of each line are an 
indication of what the line is about, such as simple text
or manipulating values.

In the simplest case, you would write stylized text to be
read in the console. Write the following file and save it
as `book.st`. Then run `python engine.py` to get an 
animated text in your screen. 

```toml
Hello world!
```

Don't want animation? Just put `|` at the beginning of the
line. For simple formatting options, like colors, manual
line ends, place a name into square brackets `[...]`.
Formatting is reset at the end of each line or if you write
`[reset]`.
As an example, below we print two green lines without animation.
Formatting is reset for the last set of exclamations. 

```toml
|[green]Hello[end]world[reset]!!!
```

If a line is incomplete, end it with [noend] and the next
one will continue from its end.


## Variables


## Hud

In some cases, you might want to e
