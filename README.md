# JS
```js
var data = JSON.stringify({
   "pregnancies": 6,
   "glucose": 148,
   "blood_pressure": 72,
   "skin_thickness": 35,
   "insulin": 0,
   "bmi": 33.6,
   "diabetes_pedigree_function": 0.627,
   "age": 50
});
```

# Nginx
```nginx
server {
        listen 8080;
        server_name diabetes.test

        location / {
                proxy_pass http://127.0.0.1:8000;
                proxy_set_header Host $host;
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
}
```

# Gunicorn
```bash
gunicorn --workers 4 --bind 127.0.0.1:8000 serve:app
```
