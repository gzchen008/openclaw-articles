# 数据模型

## 1. ER图设计

```mermaid
erDiagram
    ECIF_CLIENTS_INFO ||--o{ ECIF_CLIENTS_INFO_PRODUCT : "拥有"
    ECIF_CLIENTS_INFO ||--o{ ECIF_CCIF_INFO : "关联"
    ECIF_CLIENTS_INFO ||--o{ ECIF_ADDRESS_INFO : "拥有"
    ECIF_CLIENTS_INFO ||--o{ ECIF_TELEPHONE_INFO : "拥有"
    ECIF_CLIENTS_INFO ||--o{ ECIF_CERTIFICATE_INFO : "拥有"
    ECIF_CLIENTS_INFO ||--o{ ECIF_FACE_FILE : "关联"
    
    ECIF_CLIENTS_INFO {
        string ecif_no PK "个人客户号，系统唯一标识"
        string personal_name "个人姓名"
        string personal_identification_number "身份证号码"
        string personal_identification_type "证件类型"
        string name_status "姓名状态(A-有效,D-无效)"
        datetime created_date "创建时间"
        datetime updated_date "更新时间"
        string remark "备注信息"
        string tb "分表标识"
        string version "版本号，用于乐观锁"
    }
    
    ECIF_CLIENTS_INFO_PRODUCT {
        string ecif_no PK1 "个人客户号"
        string ccif_no PK2 "公司客户号"
        string product_code PK3 "产品代码"
        string status "状态(A-有效,D-无效)"
        string created_by "创建人"
        datetime created_date "创建时间"
        string updated_by "更新人"
        datetime updated_date "更新时间"
    }
    
    ECIF_CCIF_INFO {
        string ecif_no PK1 "个人客户号"
        string ccif_no PK2 "公司客户号"
        string product_code PK3 "产品代码"
        string status "状态(A-有效,D-无效)"
        string created_by "创建人"
        datetime created_date "创建时间"
        string updated_by "更新人"
        datetime updated_date "更新时间"
    }
    
    ECIF_ADDRESS_INFO {
        bigint id PK "主键ID"
        string ecif_no FK "个人客户号"
        string address_type "地址类型(HOME-家庭,WORK-工作)"
        string province_code "省份代码"
        string city_code "城市代码"
        string district_code "区县代码"
        string detail_address "详细地址"
        string postcode "邮政编码"
        datetime created_date "创建时间"
        datetime updated_date "更新时间"
    }
    
    ECIF_TELEPHONE_INFO {
        bigint id PK "主键ID"
        string ecif_no FK "个人客户号"
        string telephone_type "电话类型(MOBILE-手机,LANDLINE-固话)"
        string telephone_number "电话号码"
        string area_code "区号"
        datetime created_date "创建时间"
        datetime updated_date "更新时间"
    }
    
    ECIF_CERTIFICATE_INFO {
        bigint id PK "主键ID"
        string ecif_no FK "个人客户号"
        string certificate_type "证件类型"
        string certificate_number "证件号码"
        datetime issue_date "签发日期"
        datetime expiry_date "到期日期"
        datetime created_date "创建时间"
        datetime updated_date "更新时间"
    }
    
    ECIF_FACE_FILE {
        string ecif_no PK "个人客户号"
        string file_id "文件ID"
        string file_hash "文件哈希值"
        string file_type "文件类型(FACE-人脸,DOC-文档)"
        string status "状态(A-有效,D-无效)"
        datetime created_date "创建时间"
        datetime updated_date "更新时间"
        string created_by "创建人"
    }
```

## 2. 核心表结构说明

### 2.1 客户基本信息表 (ecif_clients_info)

**表描述**: 存储个人客户的基本信息，是ECIF系统的核心数据表。

