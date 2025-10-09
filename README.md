# Jaymahankali Enterprises Chatbot

A multilingual (English & Marathi) virtual assistant chatbot for **Jaymahankali Enterprises** built with **Flask**, **Google Gemini API**, and **Deep Translator**. It can answer greetings, office timings, address, and company information politely and professionally.

---

## Features

- **Multilingual Support:** English ↔ Marathi (automatic translation for user queries and responses).  
- **Polite & Professional Responses:** Follows fixed guidelines for greetings, office time & address.  
- **WhatsApp Integration:** Chat with the bot via WhatsApp using Twilio.  
- **REST API Support:** Can also be used via API `/chat`.  

---

## Requirements

- Python 3.9+
- Twilio account (for WhatsApp messaging)
- Ngrok (for exposing local server to the internet)
- Google Gemini API key
- Libraries listed in `requirements.txt`  

Install dependencies:
```bash
pip install -r requirements.txt
```

Setup Instructions
1. Clone the repository
```bash
git clone https://github.com/yourusername/jaymahankali-chatbot.git
cd jaymahankali-chatbot
```
2. Set your Gemini API KEY in code

3. Run Flask backend
```
python app.py
```
By default, the Flask server will run at http://0.0.0.0:5000.

4. Expose your local server with Ngrok

Install and run ngrok:
```
ngrok http 5000
```
Ngrok will give you a public URL, e.g., https://abcd1234.ngrok.io.

5. Configure Twilio WhatsApp

- Sign in to your Twilio Console

- Go to Messaging → Try it Out → WhatsApp Sandbox.

- Set the Webhook URL for incoming messages to your ngrok URL:
```
  https://abcd1234.ngrok.io/whatsapp
```
 - Follow Twilio instructions to join the sandbox via WhatsApp.

6. Chat with the Bot
- 🤖😊 Chatbot is ready!
  
- Send a message to your Twilio WhatsApp sandbox number.

- The bot will ask for your preferred language (English / Marathi) only once.

- Subsequent messages will continue in your selected language.

