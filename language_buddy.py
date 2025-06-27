"""
AI-Powered Language Buddy
A user-friendly language learning and translation app
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import json
import os
from datetime import datetime
import webbrowser
try:
    import pyttsx3
    speech_available = True
except ImportError:
    speech_available = False

try:
    import speech_recognition as sr
    speech_recognition_available = True
except ImportError:
    speech_recognition_available = False

try:
    from googletrans import Translator
    translator_available = True
    google_translator = Translator()
except ImportError:
    translator_available = False
    google_translator = None

# Language data - In a real app, this would connect to translation APIs
LANGUAGES = {
    "English": "en",
    "Spanish": "es", 
    "French": "fr",
    "German": "de",
    "Italian": "it",
    "Portuguese": "pt",
    "Chinese": "zh",
    "Japanese": "ja",
    "Korean": "ko",
    "Arabic": "ar",
    "Russian": "ru",
    "Hindi": "hi",
    "Urdu": "ur"
}

# Comprehensive translations for demo purposes - covers most common phrases
SAMPLE_TRANSLATIONS = {
    # Hello translations
    ("Hello", "es"): "Hola",
    ("Hello", "fr"): "Bonjour",
    ("Hello", "de"): "Hallo",
    ("Hello", "it"): "Ciao",
    ("Hello", "pt"): "Olá",
    ("Hello", "zh"): "你好",
    ("Hello", "ja"): "こんにちは",
    ("Hello", "ko"): "안녕하세요",
    ("Hello", "ar"): "مرحبا",
    ("Hello", "ru"): "Привет",
    ("Hello", "hi"): "नमस्ते",
    ("Hello", "ur"): "ہیلو / السلام علیکم",
    
    # Thank you translations
    ("Thank you", "es"): "Gracias",
    ("Thank you", "fr"): "Merci",
    ("Thank you", "de"): "Danke",
    ("Thank you", "it"): "Grazie",
    ("Thank you", "pt"): "Obrigado",
    ("Thank you", "zh"): "谢谢",
    ("Thank you", "ja"): "ありがとう",
    ("Thank you", "ko"): "감사합니다",
    ("Thank you", "ar"): "شكرا",
    ("Thank you", "ru"): "Спасибо",
    ("Thank you", "hi"): "धन्यवाद",
    ("Thank you", "ur"): "شکریہ",
    
    # Good morning translations
    ("Good morning", "es"): "Buenos días",
    ("Good morning", "fr"): "Bonjour",
    ("Good morning", "de"): "Guten Morgen",
    ("Good morning", "it"): "Buongiorno",
    ("Good morning", "pt"): "Bom dia",
    ("Good morning", "zh"): "早上好",
    ("Good morning", "ja"): "おはよう",
    ("Good morning", "ko"): "좋은 아침",
    ("Good morning", "ar"): "صباح الخير",
    ("Good morning", "ru"): "Доброе утро",
    ("Good morning", "hi"): "सुप्रभात",
    ("Good morning", "ur"): "صبح بخیر",
    
    # How are you translations
    ("How are you?", "es"): "¿Cómo estás?",
    ("How are you?", "fr"): "Comment allez-vous?",
    ("How are you?", "de"): "Wie geht es dir?",
    ("How are you?", "it"): "Come stai?",
    ("How are you?", "pt"): "Como você está?",
    ("How are you?", "zh"): "你好吗？",
    ("How are you?", "ja"): "元気ですか？",
    ("How are you?", "ko"): "어떻게 지내세요?",
    ("How are you?", "ar"): "كيف حالك؟",
    ("How are you?", "ru"): "Как дела?",
    ("How are you?", "hi"): "आप कैसे हैं?",
    ("How are you?", "ur"): "آپ کیسے ہیں؟",
    
    # Please translations
    ("Please", "es"): "Por favor",
    ("Please", "fr"): "S'il vous plaît",
    ("Please", "de"): "Bitte",
    ("Please", "it"): "Per favore",
    ("Please", "pt"): "Por favor",
    ("Please", "zh"): "请",
    ("Please", "ja"): "お願いします",
    ("Please", "ko"): "부탁드립니다",
    ("Please", "ar"): "من فضلك",
    ("Please", "ru"): "Пожалуйста",
    ("Please", "hi"): "कृपया",
    ("Please", "ur"): "برائے کرم",
    
    # Goodbye translations
    ("Goodbye", "es"): "Adiós",
    ("Goodbye", "fr"): "Au revoir",
    ("Goodbye", "de"): "Auf Wiedersehen",
    ("Goodbye", "it"): "Arrivederci",
    ("Goodbye", "pt"): "Tchau",
    ("Goodbye", "zh"): "再见",
    ("Goodbye", "ja"): "さようなら",
    ("Goodbye", "ko"): "안녕히 가세요",
    ("Goodbye", "ar"): "وداعا",
    ("Goodbye", "ru"): "До свидания",
    ("Goodbye", "hi"): "अलविदा",
    ("Goodbye", "ur"): "الوداع",
    
    # Yes/No translations
    ("Yes", "es"): "Sí",
    ("Yes", "fr"): "Oui",
    ("Yes", "de"): "Ja",
    ("Yes", "it"): "Sì",
    ("Yes", "pt"): "Sim",
    ("Yes", "zh"): "是",
    ("Yes", "ja"): "はい",
    ("Yes", "ko"): "네",
    ("Yes", "ar"): "نعم",
    ("Yes", "ru"): "Да",
    ("Yes", "hi"): "हाँ",
    ("Yes", "ur"): "جی ہاں",
    
    ("No", "es"): "No",
    ("No", "fr"): "Non",
    ("No", "de"): "Nein",
    ("No", "it"): "No",
    ("No", "pt"): "Não",
    ("No", "zh"): "不",
    ("No", "ja"): "いいえ",
    ("No", "ko"): "아니요",
    ("No", "ar"): "لا",
    ("No", "ru"): "Нет",
    ("No", "hi"): "नहीं",
    ("No", "ur"): "نہیں",
    
    # I love you translations
    ("I love you", "es"): "Te amo",
    ("I love you", "fr"): "Je t'aime",
    ("I love you", "de"): "Ich liebe dich",
    ("I love you", "it"): "Ti amo",
    ("I love you", "pt"): "Eu te amo",
    ("I love you", "zh"): "我爱你",
    ("I love you", "ja"): "愛してる",
    ("I love you", "ko"): "사랑해요",
    ("I love you", "ar"): "أحبك",
    ("I love you", "ru"): "Я тебя люблю",
    ("I love you", "hi"): "मैं तुमसे प्यार करता हूँ",
    ("I love you", "ur"): "میں تم سے محبت کرتا ہوں",
    
    # Water translations
    ("Water", "es"): "Agua",
    ("Water", "fr"): "Eau",
    ("Water", "de"): "Wasser",
    ("Water", "it"): "Acqua",
    ("Water", "pt"): "Água",
    ("Water", "zh"): "水",
    ("Water", "ja"): "水",
    ("Water", "ko"): "물",
    ("Water", "ar"): "ماء",
    ("Water", "ru"): "Вода",
    ("Water", "hi"): "पानी",
    ("Water", "ur"): "پانی",
    
    # Food translations
    ("Food", "es"): "Comida",
    ("Food", "fr"): "Nourriture",
    ("Food", "de"): "Essen",
    ("Food", "it"): "Cibo",
    ("Food", "pt"): "Comida",
    ("Food", "zh"): "食物",
    ("Food", "ja"): "食べ物",
    ("Food", "ko"): "음식",
    ("Food", "ar"): "طعام",
    ("Food", "ru"): "Еда",
    ("Food", "hi"): "खाना",
    ("Food", "ur"): "کھانا",
    
    # Additional common words
    ("Good", "es"): "Bueno",
    ("Good", "fr"): "Bon",
    ("Good", "de"): "Gut",
    ("Good", "it"): "Buono",
    ("Good", "pt"): "Bom",
    ("Good", "zh"): "好",
    ("Good", "ja"): "良い",
    ("Good", "ko"): "좋은",
    ("Good", "ar"): "جيد",
    ("Good", "ru"): "Хороший",
    ("Good", "hi"): "अच्छा",
    ("Good", "ur"): "اچھا",
    
    ("Bad", "es"): "Malo",
    ("Bad", "fr"): "Mauvais",
    ("Bad", "de"): "Schlecht",
    ("Bad", "it"): "Cattivo",
    ("Bad", "pt"): "Mau",
    ("Bad", "zh"): "坏",
    ("Bad", "ja"): "悪い",
    ("Bad", "ko"): "나쁜",
    ("Bad", "ar"): "سيء",
    ("Bad", "ru"): "Плохой",
    ("Bad", "hi"): "बुरा",
    ("Bad", "ur"): "برا",
    
    ("Beautiful", "es"): "Hermoso",
    ("Beautiful", "fr"): "Beau",
    ("Beautiful", "de"): "Schön",
    ("Beautiful", "it"): "Bello",
    ("Beautiful", "pt"): "Bonito",
    ("Beautiful", "zh"): "美丽",
    ("Beautiful", "ja"): "美しい",
    ("Beautiful", "ko"): "아름다운",
    ("Beautiful", "ar"): "جميل",
    ("Beautiful", "ru"): "Красивый",
    ("Beautiful", "hi"): "सुंदर",
    ("Beautiful", "ur"): "خوبصورت",
    
    ("Friend", "es"): "Amigo",
    ("Friend", "fr"): "Ami",
    ("Friend", "de"): "Freund",
    ("Friend", "it"): "Amico",
    ("Friend", "pt"): "Amigo",
    ("Friend", "zh"): "朋友",
    ("Friend", "ja"): "友達",
    ("Friend", "ko"): "친구",
    ("Friend", "ar"): "صديق",
    ("Friend", "ru"): "Друг",
    ("Friend", "hi"): "दोस्त",
    ("Friend", "ur"): "دوست",
    
    ("Family", "es"): "Familia",
    ("Family", "fr"): "Famille",
    ("Family", "de"): "Familie",
    ("Family", "it"): "Famiglia",
    ("Family", "pt"): "Família",
    ("Family", "zh"): "家庭",
    ("Family", "ja"): "家族",
    ("Family", "ko"): "가족",
    ("Family", "ar"): "عائلة",
    ("Family", "ru"): "Семья",
    ("Family", "hi"): "परिवार",
    ("Family", "ur"): "خاندان",
    
    ("House", "es"): "Casa",
    ("House", "fr"): "Maison",
    ("House", "de"): "Haus",
    ("House", "it"): "Casa",
    ("House", "pt"): "Casa",
    ("House", "zh"): "房子",
    ("House", "ja"): "家",
    ("House", "ko"): "집",
    ("House", "ar"): "بيت",
    ("House", "ru"): "Дом",
    ("House", "hi"): "घर",
    ("House", "ur"): "گھر",
    
    ("Book", "es"): "Libro",
    ("Book", "fr"): "Livre",
    ("Book", "de"): "Buch",
    ("Book", "it"): "Libro",
    ("Book", "pt"): "Livro",
    ("Book", "zh"): "书",
    ("Book", "ja"): "本",
    ("Book", "ko"): "책",
    ("Book", "ar"): "كتاب",
    ("Book", "ru"): "Книга",
    ("Book", "hi"): "किताब",
    ("Book", "ur"): "کتاب",
}

class LanguageBuddy:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🌍 AI Language Buddy - Your Personal Language Helper")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f8ff")
        
        # Initialize text-to-speech
        self.tts_engine = None
        if speech_available:
            try:
                self.tts_engine = pyttsx3.init()
                self.tts_engine.setProperty('rate', 150)
            except:
                pass
        
        # Initialize speech recognition
        self.recognizer = None
        self.microphone = None
        if speech_recognition_available:
            try:
                self.recognizer = sr.Recognizer()
                self.microphone = sr.Microphone()
            except:
                pass
        
        # User progress data
        self.user_data = self.load_user_data()
        
        # Current selected language
        self.target_language = tk.StringVar(value="Spanish")
        
        self.create_main_interface()
        
    def load_user_data(self):
        """Load user progress from file"""
        try:
            if os.path.exists("user_progress.json"):
                with open("user_progress.json", "r") as f:
                    return json.load(f)
        except:
            pass
        return {"daily_words_learned": 0, "total_translations": 0, "learning_streak": 0}
    
    def save_user_data(self):
        """Save user progress to file"""
        try:
            with open("user_progress.json", "w") as f:
                json.dump(self.user_data, f)
        except:
            pass
    
    def create_main_interface(self):
        """Create the main user interface"""
        # Clear the window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Title
        title_frame = tk.Frame(self.root, bg="#f0f8ff")
        title_frame.pack(pady=20)
        
        title_label = tk.Label(
            title_frame,
            text="🌍 Welcome to Language Buddy!",
            font=("Arial", 24, "bold"),
            bg="#f0f8ff",
            fg="#2c3e50"
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            title_frame,
            text="Your friendly companion for learning and translating languages",
            font=("Arial", 12),
            bg="#f0f8ff",
            fg="#7f8c8d"
        )
        subtitle_label.pack(pady=5)
        
        # Language selection
        lang_frame = tk.Frame(self.root, bg="#f0f8ff")
        lang_frame.pack(pady=20)
        
        tk.Label(
            lang_frame,
            text="🎯 Choose your target language:",
            font=("Arial", 14, "bold"),
            bg="#f0f8ff",
            fg="#2c3e50"
        ).pack()
        
        lang_dropdown = ttk.Combobox(
            lang_frame,
            textvariable=self.target_language,
            values=list(LANGUAGES.keys()),
            state="readonly",
            font=("Arial", 12),
            width=20
        )
        lang_dropdown.pack(pady=10)
        
        # Main buttons
        button_frame = tk.Frame(self.root, bg="#f0f8ff")
        button_frame.pack(pady=30)
        
        # Translate Text Button
        translate_text_btn = tk.Button(
            button_frame,
            text="📝 Translate Text\n(Type words to translate)",
            font=("Arial", 14, "bold"),
            bg="#3498db",
            fg="white",
            width=25,
            height=3,
            command=self.open_text_translation,
            cursor="hand2"
        )
        translate_text_btn.pack(pady=10)
        
        # Translate Speech Button
        translate_speech_btn = tk.Button(
            button_frame,
            text="🎤 Translate Speech\n(Speak and get translation)",
            font=("Arial", 14, "bold"),
            bg="#e74c3c",
            fg="white",
            width=25,
            height=3,
            command=self.open_speech_translation,
            cursor="hand2"
        )
        translate_speech_btn.pack(pady=10)
        
        # Learning Mode Button
        learning_btn = tk.Button(
            button_frame,
            text="🎓 Start Learning\n(Interactive lessons & practice)",
            font=("Arial", 14, "bold"),
            bg="#2ecc71",
            fg="white",
            width=25,
            height=3,
            command=self.open_learning_mode,
            cursor="hand2"
        )
        learning_btn.pack(pady=10)
        
        # Progress section
        progress_frame = tk.Frame(self.root, bg="#ecf0f1", relief="raised", bd=2)
        progress_frame.pack(pady=20, padx=50, fill="x")
        
        tk.Label(
            progress_frame,
            text="📊 Your Progress Today",
            font=("Arial", 14, "bold"),
            bg="#ecf0f1",
            fg="#2c3e50"
        ).pack(pady=10)
        
        progress_text = f"Words Learned: {self.user_data['daily_words_learned']} | " \
                       f"Translations: {self.user_data['total_translations']} | " \
                       f"Learning Streak: {self.user_data['learning_streak']} days"
        
        tk.Label(
            progress_frame,
            text=progress_text,
            font=("Arial", 11),
            bg="#ecf0f1",
            fg="#34495e"
        ).pack(pady=(0, 10))
        
        # Help button
        help_btn = tk.Button(
            self.root,
            text="❓ Need Help?",
            font=("Arial", 10),
            bg="#9b59b6",
            fg="white",
            command=self.show_help,
            cursor="hand2"
        )
        help_btn.pack(pady=10)
    
    def open_text_translation(self):
        """Open the text translation interface"""
        # Clear the window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Header
        header_frame = tk.Frame(self.root, bg="#f0f8ff")
        header_frame.pack(fill="x", pady=10)
        
        tk.Button(
            header_frame,
            text="⬅️ Back to Home",
            font=("Arial", 10),
            bg="#95a5a6",
            fg="white",
            command=self.create_main_interface,
            cursor="hand2"
        ).pack(side="left", padx=10)
        
        tk.Label(
            header_frame,
            text="📝 Text Translation",
            font=("Arial", 18, "bold"),
            bg="#f0f8ff",
            fg="#2c3e50"
        ).pack()
        
        # Language selection
        lang_frame = tk.Frame(self.root, bg="#f0f8ff")
        lang_frame.pack(pady=10)
        
        tk.Label(
            lang_frame,
            text=f"Translating to: {self.target_language.get()}",
            font=("Arial", 12, "bold"),
            bg="#f0f8ff",
            fg="#e74c3c"
        ).pack()
        
        # Input section
        input_frame = tk.Frame(self.root, bg="#f0f8ff")
        input_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        tk.Label(
            input_frame,
            text="Type your text here (English):",
            font=("Arial", 12, "bold"),
            bg="#f0f8ff",
            fg="#2c3e50"
        ).pack(anchor="w")
        
        self.text_input = scrolledtext.ScrolledText(
            input_frame,
            height=6,
            font=("Arial", 11),
            wrap=tk.WORD
        )
        self.text_input.pack(fill="both", expand=True, pady=5)
        
        # Translate button
        translate_btn = tk.Button(
            input_frame,
            text="🔄 Translate Now",
            font=("Arial", 12, "bold"),
            bg="#3498db",
            fg="white",
            command=self.translate_text,
            cursor="hand2"
        )
        translate_btn.pack(pady=10)
        
        # Output section
        tk.Label(
            input_frame,
            text="Translation:",
            font=("Arial", 12, "bold"),
            bg="#f0f8ff",
            fg="#2c3e50"
        ).pack(anchor="w", pady=(20, 0))
        
        self.text_output = scrolledtext.ScrolledText(
            input_frame,
            height=6,
            font=("Arial", 11),
            wrap=tk.WORD,
            state="disabled"
        )
        self.text_output.pack(fill="both", expand=True, pady=5)
        
        # Action buttons
        action_frame = tk.Frame(input_frame, bg="#f0f8ff")
        action_frame.pack(pady=10)
        
        speak_btn = tk.Button(
            action_frame,
            text="🔊 Hear Translation",
            font=("Arial", 10),
            bg="#e67e22",
            fg="white",
            command=self.speak_translation,
            cursor="hand2"
        )
        speak_btn.pack(side="left", padx=5)
        
        copy_btn = tk.Button(
            action_frame,
            text="📋 Copy Translation",
            font=("Arial", 10),
            bg="#27ae60",
            fg="white",
            command=self.copy_translation,
            cursor="hand2"
        )
        copy_btn.pack(side="left", padx=5)
    
    def translate_text(self):
        """Translate the input text using Google Translate API"""
        input_text = self.text_input.get("1.0", tk.END).strip()
        if not input_text:
            messagebox.showwarning("No Text", "Please enter some text to translate!")
            return
        
        target_lang = LANGUAGES.get(self.target_language.get(), "es")
        translated_text = ""
        
        # Try Google Translate first
        if translator_available and google_translator:
            try:
                translation = google_translator.translate(input_text, dest=target_lang)
                translated_text = translation.text
            except Exception as e:
                print(f"Google Translate error: {e}")
                translated_text = None
        
        # If Google Translate fails, use fallback dictionary
        if not translated_text:
            # Try exact match first
            translated_text = SAMPLE_TRANSLATIONS.get((input_text, target_lang))
            
            # Try case-insensitive match
            if not translated_text:
                for (english_text, lang_code), trans in SAMPLE_TRANSLATIONS.items():
                    if english_text.lower() == input_text.lower() and lang_code == target_lang:
                        translated_text = trans
                        break
            
            # Try partial match for common phrases
            if not translated_text:
                input_lower = input_text.lower()
                for (english_text, lang_code), trans in SAMPLE_TRANSLATIONS.items():
                    if lang_code == target_lang and english_text.lower() in input_lower:
                        translated_text = trans
                        break
            
            # If still no translation found, provide helpful message
            if not translated_text:
                target_lang_name = self.target_language.get()
                translated_text = f"Translation to {target_lang_name} not available for '{input_text}'. Try common phrases like: Hello, Thank you, Good morning, How are you?, Please, Goodbye, Yes, No, Water, Food, I love you."
        
        # Update output
        self.text_output.config(state="normal")
        self.text_output.delete("1.0", tk.END)
        self.text_output.insert("1.0", translated_text)
        self.text_output.config(state="disabled")
        
        # Update user progress
        self.user_data["total_translations"] += 1
        self.save_user_data()
        
        # Store translation for speech
        self.current_translation = translated_text
    
    def speak_translation(self):
        """Speak the translation using text-to-speech"""
        if not hasattr(self, 'current_translation'):
            messagebox.showwarning("No Translation", "Please translate some text first!")
            return
        
        if not speech_available or not self.tts_engine:
            messagebox.showinfo("Speech Not Available", 
                              "Text-to-speech is not available. Please install pyttsx3:\n\n"
                              "pip install pyttsx3")
            return
        
        try:
            self.tts_engine.say(self.current_translation)
            self.tts_engine.runAndWait()
        except Exception as e:
            messagebox.showerror("Speech Error", f"Could not speak the translation: {str(e)}")
    
    def copy_translation(self):
        """Copy translation to clipboard"""
        if not hasattr(self, 'current_translation'):
            messagebox.showwarning("No Translation", "Please translate some text first!")
            return
        
        self.root.clipboard_clear()
        self.root.clipboard_append(self.current_translation)
        messagebox.showinfo("Copied!", "Translation copied to clipboard!")
    
    def open_speech_translation(self):
        """Open the speech translation interface"""
        if not speech_recognition_available:
            messagebox.showinfo("Speech Recognition Not Available", 
                              "Speech recognition is not available. Please install:\n\n"
                              "pip install speechrecognition\n"
                              "pip install pyaudio\n\n"
                              "For now, you can use the text translation feature.")
            return
        
        # Clear the window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Header
        header_frame = tk.Frame(self.root, bg="#f0f8ff")
        header_frame.pack(fill="x", pady=10)
        
        tk.Button(
            header_frame,
            text="⬅️ Back to Home",
            font=("Arial", 10),
            bg="#95a5a6",
            fg="white",
            command=self.create_main_interface,
            cursor="hand2"
        ).pack(side="left", padx=10)
        
        tk.Label(
            header_frame,
            text="🎤 Speech Translation",
            font=("Arial", 18, "bold"),
            bg="#f0f8ff",
            fg="#2c3e50"
        ).pack()
        
        # Instructions
        instruction_frame = tk.Frame(self.root, bg="#fff3cd", relief="raised", bd=2)
        instruction_frame.pack(pady=20, padx=20, fill="x")
        
        tk.Label(
            instruction_frame,
            text="💡 How to use:",
            font=("Arial", 12, "bold"),
            bg="#fff3cd",
            fg="#856404"
        ).pack(anchor="w", padx=10, pady=5)
        
        tk.Label(
            instruction_frame,
            text="1. Click 'Start Recording' button\n"
                 "2. Speak clearly in English\n"
                 "3. Click 'Stop Recording' when done\n"
                 "4. Your speech will be translated automatically!",
            font=("Arial", 10),
            bg="#fff3cd",
            fg="#856404",
            justify="left"
        ).pack(anchor="w", padx=20, pady=(0, 10))
        
        # Recording section
        record_frame = tk.Frame(self.root, bg="#f0f8ff")
        record_frame.pack(pady=30)
        
        self.record_btn = tk.Button(
            record_frame,
            text="🎤 Start Recording",
            font=("Arial", 14, "bold"),
            bg="#e74c3c",
            fg="white",
            width=20,
            height=2,
            command=self.toggle_recording,
            cursor="hand2"
        )
        self.record_btn.pack(pady=10)
        
        self.recording_status = tk.Label(
            record_frame,
            text="Ready to record",
            font=("Arial", 12),
            bg="#f0f8ff",
            fg="#7f8c8d"
        )
        self.recording_status.pack(pady=5)
        
        # Results section
        results_frame = tk.Frame(self.root, bg="#f0f8ff")
        results_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        tk.Label(
            results_frame,
            text="What you said:",
            font=("Arial", 12, "bold"),
            bg="#f0f8ff",
            fg="#2c3e50"
        ).pack(anchor="w")
        
        self.speech_input = scrolledtext.ScrolledText(
            results_frame,
            height=4,
            font=("Arial", 11),
            state="disabled"
        )
        self.speech_input.pack(fill="x", pady=5)
        
        tk.Label(
            results_frame,
            text="Translation:",
            font=("Arial", 12, "bold"),
            bg="#f0f8ff",
            fg="#2c3e50"
        ).pack(anchor="w", pady=(20, 0))
        
        self.speech_output = scrolledtext.ScrolledText(
            results_frame,
            height=4,
            font=("Arial", 11),
            state="disabled"
        )
        self.speech_output.pack(fill="x", pady=5)
        
        # Action buttons
        action_frame = tk.Frame(results_frame, bg="#f0f8ff")
        action_frame.pack(pady=10)
        
        speak_btn = tk.Button(
            action_frame,
            text="🔊 Hear Translation",
            font=("Arial", 10),
            bg="#e67e22",
            fg="white",
            command=self.speak_translation,
            cursor="hand2"
        )
        speak_btn.pack(side="left", padx=5)
        
        # Recording state
        self.is_recording = False
    
    def toggle_recording(self):
        """Toggle speech recording"""
        if not self.is_recording:
            threading.Thread(target=self.start_recording, daemon=True).start()
        else:
            self.stop_recording()
    
    def start_recording(self):
        """Start recording speech"""
        self.is_recording = True
        self.record_btn.config(text="⏹️ Stop Recording", bg="#f39c12")
        self.recording_status.config(text="🔴 Recording... Speak now!", fg="#e74c3c")
        
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source)
                audio = self.recognizer.listen(source, timeout=10)
            
            # Recognize speech
            text = self.recognizer.recognize_google(audio)
            
            # Update input display
            self.speech_input.config(state="normal")
            self.speech_input.delete("1.0", tk.END)
            self.speech_input.insert("1.0", text)
            self.speech_input.config(state="disabled")
            
            # Translate using the same improved logic as text translation
            target_lang = LANGUAGES.get(self.target_language.get(), "es")
            target_lang_name = self.target_language.get()
            translation = SAMPLE_TRANSLATIONS.get((text, target_lang))
            
            # Try case-insensitive match if exact match fails
            if not translation:
                for (english_text, lang_code), trans in SAMPLE_TRANSLATIONS.items():
                    if english_text.lower() == text.lower() and lang_code == target_lang:
                        translation = trans
                        break
            
            # Try simple word substitutions
            if not translation:
                simple_substitutions = {
                    "hello": {"es": "Hola", "fr": "Bonjour", "de": "Hallo", "ur": "السلام علیکم", "hi": "नमस्ते", "ar": "مرحبا"},
                    "thanks": {"es": "Gracias", "fr": "Merci", "de": "Danke", "ur": "شکریہ", "hi": "धन्यवाद", "ar": "شكرا"},
                    "yes": {"es": "Sí", "fr": "Oui", "de": "Ja", "ur": "جی ہاں", "hi": "हाँ", "ar": "نعم"},
                    "no": {"es": "No", "fr": "Non", "de": "Nein", "ur": "نہیں", "hi": "नहीं", "ar": "لا"}
                }
                
                text_lower = text.lower().strip()
                if text_lower in simple_substitutions and target_lang in simple_substitutions[text_lower]:
                    translation = simple_substitutions[text_lower][target_lang]
            
            # If still no translation found, provide helpful message
            if not translation:
                translation = f"Translation to {target_lang_name} not available for '{text}'. Try saying: Hello, Thank you, Good morning, Yes, or No."
            
            # Update output
            self.speech_output.config(state="normal")
            self.speech_output.delete("1.0", tk.END)
            self.speech_output.insert("1.0", translation)
            self.speech_output.config(state="disabled")
            
            # Store for speech
            self.current_translation = translation
            
            # Update progress
            self.user_data["total_translations"] += 1
            self.save_user_data()
            
        except sr.UnknownValueError:
            self.recording_status.config(text="Could not understand speech. Try again!", fg="#e74c3c")
        except sr.RequestError:
            self.recording_status.config(text="Speech service error. Check internet connection.", fg="#e74c3c")
        except Exception as e:
            self.recording_status.config(text=f"Error: {str(e)}", fg="#e74c3c")
        
        # Reset recording state
        self.is_recording = False
        self.record_btn.config(text="🎤 Start Recording", bg="#e74c3c")
        if self.recording_status.cget("text").startswith("🔴"):
            self.recording_status.config(text="Ready to record", fg="#7f8c8d")
    
    def stop_recording(self):
        """Stop recording (handled automatically)"""
        pass
    
    def open_learning_mode(self):
        """Open the interactive learning mode"""
        # Clear the window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Header
        header_frame = tk.Frame(self.root, bg="#f0f8ff")
        header_frame.pack(fill="x", pady=10)
        
        tk.Button(
            header_frame,
            text="⬅️ Back to Home",
            font=("Arial", 10),
            bg="#95a5a6",
            fg="white",
            command=self.create_main_interface,
            cursor="hand2"
        ).pack(side="left", padx=10)
        
        tk.Label(
            header_frame,
            text="🎓 Interactive Learning Mode",
            font=("Arial", 18, "bold"),
            bg="#f0f8ff",
            fg="#2c3e50"
        ).pack()
        
        # Daily words section
        words_frame = tk.Frame(self.root, bg="#e8f5e8", relief="raised", bd=2)
        words_frame.pack(pady=20, padx=20, fill="x")
        
        tk.Label(
            words_frame,
            text="📚 Daily Word Practice",
            font=("Arial", 14, "bold"),
            bg="#e8f5e8",
            fg="#27ae60"
        ).pack(pady=10)
        
        # Sample daily words - now includes multiple languages
        target_lang = LANGUAGES.get(self.target_language.get(), "es")
        
        if target_lang == "es":  # Spanish
            daily_words = [
                ("Hello", "Hola", "OH-lah"),
                ("Thank you", "Gracias", "GRAH-see-ahs"),
                ("Please", "Por favor", "por fah-VOR"),
                ("Goodbye", "Adiós", "ah-DYOHS")
            ]
        elif target_lang == "fr":  # French
            daily_words = [
                ("Hello", "Bonjour", "bon-ZHOOR"),
                ("Thank you", "Merci", "mer-SEE"),
                ("Please", "S'il vous plaît", "see voo PLAY"),
                ("Goodbye", "Au revoir", "oh ruh-VWAHR")
            ]
        elif target_lang == "de":  # German
            daily_words = [
                ("Hello", "Hallo", "HAH-loh"),
                ("Thank you", "Danke", "DAHN-keh"),
                ("Please", "Bitte", "BIT-teh"),
                ("Goodbye", "Auf Wiedersehen", "owf VEE-der-zayn")
            ]
        elif target_lang == "ur":  # Urdu
            daily_words = [
                ("Hello", "ہیلو / السلام علیکم", "As-salaam alaykum"),
                ("Thank you", "شکریہ", "Shukriya"),
                ("Please", "برائے کرم", "Barae karam"),
                ("Goodbye", "الوداع", "Alvida")
            ]
        elif target_lang == "hi":  # Hindi
            daily_words = [
                ("Hello", "नमस्ते", "na-mas-teh"),
                ("Thank you", "धन्यवाद", "dhan-ya-vaad"),
                ("Please", "कृपया", "kri-pa-ya"),
                ("Goodbye", "अलविदा", "al-vi-da")
            ]
        elif target_lang == "ar":  # Arabic
            daily_words = [
                ("Hello", "مرحبا", "mar-ha-ban"),
                ("Thank you", "شكرا", "shuk-ran"),
                ("Please", "من فضلك", "min fad-lak"),
                ("Goodbye", "وداعا", "wa-da-an")
            ]
        else:  # Default to Spanish
            daily_words = [
                ("Hello", "Hola", "OH-lah"),
                ("Thank you", "Gracias", "GRAH-see-ahs"),
                ("Please", "Por favor", "por fah-VOR"),
                ("Goodbye", "Adiós", "ah-DYOHS")
            ]
        
        for english, target_word, pronunciation in daily_words:
            word_frame = tk.Frame(words_frame, bg="#ffffff", relief="ridge", bd=1)
            word_frame.pack(fill="x", padx=10, pady=5)
            
            tk.Label(
                word_frame,
                text=f"English: {english}",
                font=("Arial", 11, "bold"),
                bg="#ffffff",
                fg="#2c3e50"
            ).pack(anchor="w", padx=10, pady=2)
            
            tk.Label(
                word_frame,
                text=f"{self.target_language.get()}: {target_word}",
                font=("Arial", 11),
                bg="#ffffff",
                fg="#e74c3c"
            ).pack(anchor="w", padx=10)
            
            tk.Label(
                word_frame,
                text=f"Pronunciation: {pronunciation}",
                font=("Arial", 10, "italic"),
                bg="#ffffff",
                fg="#7f8c8d"
            ).pack(anchor="w", padx=10, pady=(0, 5))
            
            # Practice button
            practice_btn = tk.Button(
                word_frame,
                text="🔊 Practice",
                font=("Arial", 9),
                bg="#3498db",
                fg="white",
                command=lambda w=target_word: self.practice_word(w),
                cursor="hand2"
            )
            practice_btn.pack(anchor="e", padx=10, pady=5)
        
        # Quiz section
        quiz_frame = tk.Frame(self.root, bg="#fff3cd", relief="raised", bd=2)
        quiz_frame.pack(pady=20, padx=20, fill="x")
        
        tk.Label(
            quiz_frame,
            text="🧠 Quick Quiz",
            font=("Arial", 14, "bold"),
            bg="#fff3cd",
            fg="#856404"
        ).pack(pady=10)
        
        tk.Label(
            quiz_frame,
            text="What does 'Hola' mean in English?",
            font=("Arial", 12),
            bg="#fff3cd",
            fg="#856404"
        ).pack(pady=5)
        
        # Quiz options
        self.quiz_var = tk.StringVar()
        quiz_options = [("Hello", "Hello"), ("Goodbye", "Goodbye"), ("Thank you", "Thank you")]
        
        for text, value in quiz_options:
            tk.Radiobutton(
                quiz_frame,
                text=text,
                variable=self.quiz_var,
                value=value,
                font=("Arial", 11),
                bg="#fff3cd",
                fg="#856404"
            ).pack(anchor="w", padx=50)
        
        check_btn = tk.Button(
            quiz_frame,
            text="✓ Check Answer",
            font=("Arial", 11, "bold"),
            bg="#f39c12",
            fg="white",
            command=self.check_quiz_answer,
            cursor="hand2"
        )
        check_btn.pack(pady=10)
        
        # Progress section
        progress_frame = tk.Frame(self.root, bg="#ecf0f1", relief="raised", bd=2)
        progress_frame.pack(pady=20, padx=20, fill="x")
        
        tk.Label(
            progress_frame,
            text="📊 Learning Progress",
            font=("Arial", 14, "bold"),
            bg="#ecf0f1",
            fg="#2c3e50"
        ).pack(pady=10)
        
        # Progress bar
        progress_bar = ttk.Progressbar(
            progress_frame,
            length=300,
            mode='determinate'
        )
        progress_bar.pack(pady=5)
        progress_bar['value'] = min(self.user_data['daily_words_learned'] * 25, 100)
        
        tk.Label(
            progress_frame,
            text=f"Daily Goal: {self.user_data['daily_words_learned']}/4 words learned",
            font=("Arial", 11),
            bg="#ecf0f1",
            fg="#34495e"
        ).pack(pady=(5, 10))
    
    def practice_word(self, word):
        """Practice pronunciation of a word"""
        if not speech_available or not self.tts_engine:
            messagebox.showinfo("Speech Not Available", 
                              "Text-to-speech is not available. Please install pyttsx3:\n\n"
                              "pip install pyttsx3")
            return
        
        try:
            self.tts_engine.say(word)
            self.tts_engine.runAndWait()
        except Exception as e:
            messagebox.showerror("Speech Error", f"Could not speak the word: {str(e)}")
    
    def check_quiz_answer(self):
        """Check the quiz answer"""
        if self.quiz_var.get() == "Hello":
            messagebox.showinfo("Correct! 🎉", "Great job! 'Hola' means 'Hello' in English.")
            self.user_data["daily_words_learned"] += 1
            self.save_user_data()
        else:
            messagebox.showinfo("Try Again", "Not quite right. 'Hola' means 'Hello' in English. Keep practicing!")
    
    def show_help(self):
        """Show help information"""
        help_text = """
