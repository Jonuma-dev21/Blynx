#!/bin/bash

# Script pour supprimer l'infrastructure PostgreSQL résiliente sur Kubernetes

set -e  # Arrêter le script si une commande échoue

POD_DIR="postgres"





echo "Suppression du primaire..."
kubectl delete -f $POD_DIR/postgres-primary.yaml --ignore-not-found

echo "Suppression des réplicas..."
kubectl delete -f $POD_DIR/postgres-replica.yaml --ignore-not-found

echo "Suppression du service primaire..."
kubectl delete -f $POD_DIR/postgres-primary-svc.yaml --ignore-not-found

echo "Suppression du service réplicas..."
kubectl delete -f $POD_DIR/postgres-replica-svc.yaml --ignore-not-found

echo "Suppression du ConfigMap pour initialisation des réplicas..."
kubectl delete -f $POD_DIR/init-replica-configmap.yaml --ignore-not-found

echo "Suppression des réplicas..."
kubectl delete -f $POD_DIR/postgres-replica.yaml --ignore-not-found

echo "Suppression terminée !"

# Optionnel : afficher les pods et services restants
echo "État des pods restant :"
kubectl get pods -o wide

echo "État des services restant :"
kubectl get svc
