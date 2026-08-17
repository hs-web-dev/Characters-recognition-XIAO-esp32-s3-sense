# Characters-recognition-XIAO-esp32-s3-sense

### English Version

**ESP32-S3 Real-Time Air Writing & Character Recognition**

An advanced, lightweight, and fully offline computer vision system designed to capture, analyze, and recognize handwritten characters or shapes in real-time using an **ESP32-S3** camera stream and **Python (OpenCV)**.

Unlike heavy machine learning pipelines, this project relies on a deterministic geometric approach and a structured text-based configuration system.

**Key Features & Capabilities:**

* **Live Video Streaming Integration:** Connects seamlessly to an ESP32-S3 camera module (`/stream`) to process live handwriting frames.
* **Dense Point Extraction & Skeletonization:** Automatically detects the starting point (lowest point on the frame) and extracts a dense, high-resolution web of points covering the entire stroke path.
* **20x20 Binary Grid Mapping:** Divises the Region of Interest (ROI) into a fine binary matrix (20x20 cells) where active touch zones are marked as green cubes and empty zones as red cubes.
* **Geometric Feature Analysis:** Computes precise angles in degrees and detects curve counts to assist in shape evaluation.
* **Config-File-Driven Recognition:** Performs pattern matching entirely against a structured local text file (`characters_config.txt`), eliminating complex model training dependencies.
* **Auto-Organized Dataset Storage:** Automatically sorts and groups new variations by character (e.g., grouping all versions of '1' or 'A' together) whenever a user validates or corrects a trace.
* **Serial UART Communication:** Instantly transmits recognized or validated characters over a serial port to connected microcontrollers or hardware.

---

### French Version

**Système de Reconnaissance d'Écriture et de Caractères en Temps Réel avec ESP32-S3**

Un système de vision par ordinateur léger, performant et entièrement autonome (hors ligne), conçu pour capturer, analyser et reconnaître des caractères ou tracés manuscrits en temps réel via un flux vidéo **ESP32-S3** et **Python (OpenCV)**.

Contrairement aux pipelines de Machine Learning lourds, ce projet repose sur une approche géométrique précise et un système de configuration textuel structuré.

**Fonctionnalités et Capacités Principales :**

* **Flux vidéo en direct :** Connexion transparente au module caméra de l'ESP32-S3 (`/stream`) pour traiter l'écriture en direct.
* **Extraction de points denses :** Détection automatique du point de départ (le point le plus bas du tracé) et maillage dense recouvrant l'intégralité du dessin.
* **Grille binaire 20x20 :** Découpage de la zone d'intérêt en une matrice fine (20x20) où les zones de contact apparaissent en carrés verts et les zones vides en carrés rouges.
* **Analyse géométrique :** Calcul des angles précis en degrés et détection du nombre de courbes pour affiner l'évaluation de la forme.
* **Reconnaissance par fichier de configuration :** Comparaison des tracés effectuée entièrement à partir d'un fichier texte local structuré (`characters_config.txt`), sans dépendance à des bibliothèques de modèles complexes.
* **Organisation automatique des versions :** Classement et regroupement automatique des nouvelles variantes par caractère (ex: toutes les versions du chiffre '1' ou de la lettre 'A' sont regroupées ensemble) lors de la validation ou de la correction par l'utilisateur.
* **Communication Série UART :** Envoi instantané du caractère reconnu ou validé via le port série vers des microcontrôleurs ou du matériel externe.



Voici le guide complet pas à pas, clic par clic, pour créer votre dépôt sur GitHub, y ajouter votre description et publier votre projet. Le guide est proposé en **anglais** (recommandé pour GitHub) et en **français**.

---

### 🇬🇧 English Version (Step-by-Step Click-by-Click Guide)

#### Step 1: Create the Repository on GitHub

1. Open your web browser and go to [github.com](https://github.com/). Log in to your account.
2. In the **top-right corner** of the page, click on the **`+`** (plus) icon button.
3. In the dropdown menu that appears, click on **`New repository`**.

#### Step 2: Configure Your Repository Settings

1. **Repository name:** Type your project name (e.g., `esp32-air-writing-recognition`).
2. **Description (Optional):** Paste a short description (e.g., *Real-time character recognition using ESP32-S3, OpenCV, and a binary grid configuration file.*).
3. Select **`Public`** (so anyone can view and download your files).
4. **Important:** Leave **all boxes unchecked** underneath ("Add a README file", "Add .gitignore", "Choose a license"), because you already created them locally.
5. Scroll down to the bottom of the page and click the green **`Create repository`** button.

#### Step 3: Push Your Files from Your Computer

1. Open your computer's terminal (or command prompt) inside your project folder.
2. Copy and paste the commands provided by GitHub on the screen (they will look like this, adapted to your username):
```bash
git branch -M main
git remote add origin https://github.com/your-username/your-repository-name.git
git push -u origin main

```


3. Press **Enter** and wait for the upload to complete. Refresh your GitHub page: your project is now online!

---

### 🇫🇷 French Version (Guide étape par étape, clic par clic)

#### Étape 1 : Créer le dépôt sur GitHub

1. Ouvrez votre navigateur internet et rendez-vous sur [github.com](https://github.com/). Connectez-vous à votre compte.
2. Dans le **coin supérieur droit** de la page, cliquez sur le bouton représentant un **`+`** (plus).
3. Dans le menu déroulant qui s'ouvre, cliquez sur **`New repository`** (Nouveau dépôt).

#### Étape 2 : Configurer les paramètres du dépôt

1. **Repository name (Nom du dépôt) :** Tapez le nom de votre projet (par exemple : `esp32-air-writing-recognition`).
2. **Description (Optionnel) :** Collez une courte description (par ex. : *Reconnaissance de caractères en temps réel avec ESP32-S3, OpenCV et grille binaire.*).
3. Cochez l'option **`Public`** (pour que tout le monde puisse voir et télécharger vos fichiers).
4. **Très important :** Ne cochez **aucune** des cases en dessous ("Add a README file", "Add .gitignore", "Choose a license"), car vous les avez déjà créées sur votre ordinateur.
5. Faites défiler la page tout en bas et cliquez sur le gros bouton vert **`Create repository`** (Créer le dépôt).

#### Étape 3 : Envoyer vos fichiers depuis votre ordinateur

1. Ouvrez le terminal (ou l'invite de commande) de votre ordinateur directement à l'intérieur du dossier de votre projet.
2. Copiez et collez les commandes affichées par GitHub à l'écran (elles ressembleront à ceci, adaptées à votre nom d'utilisateur) :
```bash
git branch -M main
git remote add origin https://github.com/votre-nom-utilisateur/nom-de-votre-depot.git
git push -u origin main

```


3. Appuyez sur **Entrée** et patientez pendant le transfert. Actualisez votre page GitHub : votre projet y est désormais en ligne !
