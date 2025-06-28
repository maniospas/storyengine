=10 max_health
=10 health
=10 strength
=10 intellect
=10 sight
=10 speed
=10 social
=0 provisions
="none" trait
= "WONDERS" progress
= 20 __refresh

%
  =[max_health] _lost_
  -[health] _lost_
  !0 _lost_ [white][noend]
  !0 _lost_ ▌[red][noend]
  !0 _lost_ > 3 health < 8 health ^ health 🧡[noend]
  !0 _lost_ > 7 health ^ health 💚[noend]
  !0 _lost_ < 4 health ^ health ❤️[noend]
  !0 _lost_ [white][noend]
  !0 _lost_ ^ _lost_ 🤍
%
%
  !0 provisions ▌[noend]
  !0 provisions ^ provisions 🥥
%
% 
  !10 strength ▌✊ [strength] strength
  !10 intellect ▌🧠 [intellect] intellect
  !10 sight ▌👀 [sight] sight
  !10 speed ▌🐾 [speed] speed
  !10 social ▌🎭 [social] social
[end][cyan]---------------------------------------------------------------------
[cyan]  [progress]
[cyan]---------------------------------------------------------------------[end]
%



# book cover
=10 max_health
=10 health
=10 strength
=10 intellect
=10 sight
=10 speed
=10 social
=0 provisions
="none" trait
= "WONDERS" progress

This is an interactive short story where choices matter.
|
[purple]Controls[reset] 
[reset]- Any key skips text animation.
[reset]- Left/right arrows change selection. 
[reset]- Press space or enter to select.
|
>>> start reading,close the book

# start reading
<<<
= "SUMMONED" progress
|
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
  `[cyan]+2 intellect[yellow]
  +2 intellect
  >>> hit

  # stand
  I saumersault from face down to standing up. My body is surprisingly 
  muscular. Sense of balance is alright too. I probably worked out or
  something, though I feel not like the type of person that sticks to
  a training schedule. A mystery, perhaps for another time. Who cares?
  |
  `[cyan]+2 strength[yellow]
  +2 strength
  >>> hit

  # hit
  A blunt pain on my head stops my train of thought. It hurts!
  |
  `[red]-2 health[yellow]
  -2 health
  >>> coconut

  # look
  Anyway, looking arround I can see the dust parting somewhat.  Enough 
  to make out a coconut zooming towards me! I barely avoid it by rolling 
  away. Standing up shaken but having gained a small victory, I 
  mechanically touch the bridge of my nose in triumph. 
  'Not on MY watch!' I shout.
  |
  `[cyan]+2 sight +1 speed[yellow]
  +2 sight
  +1 speed
  >>> coconut

# coconut
Who did that? A short distance away, a monkey on top of a tree aims 
a second coconut at me.
|
>>> dodge,block,wait

  # dodge
  ? 20 _chance_
  = "fail" _next_
  < [speed] _chance_ = "dodge" _next_
  >>> [_next_]

  # dodge
  It is trivial to dodge the telegraphed attack. I am getting good at 
  this! Maybe I should start dodging for a living. What did I do for a 
  living again? At best vague colors move in my memory.
  |
  `[cyan]+2 speed[yellow]
  +2 speed
  >>> flee

  # fail
  I fail to properly move out of the way. If only I was faster... But 
  you cannot cry over spilled mango juice. No, this sounds a bit wrong 
  but I fail to recall how the true saying goes.
  |
  >>> hit

  # block
  I take the safe option of raising my arms to block the projectile. It
  smarts, but I withstand the attack. Maybe it will bruise a bit, though 
  nothing serious.
  |
  `[red]-1 health [cyan]+1 strength[yellow]
  -1 health
  +1 strength
  >>> flee

  # wait
  I laugh, finding the situation hilariousl. I will not dodge! 
  I will stand there and take the hit - to make a statement! Of what
  I know not.
  |
  >>> hit


# hit
The monkey should be some kind of champion in its art. The coconut 
hits me squarely in the face with the elegance of a brick. I also 
take the emoitional damage of remembering what bricks are but not 
who I am.
|
`[red]-2 health[yellow]
-2 health
= "flee" _next_
< 7 health = "tough" _next_
>>> [_next_]

  # tough
  At least I feel like my tolerance for pain has increased from all 
  the beating I took. Or maybe I only now discovered that I can take 
  a beating and keep standing perfectly fine.
  |
  `[cyan]+2 max health[yellow]
  +2 max_health
  >>> flee


