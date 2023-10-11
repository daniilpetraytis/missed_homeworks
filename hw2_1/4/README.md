### Сборка
```bash
docker build -t script_4 .
```
### Запуск
```bash
docker run -p 3000:3000 script_4
```
### Дергаем ручку
```bash
curl 'http://127.0.0.1:3000/hello'
```
