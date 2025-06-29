#!/usr/bin/env python3
"""
Test script for the Language Buddy translation functionality
"""

import sys
import os

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from language_buddy import LanguageBuddy
import tkinter as tk

def test_translation():
    """Test the translation functionality"""
    print("Testing Language Buddy Translation...")
    
    # Create a minimal version for testing
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    
    app = LanguageBuddy()
    
    # Test cases
    test_cases = [
        ("Hello", "Spanish"),
        ("Thank you", "French"),
        ("Good morning", "German"),
        ("Yes", "Urdu"),
        ("How are you?", "Spanish"),
        ("I love programming", "French")
    ]
    
    for text, language in test_cases:
        print(f"\n--- Testing: '{text}' -> {language} ---")
        
        # Set target language
        app.target_language.set(language)
        
        # Get translation
        result = app.translate_any_text(text)
        
        print(f"Input: {text}")
        print(f"Target: {language}")
        print(f"Result: {result}")
        print(f"Same as input: {result.lower() == text.lower()}")
        
        if result.lower() != text.lower():
            print("✅ SUCCESS: Translation performed")
        else:
            print("❌ FAILED: Same text returned")
    
    root.destroy()
    print("\nTest completed!")

if __name__ == "__main__":
    test_translation()
