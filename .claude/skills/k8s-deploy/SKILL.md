---
name: k8s-deploy
description: Manages Kubernetes manifests, Helm charts, and Kustomize overlays for CV Simulator deployment
---

# Kubernetes Deployment Standards

## Structure
infra/
  ├── helm/
  │   └── cv-simulator/
  │       ├── Chart.yaml
  │       ├── values.yaml
  │       ├── values-dev.yaml
  │       ├── values-prod.yaml
  │       └── templates/
  ├── kustomize/
  │   ├── base/
  │   └── overlays/
  │       ├── dev/
  │       └── prod/
  └── k8s/
      ├── namespace.yaml
      └── secrets.yaml

## Rules
- All services have resource limits (CPU + memory)
- Liveness and readiness probes on every deployment
- Secrets managed via Kubernetes secrets, never hardcoded
- Use Kustomize overlays for dev vs prod differences
- Helm values parameterize: replicas, image tag, resource limits
- HPA (Horizontal Pod Autoscaler) for the API service
