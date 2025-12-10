# Guide de Déploiement VPS / VPS Deployment Guide

**Par MOA Digital Agency LLC**

Ce guide explique comment déployer TheDraftClinic sur un serveur VPS (Virtual Private Server).

This guide explains how to deploy TheDraftClinic on a VPS (Virtual Private Server).

---

## Prérequis / Prerequisites

- Un VPS avec Ubuntu 22.04 LTS / A VPS with Ubuntu 22.04 LTS
- Accès root ou sudo / Root or sudo access
- Un nom de domaine (optionnel) / A domain name (optional)
- Minimum 1GB RAM, 20GB stockage / Minimum 1GB RAM, 20GB storage

## 1. Configuration Initiale / Initial Setup

### Mise à jour du système / System Update

```bash
sudo apt update && sudo apt upgrade -y
```

### Installation des dépendances / Install Dependencies

```bash
# Python 3.11
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt install -y python3.11 python3.11-venv python3.11-dev

# PostgreSQL
sudo apt install -y postgresql postgresql-contrib

# Nginx
sudo apt install -y nginx

# Autres outils / Other tools
sudo apt install -y git supervisor
```

## 2. Configuration PostgreSQL

```bash
# Connexion à PostgreSQL / Connect to PostgreSQL
sudo -u postgres psql

# Créer l'utilisateur et la base / Create user and database
CREATE USER thedraftclinic WITH PASSWORD 'votre_mot_de_passe_securise';
CREATE DATABASE thedraftclinic_db OWNER thedraftclinic;
GRANT ALL PRIVILEGES ON DATABASE thedraftclinic_db TO thedraftclinic;
\q
```

## 3. Déploiement de l'Application / Application Deployment

### Créer un utilisateur dédié / Create a dedicated user

```bash
sudo adduser --disabled-password --gecos "" thedraftclinic
sudo usermod -aG www-data thedraftclinic
```

### Cloner et configurer / Clone and configure

```bash
cd /var/www
sudo git clone https://github.com/your-repo/thedraftclinic.git
sudo chown -R thedraftclinic:www-data thedraftclinic
cd thedraftclinic

# Créer l'environnement virtuel / Create virtual environment
sudo -u thedraftclinic python3.11 -m venv venv
sudo -u thedraftclinic venv/bin/pip install -r requirements.txt
sudo -u thedraftclinic venv/bin/pip install gunicorn
```

### Configuration des variables d'environnement / Environment Variables

```bash
sudo -u thedraftclinic nano /var/www/thedraftclinic/.env
```

Contenu / Content:
```env
DATABASE_URL=postgresql://thedraftclinic:votre_mot_de_passe@localhost:5432/thedraftclinic_db
SESSION_SECRET=generez-une-cle-securisee-tres-longue-ici
ADMIN_EMAIL=admin@votredomaine.com
ADMIN_PASSWORD=MotDePasseSecurise123!
```

### Initialiser la base / Initialize database

```bash
sudo -u thedraftclinic venv/bin/python init_db.py
```

## 4. Configuration Gunicorn avec Supervisor

```bash
sudo nano /etc/supervisor/conf.d/thedraftclinic.conf
```

Contenu / Content:
```ini
[program:thedraftclinic]
directory=/var/www/thedraftclinic
command=/var/www/thedraftclinic/venv/bin/gunicorn --workers 3 --bind unix:/var/www/thedraftclinic/thedraftclinic.sock main:app
user=thedraftclinic
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
stderr_logfile=/var/log/thedraftclinic/error.log
stdout_logfile=/var/log/thedraftclinic/access.log
environment=FLASK_ENV="production"
```

```bash
sudo mkdir -p /var/log/thedraftclinic
sudo chown -R thedraftclinic:www-data /var/log/thedraftclinic
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start thedraftclinic
```

## 5. Configuration Nginx

```bash
sudo nano /etc/nginx/sites-available/thedraftclinic
```

Contenu / Content:
```nginx
server {
    listen 80;
    server_name votredomaine.com www.votredomaine.com;

    location /static {
        alias /var/www/thedraftclinic/static;
        expires 30d;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/thedraftclinic/thedraftclinic.sock;
    }

    client_max_body_size 50M;
}
```

```bash
sudo ln -s /etc/nginx/sites-available/thedraftclinic /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## 6. SSL avec Let's Encrypt (HTTPS)

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d votredomaine.com -d www.votredomaine.com
```

## 7. Configuration du Pare-feu / Firewall

```bash
sudo ufw allow OpenSSH
sudo ufw allow 'Nginx Full'
sudo ufw enable
```

## 8. Maintenance

### Mise à jour de l'application / Update Application

```bash
cd /var/www/thedraftclinic
sudo -u thedraftclinic git pull
sudo -u thedraftclinic venv/bin/pip install -r requirements.txt
sudo supervisorctl restart thedraftclinic
```

### Vérifier les logs / Check Logs

```bash
# Logs applicatifs / Application logs
tail -f /var/log/thedraftclinic/error.log
tail -f /var/log/thedraftclinic/access.log

# Logs Nginx
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
```

### Sauvegardes PostgreSQL / PostgreSQL Backups

```bash
# Créer un script de backup / Create backup script
sudo nano /var/www/thedraftclinic/backup.sh
```

```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/var/www/thedraftclinic/backups"
mkdir -p $BACKUP_DIR
pg_dump -U thedraftclinic thedraftclinic_db > $BACKUP_DIR/backup_$DATE.sql
# Garder les 7 derniers backups / Keep last 7 backups
find $BACKUP_DIR -type f -mtime +7 -delete
```

```bash
chmod +x /var/www/thedraftclinic/backup.sh
# Ajouter au cron (tous les jours à 2h) / Add to cron (daily at 2am)
(crontab -l ; echo "0 2 * * * /var/www/thedraftclinic/backup.sh") | crontab -
```

## Dépannage / Troubleshooting

### L'application ne démarre pas / Application won't start
```bash
sudo supervisorctl status thedraftclinic
tail -50 /var/log/thedraftclinic/error.log
```

### Erreur 502 Bad Gateway
```bash
sudo systemctl status nginx
ls -la /var/www/thedraftclinic/thedraftclinic.sock
```

### Problèmes de permissions / Permission issues
```bash
sudo chown -R thedraftclinic:www-data /var/www/thedraftclinic
sudo chmod -R 755 /var/www/thedraftclinic
```

---

**MOA Digital Agency LLC** - www.myoneart.com
