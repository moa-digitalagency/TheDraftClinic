# guide de deploiement vps / vps deployment guide

**par MOA Digital Agency LLC**

Ce guide explique comment deployer TheDraftClinic sur un serveur VPS (Virtual Private Server).

This guide explains how to deploy TheDraftClinic on a VPS (Virtual Private Server).

---

## prerequis / prerequisites

- un vps avec Ubuntu 22.04 LTS / a vps with Ubuntu 22.04 LTS
- acces root ou sudo / root or sudo access
- un nom de domaine (optionnel) / a domain name (optional)
- minimum 1gb ram, 20gb stockage / minimum 1gb ram, 20gb storage

## 1. configuration initiale / initial setup

### mise a jour du systeme / system update

```bash
sudo apt update && sudo apt upgrade -y
```

### installation des dependances / install dependencies

```bash
# python 3.11
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt install -y python3.11 python3.11-venv python3.11-dev

# postgresql
sudo apt install -y postgresql postgresql-contrib

# nginx
sudo apt install -y nginx

# autres outils / other tools
sudo apt install -y git supervisor
```

## 2. configuration postgresql

```bash
# connexion a postgresql / connect to postgresql
sudo -u postgres psql

# creer l'utilisateur et la base / create user and database
CREATE USER thedraftclinic WITH PASSWORD 'votre_mot_de_passe_securise';
CREATE DATABASE thedraftclinic_db OWNER thedraftclinic;
GRANT ALL PRIVILEGES ON DATABASE thedraftclinic_db TO thedraftclinic;
\q
```

## 3. deploiement de l'application / application deployment

### creer un utilisateur dedie / create a dedicated user

```bash
sudo adduser --disabled-password --gecos "" thedraftclinic
sudo usermod -aG www-data thedraftclinic
```

### cloner et configurer / clone and configure

```bash
cd /var/www
sudo git clone https://github.com/your-repo/thedraftclinic.git
sudo chown -R thedraftclinic:www-data thedraftclinic
cd thedraftclinic

# creer l'environnement virtuel / create virtual environment
sudo -u thedraftclinic python3.11 -m venv venv
sudo -u thedraftclinic venv/bin/pip install -r requirements.txt
sudo -u thedraftclinic venv/bin/pip install gunicorn
```

### configuration des variables d'environnement / environment variables

```bash
sudo -u thedraftclinic nano /var/www/thedraftclinic/.env
```

contenu / content:
```env
DATABASE_URL=postgresql://thedraftclinic:votre_mot_de_passe@localhost:5432/thedraftclinic_db
SESSION_SECRET=generez-une-cle-securisee-tres-longue-ici
ADMIN_EMAIL=admin@votredomaine.com
ADMIN_PASSWORD=MotDePasseSecurise123!
```

### initialiser la base / initialize database

```bash
sudo -u thedraftclinic venv/bin/python init_db.py
```

## 4. configuration gunicorn avec supervisor

```bash
sudo nano /etc/supervisor/conf.d/thedraftclinic.conf
```

contenu / content:
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

## 5. configuration nginx

```bash
sudo nano /etc/nginx/sites-available/thedraftclinic
```

contenu / content:
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

## 6. ssl avec let's encrypt (https)

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d votredomaine.com -d www.votredomaine.com
```

## 7. configuration du pare-feu / firewall

```bash
sudo ufw allow OpenSSH
sudo ufw allow 'Nginx Full'
sudo ufw enable
```

## 8. maintenance

### mise a jour de l'application / update application

```bash
cd /var/www/thedraftclinic
sudo -u thedraftclinic git pull
sudo -u thedraftclinic venv/bin/pip install -r requirements.txt
sudo supervisorctl restart thedraftclinic
```

### verifier les logs / check logs

```bash
# logs applicatifs / application logs
tail -f /var/log/thedraftclinic/error.log
tail -f /var/log/thedraftclinic/access.log

# logs nginx
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
```

### sauvegardes postgresql / postgresql backups

```bash
# creer un script de backup / create backup script
sudo nano /var/www/thedraftclinic/backup.sh
```

```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/var/www/thedraftclinic/backups"
mkdir -p $BACKUP_DIR
pg_dump -U thedraftclinic thedraftclinic_db > $BACKUP_DIR/backup_$DATE.sql
# garder les 7 derniers backups / keep last 7 backups
find $BACKUP_DIR -type f -mtime +7 -delete
```

```bash
chmod +x /var/www/thedraftclinic/backup.sh
# ajouter au cron (tous les jours a 2h) / add to cron (daily at 2am)
(crontab -l ; echo "0 2 * * * /var/www/thedraftclinic/backup.sh") | crontab -
```

## depannage / troubleshooting

### l'application ne demarre pas / application won't start
```bash
sudo supervisorctl status thedraftclinic
tail -50 /var/log/thedraftclinic/error.log
```

### erreur 502 bad gateway
```bash
sudo systemctl status nginx
ls -la /var/www/thedraftclinic/thedraftclinic.sock
```

### problemes de permissions / permission issues
```bash
sudo chown -R thedraftclinic:www-data /var/www/thedraftclinic
sudo chmod -R 755 /var/www/thedraftclinic
```

---

**MOA Digital Agency LLC** - www.myoneart.com
