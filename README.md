# 🌍 Sanjeevani - Multilingual AI Doctor

**Sanjeevani** is an AI-powered virtual doctor that accepts voice, image, or text input from patients, analyzes symptoms using Groq LLM, and responds in the selected language using Murf AI for translation and text-to-speech. It features a beautiful Gradio-based UI and supports 16+ global languages.

---

## 🔧 Features

* 🎧 Voice-based symptom input with automatic language detection
* 📄 Text file input support for written symptoms
* 📷 Image-based diagnosis using powerful multimodal LLMs
* 🗣️ AI-generated multilingual voice responses using Murf
* 📂 Downloadable medical advice in `.txt` format
* 🌐 Language support for English, Hindi, Spanish, French, Chinese, and more
* 🖥️ Clean Gradio UI with dark 3D-styled theme

---

## 🏠 Tech Stack

| Feature            | Technology Used          |
| ------------------ | ------------------------ |
| Voice Input + STT  | Groq Whisper STT         |
| Multilingual LLM   | Groq LLaMA 4             |
| Translation + TTS  | Murf API                 |
| UI Interface       | Gradio                   |
| Language Detection | langdetect (Python)      |
| Audio Handling     | PyDub, SpeechRecognition |
| Deployment         | Render / Localhost       |

---

## 🗂️ Project Structure

```
sanjeevani/
├── ai_doctor.py          # Image analysis with Groq LLM
├── input_voice.py        # Voice input & transcription
├── output_voice.py       # TTS & translation using Murf
├── gradio_app.py         # Gradio UI and end-to-end integration
├── logo.png              # Project logo for UI
├── requirements.txt      # Python dependencies
└── README.md             # You're here!
```

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/sanjeevani.git
cd sanjeevani
```

### 2. Install Dependencies

Make sure Python 3.8+ is installed.

```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables

Create a `.env` file in the root directory with the following:

```
GROQ_API_KEY=your_groq_api_key_here
MURF_API_KEY=your_murf_api_key_here
```

Or export them manually:

```bash
export GROQ_API_KEY=your_groq_api_key_here
export MURF_API_KEY=your_murf_api_key_here
```

### 4. Run the App

```bash
python gradio_app.py
```

Visit: [http://localhost:10000](http://localhost:10000)

---

## 🌐 Supported Languages

* English (`en-US`, `en-IN`, `en-UK`)
* Hindi (`hi-IN`)
* Spanish (`es-ES`)
* French (`fr-FR`)
* German (`de-DE`)
* Chinese (`zh-CN`)
* Japanese (`ja-JP`)
* Korean (`ko-KR`)
* Tamil (`ta-IN`)
* Bengali (`bn-IN`)
* Polish (`pl-PL`)
* Greek (`el-GR`)
* Romanian (`ro-RO`)
* Dutch (`nl-NL`)
* Italian (`it-IT`)
* Portuguese (`pt-BR`)
* Slovak (`sk-SK`)
* Croatian (`hr-HR`)

---

## 📅 Inputs

* **🎧 Microphone**: Record your symptoms
* **📄 .txt File**: Upload written symptom descriptions
* **📷 Image**: Upload an image of the affected area

---

## 📄 Outputs

* **📝 Transcription**: Text from your voice
* **💬 Doctor's Response**: AI-generated diagnosis
* **🔊 Voice Response**: Audio in your selected language
* **📄 TXT Report**: Downloadable remedy file

---

## 🤝 Contributing

1. Fork the repo
2. Create a feature branch (`git checkout -b feature-name`)
3. Commit your changes (`git commit -m 'add feature'`)
4. Push to your branch (`git push origin feature-name`)
5. Create a Pull Request

---

## 🙏 Acknowledgements

* [Groq](https://groq.com/) – STT and LLM services
* [Murf AI](https://murf.ai/) – TTS and translation APIs
* [Gradio](https://gradio.app/) – UI components
* [SpeechRecognition](https://github.com/Uberi/speech_recognition)
* [PyDub](https://github.com/jiaaro/pydub)

---


