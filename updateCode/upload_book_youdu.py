import requests
from lxml import etree
import jsonpath
import json,os
from api_requests import sendRequest
from upload_book_sql import uploadBookSql
import os, time,shutil,re
from hashlib import md5
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient,ContentSettings
from cache_clear import cache_name,test_string_list, text_list


class upload_biqu_book(object):
    def __init__(self):
        connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
        self.blob_service_client=BlobServiceClient.from_connection_string(connect_str)
        self.req = sendRequest()
        self.biquSql = uploadBookSql()
        self.base_url = "http://www.biqugew.com"
        self.url=""
        self.parts_link = "https://4newtext.blob.core.windows.net/"
        self.cache_url = "http://api10.youduwen.com/book/part/clean-cache?"
        self.mengzeda = "https://www.mengzeda.cn"
        self.kanxs = "https://www.5kanxs.com"
        self.yqhy = "https://www.yqhy.org"
        self.basePath = "E:/youduAPP/"


    def uploadBook(self):
        global chapterParts, timeStr
        timeStr = int(time.time())
        try:
            # 请求链接拿到json书籍数据
            res = self.req.send_request(self.url).content
            dictData = json.loads(res)
        except:
            res = requests.get(self.url, timeout=30).content
            dictData = json.loads(res)

        book_status_list = jsonpath.jsonpath(dictData, "$.data[*]..book_status")
        book_id_list = jsonpath.jsonpath(dictData, "$.data[*]..id") # 书id
        book_author_list = jsonpath.jsonpath(dictData, "$.data[*]..book_author") #作者
        book_name_list = jsonpath.jsonpath(dictData, "$.data[*]..book_name") # 书名
        chapter_parts_list = jsonpath.jsonpath(dictData, "$.data[*]..parts") # parts
 
        upload_chapterNum_list = []
        for bookStatus, bookId, bookAuthor, bookName, chapterParts in zip(book_status_list, book_id_list, book_author_list, book_name_list,chapter_parts_list):
 
            dbData_list = self.biquSql.selectBookName(bookName, bookAuthor)  
            if len(dbData_list) == 0:
                print(f"这本书数据库没有记录-->[{bookName}]")
                continue
            try:
                # 请求书籍章节
                res2 = self.req.send_request(self.parts_link + chapterParts).content
            except Exception as e:
                print("[请求章节接口出现异常信息]__:", e)
                continue

            dict_data = json.loads(res2)
            try:
                chapter_index_list = jsonpath.jsonpath(dict_data, "$..number")
                last_chapter_name_list = jsonpath.jsonpath(dict_data, "$..title") 
                chapterIndex = chapter_index_list[-1]
                lastChapterName = last_chapter_name_list[-1] 

                for web_site, _id, book_url in dbData_list:
                    if web_site == 'biqu2' or web_site=="bbiquge" or web_site =="mengzeda" or web_site=="xiaoshuo5" or web_site == "33yq" or web_site == "biquge" or web_site=="bjgjwy" or web_site == "dhzw" or web_site == "biquguan" or web_site == "78zw" or web_site == "biduo" or web_site == "xs386" or web_site == "23txt" or web_site == "huangyixiaoshuo" or web_site == "91baby" or web_site == "tianxiabachang" or web_site == "biqubao" or web_site == "pinshu" or web_site=="booktxt" or web_site=="xsw5":
                        
                        print(f"【现在更新的是{web_site}站点】")
                        _book_id = self.update_biqu2_chapter(bookId, web_site, _id, bookName, lastChapterName, chapterIndex, book_url, bookAuthor, last_chapter_name_list, dict_data)
                        if isinstance(_book_id, int):
                            upload_chapterNum_list.append(_book_id)

                    elif web_site == "biqutxt" or web_site== "5kanxs" or web_site== "yqhy" or web_site=="lianzais":
                        print(f"【现在更新的是{web_site}站点】")
                        _book_id = self.update_aile_book(bookId, web_site, _id, book_url, bookName, lastChapterName, chapterIndex, bookAuthor, last_chapter_name_list, dict_data)
                        if isinstance(_book_id, int):
                            upload_chapterNum_list.append(_book_id)

                    elif web_site == '2kxs' or web_site == "zuimeng" or web_site == "kanshu8" or web_site == "jjwxc":
                        print(f"【现在更新的是{web_site}站点】")
                        _book_id = self.update_2kxs_book(bookId, web_site, _id, bookName, lastChapterName, book_url, chapterIndex, bookAuthor, last_chapter_name_list, dict_data)
                        if isinstance(_book_id, int):
                            upload_chapterNum_list.append(_book_id)
                    
                    elif web_site == 'biquinfo' or web_site == 'shusvip' or web_site == "nbaxiaoshuo" or web_site == "mmmli" or web_site == "kenshu":
                        print(f"【现在更新的是{web_site}站点】")
                        _book_id = self.update_biquinfo_book(bookId, web_site, _id, bookName, bookAuthor, lastChapterName, book_url, chapterIndex, last_chapter_name_list, dict_data)
                        if isinstance(_book_id, int):
                            upload_chapterNum_list.append(_book_id)

                    elif web_site == "liudatxt" or web_site == "dingdianorg" or web_site == "shuhaige" or web_site == "biqusa" or web_site =="bqg5" or web_site == "xxxbiquge" or web_site == "999xs" or web_site == "biqugetv" or web_site =="biqugela" or web_site == "geilwx":
                        print(f"【现在更新的是{web_site}站点】")

                        _book_id = self.update_aszw_book(bookId, web_site, _id, bookName, lastChapterName, chapterIndex, book_url, bookAuthor, last_chapter_name_list, dict_data)
                        if isinstance(_book_id, int):
                            upload_chapterNum_list.append(_book_id)

                    elif web_site == "biqushu" or web_site == "f96" or web_site == "longwangtai":
                        print(f"【现在更新的是{web_site}站点】")
                        _book_id = self.update_biqushu_book(bookId, web_site, _id, bookName, lastChapterName, chapterIndex, book_url, bookAuthor, last_chapter_name_list, dict_data)
                        if isinstance(_book_id, int):
                            upload_chapterNum_list.append(_book_id)

                    else:
                        print("【现在更新的是其他的站点~~~】")
                        _book_id = self.update_newbiqu_book(web_site, book_url, bookId, _id, bookName, bookAuthor, lastChapterName, chapterIndex, last_chapter_name_list, dict_data)
                        if isinstance(_book_id, int):
                            upload_chapterNum_list.append(_book_id)

            except Exception as e:
                print("******", e)

        if upload_chapterNum_list == []:
            return
        try:
            api_url = "http://api10.youduwen.com/v2/app/j-push/book-renew-push"
            params = {
                "book_id": str(upload_chapterNum_list)
            }
            res = requests.post(api_url, params, timeout=30).text
            print("【推荐书籍ID成功~】__")
        except Exception as e:
            print("【*推荐书本ID失败*】", e)

        # 删除本地存放书籍内容的文件夹,所有更新书籍!
        shutil.rmtree(self.basePath)

    def process_chapterIndex(self, chapter_name_list, lastChapterName, bookName, last_chapter_name_list, chapterIndex, dict_data, recursive):
        try:
            count_index = []
            for index, chapterName in enumerate(chapter_name_list, 1):
                if lastChapterName == chapterName:
                    count_index.append(index)
            if len(count_index) == 1:
                newChapterIndex = count_index[0]
            else:
                newChapterIndex = sorted(count_index)[-1]
            return newChapterIndex, chapterIndex, dict_data
        except:
            try:
                newChapterName_list = [chapterName.replace("  ","").strip() for chapterName in chapter_name_list]
                count_index2 = []
                for index, chapterName in enumerate(newChapterName_list, 1):
                    if lastChapterName==chapterName:
                        count_index2.append(index)
                
                if len(count_index2) == 1:
                    newChapterIndex = count_index2[0]
                else:
                    newChapterIndex = sorted(count_index2)[-1]
                return newChapterIndex, chapterIndex, dict_data
            except Exception as e:
                # if recursive < 3:
                #     del last_chapter_name_list[-1] # 这个是接口里的章节列表
                #     lastName = last_chapter_name_list[-1]
                #     recursive += 1
                #     del dict_data[-1] #删除最后一章
                #     chapterIndex -= 1 #索引递减一

                #     self.process_chapterIndex(chapter_name_list, lastName, bookName, last_chapter_name_list, chapterIndex, dict_data, recursive)
                    
                #     return self.process_chapterIndex(chapter_name_list, lastName, bookName, last_chapter_name_list, chapterIndex, dict_data, recursive)
                # else:    
                print("章节名完全不对__", bookName)
                return False


    def all_book_path(self, web_site, bookName, bookAuthor):
        # 构建本地磁盘存储的路径
        webPath = f"{self.basePath}{web_site}/"  # 站点路径
        filename = md5((bookName + '-' + bookAuthor).encode("utf-8")).hexdigest()
        book_path = f'{webPath}{filename}/{timeStr}/'
        if os.path.exists(book_path) is False:
            os.makedirs(book_path)
        return book_path

    def upload_weiRuanYun(self, book_path, bookId, bookName, dict_data):
        md5Txt = chapterParts.split("/")[2] # 路径
        new_data = json.dumps(dict_data) # 数据
        # 写到本地文件夹
        with open(book_path + md5Txt, "w", encoding="utf-8") as f:
            f.write(new_data)

        blok = chapterParts.split("/")[0] + "/" + chapterParts.split("/")[1]
        my_content_settings=ContentSettings(content_type='text/plain;charset=utf-8')

        # 把这个路径里的数据迭代出来，分别上传
        if len(os.listdir(book_path)) > 1:
            for chapterTxt in os.listdir(book_path):
                # num=0
                # while num < 5:
                try:
                    blob_client = self.blob_service_client.get_blob_client(container=blok, blob=chapterTxt)

                    with open(book_path+chapterTxt, "rb") as data:
                        blob_client.upload_blob(data, overwrite=True, content_settings=my_content_settings)
                    # num += 5
                except:
                        # num += 1
                    print(f"上传失败~{bookName}")

            self.cache_clear(bookId, bookName)

            for k,v in cache_name.items():
                if bookName == k:
                    for _id in v:
                        self.cache_clear(_id, k)

    def cache_clear(self, bookId, bookName):
        params = {
            "book_id": bookId
        }
        res = self.req.send_request(self.cache_url, params)
        info = json.loads(res)
        print("【清除缓存后返回的信息,书籍对应的马甲包会同步清除缓存~】:",info["message"],bookName)

    def parse_chapterLink(self, web_site, chapterLink, book_url):
        if web_site=="jjwxc" or web_site=="longwangtai" or web_site=="yqhy":
            chapter_url = chapterLink
        elif web_site == "mengzeda":
            chapter_url = "https://www.mengzeda.cn" + chapterLink
        elif web_site == "xiaoshuo5":
            chapter_url = "https://www.xiaoshuo5.org" + chapterLink
        elif web_site == "33yq":
            chapter_url = "https://www.33yq.com" + chapterLink  
        elif web_site == "f96":
            chapter_url = "https://www.f96.net" + chapterLink
        elif web_site == "kanshu8":
            chapter_url = "http://www.kanshu8.net" + chapterLink
        elif web_site == "bjgjwy":
            chapter_url = "http://www.bjgjwy.net" + chapterLink
        elif web_site == "biquguan":
            chapter_url = "https://www.biquguan.com" + chapterLink
        elif web_site == "78zw":
            chapter_url = "https://www.78zw.com" + chapterLink
        elif web_site == "nbaxiaoshuo":
            chapter_url = "http://www.nbaxiaoshuo.com" + chapterLink
        elif web_site == "xs386":
            chapter_url = "https://www.xs386.com" + chapterLink
        elif web_site == "biqubao":
            chapter_url = "https://www.biqubao.com" + chapterLink
        elif web_site == "23txt":
            chapter_url = "https://www.23txt.com" + chapterLink
        elif web_site == "huangyixiaoshuo":
            chapter_url = "https://www.huangyixiaoshuo.com" + chapterLink
        elif web_site == "dingdianorg":
            chapter_url = "https://www.dingdianorg.com" + chapterLink
        elif web_site == "shuhaige":
            chapter_url = "https://www.shuhaige.net" + chapterLink
        elif web_site == "bqg5":
            chapter_url = "https://www.bqg5.cc" + chapterLink
        elif web_site == "91baby":
            chapter_url = "http://www.91baby.org" + chapterLink
        elif web_site == "xxxbiquge":
            chapter_url = "https://www.xxxbiquge.com" + chapterLink
        elif web_site == "biqusa":
            chapter_url = "https://www.biqusa.com" + chapterLink
        elif web_site == "999xs":
            chapter_url = "https://www.999xs.com" + chapterLink
        elif web_site == "biqugetv":
            chapter_url = "https://www.biqugetv.com" + chapterLink
        elif web_site == "kenshu":
            chapter_url = "http://www.kenshuzw.com" + chapterLink
        elif web_site == "biqugela":
            chapter_url = "https://www.biqugela.com" + chapterLink
        elif web_site == "geilwx":
            chapter_url = "https://www.geilwx.com" + chapterLink 
        elif web_site == "biduo":
            chapter_url = "https://www.biduo.cc" + chapterLink
        elif web_site == "tianxiabachang":
            chapter_url = "http://www.tianxiabachang.cn" + chapterLink
        elif web_site == "biqutxt":
            chapter_url = "http://www.biqutxt.com" + chapterLink  
        elif web_site == "5kanxs":
            chapter_url = self.kanxs + chapterLink
        elif web_site=="booktxt":
            chapter_url = "https://www.booktxt.com" + chapterLink    
        elif web_site == "lianzais":
            chapter_url = "http://www.lianzais.com" + chapterLink
        elif web_site == "xsw5":
            chapter_url = "https://www.xsw5.com" + chapterLink   
        else:
            chapter_url = book_url + chapterLink
       
        res2 = self.req.send_request(chapter_url)
        return res2, chapter_url


    def parse_textLink(self, web_site, res2, bookName, chapter_url):
        # 解析详情页的文章内容text
        try:
            html = etree.HTML(res2.content)
            if web_site == "2kxs":
                chapter_content_list = html.xpath("//p[@class='Text']/text()")
            elif web_site=="kushubao":
                r = res2.text
                b = r.encode('ISO-8859-1', errors='replace').decode(requests.utils.get_encodings_from_content(r)[0], errors='replace')
                html = etree.HTML(b)
                chapter_content_list = html.xpath("//div[@id='htmlContent']/text()")
        
            elif web_site == "biqugeso":
                chapter_content_list = html.xpath("//div[@id='content']/div[3]/text()")
           
            elif web_site == "zuimeng":
                chapter_content_list = html.xpath("//p[@id='articlecontent']/text()")
            elif web_site == "33yq" or web_site == "yqhy":
                html = etree.HTML(res2.text)
                chapter_content_list = html.xpath("//div[@id='content']/p/text()")
            elif web_site == "kanshu8":
                chapter_content_list = html.xpath("//div[@class='size16 color5 pt-read-text']/p/text()")     
          
            elif web_site == "dhzw":
                chapter_content_list = html.xpath("//div[@id='BookText']/text()")
            
            elif web_site == "shusvip" or web_site == "bqg5" or web_site == "biqugela" or web_site == "geilwx" or web_site == "xsw5":
                chapter_content_list = html.xpath("//div[@id='content']/p/text()") 
            
            elif web_site == "biqushu" or web_site == "biquinfo2" or web_site=="f96":
                r = res2.text
                b = r.encode('ISO-8859-1', errors='replace').decode(requests.utils.get_encodings_from_content(r)[0], errors='replace')
                html = etree.HTML(b)
                chapter_content_list = html.xpath("//div[@id='htmlContent']/text()")
            elif web_site == "nbaxiaoshuo":
                chapter_content_list = html.xpath("//div[@class='readcotent001 readcotent font-normal']/p/text() | //div[@class='readcotent font-normal']/text()")

            elif web_site == "mmmli" or web_site == "shuhaige":
                chapter_content_list = html.xpath("//div[@class='content']/text()")
            elif web_site == "jjwxc":
                chapter_content_list = html.xpath("//div[@class='noveltext']/text()") 
            elif web_site == "dingdianorg":
                html = etree.HTML(res2.text)
                chapter_content_list = html.xpath("//div[@id='TXT']/text()")
            
            elif web_site == "longwangtai":
                chapter_content_list = html.xpath("//div[@id='BookText']/p/text()")
            elif web_site == "kenshu":
                chapter_content_list = html.xpath("//div[@class='article-con']/text()")

            elif web_site == "5kanxs":
                chapter_content_list=html.xpath("//div[@id='htmlContent']/p/text()") 
            elif web_site == "lianzais":
                chapter_content_list=html.xpath("//div[@id='read-content']/p/text()")     
            else:
                chapter_content_list = html.xpath("//div[@id='content']/text()")
        except:
            print(f"--请求章节内容没有成功~--{bookName}----{chapter_url}")            

        return chapter_content_list, html


    def parse_next_text(self, web_site, nextLink):
        res3 = self.req.send_request(nextLink)
        html_obj2 = etree.HTML(res3.content)
        if web_site == "biquinfo2":
            next_content_list2 = html_obj2.xpath("//*[@id='htmlContent']/text()")
        elif web_site == "biqugeso":
            next_content_list2 = html_obj2.xpath("//*[@id='content']/div[3]/text()")
        elif web_site == "5kanxs":
            next_content_list2 = html_obj2.xpath("//*[@id='htmlContent']/p/text()")
        else:
            next_content_list2 = html_obj2.xpath("//div[@id='content']/text()")
        return next_content_list2

    def parse_three_method(self, nextLink):
        res = self.req.send_request(nextLink)
        html_obj = etree.HTML(res.text)
        next_content_list2 = html_obj.xpath("//div[@id='content']/p/text()")     
        s_content=""
        for second in next_content_list2:
            s_content += second.strip() + '\n'
        # 万一有第三页的情况存在:
        three_link = html_obj.xpath("//div[@id='thumb']/a[3]/@href")[0]
        
        if "_" in three_link:
            new_three_link = self.yqhy+three_link
            print("这个就是第三页的内容", new_three_link)
            res2 = self.req.send_request(new_three_link).text
            html_obj2 = etree.HTML(res2)
            three_content_list = html_obj2.xpath("//div[@id='content']/p/text()")
            
            three_content=""
            for t in three_content_list:
                three_content += t.strip() + '\n'
            return s_content + "\n" + three_content
        else:
            return s_content

    def total_method(self, chapter_name_list, chapter_link_list, bookName, bookId, web_site, book_url, lastChapterName, chapter_index, bookAuthor, _id, last_chapter_name_list, dict_data):

        recursive=0
        # 下标索引!
        newChapterIndex, chapterIndex, dict_data = self.process_chapterIndex(chapter_name_list, lastChapterName, bookName, last_chapter_name_list, chapter_index, dict_data, recursive)
       
        if newChapterIndex is False:
            return
        if chapter_name_list[newChapterIndex:]:
            # 所有书籍路径!
            book_path = self.all_book_path(web_site, bookName, bookAuthor)
            
            index = 0
            self.next_content = ""
            for chapter_name, chapterLink in zip(chapter_name_list[newChapterIndex:],chapter_link_list[newChapterIndex:]):
                res2, chapter_url = self.parse_chapterLink(web_site, chapterLink, book_url)
                
                if res2 is False:
                    break
                # 第一页内容
                chapter_content_list, html=self.parse_textLink(web_site, res2, bookName,chapter_url)
                
                Content = ''
                for text in chapter_content_list:
                    Content += '  '+text.replace('\n','').strip().replace('\r\n', '')+'\n'
                for t in test_string_list:
                    newContent = Content.strip().replace(t, '')
                
                if len(newContent.strip().replace('\n', '')) < 300:
                    continue
                
                next_text = ''
                index += 1
                chapterIndex2 = int(chapterIndex) + index
                if web_site == "biqugeso" or web_site=="kushubao" or web_site == "mengzeda" or web_site == "biquinfo2" or web_site=="5kanxs" or web_site=="yqhy":

                    if web_site == "mengzeda":
                        next_page_list = html.xpath("//div[@class='bottem2']/a[4]/text()")
                    elif web_site == "biquinfo2" or web_site=="5kanxs":
                        next_page_list = html.xpath("//a[@id='linkNext']/text()")
                    elif web_site == "yqhy":
                        next_page_list = ["下一页"]       
                    else:    
                        next_page_list= html.xpath("//p[@class='text-center']/a[3]/text()")

                    if next_page_list[0] == "下一页" or next_page_list[0] =="下一页(→)":
                        next_text_link = html.xpath("//div[@class='bottem2']/a[4]/@href")
                        if web_site == "mengzeda":
                            next_content_url = self.mengzeda + next_text_link[0]
                        elif web_site == "5kanxs":
                            next_content_url = self.kanxs + html.xpath("//a[@id='linkNext']/@href")[0]    
                        
                        elif web_site == "yqhy":
                            next_link = html.xpath("//div[@id='thumb']/a[3]/@href")[0]
                            if "_" in next_link:
                                next_content_url = self.yqhy + next_link
                            else:
                                print("因为没第二页内容，只采了第一页是:",chapter_name)
                                self.writeLocalFile(book_path,next_text,newContent,chapterIndex2,chapter_name,chapter_url,dict_data)
                                continue
                        else:    
                            next_content_url= html.xpath("//a[@id='linkNext']/@href")[0]

                        print("正采集第二页内容:",bookName,chapter_name,next_content_url)
                        
                        if web_site == "yqhy":
                            # 处理第2, 3页
                            self.next_content=self.parse_three_method(next_content_url)
                        else:
                            next_content_list2 = self.parse_next_text(web_site,next_content_url)
                            for secondText in next_content_list2:
                                next_text += '  ' + secondText.strip().replace(text_list[0], '').replace(text_list[1], '').replace("</p>", '').replace(chapter_name, '') + '\n'
               
                print(f"【{web_site}】现在更新的书是第:{bookName}-{chapterIndex2}-{chapter_name}")
                self.writeLocalFile(book_path,next_text,newContent,chapterIndex2,chapter_name,chapter_url,dict_data)
            try:
                self.upload_weiRuanYun(book_path, bookId, bookName, dict_data)
                return bookId
            except Exception as e:
                print(f"{web_site}__:上传更新失败!", e)
        else:
            print(f"【{web_site}__:这本书在这个站点没有更新新的章节】", bookName)


    def writeLocalFile(self, book_path, next_text, newContent,chapterIndex2, chapter_name,chapter_url,dict_data):
        allPath = book_path + str(chapterIndex2) + '.txt'
        
        if next_text:
            allContent = (newContent + '\n' + next_text).replace(f"笔趣阁 www.biqu.info，", '')
            with open(allPath, 'w', encoding="utf-8") as f:
                f.write(allContent)
        elif self.next_content:
            allContent2 = (newContent + '\n' + self.next_content)
            with open(allPath, 'w', encoding="utf-8") as f:
                f.write(allContent2)
        else:
            with open(allPath, 'w', encoding="utf-8") as f:
                f.write(newContent)

        label_path = ''.join(re.findall(r'(.*)/',chapterParts))+f'/{chapterIndex2}.txt'
        data = {"title": chapter_name, "content": label_path, "number": chapterIndex2, "create_time": timeStr, "update_time": timeStr, "url": chapter_url}
        dict_data.append(data)                

    def update_biqu2_chapter(self, bookId, web_site, _id, bookName, lastChapterName, chapterIndex, book_url, bookAuthor, last_chapter_name_list, dict_data):
        if book_url:
            try:
                res = self.req.send_request(book_url).content
            except:
                try:
                   res = requests.get(book_url,timeout=30).content
                except:
                    return

            html_obj = etree.HTML(res)
            if web_site == "biqu2" or web_site == "bbiquge" or web_site == "33yq" or web_site == "biquge" or web_site == "dhzw" or web_site == "biduo" or web_site =="xs386" or web_site == "23txt" or web_site == "91baby" or web_site == "biqubao" or web_site == "pinshu" or web_site=="booktxt":
                chapter_name_list = html_obj.xpath("//div[@id='list']/dl/dd/a/text()") 
                chapter_link_list = html_obj.xpath("//div[@id='list']/dl/dd/a/@href") 

            elif web_site == "mengzeda" or web_site == "78zw" or web_site == "tianxiabachang" :
                chapter_name_list=html_obj.xpath("//div[@id='list']/dl/dd/a/text()")[9:]
                chapter_link_list = html_obj.xpath("//div[@id='list']/dl/dd/a/@href")[9:]
            
            elif web_site=="xiaoshuo5":
                chapter_name_list = html_obj.xpath("//div[@id='list']/dl/dd/a/text()")[10:]
                chapter_link_list = html_obj.xpath("//div[@id='list']/dl/dd/a/@href")[10:]
             
            else:
                chapter_list = html_obj.xpath("//div[@id='list']/dl/dd/a/text()")[12:]
                chapter_name_list=[i.replace("\n","").strip() for i in chapter_list if len(i)>=2]
                
                chapter_link_list = html_obj.xpath("//div[@id='list']/dl/dd/a/@href")[12:]

            if chapter_link_list == []:
                return

            bookId = self.total_method(chapter_name_list, chapter_link_list, bookName, bookId, web_site, book_url, lastChapterName, chapterIndex, bookAuthor, _id, last_chapter_name_list, dict_data)
            return bookId
        else:
            print("由于有一个站点被KILL,所以换到另外一个方法~")
            self.update_newbiqu_book(web_site, book_url, bookId, _id, bookName, bookAuthor, lastChapterName, chapterIndex, last_chapter_name_list, dict_data)

    def update_aile_book(self, bookId, web_site, _id, book_url, bookName, lastChapterName, chapterIndex, bookAuthor, last_chapter_name_list, dict_data):
        res = self.req.send_request(book_url).content
        html_obj = etree.HTML(res)
        
        if web_site =="biqutxt":
            chapter_name_list = html_obj.xpath("//div[@id='list1']/dl/dd/a/text()")[9:]
            chapter_link_list = html_obj.xpath("//div[@id='list1']/dl/dd/a/@href")[9:]
       
        elif web_site =="5kanxs":
            chapter_name_list = html_obj.xpath("//dd[@class='col-md-3']/a/text()")
            chapter_link_list = html_obj.xpath("//dd[@class='col-md-3']/a/@href")
        
        elif web_site =="lianzais":
            chapter_name_list = html_obj.xpath("//div[@class='chapter-list']/ul/li/a/text()")
            chapter_link_list = html_obj.xpath("//div[@class='chapter-list']/ul/li/a/@href")
        
        elif web_site =="yqhy":
            chapter_name_list = html_obj.xpath("//div[@class='article-list']/dl/dd/a/text()")
            link_list = html_obj.xpath("//div[@class='article-list']/dl/dd/a/@href")
            chapter_link_list = [i.replace("\n","") for i in link_list]

        else:
            res = self.req.send_request(book_url).text
            html_obj = etree.HTML(res)
            chapter_name_list = html_obj.xpath("//ul[@class='_chapter']/li/a/text()")
            chapter_link_list = html_obj.xpath("//ul[@class='_chapter']/li/a/@href") 

        bookId = self.total_method(chapter_name_list, chapter_link_list, bookName, bookId, web_site, book_url, lastChapterName, chapterIndex, bookAuthor, _id, last_chapter_name_list, dict_data)
        return bookId

    def update_2kxs_book(self, bookId, web_site, _id, bookName, lastChapterName, book_url, chapterIndex, bookAuthor, last_chapter_name_list, dict_data):
        res = self.req.send_request(book_url)
        html_obj = etree.HTML(res.content)
        if web_site == "2kxs":
            chapter_name_list = html_obj.xpath("//dl[@class='book']/dd/a/text()")[3:]
            chapter_link_list = html_obj.xpath("//dl[@class='book']/dd/a/@href")[3:]
           
        elif web_site == "kanshu8":
            chapter_name_list = html_obj.xpath("//div[@class='pt-chapter-cont-detail full']/a/text()")
            chapter_link_list = html_obj.xpath("//div[@class='pt-chapter-cont-detail full']/a/@href")
        elif web_site == "jjwxc":
            chapter_name_list = html_obj.xpath("//span[@itemprop='headline']/div/a/text()")
            chapter_link_list = html_obj.xpath("//span[@itemprop='headline']/div/a/@href")       
        else:
            chapter_name_list = html_obj.xpath("//div[@class='ml_list']/ul/li/a/text()")
            chapter_link_list = html_obj.xpath("//div[@class='ml_list']/ul/li/a/@href")
        
        new_name_list = [i.replace("\n","").strip() for i in chapter_name_list if len(i)>=2]
       
        bookId = self.total_method(new_name_list, chapter_link_list, bookName, bookId, web_site, book_url, lastChapterName, chapterIndex, bookAuthor, _id, last_chapter_name_list, dict_data)
        return bookId


    def update_biquinfo_book(self, bookId, web_site, _id, bookName, bookAuthor, lastChapterName, book_url, chapterIndex, last_chapter_name_list, dict_data):
        try:
            res = self.req.send_request(book_url).content
        except:
            res = requests.get(book_url, timeout=30).content
        
        html_obj = etree.HTML(res)
        if web_site == "biquinfo":
            chapter_name_list = html_obj.xpath("//div[@id='list']/dl/dd/a/text()") # 章节
            chapter_link_list = html_obj.xpath("//div[@id='list']/dl/dd/a/@href") # 链接
        elif web_site == "nbaxiaoshuo":
            chapter_name_list = html_obj.xpath("//div[@id='list-chapterAll']/div/dd/a/text()") # 章节
            chapter_link_list = html_obj.xpath("//div[@id='list-chapterAll']/div/dd/a/@href") 
        elif web_site == "mmmli":
            chapter_name_list = html_obj.xpath("//div[@class='volume']/dd/a/text()") 
            chapter_link_list = html_obj.xpath("//div[@class='volume']/dd/a/@href")
        elif web_site == "kenshu":
            chapter_name_list = html_obj.xpath("//ul[@class='clearfix chapter-list']/li/span/a/text()") # 章节
            chapter_link_list = html_obj.xpath("//ul[@class='clearfix chapter-list']/li/span/a/@href")             
        else:
            chapter_name_list = html_obj.xpath("//div[@class='chapterlist']/ul/li/a/text()") # 章节
            chapter_link_list = html_obj.xpath("//div[@class='chapterlist']/ul/li/a/@href")   
        # print(chapter_name_list)
        # return
        bookId = self.total_method(chapter_name_list, chapter_link_list, bookName, bookId, web_site, book_url, lastChapterName, chapterIndex, bookAuthor, _id, last_chapter_name_list, dict_data)
        return bookId

    def update_aszw_book(self, bookId, web_site, _id, bookName, lastChapterName, chapterIndex, book_url, bookAuthor, last_chapter_name_list, dict_data):
        r = self.req.send_request(book_url)
        html_obj = etree.HTML(r.content)
        if web_site == "dingdianorg":
            html_obj = etree.HTML(r.text)
            chapter_name_list = html_obj.xpath("//div[@id='list']/dl/dd/a/text()")[12:] # 章节名字
            chapter_link_list = html_obj.xpath("//div[@id='list']/dl/dd/a/@href")[12:]
        elif web_site == "999xs" or web_site == "biqugetv":
            chapter_name_list = html_obj.xpath("//div[@id='list']/dl/dd/a/text()") # 章节名字
            chapter_link_list = html_obj.xpath("//div[@id='list']/dl/dd/a/@href")
        
        elif web_site == "shuhaige":
            chapter_name_list = html_obj.xpath("//div[@class='novel_list']/dl/dd/a/text()") # 章节名字
            chapter_link_list = html_obj.xpath("//div[@class='novel_list']/dl/dd/a/@href")
        
        elif web_site == "biqusa" or web_site == "xxxbiquge" or web_site =="biqugela" or web_site == "geilwx":
            chapter_name_list = html_obj.xpath("//div[@id='list']/dl/dd/a/text()")[12:]
            chapter_link_list = html_obj.xpath("//div[@id='list']/dl/dd/a/@href")[12:]
        
        elif web_site == "bqg5":
            chapter_name_list = html_obj.xpath("//div[@id='list']/dl/dd/a/text()")[9:] # 章节名字
            chapter_link_list = html_obj.xpath("//div[@id='list']/dl/dd/a/@href")[9:]          
        else:
            chapter_name_list = html_obj.xpath("//div[@id='readerlist']/ul/li/a/text()") # 章节名字
            chapter_link_list = html_obj.xpath("//div[@id='readerlist']/ul/li/a/@href") # 章节链接

        new_name_list = [i.replace("\n","").strip() for i in chapter_name_list if len(i)>=2]

        bookId = self.total_method(new_name_list, chapter_link_list, bookName, bookId, web_site, book_url, lastChapterName,chapterIndex, bookAuthor, _id, last_chapter_name_list, dict_data)
        return bookId

    def update_biqushu_book(self, bookId, web_site, _id, bookName, lastChapterName, chapterIndex, book_url, bookAuthor, last_chapter_name_list, dict_data):
        try:    
            res = self.req.send_request(book_url).content
        except:
            try:
                res = requests.get(book_url,timeout=30).content
            except:
                return

        html_obj = etree.HTML(res)
        if web_site == "longwangtai":
            chapter_name_list = html_obj.xpath("//div[@class='booklist clearfix']/span/a/text()")  # 章节名字
            chapter_link_list = html_obj.xpath("//div[@class='booklist clearfix']/span/a/@href")
        else:
            chapter_name_list = html_obj.xpath("//ul[@class='mulu_list']/li/a/text()")  # 章节名字
            chapter_link_list = html_obj.xpath("//ul[@class='mulu_list']/li/a/@href")  # 章节链接
        bookId = self.total_method(chapter_name_list, chapter_link_list, bookName, bookId, web_site, book_url, lastChapterName, chapterIndex, bookAuthor, _id, last_chapter_name_list, dict_data)
        return bookId


    def update_heiyan_book(self, bookId, web_site, _id, bookName, lastChapterName, chapterIndex, book_url, bookAuthor, last_chapter_name_list, dict_data):
        # 黑岩收费站点~！
        res = self.req.send_request(book_url).text
        html_obj = etree.HTML(res)
        chapter_name_list = html_obj.xpath("//ul[@class='float-list fill-block']/li/a/text()")
        chapter_link_list = html_obj.xpath("//ul[@class='float-list fill-block']/li/a/@href")

        bookId = self.total_method(chapter_name_list, chapter_link_list, bookName, bookId, web_site, book_url, lastChapterName, chapterIndex, bookAuthor, _id, last_chapter_name_list, dict_data)
        return bookId

    def update_newbiqu_book(self, web_site, book_url, bookId, _id, bookName, bookAuthor, lastChapterName, chapterIndex, last_chapter_name_list, dict_data):
        if web_site == "biqugeso":
            res = self.req.send_request(book_url).content
        elif web_site == "biquinfo2" and book_url:
            res = self.req.send_request(book_url).content    
        else:
            biquInfo2 = self.biquSql.select_biquInfo_book(bookName, bookAuthor)
            for web_site, bookName, bookAuthor, book_url in biquInfo2:
                res = self.req.send_request(book_url).content

        html_obj = etree.HTML(res)
        chapter_name_list = html_obj.xpath("//dd[@class='col-md-3']/a/text()") # 章节名
        chapter_link_list = html_obj.xpath("//dd[@class='col-md-3']/a/@href") # 链接
        
        bookId = self.total_method(chapter_name_list, chapter_link_list, bookName, bookId, web_site, book_url, lastChapterName, chapterIndex, bookAuthor, _id, last_chapter_name_list, dict_data)
        
        return bookId

if __name__ == '__main__':
    print(time.strftime("%Y-%m-%d %H:%M:%S"))
    start = time.time()
    biqu = upload_biqu_book()
    biqu.uploadBook()
    end = time.time()
    print("耗时:_", end-start, time.strftime("%Y-%m-%d %H:%M:%S"))
