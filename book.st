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
= 25 __refresh

% HEALTH
  =[max_health] _lost_
  -[health] _lost_
  !0 _lost_ [reset][noend]
  !0 _lost_ ▌[red][noend]
  !0 _lost_ > 3 health < 8 health ^ health 🧡[noend]
  !0 _lost_ > 7 health ^ health 💚[noend]
  !0 _lost_ < 4 health ^ health ❤️[noend]
  !0 _lost_ [white][noend]
  !0 _lost_ ^ _lost_ 🤍
%
% PROVISIONS
  !0 provisions ▌[noend]
  !0 provisions ^ provisions 🥥
%
% ABILITIES
  !10 strength ▌✊ [strength] strength
  !10 intellect ▌🧠 [intellect] intellect
  !10 sight ▌👀 [sight] sight
  !10 speed ▌🐾 [speed] speed
  !10 social ▌🎭 [social] social
%
% HEADER
[end][cyan]---------------------------------------------------------------------
[cyan]  [progress]
[cyan]---------------------------------------------------------------------
%

& GAIN _effect_
  |
  `[cyan][_effect_][yellow]
  [_effect_]
  >[max_health] health = [max_health] health
&

& DAMAGE _value_
  |
  `[red]-[_value_] health[yellow]
  -[_value_] health
  <1 health >>> death
&

& HUNGRY 
  @0 provisions >5 health I am out of provisions but can still go on,
  @0 provisions >3 health <6 health Unfortunately I am out of provisions. My stomach rumbles, hungry.[end]It's still bearable though.
  @0 provisions <4 health I am hungry and miserable. I feel faint.
  @0 provisions |
  @0 provisions `[red]-1 health[yellow]
  @0 provisions -1 health
  <1 health >>> death
  >0 provisions `eat
  >0 provisions I eye my provisions carefully and pick the most tasty. Yum![end]
  >0 provisions -1 provisions
&

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
  \\ GAIN +2 intellect
  >>> hit

  # stand
  I saumersault from face down to standing up. My body is surprisingly 
  muscular. Sense of balance is alright too. I probably worked out or
  something, though I feel not like the type of person that sticks to
  a training schedule. A mystery, perhaps for another time. Who cares?
  \\ GAIN +2 strength
  >>> hit

  # hit
  A blunt pain on my head stops my train of thought. It hurts!
  \\ DAMAGE 2
  >>> coconut

  # look
  Anyway, looking arround I can see the dust parting somewhat. Enough 
  to make out a coconut zooming towards me! I barely avoid it by rolling 
  away. Standing up shaken but having gained a small victory, I 
  mechanically touch the bridge of my nose in triumph. 
  'Not on MY watch!' I shout.
  |
  `[cyan]+2 sight, +1 speed[yellow]
  +2 sight
  +1 speed
  >>> coconut

# coconut
Who did that? A short distance away, a monkey on top of a tree aims 
a second coconut at me.
|
>>> dodge,block,wait

  # dodge
  ?20 random
  <[random] speed >>> fail
  It is trivial to dodge the telegraphed attack. I am getting good at 
  this! Maybe I should start dodging for a living. What did I do for a 
  living again? At best vague colors move in my memory.
  \\ GAIN +2 speed
  >>> flee

  # fail
  I fail to properly move out of the way. If only I was faster... But 
  you cannot cry over spilled mango juice. No, this sounds a bit wrong 
  but I fail to recall how the true saying goes.
  |
  >>> hit

  # block
  I take the safe option of raising my arms to block the projectile.
  It smarts, but I withstand the attack. Maybe it will bruise a bit, 
  though nothing serious.
  |
  `[red]-1 health [cyan]+1 strength[yellow]
  -1 health
  +1 strength
  >>> flee

  # wait
  I laugh, finding the situation hilarious. I will not dodge! I will 
  stand there and take the hit. To make a statement! About what, I 
  know not.
  |
  >>> hit


