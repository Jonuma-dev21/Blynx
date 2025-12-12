# TP8

## 1 Configuration de base

Commande pour envoyer les fichiers

```bash
scp -r postgres/ deployment.sh desinstaller.sh    debian@172.28.100.130:/home/debian
```
Je n'ai pas pu mettre en marche la configuration j'ai mis en place des totalement, mais les pods ont bien été lancé

![image](./pic/replication.png)

la commmande 

```bash
./deployment.sh
```

pour lancer 

et celle la 

```bash
./desinstaller.sh 
```

J'arrive à mettre en place le cluster mais j'ai rencontré quelques difficultés qui m'ont empêché de valider cette partie et les voici :

# Difficultés rencontrés
Je comprends très bien l'idée de la première partie mais le problème c'est que je n'ai pas réussi à valider ma configuration et je pense que cela est dû au fait qu'il faut laisser une marge de temps ou arrêter les fonctionnement de la réplication sur les autres pods afin de donner le temps à la base de données primaiare qu'elle soit prête pour que les autres bases de données peuvent bien réaliser la réplication `Maître-Esclave` et donc concrètement il faut mettre en place une sorte de boucle `until do` en bash avec la condition _Attendre que la base de données primaire soit prête_, puis on peut lancer la configuration des autres pods.