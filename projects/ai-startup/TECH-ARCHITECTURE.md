# 技术架构设计文档

**项目名称**：小红书文案AI  
**文档版本**：v1.0  
**创建日期**：2026-02-07  
**最后更新**：2026-02-07

---

## 🎯 设计目标

1. **低成本启动**：首月运营成本 < ¥500
2. **快速迭代**：支持1周MVP上线
3. **可扩展性**：支持1000→10000用户平滑扩容
4. **稳定可靠**：99.9%可用性，数据安全

---

## 🏗️ 技术栈选型

### 1. 前端技术栈

| 技术 | 选择 | 理由 | 替代方案 |
|-----|------|------|---------|
| **框架** | Next.js 14 (App Router) | 全栈能力、SSR优化、部署便利 | Nuxt.js、React SPA |
| **样式** | Tailwind CSS | 快速开发、一致性、包体积小 | styled-components、CSS Modules |
| **UI组件** | shadcn/ui + Radix | 高质量组件、可定制、无障碍 | Ant Design、MUI |
| **状态管理** | Zustand | 轻量、TypeScript友好 | Redux、Jotai |
| **表单处理** | React Hook Form | 性能好、验证集成 | Formik |
| **HTTP客户端** | TanStack Query | 缓存、乐观更新、离线支持 | SWR、axios |

**选择理由**：
- Next.js 14的App Router提供更好的性能和SEO
- shadcn/ui组件可直接复制到项目，无额外依赖
- 整套栈都是TypeScript原生，类型安全

### 2. 后端技术栈

| 技术 | 选择 | 理由 | 替代方案 |
|-----|------|------|---------|
| **运行时** | Node.js 20 | Next.js原生支持、生态丰富 | Deno、Bun |
| **API路由** | Next.js API Routes | 全栈框架、部署简单 | Express、Fastify |
| **数据库** | Supabase (PostgreSQL) | 免费额度高、实时订阅、Auth集成 | PlanetScale、Railway |
| **ORM** | Prisma | 类型安全、迁移管理、查询优化 | Drizzle、TypeORM |
| **缓存** | Upstash Redis | 无服务器、按量付费、低延迟 | Vercel KV、自托管 |
| **搜索** | Algolia / Meilisearch | 全文搜索、 typo容错 | 数据库like查询 |

**选择理由**：
- Supabase免费层足够支撑10000用户
- Prisma的迁移系统确保数据库schema安全演进
- Upstash Redis用于限流、缓存热点数据

### 3. AI/LLM技术栈

| 技术 | 选择 | 理由 | 成本估算 |
|-----|------|------|---------|
| **主模型** | OpenAI GPT-4o-mini | 性价比高、中文好 | ~¥0.01-0.03/次 |
| **备用模型** | Claude 3.5 Haiku | 备用方案、创意好 | ~¥0.02-0.04/次 |
| **国内备用** | Moonshot Kimi / GLM-4 | 合规、无需代理 | ~¥0.01-0.02/次 |
| **Prompt管理** | Vercel AI SDK | 流式响应、工具调用 | 免费 |
| **提示词版本** | 代码管理 | Git追踪、A/B测试 | - |

**模型选择策略**：
```typescript
// 模型路由策略
const modelRouter = {
  // 默认：性价比最优
  default: 'gpt-4o-mini',
  
  // 高质量需求：创意文案
  creative: 'claude-3.5-haiku',
  
  // 国内用户：合规访问
  china: 'moonshot-kimi',
  
  // 降级方案：网络问题自动切换
  fallback: 'glm-4-flash'
}
```

### 4. 基础设施

| 服务 | 选择 | 用途 | 成本 |
|-----|------|------|------|
| **托管** | Vercel Pro | 前端+API、CDN、分析 | $20/月 |
| **域名** | Cloudflare | 域名注册、DNS、安全防护 | ~$10/年 |
| **存储** | Cloudflare R2 | 图片/文件存储、免 egress 费 | 免费额度 |
| **监控** | Vercel Analytics + Logflare | 性能监控、日志 | 免费额度 |
| **错误追踪** | Sentry | 错误监控、性能追踪 | 免费额度 |

