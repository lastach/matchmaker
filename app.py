import streamlit as st
import os
import json
import csv
from uuid import uuid4

# -------------------------
# Basic config
# -------------------------
st.set_page_config(page_title="AI Matchmaker Prototype", layout="centered")

PHOTO_DB_PATH = "photo_db.json"    # for generic swipe photos (not the profile pics)
PHOTO_DIR = "photos"
RATINGS_PATH = "photo_ratings.csv"

os.makedirs(PHOTO_DIR, exist_ok=True)

STYLE_OPTIONS = [
    "Outdoorsy / athletic",
    "Polished / professional",
    "Alternative / tattoos / edgy",
    "Soft / cozy / nurturing",
    "Minimalist / creative",
]


# -------------------------
# Helper functions for swipe photos
# -------------------------
def load_photos():
    if not os.path.exists(PHOTO_DB_PATH):
        return []
    with open(PHOTO_DB_PATH, "r") as f:
        return json.load(f)


def save_photos(photos):
    with open(PHOTO_DB_PATH, "w") as f:
        json.dump(photos, f, indent=2)


def log_photo_rating(session_id, photo_id, rating):
    file_exists = os.path.exists(RATINGS_PATH)
    with open(RATINGS_PATH, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["session_id", "photo_id", "rating"])
        writer.writerow([session_id, photo_id, rating])


