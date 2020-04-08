## <a name = "upload">upload相关接口</a>

* [x] <a href='#avatar'>avatar</a>   
* [x] <a href='#itemImg'>itemImg</a>  



***如果用户是第一次注册，就先调用avatar方法保存用户头像，并将返回值保存后留等调用login方法时提交，以此来将用户的头像保存在本地加快内容加载速度。***

### <a name='avatar'>avatar</a> 上传用户头像

**这个接口接受一个给定的url，并将指定的图片保存在本地。一般用于呈现用户的微信头像。**

url = www.example.com/service/upload/avatar      
method = post   
params:   

| 名称   |  类型  | 必须 |        备注         |
| :----- | :----: | :--: | :-----------------: |
| openid |  int   |  是  |    用户唯一标识     |
| avatar | string |  是  | 头像url（微信头像） |

return:

```json
{
    "code": 0,
    "msg": "success",
    "data": {
        "avatar": "https://www.example.com/media/avatar/test.jpg"
    }
}
```

错误代码

| code |           含义           |
| ---- | :----------------------: |
| -1   |      提交的参数非法      |
| -2   | 其他错误，详情见错误输出 |



### <a name='itemImg'>itemImg</a> 上传用户头像

**这个接口上传的是图片文件，用来在物品描述也上传图片用。如果用于用户自定义头像，建议还是用avatar方法较好，用用户的微信头像以免上传的头像出现其他问题**

url = www.example.com/service/upload/itemImg      
method = post   
params:   

| 名称   | 类型 | 必须 |                    备注                     |
| :----- | :--: | :--: | :-----------------------------------------: |
| images | file |  是  | 可传多个、要将input标签中的name设置为images |

return:

```json
{
    "code": 0,
    "msg": "success",
    "data": "[\"https://www.example.com/media/item/2020/3/27/011216_59730.jpg\", \"https://www.example.com/media/item/2020/3/27/011216_89864.jpg\"]"
}
```

| code |             含义             |
| ---- | :--------------------------: |
| -1   | 提交的参数非法或文件不是图片 |
| -2   |   其他错误，详情见错误输出   |