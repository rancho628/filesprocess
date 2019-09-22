#coding=utf-8

# """
# Description: 多类型文档格式转换为Txt工具
# """
#
import os,fnmatch
import docx2txt
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.converter import TextConverter, PDFPageAggregator
from pdfminer.layout import LAParams

from pdfminer.pdfparser import PDFParser
#from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfparser import PDFDocument



'''
功能描述：把输入的文件保存为txt格式
参数描述：1 filePath：文件路径  2 savePath：指定保存路径
'''
def Files2Txt(filePath,savePath=''):
    # try:
        # 1 切分路径：目录+文件名
        dirs,filename = os.path.split(filePath)
        #print('目录：',dirs,'\n文件名：',filename)

        # 2 修改转化后的文件名
        typename = os.path.splitext(filename)[-1].lower() # 获取后缀
        new_name = TranType(filename,typename) #根据后缀不同切了后缀
        #print('新的文件名：',new_name)

        # 3 文件转化后的保存路径
        if savePath=="":
            savePath = dirs
        else:
            savePath = savePath
        new_save_path = os.path.join(savePath,new_name)
        #print('保存路径：',new_save_path)


        # 4 加载处理应用，根据保存路径进行保存
        if typename=='.pdf':

            fp = open(filePath, 'rb')

            # 创建一个与文档相关的解释器
            parser = PDFParser(fp)

            # pdf文档的对象，与解释器连接起来
            doc = PDFDocument(parser=parser)
            parser.set_document(doc=doc)

            # 如果是加密pdf，则输入密码
            # doc._initialize_password()

            # 创建pdf资源管理器
            resource = PDFResourceManager()

            # 参数分析器
            laparam = LAParams()

            # 创建一个聚合器
            device = PDFPageAggregator(resource, laparams=laparam)

            # 创建pdf页面解释器
            interpreter = PDFPageInterpreter(resource, device)

            # 获取页面的集合
            for page in PDFPage.get_pages(fp):
                # 使用页面解释器来读取
                interpreter.process_page(page)

                # 使用聚合器来获取内容
                layout = device.get_result()
                for out in layout:
                    if hasattr(out, 'get_text'):

                        # 写入txt文件
                        fw = open(new_save_path, 'a')
                        fw.write(out.get_text())

        elif typename=='.docx':
            my_text = docx2txt.process(filePath)
            fpb = open(new_save_path, "w")
            for line in my_text.splitlines():
                if line !='':
                    fpb.write(line+'\n')
            fpb.close()



        # pythoncom.CoInitialize()
        # wordapp = client.Dispatch('Word.Application')
        # mytxt = wordapp.Documents.Open(filePath)
        # mytxt.SaveAs(new_save_path, 4)
        # mytxt.Close()

    # except Exception as e:
    #     print('抛出错误')


'''
功能描述：根据文件不同后缀都修改为txt
参数描述：1 filePath：文件路径  2 typename 文件后缀
返回数据：new_name 返回修改后的文件名
'''
def TranType(filename,typename):
    # 新的文件名称
    new_name = ""
    if typename == '.pdf' : # pdf->txt
        if fnmatch.fnmatch(filename,'*.pdf') :
            new_name = filename[:-4]+'.txt' # 截取".pdf"之前的文件名
        else: return
    elif typename == '.doc' or typename == '.docx' :  # word->txt
        if fnmatch.fnmatch(filename, '*.doc') :
            new_name = filename[:-4]+'.txt'
        elif fnmatch.fnmatch(filename, '*.docx'):
            new_name = filename[:-5]+'.txt'
        else: return
    else:
        print('警告：\n您输入[',typename,']不合法，本工具支持pdf/doc/docx格式,请输入正确格式。')
        return
    return new_name



if __name__ == '__main__':
    filePath1 = os.path.abspath('/Users/darren/Downloads/filesprocess/legalfiles/extracttext/nihao.docx')
    # Newpath = os.path.split(os.path.realpath(__file__))[0]
    # Files2Txt(filePath1, savePath=Newpath)
    Files2Txt(filePath1,'/Users/darren/Downloads/filesprocess/legalfiles/files2Txt')


