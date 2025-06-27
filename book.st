=10 max_health
=10 health
=10 strength
=10 intellect
=10 sight
=10 speed
=10 social

%
  !health 10 ▌[red][noend]
  !health 10 > 3 health [yellow][noend]
  !health 10 > 7 health [green][noend]
  !health 10 * health ❤
  [end]
%
% 
  !10 strength  ▌✊ Strength   [strength]
  !10 intellect ▌🧠 Intellect  [intellect]
  !10 sight     ▌👀 Sight      [sight]
  !10 speed     ▌🐾 Speed      [speed]
  !10 social    ▌🎭 Social     [social]
%



# book cover
=10 max_health
=10 health
=10 strength
=10 intellect
=10 sight
=10 speed
=10 social
|[cyan]---------------------------------------------------------------------
|[cyan]                          BOOK OF WONDERS
|[cyan]---------------------------------------------------------------------
|
This is an interactive short story where choices matter.
[end][purple]Controls[reset] 
[reset]- Any key skips text animation.
[reset]- Left/right arrows change selection. 
[reset]- Press space or enter to select.[end]
>>> start reading,close the book

# start reading
<<<
|[cyan]---------------------------------------------------------------------
|[cyan]                             CHAPTER I
|[cyan]---------------------------------------------------------------------[end]

Ugh! What happened? Where is this? Wait! More importantly, who am I? 
If only this dust could settle... Maybe I could - hang on, what could 
I do again? Seems I know nothing.
|
>>> think,stand,look

# think
My head hurts terribly whenever I try to remember. Only the name 
[purple]Haian![reset] sounds familiar. But I cannot make out who that is supposed 
to be. Let's just be thankful that I am not stripped of language 
or the ability to reason. I think therefore I am... I think.
|
' +2 intellect
+2 intellect
>>> hit


# stand
I saumersault from face down to standing up. My body is surprisingly 
muscular, it seems. Sense of balance is alright too. I probably worked 
out or something, though I get the feeling that I shouldn't be that type 
of person. A mystery, perhaps for another time. Who cares?

' +2 strength
+2 strength
>>> hit

# book end
<<<
|[cyan]----------------------------------------------------------------
|[cyan]                            THE END
|[cyan]----------------------------------------------------------------
|
Reread and do different things. You may be surprised!

<<< book cover,close the book


# close the book
<<<
|[cyan]----------------------------------------------------------------
|[cyan]                            GOODBYE
|[cyan]----------------------------------------------------------------
|
I hope that you had fun. :-)
Best wishes in these troubled times. 
|                                                        - Manios
|
|
` Goodbye.