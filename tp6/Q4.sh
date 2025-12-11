#!/bin/bash
set -e

echo "= Création du Service NodePort pour la connexion locale ="
minikube kubectl -- apply -f Q4.yaml

echo "= Attente du Service ="
sleep 5


MINIKUBE_IP=$(minikube ip)
echo "Service PostgreSQL accessible sur $MINIKUBE_IP:32345"

echo "= Test de connexion SQL depuis la machine hôte ="
PGPASSWORD=bzibzi psql -h $MINIKUBE_IP -p 32345 -U postgres -c "\dt"