🌍 Welcome to Language Buddy Help!

📝 TEXT TRANSLATION:
• Type any text in English
• Choose your target language
• Click 'Translate Now'
• Use 'Hear Translation' to listen
• Use 'Copy Translation' to copy text

🎤 SPEECH TRANSLATION:
• Click 'Start Recording'
• Speak clearly in English
• Click 'Stop Recording'
• Get instant translation!

🎓 LEARNING MODE:
• Practice daily words
• Take quick quizzes
• Track your progress
• Learn pronunciation

💡 TIPS:
• Speak clearly for best results
• Use a quiet environment for speech
• Practice daily for best results
• Try different phrases and words!

❓ Need more help?
Visit our website for tutorials and guides.
        """
        
        help_window = tk.Toplevel(self.root)
        help_window.title("Language Buddy Help")
        help_window.geometry("500x600")
        help_window.configure(bg="#f0f8ff")
        
        help_text_widget = scrolledtext.ScrolledText(
            help_window,
            wrap=tk.WORD,
            font=("Arial", 10),
            bg="#ffffff",
            fg="#2c3e50"
        )
        help_text_widget.pack(fill="both", expand=True, padx=20, pady=20)
        help_text_widget.insert("1.0", help_text)
        help_text_widget.config(state="disabled")
        
        close_btn = tk.Button(
            help_window,
            text="Close",
            font=("Arial", 11),
            bg="#3498db",
            fg="white",
            command=help_window.destroy,
            cursor="hand2"
        )
        close_btn.pack(pady=10)
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = LanguageBuddy()
    app.run()
