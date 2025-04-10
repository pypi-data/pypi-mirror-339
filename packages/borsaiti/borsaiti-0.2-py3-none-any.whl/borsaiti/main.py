
import os
import time
import random
import threading
import soundcard as sc
import soundfile as sf
from mtranslate import translate
import ollama
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
import speech_recognition as sr

api_key = None

def set_api(key):
    global api_key
    if key != "374gıayfaud738q":
        raise ValueError("❌ Geçersiz API anahtarı!")
    api_key = key

def baslat():
    if api_key is None:
        raise ValueError("❌ API anahtarı girilmemiş!")

    # GEMMA kontrolü
    try:
        _ = ollama.chat(model="gemma:2b", messages=[{"role": "user", "content": "ping"}])
    except Exception:
        print("⚠️ Gemma:2b modeli yüklü değil. Lütfen önce `ollama run gemma:2b` komutuyla yükleyin.")
        return

    profile_path = os.path.join(os.getcwd(), "borsaiti_chrome_profile")
    os.makedirs(profile_path, exist_ok=True)

    options = uc.ChromeOptions()
    options.user_data_dir = profile_path
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0")

    driver = uc.Chrome(options=options)
    driver.get("https://kick.com")

    print("✅ Kick.com açıldı! Lütfen giriş yap ve sonra ENTER’a bas.")
    input("🧑 Giriş yaptıysan ENTER'a bas: ")

    chat_input_xpath = input("✏️ Sohbet kutusunun XPath'ini gir: ")
    send_button_xpath = input("📤 Gönderme butonunun XPath'ini gir: ")

    def start_ai():
        SAMPLE_RATE = 48000
        RECORD_SEC = 10
        use_file_index = 1
        chat_history = []
        follow_up_questions = [
            "Senin düşüncen ne bu konuda?",
            "Sence bu yayında ne eksik?",
            "Chat buna ne diyor?",
            "Sen olsan ne yapardın?",
            "Daha iyisi nasıl olurdu sence?"
        ]
        system_prompt = {
            "role": "system",
            "content": (
                "You are an AI assistant in a Kick livestream. "
                "Speak in a short, natural, human way. Be very casual and realistic. "
                "Reply in 1 short sentence only. No robotic tone. Respond based on what the user says."
            )
        }

        def build_prompt(user_input):
            chat_history.append({"role": "user", "content": user_input})
            return [system_prompt] + chat_history[-5:]

        while True:
            file_current = f"out{use_file_index}.wav"
            file_to_delete = f"out{2 if use_file_index == 1 else 1}.wav"

            print("🎧 Masaüstü sesi dinleniyor...")
            try:
                with sc.get_microphone(id=str(sc.default_speaker().name), include_loopback=True).recorder(samplerate=SAMPLE_RATE) as mic:
                    data = mic.record(numframes=SAMPLE_RATE * RECORD_SEC)
                    sf.write(file_current, data[:, 0], samplerate=SAMPLE_RATE)
            except Exception as e:
                print(f"🎙️ Kayıt hatası: {e}")
                continue

            try:
                if os.path.exists(file_to_delete):
                    time.sleep(0.5)
                    os.remove(file_to_delete)
            except Exception as e:
                print(f"🗑️ Dosya silme hatası: {e}")

            try:
                recognizer = sr.Recognizer()
                with sr.AudioFile(file_current) as source:
                    audio = recognizer.record(source)
                turkish_text = recognizer.recognize_google(audio, language="tr-TR")
                print("🧑 (Sen):", turkish_text)
            except Exception as e:
                print(f"❌ Ses tanıma hatası: {e}")
                use_file_index = 2 if use_file_index == 1 else 1
                continue

            translated_text = translate(turkish_text, "en", "tr")
            prompt = build_prompt(translated_text)
            response = ollama.chat(model="gemma:2b", messages=prompt)
            english_reply = response["message"]["content"].strip().split(".")[0].strip() + "."
            translated_reply = translate(english_reply, "tr", "en")

            if random.random() < 0.1:
                translated_reply += " " + random.choice(follow_up_questions)

            delay = random.randint(5, 10)
            print(f"⌛ Cevap {delay} sn sonra geliyor...")
            time.sleep(delay)
            print("🤖 (AI):", translated_reply)
            chat_history.append({"role": "assistant", "content": english_reply})

            try:
                message_input = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, chat_input_xpath))
                )
                ActionChains(driver).move_to_element(message_input).click().send_keys(translated_reply).perform()
                send_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, send_button_xpath))
                )
                send_button.click()
                print("📤 Gönderildi!")
            except Exception as msg_err:
                print(f"❗ Mesaj gönderme hatası: {msg_err}")

            use_file_index = 2 if use_file_index == 1 else 1

    print("🕒 AI sistemi 60 saniye sonra devreye girecek...")
    threading.Timer(60, start_ai).start()
