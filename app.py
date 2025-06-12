from flask import Flask, render_template, request, send_file, after_this_request
from gtts import gTTS
from pydub import AudioSegment
import os
from datetime import datetime
import time

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/audio'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text = request.form['text']
        language = 'id'  # Bahasa Indonesia
        speed = request.form.get('speed', 'normal')
        gender = request.form.get('gender', 'female')
        
        # Ambil rasio kecepatan dari slider (default 1.0)
        try:
            speed_ratio = float(request.form.get('speed', 1.0))
        except ValueError:
            speed_ratio = 1.0

        # Gender (gTTS terbatas, untuk alternatif lebih baik gunakan pyttsx3)
        tld = 'com'  # default female
        if gender == 'male':
            tld = 'com.au'  # aksen yang lebih dalam (tidak selalu bekerja)

        # Generate TTS (gTTS hanya support slow True/False, jadi pakai normal dulu)
        tts = gTTS(text=text, lang=language, slow=False, tld=tld)

        # Simpan file dengan timestamp unik
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"tts_{timestamp}.mp3"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        tts.save(filepath)

        # Jika speed_ratio bukan 1.0, ubah kecepatan audio dengan pydub
        if abs(speed_ratio - 1.0) > 0.01:
            # Pastikan file benar-benar sudah selesai ditulis oleh gTTS
            for _ in range(20):
                if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
                    try:
                        sound = AudioSegment.from_file(filepath)
                        new_frame_rate = int(sound.frame_rate * speed_ratio)
                        new_sound = sound._spawn(sound.raw_data, overrides={"frame_rate": new_frame_rate})
                        new_sound = new_sound.set_frame_rate(sound.frame_rate)
                        new_sound.export(filepath, format="mp3")
                        break
                    except Exception as e:
                        time.sleep(0.1)
                else:
                    time.sleep(0.1)
            else:
                print(f"File {filepath} tidak ditemukan atau gagal diproses setelah menunggu.")

        # Kirim file dan hapus setelah didownload
        @after_this_request
        def remove_file(response):
            try:
                os.remove(filepath)
            except Exception as error:
                app.logger.error("Error removing file", error)
            return response
        
        return send_file(filepath, as_attachment=True, download_name=f"tts_output.mp3")
    
    return render_template('index.html')

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)