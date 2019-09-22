from django.shortcuts import render
from legalfiles.models import Txt,Tag
# Create your views here.
from django.http import HttpResponse
import os
import legalfiles.processtext.batchdealtext
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView
from legalfiles.operateobject import savetxt,savetag,savetxttags,deletetag,deletetxt,deletetxttags,addtag,addtxttag
from legalfiles.processtext.deletefiles import deletefiles,deletefiles2txt
from django.shortcuts import render, get_object_or_404
#表现层不是一个个的功能，只是中间人
#可以调用业务层，可以调用工具方法

from django.shortcuts import render, redirect

from .forms import RegisterForm
from django.http import HttpRequest
myrequest = HttpRequest()

def register(request):
    # 从 get 或者 post 请求中获取 next 参数值
    # get 请求中，next 通过 url 传递，即 /?next=value
    # post 请求中，next 通过表单传递，即 <input type="hidden" name="next" value="{{ next }}"/>
    redirect_to = request.POST.get('next', request.GET.get('next', ''))

    # 只有当请求为 POST 时，才表示用户提交了注册信息
    if request.method == 'POST':
        # request.POST 是一个类字典数据结构，记录了用户提交的注册信息
        # 这里提交的就是用户名（username）、密码（password）、确认密码、邮箱（email）
        # 用这些数据实例化一个用户注册表单
        form = RegisterForm(request.POST)

        # 验证数据的合法性
        if form.is_valid():
            # 如果提交数据合法，调用表单的 save 方法将用户数据保存到数据库
            form.save()

            if redirect_to:
                return redirect(redirect_to)
            else:
                return redirect('/')
    else:
        # 请求不是 POST，表明用户正在访问注册页面，展示一个空的注册表单给用户
        form = RegisterForm()

    # 渲染模板
    # 如果用户正在访问注册页面，则渲染的是一个空的注册表单
    # 如果用户通过表单提交注册信息，但是数据验证不合法，则渲染的是一个带有错误信息的表单
    # 将记录用户注册前页面的 redirect_to 传给模板，以维持 next 参数在整个注册流程中的传递
    return render(request, 'legalfiles/register.html', context={'form': form, 'next': redirect_to})


def index2(request):
    return render(request,'index2.html')

def to_upload(request):
    print(request.session)

    #print(request.COOKIES)
    return render(request, 'legalfiles/upload.html')

def upload_file(request):

    # if request.method == "POST":    # 请求方法为POST时，进行处理
    myFile = request.FILES.getlist("myfile", None)  # 获取上传的文件，如果没有文件，则默认为None

    # if not myFile:
    #     return HttpResponse("no files for upload!")

    for f in myFile:
        print(f.name)
        destination = open('legalfiles/files/' + f.name, 'wb+')  # 打开特定的文件进行二进制的写操作
        for chunk in f.chunks():
            destination.write(chunk)
        destination.close()
    return HttpResponse("上传成功! 请关闭窗口")


def to_process(request):
    return render(request, 'legalfiles/processfiles.html')


def process_file(request):

    # if request.method == "POST":
    #先处理txt们,分词什么的
    bat=legalfiles.processtext.batchdealtext.Batchdealtext()
    bat.processfile()
    #保存文件到数据库
    legalfiles.operateobject.savetxt.save_txt(request)

    # 保存标签到数据库
    legalfiles.operateobject.savetag.save_tag(request)
    #
    legalfiles.operateobject.savetxttags.save_txttags(request)
    # 删除上传上来的文件和我们生成的txt文件
    deletefiles()
    deletefiles2txt()
    #清空类变量
    bat.clear()





    return HttpResponse("处理文件成功! 请关闭窗口")

def detail(request, txt_id):
    all_txt = Txt.objects.all()

    curr_txt = None
    previous_txt = None
    next_txt = None

    previous_index = 0
    next_index = 0

    for index, txt in enumerate(all_txt):
        if index == 0:
            previous_index = 0
            next_index = index + 1
        elif index == len(all_txt) - 1:
            previous_index = index - 1
            next_index = index
        else:
            previous_index = index - 1
            next_index = index + 1
        #弄完上面的下表，就检查循环到这篇文章没
        if txt.txt_id == txt_id:
            curr_txt = txt
            #用enumerate的好处就在这里了，给all_txt的每一个对象弄一个顺序下标，而不用管pk
            previous_txt = all_txt[previous_index]
            next_txt = all_txt[next_index]
            break


    section_list = curr_txt.content.split('\n')

    return render(request, 'legalfiles/detail.html',
                  {
                      'curr_txt': curr_txt,
                      'section_list': section_list,
                      'previous_txt': previous_txt,
                      'next_txt': next_txt
                  }
                  )

def test(request):
    return render(request, 'legalfiles/test.html')

from xpinyin import Pinyin
#把标签列表按字母排序
def get_tags(tags):
    pin = Pinyin()
    ret={}
    list=[]
    for tag in tags:
        #把一个个标签的拼音和名字组合起来，list是一个元组列表
        list.append((pin.get_pinyin(tag),tag))
    #默认按照元组的第一个元素排序
    list.sort()
    temp_list = []
    #排序完的列表的长度
    length=len(list)
    #print(length)
    for i in range(length):
        if i>0:
            #如果首字母和前一个相同，加进去temp
           if list[i][0][0]==list[i-1][0][0]:
              temp_list.append(list[i][1])
              # #到了结尾了，别忘了弄进去ret，之前忽略了
              # if i==length-1:
              #     ret[list[i][0][0]] = temp_list
            #发现不相同，就是新的首字母开启，旧字母作为key，temp这个列表作为内容，放进去ret
           else:
              #保存旧字母的
              ret[list[i-1][0][0]]=temp_list
              #清空
              temp_list=[]
              temp_list.append(list[i][1])
        else:
            #第一个，那就开辟
            temp_list.append(list[i][1])
    if length>0:
    #返回一个key是首字母，value是列表的字典
        ret[list[length-1][0][0]] = temp_list
    return ret

#获取用户的标签
def get_mytags(request):
    mytags = set()
    mytxts = Txt.objects.filter(users_id=request.user)
    for mytxt in mytxts:
        txt_tag = Txt.objects.filter(txt_id=mytxt.txt_id).values_list("tags")
        for tag_id in txt_tag:
            # mytags_id.add(tag_id[0])
            if tag_id[0]!=None :
                mytags.add(Tag.objects.get(id=tag_id[0]).name)
    return mytags

#search in input
class TagView(ListView):
    model = Txt
    template_name = 'legalfiles/index.html'
    context_object_name = 'txts'

    #有时候真的乱，这个查询对应标签的文本的功能不是应该写在业务层吗，但是教程就写在这里
    #重写了父类方法
    def get_queryset(self):
        #先把用户的查出来
        ret = Txt.objects.filter(users_id=self.request.user)

        #下面再慢慢过滤
        if self.kwargs.get('name1')!=' ':
          tag1 = get_object_or_404(Tag, name=self.kwargs.get('name1'),users=self.request.user)
          ret=ret.filter(tags=tag1)
        else:
          pass

        if self.kwargs.get('name2')!=' ':
          tag2 = get_object_or_404(Tag, name=self.kwargs.get('name2'),users=self.request.user)
          ret=ret.filter(tags=tag2)
        else:
          pass

        if self.kwargs.get('name3')!=' ':
          tag3 = get_object_or_404(Tag, name=self.kwargs.get('name3'),users=self.request.user)
          ret=ret.filter(tags=tag3)
        else:
          pass

        if self.kwargs.get('name4')!=' ':
          tag4 = get_object_or_404(Tag, name=self.kwargs.get('name4'),users=self.request.user)
          ret=ret.filter(tags=tag4)
        else:
          pass

        if self.kwargs.get('name5')!=' ':
          tag5 = get_object_or_404(Tag, name=self.kwargs.get('name5'),users=self.request.user)
          ret=ret.filter(tags=tag5)
        else:
          pass

        if self.kwargs.get('name6')!=' ':
          tag6 = get_object_or_404(Tag, name=self.kwargs.get('name6'),users=self.request.user)
          ret=ret.filter(tags=tag6)
        else:
          pass

        if self.kwargs.get('name7')!=' ':
          tag7 = get_object_or_404(Tag, name=self.kwargs.get('name7'),users=self.request.user)
          ret=ret.filter(tags=tag7)
        else:
          pass

        if self.kwargs.get('name8')!=' ':
          tag8 = get_object_or_404(Tag, name=self.kwargs.get('name8'),users=self.request.user)
          ret=ret.filter(tags=tag8)
        else:
          pass

        return ret
    def get_context_data(self, **kwargs):
        """
        在视图函数中将模板变量传递给模板是通过给 render 函数的 context 参数传递一个字典实现的，
        例如 render(request, 'blog/index.html', context={'post_list': post_list})，
        这里传递了一个 {'post_list': post_list} 字典给模板。
        在类视图中，这个需要传递的模板变量字典是通过 get_context_data 获得的，
        所以我们复写该方法，以便我们能够自己再插入一些我们自定义的模板变量进去。
        """
        context = super(TagView, self).get_context_data(**kwargs)
        context['mytags'] = get_tags(get_mytags(self.request))
        # 首先获得父类生成的传递给模板的字典。
        #context = super(IndexView, self).get_context_data(**kwargs)
        # 父类生成的字典中已有 paginator、page_obj、is_paginated 这三个模板变量，
        # paginator 是 Paginator 的一个实例，
        # page_obj 是 Page 的一个实例，
        # is_paginated 是一个布尔变量，用于指示是否已分页。
        # 例如如果规定每页 10 个数据，而本身只有 5 个数据，其实就用不着分页，此时 is_paginated=False。
        # 关于什么是 Paginator，Page 类在 Django Pagination 简单分页：http://zmrenwu.com/post/34/ 中已有详细说明。
        # 由于 context 是一个字典，所以调用 get 方法从中取出某个键对应的值。
        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')

        # 调用自己写的 pagination_data 方法获得显示分页导航条需要的数据，见下方。
        pagination_data = self.pagination_data(paginator, page, is_paginated)

        # 将分页导航条的模板变量更新到 context 中，注意 pagination_data 方法返回的也是一个字典。
        context.update(pagination_data)

        # 将更新后的 context 返回，以便 ListView 使用这个字典中的模板变量去渲染模板。
        # 注意此时 context 字典中已有了显示分页导航条所需的数据。
        #我写：这个就是返回给html的字典
        return context

    def pagination_data(self, paginator, page, is_paginated):
        if not is_paginated:
            # 如果没有分页，则无需显示分页导航条，不用任何分页导航条的数据，因此返回一个空的字典
            return {}

        # 当前页左边连续的页码号，初始值为空
        left = []

        # 当前页右边连续的页码号，初始值为空
        right = []

        # 标示第 1 页页码后是否需要显示省略号
        left_has_more = False

        # 标示最后一页页码前是否需要显示省略号
        right_has_more = False

        # 标示是否需要显示第 1 页的页码号。
        # 因为如果当前页左边的连续页码号中已经含有第 1 页的页码号，此时就无需再显示第 1 页的页码号，
        # 其它情况下第一页的页码是始终需要显示的。
        # 初始值为 False
        first = False

        # 标示是否需要显示最后一页的页码号。
        # 需要此指示变量的理由和上面相同。
        last = False

        # 获得用户当前请求的页码号
        page_number = page.number

        # 获得分页后的总页数
        total_pages = paginator.num_pages

        # 获得整个分页页码列表，比如分了四页，那么就是 [1, 2, 3, 4]
        page_range = paginator.page_range

        if page_number == 1:
            # 如果用户请求的是第一页的数据，那么当前页左边的不需要数据，因此 left=[]（已默认为空）。
            # 此时只要获取当前页右边的连续页码号，
            # 比如分页页码列表是 [1, 2, 3, 4]，那么获取的就是 right = [2, 3]。
            # 注意这里只获取了当前页码后连续两个页码，你可以更改这个数字以获取更多页码。
            right = page_range[page_number:page_number + 2]

            # 如果最右边的页码号比最后一页的页码号减去 1 还要小，
            # 说明最右边的页码号和最后一页的页码号之间还有其它页码，因此需要显示省略号，通过 right_has_more 来指示。
            if right[-1] < total_pages - 1:
                right_has_more = True

            # 如果最右边的页码号比最后一页的页码号小，说明当前页右边的连续页码号中不包含最后一页的页码
            # 所以需要显示最后一页的页码号，通过 last 来指示
            if right[-1] < total_pages:
                last = True

        elif page_number == total_pages:
            # 如果用户请求的是最后一页的数据，那么当前页右边就不需要数据，因此 right=[]（已默认为空），
            # 此时只要获取当前页左边的连续页码号。
            # 比如分页页码列表是 [1, 2, 3, 4]，那么获取的就是 left = [2, 3]
            # 这里只获取了当前页码后连续两个页码，你可以更改这个数字以获取更多页码。
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]

            # 如果最左边的页码号比第 2 页页码号还大，
            # 说明最左边的页码号和第 1 页的页码号之间还有其它页码，因此需要显示省略号，通过 left_has_more 来指示。
            if left[0] > 2:
                left_has_more = True

            # 如果最左边的页码号比第 1 页的页码号大，说明当前页左边的连续页码号中不包含第一页的页码，
            # 所以需要显示第一页的页码号，通过 first 来指示
            if left[0] > 1:
                first = True
        else:
            # 用户请求的既不是最后一页，也不是第 1 页，则需要获取当前页左右两边的连续页码号，
            # 这里只获取了当前页码前后连续两个页码，你可以更改这个数字以获取更多页码。
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
            right = page_range[page_number:page_number + 2]

            # 是否需要显示最后一页和最后一页前的省略号
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True

            # 是否需要显示第 1 页和第 1 页后的省略号
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True

        data = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
        }

        return data


class TagAdmin(ListView):
    model = Txt
    template_name = 'legalfiles/tag_admin.html'
    context_object_name = 'txts'
    paginate_by = 7
    def get_queryset(self):

        #查出标签前看一下url来判断是什么操作，三空就是进入标签管理
        if self.kwargs.get('tag_name')!=' ' or self.kwargs.get('txt_name')!=' ' or self.kwargs.get('status')!=' ':
            if self.kwargs.get('status')=='delete':
                #点击了左侧的标签
                if self.kwargs.get('txt_name') ==' ':
                      deletetag.delete_tag(self.request,self.kwargs.get('tag_name'))
                #点击了某篇文章的标签
                else :
                    deletetxttags.delete_txttags(self.request,self.kwargs.get('tag_name'),self.kwargs.get('txt_name'))
            else:
                #点击了添加按钮
                addtag.add_tag(self.request,self.kwargs.get('tag_name'))
                addtxttag.add_txttag(self.request,self.kwargs.get('txt_name'),self.kwargs.get('tag_name'))


        return Txt.objects.filter(users_id=self.request.user)

    def get_context_data(self, **kwargs):
        """
        在视图函数中将模板变量传递给模板是通过给 render 函数的 context 参数传递一个字典实现的，
        例如 render(request, 'blog/index.html', context={'post_list': post_list})，
        这里传递了一个 {'post_list': post_list} 字典给模板。
        在类视图中，这个需要传递的模板变量字典是通过 get_context_data 获得的，
        所以我们复写该方法，以便我们能够自己再插入一些我们自定义的模板变量进去。
        """
        # 首先获得父类生成的传递给模板的字典。
        context = super(TagAdmin, self).get_context_data(**kwargs)
        context['mytags'] = get_tags(get_mytags(self.request))
        # txttags = []
        # mytxts = Txt.objects.filter(users_id=self.request.user)
        # for mytxt in mytxts:
        #     txt_tag = Txt.objects.filter(txt_id=mytxt.txt_id).values_list("tags")
        #     for tag_id in txt_tag:
        #         # mytags_id.add(tag_id[0])
        #         txttags.append(Tag.objects.get(id=tag_id[0]).name)
        #     txttags.append("#")
        # context['txttags']=txttags

        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')

        # 调用自己写的 pagination_data 方法获得显示分页导航条需要的数据，见下方。
        pagination_data = self.pagination_data(paginator, page, is_paginated)

        # 将分页导航条的模板变量更新到 context 中，注意 pagination_data 方法返回的也是一个字典。
        context.update(pagination_data)

        # 将更新后的 context 返回，以便 ListView 使用这个字典中的模板变量去渲染模板。
        # 注意此时 context 字典中已有了显示分页导航条所需的数据。
        #我写：这个就是返回给html的字典
        return context

    def pagination_data(self, paginator, page, is_paginated):
        if not is_paginated:
            # 如果没有分页，则无需显示分页导航条，不用任何分页导航条的数据，因此返回一个空的字典
            return {}

        # 当前页左边连续的页码号，初始值为空
        left = []

        # 当前页右边连续的页码号，初始值为空
        right = []

        # 标示第 1 页页码后是否需要显示省略号
        left_has_more = False

        # 标示最后一页页码前是否需要显示省略号
        right_has_more = False

        # 标示是否需要显示第 1 页的页码号。
        # 因为如果当前页左边的连续页码号中已经含有第 1 页的页码号，此时就无需再显示第 1 页的页码号，
        # 其它情况下第一页的页码是始终需要显示的。
        # 初始值为 False
        first = False

        # 标示是否需要显示最后一页的页码号。
        # 需要此指示变量的理由和上面相同。
        last = False

        # 获得用户当前请求的页码号
        page_number = page.number

        # 获得分页后的总页数
        total_pages = paginator.num_pages

        # 获得整个分页页码列表，比如分了四页，那么就是 [1, 2, 3, 4]
        page_range = paginator.page_range

        if page_number == 1:
            # 如果用户请求的是第一页的数据，那么当前页左边的不需要数据，因此 left=[]（已默认为空）。
            # 此时只要获取当前页右边的连续页码号，
            # 比如分页页码列表是 [1, 2, 3, 4]，那么获取的就是 right = [2, 3]。
            # 注意这里只获取了当前页码后连续两个页码，你可以更改这个数字以获取更多页码。
            right = page_range[page_number:page_number + 2]

            # 如果最右边的页码号比最后一页的页码号减去 1 还要小，
            # 说明最右边的页码号和最后一页的页码号之间还有其它页码，因此需要显示省略号，通过 right_has_more 来指示。
            if right[-1] < total_pages - 1:
                right_has_more = True

            # 如果最右边的页码号比最后一页的页码号小，说明当前页右边的连续页码号中不包含最后一页的页码
            # 所以需要显示最后一页的页码号，通过 last 来指示
            if right[-1] < total_pages:
                last = True

        elif page_number == total_pages:
            # 如果用户请求的是最后一页的数据，那么当前页右边就不需要数据，因此 right=[]（已默认为空），
            # 此时只要获取当前页左边的连续页码号。
            # 比如分页页码列表是 [1, 2, 3, 4]，那么获取的就是 left = [2, 3]
            # 这里只获取了当前页码后连续两个页码，你可以更改这个数字以获取更多页码。
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]

            # 如果最左边的页码号比第 2 页页码号还大，
            # 说明最左边的页码号和第 1 页的页码号之间还有其它页码，因此需要显示省略号，通过 left_has_more 来指示。
            if left[0] > 2:
                left_has_more = True

            # 如果最左边的页码号比第 1 页的页码号大，说明当前页左边的连续页码号中不包含第一页的页码，
            # 所以需要显示第一页的页码号，通过 first 来指示
            if left[0] > 1:
                first = True
        else:
            # 用户请求的既不是最后一页，也不是第 1 页，则需要获取当前页左右两边的连续页码号，
            # 这里只获取了当前页码前后连续两个页码，你可以更改这个数字以获取更多页码。
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
            right = page_range[page_number:page_number + 2]

            # 是否需要显示最后一页和最后一页前的省略号
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True

            # 是否需要显示第 1 页和第 1 页后的省略号
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True

        data = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
        }

        return data

class IndexView(ListView):
    model = Txt
    template_name = 'legalfiles/index.html'
    context_object_name = 'txts'
    paginate_by =7
    def get_queryset(self):
        #MyTagsIndex.as_view()

        return Txt.objects.filter(users_id=self.request.user)



    def get_context_data(self, **kwargs):
        """
        在视图函数中将模板变量传递给模板是通过给 render 函数的 context 参数传递一个字典实现的，
        例如 render(request, 'blog/index.html', context={'post_list': post_list})，
        这里传递了一个 {'post_list': post_list} 字典给模板。
        在类视图中，这个需要传递的模板变量字典是通过 get_context_data 获得的，
        所以我们复写该方法，以便我们能够自己再插入一些我们自定义的模板变量进去。
        """
        context = super(IndexView, self).get_context_data(**kwargs)
        context['mytags'] = get_tags(get_mytags(self.request))
        # 首先获得父类生成的传递给模板的字典。
        #context = super(IndexView, self).get_context_data(**kwargs)
        # 父类生成的字典中已有 paginator、page_obj、is_paginated 这三个模板变量，
        # paginator 是 Paginator 的一个实例，
        # page_obj 是 Page 的一个实例，
        # is_paginated 是一个布尔变量，用于指示是否已分页。
        # 例如如果规定每页 10 个数据，而本身只有 5 个数据，其实就用不着分页，此时 is_paginated=False。
        # 关于什么是 Paginator，Page 类在 Django Pagination 简单分页：http://zmrenwu.com/post/34/ 中已有详细说明。
        # 由于 context 是一个字典，所以调用 get 方法从中取出某个键对应的值。
        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')

        # 调用自己写的 pagination_data 方法获得显示分页导航条需要的数据，见下方。
        pagination_data = self.pagination_data(paginator, page, is_paginated)

        # 将分页导航条的模板变量更新到 context 中，注意 pagination_data 方法返回的也是一个字典。
        context.update(pagination_data)

        # 将更新后的 context 返回，以便 ListView 使用这个字典中的模板变量去渲染模板。
        # 注意此时 context 字典中已有了显示分页导航条所需的数据。
        #我写：这个就是返回给html的字典
        return context

    def pagination_data(self, paginator, page, is_paginated):
        if not is_paginated:
            # 如果没有分页，则无需显示分页导航条，不用任何分页导航条的数据，因此返回一个空的字典
            return {}

        # 当前页左边连续的页码号，初始值为空
        left = []

        # 当前页右边连续的页码号，初始值为空
        right = []

        # 标示第 1 页页码后是否需要显示省略号
        left_has_more = False

        # 标示最后一页页码前是否需要显示省略号
        right_has_more = False

        # 标示是否需要显示第 1 页的页码号。
        # 因为如果当前页左边的连续页码号中已经含有第 1 页的页码号，此时就无需再显示第 1 页的页码号，
        # 其它情况下第一页的页码是始终需要显示的。
        # 初始值为 False
        first = False

        # 标示是否需要显示最后一页的页码号。
        # 需要此指示变量的理由和上面相同。
        last = False

        # 获得用户当前请求的页码号
        page_number = page.number

        # 获得分页后的总页数
        total_pages = paginator.num_pages

        # 获得整个分页页码列表，比如分了四页，那么就是 [1, 2, 3, 4]
        page_range = paginator.page_range

        if page_number == 1:
            # 如果用户请求的是第一页的数据，那么当前页左边的不需要数据，因此 left=[]（已默认为空）。
            # 此时只要获取当前页右边的连续页码号，
            # 比如分页页码列表是 [1, 2, 3, 4]，那么获取的就是 right = [2, 3]。
            # 注意这里只获取了当前页码后连续两个页码，你可以更改这个数字以获取更多页码。
            right = page_range[page_number:page_number + 2]

            # 如果最右边的页码号比最后一页的页码号减去 1 还要小，
            # 说明最右边的页码号和最后一页的页码号之间还有其它页码，因此需要显示省略号，通过 right_has_more 来指示。
            if right[-1] < total_pages - 1:
                right_has_more = True

            # 如果最右边的页码号比最后一页的页码号小，说明当前页右边的连续页码号中不包含最后一页的页码
            # 所以需要显示最后一页的页码号，通过 last 来指示
            if right[-1] < total_pages:
                last = True

        elif page_number == total_pages:
            # 如果用户请求的是最后一页的数据，那么当前页右边就不需要数据，因此 right=[]（已默认为空），
            # 此时只要获取当前页左边的连续页码号。
            # 比如分页页码列表是 [1, 2, 3, 4]，那么获取的就是 left = [2, 3]
            # 这里只获取了当前页码后连续两个页码，你可以更改这个数字以获取更多页码。
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]

            # 如果最左边的页码号比第 2 页页码号还大，
            # 说明最左边的页码号和第 1 页的页码号之间还有其它页码，因此需要显示省略号，通过 left_has_more 来指示。
            if left[0] > 2:
                left_has_more = True

            # 如果最左边的页码号比第 1 页的页码号大，说明当前页左边的连续页码号中不包含第一页的页码，
            # 所以需要显示第一页的页码号，通过 first 来指示
            if left[0] > 1:
                first = True
        else:
            # 用户请求的既不是最后一页，也不是第 1 页，则需要获取当前页左右两边的连续页码号，
            # 这里只获取了当前页码前后连续两个页码，你可以更改这个数字以获取更多页码。
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
            right = page_range[page_number:page_number + 2]

            # 是否需要显示最后一页和最后一页前的省略号
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True

            # 是否需要显示第 1 页和第 1 页后的省略号
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True

        data = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
        }

        return data
