# Story engine

This is a domain-specific language for writting small text-based
games. Its rules are fairly simple and it aims at letting the
author create highly interactive stories. 

**Use an toml or markdown (better in vscode, in github use mdx) highlighter for .st files.**

## Text formatting

The syntax mainly depends on separating instructions into lines.
The first 1-3 characters of each line are an 
indication of what the line is about, such being simple text
or containing value manipulation.

In the simplest case, you would write stylized text to be
read in the console. Save the following file
as `book.st`. Then run `python engine.py` to get an 
animated text in your screen. 

```mdx
Hello world!
```

Don't want animation? Just put `|` at the beginning of the
line. For simple formatting options, like colors, manual
line ends, place a name into square brackets `[...]`.
Formatting is reset at the end of each line or if you write
`[reset]`.
As an example, below we print two green lines without animation.
Formatting is reset for the last set of exclamations. Note that
formatting resets automatically at the end of *your* lines,
that is, not at `[end]`, which is just a line break character
and should be largely avoided.

```mdx

|[green]Hello[end]world[reset]!!!
```

If a line is incomplete, end it with `[noend]` and the next
one will continue from its end in the same line. To avoid
any kind of formatting from special symbols but use them
as the first characters of lines, start those lines
with a color declaration or `[reset]`. You may also have
some empty lines for spacing. Denote those with `|`.

## Changing the next option

You can name separate segments of your text by starting
a line with `#`. Other segments can redirect there by
starting a line with `>>>` and containing comma-separated
options with the same title. Segment titles can contain
spaces but not commas and will appear to your users
so that they can select from those with the arrows and
pressing space or enter to confirm the selection.
Here is an example:

```mdx
Had fun?
>>> of course
>>> perhaps

# of course
Of course we did!
>>> end

# perhaps
Perhaps, but joy is too ephemeral to remember.
>>> end

# end
That's all.
```

If you only have only one option, you move to that automatically.
Furthermore, If you want to wait for your user about something 
and wait for them to progress, start a line with `\``. In general,
options are never 

```mdx
Hi!
`OK
```

You also have the option to completely clear the gathered text and
continue from a custom point. To do this, change the option line to start 
with `<<<`. Note that this will find *the first segment that
matches (not the last) and will also skip over the beginning
of the file. Note that this will not reset the Hud later.
Use the same symbol without any options to clear text without
restarting.

```mdx
[red]This is an obnoxious machine we are playing with.

# start
Think of a number, any number.
>>> 5
>>> another

# 5
I win.
>>> end

# another
You are wrong. 
<<< start
```

## Variables

Operating the game logic, you might want to store some numbers
or names/properties. Either integer numbers, like `0,42,-3`, or
text enclosed in quotations, like `"myname"` can be stored. 
You must name the value to be remembered, where the name 
is called a *variable* in programming.

Set a variable's value 
by starting a line with `=` and writing first the value and then
the name on which it will be stored, like below. You can print the value
of a variable by enclosing it in square brackets, similarly to
how we could declare colors and other special effects. In fact,
those are just variables that contain textual replacement for some
ANSI codes, which are special characters to indicate text
formatting. 

```mdx
= 100 patience
You have [patience]% patience left.
```

You can also set a random number from 0 to the designated value (including
both zero and the designated value) like below.

```mdx
? 100 patience
You have [patience]% patience left.
```

The variable name should not contain spaces, but you can separate
segments with symbols like `_` and `.`. At any point in the game,
you can increase, decrease, multiple, or divide numbers by starting 
a line with a similar syntax but switching the assignment symbol for `+`,
`-`, `*`, or `/` instead. Modifications persist as you hop from segment
to segment, so they carry on to the rest of your story.

```mdx
= 100 patience
You started with [patience]% patience.
But, oh no! Something stupid happened!
|
`But why?
-70 patience
You are at [patience]% patience.
```

Values placed into square brackets are generally replaced
by their values too. For example you can add a value to itself,
like below. You can also get the variable name from another variable
storing text, but this can get too complicated quickly and is
not recommended.

```mdx
+[patience] patience
```

Similarly, you can use square brackets for determining options,
like below.

```mdx
= "explode" _option_
>>> [_option_]
```

Finally, you can determine whether to perform a value modification
by starting a line with comparisons, which take the form
`@ [value] [name] [rest_of_line]` to run the line only when the
value is exactly equal to the name (numbers are never the same
as strings), `! [value] [name] [rest_of_line]` when they are different,
`< [value] [name] [rest_of_line]` when the value is greater than the name,
for example `< 10 apples` reading as *we have less than 10 apples*,
and `> [value] [name] [rest_of_line]`. Inequalities only apply for numbers,
and not that there is no equality-inclusive check because this is redundant
while also a bit confusing given the rest of the syntax.

You can combine logical checks in the same line by placing them one after the 
other. In this case, all of them must hold true.
On the other hand, you can get alternative options by copying the same line
and making a different check. In general, this is a bit verbose compared
to normal programming languages, but it helps readability.

Performing logical checks does *not* work for `>>>`, `\``, '#` because these *must*
start a line to apply. In those cases, compute a temporary variable,
making it clear that you will not reuse its value elsewhere 
by starting and ending it with an underscore `_` as a convention. 
Here is a full example. This basically reads as *"start by setting a peace option, 
if we are at less than 50 patience, set an explode option, move to the
namesake segment"*.

```mdx
= "peace" _option_
< 50 patience = "explode" _option_
>>> [_option_]
```

**Future versions of this engine will be safe in preventing logical
error while running, but this is not the case for this prototype.
Do check your stories.**



## Hud

You can also crate an interface at the top of your screen.
You can add to this interface as the story progresses by
enclosing a set of lines into `%%`. Each of those two symbols
should be placed in a line separately from other text
to mark the beginning
and end of the information. This text is also re-evaluated
every time it is drawn. For example, the code below

```mdx
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

# start

This is my adventure.
```