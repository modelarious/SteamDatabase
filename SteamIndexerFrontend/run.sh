echo 
docker run --rm \
    --name steam_indexer_frontend \
    -v "${PWD}/steam-indexer-frontend/src":"/steam-indexer-frontend/src" \
    -p 5173:5173 \
    steam_indexer_frontend
