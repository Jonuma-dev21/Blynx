#!/bin/bash
set -e

echo "demarre minikube si ce n'est pas deja fait"
minikube status || minikube start --memory=2048mb


echo "= Création du secret ="
minikube kubectl -- apply -f Q3-secret.yaml

echo "= Déploiement PostgreSQL avec import Netflix ="
minikube kubectl -- apply -f Q3.yaml

echo "= Attente du Pod ="
minikube kubectl -- wait --for=condition=ready pod -l app=postgres-netflix --timeout=180s

