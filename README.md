# django + vue 后台管理系统
包含 `用户`、`角色`、`菜单`、`权限`。

## 开发环境
### 后端
安装依赖
```bash
cd backend
pip install -r requirements.txt
```

初始化系统
- 管理员账号 `admin 123456`, 普通账号 `test 123456`, 
```bash
python manage.py migrate
python manage.py init_sys
```

- 生成普通账号 `aaa 123456`, 用户名随意填写
```bash
 python manage.py create_user <username> 
```