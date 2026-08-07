# 黑马新闻资讯

基于 **FastAPI** 的新闻资讯后端项目，配套【黑马程序员】FastAPI 视频教程。

## 教程视频

[黑马程序员PythonWeb开发：FastAPI从入门到实战视频教程](https://www.bilibili.com/video/BV1zV2QBtE39/?share_source=copy_web&vd_source=df5dd54419af95e5585b85f42092537d)

涵盖：路由、依赖注入、Pydantic、异步编程、ORM、项目拆分、模型训练、部署、接口测试。

> 其中**模型训练、AI 部署**章节未发布，故本项目未开发对应功能。

## 项目状态

✅ **基本完成** — 核心业务功能已开发完成并通过接口测试，可正常运行。

> 📌 **说明**：本项目在实现上参考了 CSDN 作者「2402_84971234」的 [FastAPI 项目系列笔记](https://blog.csdn.net/2402_84971234/category_13162776.html)（即黑马程序员 FastAPI 教程的学习文档）。部分代码的**具体写法与教程不完全一样**（如缓存键设计、数据校验方式、代码组织），但**整体业务逻辑是相同的**。

> ⚠️ **未开发部分**：教程中的 **AI 相关功能（模型训练、AI 部署）** 内容未发布，因此本项目**暂未开发该部分**。

## 项目结构

```
newsHeima/
├── cache/     # 缓存层：Redis 缓存读写（新闻分类、新闻列表等）
├── config/    # 配置：数据库连接、Redis 缓存、全局异常处理器
├── crud/      # 数据访问层：各业务模块的数据库操作
├── models/    # 数据模型：SQLAlchemy ORM 模型
├── routers/   # API 路由：业务接口定义
├── schemas/   # 数据校验：Pydantic 请求/响应模型
├── utils/     # 工具：JWT 认证、密码加密、时间工具
├── sql/       # SQL 脚本：建库建表
├── main.py    # 应用入口
└── test_main.http  # HTTP 接口测试文件
```

## 环境要求

- Python 3.10+
- MySQL 8.0+
- Redis 6.0+（使用新连接协议，需 6.0 及以上版本）

## 依赖安装

```bash
pip install -r requirements.txt
```

依赖已精简为项目实际用到的直接依赖（见 `requirements.txt`），其中 `fastapi[standard]` 会一并安装 uvicorn、python-multipart 等常用组件。

## 快速启动

### 1. 创建虚拟环境

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux / macOS
source .venv/bin/activate
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 初始化数据库

在 MySQL 中执行 `sql/database.sql` 创建数据库和表：

```bash
mysql -u root -p < sql/database.sql
```

### 4. 配置环境变量

复制 `.env.example` 为 `.env` 并填写配置：

```bash
cp .env.example .env
# Windows
copy .env.example .env
```

`.env` 已加入 `.gitignore`，不会提交到仓库，其中包含：

- `SECRET_KEY`：JWT 签名密钥，可用 `python -c "import secrets; print(secrets.token_hex(32))"` 生成
- `DB_USER` / `DB_PASSWORD` / `DB_HOST` / `DB_PORT` / `DB_NAME`：数据库连接信息

### 5. 启动服务

```bash
fastapi dev 
```

访问 API 文档：

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## License

仅供学习使用。
