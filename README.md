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
---










# English Setup Guide

### Step 1: Flash the ESP32-S3 Camera Web Server

1. **Open** the **Arduino IDE** software on your computer.
2. Navigate to `File` > `Examples` > `ESP32` > `Camera` and select `CameraWebServer`.
3. Scroll through the code and **uncomment** the line matching your specific camera board model (e.g., `#define CAMERA_MODEL_XIAO_ESP32S3` or your specific ESP32-S3 module).
4. Enter your local Wi-Fi credentials in the script:
```cpp
const char* ssid = "YOUR_WIFI_NAME";
const char* password = "YOUR_WIFI_PASSWORD";

```


5. Connect your ESP32-S3 to your PC via USB, select your board and the correct **COM Port** in the `Tools` menu, and click `Upload`.
6. Open the `Serial Monitor` (set baud rate to `115200`), press the reset button on your board, and copy the **IP Address** assigned by your router (e.g., `192.168.1.50`).

---

### Step 2: Install Python Dependencies

1. Ensure you have **Python** installed on your computer.
2. Open your terminal (or command prompt) and run the following command to install the required libraries:
```bash
pip install opencv-python numpy pyserial

```



---

### Step 3: Run the Python Script

1. Download or clone this repository to your computer.
2. Open your terminal *inside* the project folder.
3. Run the script by passing your **ESP32 IP address** and your computer's **COM port**:
```bash
python main.py --ip <ESP32_IP_ADDRESS> --com <YOUR_PC_COM_PORT>

```


* *Example:* `python main.py --ip 192.168.1.50 --com COM6`



---













# Guide d'installation en Français

### Étape 1 : Flasher le serveur web de la caméra sur l'ESP32-S3

1. **Ouvrez** le logiciel **Arduino IDE** sur votre ordinateur.
2. Allez dans le menu `Outils` > `Carte` > `Gestionnaire de cartes` > `esp32 par Espressif Systems (3 3.11)`.
3. Ensuite allez dans Outils > Carte, Une case esp32 est alors apparue, cliquer dessus descendez et sélectionnez XIAO_ESP32S3.
4. Importez le fichier "" si pas déjà fait. Renseignez les identifiants de votre réseau Wi-Fi dans le code :
```cpp
const char* ssid = "NOM_DE_VOTRE_WIFI";
const char* password = "MOT_DE_PASSE_WIFI";

```
<p align="center"><img src="Dtest_signe/images/motdepasse.png" width="600"></p>

5. Branchez votre ESP32-S3 en USB, sélectionnez votre carte et le bon **Port COM** dans le menu `Outils`, puis cliquez sur `Téléverser`.
6. Ouvrez le `Moniteur Série` (réglez la vitesse sur `115200`), appuyez sur le bouton de réinitialisation de la carte, et notez l'**Adresse IP** qui s'affiche (ex: `192.168.1.50`).

---

### Étape 2 : Installer les dépendances Python

1. Assurez-vous d'avoir **Python** installé sur votre machine.
2. Ouvrez votre terminal (ou invite de commande) et tapez la commande suivante pour installer les bibliothèques indispensables :
```bash
pip install opencv-python numpy pyserial

```



---

### Étape 3 : Lancer le script Python

1. Téléchargez ou clonez ce dépôt sur votre ordinateur.
2. Ouvrez votre terminal directement **à l'intérieur du dossier** du projet.
3. Lancez le programme en indiquant l'**adresse IP de votre ESP32** et votre **port de communication (COM)** :
```bash
python main.py --ip <ADRESSE_IP_ESP32> --com <VOTRE_PORT_COM>

```


* *Exemple :* `python main.py --ip 192.168.1.50 --com COM6`


3. Appuyez sur **Entrée** et patientez pendant le transfert. Actualisez votre page GitHub : votre projet y est désormais en ligne !


# ✍️ ESP32-S3 Real-Time Air Writing & Character Recognition

Un système de reconnaissance de caractères en temps réel basé sur un flux vidéo **ESP32-S3 Sense** et **OpenCV**, utilisant une grille binaire 20x20 et un apprentissage direct par fichier texte avec communication série.

<p align="center"><img src="images/motdepasse.png" width="600"></p>

---

## <u>Guide d'installation / Setup Guide</u>

### <u>1. Flasher l'ESP32-S3 / Flash the ESP32-S3</u>
1. Ouvrez **Arduino IDE**.
2. Allez dans `Fichier` > `Exemples` > `ESP32` > `Camera` et choisissez `CameraWebServer`.
3. Décommentez la ligne correspondant à votre modèle de carte (ex: `#define CAMERA_MODEL_XIAO_ESP32S3`).
4. Renseignez vos identifiants Wi-Fi :
   ```cpp
   const char* ssid = "VOTRE_WIFI";
   const char* password = "VOTRE_MOT_DE_PASSE";
