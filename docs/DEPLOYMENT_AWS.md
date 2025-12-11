# guide de deploiement aws / aws deployment guide

**par MOA Digital Agency LLC**

Ce guide explique comment deployer TheDraftClinic sur Amazon Web Services (AWS).

This guide explains how to deploy TheDraftClinic on Amazon Web Services (AWS).

---

## architecture recommandee / recommended architecture

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

## option 1: deploiement ec2 simple / simple ec2 deployment

### 1.1 creer une instance ec2 / create ec2 instance

1. aller sur aws console > ec2 > launch instance
2. choisir / choose:
   - ami: Ubuntu Server 22.04 LTS
   - instance type: t2.micro (free tier) ou t2.small
   - storage: 20gb gp3
   - security group: ssh (22), http (80), https (443)

### 1.2 creer une base rds postgresql / create rds postgresql

1. rds > create database
2. configuration:
   - engine: PostgreSQL 15
   - template: free tier (ou production)
   - db instance: db.t3.micro
   - storage: 20gb gp2
   - credentials: noter le username/password

### 1.3 configurer le security group rds

- autoriser le trafic entrant sur port 5432 depuis le security group de l'ec2

### 1.4 deployer sur ec2

```bash
# se connecter a l'instance / connect to instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# suivre le guide vps depuis la section "configuration initiale"
# follow vps guide from "initial setup" section
```

la seule difference: utilisez l'endpoint rds pour DATABASE_URL:
```env
DATABASE_URL=postgresql://username:password@your-rds-endpoint:5432/thedraftclinic_db
```

## option 2: deploiement avec elastic beanstalk / elastic beanstalk deployment

### 2.1 preparation du projet

creer un fichier `.ebextensions/01_packages.config`:
```yaml
packages:
  yum:
    postgresql-devel: []
```

creer un fichier `Procfile`:
```
web: gunicorn --bind :8000 --workers 3 main:app
```

creer un fichier `.platform/nginx/conf.d/client_max_body_size.conf`:
```
client_max_body_size 50M;
```

### 2.2 deploiement via eb cli

```bash
# installer eb cli / install eb cli
pip install awsebcli

# initialiser / initialize
eb init -p python-3.11 thedraftclinic

# creer l'environnement / create environment
eb create thedraftclinic-prod

# configurer les variables / configure variables
eb setenv DATABASE_URL=postgresql://... SESSION_SECRET=...

# deployer / deploy
eb deploy
```

## option 3: deploiement ecs avec fargate / ecs fargate deployment

### 3.1 creer le dockerfile

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

### 3.2 creer le repository ecr

```bash
aws ecr create-repository --repository-name thedraftclinic

# authentification
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com

# build et push
docker build -t thedraftclinic .
docker tag thedraftclinic:latest YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/thedraftclinic:latest
docker push YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/thedraftclinic:latest
```

### 3.3 creer le cluster ecs

via aws console:
1. ecs > create cluster > networking only (fargate)
2. create task definition > fargate
3. create service avec alb

## configuration s3 pour les uploads

### creer un bucket s3

```bash
aws s3 mb s3://thedraftclinic-uploads --region us-east-1
```

### configurer cors

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

### modifier le code pour s3

installer boto3:
```bash
pip install boto3
```

modifier `services/file_service.py` pour utiliser s3 au lieu du stockage local.

## configuration cloudfront (cdn)

1. cloudfront > create distribution
2. origin: votre alb ou s3
3. ssl: certificate manager (acm)
4. cache policy: optimise pour flask

## monitoring avec cloudwatch

### metriques a surveiller / metrics to monitor
- ec2: cpu, memory, network
- rds: connections, cpu, storage
- alb: request count, latency, 5xx errors

### alarmes recommandees / recommended alarms
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

## couts estimes / estimated costs

### configuration minimale (free tier)
- ec2 t2.micro: gratuit (12 mois)
- rds db.t3.micro: ~$15/mois
- alb: ~$16/mois
- total: ~$30/mois

### configuration production
- ec2 t3.small: ~$15/mois
- rds db.t3.small: ~$30/mois
- alb: ~$16/mois
- cloudfront: ~$10/mois
- s3: ~$5/mois
- total: ~$75-100/mois

## securite aws / aws security

### iam best practices
- creer des utilisateurs iam dedies
- utiliser des roles pour ec2/ecs
- activer mfa sur tous les comptes

### secrets manager
```bash
aws secretsmanager create-secret \
    --name thedraftclinic/prod \
    --secret-string '{"DATABASE_URL":"...","SESSION_SECRET":"..."}'
```

### vpc configuration
- placer rds dans un subnet prive
- utiliser nat gateway pour l'acces sortant
- security groups restrictifs

---

**MOA Digital Agency LLC** - www.myoneart.com
