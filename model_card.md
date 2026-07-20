# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeFinder 1.0**

VibeFinder is a small music recommender. Its goal is simple: you tell it the
kind of music you are in the mood for, and it suggests songs that fit. You
describe your taste with four things — your **favorite genre**, your
**favorite mood**, the **energy level** you want, and whether you **prefer
acoustic** music. VibeFinder then picks the songs that best match all of that.

Importantly, VibeFinder does **not** use machine learning. It uses a simple
weighted scoring system: each song earns points for how well it matches your
preferences, and the songs with the most points are recommended. This makes it
easy to understand exactly why any song was chosen.

---

## 2. Intended Use  

**Intended use.** VibeFinder is built for the classroom. It is meant to be a
hands-on demonstration that helps students understand how recommender systems
work, and a safe place to experiment with a scoring algorithm — for example, by
changing the weights and watching how the recommendations shift. It assumes the
user can describe their taste with one favorite genre, one favorite mood, a
target energy level, and an acoustic preference.

**Non-intended use.** VibeFinder should **not** be used for commercial music
streaming, to make personalized recommendations for millions of real users, or
to predict how real listeners will actually behave. It runs on a tiny,
hand-made catalog of 20 songs with numbers that were assigned by people, not
measured from real audio, so it simply is not built to make trustworthy
real-world predictions.

---

## 3. How the Model Works  

Think of VibeFinder as a judge that gives every song a score, then lines the
songs up from best to worst.

For each song, it compares the song to what you asked for and hands out points:

- If the song's **genre** matches your favorite genre, it earns the most points.
- If the song's **mood** matches your favorite mood, it earns a good chunk of
  points too.
- The closer the song's **energy** is to the energy level you wanted, the more
  points it earns — a song that is way too calm or way too loud earns fewer.
- Finally, it looks at your **acoustic** preference: if you like acoustic music,
  more acoustic songs earn more points, and if you don't, the opposite is true.

After every song has a score, VibeFinder ranks them from the highest score to
the lowest and returns the best few as your recommendations. Genre and mood
count for the most, so they steer the list, while energy and acoustic fit act
as tie-breakers that fine-tune the order.

---

## 4. Data  

VibeFinder uses a small catalog of **20 songs** stored in `data/songs.csv`. I
**expanded this dataset from the starter project**, which began with only 10
songs; I added 10 more to bring in styles the original set was missing.

**Genres represented** include pop, lofi, rock, ambient, jazz, synthwave, indie
pop, hip hop, edm, classical, country, metal, rnb, reggae, folk, funk, and
k-pop. **Moods represented** include happy, chill, intense, relaxed, focused,
moody, confident, energetic, melancholic, nostalgic, aggressive, romantic,
groovy, and upbeat.

Each song also carries five numeric features:

- **energy** — how intense or calm the song feels
- **tempo** (tempo_bpm) — how fast the song is, in beats per minute
- **valence** — how positive or happy the song sounds
- **danceability** — how easy the song is to dance to
- **acousticness** — how acoustic (versus electronic) the song sounds

**Limitations of the data.** The catalog is very small, and some genres (like
metal) appear only once, so there is not much to choose from. It is also not
representative of all music: many real genres, languages, and cultures are
missing, and the numbers were assigned by hand rather than measured, so they are
rough approximations of how a song actually sounds.

---

## 5. Strengths  

VibeFinder works best when a user's preferences agree with each other. For the
**High-Energy Pop**, **Chill Lofi**, and **Deep Intense Rock** profiles — where
the favorite genre, mood, and energy all point at the same kind of song — the
top recommendation was a clear, sensible match that lined up with my intuition
(an upbeat pop track, a calm acoustic study track, and a loud intense rock
track, respectively).

The scoring also captures a couple of patterns well. Because it rewards energy
*closeness* rather than raw loudness, a calm listener is never handed the
loudest song just because its number is bigger. And because every recommendation
comes with its point breakdown, the system is fully transparent — you can always
see exactly why a song was chosen, which makes it a strong teaching tool.

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

Here are a few ideas for making VibeFinder better next time:

1. **Use a larger, more realistic dataset.** With far more songs across many
   genres, the recommender would have real choices instead of resurfacing the
   same handful of versatile tracks.
2. **Add smarter similarity between genres and moods.** Instead of an exact
   match, the system could understand that "rock" and "metal," or "sad" and
   "melancholic," are close, so a near-match would still earn partial points.
3. **Learn the user's preferences automatically.** Rather than asking the user
   to type in a genre and mood, the system could watch which songs they like or
   skip and adjust over time — closer to how real apps learn from feedback.
4. **Diversify the top results.** The list could be nudged to avoid five
   near-identical songs and instead offer some variety while still respecting
   the user's taste.
5. **Try a real machine-learning approach.** A learned model could pick up
   patterns in listening behavior that a fixed, hand-tuned scoring rule cannot.

---

## 9. Personal Reflection  

My biggest learning moment in this project was realizing that a recommendation
system does not need machine learning to produce believable results. I went in
assuming that anything that "recommends" music must be powered by some complex
trained model, but VibeFinder is just addition and sorting — a few points for a
genre match, a few for mood, a bit for energy and acoustics — and yet the songs
it suggests genuinely feel right for each profile. Seeing simple arithmetic
behave like real intuition changed how I think about the apps I use every day.

AI tools helped me a lot along the way. I used Claude Code to help generate and
organize the code, explain Python techniques like reading a CSV and using
`sorted()`, and generally speed up development so I could focus on the ideas
instead of getting stuck on syntax. At the same time, I did not blindly accept
what it suggested — I ran the program myself, tested all four user profiles,
and checked that the recommendations actually matched what I expected before
trusting them.

What surprised me most was how sensitive the rankings were: changing only a
couple of scoring weights noticeably reshuffled the results, and in one case it
even pushed a song out of the top five entirely. It made the idea of "tuning" a
system feel very real.

If I kept working on this, I would build a larger dataset, add smarter genre and
mood similarity so related styles count for something, let the system learn from
user feedback, and make the recommendations feel more personalized over time.