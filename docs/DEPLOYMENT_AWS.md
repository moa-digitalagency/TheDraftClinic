# Guide de Déploiement AWS / AWS Deployment Guide

**Par MOA Digital Agency LLC**

Ce guide explique comment déployer TheDraftClinic sur Amazon Web Services (AWS).

This guide explains how to deploy TheDraftClinic on Amazon Web Services (AWS).

---

## Architecture Recommandée / Recommended Architecture

```
                    ┌─────────────┐
                    │   Route 53  │
                    │   (DNS)     │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │ CloudFront  │
                    │   (CDN)     │
                    └──────┬──────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
       ┌──────▼──────┐     │     ┌──────▼──────┐
       │     ALB     │     │     │     S3      │
       │  (Load Bal) │     │     │  (Static)   │
       └──────┬──────┘     │     └─────────────┘
              │            │
       ┌──────▼──────┐     │
       │   EC2/ECS   │     │
       │ (App Server)│     │
       └──────┬──────┘     │
              │            │
       ┌──────▼──────┐     │
       │    RDS      │     │
       │ (PostgreSQL)│     │
       └─────────────┘
```

## Option 1: Déploiement EC2 Simple / Simple EC2 Deployment

### 1.1 Créer une Instance EC2 / Create EC2 Instance

1. Aller sur AWS Console > EC2 > Launch Instance
2. Choisir / Choose:
   - AMI: Ubuntu Server 22.04 LTS
   - Instance Type: t2.micro (free tier) ou t2.small
   - Storage: 20GB gp3
   - Security Group: SSH (22), HTTP (80), HTTPS (443)

### 1.2 Créer une Base RDS PostgreSQL / Create RDS PostgreSQL

1. RDS > Create Database
2. Configuration:
   - Engine: PostgreSQL 15
   - Template: Free tier (ou Production)
   - DB Instance: db.t3.micro
   - Storage: 20GB gp2
   - Credentials: Noter le username/password

### 1.3 Configurer le Security Group RDS

- Autoriser le trafic entrant sur port 5432 depuis le Security Group de l'EC2

### 1.4 Déployer sur EC2

```bash
# Se connecter à l'instance / Connect to instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# Suivre le guide VPS depuis la section "Configuration Initiale"
# Follow VPS guide from "Initial Setup" section
```

La seule différence: utilisez l'endpoint RDS pour DATABASE_URL:
```env
DATABASE_URL=postgresql://username:password@your-rds-endpoint:5432/thedraftclinic_db
```

## Option 2: Déploiement avec Elastic Beanstalk / Elastic Beanstalk Deployment

### 2.1 Préparation du Projet

Créer un fichier `.ebextensions/01_packages.config`:
```yaml
packages:
  yum:
    postgresql-devel: []
```

Créer un fichier `Procfile`:
```
web: gunicorn --bind :8000 --workers 3 main:app
```

Créer un fichier `.platform/nginx/conf.d/client_max_body_size.conf`:
```
client_max_body_size 50M;
```

### 2.2 Déploiement via EB CLI

```bash
# Installer EB CLI / Install EB CLI
pip install awsebcli

# Initialiser / Initialize
eb init -p python-3.11 thedraftclinic

# Créer l'environnement / Create environment
eb create thedraftclinic-prod

# Configurer les variables / Configure variables
eb setenv DATABASE_URL=postgresql://... SESSION_SECRET=...

# Déployer / Deploy
eb deploy
```

## Option 3: Déploiement ECS avec Fargate / ECS Fargate Deployment

### 3.1 Créer le Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

COPY . .

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "3", "main:app"]
```

### 3.2 Créer le Repository ECR

```bash
aws ecr create-repository --repository-name thedraftclinic

# Authentification
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com

# Build et push
docker build -t thedraftclinic .
docker tag thedraftclinic:latest YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/thedraftclinic:latest
docker push YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/thedraftclinic:latest
```

### 3.3 Créer le Cluster ECS

Via AWS Console:
1. ECS > Create Cluster > Networking only (Fargate)
2. Create Task Definition > Fargate
3. Create Service avec ALB

## Configuration S3 pour les Uploads

### Créer un Bucket S3

```bash
aws s3 mb s3://thedraftclinic-uploads --region us-east-1
```

### Configurer CORS

```json
[
    {
        "AllowedHeaders": ["*"],
        "AllowedMethods": ["GET", "PUT", "POST"],
        "AllowedOrigins": ["https://votredomaine.com"],
        "ExposeHeaders": []
    }
]
```

### Modifier le Code pour S3

Installer boto3:
```bash
pip install boto3
```

Modifier `services/file_service.py` pour utiliser S3 au lieu du stockage local.

## Configuration CloudFront (CDN)

1. CloudFront > Create Distribution
2. Origin: Votre ALB ou S3
3. SSL: Certificate Manager (ACM)
4. Cache Policy: Optimisé pour Flask

## Monitoring avec CloudWatch

### Métriques à Surveiller / Metrics to Monitor
- EC2: CPU, Memory, Network
- RDS: Connections, CPU, Storage
- ALB: Request count, Latency, 5xx errors

### Alarmes Recommandées / Recommended Alarms
```bash
aws cloudwatch put-metric-alarm \
    --alarm-name "CPU-High" \
    --metric-name CPUUtilization \
    --namespace AWS/EC2 \
    --statistic Average \
    --period 300 \
    --threshold 80 \
    --comparison-operator GreaterThanThreshold \
    --evaluation-periods 2
```

## Coûts Estimés / Estimated Costs

### Configuration Minimale (Free Tier)
- EC2 t2.micro: Gratuit (12 mois)
- RDS db.t3.micro: ~$15/mois
- ALB: ~$16/mois
- **Total: ~$30/mois**

### Configuration Production
- EC2 t3.small: ~$15/mois
- RDS db.t3.small: ~$30/mois
- ALB: ~$16/mois
- CloudFront: ~$10/mois
- S3: ~$5/mois
- **Total: ~$75-100/mois**

## Sécurité AWS / AWS Security

### IAM Best Practices
- Créer des utilisateurs IAM dédiés
- Utiliser des rôles pour EC2/ECS
- Activer MFA sur tous les comptes

### Secrets Manager
```bash
aws secretsmanager create-secret \
    --name thedraftclinic/prod \
    --secret-string '{"DATABASE_URL":"...","SESSION_SECRET":"..."}'
```

### VPC Configuration
- Placer RDS dans un subnet privé
- Utiliser NAT Gateway pour l'accès sortant
- Security Groups restrictifs

---

**MOA Digital Agency LLC** - www.myoneart.com
