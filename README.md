# Story engine

This is a domain-specific language for writting small text-based
games. Its rules are fairly simple and it aims at letting the
author create highly interactive stories. 

**Use an properties, toml, or markdown (better for vscode) highlighter for .st files.**

## Text formatting

The syntax mainly depends on separating stuff into lines.
The first 1-3 characters of each line are an 
indication of what the line is about, such as simple text
or manipulating values.

In the simplest case, you would write stylized text to be
read in the console. Write the following file and save it
as `book.st`. Then run `python engine.py` to get an 
animated text in your screen. 

```properties
Hello world!
```

Don't want animation? Just put `|` at the beginning of the
line. For simple formatting options, like colors, manual
line ends, place a name into square brackets `[...]`.
Formatting is reset at the end of each line or if you write
`[reset]`.
As an example, below we print two green lines without animation.
Formatting is reset for the last set of exclamations. 

```properties

|[green]Hello[end]world[reset]!!!
```

If a line is incomplete, end it with [noend] and the next
one will continue from its end.


## Variables


## Hud

You can also crate a an interface at the top of your screen.
You can add to this interface as the story progresses by
enclosing a set of lines into `%%`. These two symbols
should be placed in a line separately to mark the beginning
and end of the information. This text is also re-evaluated
every time it is drawn.

```properties
=10 max_health
=10 health
=10 strength
=10 intellect
=10 sight
=10 speed
=10 social

%
  ▌[red][noend]
  > 3 health [yellow][noend]
  > 7 health [green][noend]
  * health ❤
  [end]
%
% 
  ▌✊ Strength   [strength]
  ▌🧠 Intellect  [intellect]
  ▌👀 Sight      [sight]
  ▌🐾 Speed      [speed]
  ▌🎭 Social     [social]
%

# test

This is my text
```
