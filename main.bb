final repeat(str value, int i) = {
    default shade = 0;
    ret = "";
    while(j in range(i)) ret += value;
    if(shade!=0) ret += bb.ansi.lightwhite;
    while(j in range(shade)) ret += value;
    if(shade!=0) ret += bb.ansi.reset;
    return ret;
}
final hbar = bb.ansi.cyan+repeat("-",60)+bb.ansi.reset;
final state = new {
    final max_line = 30;
    final max_width = 60;
    rand = random(0);
    stats = new {
        max_health = 10;
        health = 10;
        strength = 10;
        intellect = 10;
        sight = 10;
        speed = 10;
        social = 10;
    }
    tags = list::element("alive");
    running = true;
    lines = list::element("");
    player_info = {
        if(this.stats.health!=this.stats.max_health) {
            if(this.stats.health>6) print("▌  "+bb.ansi.green+repeat("❤",this.stats.health :: shade=this.stats.max_health-this.stats.health)+bb.ansi.reset)
                else if(this.stats.health>3) print("▌  "+bb.ansi.yellow+repeat("❤",this.stats.health :: shade=this.stats.max_health-this.stats.health)+bb.ansi.reset)
                    else print("▌  "+bb.ansi.red+repeat("❤",this.stats.health :: shade=this.stats.max_health-this.stats.health)+bb.ansi.reset);
        }
        if(this.stats.strength!=10)  print("▌  ✊ Strength  "+bb.ansi.cyan+str(this.stats.strength)+bb.ansi.reset);
        if(this.stats.intellect!=10) print("▌  🧠 Intellect "+bb.ansi.cyan+str(this.stats.intellect)+bb.ansi.reset);
        if(this.stats.sight!=10)     print("▌  👀 Sight     "+bb.ansi.cyan+str(this.stats.sight)+bb.ansi.reset);
        if(this.stats.speed!=10)     print("▌  🐾 Speed     "+bb.ansi.cyan+str(this.stats.speed)+bb.ansi.reset);
        if(this.stats.social!=10)    print("▌  🎭 Social  "+bb.ansi.cyan+str(this.stats.social)+bb.ansi.reset);
    }
    draw = {
        print(bb.ansi.clear_screen);

        end = this.lines|len;
        if(end>this.max_line) first = end-this.max_line else first = 0;
        while(i in range(first, end)) print(this.lines[i]);
    }
    has(text) = {
        while(tag in this.tags) if(tag==text) return true;
        return false;
    }
    progress(text) = {
        default prefix = "";
        default question = bb.ansi.yellow+prefix+bb.ansi.cyan+">>"+bb.ansi.reset;
        start = -1;
        line = "";
        while(i in text|len|range) {
            if(line|len>this.max_width) {this.lines << line;line="";}
            if(text[i]==" ") {line += text[range(start+1, i+1)]; start = i;}
        }
        line += text[range(start+1, text|len)];
        if(line|len|bool) this.lines << line;
        this.question = question;
        this.original_question = question;
        this.draw();
    }
    ask(options) = {
        default prefix = "";
        question = "";
        while(option in options) question += "["+option+"] ";
        question = prefix+bb.ansi.yellow+question+"\n"+bb.ansi.cyan+">>"+bb.ansi.reset;
        this.question = question;
        this.original_question = question;
        this.draw();
        while(true) {
            command = read(this.question);
            contained = false;
            while(option in options) if(option==command) return command;
            this.draw();
        }
    }
}

final generics = {
    if(command=="leave") {state.progress("Thus ends my story."); return;}
}

final intro_wake = {
    state.progress("Ugh! What happened? Where is this? Wait! More importantly; who am I? If only this dust could settle... Maybe I could - hang on, what could I do again? Seems I know nothing.\n");
    command = state.ask(list("think", "stand", "look"));
    generics:
    if(command=="think") intro_think();
    if(command=="stand") intro_stand();
    if(command=="look") intro_look();
}

