%run module.py

date = input("조회 시작 날짜 : ")
per = int(input("조회할 기간 : "))
today = date[:4] + '-' + date[4:6] + '-' + date[6:]
date1 = str(int(date) + per)
target_date = date1[:4] + '-' + date1[4:6] + '-' + date1[6:]

my_key = "a19a4199-9fe3-4dff-90ed-6512bb359f2b"

result_url = 'http://tools.kinds.or.kr:8888/search/news'

data = {
    "access_key": f"{my_key}",
    "argument": {
        "query": "",
        "published_at": {
            "from": today,
            "until": target_date
        },
        "provider": [""],
        "category": [""],
        "provider_subject": [""],
        "subject_info": [""],
        "sort": {"date": "desc"},
        "hilight": 200,
        "return_from": 0,
        "return_size": 20000,
        "fields": ["hilight", "byline", "category", "category_incident", "images", "provider_subject", "subject_info",
                   "provider_news_id", "publisher_code"]}
}

response = requests.post(result_url, data=json.dumps(data))
res_json = response.json()
res_doc = res_json['return_object']['documents']
res_title = [x['title'] for x in res_doc]

sen_res = []
# 여러 유형 따옴표를 하나로 통일
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
# 따옴표 밖의 내용만 추출(2번 있는 경우도 있음)
res_fin = []
for i in range(len(sen_res)):
    if sen_res[i].count('"') == 1:
        sen_fin = sen_res[i].replace('"', ' ')
        res_fin.append(sen_fin)
    else:
        begin = sen_res[i].index('"')
        if '"' in sen_res[i][begin + 1:]:
            end = sen_res[i][begin + 1:].index('"')
        else:
            end = begin

        sen = sen_res[i].replace(sen_res[i][begin:begin + end + 2], ' ')
        if '"' in sen:
            second = sen.index('"')
            if '"' in sen[second + 1:]:
                second_end = sen[second + 1:].index('"')
            else:
                second_end = second
            sen_fin = sen.replace(sen[second:second + second_end + 2], ' ')
            res_fin.append(sen_fin)
        else:
            res_fin.append(sen)

# 특수문자, vs, 등 제거해서 단어수 count
words = []
props = [',', '.', '"', '?', '…', '+', '[', ']', 'vs', '‘', '’', '  ', '   ', '    ', '     ']
for sen in res_fin:
    for prop in props:
        sen = sen.replace(prop, " ")
    sen = sen.split(" ")
    for word in sen:
        words.append(word)

word_cnt = []
for word in words:
    cnt = words.count(word)
    word_cnt.append((cnt, word))

se = set(word_cnt)
fin = list(se)
# fin.sort(reverse=True)

word_list = []
num_list = []
for i in range(len(fin)):
    word_list.append(fin[i][1])
    num_list.append(fin[i][0])

for j in range(1, len(word_list)):
    for i in range(j + 1, len(word_list)):
        if word_list[j] in word_list[i]:
            num_list[j] += 1
final = []
# 한글자 이상의 것들만 추출하여 sort
for i in range(len(word_list)):
    if len(word_list[i]) > 1:
        final.append([num_list[i], word_list[i]])
final.sort(reverse=True)
# print(final[:20])
print("{}부터 {}일간 가장 많이 인용된 키워드는 '{}'입니다.".format(today, per, final[0][1]))