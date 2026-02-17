# Audio GPT Chatbot - Multimodal AI Assistant

A secure, multimodal chatbot application with voice input/output capabilities and comprehensive anti-prompt injection protection. Built with Python, Tkinter, OpenAI GPT, and Inworld AI TTS.

## 🌟 Features

### Core Functionality
- 🎤 **Voice Input**: Record audio messages using your microphone
- 🗣️ **Speech-to-Text**: Automatic transcription using OpenAI Whisper
- 🤖 **AI Responses**: Intelligent responses powered by OpenAI GPT-5-nano
- 🔊 **Text-to-Speech**: Natural voice synthesis using Inworld AI
- 💬 **Chat Interface**: Standard Tkinter GUI with conversation history
- 📝 **System Logs**: Real-time logging panel for monitoring

### Security Features
- 🛡️ **Prompt Injection Detection**: 20+ attack patterns detected
- 🧹 **Input Sanitization**: Unicode normalization, control character removal
- ⏱️ **Rate Limiting**: Configurable message throttling per session
- 🔐 **System Prompt Hardening**: AI-level protection against manipulation
- 🎯 **Multi-Level Security**: LOW, MEDIUM, HIGH sensitivity settings
- 🔍 **Encoding Bypass Detection**: Base64, hex, Unicode escape detection

## 🏗️ Architecture

```
Multimodal_Chatbot4/
├── main.py                 # Application entry point
├── config/                 # Configuration management
│   ├── settings.py        # Centralized settings
│   └── constants.py       # Application constants
├── gui/                   # User interface
│   └── chat_gui.py        # Tkinter chat interface
├── services/              # Core services
│   ├── audio_service.py   # Audio recording/playback
│   ├── stt_service.py     # Speech-to-text (OpenAI)
│   ├── response_service.py # GPT conversation management
│   └── tts_service.py     # Text-to-speech (Inworld)
├── security/              # Security modules
│   ├── prompt_injection_detector.py
│   ├── input_sanitizer.py
│   └── content_moderator.py
└── utils/                 # Utilities
    ├── logger.py          # Logging configuration
    ├── validators.py      # Input validation
    └── exceptions.py      # Custom exceptions
```

## 🚀 Quick Start

See [SETUP.md](SETUP.md) for detailed installation and configuration instructions.

```bash
# 1. Clone the repository
git clone <repository-url>
cd Multimodal_Chatbot4

# 2. Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env with your API keys

# 5. Run the application
python main.py
```

## 🔑 API Keys Required

- **OpenAI API Key**: For GPT responses and speech-to-text
- **Inworld AI API Key**: For text-to-speech synthesis

Get your keys:
- OpenAI: https://platform.openai.com/api-keys
- Inworld AI: https://studio.inworld.ai/

## 🛡️ Security

This chatbot implements comprehensive anti-prompt injection mechanisms:

- **Pattern Detection**: Identifies malicious instruction patterns
- **Input Sanitization**: Cleans and normalizes all user input
- **Rate Limiting**: Prevents spam and flooding attacks
- **Content Moderation**: Blacklist/whitelist support

See [SECURITY.md](SECURITY.md) for detailed security documentation.

### Security Levels

| Level | Description | Use Case |
|-------|-------------|----------|
| **LOW** | Minimal protection | Trusted environments |
| **MEDIUM** | Balanced security | **Recommended** for general use |
| **HIGH** | Maximum protection | High-security environments |

## 📋 Configuration

Key environment variables (see `.env.example`):

```bash
# API Keys
OPENAI_API_KEY=your_key_here
INWORLD_API_KEY=your_key_here

# Security
SECURITY_LEVEL=MEDIUM
MAX_INPUT_LENGTH=2000
RATE_LIMIT_MESSAGES_PER_MINUTE=10

# Models
OPENAI_GPT_MODEL=gpt-5-nano
OPENAI_STT_MODEL=gpt-4o-mini-transcribe
INWORLD_VOICE_ID=Hana
```

## 🧪 Testing

Run security tests to verify protection mechanisms:

```bash
python test_security.py
```

Expected output:
```
✓ PASS | Prompt Injection Detection
✓ PASS | Input Sanitization
✓ PASS | Content Moderation
✓ PASS | Encoding Bypass Detection
```

## 📖 Documentation

- [SETUP.md](SETUP.md) - Installation and setup guide
- [SECURITY.md](SECURITY.md) - Security features and configuration
- `.env.example` - Environment variable template

## 🎯 Use Cases

- **Voice Assistant**: Hands-free AI interaction
- **Language Learning**: Practice conversations with AI
- **Accessibility**: Voice interface for text-based AI
- **Research**: Study prompt injection and AI security
- **Development**: Template for secure AI applications

## 🔧 Technology Stack

- **Python 3.8+**: Core language
- **Tkinter**: Python's standard GUI framework
- **OpenAI API**: GPT-5-nano for responses, Whisper for STT
- **Inworld AI**: Natural text-to-speech
- **sounddevice**: Audio recording
- **python-dotenv**: Environment management

## 📊 Project Status

✅ **Completed Features**:
- Voice recording and playback
- Speech-to-text transcription
- GPT conversation management
- Text-to-speech synthesis
- Tkinter GUI with logs
- Comprehensive security system
- Rate limiting and moderation
- Full documentation

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Additional language support
- More TTS voice options
- Enhanced security patterns
- Mobile app version
- Docker deployment

## 📝 License

This project is provided as-is for educational and development purposes.

## 🙏 Acknowledgments

- OpenAI for GPT and Whisper APIs
- Inworld AI for TTS capabilities
- Tkinter for the GUI framework

## 📞 Support

For issues or questions:
1. Check [SETUP.md](SETUP.md) for installation help
2. Review [SECURITY.md](SECURITY.md) for security configuration
3. Check logs in `chatbot.log` for debugging

## 🔒 Security Notice

This application includes anti-prompt injection mechanisms, but no security system is perfect. Always:
- Monitor logs for suspicious activity
- Keep API keys secure
- Update security patterns regularly
- Use appropriate security levels for your environment

---

**Built with ❤️ for secure AI interactions**
