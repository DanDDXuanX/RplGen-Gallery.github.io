#!/usr/bin/env python
# coding: utf-8

# 命令行工具

import os
import json
from pathlib import Path
from getpass import getpass

class RplGenTpltEditorCLI:
    input_promote = {
        'path' : '请输入文件路径，或者将项目文件夹拖入命令行窗口：',
        'rgpj' : '选中的文件夹下有多个项目文件，请选择一个项目文件：',
        'header' : '请选择一个角色自定义属性，作为角色的显示名：',
        'name' : '请给你的模板，取一个直观，好听的名字吧！',
        'cover' : '请在下列图片中，选择你的模板封面：',
        'describe' : '请简单介绍一下这个预设模板，最多40字：',
        'author' : '请留下作者的署名：',
        'usage' : '请选择：允许其他用户在什么范围内使用这个预设模板的素材？',
        'signature' : '请选择：如果用户使用了该模板，是否需要署名模板作者？',
        'delrgpj' : '模板（RGINT）已经创建完成，是否要删除原始项目文件（RGPJ）？',
        'upload' : '文件已经准备就绪，是否立刻上传到创意工坊？',
        'success' : '上传是否已经成功了？如果没有成功，选择否，我们可以重新尝试上传一次。'
    }
    initial_info = [
        '回声工坊-模板制作工具 © 2024, Betelgeuse Industry',
        '请按照下述流程，完成模板创建；',
        '如果需要返回上一个选项，请输入井号#后按回车键。'
    ]     
    input_pipe = [
        'path',
        'header',
        'cover',
        'name',
        'describe',
        'author',
        'usage',
        'signature',
    ]
    table_col = ['Name','Subtype','Animation','Bubble','Voice','SpeechRate','PitchRate']
    def bulid_template(self,path,header,meta):
        # 需要用户输入的内容
        # path = './明日方舟'
        # header = '显示名'
        # meta = {
        #     "name":"明日方舟对话框",
        #     "cover":"@/cover.png",
        #     "describe":"明日方舟的极简风格，没有多加东西，请以实际情况调整。",
        #     "author":"GULILI",
        #     "licence":"不可以用于商业用途，无需注明作者"
        # }
        # 创建智能模板
        # 载入rgpj
        workpath = Path(path)
        find_result = list(workpath.glob('*.rgpj'))
        if find_result:
            rplgen_project = json.load(open(find_result[0].absolute()))
        # 创建一个空白的模板
        rplgen_intel_template = {}
        # 写入meta信息
        # 封面要求：540p，jpg
        rplgen_intel_template['meta'] = meta
        # 项目配置，移除原有的项目名称和封面
        config = rplgen_project['config'].copy()
        config.pop('Name')
        config.pop('Cover')
        rplgen_intel_template['config'] = config

        # 排序媒体
        media_order = {
            'Pos'       : ['Pos','FreePos','PosGrid','BezierCurve'],
            'Text'      : ['Text', 'StrokeText', 'RichText', 'HPLabel'],
            'Animation' : ['Animation'],
            'Bubble'    : ['Bubble','Balloon','DynamicBubble','ChatWindow'],
            'Background': ['Background'],
            'Audio'     : ['Audio','BGM'],
        }
        static_media = {}
        for type in media_order:
            this_type:list = media_order[type]
            for name in rplgen_project['mediadef']:
                item = rplgen_project['mediadef'][name]
                if item['type'] in this_type:
                    static_media[name] = item
        # 添加媒体
        rplgen_intel_template['media'] = {
            'static':static_media,
            'dynamic':{}
        }
        # 检视角色
        # 获取自定义列的信息
        custom = []
        static_list = []
        dynamic_list = []
        for keyword in rplgen_project['chartab']:
            this_char = rplgen_project['chartab'][keyword]
            # 检视自定义
            for col in this_char:
                if col not in self.table_col and col not in custom:
                    custom.append(col)
            # 检视名字
            name:str = this_char['Name']
            if name.isdigit():
                dynamic_list.append(keyword)
            else:
                static_list.append(keyword)
        dynamic_charactor = {}
        static_charactor = {}
        # 静态角色采用的列
        static_use_col = ['Name','Subtype','Animation','Bubble'] + custom
        # 动态角色采用的列，不含header
        dynamic_use_col = ['Animation','Bubble'] + custom
        dynamic_use_col.remove(header)
        # 获取静态角色
        for keyword in static_list:
            this_char = rplgen_project['chartab'][keyword]
            tplt_char = {}
            name = this_char['Name']
            for col in static_use_col:
                tplt_char[col] = this_char[col]
            static_charactor[name] = tplt_char
        # 获取动态角色
        for keyword in dynamic_list:
            this_char = rplgen_project['chartab'][keyword]
            tplt_char = {}
            name = this_char['Name']
            for col in dynamic_use_col:
                tplt_char[col] = this_char[col]
            dynamic_charactor[name] = tplt_char
        # 添加角色
        rplgen_intel_template['charactor'] = {
            "custom":custom,
            "header":header,
            'static':static_charactor,
            'dynamic':dynamic_charactor
        }
        # 剧本
        rplgen_intel_template['preset'] = rplgen_project['logfile']['preset']
        if 'example' in rplgen_project['logfile']:
            rplgen_intel_template['example'] = rplgen_project['logfile']['example']
        else:
            rplgen_intel_template['example'] = None
        # 输出
        with open(workpath.absolute()/'main.rgint','w',encoding='utf-8') as rgint:
            json.dump(rplgen_intel_template,rgint,ensure_ascii=False,indent=4)
    # 创建vdf
    def bulid_vdf(self,path:Path,version):
    # path = './明日方舟'
    # version = 'RGS @ beta 2.0.6'
    # 创建VDF文件
        vdf_tplt = open('./workshop_newitem.vdf','r').read()
        meta = json.load(open(path / 'main.rgint','r',encoding='utf-8'))['meta']
        name = meta['name']

        folder = path.absolute().__str__()
        cover = meta['cover'].replace('@',folder).replace('/','\\')

        description = '简介：{describe} 作者：{author} 授权：{licence}'.format(**meta)
        # 保存vdf
        with open(f'./steamcmd/{name}.vdf','w',encoding='utf-8') as of:
            of.write(
                vdf_tplt
                .replace('{path}',folder)
                .replace('{cover}',cover)
                .replace('{title}',meta['name'])
                .replace('{description}',description)
                .replace('{version}',version)
            )
        return f'{name}.vdf'
    # 获取输入
    def get_input(self):
        metainfo = {
            'path' : '',
            'header' : '',
            'meta' : {
                "name":"",
                "cover":"",
                "describe":"",
                "author":"",
                "licence":""
            }
        }
        # 显示初始信息
        for line in self.initial_info:
            print(line)
        # 开始用户输入流程
        idx = 0
        while idx < len(self.input_pipe):
            # 序号不能小于0
            if idx < 0:
                idx = 0
            keyword = self.input_pipe[idx]
            # 1. 项目路径
            if keyword == 'path':
                get = input(self.format_promote(self.input_promote['path']))
                if get == '#':
                    idx -= 1
                    continue
                # 定位到rgpj文件
                metainfo['path'] = Path(get)
                rgpj = []
                for file in metainfo['path'].glob('./*.rgpj'):
                    rgpj.append(file.name)
                if len(rgpj) == 1:
                    main_rgpj = metainfo['path'] / rgpj[0]
                elif len(rgpj) > 1:
                    options = self.format_options(rgpj)
                    get = input(self.format_promote(self.input_promote['rgpj']+'\n'+options))
                    if get == '#':
                        continue
                    try:
                        main_rgpj = metainfo['path'] / rgpj[ord(get.upper()) - ord('A')]
                    except Exception:
                        print('错误：无效的选项！')
                        continue
                else:
                    print('错误：这个路径下没有项目文件（RGPJ）！')
                    idx = 0
                    continue
                # 读取rgpj
                self.main_rgpj:Path = main_rgpj
                rplgen_project = json.load(open(main_rgpj))
                # 检视角色
                if '0.default' not in rplgen_project['chartab']:
                    print('错误：项目中缺少必要的角色【0】！')
                    continue
                # 检查媒体目录是否存在
                if not (metainfo['path'] / 'media').is_dir():
                    print('错误：项目文件夹中缺少必要的素材文件夹【media】！')
                    continue
                # 检查是否是相对引用
                warnings = {}
                for name in rplgen_project['mediadef']:
                    mobject = rplgen_project['mediadef'][name]
                    if 'fontfile' in mobject:
                        if mobject['fontfile'][0:8] != '@/media/':
                            warnings[name] = mobject['fontfile']
                    elif 'filepath' in mobject:
                        if mobject['filepath'][0:8] != '@/media/':
                            warnings[name] = mobject['filepath']
                if len(warnings) != 0:
                    print('警告：下列媒体使用的文件路径不在素材文件夹【media】下，请确保这些文件是始终可及的。')
                    for name in warnings:
                        print(name, warnings[name])
                # 更新序号
                idx += 1
                continue
            # 2. 显示名
            elif keyword == 'header':
                # 获取自定义列
                custom = []
                for keyword in rplgen_project['chartab']:
                    this_char = rplgen_project['chartab'][keyword]
                    # 检视自定义
                    for col in this_char:
                        if col not in self.table_col and col not in custom:
                            custom.append(col)
                # 创建选项
                if len(custom) == 0:
                    print('错误：当前项目中，角色缺少用于专用于显示角色名的自定义属性。')
                    idx = 0 # 退回选择目录的位置
                    continue
                options = self.format_options(custom)
                get = input(self.format_promote(self.input_promote['header']+'\n'+options))
                if get == '#':
                    idx -= 1
                    continue
                try:
                    metainfo['header'] = custom[ord(get.upper()) - ord('A')]
                    idx += 1
                    continue
                except Exception:
                    print('错误：无效的选项！')
                    continue
            # 3. 模板名
            elif keyword == 'name':
                get = input(self.format_promote(self.input_promote['name']))
                if get == '#':
                    idx -= 1
                    continue
                else:
                    metainfo['meta']['name'] = get[0:14]
                    idx += 1
                    continue
            # 4. 封面
            elif keyword == 'cover':
                imgs = self.get_all_img_from_root(directory=metainfo['path'])
                if len(imgs) == 0:
                    print('错误：项目文件夹下缺少封面图片！')
                    idx = 0
                options = self.format_options(imgs)
                get = input(self.format_promote(self.input_promote['cover']+'\n'+options))
                if get == '#':
                    idx -= 1
                    continue
                else:
                    try:
                        metainfo['meta']['cover'] = '@/' + imgs[ord(get.upper()) - ord('A')]
                        idx += 1
                        continue
                    except Exception:
                        print('错误：无效的选项！')
                        continue
            # 5. 描述
            elif keyword == 'describe':
                get = input(self.format_promote(self.input_promote['describe']))
                if get == '#':
                    idx -= 1
                    continue
                else:
                    metainfo['meta']['describe'] = get[0:40]
                    idx += 1
                    continue
            # 6. 作者
            elif keyword == 'author':
                get = input(self.format_promote(self.input_promote['author']))
                if get == '#':
                    idx -= 1
                    continue
                else:
                    metainfo['meta']['author'] = get[0:14]
                    idx += 1
                    continue
            # 7. 选择用途
            elif keyword == 'usage':
                usage_options = [
                    '可以用于任何用途',
                    '不可以用于商业用途',
                    '仅供测试和学习使用',
                ]
                options = self.format_options(usage_options)
                get = input(self.format_promote(self.input_promote['usage']+'\n'+options))
                if get == '#':
                    idx -= 1
                    continue
                else:
                    try:
                        usage = usage_options[ord(get.upper()) - ord('A')]
                        idx += 1
                        continue
                    except Exception:
                        print('错误：无效的选项！')
                        continue
            # 8. 选择署名
            elif keyword == 'signature':
                signature_options = [
                    '无需注明作者',
                    '建议注明作者',
                    '必须注明作者'
                ]
                options = self.format_options(signature_options)
                get = input(self.format_promote(self.input_promote['signature']+'\n'+options))
                if get == '#':
                    idx -= 1
                    continue
                else:
                    try:
                        signature = signature_options[ord(get.upper()) - ord('A')]
                        metainfo['meta']['licence'] = f'{usage}，{signature}'
                        idx += 1
                        continue
                    except Exception:
                        print('错误：无效的选项！')
                        continue
            else:
                continue
        # 返回结果
        return metainfo

    def format_options(self,options):
        formatted_string = ""
        for index, option in enumerate(options):
            formatted_string += f"{chr(65 + index)}. {option} ; "
        # 删除最后的分号和空格
        formatted_string = formatted_string[:-2]
        return formatted_string

    def get_all_img_from_root(self,directory):
        # 指定目录路径
        # 使用glob模块来匹配所有的png和jpg文件
        path = Path(directory)
        png_files = path.glob('./*.png')
        jpg_files = path.glob('./*.jpg')

        # 打印所有找到的png和jpg文件
        files = []
        for file in png_files:
            files.append(file.name)
        for file in jpg_files:
            files.append(file.name)
        return files

    def format_promote(self,string):
        return '--------------------------------------------\n' + string + '\n> '

    def run_bulid_template(self,metainfo):
        try:
            self.bulid_template(
                path=metainfo['path'].absolute(),
                header=metainfo['header'],
                meta=metainfo['meta']
            )
            yesno = ['是','否']
            options = self.format_options(yesno)
            while 1:
                get = input(self.format_promote(self.input_promote['delrgpj']+'\n'+options))
                try:
                    choice = yesno[ord(get.upper()) - ord('A')]
                    if choice == '是':
                        os.remove(self.main_rgpj)
                    else:
                        pass
                    break
                except Exception:
                    print('错误：无效的选项！')
                    continue
            return 0 # 正常退出
        except Exception as E:
            print('错误：无法将项目转为模板，由于：', E)
            return 1 # 错误
    ## steamcmd
    # ```bash
    # cd ./steamcmd
    # steamcmd.exe +login $myLoginName $myPassword +workshop_build_item ${tplt_name}.vdf +quit
    # ```
    def run_upload_workshop(self,metainfo):
        try:
            vdf = self.bulid_vdf(
                path=metainfo['path'].absolute(),
                version='RGSE @ beta 2.0.6'
            )
            yesno = ['是','否']
            options = self.format_options(yesno)
            # 是否上传
            while 1:
                get = input(self.format_promote(self.input_promote['upload']+'\n'+options))
                try:
                    choice = yesno[ord(get.upper()) - ord('A')]
                    if choice == '是':
                        pass
                    else:
                        return 1 # 选择不上传
                    break
                except Exception:
                    print('错误：无效的选项！')
                    continue
            # 上传是否成功
            os.chdir('./steamcmd')
            while 1:
                # 执行上传
                username, password = self.ask_username_passwd()
                command = f'steamcmd.exe +login {username} {password} +workshop_build_item {vdf} +quit'
                os.system(command=command)
                # print(command)
                # 询问
                get = input(self.format_promote(self.input_promote['success']+'\n'+options))
                try:
                    choice = yesno[ord(get.upper()) - ord('A')]
                    if choice == '是':
                        break
                    else:
                        print('重试')
                except Exception:
                    print('错误：无效的选项，重试！')
                    continue
            return 0 # 正常退出
        except Exception as E:
            print('错误：无法准备上传信息，由于：', E)
            raise E
            return 1 # 错误
    def ask_username_passwd(self):
        username = input(self.format_promote('请输入steam账号：'))
        password = getpass(self.format_promote('请输入steam密码：（注意，本软件不会存储您的密码；您输入的密码不会明文显示）'))
        return username , password
    def __init__(self):
        # 获取输入，检查内容
        metainfo = self.get_input()
        # 将项目转化为脚本
        status = self.run_bulid_template(metainfo=metainfo)
        if status:
            return
        # 将项目上传
        status = self.run_upload_workshop(metainfo=metainfo)

RplGenTpltEditorCLI()