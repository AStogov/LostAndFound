## <a name = "user">user相关接口文档</a>

* [x] <a href='#login'>login</a>   
* [x] <a href='#getOpenid'>getOpenid</a>   
* [x] <a href='#loginByOpenid'>loginByOpenid</a>   
* [x] <a href='#logout'>logout</a>   
* [x] <a href='#get'>get</a>   
* [x] <a href='#update'>update</a>    

用户交互流程  

**注：用户的openid是所有操作的必须项**

### 数据模型

| 变量名    | 类型   | 变量含义                             |
| --------- | ------ | :----------------------------------- |
| id        | int    | 数据模型内部自增索引。前端无需操作。 |
| openid    | string | 前端获取的用户唯一标识               |
| name | string | 用户姓名                             |
| phone     | string | 用户手机号   |
| card | string | 用户的校园卡号 |
| contact | string | 用户的其他联系方式，如QQ/微信等（可不填） |
| ctime     | string | 数据创建时间（所有model共有的特性）  |
| mtime     | string | 数据修改时间（所有model共有的特性）  |

### Token鉴权

[Token账户鉴权系统][https://gogs.itoken.team/634308664/token-sso/src/master]

请前端同学先调用token账户鉴权系统，鉴权成功后再以流程验证登录。

**鉴权成功后，鉴权返回的手机号、姓名、校园卡号可以直接作为login的参数进行注册。**


```mermaid
graph LR
    H(Token鉴权) --> A[获取openid]
    A --> B(loginByOpenid)
    B --> C{数据库存在此openid}
    C -->|是| D(缓存用户信息)
    C -->|否| E[调用login注册]
    E -->D
```

数据库是否存在openid这一过程是依靠返回值判断的。

所有正确操作的返回值都是0

### <a name='login'>login</a> 用户登录（无状态注册）

**如果没有数据库内用户的openid，则用login进行注册**

url = www.example.com/service/user/login   
method = post   
params:   

| 名称      |  类型  | 必须 |                       备注                        |
| --------- | :----: | :--: | :-----------------------------------------------: |
| openid    | string |  是  | 可通过云函数或getOpenid获取，是每个用户的唯一凭证 |
| phone     | string |  是  |            手机号             |
| name | string |  是  |            用户姓名             |
| card | string | 是 | 用户的校园卡号 |
| contact | string | 否 | （可选）用户的其他联系方式，如QQ/微信等 |

return:

```json
{
    "code": 0,
    "msg": "success",
    "data": {
        "id": 1,
        "openid": "xxxxxxxx",
        "phone": "12345678912",
        "name": "张三",
        "card": "222222",
        "contact": "weixin_id123",
        "ctime": "2020-03-26 11:34:29",
        "mtime": "2020-03-26 11:34:35",
    }
}
```

错误码：

| code |           含义           |
| ---- | :----------------------: |
| -1   |      提交的参数非法      |
| -2   | 其他错误，详情见错误输出 |

### <a name='getOpenid'>getOpenid</a> 获取用户openid   

url = www.example.com/service/user/getOpenid   
method = post   
params:   

*不建议使用*

| 名称    |  类型  | 必须 | 备注 |
| :------ | :----: | :--: | :--: |
| js_code | string |  是  |      |

**建议使用云函数：   **
https://developers.weixin.qq.com/miniprogram/dev/wxcloud/guide/functions/userinfo.html

### <a name='loginByOpenid'>loginByOpenid</a> 通过openid登陆，获取个人信息  

url = www.example.com/service/user/loginByOpenid   
method = post   
params:   

| 名称   |   类型 | 必须 | 备注 |
| :----- | -----: | :--: | :--: |
| openid | string |  是  |      |

return:

```json
{
    "code": 0,
    "msg": "success",
    "data": {
        "id": 1,
        "openid": "xxxxxxxx",
        "phone": "12345678912",
        "name": "张三",
        "card": "222222",
        "contact": "weixin_id123",
        "ctime": "2020-03-26 11:34:29",
        "mtime": "2020-03-26 11:34:35",
    }
}
```

错误码：

| code |                含义                 |
| ---- | :---------------------------------: |
| -1   |           提交的参数非法            |
| -2   | 不存在此用户，此时应该调用login方法 |


### <a name='get'>get</a> 获取用户详情   

url = www.example.com/service/user/get   
method = post   
params:   

| 名称   | 类型 | 必须 | 备注 |
| :----- | :--: | :--: | :--: |
| openid | int  |  是  |      |

return:

```json
{
    "code": 0,
    "msg": "success",
    "data": {
        "id": 1,
        "openid": "xxxxxxxx",
        "phone": "12345678912",
        "name": "张三",
        "card": "222222",
        "contact": "weixin_id123",
        "ctime": "2020-03-26 11:34:29",
        "mtime": "2020-03-26 11:34:35",
    }
}
```

错误码：

| code |                    含义                    |
| ---- | :----------------------------------------: |
| -1   |               提交的参数非法               |
| -2   | 返回了多组数据（一个openid对应了多个用户） |
| -3   |          其他错误，详情见错误输出          |
| -4   |                 用户不存在                 |



### <a name='update'>update</a> 更新用户信息   

url = www.example.com/service/user/update   
method = post   
params:   

| 名称    |     类型     | 必须 |                            备注                             |
| :------ | :----------: | :--: | :---------------------------------------------------------: |
| user_id |     int      |  是  |                                                             |
| update  | json(string) |  是  | 如果提交的是字符串格式的json程序会loads，但最好提交json格式 |

e.g.:   
update={"phone":"13333333333"}   

return:   

```json
{
    "code": 0,
    "msg": "success",
    "data": []
}
```

错误码：

| code |                含义                |
| ---- | :--------------------------------: |
| -1   |           提交的参数非法           |
| -2   |      其他错误，详情见错误输出      |
| -3   | update参数提交的不是有效的json格式 |
| -4   |            json处理错误            |



