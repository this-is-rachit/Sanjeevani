import os
import base64
import gradio as gr
from input_voice import transcribe_audio_and_detect_language
from output_voice import text_to_speech_with_murf, murf_translate, VOICE_MAP
from groq import Groq
import matplotlib.pyplot as plt

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
LLM_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"

LANG_CHOICES = [
    ("English", "en-US"),
    ("French", "fr-FR"),
    ("German", "de-DE"),
    ("Spanish", "es-ES"),
    ("Italian", "it-IT"),
    ("Portuguese", "pt-BR"),
    ("Chinese", "zh-CN"),
    ("Dutch", "nl-NL"),
    ("Hindi", "hi-IN"),
    ("Korean", "ko-KR"),
    ("Tamil", "ta-IN"),
    ("Polish", "pl-PL"),
    ("Bengali", "bn-IN"),
    ("Japanese", "ja-JP"),
    ("Greek", "el-GR"),
    ("Romanian", "ro-RO"),
    ("Slovak", "sk-SK"),
]

lang_code_map = {label: code for label, code in LANG_CHOICES}

def encode_image_base64(path: str) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def analyze_with_groq(prompt: str, image_b64: str = None) -> str:
    client = Groq(api_key=GROQ_API_KEY)
    content = [{"type": "text", "text": prompt}]
    if image_b64:
        content.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}})
    resp = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": content}]
    )
    return resp.choices[0].message.content.strip()

def generate_flowchart(text):
    steps = [s.strip() for s in text.split('.') if s.strip()]
    fig, ax = plt.subplots(figsize=(6, len(steps)))
    ax.axis("off")
    y = len(steps) * 1.5
    for i, step in enumerate(steps):
        ax.text(0.5, y - i * 1.5, step, ha='center', va='center',
                bbox=dict(boxstyle="round,pad=0.6", facecolor="#1e40af", edgecolor="white", linewidth=2),
                fontsize=12, color='white')
    flowchart_path = "flowchart.png"
    fig.savefig(flowchart_path, bbox_inches="tight", facecolor="#0f172a")
    plt.close()
    return flowchart_path

def process(audio_path, image_path, lang_code, txt_file):
    if txt_file:
        with open(txt_file.name, "r", encoding="utf-8") as f:
            transcript = f.read()
        input_lang = "en"
    else:
        transcript, input_lang = transcribe_audio_and_detect_language(audio_path)

    prompt = f"You are a professional medical assistant. Concisely advise conditions and remedies (≤2 sentences):\n\n{transcript}"
    image_b64 = encode_image_base64(image_path) if image_path else None
    doctor_response = analyze_with_groq(prompt, image_b64)

    if lang_code.split("-")[0] != input_lang:
        doctor_response = murf_translate(doctor_response, lang_code)

    _, voice_id = VOICE_MAP.get(lang_code, VOICE_MAP["en-US"])
    out_wav = f"doctor_response_{lang_code}.wav"
    text_to_speech_with_murf(doctor_response, out_wav, voice_id)

    flowchart_path = generate_flowchart(doctor_response)

    return transcript, doctor_response, out_wav, flowchart_path

# Base64 encode logo
LOGO_PATH = "logo.png"
logo_b64 = encode_image_base64(LOGO_PATH)

css = """
body {
    background: linear-gradient(145deg, #0f172a, #1e293b);
    font-family: 'Segoe UI', sans-serif;
    color: #ffffff;
}
canvas#particles-js {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: -1;
    opacity: 0.15;
}
.gr-button {
    background-color: #6366f1;
    color: white;
    border-radius: 8px;
    padding: 12px;
    font-weight: bold;
    transition: background-color 0.3s ease, transform 0.3s ease;
}
.gr-button:hover {
    background-color: #4f46e5;
    transform: scale(1.05);
}
.gr-box {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.37);
    backdrop-filter: blur(6px);
}
"""

with gr.Blocks(css=css) as demo:
    gr.HTML('<canvas id="particles-js"></canvas>')
    gr.HTML(f'''
    <div style="display: flex; justify-content: center; align-items: center; margin-bottom: 10px;">
        <img src="data:image/png;base64,{logo_b64}" width="110" style="border-radius: 50%; box-shadow: 0 0 10px #4f46e5;">
    </div>
''')
    gr.HTML("<h1 style='text-align:center;color:#fcd34d;'>🌍 Sanjeevani - Multilingual AI Doctor</h1>")

    with gr.Row():
        with gr.Column(elem_classes="gr-box"):
            mic    = gr.Audio(sources=["microphone"], type="filepath", label="🎙️ Speak your concern")
            img    = gr.Image(type="filepath", label="📷 Upload image (optional)")
            txt    = gr.File(label="📄 Or Upload Symptom .txt", file_types=[".txt"])
            lang   = gr.Dropdown(choices=[label for label, _ in LANG_CHOICES], value="English", label="🌐 Response Language")
            submit = gr.Button("🩺 Diagnose")

        with gr.Column(elem_classes="gr-box"):
            out1 = gr.Textbox(label="📝 Transcription")
            out2 = gr.Textbox(label="💬 Doctor's Response")
            out3 = gr.Audio(type="filepath", label="🔊 Voice Response")
            out4 = gr.Image(label="📊 Flowchart")

    def wrapped_process(mic, img, lang_label, txt):
        return process(mic, img, lang_code_map[lang_label], txt)

    submit.click(wrapped_process, inputs=[mic, img, lang, txt], outputs=[out1, out2, out3, out4])

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=10000)