# -------------------------
# Fictional profiles + photos
#   Update `photo_path` to match your actual filenames.
# -------------------------
PROFILES = [
    {
        "name": "Chris",
        "age": 41,
        "gender": "Man",
        "location": "Travels often",
        "wants_kids": "Maybe / unsure",
        "timeline_kids": "Open-ended",
        "relationship_goal": "Long-term but very independent",
        "adventure_level": 5,
        "stability_level": 2,
        "ambition_level": 5,
        "emotional_availability": 2,
        "communication_style": "Analytical, not very emotive",
        "conflict_style": "Withdraws, then reappears",
        "attachment_style": "Fearful-avoidant",
        "schedule_flexibility": 4,
        "social_energy": 4,
        "style_tags": ["Outdoorsy / athletic", "Minimalist / creative"],
        "photo_path": "profile_photos/Chris.jpg",
        "description": (
            "Entrepreneur constantly on the move. Loves big ideas, risk, and novelty; "
            "struggles with emotional consistency and long-term planning."
        ),
    },
    {
        "name": "Taylor",
        "age": 45,
        "gender": "Woman",
        "location": "Arlington, MA",
        "wants_kids": "Yes",
        "timeline_kids": "ASAP (0-2 years)",
        "relationship_goal": "Marriage & family",
        "adventure_level": 2,
        "stability_level": 5,
        "ambition_level": 3,
        "emotional_availability": 5,
        "communication_style": "Supportive & patient",
        "conflict_style": "Avoids conflict, then gets overwhelmed",
        "attachment_style": "Anxious-preoccupied",
        "schedule_flexibility": 2,
        "social_energy": 2,
        "style_tags": ["Soft / cozy / nurturing"],
        "photo_path": "profile_photos/Taylor.jpg",
        "description": (
            "Teacher who craves security and a warm home life. Loves routine, "
            "friends, and family dinners. Big heart, lower appetite for risk."
        ),
    },
    {
        "name": "Riley",
        "age": 36,
        "gender": "Non-binary",
        "location": "Somerville, MA",
        "wants_kids": "Yes",
        "timeline_kids": "Someday (3-7 years)",
        "relationship_goal": "Primary partnership, open to non-traditional structure",
        "adventure_level": 5,
        "stability_level": 3,
        "ambition_level": 4,
        "emotional_availability": 4,
        "communication_style": "Playful & emotionally aware",
        "conflict_style": "Collaborative and curious",
        "attachment_style": "Secure with slight anxious tendencies",
        "schedule_flexibility": 3,
        "social_energy": 5,
        "style_tags": ["Alternative / tattoos / edgy", "Minimalist / creative"],
        "photo_path": "profile_photos/Riley.jpg",
        "description": (
            "Product manager at a climate tech startup. Loves festivals, dance, "
            "outdoors, and designing a non-traditional life."
        ),
    },
    {
        "name": "Sam",
        "age": 39,
        "gender": "Man",
        "location": "Providence, RI",
        "wants_kids": "No",
        "timeline_kids": "Not applicable",
        "relationship_goal": "Committed partnership, no marriage needed",
        "adventure_level": 4,
        "stability_level": 4,
        "ambition_level": 3,
        "emotional_availability": 3,
        "communication_style": "Direct but sometimes blunt",
        "conflict_style": "Talks only when pushed",
        "attachment_style": "Dismissive-avoidant",
        "schedule_flexibility": 5,
        "social_energy": 4,
        "style_tags": ["Outdoorsy / athletic"],
        "photo_path": "profile_photos/Sam.jpg",
        "description": (
            "Freelance designer with a flexible lifestyle. Loves road trips, live music, "
            "and trying hobbies, but avoids heavy emotional talks."
        ),
    },
    {
        "name": "Jordan",
        "age": 42,
        "gender": "Woman",
        "location": "Cambridge, MA",
        "wants_kids": "Maybe / unsure",
        "timeline_kids": "Open-ended",
        "relationship_goal": "Long-term, see where it goes",
        "adventure_level": 3,
        "stability_level": 5,
        "ambition_level": 4,
        "emotional_availability": 5,
        "communication_style": "Warm & reflective",
        "conflict_style": "Needs a bit of time, then talks",
        "attachment_style": "Secure",
        "schedule_flexibility": 4,
        "social_energy": 3,
        "style_tags": ["Soft / cozy / nurturing", "Polished / professional"],
        "photo_path": "profile_photos/Jordan.jpg",
        "description": (
            "Consultant turned leadership coach. Loves deep conversation, quiet nights in, "
            "and the occasional big trip. Very emotionally attuned."
        ),
    },
    {
        "name": "Alex",
        "age": 38,
        "gender": "Man",
        "location": "Boston, MA",
        "wants_kids": "Yes",
        "timeline_kids": "Soon (1-3 years)",
        "relationship_goal": "Long-term / marriage",
        "adventure_level": 5,
        "stability_level": 3,
        "ambition_level": 5,
        "emotional_availability": 4,
        "communication_style": "Direct & logical",
        "conflict_style": "Discuss quickly & calmly",
        "attachment_style": "Secure",
        "schedule_flexibility": 3,
        "social_energy": 4,
        "style_tags": ["Outdoorsy / athletic", "Polished / professional"],
        "photo_path": "profile_photos/Alex.jpg",
        "description": (
            "Startup exec who loves travel, skiing, and trying new restaurants. "
            "Wants a true partner to build a big life with but works a lot."
        ),
    },
    {
        "name": "Morgan",
        "age": 37,
        "gender": "Woman",
        "location": "Boston, MA",
        "wants_kids": "No",
        "timeline_kids": "Not applicable",
        "relationship_goal": "Long-term partnership",
        "adventure_level": 3,
        "stability_level": 4,
        "ambition_level": 4,
        "emotional_availability": 4,
        "communication_style": "Direct & kind",
        "conflict_style": "Addresses issues early",
        "attachment_style": "Secure",
        "schedule_flexibility": 3,
        "social_energy": 3,
        "style_tags": ["Polished / professional", "Minimalist / creative"],
        "photo_path": "profile_photos/Morgan.jpg",
        "description": (
            "In-house counsel who loves travel, fitness, and thoughtful conversation. "
            "Values fairness, reliability, and mutual respect."
        ),
    },
    {
        "name": "Jamie",
        "age": 40,
        "gender": "Man",
        "location": "Brookline, MA",
        "wants_kids": "Yes",
        "timeline_kids": "Soon (1-3 years)",
        "relationship_goal": "Marriage & family",
        "adventure_level": 3,
        "stability_level": 4,
        "ambition_level": 4,
        "emotional_availability": 4,
        "communication_style": "Balanced logical/emotional",
        "conflict_style": "Listens first, then responds",
        "attachment_style": "Secure",
        "schedule_flexibility": 3,
        "social_energy": 3,
        "style_tags": ["Soft / cozy / nurturing", "Polished / professional"],
        "photo_path": "profile_photos/Jamie.jpg",
        "description": (
            "Healthcare ops leader. Loves weekend trips, cooking at home, and game nights. "
            "Dependable, thoughtful, and future-oriented."
        ),
    },
]

