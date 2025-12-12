#!/bin/bash



FICHIER_YML="replicaset.yaml"


# Applique le fichier YAML avec kubectl
echo "Déploiement de $FICHIER_YML sur Kubernetes..."
kubectl apply -f "$FICHIER_YML"

# Affiche le statut des ressources créées
echo "Ressources déployées :"
kubectl get all
