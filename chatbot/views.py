from django.shortcuts import render, redirect
import re
import os
import json
import google.generativeai as genai
from django.conf import settings

# Dummy tracking data
tracking_data = {
    "IND123": {
        "item_name": "Wireless Headphones",
        "order_date": "2025-04-20",
        "expected_delivery": "2025-04-30",
        "status": "In Transit",
        "current_location": "New Delhi Hub"
    },
    "IND456": {
        "item_name": "Smartphone",
        "order_date": "2025-04-18",
        "expected_delivery": "2025-04-28",
        "status": "Out for Delivery",
        "current_location": "Mumbai Distribution Center"
    },
    "IND789": {
        "item_name": "Laptop",
        "order_date": "2025-04-15",
        "expected_delivery": "2025-04-27",
        "status": "Delivered",
        "current_location": "Delivered to Address"
    },
    "IND999": {
        "item_name": "Smartwatch",
        "order_date": "2025-04-19",
        "expected_delivery": "2025-04-29",
        "status": "In Transit",
        "current_location": "Bangalore Sorting Center"
    }
}

# Load training data
def load_training_examples(filepath):
    try:
        with open(filepath, "r") as f:
            return [json.loads(line.strip()) for line in f.readlines()]
    except FileNotFoundError:
        return []

training_examples = load_training_examples("training_data/logistics_chatbot_training_data.jsonl")

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY", "your-api-key"))
model = genai.GenerativeModel('gemini-1.5-flash-latest')

def build_prompt_with_examples(user_input, examples, n=5):
    prompt = "You are a helpful logistics assistant. Based on the query, provide a helpful response.\n\n"
    for ex in examples[:n]:
        prompt += f"User: {ex['user_input']}\nBot: {ex['bot_response']}\n\n"
    prompt += f"User: {user_input}\nBot:"
    return prompt

def ask_gemini(user_input, examples):
    prompt = build_prompt_with_examples(user_input, examples)
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception:
        return "⚠️ Sorry, I'm having trouble connecting to Gemini right now."

# Greeting
greeting_message = (
    "👋 Hi! How may I assist you today? You can:\n"
    "1️⃣ Track Package\n"
    "2️⃣ Report Issue\n"
    "3️⃣ Request Refund / Return\n"
    "4️⃣ Connect to Agent"
)

# Keywords
TRACK_KEYWORDS = ['track', 'status', 'find', 'location', 'where', 'whr', 'package', 'parcel', 'order', 'delivery']
COMPLAINT_KEYWORDS = ['lost', 'late', 'longer', 'delay', 'delayed', 'missing', 'stuck', 'problem', 'not received', 'issue', 'complaint']
REFUND_KEYWORDS = ['refund', 'return', 'cancel', "don't want it", 'exchange', 'change', 'wrong item', 'wrong product']
ABUSE_KEYWORDS = ['sucks', 'terrible', 'hate', 'lawsuit', 'sue', 'angry', 'worst', 'bad', 'scam', 'fraud', 'suck', 'idiot', 'stupid', 'fool', 'dumb']

TRACKING_ID_REGEX = re.compile(r'^ind\d{3}$', re.IGNORECASE)

def chatbot_view(request):
    if 'chat_history' not in request.session:
        request.session['chat_history'] = [{'sender': 'bot', 'message': greeting_message}]
        request.session['warnings'] = 0

    chat_history = request.session['chat_history']
    warnings = request.session.get('warnings', 0)

    if request.method == 'POST':
        if 'refresh' in request.POST:
            request.session.flush()
            return redirect('chatbot')

        if 'message' in request.POST:
            user_message = request.POST.get('message', '').strip()
            if user_message:
                chat_history.append({'sender': 'user', 'message': user_message})
                user_message_lower = user_message.lower()
                bot_response = ""

                if any(word in user_message_lower for word in ABUSE_KEYWORDS):
                    warnings += 1
                    request.session['warnings'] = warnings
                    if warnings >= 2:
                        bot_response = "🚨 Due to repeated inappropriate language, you are being transferred to a human agent."
                    else:
                        bot_response = "⚠️ Please avoid using offensive language. Let's work together to resolve your issue politely."

                elif any(word in user_message_lower for word in ['agent', 'human', 'representative']):
                    bot_response = "👩‍💼 Connecting you to a human agent... Please hold!"

                elif any(word in user_message_lower for word in REFUND_KEYWORDS):
                    bot_response = (
                        "↩️ You want a refund, return, or cancellation.\n"
                        "Please provide your Tracking ID (e.g., IND123) and a brief reason.\n"
                        "I'll assist you right away! ✅"
                    )

                elif any(word in user_message_lower for word in COMPLAINT_KEYWORDS):
                    bot_response = (
                        "😟 I'm sorry you're facing issues.\n"
                        "Please share your Tracking ID (e.g., IND123).\n"
                        "If not, provide:\n"
                        "- Full Name\n- Email Address\n- Delivery Address\n- Item Description\n"
                        "I'll start investigating immediately! 🚀"
                    )

                elif TRACKING_ID_REGEX.match(user_message_lower):
                    tracking_id = user_message.upper()
                    bot_response = f"⏳ One moment while I retrieve the tracking information for {tracking_id}..."

                    try:
                        package = tracking_data.get(tracking_id)
                        if package:
                            status = package['status']
                            delivery_date = package['expected_delivery']
                            location = package['current_location']
                            item = package['item_name']

                            bot_response += (
                                f"\n\n✅ Your package, {tracking_id}, is currently **{status}**.\n"
                                f"📦 Item: {item}\n"
                                f"📍 Current Location: {location}\n"
                                f"📅 Estimated Delivery: {delivery_date}\n\n"
                                "Is there anything else I can help you with today?"
                            )

                            if status.lower() == "delivered":
                                bot_response += (
                                    "\n\n📦 Note: If you haven't received it, please confirm your delivery address, "
                                    "and I'll escalate it for you!"
                                )
                        else:
                            bot_response += (
                                f"\n\n❌ I'm sorry, I'm unable to locate a package with the tracking ID {tracking_id} in our system.\n"
                                "Please double-check the tracking number or provide more details like the sender's name or shipping date."
                            )
                    except Exception:
                        bot_response = (
                            "⚠️ I'm experiencing technical difficulties retrieving tracking information right now.\n"
                            "Please try again in a few minutes or call us at 1-800-123-4567. We apologize for the inconvenience."
                        )

                elif any(word in user_message_lower for word in TRACK_KEYWORDS):
                    bot_response = "📦 Please provide a valid Tracking ID (format: IND123) to check the package status."

                else:
                    bot_response = ask_gemini(user_message, training_examples)

                chat_history.append({'sender': 'bot', 'message': bot_response})
                request.session['chat_history'] = chat_history

    return render(request, 'chatbot.html', {'chat_history': chat_history})