# -------------------------
# Assumed preferences from their (imagined) swipe data
# -------------------------
PROFILE_PREFERENCES = {
    # likes slightly younger women, outdoorsy / polished
    "Chris": {
        "preferred_genders": ["Woman"],
        "preferred_styles": ["Outdoorsy / athletic", "Polished / professional"],
        "min_age": 32,
        "max_age": 45,
    },
    # Taylor likes warm, stable men a bit 40–52
    "Taylor": {
        "preferred_genders": ["Man"],
        "preferred_styles": ["Soft / cozy / nurturing", "Polished / professional"],
        "min_age": 40,
        "max_age": 52,
    },
    # Riley is pretty queer / open
    "Riley": {
        "preferred_genders": ["Woman", "Man", "Non-binary"],
        "preferred_styles": ["Alternative / tattoos / edgy", "Minimalist / creative"],
        "min_age": 30,
        "max_age": 45,
    },
    # Sam: straight, outdoorsy, laid-back
    "Sam": {
        "preferred_genders": ["Woman"],
        "preferred_styles": ["Outdoorsy / athletic", "Minimalist / creative"],
        "min_age": 30,
        "max_age": 42,
    },
    # Jordan: emotionally attuned, likes kind, grounded partners
    "Jordan": {
        "preferred_genders": ["Man"],
        "preferred_styles": ["Soft / cozy / nurturing", "Polished / professional"],
        "min_age": 38,
        "max_age": 50,
    },
    # Alex: ambitious, likes similarly driven / polished
    "Alex": {
        "preferred_genders": ["Woman"],
        "preferred_styles": ["Polished / professional", "Minimalist / creative"],
        "min_age": 32,
        "max_age": 42,
    },
    # Morgan: likes balanced, thoughtful men ~mid 30s–mid 40s
    "Morgan": {
        "preferred_genders": ["Man"],
        "preferred_styles": ["Polished / professional", "Soft / cozy / nurturing"],
        "min_age": 35,
        "max_age": 45,
    },
    # Jamie: attracted to warm, grounded partners; fairly flexible
    "Jamie": {
        "preferred_genders": ["Woman"],
        "preferred_styles": ["Soft / cozy / nurturing", "Polished / professional"],
        "min_age": 34,
        "max_age": 45,
    },
}


# -------------------------
# Matching logic
# -------------------------
def passes_dealbreakers(user, profile):
    # geography – simple: city name match unless open to long-distance
    if not user["open_to_long_distance"]:
        user_city = user["city"].split(",")[0].strip().lower()
        profile_city = profile["location"].split(",")[0].strip().lower()
        if user_city != profile_city:
            return False

    # age range
    if not (user["min_age"] <= profile["age"] <= user["max_age"]):
        return False

    # kids strictness
    if user["kids_strict"]:
        if user["wants_kids"] != profile["wants_kids"]:
            return False

    return True


def score_profile(user, profile):
    """Compatibility (values/goals/lifestyle) – 0–100."""
    weights = {
        "kids": 0.25,
        "timeline": 0.15,
        "goal": 0.20,
        "adventure": 0.10,
        "stability": 0.05,
        "ambition": 0.10,
        "emotional": 0.10,
        "communication": 0.05,
    }

    if user["wants_kids"] == profile["wants_kids"]:
        kids_score = 1.0
    elif "Maybe" in (user["wants_kids"], profile["wants_kids"]):
        kids_score = 0.6
    else:
        kids_score = 0.1

    timeline_score = 0.6 if user["timeline_kids"] == profile["timeline_kids"] else 0.3
    if (
        user["wants_kids"] == "No"
        or profile["wants_kids"] == "No"
        or "Not applicable" in (user["timeline_kids"], profile["timeline_kids"])
    ):
        timeline_score = 0.4

    goal_score = 0.6 if user["relationship_goal"] == profile["relationship_goal"] else 0.3

    def trait_score(trait, scale=5):
        u = user[trait]
        p = profile[trait]
        diff = abs(u - p)
        return 1.0 - (diff / (scale - 1))

    adventure_score = trait_score("adventure_level")
    stability_score = trait_score("stability_level")
    ambition_score = trait_score("ambition_level")
    emotional_score = trait_score("emotional_availability")

    comm_score = 0.6 if user["communication_style"] == profile["communication_style"] else 0.4

    breakdown = {
        "kids": kids_score,
        "timeline": timeline_score,
        "goal": goal_score,
        "adventure": adventure_score,
        "stability": stability_score,
        "ambition": ambition_score,
        "emotional": emotional_score,
        "communication": comm_score,
    }

    total = sum(breakdown[k] * weights[k] for k in weights) * 100
    return round(total, 1), breakdown


