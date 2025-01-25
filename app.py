import streamlit as st
import speech_recognition as sr
import pyttsx3
import google.generativeai as genai

class SpeechBot:
    def __init__(self):
        genai.configure(api_key="AIzaSyDgwigYRrAUJVga_0jzfRzfZY-MXGgf6nU")
        self.model = genai.GenerativeModel("gemini-1.5-flash")

        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 1)

        self.is_listening = False
    def recognize_speech(self):
        try:
            with sr.Microphone() as source:
                st.write("🎤 Listening... Please speak into the microphone.")
                audio = self.recognizer.listen(source, timeout=10)
                text = self.recognizer.recognize_google(audio)
                return text
        except sr.WaitTimeoutError:
            st.warning("Listening timed out.")
        except sr.UnknownValueError:
            st.warning("Sorry, I couldn't understand that.")
        except Exception as e:
            st.error(f"Error: {e}")
        return None

    def generate_response(self, input_text):
        try:
            response = self.model.generate_content(input_text)
            return response.text
        except Exception as e:
            return f"Error generating response: {e}"

    def speak_response(self, text):
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            st.error(f"Error in text-to-speech: {e}")

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
    user_input = None

    with col1:
        user_input = st.text_input("Type your message:")

    with col2:
        if st.button("🎤 Listen"):
            user_input = bot.recognize_speech()
            if user_input:
                st.write(f"You said: {user_input}")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        bot_response = bot.generate_response(user_input)
        st.session_state.messages.append({"role": "assistant", "content": bot_response})
        with st.chat_message("assistant"):
            st.markdown(bot_response)

        bot.speak_response(bot_response)

if __name__ == "__main__":
    main()