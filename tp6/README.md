# TP6

## 1- Installation de Minikube

Pour l'installation de `Minikube` depuis votre poste sur machine distante.


### Etape 1 configuration de ton inventaire.yml

voici ma configuration que vous pouvez l'adaptez en fonction de votre besoin.

```yml
serveur:
  hosts:
    serveur:
      ansible_host: 172.28.100.126
      ansible_user: ubuntu
      ansible_private_key_file: '~/.ssh/cloud.key'
```
### Etape 2 Lancer l'installation

Pour lancer l'installation sur ta machine distance configurée il suffit de lancer cette dans le repertoire `/tp6`

```bash
ansible-playbook -i inventaire.yaml Q1_installation_minikube.yaml
```

## Le role du fichier deploiement.yaml

Deploiment ce charge d'envoyer les fichiers necessaires sur ta machine distante, congiurée avec l'inventaire, et lancer le sript passé en paramètre avec l'argument `cript_name`. 

## 2- Pod PostgreSQL basique

Pour pouvoir lancer un pod « manuel » contenant seulement un conteneur PostgreSQL
avec une configuration valide.

Il suffit juste de lancer cette commande depuis ton poste local depuis le repertoire `/tp6`
```bash
ansible-playbook -i inventaire.yaml deploiement.yaml -e "script_name=Q2.sh"
```

J’ai déployé un Pod Kubernetes contenant un conteneur PostgreSQL, configuré pour exposer le port 5432. J’ai défini les variables pour créer la base ecole avec l’utilisateur admin et le mot de passe bzibzi.

## 3- Pod PostgreSQL type Deployment

Miantenant, nous allons utliser un `Deployment` contenant un seul conteneur PostgreSQL.
Le conteneur va etre peupler automatiquement avec un jeu de données de Netflix.

Il suffit juste de lancer cette commande depuis ton poste local depuis le repertoire `/tp6`
```bash
ansible-playbook -i inventaire.yaml deploiement.yaml -e "script_name=Q3.sh"
```

J’ai créé un Deployment Kubernetes pour PostgreSQL avec un seul replica.
Un initContainer télécharge et décompresse la base Netflix dans un volume partagé.
Le conteneur principal PostgreSQL utilise ce volume pour initialiser la base.
Le mot de passe est sécurisé via un Secret.
Le service expose PostgreSQL sur le port 5432 pour l’accès interne et externe.


## 4- Publication de service

Il suffit juste de lancer cette commande depuis ton poste local depuis le repertoire `/tp6`
```bash
ansible-playbook -i inventaire.yaml deploiement.yaml -e "script_name=Q4.sh"
```

J’ai créé un Service pour exposer la base de données PostgreSQL.
J’ai choisi le type NodePort afin de pouvoir accéder à PostgreSQL depuis l’extérieur du cluster, en attribuant un port fixe (32345) sur chaque nœud.
Le Service écoute sur le port interne 5432 et redirige les connexions vers le même port sur les Pods, utilisant le protocole TCP propre à PostgreSQL. Grâce à cette configuration, je peux me connecter à la base de données de manière stable et fiable, sans avoir à connaître l’IP exacte de chaque Pod, tout en gardant la possibilité d’accès interne et externe.

