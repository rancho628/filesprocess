from django.shortcuts import render
from legalfiles.models import Txt,Tag
# Create your views here.
from django.http import HttpResponse
import os
import legalfiles.processtext.batchdealtext
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView
from legalfiles.operateobject import savetxt,savetag,savetxttags
from legalfiles.processtext.deletefiles import deletefiles,deletefiles2txt
from django.shortcuts import render, get_object_or_404
#表现层不是一个个的功能，只是中间人
#可以调用业务层，可以调用工具方法



class IndexView(ListView):
    model = Txt
    template_name = 'legalfiles/index.html'
    context_object_name = 'txts'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        """
        在视图函数中将模板变量传递给模板是通过给 render 函数的 context 参数传递一个字典实现的，
        例如 render(request, 'blog/index.html', context={'post_list': post_list})，
        这里传递了一个 {'post_list': post_list} 字典给模板。
        在类视图中，这个需要传递的模板变量字典是通过 get_context_data 获得的，
        所以我们复写该方法，以便我们能够自己再插入一些我们自定义的模板变量进去。
        """

        # 首先获得父类生成的传递给模板的字典。
        context = super(IndexView, self).get_context_data(**kwargs)

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

def to_upload(request):
    return render(request, 'legalfiles/upload.html')

def upload_file(request):
    # if request.method == "POST":    # 请求方法为POST时，进行处理
    myFile = request.FILES.getlist("myfile", None)  # 获取上传的文件，如果没有文件，则默认为None

    # if not myFile:
    #     return HttpResponse("no files for upload!")

    for f in myFile:
        destination = open('legalfiles\\files\\' + f.name, 'wb+')  # 打开特定的文件进行二进制的写操作
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
    legalfiles.operateobject.savetxt.save_txt()
    # 保存标签到数据库
    legalfiles.operateobject.savetag.save_tag()
    #
    legalfiles.operateobject.savetxttags.save_txttags()
    # 删除上传上来的文件和我们生成的txt文件
    deletefiles()
    deletefiles2txt()

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

class TagView(ListView  ):
    model = Txt
    template_name = 'legalfiles/index.html'
    context_object_name = 'txts'


    # def get_context_data(self, **kwargs):
    #     # 我们需要先继承至父模板的get_context_data方法，否则我们有很多方法将不能使用
    #     context = super(TagView, self).get_context_data(**kwargs)
    #     paginator = context.get('paginator')

    #有时候真的乱，这个查询对应标签的文本的功能不是应该写在业务层吗，但是教程就写在这里
    #重写了父类方法
    def get_queryset(self):
        # #根据页面传递来的name查询到tag
        # tag1 = get_object_or_404(Tag, name=self.kwargs.get('name1'))
        # tag2 = get_object_or_404(Tag, name=self.kwargs.get('name2'))
        # print(type(self.kwargs.get('name1')))
        #
        # #把有这个tag的文本返回
        # return super(TagView, self).get_queryset().filter(tags=tag1).filter(tags=tag2)

        ret = super(TagView, self).get_queryset()

        if self.kwargs.get('name1')!=' ':
          tag1 = get_object_or_404(Tag, name=self.kwargs.get('name1'))
          ret=ret.filter(tags=tag1)
        else:
          pass

        if self.kwargs.get('name2')!=' ':
          tag2 = get_object_or_404(Tag, name=self.kwargs.get('name2'))
          ret=ret.filter(tags=tag2)
        else:
          pass

        if self.kwargs.get('name3')!=' ':
          tag3 = get_object_or_404(Tag, name=self.kwargs.get('name3'))
          ret=ret.filter(tags=tag3)
        else:
          pass

        if self.kwargs.get('name4')!=' ':
          tag4 = get_object_or_404(Tag, name=self.kwargs.get('name4'))
          ret=ret.filter(tags=tag4)
        else:
          pass

        if self.kwargs.get('name5')!=' ':
          tag5 = get_object_or_404(Tag, name=self.kwargs.get('name5'))
          ret=ret.filter(tags=tag5)
        else:
          pass

        if self.kwargs.get('name6')!=' ':
          tag6 = get_object_or_404(Tag, name=self.kwargs.get('name6'))
          ret=ret.filter(tags=tag6)
        else:
          pass

        if self.kwargs.get('name7')!=' ':
          tag7 = get_object_or_404(Tag, name=self.kwargs.get('name7'))
          ret=ret.filter(tags=tag7)
        else:
          pass

        if self.kwargs.get('name8')!=' ':
          tag8 = get_object_or_404(Tag, name=self.kwargs.get('name8'))
          ret=ret.filter(tags=tag8)
        else:
          pass

        return ret
