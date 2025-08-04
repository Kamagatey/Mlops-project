# tests/test_integration_training.py

import subprocess


def test_training_runs():
    result = subprocess.run(
        ["python", "train_rf_optuna.py"],
        capture_output=True, text=True
        )

    print("\n[stdout]\n", result.stdout)
    print("\n[stderr]\n", result.stderr)

    assert result.returncode == 0, \
        "Le script d'entraînement a échoué"
    assert (
        "Model saved" in result.stdout
        or "Modèle sauvegardé" in result.stdout
    ), "Aucune confirmation que le modèle a été sauvegardé"
