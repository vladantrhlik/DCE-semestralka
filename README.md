# DCE semestrálka

Distribuovaný key-value store postavený na Apache ZooKeeperu s jednoduchým REST
frontendem. Zdrojové soubory obou kontejnerů jsou oddělené v adresářích `zookeeper/`
a `frontend/`; oba image vycházejí z Alpine Linuxu.

## Spuštění

Z kořene projektu spusťte tříuzlový ZooKeeper ensemble a jeden frontend:

```sh
docker compose pull
docker compose up -d
```

REST API je dostupné z hostitele na `http://localhost:5000`. Kontejnery ve
stejné Compose síti jej mohou volat na `http://frontend:5000`.
Swagger UI otevřete na `http://localhost:5000/docs`.

Compose definuje tříuzlový ZooKeeper ensemble; každý uzel má vlastní
pojmenovaný Docker volume. ZooKeeper uzly mají pevné identity a seznam peerů.
Chcete-li změnit počet uzlů, upravte jejich služby, `ZOO_SERVERS` ve všech
uzlech a `ZK_HOSTS` frontendu v `compose.yaml`.

Pro zastavení:

```sh
docker compose down
```

Pojmenované volumes zůstanou zachované; pro jejich odstranění je třeba spustit
`docker compose down -v`.

### Publikování do GitHub Container Registry

Workflow `.github/workflows/publish-images.yml` sestaví a publikuje oba
image do GHCR při pushnutí tagu ve tvaru `dce-semestralka-vX.Y.Z`. Například:

```sh
git tag dce-semestralka-v1.0.0
git push origin dce-semestralka-v1.0.0
```

Výsledné image budou `ghcr.io/vladantrhlik/dce-zookeeper:1.0.0` a
`ghcr.io/vladantrhlik/dce-frontend:1.0.0`; workflow zároveň aktualizuje tag
`latest`.

## REST API

OpenAPI/Swagger specifikace je v souboru [`frontend/openapi.yaml`](frontend/openapi.yaml)
a Swagger UI ji načítá z `http://localhost:5000/openapi.yaml`.

- `GET /health` — stav spojení frontendu se ZooKeeperem.
- `GET /kv` — seznam klíčů.
- `GET /kv/<key>` — načtení hodnoty.
- `PUT /kv/<key>` — vytvoření nebo přepsání hodnoty; tělo požadavku musí být
  JSON (například `{"name":"Ada"}`).
- `DELETE /kv/<key>` — odstranění klíče.

Příklad zápisu a čtení:

```sh
curl -X PUT http://localhost:5000/kv/greeting \
  -H "Content-Type: application/json" -d '"hello"'
curl http://localhost:5000/kv/greeting
```