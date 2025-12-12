reformuler ce rapport
et envoie le resuktat sous code markdown
# TP7

## 1 Provisionnement avec OpenTofu

Pour l’approvisionnement, place-toi dans le répertoire tofu, configure le fichier `terraform.tfvars` , puis exécute les trois commandes suivantes :
```bash
docker run --rm -it -v "$PWD":/workspace -w /workspace ghcr.io/opentofu/
opentofu:latest init

docker run --rm -it -v "$PWD":/workspace -w /workspace ghcr.io/opentofu/
opentofu:latest plan -var 'ssh_key_name=yourKey'

docker run --rm -it -v "$PWD":/workspace -w /workspace ghcr.io/opentofu/
opentofu:latest apply -var 'ssh_key_name=yourKey'
```

## 2 Inventaire dynamique
Pour le fichier inventaire
[cliquez ici](./ansible/openstack.yaml)

## 3 Installation de Kubernetes
### 3.1 Installation des paquets
Comme demandé, les paquets sont installés avec des versions fixes

```
kubernetes_version: "1.30"
kube_version: "1.30.14-1.1"
containerd_version: "1.7.27-1"
pod_network_cidr: "10.244.0.0/16"
```
Pour lander l'installation il faut se placer dans le repertoire `ansible` et lancer cette commande

```bash
ansible-playbook -i openstack.yaml lancement.yml
```
### 3.2 L’installation est organisée en plusieurs rôles Ansible :

#### 3.2.1 Rôle containerd

Configuration du runtime, incluant l’activation de :

`SystemdCgroup=true`

#### 3.2.2 Rôle kubernetes

Installation des paquets Kubernetes avec les versions spécifiées.

#### 3.2.3 Rôle control_plane

Configuration et initialisation du nœud maître (kubeadm init, configuration kubectl, etc.).

#### 3.2.4 Rôle workers

Configuration des nœuds worker et procédure d’adhésion au cluster (kubeadm join).

### 3.3 Lancement du cluster

Une fois les configurations système et l’installation de Kubernetes terminées sur le nœud de contrôle, il est possible d’initialiser le cluster.  
Cette étape s’effectue avec `kubeadm`, en veillant à préciser le CIDR du réseau des pods si vous utilisez Flannel.

#### Initialisation du Control Plane

Pour lancer le cluster depuis le nœud maître :

```bash
sudo kubeadm init --pod-network-cidr=10.244.0.0/16
```

### 3.4 Ajout des Nœuds au Cluster

L'intégration des nœuds **Worker** au cluster a été réalisée en utilisant `kubeadm`.

1.  **Génération de la commande `join` :** Une commande d'adhésion a été générée depuis le nœud du plan de contrôle (`control_plane`) via `kubeadm`.
2.  **Transmission et Exécution :** Cette commande `kubeadm join` a été transmise et exécutée sur tous les nœuds *Worker* via Ansible, permettant à ces derniers de rejoindre le cluster Kubernetes.

---

## 4- Validation du Déploiement du Cluster

La validation confirme le bon fonctionnement du cluster, notamment sa capacité à répartir les charges de travail sur plusieurs machines.

### Procédure de Validation

Pour valider le déploiement, un **ReplicaSet** a été déployé avec un nombre de conteneurs **supérieur** au nombre de nœuds `Worker` disponibles.

Fichiers Nécessaires :
    * Le playbook Ansible : `ansible/deploiment.yml`
    * Le script de déploiement (ReplicaSet) : `replica.sh`
    * Le fichier d'inventaire : `ansible/openstack.yaml`

### Commande de Lancement

Placez-vous dans le répertoire racine `/tp7` pour lancer le déploiement :

```bash
ansible-playbook -i ansible/openstack.yaml deploiment.yml -e "script_name=replica.sh"
```