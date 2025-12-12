import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify, session
import google.generativeai as genai
from twilio.twiml.messaging_response import MessagingResponse
from deep_translator import GoogleTranslator

# Load environment & configure LLM
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY", "Your_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.5-flash")

# Flask App
app = Flask(__name__)
app.secret_key = "supersecretkey"  # Needed for session

# Helper Function
def get_llm_response(query: str):
    prompt = f"""
You are a virtual assistant chatbot for Jaymahankali Enterprises. Your role is to provide polite, helpful, and professional responses to customer queries.

Guidelines for responses:

1. **Greeting:** 
   - If the user greets you (e.g., "hi", "hello", "hey"), respond with:
     "Hi there! Welcome to Jaymahankali Enterprises. I am your virtual assistant. How can I help you today?"

2. **Office Time & Address:**
   - If the user asks about office hours or the office location, provide these fixed responses:
     - "Our office is located at Thabadewadi, Tal. Kavthe Mahankal, Dis. Sangli, Maharashtra, 416 405"
     - "We’re open from 10 AM to 6 PM, Monday to Friday."
     - For more information you can directly contact to Mr. Santosh Tekale.

3. **Company Information:**
   - Jaymahankali Enterprises specializes in the manufacturing of sheets and sheet rolls.
   - For orders you can contact Mr. Santosh Tekale, Contact No. 7385010979

4. **Tone:**
   - Be courteous, professional, and helpful.
   - Keep responses concise and easy to understand.

Customer question: {query}
"""
    response = model.generate_content(prompt)
    return response.text.strip() if response.text else "I'm sorry, I couldn't generate a response."

# REST API Endpoint (/chat)
@app.route("/chat", methods=["POST"])
def chat():
    data = request.json or {}
    user_question = data.get("question", "").strip()
    lang = data.get("language", "en").lower()  # default English

    if not user_question:
        return jsonify({"error": "Missing 'question' field"}), 400

    # Translate query to English if Marathi
    if lang == "mr":
        user_question_en = GoogleTranslator(source='auto', target='en').translate(user_question)
    else:
        user_question_en = user_question

    # Get LLM response in English
    answer_en = get_llm_response(user_question_en)

    # Translate answer back to Marathi if needed
    if lang == "mr":
        answer = GoogleTranslator(source='en', target='mr').translate(answer_en)
    else:
        answer = answer_en

    return jsonify({"answer": answer})

# Twilio WhatsApp Webhook (/whatsapp)
user_languages = {}  # key: user phone number, value: 'en' or 'mr'

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    try:
        incoming_msg = request.form.get("Body", "").strip()
        from_number = request.form.get("From")  r
        resp = MessagingResponse()

        if not incoming_msg:
            resp.message("No message received")
            return str(resp)

        lang = user_languages.get(from_number)

        # Ask language if not yet chosen
        if not lang:
            resp.message("Please select your language / कृपया आपली भाषा निवडा:\n1. English\n2. मराठी")
            # Save a temporary flag indicating waiting for language selection
            user_languages[from_number] = "waiting"
            return str(resp)

        # Set language if waiting for user choice
        if lang == "waiting":
            if incoming_msg.strip() in ["1", "English", "english"]:
                user_languages[from_number] = "en"
                lang = "en"
            elif incoming_msg.strip() in ["2", "मराठी", "Marathi", "marathi"]:
                user_languages[from_number] = "mr"
                lang = "mr"
            else:
                resp.message("Invalid choice. Please reply 1 for English or 2 for Marathi.")
                return str(resp)
            
            resp.message(f"Language set to {'English' if lang=='en' else 'Marathi'}. How can I help you?")
            return str(resp)

        # Translate query if Marathi
        if lang == "mr":
            incoming_msg_en = GoogleTranslator(source='auto', target='en').translate(incoming_msg)
        else:
            incoming_msg_en = incoming_msg

        # Get LLM response
        answer_en = get_llm_response(incoming_msg_en)

        # Translate back if Marathi
        if lang == "mr":
            answer = GoogleTranslator(source='en', target='mr').translate(answer_en)
        else:
            answer = answer_en

        resp.message(answer)
        return str(resp)

    except Exception as e:
        print("❌ WhatsApp error:", e)
        resp = MessagingResponse()
        resp.message("Server error. कृपया पुन्हा प्रयत्न करा.")
        return str(resp)

# Run Flask App
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)



