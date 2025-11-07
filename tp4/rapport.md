# TP4

### Pour ce debut de TP j'ai commencé par par creer un fichier setup_ufw.yml qui met en place la securite sur toutes les machines.

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
    - name: Réinitialiser les
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
### La prochiane etape c'est créer un playbook qui peut installer et configurer les deux serveurs.
