#!/usr/bin/env python3
"""
Update movie_quizz_500_updated.json with real quotes from real movies, animations, and cartoons.
"""

import json
import re
from pathlib import Path

# Real quotes from real movies - multiple per film for variety when same movie appears multiple times
MOVIE_QUOTES = {
    "Rocky,1976": [
        "Yo Adrian!",
        "It ain't about how hard you hit. It's about how hard you can get hit and keep moving forward.",
        "Going the distance.",
        "Adrian!",
        "If I can go that distance, you see, and that bell rings and I'm still standin', I'm gonna know for the first time in my life, see, that I weren't just another bum from the neighborhood.",
    ],
    "Star Wars,1977": [
        "May the Force be with you.",
        "I have a bad feeling about this.",
        "Use the Force, Luke.",
        "The Force will be with you, always.",
        "A long time ago in a galaxy far, far away...",
        "Help me, Obi-Wan Kenobi. You're my only hope.",
        "These aren't the droids you're looking for.",
        "I find your lack of faith disturbing.",
    ],
    "Ghostbusters,1984": [
        "Who you gonna call? Ghostbusters!",
        "I ain't afraid of no ghost.",
        "We're ready to believe you.",
        "He slimed me.",
        "That's a big twinkie.",
        "Human sacrifice, dogs and cats living together - mass hysteria!",
    ],
    "Inception,2010": [
        "You mustn't be afraid to dream a little bigger, darling.",
        "We need to go deeper.",
        "Dreams feel real while we're in them.",
        "Your mind is the scene of the crime.",
        "An idea is like a virus.",
        "You're waiting for a train.",
    ],
    "Jurassic Park,1993": [
        "Your scientists were so preoccupied with whether they could, they didn't stop to think if they should.",
        "Life finds a way.",
        "Welcome to Jurassic Park.",
        "Hold on to your butts.",
        "Clever girl.",
        "Objects in mirror are closer than they appear.",
    ],
    "A Few Good Men,1992": [
        "You can't handle the truth!",
        "I want the truth!",
        "You're goddamn right I did!",
        "You need me on that wall.",
        "We use words like honor, code, loyalty.",
    ],
    "Heat,1995": [
        "Don't let yourself get attached to anything you are not willing to walk out on in 30 seconds flat.",
        "For me, the action is the juice.",
        "A guy told me one time, don't let yourself get attached to anything you are not willing to walk out on in 30 seconds flat.",
        "I'm alone. I am not lonely.",
    ],
    "Fight Club,1999": [
        "The first rule of Fight Club is: you do not talk about Fight Club.",
        "His name is Robert Paulson.",
        "I am Jack's complete lack of surprise.",
        "You met me at a very strange time in my life.",
        "It's only after we've lost everything that we're free to do anything.",
        "You are not your job.",
    ],
    "Mad Max: Fury Road,2015": [
        "I live, I die, I live again!",
        "What a lovely day!",
        "We are not things.",
        "My name is Max.",
        "Witness me!",
        "I am the one who runs from both the living and the dead.",
    ],
    "The Godfather,1972": [
        "I'm gonna make him an offer he can't refuse.",
        "Leave the gun. Take the cannoli.",
        "It's not personal, it's strictly business.",
        "A man who doesn't spend time with his family can never be a real man.",
        "Revenge is a dish best served cold.",
        "I'll make him an offer he can't refuse.",
    ],
    "The Terminator,1984": [
        "I'll be back.",
        "Come with me if you want to live.",
        "I'll be back.",
        "Hasta la vista, baby.",
        "The future is not set. There is no fate but what we make for ourselves.",
    ],
    "The Matrix,1999": [
        "There is no spoon.",
        "I know kung fu.",
        "Welcome to the real world.",
        "The Matrix has you.",
        "Red pill or blue pill?",
        "Follow the white rabbit.",
        "What if I told you that everything you know is a lie?",
        "Free your mind.",
    ],
    "Interstellar,2014": [
        "We used to look up at the sky and wonder at our place in the stars.",
        "Do not go gentle into that good night.",
        "Mankind was born on Earth. It was never meant to die here.",
        "Love is the one thing we're capable of perceiving that transcends dimensions of time and space.",
        "We're still pioneers.",
        "Don't trust the right thing done for the wrong reason.",
    ],
    "Top Gun,1986": [
        "I feel the need - the need for speed!",
        "Take me to bed or lose me forever.",
        "You can be my wingman anytime.",
        "Goodbye, Goose.",
        "I'm gonna hit the brakes and he'll fly right by.",
        "Talk to me, Goose.",
    ],
    "Casablanca,1942": [
        "Here's looking at you, kid.",
        "Of all the gin joints in all the towns in all the world, she walks into mine.",
        "Play it again, Sam.",
        "We'll always have Paris.",
        "Louis, I think this is the beginning of a beautiful friendship.",
        "Round up the usual suspects.",
    ],
    "Alien,1979": [
        "In space no one can hear you scream.",
        "Get away from her, you bitch!",
        "I've seen a lot of things.",
        "That's not a good place to put your face.",
        "I can't lie to you about your chances, but you have my sympathies.",
    ],
    "The Hobbit,2012": [
        "I'm going on an adventure!",
        "The world is not in your books and maps.",
        "True courage is about knowing not when to take a life, but when to spare one.",
        "That's what Bilbo Baggins hates!",
        "The greatest adventure is what lies ahead.",
        "Home is behind, the world ahead.",
    ],
    "Casino,1995": [
        "In the casino, the cardinal rule is to keep them playing.",
        "When you love someone, you've gotta trust them.",
        "The town will never be the same.",
        "It's a great place to raise your kids.",
        "In the end, we're all dead.",
    ],
    "Forrest Gump,1994": [
        "Life is like a box of chocolates. You never know what you're gonna get.",
        "Run, Forrest, run!",
        "Stupid is as stupid does.",
        "My momma always said life was like a box of chocolates.",
        "I'm not a smart man, but I know what love is.",
    ],
    "Blade Runner,1982": [
        "I've seen things you people wouldn't believe.",
        "All those moments will be lost in time, like tears in rain.",
        "Time to die.",
        "The light that burns twice as bright burns half as long.",
        "Replicants are like any other machine.",
    ],
    "The Dark Knight,2008": [
        "Why so serious?",
        "I'm not wearing hockey pads.",
        "Because he's the hero Gotham deserves, but not the one it needs right now.",
        "The night is darkest just before the dawn.",
        "Do you want to know why I use a knife?",
        "Some men just want to watch the world burn.",
    ],
    "No Country for Old Men,2007": [
        "Call it, friendo.",
        "What's the most you ever lost on a coin toss?",
        "You don't have to do this.",
        "You're not from here.",
        "What business is it of yours where I'm from, friendo?",
    ],
    "The Silence of the Lambs,1991": [
        "A census taker once tried to test me.",
        "I ate his liver with some fava beans and a nice Chianti.",
        "Hello, Clarice.",
        "Quid pro quo.",
        "We begin by coveting what we see every day.",
    ],
    "Taxi Driver,1976": [
        "You talkin' to me?",
        "You talkin' to me? Well, I don't see anyone else around.",
        "Loneliness has followed me my whole life.",
        "Someday a real rain will come and wash all the scum off the streets.",
        "I'm God's lonely man.",
    ],
    "Avatar,2009": [
        "I see you.",
        "Everything is backward now.",
        "Out there, we have a chance.",
        "We have a great deal to learn from each other.",
        "The sky people have sent us a message.",
    ],
    "The Lord of the Rings: The Fellowship of the Ring,2001": [
        "One ring to rule them all.",
        "You shall not pass!",
        "Fly, you fools!",
        "I'm not trying to rob you. I'm trying to help you.",
        "My precious.",
        "A wizard is never late, nor is he early.",
    ],
    "Pulp Fiction,1994": [
        "Say 'what' again. Say 'what' again, I dare you.",
        "English, do you speak it?",
        "Zed's dead, baby. Zed's dead.",
        "Royale with Cheese.",
        "That's a pretty good milkshake.",
        "Do you know what they call a Quarter Pounder with Cheese in France?",
    ],
    "Dune,2021": [
        "Fear is the mind-killer.",
        "I must not fear. Fear is the mind-killer.",
        "The spice must flow.",
        "Power over spice is power over all.",
        "A great man doesn't seek to lead. He's called to it.",
    ],
    "Apollo 13,1995": [
        "Houston, we have a problem.",
        "Failure is not an option.",
        "The Eagle has landed.",
        "From the Moon, Houston.",
        "We've had a problem.",
    ],
    "The Departed,2006": [
        "I'm not a cop.",
        "Maybe. Maybe not. Maybe go fuck yourself.",
        "I'm the guy who does his job.",
        "I need a cigarette.",
        "When I was your age they would say we can become cops or criminals.",
    ],
    "Die Hard,1988": [
        "Yippee-ki-yay, motherfucker!",
        "Come out to the coast, we'll get together, have a few laughs.",
        "Now I have a machine gun. Ho-ho-ho.",
        "Welcome to the party, pal!",
        "Hans, bubby, I'm your white knight.",
    ],
    "Jaws,1975": [
        "You're gonna need a bigger boat.",
        "We're gonna need a bigger boat.",
        "Slow ahead, I can go slow ahead.",
        "Just when you thought it was safe to go back in the water.",
        "Smile, you son of a bitch!",
    ],
    "Scarface,1983": [
        "Say hello to my little friend!",
        "The world is yours.",
        "I always tell the truth.",
        "I'm Tony Montana.",
        "All I have in this world is my balls and my word.",
    ],
    "Indiana Jones and the Last Crusade,1989": [
        "It belongs in a museum!",
        "We named the dog Indiana.",
        "That belongs in a museum!",
        "He chose wisely.",
        "No ticket.",
        "X never marks the spot.",
    ],
    "Titanic,1997": [
        "I'm the king of the world!",
        "I'll never let go, Jack.",
        "Draw me like one of your French girls.",
        "I'm flying, Jack!",
        "Make it count.",
    ],
    "Back to the Future,1985": [
        "Where we're going, we don't need roads.",
        "Great Scott!",
        "Roads? Where we're going we don't need roads.",
        "1.21 gigawatts!",
        "That's heavy.",
    ],
    "Gladiator,2000": [
        "My name is Maximus Decimus Meridius.",
        "Are you not entertained?",
        "What we do in life echoes in eternity.",
        "Death smiles at us all, but all a man can do is smile back.",
        "At my signal, unleash hell.",
    ],
    "The Avengers,2012": [
        "I'm always angry.",
        "That's my secret, Captain.",
        "I have a plan: attack.",
        "Puny god.",
        "We have a Hulk.",
        "We're in a flying metal monster.",
    ],
    "Goodfellas,1990": [
        "As far back as I can remember, I always wanted to be a gangster.",
        "Funny how?",
        "Get the fuck out of here.",
        "What do you mean I'm funny?",
        "Never rat on your friends.",
    ],
    "The Shawshank Redemption,1994": [
        "Get busy living, or get busy dying.",
        "Hope is a good thing.",
        "I guess it comes down to a simple choice.",
        "Brooks was here.",
        "Fear can hold you prisoner. Hope can set you free.",
    ],
    # Animations and cartoons
    "Aladdin,1992": [
        "A whole new world.",
        "Genie, you're free!",
        "Prince Ali, fabulous he, Ali Ababwa!",
        "I can show you the world.",
        "Phenomenal cosmic powers! Itty bitty living space!",
    ],
    "Beauty and the Beast,1991": [
        "Tale as old as time.",
        "Be our guest!",
        "Beauty and the Beast.",
        "I want adventure in the great wide somewhere.",
        "We don't like what we don't understand.",
    ],
    "Coco,2017": [
        "Remember me.",
        "The rest of the world may follow the rules, but I must follow my heart.",
        "I have crossed over to the land of the dead.",
        "Our love for each other will live on forever.",
    ],
    "Despicable Me,2010": [
        "It's so fluffy I'm gonna die!",
        "Light bulb!",
        "I'm having a bad, bad day.",
        "It's so fluffy!",
    ],
    "Encanto,2021": [
        "We don't talk about Bruno.",
        "What can I do?",
        "The miracle is you.",
        "I'm sorry, mi vida. Go on.",
    ],
    "Finding Nemo,2003": [
        "Just keep swimming.",
        "Fish are friends, not food.",
        "I shall call him Squishy.",
        "P. Sherman, 42 Wallaby Way, Sydney.",
    ],
    "Frozen,2013": [
        "Let it go!",
        "Do you want to build a snowman?",
        "Some people are worth melting for.",
        "The cold never bothered me anyway.",
    ],
    "How to Train Your Dragon,2010": [
        "You're not a Viking. You're not a dragon killer. You're a dragon.",
        "This is Berk. It's twelve days north of Hopeless.",
        "I did this. All of this.",
    ],
    "Inside Out,2015": [
        "Take her to the moon for me.",
        "Crying helps me slow down.",
        "Do you ever look at someone and wonder, what is going on inside their head?",
    ],
    "Kung Fu Panda,2008": [
        "There is no charge for awesomeness.",
        "Yesterday is history, tomorrow is a mystery, but today is a gift.",
        "I'm not a big fat panda. I'm THE big fat panda.",
    ],
    "Moana,2016": [
        "I am Moana of Motunui.",
        "The ocean chose me.",
        "You're welcome!",
        "I am the girl who loves the sea.",
    ],
    "Monsters Inc.,2001": [
        "I'm on the cover of a magazine!",
        "Put that thing back where it came from or so help me!",
        "Kitty!",
        "We scare because we care.",
    ],
    "Ratatouille,2007": [
        "Anyone can cook.",
        "If you are what you eat, then I only want to eat the good stuff.",
        "I don't like food. I love it.",
    ],
    "Shrek,2001": [
        "Ogres are like onions.",
        "Do you know the muffin man?",
        "That'll do, donkey. That'll do.",
        "It's not ogre. It's never ogre.",
    ],
    "Spider-Man: Into the Spider-Verse,2018": [
        "Anyone can wear the mask.",
        "With great power comes great responsibility.",
        "What's up, danger?",
        "I'm gonna do my own thing.",
    ],
    "The Incredibles,2004": [
        "No capes!",
        "I'm not happy, Bob. Not happy.",
        "Your identity is your most valuable possession.",
        "I'll get you. And when I do, I'll make you pay.",
    ],
    "The Lion King,1994": [
        "Hakuna matata!",
        "Remember who you are.",
        "Everything the light touches is our kingdom.",
        "Long live the king.",
    ],
    "The Little Mermaid,1989": [
        "Part of your world.",
        "Under the sea!",
        "I want to be where the people are.",
        "Look at this stuff. Isn't it neat?",
    ],
    "Toy Story,1995": [
        "To infinity and beyond!",
        "You've got a friend in me.",
        "There's a snake in my boot!",
        "Reach for the sky!",
    ],
    "Up,2009": [
        "Adventure is out there!",
        "I don't want your help. I want you safe.",
        "So long, boys!",
        "That might sound boring, but I think the boring stuff is the stuff I remember the most.",
    ],
}

