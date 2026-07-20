# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

The scoring in `src/recommender.py` compares genre and mood with an exact `==`
check, so it has no idea that related styles like "rock" and "metal" or moods
like "sad" and "melancholic" are close — a song is either an exact match or
worth nothing on that feature. Because a genre match is worth +2.0, which is
more than any other single feature, genre can dominate: a song can win mostly
for having the right label even when another song fits the listener's mood,
energy, and acoustic taste better. The catalog in `data/songs.csv` is also tiny
(only 20 songs, with some genres like metal represented by a single track), so
the same versatile songs keep resurfacing across different profiles and the
system can behave like a filter bubble, mostly returning songs similar to what
the user already described. Finally, the numeric features (energy, valence,
acousticness, and so on) were assigned by hand for this simulation rather than
measured from the audio, so they may not match how a real listener would
perceive a song, and conflicting profiles can receive technically high-scoring
but musically strange recommendations, as the metal-fan profile that was handed
a soft classical piece shows.

---

## 7. Evaluation  

To check whether the recommender behaves the way a listener would expect, I ran
it for four different taste profiles and looked at the top five songs for each.

### The four profiles tested

1. **High-Energy Pop** — favorite genre pop, mood happy, target energy 0.90, does not like acoustic.
2. **Chill Lofi** — favorite genre lofi, mood chill, target energy 0.35, likes acoustic.
3. **Deep Intense Rock** — favorite genre rock, mood intense, target energy 0.85, does not like acoustic.
4. **Adversarial / Conflicting** — favorite genre metal, mood melancholic, target energy 0.20, likes acoustic. This profile is contradictory on purpose, because metal songs are usually loud and non-acoustic, yet the listener also asked for low energy and acoustic music.

### What the system recommended (original weights)

The number-one pick for each profile was:

- High-Energy Pop → **Sunrise City** by Neon Echo (score 5.24)
- Chill Lofi → **Library Rain** by Paper Lanterns (score 5.36)
- Deep Intense Rock → **Storm Runner** by Voltline (score 5.34)
- Adversarial / Conflicting → **Winter Nocturne** by Amelie Rousseau (score 3.43)

The full top-five terminal output for each profile:

```
PROFILE: High-Energy Pop  (genre=pop, mood=happy, target_energy=0.9, likes_acoustic=False)
1. Sunrise City    - Neon Echo      Score 5.24  [Genre +2.0, Mood +1.5, Energy +0.92, Acoustic +0.82]
2. Gym Hero        - Max Pulse      Score 3.92  [Genre +2.0, Energy +0.97, Acoustic +0.95]
3. Rooftop Lights  - Indigo Parade  Score 3.01  [Mood +1.5, Energy +0.86, Acoustic +0.65]
4. Neon Pulse      - Voltage Kids   Score 1.92  [Energy +0.95, Acoustic +0.97]
5. Storm Runner    - Voltline       Score 1.89  [Energy +0.99, Acoustic +0.90]

PROFILE: Chill Lofi  (genre=lofi, mood=chill, target_energy=0.35, likes_acoustic=True)
1. Library Rain        - Paper Lanterns  Score 5.36  [Genre +2.0, Mood +1.5, Energy +1.00, Acoustic +0.86]
2. Midnight Coding     - LoRoom          Score 5.14  [Genre +2.0, Mood +1.5, Energy +0.93, Acoustic +0.71]
3. Focus Flow          - LoRoom          Score 3.73  [Genre +2.0, Energy +0.95, Acoustic +0.78]
4. Spacewalk Thoughts  - Orbit Bloom     Score 3.35  [Mood +1.5, Energy +0.93, Acoustic +0.92]
5. Coffee Shop Stories - Slow Stereo     Score 1.87  [Energy +0.98, Acoustic +0.89]

PROFILE: Deep Intense Rock  (genre=rock, mood=intense, target_energy=0.85, likes_acoustic=False)
1. Storm Runner      - Voltline          Score 5.34  [Genre +2.0, Mood +1.5, Energy +0.94, Acoustic +0.90]
2. Gym Hero          - Max Pulse         Score 3.37  [Mood +1.5, Energy +0.92, Acoustic +0.95]
3. Starlight Parade  - Aurora Line       Score 1.88  [Energy +0.97, Acoustic +0.91]
4. Neon Pulse        - Voltage Kids      Score 1.87  [Energy +0.90, Acoustic +0.97]
5. Iron Veins        - Blacklight Forge  Score 1.84  [Energy +0.88, Acoustic +0.96]

PROFILE: Adversarial / Conflicting  (genre=metal, mood=melancholic, target_energy=0.2, likes_acoustic=True)
1. Winter Nocturne     - Amelie Rousseau   Score 3.43  [Mood +1.5, Energy +0.98, Acoustic +0.95]
2. Paper Boats         - Hollow Pines      Score 3.25  [Mood +1.5, Energy +0.87, Acoustic +0.88]
3. Iron Veins          - Blacklight Forge  Score 2.27  [Genre +2.0, Energy +0.23, Acoustic +0.04]
4. Spacewalk Thoughts  - Orbit Bloom       Score 1.84  [Energy +0.92, Acoustic +0.92]
5. Coffee Shop Stories - Slow Stereo       Score 1.72  [Energy +0.83, Acoustic +0.89]
```

