%run module.py

category = ["정치","경제","사회","국제","문화"]

date = input()
today = date[:4]+'-'+date[4:6]+'-'+date[6:]
date1 = str(int(date)+1)
tomorrow = date1[:4]+'-'+date1[4:6]+'-'+date1[6:]

my_key = "a19a4199-9fe3-4dff-90ed-6512bb359f2b"

result_url = 'http://tools.kinds.or.kr:8888/search/news'
for i in range(len(category)):
    data = {
        "access_key": f"{my_key}",
        "argument": {
            "query":"",
            "published_at": {
                "from": today,
                "until": tomorrow
            },
            "provider": [""],
            "category": [category[i]],
            "provider_subject": [""],
            "subject_info": [""],
            "sort": {"date": "desc"},
            "hilight": 200,
            "return_from": 0,
            "return_size": 20000,
            "fields": [
                "hilight",
                "byline",
                "category",
                "category_incident",
                "images",
                "provider_subject",
                "subject_info",
                "provider_news_id",
                "publisher_code"
            ]
        }
    }

    response = requests.post(result_url, data=json.dumps(data))
    res_json = response.json()
    res_doc = res_json['return_object']['documents']
    res_title = [x['title'] for x in res_doc]

    my_ex_list = ['"','“']

    sen_res = []

    for sen in res_title :
        if '“' in sen :
            sen = sen.replace('“','"')
            if '”' in sen :
                sen = sen.replace('”','"')
            sen_res.append(sen)
        elif '”' in sen :
            sen = sen.replace('”','"')
            sen_res.append(sen)
        elif '"' in sen :
            sen_res.append(sen)
    per = len(sen_res)/len(res_title)
    print("{} {} 뉴스에 {}%의 비율로 따옴표가 쓰였습니다.".format(today,category[i],np.round(per*100,2)))
