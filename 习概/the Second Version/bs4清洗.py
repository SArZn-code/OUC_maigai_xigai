import requests
from bs4 import BeautifulSoup as BS
import json

def main():
    file = open('E:/桌面/习概/all_link.txt','w', encoding='utf-8')
    json_file = open('E:/桌面/习概/习概预题库.json','w+',encoding='utf-8')

    url = 'https://wlkc.ouc.edu.cn/webapps/gradebook/do/student/viewAttempts?method=list&course_id=_28725_1&outcome_definition_id=_188406_1&outcome_id=_4279031_1&takeTestContentId=_1236882_1&maxAttemptsReached=false'

    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0',
        'cookie': 'JSESSIONID=A9935561980D8105AD7A4552E0D0A9F7; identifyId=d90f9a462eef4cc1bf865aatywerwe23; COOKIE_CONSENT_ACCEPTED=true; CdnSignedValidation=false; BbClientCalenderTimeZone=Asia/Shanghai; BbClientDownloadExecuting=false; JSESSIONID=2E231BAB34676FC3FF1A1D9A959D59CB; web_client_cache_guid=e0afa752-894d-44a3-8d49-293e9c81b85d; s_session_id=AF31619E51E4EB65521E3FB8FAB1BE39'
    }
    text = requests.get(url, headers=header).text

    soup = BS(text,'html.parser')
    tbody = soup.find_all('tbody')

    all = 200 #### 总题目数目

    print(f'总数: {all}')

    link = []
    for tr in tbody:
        td_ = tr.find_all('a')
        for a in td_:
                a1 = str(a.get('href'))
                link.append(a1)

                file.write(str(a) + '\n')
        print(f"总页数: {len(td_)}\n总题数: {len(td_)*15}(含重复)\n")

    data = {}
    num = 0
    for i in link:
        num += 1
        url_i = 'https://wlkc.ouc.edu.cn' + i
        text_i = requests.get(url_i, headers=header).text
        soup_i = BS(text_i,'html.parser')

        ul = soup_i.find(id='content_listContainer')

        all_li = ul.find_all('li')
        for li in all_li:
            L = []
            div = li.select_one('.details',recursive=False)
            table = div.find('table',recursive=False,attrs={"width":"100%"})
            tr = table.find_all('tr',recursive=False)
            td_1 = tr[1].find_all('td')
            td_ques_pre = td_1[1].find('div')

            td_ques = td_ques_pre.text

            #  for i in tr[2:]:
            td = tr[2].find_all('td',attrs={"valign":"top"})
            # table_td = td.find('table',recursive=False)
            # tr_all = table_td.find_all('tr',recursive=False)

            Len_tr_all = len(td)


            for i in range(2,Len_tr_all):
                # td_tr_all = tr_all[i].find_all('td',recursive=False)

                ans_all = td[i].find_all('span')

                ans_span = ans_all[-1]
                i_text = ans_span.find('label').text.strip()

                tf_span = ans_all[0]
                img = tf_span.find('img')
                if img != None:     
                    i_text += '√'
                
                L.append(i_text)

            
            if len(tr) > 3:
                for tr_i in tr[3:]:
                    i_text = tr_i.find('label').text.strip()
                    L.append(i_text + '√')

            data[td_ques] = L
            # break
        print(f'完成--{num}/{len(link)}', end='\r')
        # break
    
    json.dump(data,json_file)
    
    print(f'总题数: {len(data)}(降重后)')

    for i in data.keys():
        if '对' in data[i]:
            
            # tf_num += 1
            pass
        else:
            tf_temp = 0
            for true in data[i]:
                if '√' in true:
                    tf_temp += 1

            # if tf_temp == 1:
            #     single_num += 1
            # else:
            #     multiple_num += 1 
            
    if len(data) != all:
        if len(data) < all:
            print('收集:     |  总数:')
            print('总数: %3d < %3d, 还剩%3d道题' %(len(data), all, all-len(data)))
            # 未知
            # if single_num < single:
            #     print(f'单选: %3d < %3d, 还剩%2d道题' %(single_num,single,single-single_num))
            # if multiple_num < multiple:
            #     print(f'多选: %3d < %3d, 还剩%2d道题' %(multiple_num,multiple,multiple-multiple_num))
        else:
            print('*出现问题*')
            
            # 未知
            # if single_num > single:
            #     print(f'单选: {single_num} > {single}, 超出{single_num-single}道题')
            # if multiple_num > multiple:
            #     print(f'多选: {multiple_num} > {multiple}, 超出{multiple_num-multiple}道题')

    else:
        if len(data) == all:
            print('收集完成')
        else: 
            print('**出现问题**')
    
    print('\n'*3)

    file.close()
    json_file.close()


if __name__=='__main__':
    main()
