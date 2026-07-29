# 📘 Guía completa — Hit Predictor & Trendy Dashboard

Todo lo que hay que saber para **correr el proyecto en tu computador** y para
**entender cómo funciona por dentro**, línea por línea.

Está escrita para que cualquier integrante del equipo pueda seguirla sin ayuda, y
para que puedas defender cualquier parte del código en la presentación.

---

## Índice

0. [⚠️ Estado del proyecto: qué falta](#0-estado-del-proyecto-qué-falta)
1. [Qué es esto, en 60 segundos](#1-qué-es-esto-en-60-segundos)
2. [Instalación paso a paso](#2-instalación-paso-a-paso)
3. [Correr la app](#3-correr-la-app)
4. [Volver a trabajar al día siguiente](#4-volver-a-trabajar-al-día-siguiente)
5. [El flujo completo de los datos](#5-el-flujo-completo-de-los-datos)
6. [Qué hace cada archivo](#6-qué-hace-cada-archivo)
7. [Cómo funciona Streamlit (leer esto antes de tocar app.py)](#7-cómo-funciona-streamlit)
8. [Recorrido por `app.py`](#8-recorrido-por-apppy)
9. [Recorrido por `charts.py`](#9-recorrido-por-chartspy)
10. [Recorrido por el modelo](#10-recorrido-por-el-modelo)
11. [Cómo modificar cosas](#11-cómo-modificar-cosas)
12. [Probar un gráfico suelto, sin levantar la app](#12-probar-un-gráfico-suelto)
13. [Errores comunes y cómo arreglarlos](#13-errores-comunes)
14. [Chuleta de comandos](#14-chuleta-de-comandos)
15. [Checklist: ¿está todo funcionando?](#15-checklist-final)

---

## 0. Estado del proyecto: qué falta

> **El código está terminado y probado. Lo que falta es publicarlo y entregarlo.**
> Esta sección es la lista viva de pendientes: marca las casillas a medida que se
> vayan cerrando. Los pasos detallados de cada bloque están en `docs/ENTREGA.md`.

### 🔴 Bloquea todo lo demás

Nada de esto avanza en paralelo: cada punto depende del anterior.

- [ ] **Subir el código al repositorio.** Mientras el proyecto viva solo en un ZIP en
      un computador, nadie del equipo puede probarlo, no se puede publicar la app y no
      se puede abrir el Pull Request. *(Responsable: Git & Docs Lead)*
- [ ] **Publicar la app en Streamlit Cloud** y pegar la URL en el `README.md` (aparece
      dos veces marcada como *pendiente*). La rúbrica exige una URL pública: sin eso el
      entregable está incompleto por más buena que esté la app.
      *(Responsable: App Architect)*

> ⏰ **Haz el deploy con días de margen, no la mañana de la entrega.** Es el paso que
> más se rompe — versiones de librerías, archivos que no se subieron, rutas mal
> escritas. Conviene descubrir el problema cuando todavía hay tiempo de arreglarlo.

### 🟡 Solo una persona puede resolverlos (no se pueden inventar)

- [ ] **Poner la URL real del repositorio.** Hoy hay un placeholder en dos lugares:
      la constante `REPO_URL` en `app.py` y el encabezado del `README.md`.
- [ ] **Copiar la licencia exacta del dataset** desde su ficha en Kaggle, al `README.md`
      y a la constante `LICENCIA_DATASET` de `app.py`. La rúbrica pide *licencia
      verificable*, así que no se inventa ni se asume.
- [ ] **Preguntarle al docente** el nombre exacto de la carpeta para el Pull Request y
      la fecha límite de entrega: en el repositorio del curso ambas casillas figuran
      como *(Por definir)*. Conviene preguntarlo cuanto antes, porque la respuesta
      puede cambiar el plan.
- [ ] **Que el ML Engineer valide el cambio de 7 a 10 variables.** El modelo se
      reentrenó agregando `duration_min`, `instrumentalness` y `liveness`, lo que subió
      el ROC-AUC de 0,708 a 0,743. Es una modificación sobre su entregable y tiene que
      estar de acuerdo. El detalle está en `notebooks/03_model_retraining.ipynb`.

### 🟢 Coherencia de la documentación

- [ ] **Cerrar la contradicción del notebook 02.** Ese notebook todavía afirma que *"los
      7 atributos son los mismos que luego el usuario ajustará con los sliders"*, y la
      app tiene 10. Si el docente lee los notebooks en orden va a encontrar la
      inconsistencia. Se arregla con una celda de markdown al final del 02 que explique
      que ese modelo fue reemplazado y remita al notebook 03.
- [ ] **Verificar que las capturas del `README.md` estén actualizadas** si se cambia
      algo visual de la app.

### 🔵 Entrega y presentación

- [ ] **Abrir el Pull Request** al repositorio del curso, dentro de la carpeta que
      indique el docente. Es **un solo PR por equipo**.
- [ ] **Que cada integrante levante la app en su propio computador** siguiendo la
      sección 2 de esta guía. Si a alguien no le funciona, es mucho mejor saberlo
      antes del día de la entrega.
- [ ] **Ensayar el guion cronometrado.** Son 7 minutos de presentación más 3 de
      preguntas, no 10 de exposición. El guion tramo por tramo y las preguntas más
      probables del docente están en `docs/ENTREGA.md`.
- [ ] **Grabar un video corto de la demo funcionando.** Si la conexión falla el día de
      la presentación, ese respaldo salva los 7 minutos.

### Lo que ya está listo (no hay que rehacerlo)

| | |
|---|---|
| ✅ | Los 6 gráficos en Plotly, con paleta validada para daltonismo y estados vacíos |
| ✅ | La app de Streamlit completa: 4 pestañas, filtros, glosario, 4 KPIs y simulador |
| ✅ | El modelo reentrenado, evaluado contra un baseline explícito y documentado |
| ✅ | `requirements.txt` con versiones fijadas y `.streamlit/config.toml` |
| ✅ | `README.md`, esta guía, `docs/ENTREGA.md` y la documentación técnica |
| ✅ | La app probada en 8 escenarios distintos, incluidos los casos borde, sin errores |

---

## 1. Qué es esto, en 60 segundos

Una **aplicación web** que se abre en el navegador y responde una pregunta:

> ¿Se puede saber si una canción va a ser un éxito solo a partir de cómo suena?

Tiene cuatro pantallas:

| Pestaña | Qué hace |
|---|---|
| 📈 Evolución histórica | Muestra cómo cambió el sonido de la música año a año |
| 🔍 Anatomía de un hit | Compara el perfil de un hit contra una canción común |
| 🎧 Hit Predictor | Un simulador: mueves 10 controles y el modelo predice si sería hit |
| 📋 Ficha técnica | El hallazgo en simple, las métricas del modelo y el dataset |

Por dentro son **tres piezas**:

```
Datos (CSV)  →  Modelo entrenado (.pkl)  →  App web (Streamlit)
4.494                RandomForest              4 pestañas
canciones            ROC-AUC 0,744             10 sliders
```

Y **tres tecnologías**:

- **pandas** — carga y filtra la tabla de canciones
- **scikit-learn** — el modelo de Machine Learning que hace la predicción
- **Streamlit + Plotly** — convierte todo eso en una página web interactiva sin
  escribir nada de HTML ni JavaScript

---

## 2. Instalación paso a paso

### 2.1 Tener Python instalado

Necesitas **Python 3.11, 3.12 o 3.13**. Primero revisa si ya lo tienes.

**Windows** — abre **PowerShell** (botón Inicio → escribe "PowerShell" → Enter):

```powershell
python --version
```

**macOS** — abre **Terminal** (Cmd+Espacio → escribe "Terminal" → Enter):

```bash
python3 --version
```

Si responde algo como `Python 3.12.4`, ya está. Si dice "no se reconoce el comando"
o te sale una versión 3.8 o menor, instálalo:

- **Windows:** descarga el instalador desde [python.org/downloads](https://www.python.org/downloads/).
  ⚠️ **Muy importante:** en la primera pantalla del instalador marca la casilla
  **"Add Python to PATH"** antes de darle a Install. Si no la marcas, PowerShell no
  va a encontrar Python y vas a tener que reinstalar.
- **macOS:** descarga desde [python.org/downloads](https://www.python.org/downloads/)
  y ejecuta el `.pkg`. (Si usas Homebrew: `brew install python@3.12`.)

> **Ojo en macOS:** el sistema trae un Python viejo. Por eso en Mac siempre se escribe
> `python3` y `pip3`, no `python` y `pip`. En Windows es al revés: `python` y `pip`.

### 2.2 Descargar el proyecto

Si tienes Git instalado:

```bash
git clone <URL-DEL-REPOSITORIO>.git
cd <carpeta-del-proyecto>
```

Si no tienes Git, descarga el ZIP desde GitHub (botón verde **Code → Download ZIP**),
descomprímelo, y entra a la carpeta desde la terminal.

**Cómo entrar a la carpeta desde la terminal:**

- **Windows:** abre la carpeta en el Explorador, haz clic en la barra de dirección,
  escribe `powershell` y presiona Enter. Se abre PowerShell ya ubicado ahí.
- **macOS:** escribe `cd ` (con espacio) en la Terminal y **arrastra la carpeta**
  desde el Finder a la ventana de la Terminal. Presiona Enter.

Para confirmar que estás en el lugar correcto:

```powershell
# Windows
dir
```
```bash
# macOS
ls
```

Tienes que ver `app.py`, `charts.py`, `requirements.txt` y las carpetas `data/`,
`models/`, `notebooks/`.

### 2.3 Crear el entorno virtual

Un **entorno virtual** es una carpeta donde se instalan las librerías de *este*
proyecto, sin ensuciar el resto de tu computador ni chocar con otros proyectos.
Se crea una sola vez.

**Windows (PowerShell):**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Si sale un error rojo que dice **"la ejecución de scripts está deshabilitada"**,
ejecuta esto una sola vez y vuelve a intentar el comando anterior:

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

**macOS (Terminal):**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Cómo saber que funcionó:** al principio de la línea de la terminal aparece
`(.venv)`. Así:

```
(.venv) PS C:\Users\<usuario>\proyecto>
(.venv) <usuario>@<equipo> proyecto %
```

Si no aparece `(.venv)`, el entorno **no está activado** y los siguientes pasos van a
instalar las librerías en el lugar equivocado.

### 2.4 Instalar las librerías

Con el entorno activado:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Tarda entre 1 y 4 minutos. Instala seis librerías:

| Librería | Para qué |
|---|---|
| `streamlit` | Construye la página web |
| `pandas` | Maneja la tabla de datos |
| `numpy` | Cálculo numérico (lo usa pandas por debajo) |
| `scikit-learn` | El modelo de Machine Learning |
| `plotly` | Los gráficos interactivos |
| `joblib` | Guarda y carga el modelo entrenado |

> **Si `pip install` falla** con un error de compilación o de "no matching
> distribution", es porque tu versión de Python no tiene wheels para alguna versión
> fijada. Solución: abre `requirements.txt` y borra los `==versión` de **todas menos
> scikit-learn**. `scikit-learn==1.8.0` tiene que quedarse tal cual, porque
> `model.pkl` fue creado con esa versión exacta y una distinta puede fallar al
> cargarlo o dar predicciones raras.

---

## 3. Correr la app

Con el entorno activado y estando dentro de la carpeta del proyecto:

```bash
streamlit run app.py
```

Deberías ver algo así:

```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.1.15:8501
```

El navegador se abre solo. Si no lo hace, copia `http://localhost:8501` en la barra
de direcciones.

**Para detenerla:** vuelve a la terminal y presiona `Ctrl + C` (también en Mac: es
Control, no Command).

**Truco útil:** la `Network URL` funciona desde tu celular si está en el mismo WiFi.
Sirve para probar cómo se ve la app en pantalla chica.

### Mientras la app está corriendo

Streamlit **detecta cuando guardas un archivo**. Si editas `charts.py` o `app.py` y
guardas, aparece un botón **"Rerun"** arriba a la derecha del navegador. Puedes
activar el modo automático desde el menú ⋮ → **Settings → Run on save**, y así cada
vez que guardes se recarga sola. Es la forma más cómoda de trabajar en los gráficos.

---

## 4. Volver a trabajar al día siguiente

El entorno virtual se crea una vez, pero **hay que activarlo en cada sesión nueva de
terminal**. La rutina completa es:

```powershell
# Windows
cd C:\ruta\a\carpeta-del-proyecto
.venv\Scripts\Activate.ps1
streamlit run app.py
```

```bash
# macOS
cd /ruta/a/carpeta-del-proyecto
source .venv/bin/activate
streamlit run app.py
```

Si te saltas la activación vas a ver `ModuleNotFoundError: No module named 'streamlit'`.
Ese error casi siempre significa "olvidaste activar el entorno".

---

## 5. El flujo completo de los datos

Este es el recorrido de un dato desde el disco duro hasta el gráfico en pantalla.

### 5.1 Antes de que exista la app (una sola vez, ya está hecho)

```
data/high_popularity_spotify_data.csv          ┐
data/low_popularity_spotify_data.csv           ┘
                  │
                  ▼   notebooks/01_data_cleaning.ipynb
        · junta los dos archivos
        · elimina duplicados y nulos
        · duration_ms → duration_min
        · crea is_hit = 1 si track_popularity >= 70
                  │
                  ▼
        data/spotify_clean.csv   (4.494 filas × 31 columnas)
                  │
                  ▼   notebooks/03_model_retraining.ipynb
        · separa 80% entrenamiento / 20% prueba
        · compara RandomForest vs LogisticRegression
        · elige el umbral de decisión
                  │
                  ▼
        models/model.pkl        el modelo entrenado
        models/features.pkl     el orden de las 10 variables
        models/metrics.json     las métricas que muestra la app
```

### 5.2 Cada vez que alguien abre la app

```
streamlit run app.py
        │
        ▼
1. cargar_datos()      lee spotify_clean.csv → charts.preparar() agrega
                       las columnas anio, decada y etiqueta_hit
        │
        ▼
2. cargar_modelo()     carga model.pkl, features.pkl y metrics.json
        │
        ▼
3. Se dibuja la barra lateral. El usuario elige géneros, rango de años
   y si quiere ver solo hits.
        │
        ▼
4. Se calculan dos subconjuntos:
        dff              → lo que ve el usuario (todos los filtros)
        df_comparacion   → sin el filtro de "solo hits" (lo necesita el radar)
        │
        ▼
5. Se dibujan los 4 KPIs de arriba a partir de dff
        │
        ▼
6. Cada pestaña llama a las funciones de charts.py pasándoles dff
        │
        ▼
7. En la pestaña 3, al presionar el botón:
        valores de los 10 sliders
              → DataFrame de 1 fila, con las columnas EN EL ORDEN de features.pkl
              → modelo.predict_proba(...)  → probabilidad entre 0 y 1
              → se compara contra UMBRAL (0,39) → veredicto en pantalla
```

### 5.3 El punto más importante de todo el flujo

> **`features.pkl` es un contrato.**
>
> El modelo no conoce los nombres de las columnas: recibe una lista de 10 números y
> asume que vienen en el orden en que fue entrenado. Si le pasas `energy` donde
> esperaba `danceability`, **no da error** — simplemente predice mal, en silencio.
>
> Por eso `app.py` nunca escribe la lista de variables a mano. La lee así:
>
> ```python
> features = joblib.load("models/features.pkl")
> entrada = pd.DataFrame([[valores[f] for f in FEATURES]], columns=FEATURES)
> ```
>
> Si alguna vez reentrenan el modelo agregando o quitando variables, `features.pkl`
> se actualiza solo y la app se adapta sin tocar una línea.

---

## 6. Qué hace cada archivo

```
proyecto/
│
├── app.py                    ← LA APP. Todo lo que se ve en pantalla.
├── charts.py                 ← LOS GRÁFICOS. 7 funciones que devuelven figuras.
├── requirements.txt          ← La lista de librerías con sus versiones exactas.
├── README.md                 ← La presentación del proyecto (esto lo lee el profesor).
├── GUIA.md                   ← Este archivo.
│
├── .streamlit/
│   └── config.toml           ← Fuerza el tema claro. Los colores de los gráficos
│                                están calibrados para fondo blanco.
├── data/
│   ├── high_popularity_spotify_data.csv    Datos crudos de Kaggle
│   ├── low_popularity_spotify_data.csv     Datos crudos de Kaggle
│   └── spotify_clean.csv                   ← El que usa la app (4.494 filas)
│
├── models/
│   ├── model.pkl             ← El modelo entrenado (4,5 MB)
│   ├── features.pkl          ← ['danceability', 'energy', ...] en orden
│   └── metrics.json          ← ROC-AUC, umbral, importancias, matriz de confusión
│
├── notebooks/
│   ├── 01_data_cleaning.ipynb        Limpieza (Data Engineer)
│   ├── 02_model_training.ipynb       Primer modelo (ML Engineer)
│   ├── 03_model_retraining.ipynb     Modelo corregido, con baseline
│   └── train_model.py                El notebook 03 como script ejecutable
│
└── docs/
    ├── ENTREGA.md            Pasos para publicar, hacer el PR y presentar
    ├── modelo.md             Documentación técnica del modelo
    ├── sliders_referencia.md Los 10 sliders y sus rangos
    └── capturas/             Imágenes para el README
```

**Los dos archivos que importan** son `app.py` y `charts.py`. Todo lo demás son datos,
documentación o el proceso que generó el modelo.

**La separación es intencional:** `charts.py` no sabe que existe Streamlit y `app.py`
no sabe cómo se dibuja un gráfico. Eso permite que dos personas trabajen en paralelo
sin pisarse, y permite probar un gráfico sin levantar la app entera
(ver [sección 12](#12-probar-un-gráfico-suelto)).

---

## 7. Cómo funciona Streamlit

**Esto hay que entenderlo antes de tocar `app.py`,** porque Streamlit no funciona como
un programa normal.

### La regla de oro

> **Cada vez que el usuario mueve un control, Streamlit vuelve a ejecutar
> `app.py` completo, de arriba a abajo.**

No hay "eventos" ni "callbacks" como en JavaScript. Mueves un slider → el script
entero corre otra vez desde la línea 1. Las variables se recalculan, los gráficos se
redibujan y la página se actualiza.

Esto suena ineficiente, y lo sería si no fuera por el caché.

### El caché

```python
@st.cache_data
def cargar_datos() -> pd.DataFrame:
    return charts.preparar(pd.read_csv(RAIZ / "data" / "spotify_clean.csv"))
```

`@st.cache_data` le dice a Streamlit: *"esta función siempre devuelve lo mismo, no la
ejecutes de nuevo"*. Así el CSV de 2 MB se lee **una sola vez**, no cada vez que
alguien mueve un slider.

Hay dos decoradores y se usan para cosas distintas:

| Decorador | Para qué | Por qué |
|---|---|---|
| `@st.cache_data` | datos que se pueden copiar: DataFrames, listas, diccionarios | Streamlit entrega una copia a cada usuario, así nadie modifica los datos de otro |
| `@st.cache_resource` | objetos pesados que no se copian: modelos, conexiones a bases de datos | Se comparte **la misma** instancia entre todos. Copiar un modelo de 4,5 MB en cada recarga sería absurdo |

Por eso `cargar_datos` usa `cache_data` y `cargar_modelo` usa `cache_resource`.

### Consecuencia práctica

Si cambias `data/spotify_clean.csv` o `models/model.pkl` mientras la app corre, **no
vas a ver el cambio**: el caché sigue sirviendo la versión vieja. Para forzar la
recarga, presiona `C` en el navegador o usa el menú ⋮ → **Clear cache**, y después
**Rerun**.

### El truco de las `key` en los sliders

```python
valores[f] = destino.slider(..., key=f"{preset}_{f}")
```

Streamlit identifica cada control por su `key`. Como la `key` incluye el nombre del
preset, al cambiar de "Personalizado" a "Reggaetón tipo Bad Bunny" los sliders pasan a
ser controles *distintos* y toman los valores nuevos del preset. Sin ese truco, los
sliders conservarían la posición anterior y el preset no haría nada visible.

---

## 8. Recorrido por `app.py`

El archivo está ordenado igual que la pantalla: primero lo de arriba, después lo de
abajo. Bloque por bloque:

### Bloque 1 — Configuración (líneas 13–38)

```python
RAIZ = Path(__file__).resolve().parent
```

`RAIZ` es la carpeta donde vive `app.py`. Todas las rutas se arman a partir de ahí
(`RAIZ / "data" / "spotify_clean.csv"`) en vez de escribir rutas absolutas. Esto es
lo que hace que el proyecto funcione igual en Windows, en Mac y en Streamlit Cloud
sin tocar nada.

```python
st.set_page_config(layout="wide", ...)
```

Tiene que ser **la primera llamada a Streamlit** del archivo. Si va después de
cualquier `st.algo()`, Streamlit lanza un error.

También hay dos constantes con `TODO` pendientes:

```python
REPO_URL = "https://github.com/<usuario>/<repositorio>"   # ← poner la URL real
LICENCIA_DATASET = "ver ficha del dataset en Kaggle"   # ← copiar la licencia real
```

### Bloque 2 — Carga de datos y modelo (líneas 44–59)

Las dos funciones cacheadas que ya explicamos. Al final quedan disponibles cuatro
objetos globales que usa todo el resto del archivo:

| Variable | Qué contiene |
|---|---|
| `df` | Las 4.494 canciones, ya con las columnas `anio`, `decada` y `etiqueta_hit` |
| `modelo` | El RandomForest cargado desde `model.pkl` |
| `FEATURES` | La lista de 10 nombres de variables, en orden |
| `METRICAS` | El diccionario completo de `metrics.json` |
| `UMBRAL` | `0.39` — el corte para decir "esto es un hit" |

### Bloque 3 — Configuración de los sliders (líneas 66–91)

```python
CONFIG_SLIDERS = {
    "danceability": (0.0, 1.0, 0.50, 0.01, "0.9 = Despacito · 0.2 = Bohemian Rhapsody"),
    ...
}
```

Un diccionario donde cada variable tiene una tupla de 5 elementos:
`(mínimo, máximo, valor por defecto, paso, texto de ayuda)`.

Está separado del código que dibuja los sliders a propósito: para cambiar un rango
editas una línea de datos, no lógica. El `GLOSARIO` de más abajo funciona igual.

### Bloque 4 — Barra lateral (líneas 97–121)

```python
with st.sidebar:
    ...
```

Todo lo que va dentro de ese `with` se dibuja en la barra izquierda. Tres controles:

- `st.multiselect` — géneros. Vacío significa "todos".
- `st.slider` con una tupla `(1990, anio_max)` — al pasarle dos valores, Streamlit
  crea un slider de **rango** con dos manijas.
- `st.checkbox` — el interruptor de "solo hits".

Cada uno devuelve el valor actual del control. Recuerda la regla de oro: si el usuario
mueve cualquiera de estos, el script entero vuelve a correr y estas variables traen
los valores nuevos.

### Bloque 5 — Los filtros (líneas 129–135)

Este es el bloque más sutil del archivo:

```python
mask_base = df["anio"].between(*sel_anios)
if sel_generos:
    mask_base &= df["playlist_genre"].isin(sel_generos)

mask = mask_base & (df["is_hit"] == 1) if solo_hits else mask_base
dff = df[mask]
df_comparacion = df[mask_base]
```

Una **máscara** es una columna de `True`/`False` del mismo largo que la tabla.
`df[mask]` devuelve solo las filas donde la máscara es `True`. El `&=` va acumulando
condiciones.

**Por qué existen dos subconjuntos:**

- `dff` respeta *todos* los filtros. Es lo que ve el usuario.
- `df_comparacion` ignora el check de "solo hits".

El gráfico de radar compara *hits contra canciones comunes*. Si le pasáramos `dff` con
"solo hits" marcado, se quedaría sin canciones comunes con qué comparar y quedaría
vacío. Por eso el radar recibe `df_comparacion` y todo el resto recibe `dff`.

### Bloque 6 — KPIs (líneas 141–162)

```python
k1, k2, k3, k4 = st.columns(4)
k1.metric("Canciones analizadas", miles(len(dff)), help="...")
```

`st.columns(4)` divide el ancho en cuatro y devuelve cuatro objetos. Llamar
`k1.metric(...)` dibuja dentro de la primera columna. Tres de los cuatro KPIs se
recalculan con los filtros; el ROC-AUC es fijo porque describe al modelo, no a los
datos filtrados.

Antes de los KPIs hay una guarda importante:

```python
if dff.empty:
    st.warning("Ningún dato cumple con los filtros seleccionados...")
    st.stop()
```

`st.stop()` corta la ejecución ahí mismo. Sin eso, `dff['is_hit'].mean()` sobre una
tabla vacía daría `NaN` y todos los gráficos siguientes reventarían.

### Bloque 7 — Las cuatro pestañas (línea 164 en adelante)

```python
tab1, tab2, tab3, tab4 = st.tabs([...])

with tab1:
    st.plotly_chart(charts.grafico_evolucion_atributos(dff), use_container_width=True)
```

Nota que **todas las pestañas se calculan siempre**, aunque el usuario esté viendo
solo una. Streamlit las dibuja todas y el navegador esconde las que no están activas.
Con este volumen de datos no se nota; en un proyecto con millones de filas habría que
cambiar el enfoque.

### Bloque 8 — El simulador (líneas 236–325)

Es la única parte con lógica de verdad. Cuatro pasos:

**1. Presets.** Un diccionario de canciones prearmadas. `"Personalizado"` vale `None`,
y en ese caso los sliders usan sus valores por defecto:

```python
inicial = float(base[f]) if base else defecto
```

**2. Los sliders en dos columnas.** El truco es `i % 2`:

```python
destino = c1 if i % 2 == 0 else c2
```

Los índices pares van a la columna izquierda, los impares a la derecha.

**3. La predicción.**

```python
entrada = pd.DataFrame([[valores[f] for f in FEATURES]], columns=FEATURES)
probabilidad = float(modelo.predict_proba(entrada)[0][1])
```

Se arma un DataFrame de **una sola fila** recorriendo `FEATURES` — de nuevo, el orden
sale del contrato, no de escribirlo a mano.

`predict_proba` devuelve `[[prob_no_hit, prob_hit]]`. El `[0]` toma la única fila y el
`[1]` toma la probabilidad de hit. Fíjate que **no usamos `modelo.predict()`**: eso
aplicaría el umbral 0,50 por defecto y nosotros queremos comparar contra 0,39.

**4. La sugerencia de ajuste.** Esta es la parte que suele impresionar en la demo:

```python
for f in FEATURES:
    paso_test = (maximo - minimo) * 0.15
    for direccion in (+1, -1):
        prueba = entrada.copy()
        prueba.loc[0, f] = nuevo
        p = float(modelo.predict_proba(prueba)[0][1])
        if mejor is None or p > mejor[2]:
            mejor = (f, nuevo, p, direccion)
```

Es fuerza bruta, y está bien que lo sea: prueba mover **cada** variable un 15% de su
rango **hacia arriba y hacia abajo** (20 predicciones en total, instantáneas) y se
queda con el cambio que más sube la probabilidad. Después solo lo muestra si la mejora
supera medio punto porcentual, para no sugerir ruido.

Si te preguntan en la presentación *"¿cómo calculan la sugerencia?"*, la respuesta es:
**probamos las 20 variantes y mostramos la mejor**. No hay magia.

### Bloque 9 — Ficha técnica (líneas 331–421)

Casi todo texto. Lo único a destacar es que **cada número sale de `METRICAS`**, nunca
escrito a mano:

```python
m1.metric("ROC-AUC", f"{METRICAS['roc_auc']:.3f}", ...)
```

Así, si se reentrena el modelo, la ficha técnica se actualiza sola y nunca queda
mostrando números viejos. Ese es el motivo de que exista `metrics.json`.

---

## 9. Recorrido por `charts.py`

### La regla que sigue todo el archivo

> **Las funciones son puras:** reciben un DataFrame ya filtrado y devuelven una figura
> de Plotly. No leen archivos, no importan Streamlit, no imprimen nada.

Por eso se pueden probar sueltas, reutilizar en un notebook, y por eso no se rompen
cuando alguien cambia la app.

### La paleta (líneas 27–36)

```python
AZUL = "#2a78d6"      # slot 1
NARANJA = "#eb6834"   # slot 2
AGUA = "#1baf7a"      # slot 3
ROJO = "#e34948"      # solo para el polo negativo del mapa de calor
```

No son colores elegidos por gusto: son una paleta **validada para daltonismo**. Se
verificó que cualquier par de estos colores sea distinguible con deuteranopía,
protanopía y tritanopía. Si cambias uno por "un azul más bonito", puedes romper esa
propiedad sin darte cuenta.

**El orden importa**: el primer color siempre va a la primera serie. Nunca se generan
colores nuevos ni se reciclan.

### `NOMBRES` (líneas 39–52)

Un diccionario que traduce `danceability` → `Bailabilidad`. Está en `charts.py` y no
en `app.py` porque los gráficos también lo necesitan, y `app.py` lo importa como
`charts.NOMBRES`. Una sola fuente de verdad para las etiquetas.

### `ANIO_MIN_CONFIABLE = 1990` (línea 57)

La decisión metodológica del proyecto, en una constante. Antes de 1990 el dataset
tiene menos de 400 canciones repartidas en cuatro décadas. Graficar eso sería inventar
tendencias. Está en una constante para que sea fácil de justificar y fácil de cambiar.

### `_layout()` (líneas 60–80)

La función privada (el `_` al inicio indica "uso interno") que aplica el mismo estilo
a todos los gráficos: título alineado a la izquierda, fondo blanco, rejilla tenue,
tooltip blanco. Sin esto, cada gráfico se vería distinto.

### `_vacio()` (líneas 86–100)

Cuando un filtro deja un gráfico sin datos, devuelve una figura con un mensaje
centrado y **sin ejes**. Es lo que evita que se vea un cuadriculado fantasma con
números del -1 al 6 cuando filtras un género de 9 canciones.

### `preparar(df)` (líneas 103–114)

La única función que **transforma datos** en vez de dibujar. Agrega tres columnas:

```python
fechas = pd.to_datetime(df["track_album_release_date"], errors="coerce", format="mixed")
df["anio"] = fechas.dt.year
df["decada"] = (df["anio"] // 10 * 10).astype("Int64")
df["etiqueta_hit"] = df["is_hit"].map({1: "Hit", 0: "Canción común"})
```

`format="mixed"` es necesario porque las fechas vienen en tres formatos distintos en
el mismo CSV: `2024-08-16`, `1998-03` y `2019`. `errors="coerce"` convierte lo que no
se pueda parsear en `NaT` en vez de reventar.

La división entera `// 10 * 10` convierte 1997 en 1990: es el truco estándar para
agrupar por década.

### Las siete funciones de gráficos

| Función | Tipo | Dónde se usa | Detalle a destacar |
|---|---|---|---|
| `grafico_evolucion_atributos(df, minimo_por_anio=15)` | Líneas | Pestaña 1 | Solo grafica años con 15+ canciones. Pone **etiquetas al final de cada línea**, para que la identidad de la serie no dependa solo del color |
| `grafico_evolucion_duracion(df)` | Área | Pestaña 1 | Está separado del anterior **a propósito**: los minutos y la escala 0–1 no comparten eje. Meter dos escalas en un mismo gráfico es la forma más rápida de mentir con datos |
| `grafico_correlacion(df, columnas=None)` | Mapa de calor | Pestaña 2 | Escala **divergente** azul↔rojo con gris al centro: el cero tiene que verse como "nada", no como un color más |
| `grafico_radar(df)` | Radar | Pestaña 2 | Solo usa variables que ya viven entre 0 y 1, para no inventar normalizaciones. Necesita las dos clases presentes |
| `grafico_hits_por_genero(df, top=12)` | Barras | Pestaña 2 | Filtra géneros con menos de 25 canciones: con 9 canciones el porcentaje no significa nada |
| `grafico_importancias(importancias)` | Barras | Pestaña 4 | La única que **no recibe un DataFrame**, sino el diccionario de `metrics.json` |
| `grafico_probabilidad(probabilidad, umbral)` | Medidor | Pestaña 3 | La línea negra vertical marca el umbral. Naranja si supera el umbral, azul si no |

### El patrón que se repite en todas

```python
def grafico_x(df):
    serie = df.groupby(...).agg(...)        # 1. agregar los datos
    if serie.empty:
        return _vacio(...)                  # 2. estado vacío
    fig = go.Figure()
    fig.add_trace(go.Scatter(...))          # 3. dibujar
    fig.update_yaxes(...)                   # 4. ajustar ejes
    return _layout(fig, "Título", "Subtítulo")   # 5. estilo común
```

Si vas a agregar un gráfico nuevo, copia esta estructura.

### Los `hovertemplate`

```python
hovertemplate="Año %{x}<br>%{y:.2f} min promedio<br>%{customdata} canciones<extra></extra>"
```

Controla lo que aparece al pasar el mouse. `%{x}` y `%{y}` son los valores del punto,
`%{customdata}` es un dato extra que se pasa aparte (aquí, cuántas canciones hay en
ese año), y `<extra></extra>` **vacío elimina** el recuadro gris con el nombre de la
serie que Plotly agrega por defecto y que casi nunca aporta.

---

## 10. Recorrido por el modelo

### Cómo se entrenó

Todo está en `notebooks/03_model_retraining.ipynb` (y el mismo proceso, ejecutable de
un tirón, en `notebooks/train_model.py`). Los pasos:

1. **Separar 80/20 estratificado.** `stratify=y` mantiene la proporción de hits en
   ambos grupos: sin eso, el conjunto de prueba podría quedar con 15% de hits por azar
   y las métricas no serían comparables.

2. **Calcular el baseline.** Un `DummyClassifier(strategy="most_frequent")` que
   siempre dice "no es hit". Saca **72,7%** de accuracy. Esa es la vara mínima.

3. **Comparar dos modelos por validación cruzada de 5 pliegues**, usando ROC-AUC.
   Ganó el `RandomForestClassifier` (0,742 contra 0,711 de la regresión logística).

4. **Elegir el umbral.** En vez de aceptar el 0,50 por defecto, se prueban umbrales
   de 0,20 a 0,80 y se elige el que maximiza la exactitud balanceada — calculado con
   validación cruzada **sobre el train**, nunca mirando el test. Resultado: **0,39**.

5. **Evaluar una sola vez sobre el 20% reservado** y guardar todo en `metrics.json`.

### Los números y qué significan

| Métrica | Valor | Cómo leerlo |
|---|---|---|
| ROC-AUC | **0,744** | Si tomas un hit y un no-hit al azar, el modelo le da mayor puntaje al hit el 74% de las veces. 0,50 sería lanzar una moneda |
| Exactitud balanceada | **0,671** | Promedio de aciertos en cada clase por separado. 0,50 sería azar |
| Recall de hits | 80,0% | De los hits reales, detecta 8 de cada 10 |
| Precisión de hits | 39,6% | Cuando dice "hit", acierta 4 de cada 10 |
| Accuracy simple | 61,3% | **Por debajo del baseline de 72,7%** — y es a propósito |

### Por qué la accuracy quedó bajo el baseline

Es la pregunta que más probablemente les hagan. La respuesta:

> El umbral 0,39 hace que el modelo diga "hit" más seguido. Eso sube el recall a 80% y
> baja la accuracy, porque genera falsas alarmas. Es una decisión deliberada: para un
> sello discográfico, **dejar pasar un éxito cuesta mucho más que escuchar una canción
> de más**. Y la accuracy no sirve para medir aprendizaje cuando las clases están
> desbalanceadas — por eso reportamos ROC-AUC y exactitud balanceada, donde sí
> superamos al azar con holgura.

### Qué pesa más en la decisión

```
instrumentalness  19,6%
loudness          14,2%
duration_min      10,6%
acousticness      10,0%
energy             9,9%
```

Esto sale de `modelo.feature_importances_` y se muestra en la pestaña 4.

### Reentrenar el modelo

Si cambian el dataset o quieren probar otras variables:

```bash
python notebooks/train_model.py
```

Tarda menos de un minuto e imprime todas las métricas por pantalla. Reescribe
`model.pkl`, `features.pkl` y `metrics.json`. La app toma los cambios sola en el
siguiente arranque — pero acuérdate de **limpiar el caché** si la tenías corriendo
(menú ⋮ → Clear cache).

---

## 11. Cómo modificar cosas

### Cambiar el color de una serie

Edita las constantes al principio de `charts.py`. Un solo cambio afecta a todos los
gráficos que usan ese color:

```python
AZUL = "#2a78d6"   # ← cambiar aquí
```

⚠️ Ten presente la advertencia de la sección 9: la paleta está validada para
daltonismo. Si cambias un color, cambia idealmente por otro del mismo conjunto.

### Cambiar el mínimo de canciones por año

```python
# En charts.py, la firma de la función:
def grafico_evolucion_atributos(df, minimo_por_anio: int = 15):
```

Súbelo a 30 para una línea más suave, o bájalo a 5 para ver más años (y más ruido).
También puedes pasarlo desde `app.py` sin tocar `charts.py`:

```python
charts.grafico_evolucion_atributos(dff, minimo_por_anio=30)
```

### Cambiar desde qué año se grafica

```python
# charts.py, línea 57
ANIO_MIN_CONFIABLE = 1990
```

### Cambiar el umbral de decisión del modelo

Está en `models/metrics.json`, en la clave `"umbral"`. Puedes editarlo a mano para
experimentar, pero lo correcto es reentrenar. Súbelo a 0,50 y verás que la accuracy
mejora y el recall se desploma: es exactamente el compromiso del que habla la
sección 10.

### Agregar un preset al simulador

En `app.py`, dentro del diccionario `presets`. Tiene que tener las 10 variables:

```python
"Balada pop de los 2000": dict(
    danceability=0.55, energy=0.60, valence=0.45, tempo=88.0,
    loudness=-6.5, speechiness=0.04, acousticness=0.35,
    duration_min=4.0, instrumentalness=0.0, liveness=0.13),
```

### Agregar un gráfico nuevo

**Paso 1** — escribe la función en `charts.py` siguiendo el patrón de la sección 9:

```python
def grafico_duracion_por_genero(df: pd.DataFrame, top: int = 10) -> go.Figure:
    """Barras: duración promedio por género."""
    resumen = (df.groupby("playlist_genre")
                 .agg(n=("is_hit", "size"), dur=("duration_min", "mean"))
                 .reset_index())
    resumen = resumen[resumen["n"] >= 25].sort_values("dur").tail(top)

    if resumen.empty:
        return _vacio("Duración por género", "Sin géneros suficientes.", 380)

    fig = go.Figure(go.Bar(
        x=resumen["dur"], y=resumen["playlist_genre"].str.capitalize(),
        orientation="h", marker=dict(color=AZUL, line=dict(width=0)),
        text=[f"{v:.1f} min" for v in resumen["dur"]], textposition="outside",
        hovertemplate="<b>%{y}</b><br>%{x:.2f} minutos<extra></extra>",
    ))
    fig.update_layout(bargap=0.35)
    return _layout(fig, "¿Qué géneros hacen canciones más largas?",
                   "Duración promedio · solo géneros con 25+ canciones")
```

**Paso 2** — llámalo desde `app.py`, dentro de la pestaña que corresponda:

```python
with tab2:
    st.plotly_chart(charts.grafico_duracion_por_genero(dff), use_container_width=True)
```

Guarda ambos archivos y presiona **Rerun** en el navegador.

### Agregar un filtro nuevo a la barra lateral

```python
# 1. El control, dentro del bloque `with st.sidebar:`
pop_min = st.slider("Popularidad mínima", 0, 100, 0)

# 2. Sumarlo a la máscara, en el bloque de filtros
mask_base &= df["track_popularity"] >= pop_min
```

---

## 12. Probar un gráfico suelto

Como `charts.py` no depende de Streamlit, puedes abrir un gráfico solo en el navegador
sin levantar la app. Es **mucho** más rápido para iterar sobre un diseño.

Crea un archivo `probar.py` en la raíz del proyecto:

```python
import pandas as pd
import charts

df = charts.preparar(pd.read_csv("data/spotify_clean.csv"))

# Cambia esta línea por el gráfico que quieras revisar
fig = charts.grafico_evolucion_atributos(df)
fig.show()
```

Y ejecútalo:

```bash
python probar.py
```

Se abre una pestaña del navegador con el gráfico solo, interactivo.

También puedes probarlo con datos filtrados, para revisar los casos borde:

```python
solo_pop = df[df["playlist_genre"] == "pop"]
charts.grafico_radar(solo_pop).show()

genero_chico = df[df["playlist_genre"] == "disco"]   # solo 9 canciones
charts.grafico_evolucion_atributos(genero_chico).show()   # debe mostrar el estado vacío
```

---

## 13. Errores comunes

| Error en pantalla | Qué significa | Cómo arreglarlo |
|---|---|---|
| `ModuleNotFoundError: No module named 'streamlit'` | El entorno virtual no está activado, o no instalaste las librerías | Activa `.venv` (sección 2.3) y corre `pip install -r requirements.txt` |
| `streamlit : el término no se reconoce` (Windows) | Mismo caso anterior | Activa el entorno. Si persiste, usa `python -m streamlit run app.py` |
| `la ejecución de scripts está deshabilitada` (Windows) | Política de seguridad de PowerShell | `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned` |
| `FileNotFoundError: data/spotify_clean.csv` | Estás ejecutando desde la carpeta equivocada | `cd` a la carpeta que contiene `app.py` y corre `streamlit run app.py` desde ahí |
| `Port 8501 is already in use` | Quedó otra instancia corriendo | Usa otro puerto: `streamlit run app.py --server.port 8502`. O cierra la anterior con Ctrl+C |
| `InconsistentVersionWarning` al cargar el modelo | Tu scikit-learn no es la 1.8.0 con la que se creó el `.pkl` | `pip install scikit-learn==1.8.0`. Si insiste, reentrena: `python notebooks/train_model.py` |
| Los gráficos salen en blanco | Los filtros dejaron el subconjunto vacío | Amplía el rango de años o quita géneros en la barra lateral |
| Cambié el CSV y la app muestra lo viejo | El caché sigue sirviendo la versión anterior | Menú ⋮ → **Clear cache**, después **Rerun** |
| La app se ve oscura y los colores raros | El tema oscuro del navegador o del sistema | El archivo `.streamlit/config.toml` fuerza el tema claro. Verifica que exista y que estés corriendo desde la raíz del proyecto |
| `KeyError: 'duration_min'` | Estás usando un CSV viejo, anterior a la limpieza | Usa `data/spotify_clean.csv`, no los archivos `high_` / `low_` |

---

## 14. Chuleta de comandos

| Qué quiero | Windows (PowerShell) | macOS (Terminal) |
|---|---|---|
| Ver la versión de Python | `python --version` | `python3 --version` |
| Crear el entorno | `python -m venv .venv` | `python3 -m venv .venv` |
| Activar el entorno | `.venv\Scripts\Activate.ps1` | `source .venv/bin/activate` |
| Desactivar el entorno | `deactivate` | `deactivate` |
| Instalar librerías | `pip install -r requirements.txt` | `pip install -r requirements.txt` |
| Ver qué está instalado | `pip list` | `pip list` |
| Correr la app | `streamlit run app.py` | `streamlit run app.py` |
| Correr en otro puerto | `streamlit run app.py --server.port 8502` | igual |
| Detener la app | `Ctrl + C` | `Ctrl + C` |
| Reentrenar el modelo | `python notebooks/train_model.py` | `python notebooks/train_model.py` |
| Ver los archivos de la carpeta | `dir` | `ls` |
| Entrar a una carpeta | `cd nombre` | `cd nombre` |
| Volver una carpeta atrás | `cd ..` | `cd ..` |

**Atajos dentro de la app (con el navegador enfocado):**

- `R` — recargar
- `C` — limpiar caché
- Menú ⋮ → **Settings → Run on save** — recarga automática al guardar un archivo

---

## 15. Checklist final

Si todo esto funciona, la app está bien instalada:

- [ ] `python --version` (o `python3`) responde 3.11 o superior
- [ ] Al activar el entorno aparece `(.venv)` al inicio de la línea
- [ ] `pip list` muestra streamlit, pandas, scikit-learn, plotly y joblib
- [ ] `streamlit run app.py` abre el navegador sin errores rojos
- [ ] Los 4 KPIs de arriba muestran números (4.350 · 25,4% · 52,6 · 0.74)
- [ ] La pestaña 1 muestra dos gráficos de líneas
- [ ] La pestaña 2 muestra el radar, las barras por género y el mapa de calor
- [ ] En la pestaña 3, al presionar **Evaluar potencial**, aparece el medidor con un
      porcentaje y una sugerencia
- [ ] Los tres presets dan estos valores exactos (si no coinciden, el `model.pkl` no
      es el correcto): **Reggaetón tipo Bad Bunny → 57% (HIT)** · **Balada acústica
      triste → 37% (NO HIT)** · **Techno de club → 15% (NO HIT)**
- [ ] La pestaña 4 muestra ROC-AUC 0.744
- [ ] Al escribir "pop" en el filtro de géneros, los KPIs y los gráficos cambian
- [ ] Al marcar "Ver solo hits", el radar de la pestaña 2 **sigue mostrando las dos
      series** (esa es la prueba de que `df_comparacion` funciona)

Si algún punto falla, busca el síntoma en la [sección 13](#13-errores-comunes).

---

*Guía del proyecto Hit Predictor & Trendy Dashboard — Samsung Innovation Campus
Chile 2026, Cohort 2.*
