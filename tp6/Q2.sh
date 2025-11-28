#!/bin/bash

echo "Création du Pod PostgreSQL"
minikube kubectl -- apply -f Q2.yaml

echo "Attente que le Pod soit en execution"
minikube kubectl -- wait --for=condition=Ready pod/postgres-pod --timeout=60s

echo "Vérification du Pod :"
minikube kubectl -- get pods postgres-pod

echo "Connexion a PostgreSQL dans le conteneur"
minikube kubectl -- exec -it postgres-pod -- psql -U admin -d postgres -c "SELECT datname FROM pg_database;"

echo "Test terminé : PostgreSQL est Ok dans le Pod."

