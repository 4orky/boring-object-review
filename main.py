# One-line review of the dullest thing in the house.
# The brief asks for a single funny, honest line about a genuinely
# boring everyday object, no longer than two hundred characters.
# I drafted a shortlist by hand, scored each draft on five craft
# points, and let the program pick the winner deterministically:
# the highest craft total wins, and when two drafts tie the
# shorter one wins, so the same input always yields the same line.
# The five craft points are: the object really is dull and ordinary;
# the joke grows out of something the object actually does; the
# observation is true to life; every word earns its place; and the
# turn lands early with the last words doing the sharpening.
# Note on the runner-up dustpan draft: its first wording credited
# the pan with sweeping, which is the brush's work, not the pan's.
# The winning wording fixes that job description to catching, keeps
# the grey-line image, and tightens the middle with paired dashes.
from hashlib import sha256
from os import makedirs
from sys import exit as leave, stderr

OUT_FILE = "/output/entry.txt"
LOWER_LIMIT = 1
UPPER_LIMIT = 200
FORBIDDEN = ("as an ai", "i am an ai", "five stars", "would recommend", "game changer", "literally the best")
ENTRIES = [
    {"text": "The dustpan has one job — catch the dust — and it still leaves a thin grey line behind every single time, like a signature.", "marks": 47},
    {"text": "The dustpan's one job is sweeping up dust, and it still leaves a thin grey line behind every single time, like a signature.", "marks": 44},
    {"text": "The doorstop does nothing all day except lie on the floor getting kicked, and it is the only thing in this house doing its job perfectly.", "marks": 44},
    {"text": "This spare button has lived in a tiny bag for six years, waiting for a shirt I threw away in 2019.", "marks": 43},
    {"text": "The coaster's only skill is sticking to the bottom of the glass and riding it all the way to your mouth.", "marks": 43},
    {"text": "This rubber band spent three years in a drawer, and the one time I finally needed it, it snapped instantly, as if it had been waiting to retire.", "marks": 41},
    {"text": "The tea towel has been damp since Tuesday, smells faintly of onions, and still expects to be the thing that dries the dishes.", "marks": 41},
    {"text": "The paperclip held two pages together for a year, then bent itself out of shape the moment I tried to use it again.", "marks": 41},
    {"text": "Half the cubes stay stuck in the tray, half crack in half, and the one that comes out whole melts before it reaches the glass.", "marks": 41},
    {"text": "The eraser removes the pencil mark and replaces it with a pink smear and a small pile of crumbs, which is technically progress.", "marks": 41},
    {"text": "I keep a bag full of plastic bags in case I ever need a bag, and I have never once taken a bag out of the bag of bags.", "marks": 40},
    {"text": "The wire hangers in my wardrobe have fused into a single tangled organism, and I now own one hanger that holds no clothes.", "marks": 40},
    {"text": "The sponge smells like last Tuesday's dinner, falls apart if you look at it, and is somehow still the only one we own.", "marks": 40},
    ]

def choose_best(pool):
    ranked = None
    for entry in pool:
        wording = entry["text"]
        assert LOWER_LIMIT <= len(wording) <= UPPER_LIMIT, "draft breaks the 1-200 character gate"
        assert wording.strip(), "draft is empty"
        lowered = wording.lower()
        assert not any(phrase in lowered for phrase in FORBIDDEN), "draft leans on a worn-out joke"
        ordering = (entry["marks"], -len(wording))
        if ranked is None or ordering > ranked[0]:
            ranked = (ordering, wording)
    return ranked[1]

def emit_entry():
    chosen = choose_best(ENTRIES)
    makedirs("/output", exist_ok=True)
    with open(OUT_FILE, "w", encoding="utf-8") as handle:
        handle.write(chosen)
    with open(OUT_FILE, "rb") as handle:
        payload = handle.read()
    if payload.decode("utf-8") != chosen:
        print("mismatch: entry file differs from the chosen line", file=stderr)
        leave(1)
    if sha256(chosen.encode("utf-8")).hexdigest() != sha256(payload).hexdigest():
        print("mismatch: SHA-256 of the entry file differs from the chosen line", file=stderr)
        leave(1)
    if not (LOWER_LIMIT <= len(chosen) <= UPPER_LIMIT) or "\n" in chosen or not chosen.strip():
        print("mismatch: chosen line breaks the one-line 1-200 character gate", file=stderr)
        leave(1)
    print(chosen)

if __name__ == "__main__": emit_entry()
