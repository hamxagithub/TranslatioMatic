#!/usr/bin/env python3
"""
Paragraph translation test for Language Buddy
"""

import sys
import os

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from language_buddy import LanguageBuddy
import tkinter as tk

def test_paragraph_translation():
    """Test paragraph translation functionality"""
    print("Testing Language Buddy Paragraph Translation...")
    
    # Create a minimal version for testing
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    
    app = LanguageBuddy()
    
    # Test paragraphs
    test_paragraphs = [
        ("The quick brown fox jumps over the lazy dog. This is a test sentence to check translation quality.", "Spanish"),
        ("Artificial intelligence is transforming the world. Machine learning algorithms can now process vast amounts of data.", "French"),
        ("Learning new languages opens doors to new cultures and opportunities. It's never too late to start learning.", "German"),
        ("Technology has revolutionized communication. People can now connect instantly across the globe.", "Urdu"),
        ("Education is the foundation of progress. Knowledge empowers individuals and societies.", "Hindi")
    ]
    
    for text, language in test_paragraphs:
        print(f"\n{'='*60}")
        print(f"Testing: {language}")
        print(f"{'='*60}")
        
        # Set target language
        app.target_language.set(language)
        
        # Get translation
        result = app.translate_any_text(text)
        
        print(f"Original ({len(text)} chars):")
        print(f"  {text}")
        print(f"\nTranslated to {language} ({len(result)} chars):")
        print(f"  {result}")
        print(f"\nSame as input: {result.lower() == text.lower()}")
        
        if result.lower() != text.lower() and "⚠️" not in result:
            print("✅ SUCCESS: Paragraph translated successfully")
        elif "⚠️" in result:
            print("⚠️  WARNING: Translation service unavailable")
        else:
            print("❌ FAILED: Same text returned")
    
    root.destroy()
    print(f"\n{'='*60}")
    print("Paragraph translation test completed!")
    print(f"{'='*60}")

if __name__ == "__main__":
    test_paragraph_translation()
