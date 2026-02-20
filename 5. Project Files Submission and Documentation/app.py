"""
TransLingua - AI-Powered Multilingual Translation Web Application
Built with Streamlit and Google Gemini Pro

This application provides context-aware, grammatically correct translations
using Google's Gemini 1.5 Flash model with advanced prompt engineering.
"""

import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
import time

# ========================================
# 1. CONFIGURATION & SETUP
# ========================================

def initialize_app():
    """Initialize the application with API configuration and page setup."""
    # Load environment variables from .env file
    load_dotenv()
    
    # Get API key from environment variables
    api_key = os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        st.error("⚠️ Google API Key not found! Please set GOOGLE_API_KEY in your .env file.")
        st.info("Get your API key from: https://makersuite.google.com/app/apikey")
        st.stop()
    
    # Configure Google Generative AI with the API key
    genai.configure(api_key=api_key)
    
    # Configure Streamlit page settings
    st.set_page_config(
        page_title="TransLingua - AI Translation",
        page_icon="🌐",
        layout="wide",
        initial_sidebar_state="expanded"
    )

# ========================================
# 2. SUPPORTED LANGUAGES
# ========================================

def get_supported_languages():
    """Return dictionary of supported languages with their codes."""
    return {
        "English": "en",
        "Spanish": "es",
        "French": "fr",
        "German": "de",
        "Italian": "it",
        "Portuguese": "pt",
        "Russian": "ru",
        "Japanese": "ja",
        "Korean": "ko",
        "Chinese (Simplified)": "zh-CN",
        "Chinese (Traditional)": "zh-TW",
        "Arabic": "ar",
        "Hindi": "hi",
        "Bengali": "bn",
        "Turkish": "tr",
        "Dutch": "nl",
        "Polish": "pl",
        "Swedish": "sv",
        "Norwegian": "no",
        "Danish": "da",
        "Finnish": "fi",
        "Greek": "el",
        "Hebrew": "he",
        "Thai": "th",
        "Vietnamese": "vi",
        "Indonesian": "id",
        "Malay": "ms",
        "Filipino": "fil",
        "Czech": "cs",
        "Slovak": "sk",
        "Hungarian": "hu",
        "Romanian": "ro",
        "Ukrainian": "uk",
        "Swahili": "sw",
        "Tamil": "ta",
        "Telugu": "te",
        "Marathi": "mr",
        "Gujarati": "gu",
        "Kannada": "kn",
        "Malayalam": "ml",
        "Punjabi": "pa",
        "Urdu": "ur"
    }

# ========================================
# 3. PROMPT ENGINEERING
# ========================================

def create_translation_prompt(text, source_lang, target_lang):
    """
    Create an optimized prompt for context-aware translation.
    
    This prompt engineering ensures:
    - Natural, fluent translations
    - Context preservation
    - Grammatical correctness
    - Proper handling of idioms and cultural nuances
    """
    prompt = f"""You are a professional translator with expertise in {source_lang} and {target_lang}.

Your task is to translate the following text from {source_lang} to {target_lang}.

TRANSLATION GUIDELINES:
1. Maintain the original meaning and context
2. Use natural, fluent language in the target language
3. Preserve the tone and style of the original text
4. Handle idioms and cultural expressions appropriately
5. Ensure grammatical correctness
6. Maintain any formatting (line breaks, spacing)
7. Do NOT add explanations or notes, provide ONLY the translation

SOURCE TEXT ({source_lang}):
{text}

TRANSLATION ({target_lang}):"""
    
    return prompt

# ========================================
# 4. TRANSLATION LOGIC
# ========================================

