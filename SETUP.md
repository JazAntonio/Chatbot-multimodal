# Setup Guide - Audio GPT Chatbot

Complete installation and configuration guide for the multimodal AI chatbot.

## 📋 Prerequisites

### System Requirements
- **Python**: 3.8 or higher
- **Operating System**: Linux, macOS, or Windows
- **Audio**: Microphone and speakers/headphones
- **Internet**: Active connection for API calls

### API Keys Required
You'll need API keys from:
1. **OpenAI** - For GPT responses and speech-to-text
   - Sign up: https://platform.openai.com/signup
   - Get API key: https://platform.openai.com/api-keys
   
2. **Inworld AI** - For text-to-speech
   - Sign up: https://studio.inworld.ai/
   - Get API key from your account settings

## 🔧 Installation

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd Multimodal_Chatbot4
```

### Step 2: Create Virtual Environment

**Linux/macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

You should see `(.venv)` in your terminal prompt.

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `openai` - OpenAI API client
- `sounddevice` - Audio recording
- `python-dotenv` - Environment management
- `scipy` and `numpy` - Audio processing
- And other required packages

**Note**: Tkinter comes pre-installed with Python, no additional installation needed.

### Step 4: Configure Environment Variables

1. **Copy the example file:**
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` with your API keys:**
   ```bash
   nano .env  # or use your preferred editor
   ```

3. **Add your API keys:**
   ```bash
   OPENAI_API_KEY=sk-your-openai-key-here
   INWORLD_API_KEY=your-inworld-key-here
   ```

### Step 5: Verify Installation

Run the security tests to ensure everything is working:

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

## 🚀 Running the Application

### Start the Chatbot

```bash
python main.py
```

The Tkinter GUI will open with:
- **Left column**: Chat messages
- **Middle column**: Control buttons
- **Right column**: System logs

### Using the Interface

1. **Record Audio**:
   - Click "🎤 Record" button
   - Speak your message
   - Click "⏹️ Stop" when done

2. **Send Message**:
   - Click "📤 Send" to process your audio
   - Wait for transcription and AI response
   - Response will be spoken automatically

3. **Playback**:
   - Click "▶️ Play" to replay your recording
   - Click "⏸️ Pause" to pause playback

4. **Delete Recording**:
   - Click "🗑️ Delete" to remove current recording

5. **End Session**:
   - Click "🔚 Close Session" to reset conversation

## ⚙️ Configuration

### Basic Configuration

Edit `.env` to customize behavior:

```bash
# ===========================
# SECURITY CONFIGURATION
# ===========================
SECURITY_LEVEL=MEDIUM          # LOW, MEDIUM, or HIGH
MAX_INPUT_LENGTH=2000          # Maximum characters
RATE_LIMIT_MESSAGES_PER_MINUTE=10  # Messages per minute

# ===========================
# MODEL CONFIGURATION
# ===========================
OPENAI_GPT_MODEL=gpt-5-nano
OPENAI_TEMPERATURE=1.0
MAX_TOKENS_PER_MESSAGE=500

# ===========================
# AUDIO CONFIGURATION
# ===========================
AUDIO_SAMPLE_RATE=44100
AUDIO_CHANNELS=1

# ===========================
# TTS CONFIGURATION
# ===========================
INWORLD_VOICE_ID=Hana          # Voice for TTS
INWORLD_MODEL_ID=inworld-tts-1.5-mini
```

### Security Levels Explained

| Level | Sensitivity | False Positives | Recommended For |
|-------|-------------|-----------------|-----------------|
| **LOW** | Minimal | Very few | Trusted users, testing |
| **MEDIUM** | Balanced | Rare | **General use** (recommended) |
| **HIGH** | Maximum | Possible | High-security environments |

### Available Voices

Inworld AI voices you can use (set `INWORLD_VOICE_ID`):
- `Hana` - Female, friendly
- `Marcus` - Male, professional
- `Luna` - Female, calm
- Check Inworld AI docs for more options

## 🔍 Troubleshooting

### Common Issues

#### 1. "OPENAI_API_KEY not found"

**Problem**: API key not set in `.env`

**Solution**:
```bash
# Edit .env and add your key
OPENAI_API_KEY=sk-your-actual-key-here
```

#### 2. "ModuleNotFoundError: No module named 'sounddevice'"

**Problem**: Dependencies not installed