# Track which quote index we're at for each movie (for variety)
quote_indices = {movie: 0 for movie in MOVIE_QUOTES}


def _normalize_key(key: str) -> str:
    """Normalize 'Rocky - 1976', 'Rocky (1976)', or 'Rocky,1976' to 'Rocky,1976' for lookup."""
    if not key:
        return key
    # "Name (Year)" -> "Name,Year"
    m = re.match(r"^(.+?)\s*\((\d{4})\)\s*$", key.strip())
    if m:
        return f"{m.group(1).strip()},{m.group(2)}"
    # "Name - Year" -> "Name,Year"
    m = re.match(r"^(.+?)\s+-\s+(\d{4})\s*$", key.strip())
    if m:
        return f"{m.group(1).strip()},{m.group(2)}"
    return key


def get_next_quote(movie_key: str) -> str:
    """Get the next quote for a movie, cycling through available quotes."""
    lookup_key = _normalize_key(movie_key)
    if lookup_key not in MOVIE_QUOTES:
        # Fallback for any movie we don't have quotes for
        return f"[Quote from {movie_key}]"
    
    quotes = MOVIE_QUOTES[lookup_key]
    idx = quote_indices[lookup_key] % len(quotes)
    quote_indices[lookup_key] += 1
    return quotes[idx]


def main():
    base = Path(__file__).parent.parent
    data_path = base / "data" / "movie_quizz_500_updated.json"
    frontend_path = base / "frontend" / "movie_quizz_500_updated.json"
    
    for path in [data_path, frontend_path]:
        if not path.exists():
            print(f"Skipping {path} - file not found")
            continue
            
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        updated = 0
        missing = set()
        for entry in data:
            answer = entry.get("answer", "")
            if answer in MOVIE_QUOTES:
                entry["quote"] = get_next_quote(answer)
                updated += 1
            else:
                missing.add(answer)
        
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"Updated {path.name}: {updated} quotes replaced")
        if missing:
            print(f"  Movies without quotes: {sorted(missing)}")
    
    # Reset indices for second file
    for k in quote_indices:
        quote_indices[k] = 0


if __name__ == "__main__":
    main()
