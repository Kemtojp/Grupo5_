"""
Entrenamiento del modelo Hit Predictor — Grupo 5
=================================================
Este script es la version ejecutable de notebooks/03_model_retraining.ipynb.
Entrena, evalua CONTRA UN BASELINE y guarda el modelo + metricas.

Correr con:  python notebooks/train_model.py
"""

import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "spotify_clean.csv"
MODELS = ROOT / "models"
MODELS.mkdir(exist_ok=True)

# Las 7 originales del Integrante 2 + 3 que subieron el ROC-AUC de 0.708 a 0.743
# (duration_min, instrumentalness, liveness). El orden de esta lista es el contrato:
# se guarda en features.pkl y la app SIEMPRE lo lee de ahi, nunca lo escribe a mano.
FEATURES = [
    "danceability",
    "energy",
    "valence",
    "tempo",
    "loudness",
    "speechiness",
    "acousticness",
    "duration_min",
    "instrumentalness",
    "liveness",
]
SEED = 42

# ---------------------------------------------------------------- 1. Datos
df = pd.read_csv(DATA)
X = df[FEATURES]
y = df["is_hit"]

print(f"Dataset: {len(df)} canciones | hits: {y.mean():.1%} | no-hits: {1 - y.mean():.1%}")

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=SEED, stratify=y
)

# ------------------------------------------------- 2. Baseline obligatorio
# Un modelo que SIEMPRE dice "no es hit". Cualquier modelo real debe superarlo.
dummy = DummyClassifier(strategy="most_frequent").fit(X_train, y_train)
baseline_acc = accuracy_score(y_test, dummy.predict(X_test))
print(f"\nBASELINE (siempre 'no hit') -> accuracy = {baseline_acc:.3f} | ROC-AUC = 0.500")

# ------------------------------------------------- 3. Comparacion de modelos
candidatos = {
    "LogisticRegression": Pipeline(
        [
            ("scaler", StandardScaler()),
            (
                "clf",
                LogisticRegression(
                    max_iter=2000, class_weight="balanced", random_state=SEED
                ),
            ),
        ]
    ),
    "RandomForest": RandomForestClassifier(
        n_estimators=400,
        max_depth=12,
        min_samples_leaf=5,
        class_weight="balanced_subsample",
        random_state=SEED,
        n_jobs=-1,
    ),
}

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=SEED)
resultados = {}
for nombre, modelo in candidatos.items():
    auc = cross_val_score(modelo, X_train, y_train, cv=cv, scoring="roc_auc", n_jobs=-1)
    resultados[nombre] = auc.mean()
    print(f"  {nombre:<20} ROC-AUC (CV 5-fold) = {auc.mean():.3f} (+/- {auc.std():.3f})")

mejor_nombre = max(resultados, key=resultados.get)
modelo = candidatos[mejor_nombre]
print(f"\nModelo elegido: {mejor_nombre}")

modelo.fit(X_train, y_train)

# ------------------------------------------------- 4. Umbral de decision
# El 0.5 por defecto no es sagrado. Lo elegimos maximizando la EXACTITUD
# BALANCEADA (promedio de aciertos en cada clase) usando validacion cruzada
# sobre el train, para no mirar el test antes de tiempo.
from sklearn.model_selection import cross_val_predict

proba_cv = cross_val_predict(
    candidatos[mejor_nombre], X_train, y_train, cv=cv, method="predict_proba", n_jobs=-1
)[:, 1]

umbrales = np.arange(0.20, 0.81, 0.01)
scores = [balanced_accuracy_score(y_train, (proba_cv >= t).astype(int)) for t in umbrales]
UMBRAL = float(umbrales[int(np.argmax(scores))])
print(f"Umbral optimo (exactitud balanceada en CV): {UMBRAL:.2f}")

# ------------------------------------------------- 5. Evaluacion final
proba_test = modelo.predict_proba(X_test)[:, 1]
pred_test = (proba_test >= UMBRAL).astype(int)

metrics = {
    "modelo": mejor_nombre,
    "n_total": int(len(df)),
    "n_train": int(len(X_train)),
    "n_test": int(len(X_test)),
    "tasa_hits": float(y.mean()),
    "umbral": UMBRAL,
    "baseline_accuracy": float(baseline_acc),
    "accuracy": float(accuracy_score(y_test, pred_test)),
    "balanced_accuracy": float(balanced_accuracy_score(y_test, pred_test)),
    "precision": float(precision_score(y_test, pred_test)),
    "recall": float(recall_score(y_test, pred_test)),
    "f1": float(f1_score(y_test, pred_test)),
    "roc_auc": float(roc_auc_score(y_test, proba_test)),
    "matriz_confusion": confusion_matrix(y_test, pred_test).tolist(),
    "features": FEATURES,
}

print("\n=== METRICAS SOBRE EL 20% DE PRUEBA ===")
print(f"  ROC-AUC ............ {metrics['roc_auc']:.3f}   (0.5 = azar)")
print(f"  Balanced accuracy .. {metrics['balanced_accuracy']:.3f}   (0.5 = azar)")
print(f"  Accuracy ........... {metrics['accuracy']:.3f}   (baseline {baseline_acc:.3f})")
print(f"  Precision (hit) .... {metrics['precision']:.3f}")
print(f"  Recall (hit) ....... {metrics['recall']:.3f}")
print(f"  F1 (hit) ........... {metrics['f1']:.3f}")
print("\n" + classification_report(y_test, pred_test, target_names=["No hit", "Hit"]))

# ------------------------------------------------- 6. Importancia de features
if hasattr(modelo, "feature_importances_"):
    imp = pd.Series(modelo.feature_importances_, index=FEATURES).sort_values(
        ascending=False
    )
else:
    imp = pd.Series(
        np.abs(modelo.named_steps["clf"].coef_[0]), index=FEATURES
    ).sort_values(ascending=False)
imp = imp / imp.sum()
metrics["importancias"] = {k: float(v) for k, v in imp.items()}
print("Peso de cada caracteristica:")
for k, v in imp.items():
    print(f"  {k:<15} {v:.1%}")

# ------------------------------------------------- 7. Guardar
# compress=3: baja el .pkl de ~12 MB a ~3 MB. Importante porque GitHub avisa
# a partir de 50 MB y el repo se clona mas rapido en el deploy.
joblib.dump(modelo, MODELS / "model.pkl", compress=3)
joblib.dump(FEATURES, MODELS / "features.pkl")
(MODELS / "metrics.json").write_text(json.dumps(metrics, indent=2, ensure_ascii=False))
print(f"\nGuardado en {MODELS}/ -> model.pkl, features.pkl, metrics.json")
