import requests
from bs4 import BeautifulSoup as BS
import json
import matplotlib.pyplot as plt

def main():
    statistics = []
    file = open('E:/桌面/xigai/all_link.txt','w', encoding='utf-8')
    json_file = open('E:/桌面/xigai/习概预题库.json','w+',encoding='utf-8')

    url = 'https://wlkc.ouc.edu.cn/webapps/gradebook/do/student/viewAttempts?method=list&course_id=_31237_1&outcome_definition_id=_201669_1&outcome_id=_4599508_1&takeTestContentId=_1316838_1&maxAttemptsReached=false'

    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0',
        'cookie': 'JSESSIONID=38D52DF22DACC4D333D97A7C53DC15A2; CdnSignedValidation=false; BbClientCalenderTimeZone=Asia/Shanghai; BbClientDownloadExecuting=false; identifyId=d90f9a462eef4cc1bf865aatywerwe23; JSESSIONID=9546955A95D9797C58D5DA9362D8970D; web_client_cache_guid=5b6e2a18-7531-482d-af6a-d0161bfc9329; COOKIE_CONSENT_ACCEPTED=true; s_session_id=6AF44E2C9F98AE26184D0D6088835698'
    }
    text = requests.get(url, headers=header).text

    soup = BS(text,'html.parser')
    tbody = soup.find_all('tbody')

    all = 100000 #### 总题目数目

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
            # 标题
            td_1 = tr[1].find_all('td')
            td_ques_pre = td_1[1].find('div')

            td_ques = td_ques_pre.text

            # 选项
            #  for i in tr[2:]:
            td = tr[2].find_all('td',attrs={"valign":"top"})
            td = td[1:] # 去掉第一个td
            # table_td = td.find('table',recursive=False)
            # tr_all = table_td.find_all('tr',recursive=False)

            Len_tr_all = len(td)

            tf_option = 0
            for i in range(0,Len_tr_all):
                if '答案：' == td[i].text.strip():
                    tf_option = 1
                    continue
                if tf_option == 0:
                    continue
                ans_all = td[i].find_all('span')

                ans_span = ans_all[-1]
                i_text = ans_span.find('label').text.strip()

                tf_span = ans_all[0]
                img = tf_span.find('img')
                if img != None:     
                    i_text += '√'
                
                L.append(i_text)

            data[td_ques] = L
            # break
        print(f'完成--{num}/{len(link)}', end='\r')
        statistics.append(len(data))
        # break
    
    json.dump(data,json_file)

    
    print(f'总题数: {len(data)}(降重后)')


            
    if len(data) != all:
        if len(data) < all:
            print('收集:     |  总数:')
            print('总数: %3d < %3d, 还剩%3d道题' %(len(data), all, all-len(data)))
        else: # len(data) < all
            print('*出现问题*')
    
    print('\n'*3)

    file.close()
    json_file.close()
    
    print(statistics)
    plt.plot(range(0,len(link)),statistics)
    plt.xlim(-10,120)
    plt.ylim(0,200)
    plt.show()


if __name__=='__main__':
    main()