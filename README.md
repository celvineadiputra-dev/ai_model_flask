# AI Model Prediction API Setup

## 1. Contoh Data Input

### a. Prediksi Diabetes (JSON)

Data input berupa JSON yang dikirim ke API:

```js
var data = JSON.stringify({
   "pregnancies": 6,                // Jumlah kehamilan
   "glucose": 148,                  // Kadar glukosa darah
   "blood_pressure": 72,            // Tekanan darah
   "skin_thickness": 35,            // Ketebalan lipatan kulit
   "insulin": 0,                    // Kadar insulin
   "bmi": 33.6,                     // Body Mass Index
   "diabetes_pedigree_function": 0.627, // Faktor riwayat diabetes keluarga
   "age": 50                        // Usia pasien
});
```

> JSON ini bisa dikirim menggunakan `fetch` atau library HTTP lain ke endpoint prediksi API.

### b. Prediksi Gunting-Batu-Kertas (Image)

Data input berupa file image (`multipart/form-data`) dengan field `"file"`:

```js
var formData = new FormData();
formData.append("file", myFile);

fetch("http://diabetes.test/predict-rps", {
    method: "POST",
    body: formData
});
```

---

## 2. Konfigurasi Nginx

Gunakan Nginx sebagai reverse proxy untuk meneruskan request ke aplikasi yang berjalan di Gunicorn:

```nginx
server {
        listen 8080;                   # Port yang digunakan Nginx
        server_name diabetes.test;      # Nama domain / hostname

        location / {
                proxy_pass http://127.0.0.1:8000;   # Forward ke Gunicorn
                proxy_set_header Host $host;
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
}
```

> Pastikan menambahkan `127.0.0.1 diabetes.test` pada file `/etc/hosts` jika menggunakan domain lokal.

---

## 3. Menjalankan Gunicorn

Gunicorn digunakan untuk menjalankan aplikasi Python secara production-ready:

```bash
gunicorn --workers 4 --bind 127.0.0.1:8000 serve:app --daemon
```

* `--workers 4`: Jumlah worker proses.
* `--bind 127.0.0.1:8000`: Bind ke alamat lokal.
* `serve:app`: Nama file Python (`serve.py`) dan instance Flask/FastAPI (`app`).
* `--daemon`: Jalankan sebagai background process.

---

## 4. Menghentikan Gunicorn

Jika Gunicorn dijalankan dengan `--daemon`, hentikan dengan perintah:

```bash
pkill gunicorn
```

---

## 5. Link Model Prediksi

Model yang digunakan untuk prediksi gunting-batu-kertas:

[https://drive.google.com/file/d/1mWRO3eRArrj3JLzNIVZcKdK5xgawUCZ0/view?usp=sharing](url)

> Download model ini dan letakkan di folder model.
