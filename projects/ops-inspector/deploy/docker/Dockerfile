# 构建阶段
FROM golang:1.21-alpine AS builder

WORKDIR /app

# 安装依赖
RUN apk add --no-cache git

# 复制依赖文件
COPY go.mod go.sum ./
RUN go mod download

# 复制源码
COPY . .

# 构建二进制文件
RUN CGO_ENABLED=0 GOOS=linux go build -ldflags="-w -s" -o bin/api ./cmd/api
RUN CGO_ENABLED=0 GOOS=linux go build -ldflags="-w -s" -o bin/scheduler ./cmd/scheduler
RUN CGO_ENABLED=0 GOOS=linux go build -ldflags="-w -s" -o bin/worker ./cmd/worker
RUN CGO_ENABLED=0 GOOS=linux go build -ldflags="-w -s" -o bin/migrate ./cmd/migrate

# 运行阶段
FROM alpine:latest

WORKDIR /app

# 安装基础依赖
RUN apk add --no-cache ca-certificates tzdata

# 创建非root用户
RUN adduser -D -u 1000 opsinspector

# 复制二进制文件
COPY --from=builder /app/bin/* /usr/local/bin/

# 复制配置文件
COPY --from=builder /app/configs /app/configs

# 创建插件目录
RUN mkdir -p /app/plugins

# 设置权限
RUN chown -R opsinspector:opsinspector /app

USER opsinspector

# 健康检查
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:8080/health || exit 1

EXPOSE 8080 9090 9091

CMD ["api"]
