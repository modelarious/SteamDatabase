docker run --rm \
    -d \
    --name steam_gremlin_backend \
    -v "${PWD}/backend/src":"/SteamGremlinBackend/src" \
    -p 3091:3091 \
    steam_gremlin_backend
