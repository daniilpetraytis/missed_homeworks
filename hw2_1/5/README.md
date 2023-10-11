### Сборка
```bash
docker build -t script_5 .
```
### Запуск
```bash
docker run -v //path/to/script/dir:/my_docker -v //path/to/script/dir:/report -e FILE=/my_docker/main.py script_5
```