**主要字段**:
| 字段名 | 数据类型 | 是否主键 | 说明 |
|--------|----------|----------|------|
| ecif_no | VARCHAR(16) | 是 | 个人客户号，系统唯一标识 |
| personal_name | VARCHAR(100) | 否 | 个人姓名 |
| personal_identification_number | VARCHAR(30) | 否 | 身份证号码 |
| personal_identification_type | VARCHAR(10) | 否 | 证件类型 |
| name_status | VARCHAR(1) | 否 | 姓名状态，A-有效，D-失效 |
| created_date | DATETIME | 否 | 创建时间 |
| updated_date | DATETIME | 否 | 更新时间 |
| remark | VARCHAR(500) | 否 | 备注信息 |
| tb | VARCHAR(20) | 否 | 分表标识 |

**索引信息**:
- 主键索引: ecif_no
- 普通索引: personal_identification_number, personal_name, updated_date

### 2.2 客户产品关系表 (ecif_clients_info_product)

**表描述**: 存储个人客户与产品的关系信息，记录客户在各产品的状态。

**主要字段**:
| 字段名 | 数据类型 | 是否主键 | 说明 |
|--------|----------|----------|------|
| ecif_no | VARCHAR(16) | 是(PK1) | 个人客户号 |
| ccif_no | VARCHAR(16) | 是(PK2) | 公司客户号 |
| product_code | VARCHAR(20) | 是(PK3) | 产品代码 |
| status | VARCHAR(1) | 否 | 状态，A-有效，D-失效 |
| created_by | VARCHAR(50) | 否 | 创建人 |
| created_date | DATETIME | 否 | 创建时间 |
| updated_by | VARCHAR(50) | 否 | 更新人 |
| updated_date | DATETIME | 否 | 更新时间 |

**索引信息**:
- 复合主键: (ecif_no, ccif_no, product_code)
- 普通索引: updated_date

### 2.3 ECIF与CCIF关系表 (ecif_ccif_info)

**表描述**: 存储ECIF与CCIF系统的客户关系映射信息。

**主要字段**:
| 字段名 | 数据类型 | 是否主键 | 说明 |
|--------|----------|----------|------|
| ecif_no | VARCHAR(16) | 是(PK1) | 个人客户号 |
| ccif_no | VARCHAR(16) | 是(PK2) | 公司客户号 |
| product_code | VARCHAR(20) | 是(PK3) | 产品代码 |
| status | VARCHAR(1) | 否 | 状态，A-有效，D-失效 |
| created_by | VARCHAR(50) | 否 | 创建人 |
| created_date | DATETIME | 否 | 创建时间 |
| updated_by | VARCHAR(50) | 否 | 更新人 |
| updated_date | DATETIME | 否 | 更新时间 |

**索引信息**:
- 复合主键: (ecif_no, ccif_no, product_code)
- 普通索引: updated_date

### 2.4 客户地址信息表 (ecif_address_info)

**表描述**: 存储客户的地址信息，支持多种地址类型。

**主要字段**:
| 字段名 | 数据类型 | 是否主键 | 说明 |
|--------|----------|----------|------|
| id | BIGINT | 是 | 主键ID |
| ecif_no | VARCHAR(16) | 否 | 个人客户号 |
| address_type | VARCHAR(20) | 否 | 地址类型 |
| province_code | VARCHAR(10) | 否 | 省份代码 |
| city_code | VARCHAR(10) | 否 | 城市代码 |
| district_code | VARCHAR(10) | 否 | 区县代码 |
| detail_address | VARCHAR(200) | 否 | 详细地址 |
| postcode | VARCHAR(10) | 否 | 邮政编码 |
| created_date | DATETIME | 否 | 创建时间 |
| updated_date | DATETIME | 否 | 更新时间 |

**索引信息**:
- 主键索引: id
- 普通索引: ecif_no, address_type, updated_date

### 2.5 客户电话信息表 (ecif_telephone_info)

**表描述**: 存储客户的电话联系方式信息。

**主要字段**:
| 字段名 | 数据类型 | 是否主键 | 说明 |
|--------|----------|----------|------|
| id | BIGINT | 是 | 主键ID |
| ecif_no | VARCHAR(16) | 否 | 个人客户号 |
| telephone_type | VARCHAR(20) | 否 | 电话类型 |
| telephone_number | VARCHAR(20) | 否 | 电话号码 |
| area_code | VARCHAR(10) | 否 | 区号 |
| created_date | DATETIME | 否 | 创建时间 |
| updated_date | DATETIME | 否 | 更新时间 |

