# Program Pengirim Email SMTP

Program Python untuk mengirim email dengan lampiran menggunakan protokol SMTP ke server MailHog.

## Deskripsi

Program ini adalah implementasi sederhana dari client SMTP yang memungkinkan pengguna untuk:
- Mengirim email dengan alamat penerima, subjek, dan isi pesan yang dinamis (input dari terminal)
- Melampirkan file `laporan_praktikum.txt` secara otomatis
- Terhubung ke server MailHog sebagai SMTP server lokal untuk testing

## Requirements

- **Python 3.x**
- **MailHog** - Server SMTP lokal untuk testing email

### Instalasi MailHog

```bash
# Menggunakan Go
go install github.com/mailhog/MailHog@latest

# Atau download binary dari releases
# https://github.com/mailhog/MailHog/releases
```

## Konfigurasi

| Parameter | Nilai Default | Deskripsi |
|-----------|---------------|-----------|
| `SMTP_SERVER` | `localhost` | Alamat server SMTP |
| `SMTP_PORT` | `1025` | Port SMTP MailHog |
| `EMAIL_PENGIRIM` | `praktikum@local.test` | Alamat email pengirim |

## Cara Menjalankan

1. **Jalankan MailHog terlebih dahulu:**
   ```bash
   mailhog
   ```
   MailHog akan berjalan di:
   - SMTP: `localhost:1025`
   - Web UI: `http://localhost:8025`

2. **Pastikan file lampiran tersedia:**
   ```bash
   # Jika belum ada, buat file lampiran
   touch laporan_praktikum.txt
   
   # Isi dengan konten (opsional)
   echo "Isi laporan praktikum" > laporan_praktikum.txt
   ```

3. **Jalankan program:**
   ```bash
   python main.py
   ```

4. **Ikuti prompt di terminal:**
   ```
   === PROGRAM PENGIRIM EMAIL ===
   Masukkan Email Penerima: recipient@example.com
   Masukkan Subjek Email: Test Email
   Masukkan Isi Pesan: Halo, ini adalah pesan testing.
   ```

5. **Cek email di MailHog Web UI:** Buka `http://localhost:8025`

## Struktur File

```
praktikum-smtp/
├── main.py                   # Program utama pengirim email
├── laporan_praktikum.txt     # File lampiran yang akan dikirim
├── Slide_SMTP_POP3.pdf       # Materi referensi SMTP/POP3
└── README.md                 # Dokumentasi ini
```

## Komponen Utama Program

### 1. Import Library
- `smtplib` - Library standar Python untuk komunikasi SMTP
- `email.mime.*` - Untuk membuat struktur email multipart (body + attachment)
- `os` - Untuk operasi file system

### 2. Fungsi `kirim_email_dinamis()`
Fungsi utama yang menangani keseluruhan proses pengiriman email:
- Menerima input dari user (penerima, subjek, isi pesan)
- Membangun objek email dengan struktur MIME
- Menambahkan lampiran file
- Mengirim email melalui koneksi SMTP

## Alur Kerja Program (Flowchart)

```mermaid
flowchart TD
    A([Start Program]) --> B[/"Input Email Penerima"/]
    B --> C[/"Input Subjek Email"/]
    C --> D[/"Input Isi Pesan"/]
    D --> E["Tentukan Path File Lampiran"]
    
    E --> F["Buat Objek Email<br/>(MIMEMultipart)"]
    F --> G["Set Header Email<br/>(From, To, Subject)"]
    G --> H["Tambahkan Body Email<br/>(MIMEText)"]
    
    H --> I{"Buka File<br/>Lampiran?"}
    
    I -->|Sukses| J["Encode File ke Base64<br/>(MIMEBase)"]
    J --> K["Attach File ke Email"]
    K --> L["Info: File Berhasil Dilampirkan"]
    
    I -->|FileNotFoundError| M["Error: File Tidak Ditemukan"]
    M --> N["Tampilkan Tips"]
    N --> Z([End Program])
    
    L --> O{"Koneksi ke<br/>Server SMTP?"}
    
    O -->|Sukses| P["Kirim Email<br/>(send_message)"]
    P --> Q["Tutup Koneksi<br/>(quit)"]
    Q --> R["SUKSES: Email Terkirim"]
    R --> Z
    
    O -->|ConnectionRefusedError| S["GAGAL: Tidak Bisa Terhubung"]
    S --> T["Tips: Pastikan MailHog Berjalan"]
    T --> Z
    
    O -->|Exception Lain| U["Error Tidak Terduga"]
    U --> Z

    style A fill:#4CAF50,color:#fff
    style Z fill:#f44336,color:#fff
    style R fill:#4CAF50,color:#fff
    style M fill:#ff9800,color:#fff
    style S fill:#ff9800,color:#fff
    style U fill:#ff9800,color:#fff
    style I fill:#2196F3,color:#fff
    style O fill:#2196F3,color:#fff
```

