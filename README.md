# 🖱️ Project LimClick

Bienvenue dans **Project LimClick** – une collection d'autoclickers Python personnalisés, conçus pour automatiser des tâches en fonction de la couleur d’un pixel à l’écran.

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

## ▶️ Lancer le script

```bash
python autoclicker.py
```

---

## 🛠 Convertir en .exe

Tu peux transformer le script en application Windows :

```bash
pyinstaller --onefile --noconsole --clean autoclicker.py
```

> Le fichier `.exe` se trouvera dans le dossier `/dist`.

---

## 📁 Structure du projet

```
📁 Project-LimClick/
├── autoclicker.py         # Script principal
├── README.md              # Ce fichier
├── requirements.txt       # Dépendances (facultatif)
└── dist/                  # Exécutables générés
```

---

## 🚨 Problèmes avec l’antivirus ?

Certains antivirus peuvent détecter à tort l’exécutable comme dangereux (faux positif), notamment à cause des modules comme `keyboard`.

✅ Compile sur un environnement propre  
✅ Utilise l'option `--clean` avec PyInstaller  
✅ Vérifie sur [VirusTotal](https://www.virustotal.com)

---

## 📌 À venir

- [ ] Choix de la touche pour activer/désactiver
- [ ] Sauvegarde et chargement des paramètres
- [ ] Interface plus esthétique
- [ ] Amélioration du support multi-écran

---

## 📃 Licence

Ce projet est distribué sous la licence **MIT**.  
Tu peux l’utiliser, le modifier et le partager librement.

---

## 🤝 Contributions

N’hésite pas à ouvrir une *issue*, une *pull request*, ou à proposer des idées !

---

**Project LimClick** – Clique malin, clique LimClick ⚡
```

Tu veux que je te génère aussi un `requirements.txt` ? Et tu veux que je te crée une version en anglais aussi dans le repo (`README.fr.md` et `README.md` par exemple) ?
