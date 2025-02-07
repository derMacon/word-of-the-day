#!/bin/bash

# Set the working directory to the script's location
cd "$(dirname "$0")"

echo -e "\n*********************"
echo "** Word of the day **"
echo "*********************"
echo " - starting wotd project at $(pwd)"

if [ ! -e ./.env ]; then
    echo " - .env file does not exist, not able to start cluster"
    echo " - take a look at the example .env file at ./invalid-example.env"
    echo "-----------"
    cat ./invalid-example.env
    echo -e "-----------\n"
else
    echo " - starting all wotd docker containers"
    echo -e " - logs are available at ./logs\n"
    docker-compose up -d
    echo ""
fi

