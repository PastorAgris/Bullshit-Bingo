
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

    st.html(
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
        </style>
        """
    )


set_background(BACKGROUND_FILE)


# --------------------------------------------------
# CSS
# --------------------------------------------------

st.html("""
<style>

/* Page spacing */
@media (max-width: 768px) {
    .block-container {
        padding-left: 0.5rem;
        padding-right: 0.5rem;
    }

    /* Keep input columns horizontal */
    div[data-testid="stHorizontalBlock"] {
        flex-wrap: nowrap !important;
        gap: 5px !important;
    }

    div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] {
        flex: 1 1 0% !important;
        width: 0 !important;
        min-width: 0 !important;
    }

    div[data-testid="stTextArea"] textarea {
        font-size: 11px !important;
        padding: 5px !important;
    }
}

/* Saved bingo cards */
.bingo-grid {
    display: grid !important;
    grid-template-columns: repeat(3, minmax(0, 1fr)) !important;
    gap: 8px;
    width: 100%;
}

.bingo-cell {
    box-sizing: border-box;
    min-width: 0;
    height: 120px;
    padding: 8px;

    display: flex;
    align-items: center;
    justify-content: center;

    text-align: center;
    overflow-wrap: anywhere;
    overflow-y: auto;

    background: rgba(30, 30, 30, 0.75);
    border: 1px solid rgba(255, 255, 255, 0.3);
    border-radius: 10px;

    color: white;
    font-size: 15px;
    line-height: 1.3;
}

@media (max-width: 600px) {
    .bingo-grid {
        gap: 5px;
    }

    .bingo-cell {
        height: 100px;
        padding: 5px;
        font-size: 11px;
    }
}

</style>
""")


# --------------------------------------------------
# JSON Storage
# --------------------------------------------------

def load_cards():
    if JSON_FILE.exists():
        try:
            with open(JSON_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data if isinstance(data, list) else []

        except (json.JSONDecodeError, OSError):
            st.error(
                "Die Bingo-Karten konnten nicht geladen werden."
            )

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

cols = st.columns(3, gap="small")

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
        st.session_state[f"scenario_{i+1}{j+1}"].strip()
        for i in range(3)
        for j in range(3)
    ]

    if not name:
        st.warning("Bitte gib deinen Namen ein.")

    elif not all(scenarios):
        st.warning("Bitte fülle alle 9 Felder aus!")

    else:
        try:
            save_card(name, scenarios)
            st.success(
                "Deine Bingo-Karte wurde gespeichert!"
            )
            st.balloons()

        except OSError:
            st.error(
                "Die Bingo-Karte konnte nicht gespeichert werden."
            )


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

        cells = "".join(
            f'<div class="bingo-cell">{escape(str(scenario))}</div>'
            for scenario in card["scenarios"]
        )

        st.html(
            f'<div class="bingo-grid">{cells}</div>'
        )


if cards:
    st.download_button(
        label="📥 Alle Bingo-Karten herunterladen",
        data=json.dumps(
            cards,
            indent=4,
            ensure_ascii=False
        ),
        file_name="bingo_cards.json",
        mime="application/json"
    )