def user_attraction_to_profile(user, profile):
    """How much you're likely attracted to them, based on style tags."""
    preferred = set(user.get("preferred_styles", []))
    if not preferred:
        return 0.5
    overlap = preferred & set(profile.get("style_tags", []))
    if not overlap:
        return 0.3
    if len(overlap) == 1:
        return 0.7
    return 0.9


def profile_attraction_to_user(profile, user):
    """How much they might be attracted to you, given imagined swipe data."""
    prefs = PROFILE_PREFERENCES.get(profile["name"])
    if not prefs:
        return 0.5  # default neutral

    # gender
    if user["gender"] != "Prefer not to say" and prefs["preferred_genders"]:
        if user["gender"] not in prefs["preferred_genders"]:
            gender_factor = 0.2
        else:
            gender_factor = 1.0
    else:
        gender_factor = 0.6

    # age
    if prefs["min_age"] <= user["age"] <= prefs["max_age"]:
        age_factor = 1.0
    else:
        age_factor = 0.5

    # visual style
    your_style = set(user.get("self_style_tags", []))
    if not your_style:
        style_score = 0.5
    else:
        overlap = your_style & set(prefs["preferred_styles"])
        if not overlap:
            style_score = 0.3
        elif len(overlap) == 1:
            style_score = 0.7
        else:
            style_score = 0.9

    return max(0.0, min(1.0, style_score * 0.6 + age_factor * 0.25 + gender_factor * 0.15))


def coaching_blurb(user, profile, comp_score, breakdown):
    themes = []

    if breakdown["kids"] > 0.8:
        themes.append("You’re well-aligned on wanting kids or not, which removes a huge source of future friction.")
    elif breakdown["kids"] < 0.4:
        themes.append("Your preferences around kids are meaningfully different; this would need very explicit conversation.")

    if breakdown["goal"] > 0.7:
        themes.append("You’re pointed in a similar direction in terms of relationship goals.")
    else:
        themes.append("Your relationship goals aren’t fully aligned, so pacing and expectations would be critical to discuss.")

    if breakdown["adventure"] > 0.7 and breakdown["stability"] > 0.7:
        themes.append("You balance adventure and stability in similar ways, which is promising for lifestyle fit.")
    elif breakdown["adventure"] > 0.7:
        themes.append("You’re both wired for adventure, which can be energizing but may need shared grounding routines.")
    elif breakdown["stability"] > 0.7:
        themes.append("You’re similarly oriented toward stability and predictability, which can support a calm partnership.")

    if breakdown["emotional"] > 0.7:
        themes.append("Your emotional availability levels are similar, which usually makes communication smoother.")
    elif breakdown["emotional"] < 0.4:
        themes.append("There’s a gap in emotional availability that could feel frustrating on one or both sides.")

    if breakdown["communication"] > 0.55:
        themes.append("Your communication styles are reasonably aligned.")
    else:
        themes.append("Your communication styles differ; with intention this can work, but it won’t be on autopilot.")

    if comp_score >= 80:
        headline = "High-potential match with real upside."
    elif comp_score >= 65:
        headline = "Solid match with a few key things to navigate."
    elif comp_score >= 50:
        headline = "Some overlap, but you’d need to be deliberate."
    else:
        headline = "More of a learning connection than a likely long-term fit."

    return headline, themes