**Solution**:
```bash
# Make sure virtual environment is activated
source .venv/bin/activate  # Linux/macOS
# or
.venv\Scripts\activate  # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

#### 3. Audio recording not working

**Problem**: Microphone permissions or device issues

**Solution**:
- Check microphone permissions in system settings
- Test microphone with another application
- Try different `AUDIO_SAMPLE_RATE` values (44100, 48000, 16000)

#### 4. "Rate limit exceeded"

**Problem**: Too many messages sent too quickly

**Solution**:
- Wait a minute before sending more messages
- Increase `RATE_LIMIT_MESSAGES_PER_MINUTE` in `.env`
- Or disable: `ENABLE_CONTENT_MODERATION=false`

#### 5. "Security threat detected"

**Problem**: Message flagged as potential prompt injection

**Solution**:
- Rephrase your message
- Lower security level: `SECURITY_LEVEL=LOW`
- Check `chatbot.log` for details on what was flagged

#### 6. "Unsupported parameter: 'max_tokens'"

**Problem**: Using wrong parameter for GPT model

**Solution**: This should already be fixed in the code. If you see this:
- Make sure you're using the latest version
- Check that `response_service.py` uses `max_completion_tokens`

#### 7. Tkinter window not appearing

**Problem**: Tkinter not properly installed or display issues

**Solution**:
- **Linux**: Install tkinter package
  ```bash
  sudo apt-get install python3-tk  # Ubuntu/Debian
  sudo dnf install python3-tkinter  # Fedora
  ```
- **macOS/Windows**: Tkinter comes with Python, reinstall Python if needed

### Checking Logs

View detailed logs for debugging:

```bash
# View recent logs
tail -f chatbot.log

# Search for errors
grep ERROR chatbot.log

# Search for security events
grep WARNING chatbot.log
```

## 🧪 Testing

### Run Security Tests

```bash
python test_security.py
```

### Test Individual Components

```python
# Test STT service
from services.stt_service import STTService
stt = STTService()
# Record audio and test transcription

# Test GPT service
from services.response_service import GPTService
gpt = GPTService()
response = gpt.generate_response("Hello!")
print(response)
```

## 📊 Monitoring

### Log Files

The application creates log files:
- `chatbot.log` - Main application log
- Rotates automatically (max 10MB, keeps 3 backups)

### Log Levels

Set in `.env`:
```bash
LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR
```

- **DEBUG**: Detailed information for debugging
- **INFO**: General information (recommended)
- **WARNING**: Warning messages and security alerts
- **ERROR**: Error messages only

## 🔒 Security Best Practices

### 1. Protect Your API Keys

```bash
# Never commit .env to git
# It's already in .gitignore

# Use environment-specific keys
# Development: Use test keys with limits
# Production: Use production keys with monitoring
```

### 2. Monitor Security Logs

```bash
# Check for attack attempts
grep "Prompt injection detected" chatbot.log

# Check rate limiting
grep "Rate limit exceeded" chatbot.log
```

### 3. Update Security Patterns

Edit `security/prompt_injection_detector.py` to add custom patterns:

```python
INJECTION_PATTERNS = {
    # Add your custom patterns
    r'your_custom_pattern': ThreatLevel.HIGH,
}
```

### 4. Use Appropriate Security Level

- **Development**: MEDIUM or LOW
- **Production**: MEDIUM or HIGH
- **Public deployment**: HIGH

## 🔄 Updating

### Update Dependencies

```bash
# Activate virtual environment
source .venv/bin/activate

# Update all packages
pip install --upgrade -r requirements.txt
```

### Update Configuration

When new features are added:
1. Check `.env.example` for new variables
2. Add them to your `.env` file
3. Restart the application

## 📱 Platform-Specific Notes

### Linux

- May need to install PortAudio:
  ```bash
  sudo apt-get install portaudio19-dev  # Ubuntu/Debian
  sudo dnf install portaudio-devel      # Fedora
  ```
- Install Tkinter if not present:
  ```bash
  sudo apt-get install python3-tk
  ```

### macOS

- Grant microphone permissions when prompted
- May need to install PortAudio via Homebrew:
  ```bash
  brew install portaudio
  ```
- Tkinter comes pre-installed with Python

### Windows

- Ensure microphone is set as default recording device
- May need to install Visual C++ redistributables
- Tkinter comes pre-installed with Python

## 🎯 Next Steps

After setup:
1. ✅ Test with simple messages
2. ✅ Review security settings in `SECURITY.md`
3. ✅ Customize voice and model settings
4. ✅ Monitor logs for any issues
5. ✅ Adjust security level as needed

## 📚 Additional Resources

- [README.md](README.md) - Project overview
- [SECURITY.md](SECURITY.md) - Security documentation
- [OpenAI API Docs](https://platform.openai.com/docs)
- [Inworld AI Docs](https://docs.inworld.ai/)
- [Python Tkinter Docs](https://docs.python.org/3/library/tkinter.html)

## 💡 Tips

1. **Start with MEDIUM security** - Best balance for most users
2. **Monitor logs initially** - Understand what's being flagged
3. **Test with various inputs** - Ensure legitimate messages work
4. **Adjust rate limits** - Based on your usage patterns
5. **Keep API keys secure** - Never share or commit them

## 🆘 Getting Help

If you encounter issues:
1. Check this SETUP.md guide
2. Review logs in `chatbot.log`
3. Run `python test_security.py` to verify installation
4. Check [SECURITY.md](SECURITY.md) for security-specific issues

---

**Ready to chat! 🎉**
