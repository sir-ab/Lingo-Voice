# Lingo-Voice Quick Start Guide

## 🚀 Getting Started

### 1. Install Dependencies
```bash
poetry install
```

### 2. Run the Chat Application
```bash
poetry run streamlit run app.py
```

### 3. Use the App
- Click "Load Model" (first time only)
- Select source and target languages
- Type your message and click "Translate"

## 🌐 Supported Languages

**European**: English, Spanish, French, German, Portuguese, Italian, Dutch, Russian, Polish, Swedish, Norwegian

**Asian**: Chinese (Simplified/Traditional), Japanese, Korean, Hindi, Thai, Vietnamese, Turkish, Arabic

**200+ More Languages Supported!**

## ⚙️ System Requirements

- Python 3.10+
- 4GB+ RAM
- 2GB+ Free Storage (for model)
- Optional: GPU for faster inference

## 📊 Model Info

- **Model**: NLLB-200 Distilled (600M parameters)
- **Size**: ~1.5GB
- **Speed**: Fast for CPU inference
- **Accuracy**: High quality translations

## 🎨 Features

✅ Real-time translation
✅ Chat history
✅ 200+ languages
✅ Beautiful UI
✅ No internet required (after model download)

## 🔧 Troubleshooting

**Q: Model download is slow?**
A: NLLB is ~1.5GB. Download time depends on internet speed.

**Q: Getting memory errors?**
A: Your system has low RAM. Try reducing other applications or use a smaller model variant.

**Q: Translations are slow?**
A: CPU inference is slower than GPU. Consider using a GPU or the tiny model variant.

## 📝 File Structure

```
.
├── app.py              # Main Streamlit app
├── pyproject.toml      # Project dependencies
├── QUICKSTART.md       # This file
└── README.md           # Full documentation
```

---

Happy translating! 🌍
