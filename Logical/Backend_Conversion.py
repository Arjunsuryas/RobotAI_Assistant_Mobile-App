from supabase import create_client, Client
from datetime import datetime
import random

# --- Supabase setup ---
SUPABASE_URL = "https://YOUR_PROJECT.supabase.co"
SUPABASE_KEY = "YOUR_SUPABASE_KEY"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- Simulate authentication context ---
user = {"id": "example-user-id"}

assistant_name = "Nova"
current_conversation_id = None


def load_preferences():
    global assistant_name
    if not user:
        return

    data = supabase.table("user_preferences").select("assistant_name").eq("user_id", user["id"]).execute()

    if data.data:
        assistant_name = data.data[0]["assistant_name"]
    else:
        supabase.table("user_preferences").insert({
            "user_id": user["id"],
            "assistant_name": "Nova",
            "theme": "dark"
        }).execute()


def create_new_conversation():
    global current_conversation_id
    if not user:
        return

    response = supabase.table("conversations").insert({
        "user_id": user["id"],
        "title": "New Conversation"
    }).execute()

    if response.data:
        current_conversation_id = response.data[0]["id"]
        print(f"\n🤖 {assistant_name}: Hi! I'm {assistant_name}, your AI assistant. How can I help you today?\n")


def generate_ai_response(user_input: str) -> str:
    text = user_input.lower()

    if any(word in text for word in ["hello", "hi"]):
        return f"Hello! I'm {assistant_name}. It's great to hear from you! What can I help you with today?"
    if "how are you" in text:
        return "I'm functioning optimally, thank you for asking!"
    if "name" in text:
        return f"My name is {assistant_name}! I'm your AI assistant."
    if "help" in text:
        return "I can answer questions, provide information, or just chat!"
    if "thank" in text:
        return "You're very welcome!"
    if "weather" in text:
        return "I don't have real-time weather data access yet."
    if "time" in text:
        return f"The current time is {datetime.now().strftime('%H:%M:%S')}."

    responses = [
        "That's an interesting question! It depends on several factors.",
        "Good question! Could you give me more details?",
        "Hmm, let me think about that...",
        "Interesting thought! Let's discuss it further.",
        "That's a complex topic — but fascinating!"
    ]
    return random.choice(responses)


def send_message(user_text: str):
    global current_conversation_id
    if not user_text.strip() or not current_conversation_id:
        return

    # Insert user message
    supabase.table("messages").insert({
        "conversation_id": current_conversation_id,
        "role": "user",
        "content": user_text.strip(),
    }).execute()

    # Update conversation timestamp
    supabase.table("conversations").update({
        "updated_at": datetime.utcnow().isoformat()
    }).eq("id", current_conversation_id).execute()

    # Generate AI response
    ai_response = generate_ai_response(user_text)

    # Insert assistant response
    supabase.table("messages").insert({
        "conversation_id": current_conversation_id,
        "role": "assistant",
        "content": ai_response,
    }).execute()

    print(f"\n👤 You: {user_text}")
    print(f"🤖 {assistant_name}: {ai_response}\n")


if __name__ == "__main__":
    load_preferences()
    create_new_conversation()

    while True:
        msg = input("You: ")
        if msg.lower() in ["exit", "quit"]:
            break
        send_message(msg)