final intro_think = {
    state.progress("My head hurts terribly whenever I try to remember. Only the name !{bb.ansi.cyan}Haian!{bb.ansi.reset} sounds familiar to my mind.\n");
    state.progress("But I cannot make out who that is supposed to be. Let's just be thankful that I am not stripped of language or the ability to reason. I think therefore I am... I think.\n");
    command = state.ask(list::element("ok") :: prefix=bb.ansi.cyan+"+2 intellect ");
    state.stats.intellect += 2;
    intro_hit:
}

final intro_stand = {
    state.progress("I saumersault from face down to standing up. My body is surprisingly muscular, it seems. Sense of balance is alright too. I probably worked out or something, though I get the feeling that I shouldn't be that type of person. A mystery, perhaps for another time. Who cares?\n");
    command = state.ask(list::element("ok") :: prefix=bb.ansi.cyan+"+2 strength ");
    state.stats.strength += 2;
    intro_hit:
}

final intro_hit = {
    state.progress("A blunt pain on my head stops my train of thought. It hurts!\n");
    command = state.ask(list::element("ok") :: prefix=bb.ansi.red+"-2 health ");
    state.stats.health -= 2;
    intro_coconut:
}

final intro_look = {
    state.progress("Anyway, looking arround I can see the dust parting somewhat. Enough to make out a coconut zooming towards me! In my surprise, I barely avoid it by rolling away. I mechanically touch the bridge of my nose in triumph. 'Not on MY watch!' I shout.\n");
    command = state.ask(list::element("ok") :: prefix=bb.ansi.cyan+"+2 sight +1 speed ");
    state.stats.sight += 2;
    state.stats.speed += 1;
    intro_coconut:
}

final intro_coconut = {
    state.progress("Who did that? A short distance away, a monkey on top of a tree aims a second coconut towards me.\n");
    command = state.ask(list("dodge", "block", "wait"));
    generics:
    if(command=="block") {
        state.progress("I take the safe option of raising my arms to block the projectile. It smarts, but I withstand the attack. Maybe it will bruise a bit but nothing serious.\n");
        command = state.ask(list::element("ok") :: prefix=bb.ansi.cyan+"+1 strength "+bb.ansi.red+"-1 health");
        state.stats.health -= 1;
        state.stats.strength += 1;
        intro_flee:
    }
    else if(command=="dodge") {
        if(state.rand|next<0.5+0.1*(state.stats.speed-10)) {
            state.progress("It is trivial to dodge the telegraphed attack. I am getting good at this! Maybe I should start dodging for a living. What did I do for a living again? At best vague colors move in my memory.\n");
            state.ask(list::element("ok") :: prefix=bb.ansi.cyan+"+2 speed ");
            state.stats.speed += 2;
            intro_flee:
        }
        else {
            state.progress("I fail to properly move out of the way. If only I was faster... But you cannot cry over spilled mango juice. No, this sounds a bit wrong but I fail to recall how the true saying goes.");
            intro_hit2:
        }
    }
    else if(command=="wait") {
        state.progress("I laugh, finding the situation hilariously funny. No, I will not dodge! I will stand there and take the hit - to make a statement.");
        intro_hit2:
    }
}