def translate_text(text, source_lang, target_lang):
    """
    Translate text using Google Gemini with robust error handling, 
    retries, and model fallback.
    """
    # List of models to try in order (Prioritizing stable free-tier models)
    models_to_try = [
        'gemini-flash-latest',    # Best for speed and free tier stability
        'gemini-pro-latest',      # Good fallback
        'gemini-2.0-flash',       # Newer, but can be limited
        'gemini-2.5-flash'        # Bleeding edge
    ]
    
    prompt = create_translation_prompt(text, source_lang, target_lang)
    last_error = None
    
    for model_name in models_to_try:
        try:
            # Initialize the model
            model = genai.GenerativeModel(model_name)
            
            # Attempt translation with retries for transient errors
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    response = model.generate_content(
                        prompt,
                        generation_config={
                            'temperature': 0.3,
                            'top_p': 0.9,
                            'top_k': 40,
                            'max_output_tokens': 2048,
                        }
                    )
                    
                    if response and response.text:
                        return True, response.text.strip(), None
                        
                except Exception as e:
                    # Check for rate limits (429)
                    if "429" in str(e):
                        if attempt < max_retries - 1:
                            # Wait and retry (exponential backoff)
                            wait_time = 2 * (attempt + 1)
                            time.sleep(wait_time)
                            continue
                    
                    # If it's not a rate limit or retries exhausted, raise to try next model
                    raise e
                    
        except Exception as e:
            last_error = e
            # Continue to next model in the list
            continue
            
    # If all models fail
    error_message = f"Translation failed. All models busy or unavailable. Last error: {str(last_error)}"
    if "429" in str(last_error):
        error_message = "⚠️ System busy (Rate Limit). Please wait 30 seconds and try again."
        
    return False, "", error_message

# ========================================
# 5. INPUT VALIDATION
# ========================================

def validate_input(text, source_lang, target_lang):
    """
    Validate user input before translation.
    
    Returns:
        tuple: (is_valid: bool, error_message: str or None)
    """
    # Check if text is empty or only whitespace
    if not text or text.strip() == "":
        return False, "⚠️ Please enter some text to translate."
    
    # Check if source language is selected
    if source_lang == "Select Language":
        return False, "⚠️ Please select a source language."
    
    # Check if target language is selected
    if target_lang == "Select Language":
        return False, "⚠️ Please select a target language."
    
    # Check if source and target languages are the same
    if source_lang == target_lang:
        return False, "⚠️ Source and target languages cannot be the same."
    
    # Check text length (Gemini has input limits)
    if len(text) > 30000:
        return False, "⚠️ Text is too long. Please limit to 30,000 characters."
    
    return True, None

# ========================================
# 6. USER INTERFACE
# ========================================

def render_ui():
    """Render the main user interface."""
    
    # Header Section
    st.title("🌐 TransLingua")
    st.markdown("### AI-Powered Multilingual Translation")
    st.markdown("Powered by **Google Gemini 1.5 Flash** | Context-aware • Natural • Accurate")
    st.divider()
    
    # Get supported languages
    languages = get_supported_languages()
    language_names = ["Select Language"] + list(languages.keys())
    
    # Create two-column layout for language selection
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📥 Source Language")
        source_lang = st.selectbox(
            "Select source language",
            options=language_names,
            key="source_lang",
            label_visibility="collapsed"
        )
    
    with col2:
        st.markdown("#### 📤 Target Language")
        target_lang = st.selectbox(
            "Select target language",
            options=language_names,
            key="target_lang",
            label_visibility="collapsed"
        )
    
    st.divider()
    
    # Text Input Section
    st.markdown("#### ✍️ Enter Text to Translate")
    input_text = st.text_area(
        "Enter your text here...",
        height=200,
        placeholder="Type or paste your text here...",
        key="input_text",
        label_visibility="collapsed"
    )
    
    # Character count
    char_count = len(input_text) if input_text else 0
    st.caption(f"Characters: {char_count:,} / 30,000")
    
    st.divider()
    
    # Translation Button
    col_button1, col_button2, col_button3 = st.columns([1, 1, 1])
    with col_button2:
        translate_button = st.button(
            "🔄 Translate",
            type="primary",
            use_container_width=True
        )
    
    # Translation Logic
    if translate_button:
        # Validate input
        is_valid, error_message = validate_input(input_text, source_lang, target_lang)
        
        if not is_valid:
            st.error(error_message)
        else:
            # Show progress indicator
            with st.spinner("🔄 Translating..."):
                # Perform translation
                success, translated_text, error = translate_text(
                    input_text, 
                    source_lang, 
                    target_lang
                )
            
            if success:
                st.divider()
                st.markdown("#### ✅ Translation Result")
                
                # Display translated text in a nice container
                st.success(translated_text)
                
                # Add copy button functionality via download
                st.download_button(
                    label="📋 Copy Translation",
                    data=translated_text,
                    file_name="translation.txt",
                    mime="text/plain",
                    use_container_width=False
                )
                
                # Show translation statistics
                col_stat1, col_stat2, col_stat3 = st.columns(3)
                with col_stat1:
                    st.metric("Source Characters", f"{len(input_text):,}")
                with col_stat2:
                    st.metric("Translated Characters", f"{len(translated_text):,}")
                with col_stat3:
                    word_count = len(translated_text.split())
                    st.metric("Words", f"{word_count:,}")
            else:
                st.error(f"❌ {error}")
    
    # Footer with Team Information
    render_footer()

    # Sidebar with Information
    render_sidebar()

