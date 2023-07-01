HWNAME=`uname -m | awk {'print $1'}`

if [ $HWNAME='arm64' ];
then
    docker-compose --file ./docker/arm64/docker-compose.yml up -d
elif [ $HWNAME='x86_64' ];
then
    docker-compose --file ./docker/x86_64/docker-compose.yml up -d
else
    echo "Unsupported machine: $HWNAME"
fi
