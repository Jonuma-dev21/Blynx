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

## 4 Validation

Il suffit de ce mettre dans le repertoire `/tp7` et lancer cette commande, inspirer du `tp6`

```bash
ansible-playbook -i ansible/openstack.yaml deploiment.yml -e "script_name=replica.sh"
```