---

## 💰 成本详细测算

### 月度成本预算（按用户规模）

#### 阶段1：0-1000用户（MVP期）

| 项目 | 服务 | 预估成本 | 说明 |
|-----|------|---------|------|
| **服务器** | Vercel Pro | ¥140/月 | 基础版免费，但Pro更稳定 |
| **数据库** | Supabase Free | ¥0/月 | 500MB存储、无限请求 |
| **缓存** | Upstash Free | ¥0/月 | 10K请求/天 |
| **LLM API** | OpenAI | ¥150-300/月 | 按1000用户、3次/天计算 |
| **域名** | Cloudflare | ¥8/月 | 均摊年费 |
| **监控** | Sentry免费版 | ¥0/月 | 5000错误/月 |
| **支付** | 微信/支付宝 | 手续费 | 收入0.6%手续费 |
| **总计** | - | **~¥300-450/月** | - |

#### 阶段2：1000-5000用户（增长期）

| 项目 | 服务 | 预估成本 | 说明 |
|-----|------|---------|------|
| **服务器** | Vercel Pro | ¥140/月 | 可能需要额外带宽 |
| **数据库** | Supabase Pro | ¥140/月 | 8GB存储、100K连接 |
| **缓存** | Upstash Pro | ¥70/月 | 100K请求/天 |
| **LLM API** | OpenAI + 备用 | ¥1500-3000/月 | 用户增长+使用频次提升 |
| **搜索** | Algolia/Meilisearch | ¥350/月 | 全文搜索功能 |
| **CDN** | Cloudflare Pro | ¥140/月 | 更大缓存、WAF |
| **总计** | - | **~¥2200-3700/月** | - |

#### 阶段3：5000-10000用户（规模化）

| 项目 | 服务 | 预估成本 | 说明 |
|-----|------|---------|------|
| **服务器** | Vercel Enterprise | ¥700/月 | 企业级支持 |
| **数据库** | Supabase Team | ¥420/月 | 更大存储、只读副本 |
| **缓存** | Upstash Pro | ¥210/月 | 更高QPS |
| **LLM API** | 混合策略 | ¥5000-10000/月 | 自建缓存降低API调用 |
| **监控** | Sentry Team | ¥560/月 | 更大配额 |
| **总计** | - | **~¥6900-12000/月** | - |

### 单用户成本分析

```
单用户月度成本 = 基础设施成本/用户数 + LLM调用成本

阶段1（1000用户）:
- 基础设施：¥450/1000 = ¥0.45/用户
- LLM调用：假设3次/天 × 30天 × ¥0.02 = ¥1.8/用户
- 总计：~¥2.25/用户/月

阶段2（5000用户）:
- 基础设施：¥3700/5000 = ¥0.74/用户
- LLM调用：假设10次/月 × ¥0.015 = ¥0.15/用户（规模效应）
- 总计：~¥0.89/用户/月

盈亏平衡点：
- 会员价格：¥19.9/月
- 毛利率：(19.9 - 2.25) / 19.9 = 88.7%
- 月留存率60%，LTV = 19.9 × 3.3 = ¥65.7
- LTV/CAC > 3（健康SaaS指标）
```

---

## 🗄️ 数据库设计

### 核心数据模型

