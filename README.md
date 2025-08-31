```bash
docker compose up -d --build
```

```commandline
docker compose down --rmi all --volumes --remove-orphans
docker ps -a | grep history_web # Проверить состояние контейнера:
`docker logs history_web --tail 50` # Посмотреть логи контейнера, чтобы понять причину перезапуска:

```