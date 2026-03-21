# 🤖 JARVIS — Voice Assistant

A Python-based AI voice assistant with a **Siri-style animated orb UI** built using Pygame.
The orb changes color based on the assistant's current state — idle, listening, speaking, or thinking.

---

## 🎬 Demo
> Run the app and click the orb or press **SPACE** to start speaking.

---

## ✨ Features

- 🎤 **Speech Recognition** — Understands your voice using Google Speech API
- 🔊 **Text to Speech** — Responds back in a natural voice
- 🌐 **Open Websites** — YouTube, Instagram, GitHub, Netflix, LinkedIn & more
- 🚀 **Launch Apps** — Notepad, Calculator, VS Code, Chrome, Paint & more
- 🌤️ **Live Weather** — Real-time weather using OpenWeatherMap API
- 🧮 **Calculator** — Supports voice-based math calculations
- 📖 **Wikipedia Search** — Instant summaries on any topic
- 🔊 **Volume Control** — Increase, decrease, mute, unmute
- 💻 **System Info** — CPU, RAM and Disk usage
- 😂 **Tell Jokes** — Because why not

---

## 🎨 Orb Color States

| State | Color |
|---|---|
| Idle | Blue → Purple |
| Listening | Bright Blue |
| Speaking | Pink → Purple |
| Thinking | Amber → Orange |

---

## 🛠️ Tech Stack

- **Python 3.x**
- **Pygame** — UI and animations
- **SpeechRecognition** — Voice input
- **pyttsx3** — Text to speech
- **Wikipedia API** — Search
- **OpenWeatherMap API** — Weather
- **psutil** — System info
- **pycaw** — Volume control (Windows)

---

## ⚙️ Installation

**1. Clone the repository**
```bash
git clone https://github.com/janardhangowda345/jarvis.git
cd jarvis
```

**2. Install dependencies**
```bash
pip install pygame speechrecognition pyttsx3 wikipedia requests pyaudio psutil pycaw comtypes
```

**3. Run**
```bash
python voice_assistant.py
```

---

## 🗣️ Example Commands

| You say | JARVIS does |
|---|---|
| "What's the time?" | Tells current time |
| "Open YouTube" | Opens YouTube in browser |
| "Open Notepad" | Launches Notepad |
| "What is Python?" | Wikipedia summary |
| "Calculate 25 plus 17" | Returns 42 |
| "What's the weather?" | Live weather update |
| "Tell me a joke" | Cracks a joke 😄 |
| "System info" | CPU, RAM, Disk stats |

---

## 📁 Project Structure

```
jarvis/
│
├── voice_assistant.py   # Main application
└── README.md            # Project documentation
```

---

## 👨‍💻 Developer

**Janardhan B E**
- GitHub: [@janardhangowda345](https://github.com/janardhangowda345)
- LinkedIn: [Janardhan B E](https://linkedin.com/in/janardhan-b-e-775937280)

---

## 📜 License
This project is open source and available under the [MIT License](LICENSE).