```prisma
// schema.prisma

generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

// 用户表
model User {
  id            String    @id @default(cuid())
  email         String?   @unique
  phone         String?   @unique
  wechatOpenId  String?   @unique
  name          String?
  avatar        String?
  membership    MembershipType @default(FREE)
  credits       Int       @default(3)  // 免费额度
  createdAt     DateTime  @default(now())
  updatedAt     DateTime  @updatedAt
  
  generations   Generation[]
  savedCopies   SavedCopy[]
  orders        Order[]
  
  @@map("users")
}

enum MembershipType {
  FREE
  PRO
  ENTERPRISE
}

// 文案生成记录
model Generation {
  id          String   @id @default(cuid())
  userId      String
  user        User     @relation(fields: [userId], references: [id])
  
  prompt      String   // 用户输入
  platform    Platform // 小红书/抖音/公众号
  style       Style    // 种草/测评/干货
  
  results     Json     // 生成的10条文案
  selectedIndex Int?   // 用户选择的文案索引
  
  creditCost  Int      @default(1)
  createdAt   DateTime @default(now())
  
  @@index([userId, createdAt])
  @@map("generations")
}

enum Platform {
  XIAOHONGSHU
  DOUYIN
  WECHAT
  WEIBO
}

enum Style {
  ZHONGCAO    // 种草
  CEPING      // 测评
  GANHUO      // 干货
  GUSHI       // 故事
}

// 收藏的文案
model SavedCopy {
  id          String   @id @default(cuid())
  userId      String
  user        User     @relation(fields: [userId], references: [id])
  
  title       String
  content     String   @db.Text
  tags        String[]
  platform    Platform
  
  folder      String?  // 收藏夹分类
  createdAt   DateTime @default(now())
  
  @@index([userId, createdAt])
  @@map("saved_copies")
}

// 订单表
model Order {
  id          String   @id @default(cuid())
  userId      String
  user        User     @relation(fields: [userId], references: [id])
  
  plan        String   // pro_monthly, pro_yearly
  amount      Decimal  @db.Decimal(10, 2)
  currency    String   @default("CNY")
  
  status      OrderStatus @default(PENDING)
  paymentMethod String?
  paidAt      DateTime?
  
  createdAt   DateTime @default(now())
  
  @@index([userId, createdAt])
  @@map("orders")
}

enum OrderStatus {
  PENDING
  PAID
  FAILED
  REFUNDED
}

// 爆款模板库
model Template {
  id          String   @id @default(cuid())
  name        String
  structure   String   @db.Text  // 结构描述
  platform    Platform
  category    String   // 美妆/穿搭/美食等
  
  usageCount  Int      @default(0)
  rating      Float    @default(5.0)
  
  isPremium   Boolean  @default(false)
  createdAt   DateTime @default(now())
  
  @@index([platform, category])
  @@map("templates")
}

// 违禁词库
model ForbiddenWord {
  id          String   @id @default(cuid())
  word        String   @unique
  severity    Severity // 严重程度
  suggestion  String?  // 替换建议
  platform    Platform? // 特定平台
  
  @@map("forbidden_words")
}

enum Severity {
  LOW      // 建议修改
  MEDIUM   // 可能影响推荐
  HIGH     // 可能限流
  CRITICAL // 可能封号
}
```

### 索引策略

```sql
-- 高频查询优化
CREATE INDEX idx_generations_user_created ON generations(user_id, created_at DESC);
CREATE INDEX idx_saved_copies_user_folder ON saved_copies(user_id, folder);
CREATE INDEX idx_templates_platform_category ON templates(platform, category) WHERE is_premium = false;

-- 全文搜索（PostgreSQL）
CREATE INDEX idx_generations_prompt_search ON generations USING gin(to_tsvector('chinese', prompt));
```

---

## 🔐 安全设计

### 1. 认证与授权

```typescript
// 使用NextAuth.js + Supabase Auth
// 支持：邮箱登录、微信扫码、手机号

// 权限模型
const permissions = {
  FREE: {
    dailyGenerations: 3,
    templates: ['basic'],
    platforms: ['xiaohongshu'],
    features: ['generate', 'save']
  },
  PRO: {
    dailyGenerations: Infinity,
    templates: ['all'],
    platforms: ['xiaohongshu', 'douyin', 'wechat', 'weibo'],
    features: ['generate', 'save', 'style-learn', 'templates']
  }
}
```

### 2. API安全

```typescript
// 限流策略
const rateLimits = {
  // 免费用户：3次/天
  FREE: { requests: 3, window: '1d' },
  
  // 付费用户：100次/小时
  PRO: { requests: 100, window: '1h' },
  
  // IP级别：防止滥用
  IP: { requests: 10, window: '1m' }
}

// 敏感操作验证
const sensitiveOperations = [
  'deleteAccount',
  'changeMembership',
  'exportData'
]
```

