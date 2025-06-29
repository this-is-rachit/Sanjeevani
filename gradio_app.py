import os
import base64
import gradio as gr
from input_voice import transcribe_audio_and_detect_language
from output_voice import text_to_speech_with_murf, murf_translate, VOICE_MAP
from groq import Groq

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
LLM_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"

LANG_CHOICES = [
    ("English", "en-US"), ("French", "fr-FR"), ("German", "de-DE"), ("Spanish", "es-ES"),
    ("Italian", "it-IT"), ("Portuguese", "pt-BR"), ("Chinese", "zh-CN"), ("Dutch", "nl-NL"),
    ("Hindi", "hi-IN"), ("Korean", "ko-KR"), ("Tamil", "ta-IN"), ("Polish", "pl-PL"),
    ("Bengali", "bn-IN"), ("Japanese", "ja-JP"), ("Greek", "el-GR"), ("Romanian", "ro-RO"),
    ("Slovak", "sk-SK")
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

def save_response_to_txt(text):
    out_path = "doctor_advice.txt"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(text.strip())
    return out_path

def process(audio_path, image_path, lang_code, txt_file):
    transcript = ""
    input_lang = "en"

    if txt_file:
        with open(txt_file.name, "r", encoding="utf-8") as f:
            transcript = f.read()
    elif audio_path:
        transcript, input_lang = transcribe_audio_and_detect_language(audio_path)

    if not transcript and image_path:
        prompt = (
            "You are a professional doctor. Based on the image, suggest the most likely medical condition and a suitable remedy. "
            "Do not include any preamble or special characters. Do not say 'I see' or 'As an AI'. "
            "Start directly with the diagnosis. Keep the response realistic and human-like in tone. "
            "Use no more than two sentences."
        )
    else:
        prompt = (
            "You are a professional doctor. Based on the symptoms described below, give a concise diagnosis and remedy. "
            "Do not include any preamble or special characters. Start the answer immediately with the condition. "
            "Respond like a human doctor would speak, not an AI. Limit your response to two sentences only.\n\n"
            + transcript
        )

    image_b64 = encode_image_base64(image_path) if image_path else None
    doctor_response = analyze_with_groq(prompt, image_b64)

    # Translate if necessary
    target_lang = lang_code.split("-")[0]
    if target_lang != input_lang:
        doctor_response = murf_translate(doctor_response, lang_code)

    _, voice_id = VOICE_MAP.get(lang_code, VOICE_MAP["en-US"])
    out_wav = f"doctor_response_{lang_code}.wav"
    text_to_speech_with_murf(doctor_response, out_wav, voice_id)

    txt_path = save_response_to_txt(doctor_response)
    return transcript or "🖼️ Image-only analysis", doctor_response, out_wav, txt_path

# UI Setup
LOGO_PATH = "logo.png"
with open(LOGO_PATH, "rb") as f:
    logo_b64 = base64.b64encode(f.read()).decode("utf-8")

css = """body { background: linear-gradient(145deg, #0f172a, #1e293b); color: white; font-family: 'Segoe UI'; }"""

with gr.Blocks(css=css) as demo:
    gr.HTML(f'''
    <div style="display: flex; justify-content: center; align-items: center; margin-top: 10px; margin-bottom: 10px;">
        <img src="data:image/png;base64,{logo_b64}" width="100">
    </div>
''')

    gr.HTML("<h1 style='text-align:center;color:#fcd34d;'>🌍 Sanjeevani - Multilingual AI Doctor</h1>")

    with gr.Row():
        with gr.Column(elem_classes="gr-box"):
            mic = gr.Audio(sources=["microphone"], type="filepath", label="🎙️ Speak your concern")
            img = gr.Image(type="filepath", label="📷 Upload image (optional)")
            txt = gr.File(label="📄 Or Upload Symptom .txt", file_types=[".txt"])
            lang = gr.Dropdown(choices=[label for label, _ in LANG_CHOICES], value="English", label="🌐 Response Language")
            submit = gr.Button("🩺 Diagnose")

        with gr.Column(elem_classes="gr-box"):
            out1 = gr.Textbox(label="📝 Transcription")
            out2 = gr.Textbox(label="💬 Doctor's Response")
            out3 = gr.Audio(type="filepath", label="🔊 Voice Response")
            out4 = gr.File(label="📄 Download TXT Report")

    def wrapped_process(mic, img, lang_label, txt):
        return process(mic, img, lang_code_map[lang_label], txt)

    submit.click(wrapped_process, inputs=[mic, img, lang, txt], outputs=[out1, out2, out3, out4])

    # ✅ JS to auto-play voice response in browser after generation
    gr.HTML("""
    <script>
    function autoplayAudio() {
        const audioEl = document.querySelector('audio');
        if (audioEl) {
            audioEl.play().catch(e => {
                console.warn("Autoplay blocked by browser:", e);
            });
        }
    }
    window.addEventListener("message", function(event) {
        if (event.data?.type === "update" && event.data?.output_index === 2) {
            setTimeout(autoplayAudio, 500);
        }
    });
    </script>
    """)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=10000)
