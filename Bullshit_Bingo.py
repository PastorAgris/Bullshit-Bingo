""" Forsthaus Bullshit Bingo App """

#from narwhals import col
import streamlit as st
import json
import base64
import uuid
from datetime import datetime
from pathlib import Path
from html import escape


st.title("🏡 Forsthaus Bullshit Bingo 💩🎱")

st.markdown(
    """
    Liebe Trash-Kugeln,
    willkommen zum **Forsthaus Bullshit Bingo!**

    Kannst du das nächste absurde Ereignis im Forsthaus vorhersagen?
    Teste dein Gespür!

    Fülle die **9 Felder unten** mit lustigen, skurrilen oder völlig
    vorhersehbaren Szenarien aus, die du im Forsthaus erwarten würdest.

    Wenn du bereit bist, klicke auf **Bingo-Karte erstellen**, um deine ganz
    persönliche Bingo-Karte zu generieren.

    GewinnerIn ist die Person, die als Erste eine Reihe, Spalte oder Diagonale auf ihrer Bingo-Karte vervollständigt. 
    Viel Spaß beim Spielen und möge der beste Trash-Connoisseur gewinnen!

    **Lasst den Chaos beginnen! 🍻**
    """,
    text_alignment="justify"
)

st.text_input(
    "Your Name",
    key="user_name",
    label_visibility="collapsed",
    placeholder="Dein Name..."
)

cols = st.columns(3, gap="small")



def set_background(image_path):
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
        </style>
        """,
        unsafe_allow_html=True
    )

set_background("background.jpg")

for i in range(3):
    with cols[i]:
        for j in range(3):
            scenario = i  + j* 3 + 1

            with st.container(border=True):
                st.markdown(f"**Szenario {scenario}**")
                st.text_area(
                    f"Szenario {scenario}",
                    key=f"scenario_{j+1}{i+1}",
                    label_visibility="collapsed",
                    height=140,
                    placeholder="Szenario-Details eingeben..."
                )

JSON_FILE = Path("bingo_cards.json")


def load_cards():
    if JSON_FILE.exists():
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_card(name, scenarios):
    cards = load_cards()

    card = {
        "name": name,
        "id": str(uuid.uuid4()),
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "scenarios": scenarios
    }

    cards.append(card)

    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(cards, f, indent=4, ensure_ascii=False)

    return card



if st.button("🎲 Bingo-Karte erstellen", type="primary"):

    scenarios = [
        st.session_state[f"scenario_{j+1}{i+1}"]
        for i in range(3)
        for j in range(3)
    ]

    if all(s.strip() for s in scenarios):
        save_card(st.session_state.get("user_name", "Anonymous"), scenarios)
        st.success("Deine Bingo-Karte wurde gespeichert!")
    else:
        st.warning("Bitte fülle alle 9 Felder aus!")


st.divider()
st.header("🍻 Alle Bingo-Karten")

cards = load_cards()

if not cards:
    st.info("Noch keine Bingo-Karten vorhanden.")

for card in reversed(cards):

    with st.expander(
        f"🎯 Bingo-Karte von {card['name']} | {card['created_at']}"
    ):
        cols = st.columns(3, gap="small")

        for i, scenario in enumerate(card["scenarios"]):
            with cols[i % 3]:
                with st.container(border=True, height=120):
                    st.markdown(
                        f"""
                        <div style="
                            height: 90px;
                            display: flex;
                            align-items: center;
                            justify-content: center;
                            text-align: center;
                            overflow-wrap: anywhere;
                        ">
                            {escape(scenario)}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )