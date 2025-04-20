import streamlit as st
from team_logic import (
    load_players, add_or_update_player, remove_player, generate_multiple_distributions
)

st.set_page_config(page_title="Aloha Team Generator ⚽", layout="centered")

st.title("⚽ Faire Fußball-Team-Aufteilung")
st.markdown("Wähle Spieler aus, generiere faire Teams und verwalte die Spielerliste.")

# === 🧠 Daten laden ===
player_points = load_players()
all_players = sorted(player_points.keys())

# === 🧍 Spieler auswählen ===
with st.form("team_form"):
    selected_players = st.multiselect("Wähle die heutigen Spieler aus:", all_players)
    num_teams = st.slider("Wie viele Teams?", min_value=2, max_value=4, value=3)
    team_size = st.slider("Spieler pro Team", min_value=3, max_value=7, value=5)
    submitted = st.form_submit_button("🎯 Teams generieren")

    if submitted:
        if len(selected_players) != num_teams * team_size:
            st.error(f"Du brauchst genau {num_teams * team_size} Spieler. Aktuell hast du {len(selected_players)} gewählt.")
        else:
            results = generate_multiple_distributions(
                selected_players, num_teams, team_size=team_size, trials=300, top_n=3
            )

            st.success(f"{len(results)} faire Vorschläge gefunden! 👇")

            for i, (varianz, teams) in enumerate(results, 1):
                st.markdown(f"### 🔹 Vorschlag {i} (Varianz: `{varianz}` Punkte)")
                for j, team in enumerate(teams, 1):
                    punkte = sum(player_points[p] for p in team)
                    st.markdown(f"- **Team {j}** ({punkte} Punkte): {', '.join(team)}")
                st.divider()

# === 🛠️ Spieler verwalten ===
st.markdown("---")
st.header("🔧 Spieler hinzufügen oder bearbeiten")

with st.form("edit_form"):
    new_name = st.text_input("Spielername")
    new_value = st.slider("Skill-Level (1 = schwach, 8 = GOAT)", 1, 8, value=4)
    add_btn = st.form_submit_button("💾 Hinzufügen / Aktualisieren")

    if add_btn:
        if new_name.strip() == "":
            st.error("Name darf nicht leer sein.")
        else:
            add_or_update_player(new_name.strip(), new_value)
            st.success(f"{new_name.strip()} wurde gespeichert!")

# === ❌ Spieler löschen ===
st.markdown("---")
st.header("🗑️ Spieler löschen")

with st.form("delete_form"):
    to_delete = st.selectbox("Wähle Spieler zum Löschen", all_players)
    delete_btn = st.form_submit_button("❌ Löschen")

    if delete_btn:
        remove_player(to_delete)
        st.success(f"{to_delete} wurde gelöscht!")