# hit
The monkey should be some kind of champion in its art. The coconut 
hits me squarely in the face with the elegance of a brick. I also 
take the emoitional damage of remembering what bricks are but not 
who I am.
\\ DAMAGE 2
>6 health >>> flee

At least I feel like my tolerance for pain has increased from all 
the beating I took. Or maybe I only now discovered that I can take 
a beating and keep standing perfectly fine.
|
`[cyan]+2 max health[yellow]
+2 max_health
>>> flee


# flee
Perhaps because I have become a target for coconut-throwing, I am 
still thoroughly confused. So I should be forgiven in noticing late 
that the perpetrator is now running away. 
|
Is it... screeching mockingly? Does it perchance have sentience?
|
>>> chase,think,look,eat

  # chase
  Enraged, I follow the monkey into a jungle. It has the home advantage, 
  but I embrace my anger, feeling myself going [cyan]berserk[reset]. How dare 
  the simian play with me that way?
  |
  I soon learn that both my anger and hopes of releasing it by smacking 
  the creature at least once are misplaced. For I both lost both my
  quary and my way in the dense forestation. If there is use for anger, 
  that is not for hunters.
  |
  = "berserk" trait
  >>> jungle depths

  # think
  <13 intellect >>> think

  I take the chance to think things through, discovering that I can work my 
  brain more and more. I am just learning about myself afterall!
  \\ GAIN +1 intellect

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
  Though my origin is still a mystery to me, I am positive that animals 
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
  Worries about a monkey -that is no longer around- have abated.
  \\ GAIN +2 health
  
  I take the other coconut with me as provisions - a rock can pry 
  it open much better than my head. Also, is my head so sturdy so as 
  to break this hard shell open? Unable to answer the question, yet 
  satiated, I look around.
  \\ GAIN +1 provisions
  >>> look

  # look
  >>> places


# places
  By now, the dust that had maybe coincided with my arrival has fully 
  settled down. There is no wind blowing, after all. 
  |
  In the distance, a tall mountain can be seen. But nearby a dirt
  trail winds away. Lastly, in the direction the monkey fled, there
  is a dense jungle. I am in a kind of junction between the three.
  ?20 _chance_
  >[_chance_] sight [end]Of the three, the trail looks most promising, as it has wagon-tracks.
  >[_chance_] sight Surely it leeds to some city. I squint, and sure enough spot chimney
  >[_chance_] sight smoke in the distance. Having such keen sight feels good, and I 
  >[_chance_] sight push my glases u-. Sorry, there's no such item on me. I just touch 
  >[_chance_] sight the top of my nose. A habit it seems.
  <[_chance_] sight [end]I weigh my options but don't have much to ponder on. 
  |
  = "trail" _trail_
  >[_chance_] sight = "city" _trail_
  >>> jungle,mountain,[_trail_]

# jungle
The jungle seems like a wild place. But there is a draw to it; the
smell of adventure! Surely I want to go there. Or do I? Meh, I will
not change my mind.
|
Most conveniently, it is close by - I am practically standing at its
fringes. So let us consider this the workings of fate, shall we?
|
Soon I realize there is no fate, no loving higher power at work that 
positioned me close to the accursed place. For I am not enjoying 
myself. At all.
| 
>>> jungle depths

# mountain
="MOUNTAIN" progress
After some deliberation, I figure getting to a high vantage point
might help me gain a sense for the lay of the land. So on to the
mountains!
|
The road towards the mountain is long. Minutes stretch into hours.
Yes, the terms are familiar, no there is no recollection of the 
learning process. In a more serious note, I grow weary. 
|
= "hot" _next_
?20 _chance_
<10 _chance_ = "rainy" _next_
>>> [_next_]

  # hot
  Above me, the sun burns scalding hot and I feel my motivation 
  draining. It took longer than advised to notice my dehydration.
  |
  `[red]-2 health[yellow]
  -2 health
  >>> shelter

  # rainy
  Something pokes the top of my head. Then again, and again.
  Hey, I know whis feeling! I look up at the dark clouds hiding
  the sun for verification. Indeed, this is rain.
  |
  >>> shelter

  # shelter
  > 0 provisions It is prudent to find shelter, but then I will need to dig
  > 0 provisions into my scant provisions while waiting for long. Maybe it's
  > 0 provisions ok, because they are delicious.[end]
  @ 0 provisions It is prudent to find shelter, but then I have no provisions
  @ 0 provisions and I fear I will perish from hunger. I regret not picking up
  @ 0 provisions some coconuts, at least those trajectorized at my head.[end]
  I am not too far, so perhaps I can also weather the weather in the
  jungle? On the other hand, the mountain is a nice vantage point. Well,
  there are options aplenty, but I know what I'm doing! Definitely!
  |
  >>> shelter,go on,jungle

  # jungle 
  With tired steps, I trace my way to the jungle as the hazardous nature 
  does its best to hammer home ... that this is not my home. Tired, I mistep 
  in the unsteady terrain and sprain my ankle horribly just a little bit
  before the first trees.
  \\ DAMAGE 3
  I curse the sky or abstractly whichever gods exist in the lands. For I 
  have forgotten mine. so I move in deeper and deeper. However, even if the 
  thick canopy overhead forms an safe shelter from heat,cold,or rain, 
  I feel like I have traded one kind of peril for another.
  |
  >>> jungle depths

  # go on
  I reach the mountain by nightfall. It seems any amount of speed
  is useless if your endurance is low. So it's strength one should
  rely on to cover long distances. Burning muscles are not good 
  for the health. Especially under extreme weather.
  |
  ?20 _chance_
  =2 _damage_
  > [_chance_] strength = 0 _damage_
  `[red]-[_damage_] health[yellow]
  -[_damage_] health
  >>> vantage

  # vantage
  Anyway, the view is breathtaking. I see the endlessly expanding
  jungle - wise to not wander in its depths. I see 
  |
  >>> death

  # shelter
  I tough out the weather under the shade of a large rock. A very
  large rock. No, you did not get me, a VERY LARGE rock. Which is why 
  it was easy to spot from very far away. If we were in the sea, 
  I would expect a lighthouse on top of that tower-like shape.
  |
  My wait ends up being lengthy, and I naturally get hungry, what with
  all the thrills and actually coming this far.
  \\ HUNGRY
  ? 20 _chance_
  > [_chance_] intellect What is this huge specimen of mansonry doing here? I am
  > [_chance_] intellect saying "mansonry" because this is the only conceivable explanation
  > [_chance_] intellect of why the rock is composed of several smoother segments.[end]
  @"curious" trait My curiocity is piqued. I think it is supposed to kill cats or
  @"curious" trait something, but whatever I am no cat. Perhaps.
  |
  @"curious" trait >>> death
  >>> death

# jungle depths
="JUNGLE" progress
The jungle is hot and sticky, and generally a pain to move
through. The tall overarching trees create flickering shadows
that mess with one's sense of direction.
|
With all hopes of finding my way forward or backward lost
under the canopy of leaves. Spiderwebs occasionally cling to 
me, but thankfully none of the large spiders weaving them take 
a fancy of my flesh.
|
>>> death

# trail
="TRAIL" progress
>>> city

# city
="CITY" progress
Having a clear sense of direction means that I do not get
confused by the trailing winding away from it. I walk and
walk just before soft rain starts falling.
|
It rings playfully at the cobblestone. Pitter-patter.
|
>>> death


# death
= "END" progress
`Last breath
Death looms over me. Silently. It waits for my last spark of thought 
and then to guide me into obscurity. The final bit of entropy going 
away makes my being whole. 
|
Now I know. I smile.
|
[purple]      Oh, silent specter, so misguided on your finality, 
[purple]      can a character perish while their story awaits?
|
>>> book end


# book end
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