import streamlit as st
import requests
import joblib
import pandas as pd

st.set_page_config(
    page_title="Estimation du prix de voiture",
    page_icon="🚗",
    layout="wide"
)

st.markdown("""
<div style="background-color:#d9dbda;padding:15px;border-radius:10px;margin-bottom:20px;">
    <h2 style="color:black;">Bienvenue dans notre application d'estimation de prix de voitures !</h2>
    <p style="font-size:16px;color:black">
        Remplissez les informations sur le véhicule et obtenez une estimation précise
        de sa valeur sur le marché marocain 🚗💰
    </p>
</div>
""", unsafe_allow_html=True)

encoder = joblib.load("encoder.pkl")

MARQUES_CONNUES = [
    'Volkswagen', 'Renault', 'Dacia', 'Peugeot', 'Mercedes-Benz', 'Fiat',
    'Hyundai', 'Ford', 'Citroen', 'Audi', 'BMW', 'Toyota', 'Opel', 'Kia',
    'Land Rover', 'Nissan', 'Skoda', 'Seat', 'Jeep', 'Honda', 'Volvo',
    'Suzuki', 'Alfa Romeo', 'Chevrolet', 'Mitsubishi'
]

ETAT_MAPPING = {"Mauvais": 0, "Moyen": 1, "Très bon": 2, "Neuf": 3}
MAIN_MAPPING = {"Oui": 1, "Non": 0}
BOITE_MAPPING = {"Manuelle": 0, "Automatique": 1}
CARBURANT_MAPPING = {
    "Diesel": 0.799746,
    "Essence": 0.182509,
    "Hybride": 0.014426,
    "Electrique": 0.002885,
    "LPG": 0.000434
}

EQUIPEMENTS_POSSIBLES = [
    "ABS", "Airbags", "CD/MP3/Bluetooth", "Caméra de recul", "Climatisation",
    "ESP", "Jantes aluminium", "Limiteur de vitesse", "Ordinateur de bord",
    "Radar de recul", "Régulateur de vitesse", "Sièges cuir",
    "Système de navigation/GPS", "Toit ouvrant",
    "Verrouillage centralisé à distance", "Vitres électriques"
]

with st.form("formulaire_prix"):
    st.subheader("📋 Informations du Véhicule")

    col1, col2 = st.columns(2)

    with col1:
        marque_input = st.text_input("Marque").strip().title()
        marque = marque_input if marque_input in MARQUES_CONNUES else "Autres"
        annee = st.number_input("Année-Modèle", min_value=1980, max_value=2025, value=2020)
        boite = st.selectbox("Boîte de vitesses", ["Manuelle", "Automatique"])
        carburant = st.selectbox("Type de carburant", ["Diesel", "Essence", "Electrique", "Hybride", "LPG"])
        puissance_fiscale = st.number_input("Puissance fiscale (CV)", min_value=1, value=6)
        origine = st.selectbox(
            "Origine",
            ["WW au Maroc", "Dédouanée", "Inconnue", "Importée neuve", "Pas encore dédouanée"]
        )

    with col2:
        modele_input = st.text_input("Modèle").strip().title()
        modele = modele_input if marque != "Autres" else "Autres"
        kilometrage = st.number_input("Kilométrage (km)", min_value=0, value=50000)
        portes = st.selectbox("Nombre de portes", [3, 5], index=1)
        premiere_main = st.selectbox("Première main", ["Oui", "Non"])
        etat = st.selectbox("État", ["Neuf", "Très bon", "Moyen", "Mauvais"], index=1)

    st.subheader("🛠️ Équipements")
    equipements = st.multiselect("Sélectionnez les équipements", EQUIPEMENTS_POSSIBLES)

    submitted = st.form_submit_button("💰 Estimer le Prix", use_container_width=True)

if submitted:
    etat_encoded = ETAT_MAPPING[etat]
    main_encoded = MAIN_MAPPING[premiere_main]
    boite_encoded = BOITE_MAPPING[boite]
    carburant_encoded = CARBURANT_MAPPING[carburant]

    equip_dict = {f"equip_{e}": int(e in equipements) for e in EQUIPEMENTS_POSSIBLES}
    equip_dict["equip_Aucun"] = int(len(equipements) == 0)

    input_data = {
        "Année-Modèle": annee,
        "Boite de vitesses": boite_encoded,
        "Kilométrage": kilometrage,
        "Puissance fiscale": puissance_fiscale,
        "Nombre de portes": portes,
        "Première main": main_encoded,
        "Carburant_encoded": carburant_encoded,
        "État_encoded": etat_encoded,
        "Marque": marque,
        "Modèle": modele,
        "Origine": origine,
        **equip_dict
    }

    input_df = pd.DataFrame([input_data])

    expected_cols = list(encoder.feature_names_in_)
    for col in expected_cols:
        if col not in input_df.columns:
            input_df[col] = 0
    input_df = input_df[expected_cols]

    input_encoded = encoder.transform(input_df)

    payload = {"features": input_encoded.to_dict(orient="records")[0]}

    response = requests.post("http://127.0.0.1:8000/predict", json=payload, timeout=5)

    if response.status_code == 200:
        prix_estime = response.json()["prix_estime"]
        st.success("✅ Estimation réussie")
        st.markdown(f"""
        <div style="background-color:#29a94f;padding:20px;border-radius:10px;text-align:center;">
            <h2 style="color:white;">💰 Prix estimé</h2>
            <h1 style="color:white;font-size:3rem;">{prix_estime:,.0f} DH</h1>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.error("Erreur lors de la prédiction")

st.markdown("---")
st.markdown("""
<div style="text-align:center;color:#666;padding:20px;">
    <p><strong>Projet de Fin de Module</strong> – Science des Données, Big Data & AI</p>
    <p>ENSIASD</p>
</div>
""", unsafe_allow_html=True)