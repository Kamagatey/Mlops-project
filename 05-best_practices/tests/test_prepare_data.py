# tests/test_prepare_data.py

import pandas as pd
from prepare_data import preprocess_data


def test_preprocess_shape():
    df = pd.read_csv(
        "data/Traffic_Crashes.csv"
    )  # Utilise bien un chemin relatif valide
    X, y, _ = preprocess_data(df)

    # Le nombre de lignes doit correspondre
    assert X.shape[0] == len(y), "Mismatch entre X et y"
    assert X.shape[1] > 0, "Aucune feature extraite"


def test_target_binary():
    """Test que la target est bien binaire (0 ou 1)"""
    df = pd.read_csv("data/Traffic_Crashes.csv")
    _, y, _ = preprocess_data(df)

    assert set(y) == {0, 1}, \
        f"ERREUR: Target non binaire. Valeurs trouvées: {set(y)}"
