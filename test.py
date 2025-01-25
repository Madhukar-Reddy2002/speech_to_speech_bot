import streamlit as st
import speech_recognition as sr
from gtts import gTTS
import os
import google.generativeai as genai

class SpeechBot:
    def __init__(self):
        # Configure Gemini API
        genai.configure(api_key="AIzaSyDgwigYRrAUJVga_0jzfRzfZY-MXGgf6nU")
        self.model = genai.GenerativeModel("gemini-1.5-flash")
        
        # Speech recognition setup
        self.recognizer = sr.Recognizer()

    def recognize_speech(self):
        try:
            with sr.Microphone() as source:
                st.write("🎤 Listening... Speak now.")
                audio = self.recognizer.listen(source, timeout=5)
                text = self.recognizer.recognize_google(audio)
                return text
        except Exception as e:
            st.error(f"Speech recognition error: {e}")
            return None

    def generate_response(self, input_text):
        try:
            response = self.model.generate_content(input_text)
            return response.text
        except Exception as e:
            return f"Error generating response: {e}"

    def text_to_speech(self, text):
        try:
            tts = gTTS(text=text, lang='en')
            audio_file = "response.mp3"
            tts.save(audio_file)
            
            # Use a context manager to ensure file is closed
            with open(audio_file, 'rb') as audio:
                st.audio(audio, format='audio/mp3')
            
            # Attempt to remove file, but don't raise an error if it fails
            try:
                os.remove(audio_file)
            except PermissionError:
                pass
        except Exception as e:
            st.error(f"Text-to-speech error: {e}")

def main():
    st.set_page_config(page_title="AI Chat Bot", page_icon="🤖")
    st.title("🤖 AI Chat Companion")

    bot = SpeechBot()

    if 'messages' not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    col1, col2 = st.columns(2)

    with col1:
        user_input = st.text_input("Type your message:")

    with col2:
        if st.button("🎤 Listen"):
            user_input = bot.recognize_speech()

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        bot_response = bot.generate_response(user_input)
        st.session_state.messages.append({"role": "assistant", "content": bot_response})
        
        with st.chat_message("assistant"):
            st.markdown(bot_response)
        
        bot.text_to_speech(bot_response)

if __name__ == "__main__":
    main()