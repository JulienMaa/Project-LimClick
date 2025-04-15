# 🖱️ Project LimClick

Bienvenue dans **Project LimClick** – une collection d'autoclickers Python personnalisés, conçus pour automatiser des tâches en fonction de la couleur d’un pixel à l’écran ou d'autres critères.

Que ce soit pour du test, du farming ou tout autre automatisation, LimClick te laisse le contrôle total !

---

## ⚙️ Fonctionnalités

- 🎨 Sélecteur de couleur (color picker)
- 📍 Sélection d’un point d’écran à surveiller
- 🖱️ Sélection d’un point d’écran où cliquer
- ⌨️ Activation/désactivation avec la touche **F7**
- ⏱️ Intervalle personnalisable entre les clics
- 🎯 Clique uniquement si la couleur ne correspond pas
- 🧭 Interface graphique simple (Tkinter)
- 🔄 Exécutable .exe possible pour Windows

---

## 🔧 Prérequis

Installe les bibliothèques nécessaires :

```bash
pip install pyautogui pillow keyboard
```

---

## ▶️ Lancer un autoclicker

Chaque autoclicker est situé dans le dossier `/autoclickers`.

Exemple :

```bash
python autoclickers/autoclicker_couleur.py
```

---

## 🛠 Convertir en .exe

Tu peux transformer un script en application Windows :

```bash
pyinstaller --onefile --noconsole --clean autoclicker_couleur.py
```

> Le fichier `.exe` se trouvera dans le dossier `/dist`.

---

## 📁 Structure du projet

```
📁 Project-LimClick/
├── autoclickers/              # Dossier contenant les différents autoclickers
│   ├── autoclicker_couleur.py
│   ├── autoclicker_key.py
│   └── autoclicker_simple.py
├── README.md
├── LICENSE
└── requirements.txt
```

---

## 📃 Licence

Ce projet est distribué sous la licence **MIT**.  
Tu peux l’utiliser, le modifier et le partager librement.

---

**Project LimClick** – Clique malin, clique LimClick ⚡
