#!/bin/bash

# Set the working directory to the script's location
cd "$(dirname "$0")"

echo -e "\n*********************"
echo "** Word of the day **"
echo "*********************"
echo " - starting wotd project at $(pwd)"

if [ ! -e ./.env2 ]; then
    echo " - .env file does not exist, not able to start cluster"
    echo " - take a look at the example .env file at ./invalid-example.env"
    echo "-----------"
    cat ./invalid-example.env
    echo -e "-----------\n"
else
    echo "- starting all wotd docker containers"
    echo "- logs are available at ./logs"
    docker-compose up -d
fi

