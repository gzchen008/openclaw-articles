.PHONY: all build clean test lint docker-build docker-run k8s-deploy k8s-delete dev migrate deps

# 变量
BINARY_NAME=opsinspector
DOCKER_IMAGE=opsinspector:latest
K8S_NAMESPACE=opsinspector

# 默认目标
all: build

# 安装依赖
deps:
	go mod download
	go mod tidy

# 构建所有二进制文件
build: deps
	mkdir -p bin
	CGO_ENABLED=0 go build -ldflags="-w -s" -o bin/api ./cmd/api
	CGO_ENABLED=0 go build -ldflags="-w -s" -o bin/scheduler ./cmd/scheduler
	CGO_ENABLED=0 go build -ldflags="-w -s" -o bin/worker ./cmd/worker
	CGO_ENABLED=0 go build -ldflags="-w -s" -o bin/migrate ./cmd/migrate

# 运行测试
test:
	go test -v ./...

# 代码检查
lint:
	golangci-lint run ./...

# 清理
 clean:
	rm -rf bin/
	go clean

# 开发模式运行（使用内存队列）
dev:
	go run ./cmd/api --config configs/config.yaml

# 数据库迁移
migrate:
	go run ./cmd/migrate --config configs/config.yaml

# Docker 构建
docker-build:
	docker build -t $(DOCKER_IMAGE) -f deploy/docker/Dockerfile .

# Docker 运行
docker-run:
	docker run -d \
		--name opsinspector \
		-p 8080:8080 \
		-p 9090:9090 \
		-p 9091:9091 \
		-e DATABASE_DSN="root:opsinspector@tcp(host.docker.internal:3306)/opsinspector?charset=utf8mb4&parseTime=True&loc=Local" \
		$(DOCKER_IMAGE)

# 停止 Docker
docker-stop:
	docker stop opsinspector || true
	docker rm opsinspector || true

# Kubernetes 部署 MySQL
k8s-mysql:
	kubectl apply -f deploy/kubernetes/mysql.yaml

# Kubernetes 部署应用
k8s-deploy: docker-build
	kind load docker-image $(DOCKER_IMAGE) || true
	kubectl apply -f deploy/kubernetes/opsinspector.yaml

# Kubernetes 删除部署
k8s-delete:
	kubectl delete -f deploy/kubernetes/opsinspector.yaml --ignore-not-found=true

# 查看日志
logs:
	kubectl logs -n $(K8S_NAMESPACE) -l app=opsinspector-api --tail=100 -f

# 端口转发
port-forward:
	kubectl port-forward -n $(K8S_NAMESPACE) svc/opsinspector-api 8080:8080

# 创建示例巡检任务
create-example:
	curl -X POST http://localhost:8080/api/v1/inspections \
		-H "Content-Type: application/json" \
		-d '{"name":"example-http-check","type":"http","schedule":"*/5 * * * *","config":{"url":"https://httpbin.org/get","method":"GET","timeout":10},"notify_channels":["webhook"]}'

# 查看 API 文档
api-docs:
	@echo "API 文档: http://localhost:8080/swagger/index.html"

# 健康检查
health:
	curl http://localhost:8080/health

# 指标
metrics:
	curl http://localhost:9091/metrics
