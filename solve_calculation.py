import argparse
import cv2
import numpy as np
import serial
import time
import os

CONFIG_FILE = "characters_config.txt"

# Paramètres de la grille de cubes (petits carrés 20x20)
GRID_ROWS = 20
GRID_COLS = 20

def get_key_points_and_skeleton(thresh):
    """Extrait un ensemble dense de points recouvrant tout le tracé à partir du point le plus bas."""
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    
    contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return [], None, [], 0, 0
    
    valid_contours = [c for c in contours if cv2.contourArea(c) > 15]
    if not valid_contours:
        return [], None, [], 0, 0

    mask = np.zeros_like(thresh)
    cv2.drawContours(mask, valid_contours, -1, 255, thickness=cv2.FILLED)
    mask = cv2.dilate(mask, kernel, iterations=1)

    all_key_points = []
    all_angle_degrees = []
    total_curves = 0

    for cnt in valid_contours:
        points_flat = cnt.reshape(-1, 2)
        if len(points_flat) < 3:
            continue

        # 1. Point le plus bas (le plus grand Y sur l'image)
        lowest_idx = max(range(len(points_flat)), key=lambda i: points_flat[i][1])
        points_flat = np.roll(points_flat, -lowest_idx, axis=0)

        # 2. Angles et inclinaisons en degrés
        epsilon = 0.025 * cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, epsilon, True)
        approx_squeezed = approx.reshape(-1, 2)
        
        angle_pts = []
        n_approx = len(approx_squeezed)
        for i in range(n_approx):
            pt = approx_squeezed[i]
            angle_pts.append(tuple(pt))
            
            prev_pt = approx_squeezed[i - 1]
            next_pt = approx_squeezed[(i + 1) % n_approx]
            
            v1 = prev_pt - pt
            v2 = next_pt - pt
            
            norm1 = np.linalg.norm(v1)
            norm2 = np.linalg.norm(v2)
            if norm1 > 0 and norm2 > 0:
                cos_angle = np.dot(v1, v2) / (norm1 * norm2)
                cos_angle = np.clip(cos_angle, -1.0, 1.0)
                deg = float(np.degrees(np.arccos(cos_angle)))
                all_angle_degrees.append(round(deg, 1))

        # 3. Dense covering: ajouter des points très rapprochés tout le long du contour
        for i in range(0, len(points_flat), 3):
            total_curves += 1

        combined_indices = []
        for apt in angle_pts:
            dists = [np.linalg.norm(np.array(apt) - np.array(cp)) for cp in points_flat]
            combined_indices.append(np.argmin(dists))

        for i in range(0, len(points_flat), 3):
            combined_indices.append(i)

        combined_indices = sorted(list(set(combined_indices)))

        filtered_indices = []
        for idx in combined_indices:
            pt = points_flat[idx]
            if not any(np.linalg.norm(np.array(pt) - np.array(points_flat[existing_idx])) < 4 for existing_idx in filtered_indices):
                filtered_indices.append(idx)

        filtered_pts = [tuple(points_flat[idx]) for idx in filtered_indices]

        if filtered_pts:
            all_key_points.append(filtered_pts)

    return all_key_points, mask, all_angle_degrees, len(all_angle_degrees), max(1, total_curves // 2) if total_curves > 0 else 0

def compute_grid_binary_matrix(roi_shape, grouped_points, rows=GRID_ROWS, cols=GRID_COLS):
    """Divise la ROI en une grille de petits cubes et retourne une matrice binaire (1 si contact, 0 sinon)."""
    h, w = roi_shape[:2]
    cell_h = h / rows
    cell_w = w / cols
    
    grid_matrix = np.zeros((rows, cols), dtype=int)
    
    points_mask = np.zeros((h, w), dtype=np.uint8)
    for contour_points in grouped_points:
        for pt in contour_points:
            cv2.circle(points_mask, pt, 4, 255, -1)

    for r in range(rows):
        for c in range(cols):
            y_start = int(r * cell_h)
            y_end = int((r + 1) * cell_h)
            x_start = int(c * cell_w)
            x_end = int((c + 1) * cell_w)
            
            cell_region = points_mask[y_start:y_end, x_start:x_end]
            if np.any(cell_region > 0):
                grid_matrix[r, c] = 1
                
    return grid_matrix

def load_dataset_from_config():
    """Charge les configurations depuis le fichier texte."""
    dataset = []
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or "Caractere:" not in line:
                    continue
                try:
                    parts = line.split(" | ")
                    char_label = parts[0].split(": ")[1].strip()
                    grid_str = parts[1].split(": ")[1].strip()
                    angles_str = parts[2].split(": ")[1].strip()
                    curves_str = parts[3].split(": ")[1].strip()

                    grid_flat = [int(char) for char in grid_str]
                    grid_matrix = np.array(grid_flat).reshape((GRID_ROWS, GRID_COLS))

                    dataset.append({
                        'char': char_label,
                        'grid': grid_matrix,
                        'angles': angles_str,
                        'curves': curves_str
                    })
                except Exception as e:
                    print(f"Erreur de lecture d'une ligne du fichier de config : {e}")
    return dataset

def save_and_organize_config(char_label, angle_degrees, has_curve, grid_matrix):
    """Enregistre la nouvelle config et trie tout le fichier par caractère."""
    dataset = load_dataset_from_config()

    grid_flat_str = "".join(str(val) for val in grid_matrix.flatten())
    angles_str = str(angle_degrees)
    
    dataset.append({
        'char': char_label,
        'grid': grid_matrix,
        'angles': angles_str,
        'curves': str(has_curve),
        'grid_str': grid_flat_str
    })

    # Trier par nom de caractère (ex: '1', '2', etc.)
    dataset.sort(key=lambda x: x['char'])

    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        for item in dataset:
            if 'grid_str' in item:
                g_str = item['grid_str']
            else:
                g_str = "".join(str(val) for val in item['grid'].flatten())
            
            line = f"Caractere: {item['char']} | Grille Binaire ({GRID_ROWS}x{GRID_COLS}): {g_str} | Angles (Degrés): {item['angles']} | Courbes: {item['curves']}\n"
            f.write(line)
    print(f">> [Fichier mis à jour] Nouvelle version enregistrée pour le caractère '{char_label}'. Total configurations : {len(dataset)}")

def predict_from_config(current_grid, dataset):
    """Compare la grille actuelle avec toutes les configurations enregistrées."""
    if not dataset:
        return "?"

    best_match = "?"
    max_similarity = -1

    for item in dataset:
        ref_grid = item['grid']
        similarity = np.sum(current_grid == ref_grid)
        
        if similarity > max_similarity:
            max_similarity = similarity
            best_match = item['char']

    total_cells = GRID_ROWS * GRID_COLS
    if max_similarity < (total_cells * 0.60):  # Seuil abaissé à 60% pour faciliter les correspondances initiales
        return "?"

    return best_match

def connect_stream(stream_url):
    print(f"Connexion au flux vidéo : {stream_url}...")
    cap = cv2.VideoCapture(stream_url)
    return cap

def main():
    parser = argparse.ArgumentParser(description="Reconnaissance exclusive via fichier de configuration")
    parser.add_argument('--ip', required=True, help="IP de l'ESP32-S3")
    parser.add_argument('--com', required=True, help="Port COM (ex: COM6)")
    args = parser.parse_args()

    stream_url = f"http://{args.ip}:81/stream"
    cap = connect_stream(stream_url)

    ser = None
    try:
        ser = serial.Serial(args.com, 115200, timeout=1)
        time.sleep(2)
        print(f"Connecté au port série {args.com}")
    except Exception as e:
        print(f"Attention - Erreur de port série : {e}")

    dataset = load_dataset_from_config()
    print(f">> Configurations chargées depuis le fichier : {len(dataset)} exemples connus.")

    print("\n--- Instructions ---")
    print("1. Écrivez votre tracé dans le carré jaune.")
    print("2. Appuyez sur 's' pour analyser.")
    print("3. Si la proposition est correcte, validez avec Entrée. Si elle est fausse, tapez 'f' pour donner la vraie valeur.")
    print("4. Appuyez sur 'q' pour quitter.\n")

    fail_count = 0

    while True:
        if cap is None or not cap.isOpened():
            time.sleep(1)
            cap = connect_stream(stream_url)
            continue

        ret, frame = cap.read()
        if not ret:
            fail_count += 1
            if fail_count > 20:
                cap.release()
                fail_count = 0
            time.sleep(0.1)
            continue
        
        fail_count = 0
        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape
        
        x1, y1, x2, y2 = int(w * 0.4), int(h * 0.4), int(w * 0.6), int(h * 0.6)
        
        display_frame = frame.copy()
        roi = frame[y1:y2, x1:x2]
        
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                      cv2.THRESH_BINARY_INV, 15, 8)
        
        grouped_points, clean_mask, angle_degrees_list, det_angles, det_curves = get_key_points_and_skeleton(thresh)
        
        grid_matrix = compute_grid_binary_matrix(roi.shape, grouped_points)

        overlay_roi = roi.copy()
        grid_h, grid_w = roi.shape[:2]
        cell_h = grid_h / GRID_ROWS
        cell_w = grid_w / GRID_COLS

        for r in range(GRID_ROWS):
            for c in range(GRID_COLS):
                y_start = int(r * cell_h)
                y_end = int((r + 1) * cell_h)
                x_start = int(c * cell_w)
                x_end = int((c + 1) * cell_w)
                
                if grid_matrix[r, c] == 1:
                    color = (0, 255, 0) # Vert
                    alpha = 0.35
                else:
                    color = (0, 0, 255) # Rouge
                    alpha = 0.12

                sub_rect = overlay_roi[y_start:y_end, x_start:x_end]
                colored_box = np.full_like(sub_rect, color, dtype=np.uint8)
                overlay_roi[y_start:y_end, x_start:x_end] = cv2.addWeighted(sub_rect, 1 - alpha, colored_box, alpha, 0)
                
                cv2.rectangle(overlay_roi, (x_start, y_start), (x_end, y_end), (200, 200, 200), 1)

        for contour_points in grouped_points:
            if len(contour_points) > 1:
                for i in range(len(contour_points) - 1):
                    cv2.line(overlay_roi, contour_points[i], contour_points[i+1], (255, 0, 0), 1)
            for pt in contour_points:
                cv2.circle(overlay_roi, pt, 3, (0, 0, 255), -1)

        display_frame[y1:y2, x1:x2] = overlay_roi
        cv2.rectangle(display_frame, (x1, y1), (x2, y2), (0, 255, 255), 2)

        total_points_count = sum(len(cp) for cp in grouped_points)
        
        live_pred = "?"
        if len(dataset) > 0 and clean_mask is not None and total_points_count >= 2:
            live_pred = predict_from_config(grid_matrix, dataset)

        cv2.putText(display_frame, f"Traduction: {live_pred}", (30, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.putText(display_frame, f"Angles: {det_angles} | Courbes: {det_curves}", (30, 90), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2, cv2.LINE_AA)

        cv2.imshow("ESP32-S3 - Reconnaissance Fichier", display_frame)

        key = cv2.waitKey(30) & 0xFF

        if key == ord('s'):
            if clean_mask is None or total_points_count < 2:
                print("\n[!] Tracé insuffisant ou mal détecté, réessayez.")
                continue

            cap.release()

            current_pred = live_pred
            print(f"\n--- Analyse ---")
            print(f">> Traduction proposée par le fichier : '{current_pred}' (Angles: {det_angles}, Courbes: {det_curves})")
            
            feedback = input("Est-ce VRAI ? [Entrée/v], tapez 'f' pour FAUX, ou 'r' pour ANNULER : ").strip().lower()

            if feedback == 'r':
                print(">> Action annulée. Retour au flux en direct.\n")
                cap = connect_stream(stream_url)
                continue

            if feedback == '' or feedback == 'v':
                if current_pred == "?":
                    print("[!] Impossible de valider automatiquement car la prédiction est '?'. Veuillez utiliser 'f' pour indiquer le caractère.")
                    true_val = input("-> Entrez la vraie valeur pour ce tracé : ").strip()
                    if true_val:
                        save_and_organize_config(true_val, angle_degrees_list, det_curves, grid_matrix)
                        dataset = load_dataset_from_config()
                        if ser and ser.is_open:
                            ser.write((true_val + "\n").encode('utf-8'))
                            print(f">> Envoyé à l'ESP32 : {true_val}")
                else:
                    print(f">> Confirmé VRAI : {current_pred}")
                    save_and_organize_config(current_pred, angle_degrees_list, det_curves, grid_matrix)
                    dataset = load_dataset_from_config()
                    if ser and ser.is_open:
                        ser.write((current_pred + "\n").encode('utf-8'))
                        print(f">> Envoyé à l'ESP32 : {current_pred}")
            
            elif feedback == 'f':
                true_val = input("-> Entrez la VRAIE valeur correcte : ").strip()
                if true_val:
                    save_and_organize_config(true_val, angle_degrees_list, det_curves, grid_matrix)
                    dataset = load_dataset_from_config()
                    if ser and ser.is_open:
                        ser.write((true_val + "\n").encode('utf-8'))
                        print(f">> Envoyé à l'ESP32 : {true_val}")
            
            print(">> Prêt pour le test suivant !\n")
            cap = connect_stream(stream_url)

        elif key == ord('q'):
            break

    if cap:
        cap.release()
    cv2.destroyAllWindows()
    if ser and ser.is_open:
        ser.close()

if __name__ == '__main__':
    main()