# 黑马新闻资讯

基于 **FastAPI** 的新闻资讯后端项目，配套【黑马程序员】FastAPI 视频教程。

## 教程视频

[黑马程序员PythonWeb开发：FastAPI从入门到实战视频教程](https://www.bilibili.com/video/BV1zV2QBtE39/?share_source=copy_web&vd_source=df5dd54419af95e5585b85f42092537d)

涵盖：路由、依赖注入、Pydantic、异步编程、ORM、项目拆分、模型训练、部署、接口测试。

## 项目状态

🚧 **开发中** — 目前仅完成项目骨架搭建，业务功能逐步开发中。

## 项目结构

```
newsHeima/
├── crud/              # 数据访问层（CRUD操作）
├── models/            # 数据模型定义（SQLAlchemy ORM）
├── routers/           # API路由定义
├── schemas/           # 数据验证模型（Pydantic）
├── utils/             # 工具函数
├── config/            # 配置文件
│   ├── db_conf.py     # 数据库配置
│   └── cache_conf.py  # Redis缓存配置
├── sql/               # SQL脚本
│   └── database.sql   # 数据库建表脚本
├── main.py            # 应用入口
└── test_main.http     # HTTP接口测试文件
```

## 环境要求

- Python 3.10+
- MySQL 8.0+
- Redis（可选，用于缓存）

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

### 4. 配置数据库连接

编辑 `config/db_conf.py`，修改数据库连接信息。

### 5. 启动服务

```bash
fastapi dev 
```

访问 API 文档：

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## License

仅供学习使用。
