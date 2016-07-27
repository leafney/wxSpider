### 根据文章临时链接获取真实链接

从文章列表中得到的链接一段时间后就过期了，那么我们接下来要做的就是根据这个临时的链接，来获取到该文章的真实链接。


比如有一篇文章，我们在微信端获取到它的链接如下：

```
http://mp.weixin.qq.com/s?__biz=MzAwNTMxMzg1MA==&mid=2654067776&idx=1&sn=b4c1261a785a59dd6268142b0b358b50&scene=4#wechat_redirect
```

可以看到该链接中几个关键的请求参数：

```
__biz=MzAwNTMxMzg1MA==
mid=2654067776
idx=1
sn=b4c1261a785a59dd6268142b0b358b50
scene=4
```

而我们在搜狗微信搜索中得到的该文章的链接如下：

```
http://mp.weixin.qq.com/s?timestamp=1469352451&src=3&ver=1&signature=56kgMk71dIMM59VsUWlueRZ1ljkNODBEgrW78vmgXfJs82nkMESO8W*7EXf2ylOyamiUvL0zQ5OAfVraI8tPp-Hhdzv5WRQKSPa-MF6hiFMZf7rqxmZRvsYsd-7WSsy5qiafAQNfxBSkWzSulgB575CWRYnn6QZTRJ4NdR*gs0s=
```

通过比较这两个链接我们可以发现，第一个链接是从微信端得到的，所以可以肯定的说，这个链接不会过期(微信端的文章用户可以分享到朋友圈或收藏)，那么可以推断那些请求参数都是必需的。
而第二个链接中我们并没有发现类似的请求参数，除了一个时间戳预示着这个链接是有时效性的之外，其他并无价值。

既然链接中没有，那么网页中是否有这些参数呢？毕竟两个链接虽然请求参数不同而网页内容都是相同的。

我们查看第二个链接的源代码，可以找到如下的一段js：

```
var page_begintime=+new Date,biz="",sn="",mid="",idx="",is_rumor="",norumor="";
1*is_rumor&&!(1*norumor)&&(document.referrer&&-1!=document.referrer.indexOf("mp.weixin.qq.com/mp/rumor")||(location.href="http://mp.weixin.qq.com/mp/rumor?action=info&__biz="+biz+"&mid="+mid+"&idx="+idx+"&sn="+sn+"#wechat_redirect")),
document.domain="qq.com";
```

从中提取出如下的一段：

```
location.href="http://mp.weixin.qq.com/mp/rumor?action=info&__biz="+biz+"&mid="+mid+"&idx="+idx+"&sn="+sn+"#wechat_redirect"
```

可以看到，这个链接似乎和我们的第一个链接即文章的真实链接长得很相像，而其中也是有几个必要的参数：`__biz` ,`mid`,`idx`,`sn`。那么，我们只要找到这几个参数对应的值也就能成功的拼接出该网页正确的链接了。

然后，我们在文章源代码的末尾处能找到如下的一段：

```
var msg_link = "http://mp.weixin.qq.com/s?__biz=MzAwNTMxMzg1MA==&amp;mid=2654067776&amp;idx=1&amp;sn=b4c1261a785a59dd6268142b0b358b50#rd";
```

从中我们就得到了想要的参数的值：

```
__biz=MzAwNTMxMzg1MA==
mid=2654067776
idx=1
sn=b4c1261a785a59dd6268142b0b358b50
```

通过得到的参数值，再根据上面得到的链接形式，我们就可以拼接出文章的真实链接如下：

```
http://mp.weixin.qq.com/s?__biz=MzAwNTMxMzg1MA==&mid=2654067776&idx=1&sn=b4c1261a785a59dd6268142b0b358b50#wechat_redirect
```

拷贝到浏览器中访问，成功。

*** 

2016-7-26 更新

刚刚在实现 “获取真实网址” 这个方法的时候，发现 `msg_link` 这个链接其实就是我们需要的链接：

```
var msg_link = "http://mp.weixin.qq.com/s?__biz=MzAwNTMxMzg1MA==&amp;mid=2654067776&amp;idx=1&amp;sn=b4c1261a785a59dd6268142b0b358b50#rd";
```

只不过需要把里面的 `&amp;` 转换成 `&` 就可以了。

