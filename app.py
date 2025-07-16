from flask import Flask, request, jsonify
from instagrapi import Client
from dotenv import load_dotenv
import os
import json # JSON modülünü import ediyoruz

load_dotenv()

app = Flask(__name__)

# instagrapi Client nesnesini başlatıyoruz
cl = Client()

# Railway'den alacağımız JSON oturum ayarlarını çekeceğiz
INSTAGRAM_SETTINGS_JSON = os.getenv("INSTAGRAM_SETTINGS_JSON")

if INSTAGRAM_SETTINGS_JSON:
    try:
        # Ortam değişkeninden gelen JSON stringini Python dict'e dönüştürüyoruz
        settings_dict = json.loads(INSTAGRAM_SETTINGS_JSON)
        # Bu ayarları instagrapi Client'a yüklüyoruz
        cl.set_settings(settings_dict)
        print("INSTAGRAM_SETTINGS_JSON yüklendi ve oturum ayarlandı.")
    except json.JSONDecodeError as e:
        # Eğer ortam değişkenindeki değer geçerli bir JSON değilse
        print(f"Hata: INSTAGRAM_SETTINGS_JSON ortam değişkeni geçerli bir JSON değil: {e}")
        raise ValueError("INSTAGRAM_SETTINGS_JSON ortam değişkeni JSON formatında olmalı.")
    except Exception as e:
        # Diğer olası hatalar için
        print(f"Oturum ayarları yüklenirken genel bir hata oluştu: {e}")
        raise ValueError("Oturum ayarları yüklenemedi. Uygulama başlatılamıyor.")
else:
    # Eğer INSTAGRAM_SETTINGS_JSON ortam değişkeni hiç ayarlanmamışsa
    print("Uyarı: INSTAGRAM_SETTINGS_JSON ortam değişkeni bulunamadı. Uygulama Instagram'a bağlanamayabilir.")
    raise ValueError("INSTAGRAM_SETTINGS_JSON ortam değişkeni gereklidir.")

@app.route("/get_user", methods=["GET"])
def get_user():
    username = request.args.get("username")
    if not username:
        return jsonify({"error": "username parametresi eksik"}), 400

    try:
        user_info = cl.user_info_by_username(username)
        return jsonify(user_info.dict())
    except Exception as e:
        # Bu kısımda daha spesifik hata yakalama (örneğin instagrapi.exceptions.LoginRequired)
        # veya JSONDecodeError gibi hataları ayrıştırmak daha iyi olabilir.
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)