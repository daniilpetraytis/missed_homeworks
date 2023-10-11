### Сборка
```bash
docker build -t script_3 .
```
### Запуск
```bash
docker run --rm -v </path/to/script/>:/my_docker script_3 file.txt
```

### Пример
```bash
docker build -t script_3 .
docker run --rm -v ~/Desktop/hse/missed_homeworks/hw2_1/3:/my_docker script_3 file.txt
```