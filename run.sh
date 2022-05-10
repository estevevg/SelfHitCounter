cmd=${@:-/bin/bash}
echo $PWD
docker run --rm \
    --user "$(id -u):$(id -g)" \
    -v "$PWD":/opt/app \
    -it $(docker build . -q) \
    $cmd
