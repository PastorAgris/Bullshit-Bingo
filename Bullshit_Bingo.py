
"""Forsthaus Bullshit Bingo App"""

import streamlit as st
import json
import base64
import uuid

from datetime import datetime
from pathlib import Path
from html import escape


# --------------------------------------------------
# Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Forsthaus Bullshit Bingo",
    page_icon="🏡",
    layout="wide"
)

JSON_FILE = Path("bingo_cards.json")
BACKGROUND_FILE = Path("background.jpg")


# --------------------------------------------------
# Background
# --------------------------------------------------

def set_background(image_path):
    if not image_path.exists():
        return

    with open(image_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image:
                linear-gradient(
                    rgba(0, 0, 0, 0.8),
                    rgba(0, 0, 0, 0.8)
                ),
                url("data:image/jpeg;base64,{encoded}");

            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            background-repeat: no-repeat;
        }}

        @media (max-width: 768px) {{
            .block-container {{
                padding-left: 0.7rem;
                padding-right: 0.7rem;
            }}
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


set_background(BACKGROUND_FILE)


# --------------------------------------------------
# JSON Storage
# --------------------------------------------------

def load_cards():
    if JSON_FILE.exists():
        try:
            with open(JSON_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            st.error("Die Bingo-Karten konnten nicht geladen werden.")

    return []


def save_card(name, scenarios):
    cards = load_cards()

    card = {
        "name": name,
        "id": str(uuid.uuid4()),
        "created_at": datetime.now().isoformat(
            timespec="seconds"
        ),
        "scenarios": scenarios
    }

    cards.append(card)

    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(
            cards,
            f,
            indent=4,
            ensure_ascii=False
        )

    return card


# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("🏡 Forsthaus Bullshit Bingo 💩🎱")

st.markdown(
    """
    Liebe Trash-Kugeln, willkommen zum
    **Forsthaus Bullshit Bingo!**

    Kannst du das nächste absurde Ereignis im Forsthaus
    vorhersagen? Teste dein Gespür!

    Fülle die **9 Felder unten** mit lustigen, skurrilen
    oder völlig vorhersehbaren Szenarien aus, die du
    im Forsthaus erwarten würdest.

    Wenn du bereit bist, klicke auf
    **Bingo-Karte erstellen**, um deine ganz persönliche
    Bingo-Karte zu generieren.

    GewinnerIn ist die Person, die als Erste eine
    Reihe, Spalte oder Diagonale auf ihrer Bingo-Karte
    vervollständigt.

    Viel Spaß beim Spielen und möge der beste
    Trash-Connoisseur gewinnen!

    **Lasst das Chaos beginnen! 🍻**
    """,
    text_alignment="justify"
)


# --------------------------------------------------
# User Input
# --------------------------------------------------

st.text_input(
    "Dein Name",
    key="user_name",
    placeholder="Dein Name..."
)

st.subheader("🎯 Deine Bingo-Szenarien")

cols = st.columns(
    3,
    gap="small",
    stack_on_mobile=False
)

for i in range(3):
    with cols[i]:
        for j in range(3):

            scenario = i + j * 3 + 1

            with st.container(border=True):
                st.markdown(f"**Szenario {scenario}**")

                st.text_area(
                    f"Szenario {scenario}",
                    key=f"scenario_{j+1}{i+1}",
                    label_visibility="collapsed",
                    height=120,
                    placeholder="Szenario eingeben..."
                )


# --------------------------------------------------
# Generate Bingo Card
# --------------------------------------------------

if st.button(
    "🎲 Bingo-Karte erstellen",
    type="primary",
    use_container_width=True
):

    name = st.session_state.get(
        "user_name", ""
    ).strip()

    scenarios = [
        st.session_state[f"scenario_{j+1}{i+1}"].strip()
        for j in range(3)
        for i in range(3)
    ]

    if not name:
        st.warning("Bitte gib deinen Namen ein.")

    elif not all(scenarios):
        st.warning("Bitte fülle alle 9 Felder aus!")

    else:
        save_card(name, scenarios)
        st.success("Deine Bingo-Karte wurde gespeichert!")
        st.balloons()


# --------------------------------------------------
# Display Saved Cards
# --------------------------------------------------

st.divider()
st.header("🍻 Alle Bingo-Karten")

cards = load_cards()

if not cards:
    st.info("Noch keine Bingo-Karten vorhanden.")


for card in reversed(cards):

    with st.expander(
        f"🎯 Bingo-Karte von "
        f"{card['name']} | {card['created_at']}"
    ):

        cols = st.columns(
            3,
            gap="small",
            stack_on_mobile=False
        )

        for i, scenario in enumerate(card["scenarios"]):

            with cols[i % 3]:

                with st.container(
                    border=True,
                    height=120
                ):

                    st.markdown(
                        f"""
                        <div style="
                            height: 90px;
                            display: flex;
                            align-items: center;
                            justify-content: center;
                            text-align: center;
                            font-size: clamp(10px, 2.5vw, 16px);
                            line-height: 1.2;
                            overflow-wrap: anywhere;
                        ">
                            {escape(scenario)}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