# ========================================
# 7. SIDEBAR INFORMATION
# ========================================

def render_sidebar():
    """Render the sidebar with app information and features."""
    with st.sidebar:
        st.markdown("## 📖 About TransLingua")
        st.markdown("""
        TransLingua is an AI-powered translation tool that uses 
        **Google Gemini 1.5 Flash** to provide context-aware, 
        natural translations across 40+ languages.
        """)
        
        st.divider()
        
        st.markdown("## ✨ Key Features")
        st.markdown("""
        - 🎯 **Context-Aware** translations
        - 🌍 **40+ Languages** supported
        - 📝 **Natural & Fluent** output
        - ⚡ **Real-time** processing
        - 🔒 **Secure** API integration
        - 🎨 **Clean** user interface
        """)
        
        st.divider()
        
        st.markdown("## 🚀 How to Use")
        st.markdown("""
        1. Select **source** language
        2. Select **target** language
        3. Enter or paste your **text**
        4. Click **Translate** button
        5. Copy or download the **result**
        """)
        
        st.divider()
        
        st.markdown("## 🛠️ Technical Stack")
        st.markdown("""
        - **Framework:** Streamlit
        - **AI Model:** Google Gemini 1.5 Flash
        - **Language:** Python 3.8+
        - **API:** Google Generative AI
        """)
        
        st.divider()
        
        st.markdown("## 📊 Limitations")
        st.markdown("""
        - Max input: 30,000 characters
        - Requires internet connection
        - API rate limits may apply
        """)
        
        st.divider()
        
        st.markdown("---")
        st.markdown("*Built with ❤️ using Streamlit & Gemini*")

# ========================================
# 8. FOOTER INFORMATION
# ========================================

def render_footer():
    """Render the detailed footer with team information."""
    st.divider()
    st.markdown("### 👨‍💻 Developed by Team")
    
    # Create columns for better layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Team Information**")
        st.write("🆔 **Team ID:** LTVIP2026TMIDS66217")
        st.write("👥 **Team Size:** 4 Members")
        
    with col2:
        st.markdown("**Team Members**")
        st.write("1. Jangita Takeshwar")
        st.write("2. Boya Hari Krishna")
        st.write("3. Kambala Manideep Reddy")
        st.write("4. Kota Lakshmi Prasanna")

# ========================================
# 9. MAIN APPLICATION ENTRY POINT
# ========================================

def main():
    """Main application entry point."""
    # Initialize the application
    initialize_app()
    
    # Render the user interface
    render_ui()

if __name__ == "__main__":
    main()
