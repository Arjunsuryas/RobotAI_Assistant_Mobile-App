# chat_app.py
# A Kivy-based chat app that mirrors the React Native chat screen logic.
# Features:
# - Connects to Supabase (conversations, messages, user_preferences)
# - Creates a new conversation on start
# - Sends user messages and stores them in Supabase
# - Generates simple AI responses (same heuristics as your RN version)
# - Shows typing indicator
# - Simple message bubble UI and keyboard-friendly input area

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.core.window import Window

import threading
from datetime import datetime
import random
import time

# Supabase client
try:
    from supabase import create_client
except Exception as e:
    raise RuntimeError(
        "supabase client import failed. Ensure 'supabase' (supabase-py) is installed."
    )

# ---------- CONFIG ----------
SUPABASE_URL = "https://YOUR_PROJECT.supabase.co"
SUPABASE_KEY = "YOUR_SUPABASE_KEY"
# Mock authenticated user id (replace with your auth flow)
USER_ID = "example-user-id"
# ----------------------------

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


# ---------- Helpers / Business Logic ----------
assistant_name = "Nova"
current_conversation_id = None


def generate_ai_response(user_input: str) -> str:
    lower_input = user_input.lower()
    if any(x in lower_input for x in ["hello", "hi"]):
        return f"Hello! I'm {assistant_name}. It's great to hear from you! What can I help you with today?"
    if "how are you" in lower_input:
        return "I'm functioning optimally, thank you for asking! As an AI assistant, I'm always ready to help."
    if "name" in lower_input:
        return f"My name is {assistant_name}! I'm your AI virtual assistant."
    if "help" in lower_input:
        return "I'm here to assist you! Ask me anything you'd like to know."
    if "thank" in lower_input:
        return "You're very welcome! Is there anything else you'd like to know?"
    if "weather" in lower_input:
        return "I don't have real-time weather data access, but check a weather app for exact info."
    if "time" in lower_input:
        now = datetime.now()
        return f"The current time is {now.strftime('%H:%M:%S')}."
    responses = [
        "That's an interesting question! It depends on multiple factors.",
        "Great question! Could you provide a few more details?",
        "I understand. From my perspective there are several angles worth exploring.",
        "That's a thoughtful inquiry — let's break it down.",
        "Interesting point! Here's a starting thought on that..."
    ]
    return random.choice(responses)


