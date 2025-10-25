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