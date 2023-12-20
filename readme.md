Google Service Account - https://console.cloud.google.com/iam-admin/serviceaccounts/

```bash
docker build -t lotinvest_tgbotimg .
```

```bash
docker run -d --name lotinvest_tgbot -p 80:80 lotinvest_tgbotimg
```

## Run ngrok

### Localy
```bash
ngrok http http://82.97.242.138:8000
```

### On server
```bash
ngrok http 8000
```