# -------------------------
# Admin panel – swipe photos
# -------------------------
def admin_panel():
    st.title("Admin Panel – Swipe Photo Management")
    st.markdown("Upload photos for the attraction 'like / not for me' exercise (not profile pics).")

    photos = load_photos()
    uploaded_files = st.file_uploader(
        "Upload one or more photos", type=["png", "jpg", "jpeg"], accept_multiple_files=True
    )

    if uploaded_files and st.button("Save uploaded photos"):
        for file in uploaded_files:
            filepath = os.path.join(PHOTO_DIR, file.name)
            with open(filepath, "wb") as f:
                f.write(file.getbuffer())
            photos.append(
                {
                    "id": len(photos) + 1,
                    "path": filepath,
                    "filename": file.name,
                }
            )
        save_photos(photos)
        st.success("Photos saved to backend.")

    st.subheader("Existing photos")
    if photos:
        for p in photos:
            st.image(p["path"], width=150, caption=f"ID {p['id']}: {p['filename']}")
    else:
        st.info("No photos uploaded yet.")


# -------------------------
# User app
# -------------------------
def user_app():
    if "session_id" not in st.session_state:
        st.session_state["session_id"] = str(uuid4())
    if "photo_index" not in st.session_state:
        st.session_state["photo_index"] = 0

    st.title("AI Matchmaker & Dating Coach – Prototype")

    st.markdown(
        "This prototype:\n"
        "- Applies **dealbreakers** first (geography, age range, kids).\n"
        "- Scores **compatibility** on relationship goals & lifestyle.\n"
        "- Models **your attraction to them** and **their attraction to you** using simple style + age rules.\n"
        "- Optionally collects extra attraction data via a swipe-style photo exercise."
    )

    st.header("1. Dealbreakers & basics")

    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Your age", min_value=20, max_value=80, value=40)
        city = st.text_input("Your city (e.g., 'Boston, MA')", value="Boston, MA")
        min_age = st.number_input("Minimum age you’d date", min_value=20, max_value=80, value=35)
    with col2:
        gender = st.selectbox("Your gender", ["Woman", "Man", "Non-binary", "Other", "Prefer not to say"])
        open_to_long_distance = st.checkbox("Open to long-distance?", value=False)
        max_age = st.number_input("Maximum age you’d date", min_value=20, max_value=90, value=48)

    st.subheader("Kids & relationship goals")
    wants_kids = st.selectbox("Do you want kids (ever)?", ["Yes", "No", "Maybe / unsure"])
    kids_strict = st.checkbox("Is alignment on wanting kids a hard dealbreaker?", value=True)

    timeline_kids = st.selectbox(
        "If kids are on the table, what timeline feels right?",
        [
            "ASAP (0-2 years)",
            "Soon (1-3 years)",
            "Someday (3-7 years)",
            "Open-ended",
            "Not applicable",
        ],
    )

    relationship_goal = st.selectbox(
        "What best describes your relationship goal?",
        [
            "Marriage & family",
            "Long-term / marriage",
            "Long-term partnership",
            "Long-term, see where it goes",
            "Committed partnership, no marriage needed",
        ],
    )

    st.subheader("Lifestyle & emotional alignment")
    adventure_level = st.slider("How much adventure / novelty do you want in your life?", 1, 5, 4)
    stability_level = st.slider("How much stability / predictability do you want?", 1, 5, 3)
    ambition_level = st.slider("How driven are you about career / projects right now?", 1, 5, 4)
    emotional_availability = st.slider("How emotionally available do you feel right now?", 1, 5, 3)

    communication_style = st.selectbox(
        "Your most natural communication style in relationships",
        [
            "Direct & logical",
            "Balanced logical/emotional",
            "Warm & reflective",
            "Playful & emotionally aware",
        ],
    )

    st.subheader("Physical attraction")
    preferred_styles = st.multiselect(
        "Which of these styles are you **usually** physically drawn to? (Pick a few)",
        STYLE_OPTIONS,
    )

    self_style_tags = st.multiselect(
        "Which of these styles best describe **how you usually look / present**?",
        STYLE_OPTIONS,
    )

    user = {
        "age": age,
        "city": city,
        "gender": gender,
        "min_age": min_age,
        "max_age": max_age,
        "open_to_long_distance": open_to_long_distance,
        "wants_kids": wants_kids,
        "kids_strict": kids_strict,
        "timeline_kids": timeline_kids,
        "relationship_goal": relationship_goal,
        "adventure_level": adventure_level,
        "stability_level": stability_level,
        "ambition_level": ambition_level,
        "emotional_availability": emotional_availability,
        "communication_style": communication_style,
        "preferred_styles": preferred_styles,
        "self_style_tags": self_style_tags,
    }

    if st.button("Find my top matches"):
        viable = [p for p in PROFILES if passes_dealbreakers(user, p)]

        st.header("2. Your matches (fictional)")

        if not viable:
            st.warning("No profiles passed your hard dealbreakers. Try relaxing one or two.")
        else:
            results = []
            for p in viable:
                comp_score, breakdown = score_profile(user, p)
                you_like_them = user_attraction_to_profile(user, p)         # 0–1
                they_like_you = profile_attraction_to_user(p, user)         # 0–1

                # combine: 50% compatibility, 25% your attraction, 25% their attraction
                final_score = (0.5 * (comp_score / 100.0)
                               + 0.25 * you_like_them
                               + 0.25 * they_like_you) * 100.0

                results.append(
                    {
                        "profile": p,
                        "comp_score": comp_score,
                        "you_like_them": you_like_them,
                        "they_like_you": they_like_you,
                        "final_score": round(final_score, 1),
                        "breakdown": breakdown,
                    }
                )

            results.sort(key=lambda x: x["final_score"], reverse=True)

            for i, item in enumerate(results[:3], start=1):
                p = item["profile"]
                comp_score = item["comp_score"]
                you_like = int(item["you_like_them"] * 100)
                they_like = int(item["they_like_you"] * 100)
                final_score = item["final_score"]
                breakdown = item["breakdown"]

                headline, themes = coaching_blurb(user, p, comp_score, breakdown)

                with st.expander(
                    f"#{i}: {p['name']} – {final_score}/100 overall "
                    f"(compat {comp_score}, you→them {you_like}, them→you {they_like})"
                ):
                    if os.path.exists(p["photo_path"]):
                        st.image(p["photo_path"], width=260)
                    st.markdown(f"**{p['name']}**, {p['age']}, {p['gender']} – {p['location']}")
                    st.markdown(p["description"])
                    st.markdown(f"**Relationship goal:** {p['relationship_goal']}")
                    st.markdown(f"**Wants kids:** {p['wants_kids']} ({p['timeline_kids']})")
                    st.markdown(f"**Style vibe:** {', '.join(p['style_tags'])}")

                    st.markdown("---")
                    st.markdown(f"### Coaching view: {headline}")
                    for t in themes:
                        st.markdown(f"- {t}")

        st.header("3. Meta: what this prototype is doing")
        st.markdown(
            "- Hard filters (dealbreakers) first.\n"
            "- Compatibility based on kids, goals, lifestyle, communication.\n"
            "- Your attraction estimated from **your stated tastes vs their style tags**.\n"
            "- Their attraction estimated from **imagined swipe data** (preferences) vs your **self-described style, age, and gender**.\n"
            "- Final score blends all three."
        )

    # -------------------------
    # Optional swipe exercise
    # -------------------------
    st.header("4. Optional: swipe-style photo exercise")

    st.markdown(
        "This collects simple 'Like' / 'Not for me' signals on generic photos to someday "
        "train a more nuanced attraction model. It’s not used directly in the scores above yet."
    )

    photos = load_photos()
    if not photos:
        st.info("No swipe photos available yet. (Admin needs to upload some.)")
        return

    if st.session_state["photo_index"] >= len(photos):
        st.success("You’ve rated all available photos. Thank you!")
        return

    current = photos[st.session_state["photo_index"]]
    st.image(current["path"], caption=f"Photo ID {current['id']}")

    col_like, col_not = st.columns(2)
    if col_like.button("❤️ Like"):
        log_photo_rating(st.session_state["session_id"], current["id"], "like")
        st.session_state["photo_index"] += 1
        st.experimental_rerun()
    if col_not.button("🙅 Not for me"):
        log_photo_rating(st.session_state["session_id"], current["id"], "not_for_me")
        st.session_state["photo_index"] += 1
        st.experimental_rerun()


# -------------------------
# Entry point
# -------------------------
mode = st.sidebar.selectbox("Mode", ["User", "Admin"])

if mode == "Admin":
    admin_panel()
else:
    user_app()