### 3. 数据安全

- **传输加密**：HTTPS强制、HSTS头部
- **存储加密**：数据库敏感字段加密
- **备份策略**：每日自动备份、保留7天
- **隐私合规**：用户可导出/删除数据（GDPR/个人信息保护法）

---

## 📊 监控与可观测性

### 关键指标

| 指标类型 | 指标名称 | 目标值 | 告警阈值 |
|---------|---------|--------|---------|
| **性能** | API响应时间 | < 500ms | > 1s |
| **性能** | 首屏加载时间 | < 2s | > 3s |
| **可用性** | 服务可用率 | 99.9% | < 99% |
| **业务** | 日活用户(DAU) | - | 下降20% |
| **业务** | 付费转化率 | > 3% | < 2% |
| **业务** | LLM调用成功率 | > 99% | < 95% |

### 告警规则

```yaml
alerts:
  - name: 高错误率
    condition: error_rate > 1%
    duration: 5m
    severity: critical
    
  - name: LLM API故障
    condition: llm_success_rate < 90%
    duration: 2m
    severity: critical
    action: 自动切换备用模型
    
  - name: 数据库慢查询
    condition: slow_query_count > 10/min
    duration: 10m
    severity: warning
```

---

## 🚀 部署流程

### CI/CD Pipeline

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v2
      - name: Run tests
        run: pnpm test
      - name: Type check
        run: pnpm type-check
      - name: Lint
        run: pnpm lint

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Deploy to Vercel
        uses: vercel/action-deploy@v1
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
```

### 环境管理

| 环境 | 用途 | 数据库 | LLM模型 |
|-----|------|--------|---------|
| **Local** | 本地开发 | Supabase本地 | Mock/测试key |
| **Preview** | PR预览 | Supabase分支 | GPT-3.5 |
| **Staging** | 预发布 | Supabase staging | GPT-4o-mini |
| **Production** | 生产 | Supabase prod | GPT-4o-mini + 备用 |

---

## 📝 POC原型清单（3天内完成）

### Day 1：基础架构

- [ ] 项目初始化（Next.js + shadcn/ui）
- [ ] 数据库schema设计 + Prisma配置
- [ ] 基础路由结构搭建
- [ ] Vercel部署配置

### Day 2：核心功能

- [ ] AI文案生成API（对接OpenAI）
- [ ] 前端生成界面
- [ ] 小红书Prompt工程
- [ ] 结果展示组件

### Day 3：闭环验证

- [ ] 用户认证（简化版）
- [ ] 免费额度限制
- [ ] 文案复制功能
- [ ] 基础监控

**POC成功标准**：
- ✅ 能生成小红书风格文案
- ✅ 响应时间 < 3秒
- ✅ 演示给3个潜在用户并获得反馈

---

## ⚠️ 技术风险评估

| 风险 | 概率 | 影响 | 应对策略 |
|-----|------|------|---------|
| LLM API不可用 | 中 | 高 | 多模型备用、降级方案 |
| 成本超预算 | 中 | 中 | 缓存策略、用量监控 |
| 数据库性能瓶颈 | 低 | 高 | 索引优化、读写分离 |
| 安全漏洞 | 低 | 高 | 依赖自动更新、安全审计 |
| 微信审核不通过 | 中 | 高 | 提前准备材料、备选方案 |

---

## 🔮 未来技术演进

### 3个月
- 引入Redis缓存降低API成本
- 自建Prompt版本管理系统
- A/B测试框架

### 6个月
- 考虑模型微调（降低长期成本）
- 实时协作功能（WebSocket）
- 移动端PWA

### 12个月
- 多区域部署（降低延迟）
- 私有化部署方案（企业版）
- AI模型训练pipeline

---

*文档版本：v1.0*  
*下次更新：根据MVP反馈迭代*