# flee
Perhaps because I have become the target for coconut-throwing, I am 
still thoroughly confused. So I should be forgiven in noticing late 
that the perpetrator is now running away. 
|
Is it... screeching mockingly? Does it perchance have sentience?
|
>>> chase,think,look,eat

  # chase
  Enraged I follow the monkey into a jungle. It has the home advantage, 
  but I embrace my anger, feeling myself going [cyan]berserk[reset]. How dare 
  the simian play with me that way?
  |
  I soon learn that both my anger and hopes of releasing it by smacking 
  the creature at least once are misplaced. For I both lost both my
  quary and my way in the dense forestation. If there is use for anger, 
  that is not for hunters.
  |
  = "berserk" trait
  >>> jungle

  # think
  ="think" _next_
  >12 intellect ="superthink" _next_
  >>> [_next_]

  # superthink
  I take the chance to think things through, discovering that I can work my 
  brain more and more. I am just learning about myself afterall!
  |
  `[cyan]+1 intellect[yellow]
  +1 intellect
  But I have reached the state of knowing a lot about my superfloous qualities. 
  I do not think I will be surprising myself in other areas, though of course 
  this can always be fixed with good-old -I shudder imagining it- training or 
  practice.
  |
  ANYWAY! Where were we? Ah, the monkey with the personality. It has long been 
  gone, because I started overthinking.
  |
  >>> think

  # think
  Though I cannot recall from where I come, I am positive that animals 
  were just animals. Therefore, it holds to reason that this should be
  a different world, right? If you eliminate all possibilities, the one 
  remaining must be true, however improbable.
  |
  Who said that? ... Can't remember... Though it seems my old world is
  ingrained in my subconsious. I am now [cyan]curious![reset] to explore this new 
  one and be taken by surprise even if I do not recall exactly why. 
  For, if even the animals have thoughts, imagine the marvels a 
  civilization could have reached!
  |
  = "curious" trait
  >>> look,eat

  # eat
  Before further action, I stoop to grab the coconuts, one of which is 
  cracked. I am able to pry it open and it is as delicious as it was 
  painful to get hit by! I feel my vitality returning from the land
  of the hungry, and resolve to always carry around delicious stuff. 
  |
  `[cyan]+2 health[yellow]
  +2 health
  >[max_health] health = [max_health] health

  I take the other coconut with me as provisions - a rock can help pry 
  it open much better than my head. Also, is my head so sturdy so as 
  to break this hard shell open? Unable to answer the question, yet 
  satiated I look around.
  |
  `[cyan]+1 provisions[yellow]
  +1 provisions
  >>> look


  # look
  >>> places


# places
  By now, the dust that had maybe coincided with my arrival has fully 
  settled down.[noend]
  >10 intellect There is no wind blowing, after all.[noend]
  This place is surely interesting.
  |
  In the distance, a tall mountain can be seen. But nearby a dirt trail
  winds away. Lastly, in the direction the monkey fled, there is a dense
  jungle. I am in a kind of junction between the three.
  >10 sight Of the three, the trail looks most promising, as it has wagon-tracks.
  >10 sight Surely it leeds to some city. I squint and sure enough spot chimney smoke in the distance.
  <11 sight [end]I weigh my options but don't have much to go for. 
  |
  = "trail" _trail_
  >10 sight = "city" _trail_
  >>> jungle,mountain,[_trail_]


# jungle

The jungle is hot and sticky, and generally a pain to move
through. The tall overarching trees create flickering shadows
that mess with one's sense of direction.
|
With all hopes of finding my way forward or backward lost
under the canopy of leaves. Spiderwebs occasionally cling to 
me, but thankfully none of the large spiders weaving them take 
a fancy on hoping on my back.


>>> book end


# mountain

The road towards the mountain is long. Minutes stretch into
hours -I still have no idea how I get to name all things
other than myself- and I grow weary. Above me, the sun burns
hot and I feel my motivation draining.
|
`[red]-2 health[yellow]
-2 health

>>> book end

# trail
>>> book end

# city
>>> book end


# book end
<<<
= "END" progress
|
Reread and do different things. You may be surprised!
|
<<< book cover,close the book


# close the book
<<<
= "GOODBYE" progress

I hope that you had fun. :-)
Best wishes in these troubled times. 
|                                                        - Manios
|
|
` Goodbye.