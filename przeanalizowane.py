import os
import pandas as pd
from sklearn.model_selection import KFold
from sklearn.preprocessing import LabelEncoder
'''
tutaj przygotowuje dane z pliku merge, zastępuje zera, przypisuje etykiety itd, podział na 5 folderów
W tym pliku tylko metadane+etykiety, już przetworzone
'''
# Ścieżki do danych
ISIC_BASE_PATH = "D:/studia/magistera/ISIC_2019"
ISIC_CSV_PATH = os.path.join(ISIC_BASE_PATH,"train", "merged", "ISIC2019.csv")  # Plik połączony
ISIC_PARSED_PATH = os.path.join(ISIC_BASE_PATH, "przeanalizowane")  # Folder na wyniki

# Utwórz folder na wyniki, jeśli nie istnieje
os.makedirs(ISIC_PARSED_PATH, exist_ok=True)

# Wczytywanie danych i zamiana braków w metadanych
data = pd.read_csv(ISIC_CSV_PATH)

# Zamiana brakujących wartości
data.fillna({"age_approx": 0, "sex": "missing", "anatom_site_general": "missing"}, inplace=True)

# Podział na K-foldery
kf = KFold(n_splits=5, shuffle=True, random_state=32)
data["fold"] = -1
for fold, (train_idx, val_idx) in enumerate(kf.split(data)):
    data.loc[val_idx, "fold"] = fold

# Zamiana etykiet na numeryczne
label_encoder = LabelEncoder()
data["diagnostic_number"] = label_encoder.fit_transform(data["diagnostic"])

# Zapis pliku wynikowego
train_output_path = os.path.join(ISIC_PARSED_PATH, "ISIC2019_przeanalizowane_train.csv")
data.to_csv(train_output_path, index=False)

print(f"Zapisano przetworzony plik treningowy: {train_output_path}")

# Opcjonalne: Przetwarzanie danych testowych (jeśli są dostępne)
test_metadata_path = os.path.join(ISIC_BASE_PATH, "test","merged_test","ISIC2019.csv")  # Ścieżka do metadanych testowych
if os.path.exists(test_metadata_path):
    data_final_test = pd.read_csv(test_metadata_path)
    
    # Zamiana brakujących wartości
    data_final_test.fillna({"age_approx": 0, "sex": "missing", "anatom_site_general": "missing"}, inplace=True)
    
    test_output_path = os.path.join(ISIC_PARSED_PATH, "ISIC2019_przeanalizowane_test.csv")
    data_final_test.to_csv(test_output_path, index=False)
    print(f"Zapisano przetworzony plik testowy: {test_output_path}")
