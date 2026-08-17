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