## Diagram Sequence Pengiriman Email

```mermaid
sequenceDiagram
    autonumber
    participant U as User
    participant P as Program (main.py)
    participant F as File System
    participant S as MailHog SMTP

    U->>P: Jalankan program
    P->>U: Minta input (penerima, subjek, pesan)
    U->>P: Berikan input
    
    P->>P: Buat objek MIMEMultipart
    P->>P: Set header (From, To, Subject)
    P->>P: Attach body email (MIMEText)
    
    P->>F: Baca file lampiran
    
    alt File ditemukan
        F-->>P: Return file content
        P->>P: Encode ke Base64
        P->>P: Attach file ke email
        
        P->>S: Buka koneksi SMTP (localhost:1025)
        
        alt Koneksi berhasil
            S-->>P: Connection established
            P->>S: send_message(email)
            S-->>P: Message accepted
            P->>S: quit()
            P->>U: Email berhasil dikirim
        else Koneksi gagal
            S-->>P: ConnectionRefusedError
            P->>U: Gagal terhubung ke server
        end
        
    else File tidak ditemukan
        F-->>P: FileNotFoundError
        P->>U: File tidak ditemukan
    end
```

## Diagram Struktur Email MIME

```mermaid
graph TB
    subgraph EMAIL["Email Message (MIMEMultipart)"]
        direction TB
        H["Headers"]
        B["Body (MIMEText)"]
        A["Attachment (MIMEBase)"]
    end
    
    subgraph HEADERS["Header Details"]
        H1["From: praktikum@local.test"]
        H2["To: user input"]
        H3["Subject: user input"]
    end
    
    subgraph BODY["Body Details"]
        B1["Content-Type: text/plain"]
        B2["Content: user input"]
    end
    
    subgraph ATTACH["Attachment Details"]
        A1["Filename: laporan_praktikum.txt"]
        A2["Content-Type: application/octet-stream"]
        A3["Encoding: Base64"]
    end
    
    H --> HEADERS
    B --> BODY
    A --> ATTACH

    style EMAIL fill:#e3f2fd,stroke:#1976d2
    style HEADERS fill:#fff3e0,stroke:#ff9800
    style BODY fill:#e8f5e9,stroke:#4caf50
    style ATTACH fill:#fce4ec,stroke:#e91e63
```

## Penanganan Error

| Error | Penyebab | Solusi |
|-------|----------|--------|
| `FileNotFoundError` | File `laporan_praktikum.txt` tidak ada | Buat file dengan `touch laporan_praktikum.txt` |
| `ConnectionRefusedError` | MailHog tidak berjalan | Jalankan `mailhog` di terminal terpisah |
| Exception lainnya | Berbagai penyebab | Cek pesan error untuk detail |

## Referensi

- [Python smtplib Documentation](https://docs.python.org/3/library/smtplib.html)
- [Python email.mime Documentation](https://docs.python.org/3/library/email.mime.html)
- [MailHog GitHub Repository](https://github.com/mailhog/MailHog)
- [RFC 5321 - Simple Mail Transfer Protocol](https://tools.ietf.org/html/rfc5321)

---

> **Catatan:** Program ini ditujukan untuk keperluan praktikum dan testing. Untuk penggunaan produksi, pertimbangkan penggunaan autentikasi SMTP dan enkripsi TLS.
