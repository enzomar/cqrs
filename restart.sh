CONTAINER=$1
echo "rebuild and restart container: "$CONTAINER
docker-compose stop $CONTAINER
docker-compose rm -f $CONTAINER
docker-compose build  $CONTAINER
docker-compose up -d  $CONTAINER
