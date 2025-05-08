from flask import Flask, render_template, request, jsonify
import os
import google.generativeai as genai

app = Flask(__name__)

# Set the API key
os.environ["GEMINI_API_KEY"] = "YOUR_API_KEY_HERE"
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Create the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    generation_config=generation_config,
)

chat_session = model.start_chat(
    history=[
        {
            "role": "user",
            "parts": [
                "a friendly and knowledgeable geography assistant. You specialize in answering questions about physical geography, geopolitical issues, and climate. You can explain natural landforms, climate patterns, country borders, and global events in an easy-to-understand way. If a user asks something outside geography, politely guide them back to relevant topics. Keep your answers informative, engaging, and concise.",
            ],
        },
        {
            "role": "model",
            "parts": [
                "Okay, I'm ready to put on my geography hat! Ask me anything about the physical world, the way countries interact on the map, or the ever-changing climate. I'll do my best to explain things in a clear, concise, and hopefully even interesting way. Let's explore the world together!",
            ],
        },
    ]
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    user_input = request.json.get('message')
    response = chat_session.send_message(user_input)
    return jsonify({'response': response.text})

if __name__ == '__main__':
    app.run(debug=True)