# ---------- Kivy UI Components ----------
class MessageBubble(BoxLayout):
    def __init__(self, role: str, content: str, timestamp: str = None, **kwargs):
        super().__init__(orientation="horizontal", size_hint_y=None, padding=(8, 6), **kwargs)
        self.height = dp(56)  # will expand if text wraps
        self.role = role

        # container to align left or right
        align_box = BoxLayout(size_hint_x=1, padding=(4, 0))
        bubble = BoxLayout(orientation="vertical", size_hint_x=None, padding=(10, 6))

        # styling based on role
        if role == "user":
            align_box.halign = "right"
            bubble.width = min(Window.width * 0.7, dp(360))
            bubble.canvas.before.clear()
            bubble.add_widget(Label(text=content, halign="right", valign="middle", size_hint_y=None, text_size=(bubble.width - dp(20), None)))
            ts = timestamp or datetime.now().isoformat()
            bubble.add_widget(Label(text=ts.split("T")[-1][:8], font_size=12, size_hint_y=None, height=dp(14), halign="right"))
            # background color simulated by Label's markup (Kivy has no direct background on BoxLayout without canvas)
            bubble_background = ("[color=ffffff][b]" + content + "[/b][/color]")
        else:
            align_box.halign = "left"
            bubble.width = min(Window.width * 0.75, dp(380))
            bubble.add_widget(Label(text=content, halign="left", valign="middle", size_hint_y=None, text_size=(bubble.width - dp(20), None)))
            ts = timestamp or datetime.now().isoformat()
            bubble.add_widget(Label(text=ts.split("T")[-1][:8], font_size=12, size_hint_y=None, height=dp(14), halign="left"))

        # Visual tweaks (Kivy requires use of canvas to draw rounded/bordered boxes; keep simple here)
        if role == "user":
            bubble.padding = (12, 8)
            bubble.spacing = 4
            align_box.add_widget(Widget())  # spacer left
            align_box.add_widget(bubble)
        else:
            bubble.padding = (12, 8)
            bubble.spacing = 4
            align_box.add_widget(bubble)
            align_box.add_widget(Widget())  # spacer right

        # Let bubble size to content (measure text height)
        # Simple heuristic: increase height based on content length
        lines = max(1, len(content) // 40 + content.count("\n"))
        bubble_height = dp(20 + lines * 18)
        bubble.height = bubble_height
        self.height = bubble_height + dp(12)

        self.add_widget(align_box)


class ChatScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", **kwargs)
        self.padding = dp(0)
        self.spacing = dp(0)

        # Header
        header = BoxLayout(size_hint_y=None, height=dp(64), padding=(12, 8), spacing=8)
        header.canvas.before.clear()
        title_box = BoxLayout(orientation="vertical")
        self.assistant_label = Label(text=f"[b]{assistant_name}[/b]\nAI Assistant", markup=True, halign="left", valign="middle")
        title_box.add_widget(self.assistant_label)
        header.add_widget(title_box)
        new_chat_btn = Button(text="+", size_hint_x=None, width=dp(44))
        new_chat_btn.bind(on_release=lambda *_: threading.Thread(target=self.create_new_conversation, daemon=True).start())
        header.add_widget(new_chat_btn)
        self.add_widget(header)

        # Messages area (ScrollView -> GridLayout)
        self.scroll = ScrollView(do_scroll_x=False)
        self.messages_layout = GridLayout(cols=1, spacing=8, size_hint_y=None, padding=(12, 12))
        self.messages_layout.bind(minimum_height=self.messages_layout.setter('height'))
        self.scroll.add_widget(self.messages_layout)
        self.add_widget(self.scroll)

        # Typing indicator
        self.typing_label = Label(text="", size_hint_y=None, height=dp(24))
        self.add_widget(self.typing_label)

        # Input area
        input_area = BoxLayout(size_hint_y=None, height=dp(72), padding=(12, 8), spacing=8)
        self.input = TextInput(hint_text="Type your message...", multiline=True, size_hint_x=1)
        self.input.bind(on_text_validate=self.on_enter)  # Enter triggers only when single-line, but keep
        send_btn = Button(text="Send", size_hint_x=None, width=dp(80))
        send_btn.bind(on_release=lambda *_: threading.Thread(target=self.on_send_pressed, daemon=True).start())
        input_area.add_widget(self.input)
        input_area.add_widget(send_btn)
        self.add_widget(input_area)

        # load initial stuff in background
        threading.Thread(target=self.initialize, daemon=True).start()

    def add_message_to_ui(self, role: str, content: str, timestamp: str = None):
        def _do(dt):
            bubble = MessageBubble(role=role, content=content, timestamp=timestamp)
            self.messages_layout.add_widget(bubble)
            # scroll to bottom
            Clock.schedule_once(lambda _dt: self.scroll.scroll_to(bubble))
        Clock.schedule_once(_do)

    def set_typing(self, is_typing: bool):
        def _do(dt):
            self.typing_label.text = "Typing..." if is_typing else ""
        Clock.schedule_once(_do)

    # ---------- Backend interactions ----------
    def initialize(self):
        # load preferences and create conversation
        self.load_preferences()
        self.create_new_conversation()

    def load_preferences(self):
        global assistant_name
        try:
            res = supabase.table("user_preferences").select("assistant_name").eq("user_id", USER_ID).execute()
            rows = res.data
            if rows:
                assistant_name = rows[0].get("assistant_name") or assistant_name
            else:
                supabase.table("user_preferences").insert({
                    "user_id": USER_ID,
                    "assistant_name": assistant_name,
                    "theme": "dark"
                }).execute()
            Clock.schedule_once(lambda dt: setattr(self.assistant_label, 'text', f"[b]{assistant_name}[/b]\nAI Assistant"))
        except Exception as e:
            print("load_preferences error:", e)

    def create_new_conversation(self):
        global current_conversation_id
        try:
            res = supabase.table("conversations").insert({
                "user_id": USER_ID,
                "title": "New Conversation"
            }).select("*").execute()
            if res.data:
                current_conversation_id = res.data[0]["id"]
                # clear UI
                Clock.schedule_once(lambda dt: self.messages_layout.clear_widgets())
                # add welcome message
                welcome = f"Hi! I'm {assistant_name}, your AI assistant. How can I help you today?"
                self.add_message_to_ui("assistant", welcome, datetime.utcnow().isoformat())
                # store welcome in messages table
                supabase.table("messages").insert({
                    "conversation_id": current_conversation_id,
                    "role": "assistant",
                    "content": welcome
                }).execute()
        except Exception as e:
            print("create_new_conversation error:", e)

    def on_send_pressed(self):
        text = self.input.text or ""
        if not text.strip():
            return
        self.input.text = ""
        # show user message locally immediately
        ts = datetime.utcnow().isoformat()
        self.add_message_to_ui("user", text.strip(), ts)

        # store user message and update conversation timestamp (do in background)
        try:
            supabase.table("messages").insert({
                "conversation_id": current_conversation_id,
                "role": "user",
                "content": text.strip()
            }).execute()
            supabase.table("conversations").update({"updated_at": datetime.utcnow().isoformat()}).eq("id", current_conversation_id).execute()
        except Exception as e:
            print("error storing user message:", e)

        # show typing indicator
        self.set_typing(True)
        # simulate AI response after short delay
        threading.Thread(target=self._delayed_ai_reply, args=(text,), daemon=True).start()

    def _delayed_ai_reply(self, user_text):
        # simulate processing delay
        time.sleep(1.2)
        ai = generate_ai_response(user_text)
        ts = datetime.utcnow().isoformat()

        # insert assistant message into DB
        try:
            supabase.table("messages").insert({
                "conversation_id": current_conversation_id,
                "role": "assistant",
                "content": ai
            }).execute()
            supabase.table("conversations").update({"updated_at": datetime.utcnow().isoformat()}).eq("id", current_conversation_id).execute()
        except Exception as e:
            print("error storing assistant message:", e)

        # update UI
        self.add_message_to_ui("assistant", ai, ts)
        self.set_typing(False)

    def on_enter(self, instance):
        # treat Enter as send (if you'd like)
        threading.Thread(target=self.on_send_pressed, daemon=True).start()


class ChatApp(App):
    def build(self):
        self.title = "Nova Chat"
        return ChatScreen()


if __name__ == "__main__":
    ChatApp().run()