**索引信息**:
- 主键索引: id
- 普通索引: ecif_no, telephone_number, updated_date

### 2.6 客户证件信息表 (ecif_certificate_info)

**表描述**: 存储客户的其他证件信息，如护照、军官证等。

**主要字段**:
| 字段名 | 数据类型 | 是否主键 | 说明 |
|--------|----------|----------|------|
| id | BIGINT | 是 | 主键ID |
| ecif_no | VARCHAR(16) | 否 | 个人客户号 |
| certificate_type | VARCHAR(20) | 否 | 证件类型 |
| certificate_number | VARCHAR(50) | 否 | 证件号码 |
| issue_date | DATETIME | 否 | 签发日期 |
| expiry_date | DATETIME | 否 | 到期日期 |
| created_date | DATETIME | 否 | 创建时间 |
| updated_date | DATETIME | 否 | 更新时间 |

**索引信息**:
- 主键索引: id
- 普通索引: ecif_no, certificate_number, updated_date

## 3. 数据关系分析

### 3.1 客户信息聚合关系
- **主表**: ecif_clients_info (客户基本信息)
- **从表**: 
  - ecif_clients_info_product (产品关系)
  - ecif_ccif_info (CCIF关系)
  - ecif_address_info (地址信息)
  - ecif_telephone_info (电话信息)
  - ecif_certificate_info (证件信息)

### 3.2 产品权限关系
- 一个客户(ecif_no)可以关联多个产品(product_code)
- 通过ecif_clients_info_product表建立多对多关系
- 支持同一客户在不同产品下的不同状态

### 3.3 系统间关系映射
- ecif_ccif_info表用于ECIF与CCIF系统间的客户号映射
- 支持一个ECIF客户号对应多个CCIF客户号
- 通过product_code区分不同的产品线映射关系

### 3.4 联系信息管理
- 地址、电话、证件信息通过ecif_no与客户主表关联
- 支持同一客户的多种联系信息类型
- 每条联系信息都有独立的创建和更新时间戳

## 4. 约束和安全

### 4.1 数据完整性约束
- **主键约束**: 所有表都有明确的主键定义
- **非空约束**: 关键字段如ecif_no、created_date等设置NOT NULL
- **默认值约束**: 状态字段默认值为'A'(有效)
- **唯一性约束**: 客户号在主表中唯一

### 4.2 索引策略
- **主键索引**: 自动创建，保证记录唯一性
- **业务索引**: 基于常用查询字段创建索引
- **时间索引**: updated_date字段用于增量查询
- **复合索引**: 多字段组合索引优化复杂查询

### 4.3 数据安全措施
- **敏感信息脱敏**: 身份证号、手机号等敏感字段在应用层脱敏
- **访问控制**: 通过RMB服务接口控制数据访问权限
- **审计日志**: 所有数据变更操作记录审计日志
- **备份策略**: 定期数据库备份，支持数据恢复

### 4.4 性能优化
- **分表策略**: 通过tb字段实现水平分表
- **读写分离**: 支持主从数据库读写分离
- **缓存机制**: Redis缓存热点数据
- **批量操作**: 支持批量数据处理提高效率

## 5. 数据生命周期管理

### 5.1 数据创建
- 新客户信息通过RMB服务接口创建
- 自动生成唯一的ecif_no客户号
- 记录创建时间和创建人信息

### 5.2 数据更新
- 客户信息变更通过专门的更新服务
- 维护updated_date时间戳
- 支持增量数据同步

### 5.3 数据状态管理
- 通过status字段管理数据有效性
- 支持软删除，保留历史数据
- 状态变更记录审计日志

### 5.4 数据归档
- 历史数据定期归档到历史表
- 归档策略基于updated_date时间
- 支持历史数据查询和恢复
