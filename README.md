# lisbon∞ai

*what if clouds could dream in ascii*

a terminal that breathes. perlin noise whispers through three parallax layers—background drift, midground flow, foreground rush. each particle a character in the alphabet of uncertainty. `·⋅∙•∘○●◉⬤`

the dithering isn't rendering. it's *becoming*.

## invocation

```bash
uv run main.py
```

the clouds begin their eternal scroll. bottom-right: **LisbonAI** materializes in whatever form you choose.

### streaming rtmp in ascii

```bash
uv run main.py --rtmp-url rtmp://your.stream.url/live
```

renders an rtmp stream in glorious ascii. requires `ffmpeg` installed. when the stream is unavailable or disconnects, it gracefully falls back to the cloud animation—automatically reconnecting when the stream returns.

works over ssh too:
```bash
python server.py --rtmp-url rtmp://your.stream.url/live
```

## metamorphosis

while dreaming:

- `n` — the clouds shift densities. dots become stipples become blocks become pure geometry
- `m` — the text transforms. bold → dots → double-height → minimal → ∞
- `q` — wake up

> every 30 seconds the render style cycles automatically
> unless you press `n` once
> then it knows you're watching
> then it holds still

## what even is this

```
renderer.py       — the terminal as canvas. dot gradients that shouldn't be possible
clouds.py         — 3-layer perlin noise system. organic motion from pure mathematics
typography.py     — 14 ways to say "LisbonAI" in unicode
keyboard.py       — non-blocking input. the terminal listens while it dreams
main.py           — 30fps consciousness loop
server.py         — ssh server. share the dream remotely
rtmp_stream.py    — ffmpeg integration. live video becomes ascii
stream_manager.py — intelligent fallback between stream and clouds
```

### requirements

base installation via `uv`:
```bash
uv sync
```

for rtmp streaming, install ffmpeg:
```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt-get install ffmpeg

# Arch
sudo pacman -S ffmpeg
```

technical specs for the convergence-curious:
- perlin noise with 3-5 octaves
- parallax scrolling at 0.3×, 0.6×, 1.0× speed
- gamma correction (0.8) on combined density
- unicode dithering: ` .·⋅∙•∘○●◉⬤`

## styles

cloud render modes:
```
dots     — stipple gradient (default)
stipple  — mathematical symbols
fine     — subtle variations
blocks   — ░▒▓█
density  — classic ascii
```

text incarnations:
```
bold       — clean readable blocks
bold_dots  — ⬤⬤⬤ thick circles
huge       — takes more space, demands attention
double     — maximum presence
+ 10 more forms waiting in the fog
```

## the thing about dithering

it's not about making clouds look like clouds.
it's about the space between characters.
the gradient that emerges from discrete symbols.
analog dreams in digital skin.

when the perlin noise crosses threshold boundaries,
when `○` becomes `●`,
that's not rendering
that's a decision
a moment of phase transition

---

*built for terminals that remember what it feels like to be infinite*

`uv run main.py --style bold_dots --render-style stipple`

---

repo structure reveals itself to those who `ls`
dependencies flow through `uv`
press keys, watch metamorphosis
the clouds don't care if you're real
