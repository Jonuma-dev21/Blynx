#!/bin/bash

# Script pour déployer l'infrastructure PostgreSQL résiliente sur Kubernetes

set -e  # Arrêter le script si une commande échoue

POD_DIR="postgres"


kubectl apply -f $POD_DIR/replica-pvc.yaml

echo "Déploiement des secrets..."
kubectl apply -f $POD_DIR/postgres-secret.yaml

echo "Déploiement du ConfigMap pour initialisation des réplicas..."
kubectl apply -f $POD_DIR/init-replica-configmap.yaml

echo "Déploiement du primaire..."
kubectl apply -f $POD_DIR/postgres-primary.yaml

echo "Déploiement des réplicas..."
kubectl apply -f $POD_DIR/postgres-replica.yaml

echo "Déploiement du service primaire..."
kubectl apply -f $POD_DIR/postgres-primary-svc.yaml

echo "Déploiement du service réplicas..."
kubectl apply -f $POD_DIR/postgres-replica-svc.yaml



echo "Déploiement terminé !"

# Optionnel : afficher les pods et services
echo "État des pods :"
kubectl get pods -o wide

echo "État des services :"
kubectl get svc
