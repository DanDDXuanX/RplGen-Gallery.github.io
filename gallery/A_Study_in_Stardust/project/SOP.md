# 星尘的研究 checklist
0. 参数
Zorder: BG2,BG1,AmS,Bb,Bb,SAm3,Am2,Am1
1. 梳理文本
2. 添加背景行
```
# 普通切换
<background>:public_library_lobby
# 黑场切换
<background><black=50>:hotel_outside
```
3. 添加设置项目
```
<set:formula>:sincurve
<set:secondary_alpha>:100
<set:tx_method_default>:<w2w=3>
<set:am_method_default>:<black=10>
<set:bb_method_default>:<black=10>
<set:bg_method_default>:<cross=30>
```
4. 添加起始画面和结束画面
```
<background><black=30>:header1
<background><replace=150>:header1
<background><black=30>:header2
<background><replace=150>:header2
<background><black=30>:header3
[场景切换]<black=30>:^《星尘的研究》#-第三章-<all=0>{NA;*4}
# ......
<background>:black
[场景切换]:未完待续<all=0>{NA;*5}
```
5. 为吐槽设置动态效果
```
# 单句
[张安翔.吐槽]<black_200_leap_down=20>:...
# 多句
[张安翔.吐槽]<black_200_leap_down_in=20>:...
[拉塔斯托克.吐槽]<replace=0>:...
[诺兰.吐槽]<black_200_leap_down_out=20>:...
```
6. 为sancheck设置动态效果
```
# 单句
[kp.sancheck]<black_circular_2=45>:...
# 多句
[kp.sancheck]<black_circular_2_in=45>:...
[kp.sancheck]<replace_circular_2=45>:...
[kp.sancheck]<black_circular_2_out=45>:...
```
7. 为特殊演示添加音效
```
# 收发邮件
[张安翔.电子邮件]:...{receive_mail}
[拉塔斯托克.电子邮件]:...{keyboard}
# 纸张翻页
[kp.书本资料]:...{open_paper}
[kp.文件]:...{open_paper}
[kp,图例.复旧党报纸]:...{open_paper}
```
8. 添加语音合成标志
```
# 角色：张安翔 诺兰 斯托克 阿米蒂奇 麦克_里斯 朱蒂
# 其他：图例 搜索引擎 sancheck 书本

# 语音合成 "^\[(kp|诺兰|拉塔斯托克|张安翔|未知姓名|搜索引擎|阿米蒂奇|麦克_里斯|朱蒂).*\].+$" > "$0{*}"
```