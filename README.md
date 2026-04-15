<div align="center">

# 🤖 FRIDAY - Your Personal AI Assistant

![Friday AI Banner](https://img.shields.io/badge/AI-Assistant-blue?style=for-the-badge&logo=robot)
![Python Version](https://img.shields.io/badge/Python-3.12.6-green?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)

**An intelligent voice-activated AI assistant with face authentication, system control, and conversational AI powered by Microsoft Bing Chat.**

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Commands](#-voice-commands) • [Demo](#-demo)

---

</div>

## 📋 Table of Contents

- [About](#-about)
- [Features](#-features)
- [Demo](#-demo)
- [Tech Stack](#-tech-stack)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [Voice Commands](#-voice-commands)
- [Project Structure](#-project-structure)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)
- [Acknowledgments](#-acknowledgments)

---

## 🌟 About

**FRIDAY** is a sophisticated AI-powered virtual assistant inspired by Iron Man's J.A.R.V.I.S. and F.R.I.D.A.Y. Built with Python, it combines cutting-edge technologies to provide a seamless voice-controlled experience with advanced features like face authentication, system control, and intelligent conversation capabilities.

### Why FRIDAY?

- 🔒 **Secure**: Face authentication ensures only authorized users
- 🎤 **Hands-free**: Voice-activated with hotword detection
- 🧠 **Intelligent**: Powered by Microsoft Bing Chat AI
- 💻 **System Control**: Manage your PC with voice commands
- 🌐 **Web Integration**: Open apps, websites, and perform searches
- 📱 **WhatsApp Integration**: Send messages and make calls

---

## ✨ Features

### 🔐 Authentication & Security
- ✅ **Face Recognition** - Secure login with facial authentication
- ✅ **Real-time Detection** - Live face verification
- ✅ **Privacy First** - All data stored locally

### 🎙️ Voice Control
- ✅ **Hotword Detection** - Activate with "Alexa"
- ✅ **Natural Language Processing** - Understand conversational commands
- ✅ **Text-to-Speech** - Clear voice responses
- ✅ **Speech Recognition** - Powered by Google Speech API

### 💻 System Control
- ✅ Shutdown, Restart, Sleep, Lock PC
- ✅ Volume Control (Mute, Unmute, Set Level)
- ✅ Battery Status Monitoring
- ✅ Screenshot Capture
- ✅ Application Management (Open/Close Apps)

### 📁 File Operations
- ✅ Open, Read, Delete Files
- ✅ Hide/Unhide Files and Folders
- ✅ Create Folders
- ✅ Search Files
- ✅ Empty Recycle Bin

### 🌐 Web & App Integration
- ✅ Open Websites (YouTube, Google, Gmail, etc.)
- ✅ Launch Applications (Chrome, Notepad, Calculator, etc.)
- ✅ YouTube Search & Playback
- ✅ WhatsApp Messaging & Calls

### 🤖 AI Chatbot
- ✅ Conversational AI powered by Bing Chat
- ✅ Context-aware responses
- ✅ General knowledge queries
- ✅ Task assistance

---

## 🎬 Demo

### Interface Preview

┌─────────────────────────────────────────┐
│ FRIDAY AI Assistant │
│ │
│ 🎤 "Friday, open YouTube" │
│ 🤖 "Opening YouTube..." │
│ │
│ 🎤 "Friday, what's the weather?" │
│ 🤖 "The weather in your area is..." │
│ │
└─────────────────────────────────────────┘


### Screenshots
*[Add your screenshots here]*

---

## 🛠️ Tech Stack

### Core Technologies

| Technology | Purpose | Version |
|------------|---------|---------|
| ![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white) | Core Language | 3.12.6 |
| ![Eel](https://img.shields.io/badge/Eel-GUI-orange) | Desktop GUI Framework | Latest |
| ![EdgeGPT](https://img.shields.io/badge/EdgeGPT-AI-blueviolet) | Bing Chat Integration | Latest |

### Libraries, Dependencies and Project Structure

```python
# AI & Speech
EdgeGPT              # Bing Chat API
pyttsx3              # Text-to-Speech
SpeechRecognition    # Speech-to-Text
pvporcupine          # Hotword Detection

# System Control
pyautogui            # GUI Automation
pycaw                # Audio Control
psutil               # System Monitoring
winshell             # Windows Shell Operations

# Web & Communication
pywhatkit            # WhatsApp & YouTube
webbrowser           # Web Navigation

# UI & Media
pygame               # Audio Playback
eel                  # Web-based GUI

# Computer Vision
opencv-python        # Face Recognition
face_recognition     # Face Detection

# Project Structure

Friday/
├── 📁 backend/
│   ├── 📁 auth/
│   │   └── recoganize.py          # Face recognition
│   ├── command.py                  # Voice command handler
│   ├── config.py                   # Configuration
│   ├── feature.py                  # Core features
│   ├── helper.py                   # Helper functions
│   ├── system_control.py           # System operations
│   └── cookie.json                 # Bing Chat cookies
├── 📁 frontend/
│   ├── 📁 assets/
│   │   ├── 📁 audio/
│   │   ├── 📁 css/
│   │   ├── 📁 images/
│   │   └── 📁 js/
│   └── index.html                  # Main UI
├── main.py                         # Entry point
├── run.py                          # Application runner
├── jarvis.db                       # SQLite database
├── .env                            # Environment variables
├── requirements.txt                # Dependencies
└── README.md                       # Documentation
```

---

## 🚀 Installation

Follow these steps to set up FRIDAY on your local machine:

### 1. Clone the Repository
```bash
git clone https://github.com/Someshsw1109/Friday.git
cd Friday
```

### 2. Set Up Virtual Environment (Recommended)
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

> **Note:** For `pyaudio` on Windows, you might need to install it via a wheel file if `pip install` fails. For `face_recognition`, ensure you have `cmake` and `dlib` installed.

---

## ⚙️ Configuration

### 1. Environment Variables
Open your `.env` file in the root directory and fill in your API keys:
- `PORCUPINE_ACCESS_KEY`: Get from [Picovoice Console](https://console.picovoice.ai/)
- `OPENWEATHER_API_KEY`: Get from [OpenWeatherMap](https://openweathermap.org/api)
- `NEWS_API_KEY`: Get from [NewsAPI](https://newsapi.org/)
- `WOLFRAMALPHA_APP_ID`: Get from [WolframAlpha Developer Portal](https://developer.wolframalpha.com/)
- `EMAIL_ADDRESS` & `EMAIL_PASSWORD`: Your Gmail address and an [App Password](https://myaccount.google.com/apppasswords)

### 2. Bing Chat Cookies
To use the AI Chatbot feature, you need to provide Bing cookies:
1. Install the "Cookie-Editor" extension in your browser.
2. Go to [bing.com](https://www.bing.com) and log in.
3. Open the extension and click "Export" -> "JSON".
4. Paste the content into `backend/cookie.json`.

---

## ▶️ Usage

To start FRIDAY, run the following command:

```bash
python run.py
```

- The application will launch a GUI.
- To activate FRIDAY, say the hotword **"Alexa"** (configurable in `backend/config.py`).
- Use the voice commands listed below.

---

## 🗣️ Voice Commands

| Category | Command Examples |
|----------|------------------|
| **System** | "Open Notepad", "Take a screenshot", "Shutdown system" |
| **Web** | "Open YouTube", "Search on Google for Python", "Play Believer on YouTube" |
| **Social** | "Send a WhatsApp message", "Make a WhatsApp call" |
| **AI Chat** | "Who is Elon Musk?", "Tell me a joke", "What is the weather in Mumbai?" |
| **Files** | "Open folder", "Create a new folder", "Delete this file" |

---

## 🛠️ Troubleshooting

- **Microphone not detected**: Ensure your microphone is set as the default recording device in system settings.
- **Hotword detection fails**: Check your `PORCUPINE_ACCESS_KEY` in the `.env` file.
- **Bing Chat errors**: Update the `backend/cookie.json` with fresh cookies from Bing.
- **GUI not loading**: Ensure `eel` is properly installed and you have a web browser (Chrome recommended).

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

## 🙏 Acknowledgments

- [Picovoice](https://picovoice.ai/) for Porcupine Hotword Detection
- [Microsoft](https://www.microsoft.com/) for Bing Chat
- [Eel Framework](https://github.com/python-eel/Eel) for the GUI
- Inspired by the Marvel Cinematic Universe's F.R.I.D.A.Y.
