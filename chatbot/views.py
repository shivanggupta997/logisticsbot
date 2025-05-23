from django.shortcuts import render, redirect
import re

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

# Bot greeting message
greeting_message = (
    "👋 Hi! How may I assist you today? You can:\n"
    "1️⃣ Track Package\n"
    "2️⃣ Report Issue\n"
    "3️⃣ Request Refund / Return\n"
    "4️⃣ Connect to Agent"
)

# Keywords
TRACK_KEYWORDS = ['track', 'status', 'find', 'location', 'where', 'whr', 'pakage', 'parcel', 'order', 'delivery']
COMPLAINT_KEYWORDS = ['lost', 'late', 'longer', 'delay', 'delayed', 'missing', 'stuck', 'problem', 'not received', 'issue', 'complaint', 'problematic', 'problematic']
REFUND_KEYWORDS = ['refund', 'return', 'cancel', 'don\'t want it', 'exchange', 'change', 'wrong item', 'wrong product']
ABUSE_KEYWORDS = ['sucks', 'terrible', 'hate', 'lawsuit', 'sue', 'angry', 'worst', 'bad', 'scam', 'fraud', 'suck', 'idiot', 'stupid', 'fool', 'dumb']

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

                # Handle abusive messages
                if any(word in user_message_lower for word in ABUSE_KEYWORDS):
                    warnings += 1
                    request.session['warnings'] = warnings
                    if warnings >= 2:
                        bot_response = "🚨 Due to repeated inappropriate language, you are being transferred to a human agent."
                    else:
                        bot_response = "⚠️ Please avoid using offensive language. Let's work together to resolve your issue politely."

                # Handle request for human agent
                elif 'agent' in user_message_lower or 'human' in user_message_lower or 'representative' in user_message_lower:
                    bot_response = "👩‍💼 Connecting you to a human agent... Please hold!"

                # Handle refund/return/cancel
                elif any(word in user_message_lower for word in REFUND_KEYWORDS):
                    bot_response = (
                        "↩️ You want a refund, return, or cancellation.\n"
                        "Please provide your Tracking ID (format: IND123) and a brief reason.\n"
                        "I'll assist you right away! ✅"
                    )

                # Handle complaints
                elif any(word in user_message_lower for word in COMPLAINT_KEYWORDS):
                    bot_response = (
                        "😟 I'm sorry you're facing issues.\n"
                        "Please share your Tracking ID if you have it (e.g., IND123).\n"
                        "If not, provide:\n"
                        "- Full Name\n- Email Address\n- Delivery Address\n- Item Description\n"
                        "I'll start investigating immediately! 🚀"
                    )

                # Handle track requests without ID
                elif any(word in user_message_lower for word in TRACK_KEYWORDS) and not re.match(r'^ind\d{3}$', user_message_lower):
                    bot_response = "📦 Sure! Please provide your Tracking ID (format: IND123) to check the package status."

                # Tracking ID given
                elif re.match(r'^ind\d{3}$', user_message_lower):
                    tracking_id = user_message.upper()
                    package = tracking_data.get(tracking_id)
                    if package:
                        bot_response = (
                            f"🔎 Tracking ID: {tracking_id}\n"
                            f"Item: {package['item_name']}\n"
                            f"Order Date: {package['order_date']}\n"
                            f"Expected Delivery: {package['expected_delivery']}\n"
                            f"Status: {package['status']}\n"
                            f"Current Location: {package['current_location']}\n\n"
                            "Is there anything else I can help you with? 😊"
                        )
                        # Handle special case where status is delivered but user complains
                        if package['status'] == 'Delivered':
                            bot_response += "\n\n📦 Note: If you haven't received it, please confirm your delivery address, and I'll escalate it!"

                    else:
                        bot_response = (
                            "❌ Sorry, that Tracking ID was not found.\n"
                            "Please double-check. Tracking IDs usually look like 'IND123'."
                        )

                # Handle repeated spamming
                recent_user_msgs = [msg['message'].lower() for msg in chat_history if msg['sender'] == 'user'][-5:]
                if recent_user_msgs.count(user_message_lower) >= 3:
                    bot_response = "⚠️ Please avoid spamming the same message. I'm here to help — let's continue politely. 🙏"

                # Handle greetings
                elif user_message_lower in ['hi', 'hello', 'hey', 'hola', 'bonjour']:
                    bot_response = greeting_message

                # Handle language/slang issues
                elif re.search(r'(¿|\bé\b|\bpor\b|\bque\b|\bmerci\b)', user_message_lower):
                    bot_response = "🌍 Currently I can assist in English only. Please rephrase your query in English."

                # Fallback for unclear messages
                if not bot_response:
                    bot_response = (
                        "🤔 I'm here to help with tracking, delivery updates, issues, refunds and returns.\n"
                        "You can say things like:\n"
                        "- 'Track my package'\n"
                        "- 'My delivery is late'\n"
                        "- 'Request refund'\n"
                        "- 'Talk to agent'\n\n"
                        "Please type your query! 🚀"
                    )

                chat_history.append({'sender': 'bot', 'message': bot_response})
                request.session.modified = True

    return render(request, 'chatbot.html', {'chat_history': chat_history})
