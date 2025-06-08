# 食品入库与过期记录系统

这是一个用于高效管理食品库存，记录食品生产日期、保质期并自动生成过期日期的系统。

## 功能

- 食品信息录入
- 过期日期自动生成
- 库存管理
- 过期预警
- 历史记录查询
- 用户管理

## 技术栈

- **前端**: Vue 3
- **后端**: Python (Flask)
- **数据库**: SQLite

## 项目结构

- `frontend/`: 前端代码
- `backend/`: 后端代码

## 运行项目

### 后端

1.  进入 `backend` 目录：
    ```bash
    cd backend
    ```
2.  创建并激活虚拟环境（如果尚未创建）：
    ```bash
    py -m venv venv
    # Windows
    .\venv\Scripts\activate
    # macOS/Linux
    # source venv/bin/activate
    ```
3.  安装依赖：
    ```bash
    pip install -r requirements.txt # 如果有 requirements.txt 文件
    # 或者手动安装 Flask 和 Flask-CORS
    pip install Flask Flask-CORS
    ```
4.  初始化数据库（首次运行或数据库文件丢失时）：
    ```bash
    py database.py
    ```
5.  启动 Flask 后端服务：
    ```bash
    flask run
    ```
    后端将在 `http://127.0.0.1:5000` 运行。

### 前端

1.  进入 `frontend` 目录：
    ```bash
    cd frontend
    ```
2.  安装依赖（如果尚未安装）：
    ```bash
    npm install
    # 或手动安装所需库：
    # npm install element-plus vue-router axios
    ```
3.  启动 Vue 开发服务器：
    ```bash
    npm run dev
    ```
    前端将在 `http://localhost:5174` (或类似地址) 运行。

## 开始

更多详细信息请参考项目文档。 