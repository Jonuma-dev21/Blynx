# TP4
## Configurations des machines virtuelles
Les machines virtuelles à ma disposition<br>
1- `vmu1@172.28.101.75` (machine -> juntu)<br>
2- `vmu2@172.28.100.101` (machine -> jobuntu)<br>
3- `vmu3@172.28.100.116` (machine -> jodev)<br>

## 1- 
### Configuration d'un fichier **inventaire**:
Pour ce l'instant on utilisera les deux (vmu2 et vmu3)
Le fichier nommé `inventaire.yml`
```
sgbd:
  hosts:
    vmu2:
      ansible_host: 172.28.100.101
      ansible_user: ubuntu

client:
  hosts:
    vmu3:
      ansible_host: 172.28.100.116
      ansible_user: ubuntu
```

### Sécurisation des instances depuis ma poste locale
 j'ai configurer un fichier setup_ufw.yml qui met en place la securite sur toutes les machines.


```
- name: Installer ufw firewall
  hosts: all
  become: true
  tasks:
    - name: Installer ufw
      apt:
        name: ufw
        state: present
        update_cache: yes
    - name: Réinitialiser les règles d'avant
      ufw:
        state: reset

    - name: Autoriser SSH
      ufw:
        rule: allow
        port: 22
        proto: tcp

    - name: Autoriser les autres ports utiles
      ufw:
        rule: allow
        port: "{{ item }}"
        proto: tcp
      loop:
        - 3306

    - name: Activer le firewall
      ufw:
        state: enabled
        policy: deny
```

Avant la requete
![images](./picture/pic1_1.png)
après la requete
![images](./picture/pic1_2.png)

### Installation et configuration des bases de données avec Ansible.
 La prochiane etape c'est créer un playbook qui peut installer et configurer les deux serveurs en créant un utlisateur pour tester depuis .

lien vers le code `->` [cliquer ici](./lancement.yml)


Avant la requete
![images](./picture/pic1_3.png)
après la requete
![images](./picture/pic1_4.png)

## Partie 2

Pour l'instant j'ai réussi à faire le master-master il me reste à intégrer le proxy

