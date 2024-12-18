import requests
from bs4 import BeautifulSoup as BS
import json

def main():
    file = open('E:/桌面/习概/all_link.txt','w', encoding='utf-8')
    json_file = open('E:/桌面/习概/习概预题库.json','w+',encoding='utf-8')

    url = ''

    header = {
        'User-Agent': '###',
        'cookie': '####'
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
            div = li.select_one('.details')
            table = div.find('table')
            tr = table.find_all('tr')
            td_1 = tr[1].find_all('td')
            td_ques_pre = td_1[1].find('div')

            td_ques = td_ques_pre.text

            td_tr_all = tr[2]
            # print(f'{td_tr_all.text}')
            check_num = 0

            check_tag = td_tr_all.find_all('td')[0].find('span')
            try:
                check = check_tag.text
            except:
                pass
            if check == '正确答案：':
                check_num = 1


            if check_num == 0:
                continue
            else:
                td_text = td_tr_all.find_all('td')[-1]
                div = td_text.find('div')
                ans_all = div.find_all('span')

                ans_span = ans_all[-1]
                i_label = ans_span.find('div')
                i_text = i_label.find('label').text.strip()

                tf_span = ans_all[0]
                img = tf_span.find('img')
                if img != None:     
                    i_text += '√'
                
                L.append(i_text)
                #正式
                # print(i_text)
                    
            #正式
            # print('<'*70)
            # print('\n')

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
