# Distributed-Systems-Lab

A cloud-native frontend application built with Nuxt.js 3, implementing the 12-factor app methodology and designed for distributed systems.

## 🚀 Features

- Server-Side Rendering (SSR) with Nuxt.js 3
- RESTful API integration
- Externalized configuration
- Docker & Kubernetes ready
- Responsive UI for item management
- Health checks and monitoring endpoints

## 📋 Prerequisites

- Node.js 18+ 
- Docker & Docker Compose
- Kubernetes cluster (optional)
- npm or yarn

## 🛠️ Installation & Setup

### Local Development

1. **Clone the repository**
```bash
git clone https://github.com/Yahyasarmini/Distributed-Systems-Lab/tree/main
cd nuxt-app
```

2. **Install dependencies**
```bash
npm install
```

3. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. **Run development server**
```bash
npm run dev
```

The application will be available at `http://localhost:3000`

### Running with Mock API

Start both the frontend and mock API:
```bash
# Terminal 1 - Start mock API
npm run mock-api

# Terminal 2 - Start frontend
npm run dev
```

## 🐳 Docker

### Build Docker Image

```bash
docker build -t items-frontend:latest .
```

### Run with Docker

```bash
docker run -p 3000:3000 \
  -e NUXT_PUBLIC_API_URL=http://your-backend:8080 \
  items-frontend:latest
```

### Docker Compose

Start the entire stack with mock API:

```bash
docker-compose up
```

This will start:
- Frontend on http://localhost:3000
- Mock API on http://localhost:8080

## ☸️ Kubernetes Deployment

### Apply all manifests

```bash
kubectl apply -k k8s/
```

### Or apply individually

```bash
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secret.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/hpa.yaml
kubectl apply -f k8s/ingress.yaml
```

### Verify deployment

```bash
kubectl get all -n items-app
kubectl logs -n items-app -l app=items-frontend
```

## 🔧 Configuration

All configuration is externalized through environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `NODE_ENV` | Environment (development/production) | production |
| `PORT` | Server port | 3000 |
| `HOST` | Server host | 0.0.0.0 |
| `NUXT_PUBLIC_API_URL` | Backend API URL | http://localhost:8080 |
| `NUXT_PUBLIC_APP_NAME` | Application name | Item Management System |
| `API_SECRET` | Secret key for API auth | - |

## 📁 Project Structure

```
nuxt-app/
├── pages/              # Vue pages
│   ├── index.vue      # Home page
│   └── items.vue      # Items management
├── components/         # Vue components
├── plugins/           # Nuxt plugins
├── server/            # Server middleware
├── k8s/               # Kubernetes manifests
├── docker-compose.yml # Docker Compose config
├── Dockerfile         # Docker image definition
└── nuxt.config.ts     # Nuxt configuration
```

## 🧪 Testing

### Manual Testing

1. **Create Item**: Click "Add Item" and fill the form
2. **List Items**: View all items in the grid
3. **Edit Item**: Click "Edit" on any item
4. **Delete Item**: Click "Delete" to remove an item

### API Testing

```bash
# Get all items
curl http://localhost:3000/api/items

# Create new item
curl -X POST http://localhost:3000/api/items \
  -H "Content-Type: application/json" \
  -d '{"name":"Test Item","quantity":10}'

# Update item
curl -X PUT http://localhost:3000/api/items/1 \
  -H "Content-Type: application/json" \
  -d '{"name":"Updated Item","quantity":20}'

# Delete item
curl -X DELETE http://localhost:3000/api/items/1
```

## 📊 Monitoring

### Health Checks

- Liveness: `GET /`
- Readiness: `GET /`

### Logs

```bash
# Docker logs
docker logs items-frontend

# Kubernetes logs
kubectl logs -n items-app -l app=items-frontend -f
```

## 🚢 Production Deployment

1. **Build production image**
```bash
docker build -t your-registry/items-frontend:v1.0.0 .
docker push your-registry/items-frontend:v1.0.0
```

2. **Update Kubernetes deployment**
```bash
kubectl set image deployment/frontend-deployment \
  frontend=your-registry/items-frontend:v1.0.0 \
  -n items-app
```

3. **Monitor rollout**
```bash
kubectl rollout status deployment/frontend-deployment -n items-app
```

## 📝 12-Factor App Implementation

See [12-FACTOR.md](./12-FACTOR.md) for detailed implementation notes.

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 🔗 Links

- [Container Image](https://hub.docker.com/r/yasait01/items-frontend)