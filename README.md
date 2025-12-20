# prediction prix voitures 


---

#  Prédiction des Prix des Voitures

Ce projet implémente un modèle de **machine learning** capable de prédire le prix d’une voiture à partir de ses caractéristiques (marque, modèle, année, kilométrage, etc.). Il inclut analyse exploratoire, ingénierie des caractéristiques, entraînement de modèles, sélection du meilleur modèle, ainsi qu’une API pour faire des prédictions.

---

## 🚀 Fonctionnalités

*  **EDA (Exploratory Data Analysis)** pour comprendre les données et leurs distributions
*  **Feature Engineering** pour préparer les données avant modélisation
*  **Modélisation et sélection de modèles** avec comparaison de performances
*  **Modèle sauvegardé** prêt à être déployé (`best_model.pkl`)
*  **API de prédiction** construite avec Python (`api.py` / `app.py`)
*  Notebooks pour traçabilité complète du développement

---

## 🧠 📈 Comment ça marche ?

1. **Nettoyage des données**

   * Gestion des valeurs manquantes
   * Conversion des variables catégorielles en numériques

2. **Analyse exploratoire**

   * Visualisation des distributions
   * Analyse des corrélations

3. **Feature Engineering**

   * Encodage des variables textuelles
   * Normalisation / mise à l’échelle si nécessaire

4. **Entraînement de modèles**

   * Test de différents algorithmes de régression
   * Comparaison des scores (ex. RMSE, R²)

---

## 🛠️ Installation

1. Clone le dépôt :

   ```bash
   git clone https://github.com/fatixa789/prediction_prix_voiture.git
   cd prediction_prix_voiture
   ```

2. Crée un environnement virtuel (fortement recommandé) :

   ```bash
   python3 -m venv venv
   source venv/bin/activate   # macOS & Linux
   venv\Scripts\activate      # Windows
   ```

3. Installe les dépendances :

   ```bash
   pip install -r requirements.txt
   ```

---

##  Lancer l’API de prédiction

Le projet inclut une API web légère pour faire des prédictions à partir de requêtes HTTP.

```bash
python app.py
```

##  Utilisation dans un Notebook

Tu peux explorer les notebooks inclus pour :

* Visualiser les données
* Explorer différentes techniques de preprocessing
* Essayer différents modèles de régression
* Améliorer l’algorithme

---

##  Résultats attendus

Ce projet vise à construire un modèle qui :

* Comprend les relations entre les caractéristiques et le prix des voitures
* Prédit de manière fiable le prix d’une voiture donnée

---


