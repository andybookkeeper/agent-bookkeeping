# Deployment Guide

## Production Deployment

This guide covers deploying the Bookkeeping Platform to production.

## Pre-Deployment Checklist

- [ ] Environment variables configured (.env)
- [ ] Database backups configured
- [ ] SSL certificates ready
- [ ] Domain name configured
- [ ] Monitoring and alerting set up
- [ ] Logging aggregation configured
- [ ] Security scanning complete

## AWS Deployment (Recommended)

### Infrastructure Requirements

1. **ECS/Fargate** - Container orchestration
   - Backend service (FastAPI)
   - Celery worker service
   - Frontend service (Next.js)

2. **RDS PostgreSQL** - Managed database
   - Multi-AZ deployment
   - Automated backups
   - Read replicas for scaling

3. **ElastiCache Redis** - Managed cache/queue
   - Multi-AZ deployment
   - Automatic failover

4. **ALB** - Load balancer
   - SSL termination
   - CORS headers
   - Request routing

5. **S3** - Object storage
   - Receipt storage
   - Static assets

### Deployment Steps

1. **Build and Push Docker Images**
```bash
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com

docker build -f Dockerfile.backend -t bookkeeping-backend:latest .
docker tag bookkeeping-backend:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/bookkeeping-backend:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/bookkeeping-backend:latest

docker build -f frontend/Dockerfile -t bookkeeping-frontend:latest frontend/
docker tag bookkeeping-frontend:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/bookkeeping-frontend:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/bookkeeping-frontend:latest
```

2. **Update ECS Task Definitions**
   - Set database connection string to RDS endpoint
   - Set Redis URL to ElastiCache endpoint
   - Configure environment variables

3. **Deploy Services**
   - Update ECS service with new task definition
   - Monitor health checks
   - Verify traffic routing

4. **Run Database Migrations**
```bash
# SSH into backend container or use task override
python -c "from backend.migrations import init_database; init_database()"
```

5. **Configure Auto-scaling**
   - Set up target tracking policies
   - Configure CPU/memory thresholds
   - Test scaling behavior under load

## Google Cloud Deployment

### Using Cloud Run + Cloud SQL + Memorystore

```bash
# Build and push to Container Registry
gcloud builds submit --tag gcr.io/<project>/bookkeeping-backend

# Deploy backend
gcloud run deploy bookkeeping-backend \
  --image gcr.io/<project>/bookkeeping-backend \
  --platform managed \
  --region us-central1 \
  --set-env-vars DATABASE_URL="postgresql://...",REDIS_URL="redis://..."

# Deploy frontend
gcloud run deploy bookkeeping-frontend \
  --image gcr.io/<project>/bookkeeping-frontend \
  --platform managed \
  --region us-central1 \
  --set-env-vars NEXT_PUBLIC_API_URL="https://bookkeeping-backend-..."
```

## Kubernetes Deployment

### Using Helm

1. Create Helm chart structure
2. Update values.yaml with production settings
3. Deploy using:
```bash
helm install bookkeeping ./helm \
  -f values-production.yaml
```

## Docker Swarm Deployment

```bash
# Initialize swarm
docker swarm init

# Deploy stack
docker stack deploy -c docker-compose.prod.yml bookkeeping
```

## Environment Configuration

### Required Environment Variables

```bash
# Database
DATABASE_URL=postgresql://user:pass@host:5432/bookkeeping

# Redis
REDIS_URL=redis://host:6379/0

# Security
ALLOWED_ORIGINS=https://app.example.com

# API
NEXT_PUBLIC_API_URL=https://api.example.com

# Email (for future features)
SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USER=user@example.com
SMTP_PASSWORD=pass
```

## SSL/TLS Certificate

Use Let's Encrypt with:
- **AWS**: ACM (AWS Certificate Manager)
- **GCP**: Cloud Armor + SSL Policy
- **Manual**: Let's Encrypt with certbot

## Database Backups

### Automated Backups
- PostgreSQL automatic backups (daily)
- S3 backup storage
- Point-in-time recovery enabled

### Restore Procedure
```bash
# Using AWS RDS
aws rds restore-db-instance-from-db-snapshot \
  --db-instance-identifier bookkeeping-restored \
  --db-snapshot-identifier snapshot-id

# Using pg_dump/pg_restore
pg_dump -h host -U user bookkeeping > backup.sql
psql -h new-host -U user bookkeeping < backup.sql
```

## Monitoring & Logging

### CloudWatch (AWS)
- Application logs → CloudWatch Logs
- Custom metrics → CloudWatch Metrics
- Alarms → SNS notifications

### ELK Stack (Self-hosted)
- Elasticsearch for storage
- Logstash for ingestion
- Kibana for visualization

### Monitoring Metrics
- API response times
- Database query performance
- Celery task success/failure rates
- Memory and CPU usage
- Disk space
- Network I/O

## Security Hardening

1. **Network Security**
   - VPC with private subnets
   - Security groups with restricted inbound rules
   - WAF (Web Application Firewall)

2. **Database Security**
   - Encrypted connections (SSL)
   - Encrypted at rest
   - Access control lists
   - Regular security patching

3. **Application Security**
   - HTTPS only
   - CORS properly configured
   - Rate limiting
   - Input validation
   - CSRF protection
   - SQL injection prevention

4. **Secrets Management**
   - AWS Secrets Manager or similar
   - Rotate credentials regularly
   - Don't commit secrets to git

## Performance Optimization

1. **Database**
   - Connection pooling
   - Query optimization
   - Indexing strategy
   - Read replicas for scaling

2. **Caching**
   - Redis caching layer
   - HTTP caching headers
   - CDN for static assets

3. **API**
   - Pagination for large result sets
   - Query optimization
   - Compression (gzip)

4. **Frontend**
   - Code splitting
   - Image optimization
   - CDN for assets
   - Service workers for offline support

## Disaster Recovery

### Recovery Time Objective (RTO)
- Target: < 1 hour
- Database: Automated RDS failover (~30 seconds)
- Application: ECS auto-recovery (~5 minutes)

### Recovery Point Objective (RPO)
- Database: < 5 minutes (automated backups)
- Implement transaction logs replication

### Testing
- Monthly failover tests
- Backup restoration tests
- Load testing under failure scenarios

## Rollback Procedure

1. **Identify Issue**
   - Monitor for errors
   - Check logs
   - Verify metrics

2. **Rollback Steps**
   ```bash
   # ECS: Deploy previous task definition
   aws ecs update-service \
     --cluster bookkeeping \
     --service backend \
     --task-definition bookkeeping-backend:previous-version
   ```

3. **Post-Rollback**
   - Verify service health
   - Monitor for issues
   - Communicate status

## Support & Maintenance

### Scheduled Maintenance
- Weekly: Log rotation
- Monthly: Security updates
- Quarterly: Performance optimization

### On-Call Support
- Monitoring alerts → On-call engineer
- Incident response procedures
- Post-incident reviews

## Additional Resources

- [AWS ECS Best Practices](https://docs.aws.amazon.com/AmazonECS/)
- [PostgreSQL Production Guide](https://www.postgresql.org/)
- [Redis Production Guide](https://redis.io/topics/admin)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
