import spacy
import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageTk, ImageSequence
import random
import datetime

# Load spaCy NLP model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    import subprocess, sys
    subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")
except Exception as e:
    print("Failed to load spaCy model:", e)
    nlp = None

# Chatbot data
jokes = [
    "Why did the computer go to the doctor? Because it had a virus! 😂",
    "Why was the math book sad? Because it had too many problems.",
    "Why don’t robots ever panic? Because they have nerves of steel!"
]

quotes = [
    "Believe in yourself and all that you are. 💪",
    "Push yourself, because no one else is going to do it for you.",
    "The future depends on what you do today."
]

greetings = ['hello', 'hi', 'hey']
responses_greetings = ['Hello! 😊', 'Hi there!', 'Hey! How can I help you?']
farewells = ['bye', 'goodbye', 'see you']
responses_farewell = ['Goodbye! 👋', 'See you soon!', 'Take care!']

questions = {
    'your name': "I'm 🤖 Vardhan's ChatBot, your assistant!",
    'how are you': "I'm running smoothly! What about you?",
    'what can you do': "I can chat, help answer questions, and more!"
}

# Global variables for animation
thinking_label = None
thinking_frames = []

# Thinking animation
def show_thinking_animation():
    global thinking_label, thinking_frames
    gif = Image.open("thinking.gif")
    thinking_frames = [ImageTk.PhotoImage(frame.copy().resize((100, 100)))
                       for frame in ImageSequence.Iterator(gif)]

    thinking_window = tk.Toplevel(window)
    thinking_window.title("🤖 Thinking...")
    thinking_window.geometry("180x180")
    thinking_window.configure(bg="#0a0f2c")

    thinking_label = tk.Label(thinking_window, bg="#0a0f2c")
    thinking_label.pack(padx=10, pady=10)

    def animate(index=0):
        thinking_label.config(image=thinking_frames[index])
        thinking_window.after(100, animate, (index + 1) % len(thinking_frames))

    animate()
    return thinking_window

# NLP response logic
def chatbot_response(user_input):
    if nlp is not None:
        doc = nlp(user_input.lower())
        tokens = [token.text for token in doc]
    else:
        tokens = user_input.lower().split()

    if 'your name' in user_input:
        return questions['your name']
    if 'how are you' in user_input:
        return questions['how are you']
    if 'what can you do' in user_input or 'help' in user_input:
        return ("Here are some things I can do:\n"
                "- Tell you the time 🕒\n"
                "- Make you laugh 😂\n"
                "- Motivate you 💡\n"
                "- Answer greetings 👋\n"
                "- Clear the chat 🧹\n"
                "- And more...")

    if 'time' in user_input:
        now = datetime.datetime.now().strftime("%H:%M:%S")
        return f"The current time is {now} 🕒"

    if 'joke' in user_input:
        return random.choice(jokes)

    if 'quote' in user_input or 'motivate' in user_input:
        return random.choice(quotes)

    if 'thank' in user_input:
        return "You're welcome, Vardhan! 😊"

    if 'weather' in user_input:
        return "It's always sunny when you're here ☀️ (Just kidding, I can't access real-time weather yet 😅)"

    if 'clear' in user_input or 'reset' in user_input:
        chat_area.delete("1.0", tk.END)
        return "Chat cleared. Ready to start fresh! ✨"

    if any(token in greetings for token in tokens):
        return random.choice(responses_greetings)

    if any(token in farewells for token in tokens):
        return random.choice(responses_farewell)

    for question in questions:
        if question in user_input.lower():
            return questions[question]

    return "🤔 I'm still learning. Could you try asking differently?"

# Send user message and get reply
def send_message():
    user_input = entry.get().strip()
    if not user_input:
        return

    chat_area.insert(tk.END, f"🧑 You: {user_input}\n", "user")
    entry.delete(0, tk.END)

    thinking = show_thinking_animation()

    def on_respond():
        thinking.destroy()
        response = chatbot_response(user_input)
        chat_area.insert(tk.END, f"🤖 VardhanBot: {response}\n\n", "bot")

    window.after(500, on_respond)  # second delay to simulate thinking

# GUI setup
window = tk.Tk()
window.title("💬 Vardhan's ChatBot")
window.geometry("500x600")
window.config(bg="#0a0f2c")  # Darkest blue

# Header
header = tk.Label(window, text="💬 Vardhan's ChatBot Assistant",
                  font=("Helvetica", 18, "bold"), bg="#0a0f2c", fg="#ff1c1c")
header.pack(pady=10)

# Chat display
chat_area = scrolledtext.ScrolledText(window, wrap=tk.WORD, font=("Consolas", 12),
                                      bg="#141b41", fg="white", insertbackground="white")
chat_area.tag_config("user", foreground="#19d3da")
chat_area.tag_config("bot", foreground="#ff4d4d")
chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# User input
entry = tk.Entry(window, font=("Consolas", 14), bg="#1e2447", fg="white", insertbackground="white")
entry.pack(padx=10, pady=(0, 10), fill=tk.X)
entry.bind("<Return>", lambda event: send_message())

# Send button
send_btn = tk.Button(window, text="Send", command=send_message,
                     font=("Arial", 12, "bold"), bg="#ff1c1c", fg="white",
                     activebackground="#ff3333")
send_btn.pack(pady=(0, 10))

# Run
window.mainloop()
