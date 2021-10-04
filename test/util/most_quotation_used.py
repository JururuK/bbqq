%run module.py

date = input()
today = date[:4] + '-' + date[4:6] + '-' + date[6:]
date1 = str(int(date) + 1)
tomorrow = date1[:4] + '-' + date1[4:6] + '-' + date1[6:]
provider = ["경향신문", "국민일보", "내일신문", "동아일보", "문화일보", "서울신문", "세계일보", "조선일보", "중앙일보", "한겨레", "경기일보", "경인일보", "강원도민일보",
            "강원일보", "대전일보", "중도일보", "중부매일", "중부일보", "충북일보", "충청일보", "충청투데이", "경남신문", "경남도민일보", "경상일보", "국제신문", "대구일보",
            "매일신문", "부산일보", "영남일보", "울산매일", "광주매일신문", "광주일보", "무등일보", "전남일보", "전북도민일보", "전북일보", "제민일보", "한라일보", "머니투데이",
            "서울경제", "파이낸셜뉴스", "한국경제", "헤럴드경제", "아시아경제", "아주경제", "전자신문"]

my_key = "a19a4199-9fe3-4dff-90ed-6512bb359f2b"

result_url = 'http://tools.kinds.or.kr:8888/search/news'
per_list = []
for i in range(len(provider)):
    data = {
        "access_key": f"{my_key}",
        "argument": {
            "query": "",
            "published_at": {
                "from": today,
                "until": tomorrow
            },
            "provider": [provider[i]],
            "category": [""],

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
    if len(res_title) == 0:
        print("{} {} 뉴스에는 따옴표가 없습니다.".format(today, provider[i], np.round(per * 100, 2)))

    else:
        sen_res = []
        for sen in res_title:
            if '“' in sen:
                sen = sen.replace('“', '"')
                if '”' in sen:
                    sen = sen.replace('”', '"')
                sen_res.append(sen)
            elif '”' in sen:
                sen = sen.replace('”', '"')
                sen_res.append(sen)
            elif '"' in sen:
                sen_res.append(sen)
        per = np.round((len(sen_res) / len(res_title)), 4)
        per_list.append([per, provider[i]])

per_list.sort(reverse=True)
print("{}에 {}이(가) {}% 비율로 가장 많이 인용 기사를 보도했습니다.".format(today, per_list[0][1], np.round(per_list[0][0] * 100, 1)))
print("{}에 {}이(가) {}% 비율로 두번째로 인용 기사를 보도했습니다.".format(today, per_list[1][1], np.round(per_list[1][0] * 100, 1)))
print("{}에 {}이(가) {}% 비율로 세번째로 인용 기사를 보도했습니다.".format(today, per_list[2][1], np.round(per_list[2][0] * 100, 1)))