### Comparing the profiles

Comparing **High-Energy Pop with Chill Lofi** shows the recommender doing its
job well: the pop listener is sent a bright, high-energy pop song (Sunrise City),
while the lofi listener is sent a calm, acoustic study track (Library Rain), and
the two lists share no songs. Because these profiles disagree on genre, mood,
energy, and acoustic preference all at once, the recommendations point in
completely opposite directions, which is exactly what we would hope to see.

Comparing **Chill Lofi with Deep Intense Rock** shows the same healthy split
from the other direction: the lofi list is full of quiet, acoustic songs with
low energy, while the rock list is led by a loud, intense, non-acoustic song
(Storm Runner). The one song that shows up on both lists is only in the lower
ranks, and it appears through energy and acoustic points rather than a genre or
mood match, so the top of each list stays clearly separated.

Comparing **Deep Intense Rock with the Conflicting profile** is the most
revealing. The rock profile is coherent, so its favorite genre, mood, and energy
all reinforce the same song and it earns a high 5.34. The conflicting profile
cannot do this, because no single song is both metal and low-energy and
acoustic, so the winner (Winter Nocturne) is actually a soft classical piece
that matches the mood, energy, and acoustic wish but not the requested genre at
all. In other words, when the preferences fight each other the system quietly
drops the genre the listener asked for and rewards the three preferences that
can be satisfied together.

### One first-place result explained with the formula

The clearest example is Chill Lofi's winner, **Library Rain**. Its genre is
lofi, which matches, so it earns +2.0. Its mood is chill, which matches, so it
earns +1.5. Its energy is 0.35, exactly the target, so the energy score is
`1 - |0.35 - 0.35| = 1.00`. The listener likes acoustic music and the song's
acousticness is 0.86, so acoustic fit adds +0.86. Adding these gives
`2.0 + 1.5 + 1.00 + 0.86 = 5.36`, the highest score in that list.

### The weight-shift experiment

I re-ran all four profiles with an experimental set of weights that lowers genre
from 2.0 to 1.0 and doubles energy from 1.0 to 2.0 (mood and acoustic stay the
same). The number-one pick did not change for any of the four profiles, but the
lower ranks moved. The most important change was in the conflicting profile:
under the original weights the only true metal song, Iron Veins, still squeezed
into third place on the strength of its +2.0 genre match, but once genre was
worth only +1.0 and energy was worth double, Iron Veins (energy 0.97 against a
target of 0.20) fell out of the top five entirely. A short before/after of the
changed top results:

```
                    ORIGINAL top 5                 EXPERIMENT top 5 (genre 1.0, energy 2.0)
High-Energy Pop:    ...#4 Neon Pulse, #5 Storm      ...#4 Storm Runner, #5 Neon Pulse (swapped)
Chill Lofi:         #3 Focus Flow, #4 Spacewalk     #3 Spacewalk Thoughts, #4 Focus Flow (swapped)
Deep Intense Rock:  #5 Iron Veins                   #5 Sunrise City (Iron Veins drops out)
Conflicting:        #3 Iron Veins (the metal song)  Iron Veins drops out; #4 Library Rain enters
```

### More accurate, or just different?

Emphasizing energy made the results *different* rather than clearly *more
accurate*. For the three coherent profiles the winners were already correct, so
raising the energy weight only reshuffled songs that were near-ties anyway. For
the conflicting profile the experiment arguably made things worse for that
listener: it removed the one song that actually matched their stated genre. The
experiment is useful because it shows how sensitive the lower ranks are to the
weights, but it does not give a better answer overall.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