final intro_hit2 = {
    state.progress("The monkey should be some kind of champion in the art. The coconut hits me squarely in the face with the elegance of a brick. Damage aside, I also take the emoitional damage of remembering what bricks are but not who I am.\n");
    command = state.ask(list::element("ok") :: prefix=bb.ansi.red+"-2 health ");
    state.stats.health -= 2;
    if(state.stats.health<7) {
        state.progress("At least I feel like my tolerance for pain has increased from all the beating I took. Or maybe I only now discovered that I can take a beating and keep standing perfectly fine.\n");
        command = state.ask(list::element("ok") :: prefix=bb.ansi.cyan+"+2 max health ");
        state.stats.max_health += 2;
    }
    intro_flee:
}
final intro_flee = {
    state.progress("Despite being physically occupied as a target for a mischievous monkey, I am still thoroughly confused. So I should be forgiven in noticing late that the monkey is now running away. Is it... screetching mockingly? Wait! Does it perchance have sentience?\n");
    command = state.ask(list("chase", "think", "look", "eat"));
    generics:
    if(command=="chase") {intro_flee_chase:}
    else if(command=="think") {intro_flee_think:}
    else if(command=="look") {
        state.progress("I ignore the fleeing annoyance. It's only an animal after all in my eyes, even if I suspect otherwise. No, I am a stranger in a strange land, and even worse a stranger to myself. I should hence remain vigilant and keep an eye out. Yes, I am resolved to be !{bb.ansi.cyan}cautious!{bb.ansi.reset}.");
        state.tags << "cautious";
        start_story:
    }
    else if(command=="eat") {
        state.progress("I ignore the fleeing lifeform, whatever it may be. For I just realized that what the coconuts have taken away, the coconuts can give. No, it doesn't sound right, but at any rate I am famished and food is always nice for recuperating, right? It's definitely not because I imagine them to be tasty and this takes priority over everything else. Ok, ok, you got me. In truth, my journey of self-discovery opens with the sad truth that I am a {bb.ansi.cyan}glutton!{bb.ansi.reset}. If you'll excuse me, I will cry while stuffing myself with this coconut's nice-smelling filling.");
        state.tags << "glutton";
        intro_flee_eat:
    }
}

final intro_flee_chase = {
    state.progress("Enraged I follow the monkey into a jungle. It has the home advantage, but I embrace my anger, feeling myself going !{bb.ansi.cyan}berserk!{bb.ansi.reset}. How dare the simian play with me that way?\n");
    state.progress("But I soon learn that both my anger and hopes of releasing it by smacking the creature at least once are misplaced. For I both lost the creature in the dense forestation and also lost my way. It seems there is a place for anger, but not for hunters.\n");
    state.tags << "berserk";
    start_story_jungle:
}

final intro_flee_think = {
    if(state.stats.intellect>12) {
        state.progress("I take the chance to think things through, discovering that I can work my brain more and more. I am just learning about myself afterall!\n");
        command = state.ask(list::element("ok") :: prefix=bb.ansi.cyan+"+1 intellect ");
        state.stats.intellect += 1;
        state.progress("But I have reached the state of knowing a lot about my superfloous qualities. I do not think I will be surprising myself in other areas, though of course this can always be fixed with good-old -I shudder imagining it- training or practice.\n");
        state.progress("ANYWAY! Where were we? Ah, the monkey. It has long been gone, because I started overthinking.\n");
    }
    state.progress("Though I cannot recall from where I come, I am positive that in all my life animals have just been animals. Therefore, it holds to reason that this should be a different world, right? If you eliminate all possibilities, the one that remains must be true, however improbable.\n");
    state.progress("Who said that? ... Can't remember... Though it seems my old world has remained ingrained in my subconsious. I am now !{bb.ansi.cyan}curious!{bb.ansi.reset} to explore this new one and be taken by surprise even if I do not recall exactly why. For, if even the animals have thoughts, imagine the marvels a civilization could have reached!\n");
    state.tags << "curious";
    command = state.ask(list("look", "eat"));
    generics:
    if(command=="eat") {intro_flee_eat:}
    start_story:
}

final intro_flee_eat = {
    if(state.stats.health>=state.stats.max_health) state.stats.health = state.stats.max_health;
    state.progress("Before further action, I stoop to grab the coconuts, one of which is cracked and that I am able to pry open. It is as delicious as it was painful to get hit by! I take the other with me as provisions. As I feel my vitality returning from the land of the hungry, my resolve becomes always carry around stuff as delicious as that.\n");
    command = state.ask(list::element("ok") :: prefix=bb.ansi.cyan+"+2 health ");
    state.stats.health += 2;
    command = state.ask(list("look"));
    generics:
    start_story:
}

final start_story = {}
final start_story_jungle = {}
final start_story_city = {}


intro_wake();

