import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

# Konfigurasi Server SMTP (MailHog)
SMTP_SERVER = "localhost"
SMTP_PORT = 1025
EMAIL_PENGIRIM = "praktikum@local.test"

def kirim_email_dinamis():
    print("=== PROGRAM PENGIRIM EMAIL ===")
    
    # Input data email dari terminal
    email_penerima = input("Masukkan Email Penerima: ")
    subjek_email = input("Masukkan Subjek Email: ")
    isi_pesan = input("Masukkan Isi Pesan: ")
    
    # Tentukan lokasi file lampiran
    nama_file = "laporan_praktikum.txt"
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, nama_file)

    # Inisialisasi objek email
    msg = MIMEMultipart()
    msg["From"] = EMAIL_PENGIRIM
    msg["To"] = email_penerima
    msg["Subject"] = subjek_email

    # Tambahkan body email
    msg.attach(MIMEText(isi_pesan, "plain"))

    # Proses lampiran file
    try:
        with open(file_path, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename={nama_file}"
            )
            msg.attach(part)
            print(f"[INFO] File '{nama_file}' berhasil dilampirkan.")
            
    except FileNotFoundError:
        print(f"[ERROR] File '{nama_file}' tidak ditemukan!")
        print("Tips: Buat file dengan perintah 'touch laporan_praktikum.txt'")
        return 

    # Proses pengiriman email via SMTP
    try:
        print("[INFO] Menghubungkan ke server MailHog...")
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.send_message(msg)
        server.quit()
        print("SUKSES: Email berhasil dikirim ke MailHog!")
        
    except ConnectionRefusedError:
        print("GAGAL: Tidak bisa terhubung ke server.")
        print("Tips: Pastikan MailHog sudah berjalan.")
        
    except Exception as e:
        print(f"TERJADI ERROR LAIN: {e}")

if __name__ == "__main__":
    kirim_email_dinamis()