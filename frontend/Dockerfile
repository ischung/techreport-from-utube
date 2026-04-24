# Frontend — multi-stage build
# Stage 1: install dependencies + build static assets with Vite
# Stage 2: serve via nginx:alpine

FROM node:20-alpine AS builder
WORKDIR /app

RUN corepack enable && corepack prepare pnpm@9 --activate

COPY package.json ./
# pnpm-lock.yaml is optional until a lockfile lands (issue #2 deferred it)
COPY pnpm-lock.yaml* ./

RUN pnpm install --frozen-lockfile || pnpm install

COPY . .
RUN pnpm build

FROM nginx:alpine AS runtime
ENV LANG=C.UTF-8 \
    LC_ALL=C.UTF-8
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget -q --spider http://localhost/ || exit 1
CMD ["nginx", "-g", "daemon off;"]
