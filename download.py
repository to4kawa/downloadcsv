import re, datetime
import urllib.request

# 仙台市中央市場　野菜果実のデータ
url='http://kei008220.webcrow.jp/seika.csv'

#　データ取り込み、文字コードがShift-jisなのでデコード

req = urllib.request.Request(url)
with urllib.request.urlopen(req) as response:
   file = response.read().decode('cp932')

#全角スペース置換
lst=file.replace('　',' ')
#金額正規化
lst2=re.sub(r"\"(\d+),(\d+)\"", r"\1\2", lst)
#最後の空白セルを正規表現で削除
lst2=re.sub(r',{15}\r\n','\r\n',lst2)
#行で改行し、csvで配列化
r = [i.split(",") for i in lst2.splitlines()]  
#最後にたくさんの空白があるので削除するつもりだったが正規表現で削除したので[:15]を除いた
l =[ r[i] for i in range(len(r)) if max(r[i])]
#行を数えて、表示
rows=sum(1 for _ in l)
#for i in range(rows):
#    print(f'行{i}: {l[i]}')

#　データ項目の抽出
wareki=l[1][0].split()[0]
weather=re.search(r'(?<=天気.)[^\)]+',l[1][0]).group()

#令和→西暦
wareki_tmp=re.search(r'(\d+)\D+(\d+)\D+(\d+)',wareki).groups()
year=str(2000+int(wareki_tmp[0])+18)
month=wareki_tmp[1].zfill(2)
day=wareki_tmp[2]
#print(f'{year}/{month}/{day}')
#日付変換
date_tmp=datetime.datetime.strptime(year+'/'+month+'/'+day,'%Y/%m/%d')
date=datetime.datetime.strftime(date_tmp,"%Y-%m-%d")

#　野菜と果物のテーブル　
# searchで文字列を検索して行番号を出している。
vegitable_row=''
furit_row=''
for i,v in [[i,re.search('野菜',v[0])]  for i,v in enumerate(l)]:
    if v:
        vegitable_row=i
for i,v in [[i,re.search('果実',v[0])]  for i,v in enumerate(l)]:
    if v:
        fruit_row=i
vegitable_lst=[]
# スライスの仕方は確認したらこれで大丈夫だった。
for i in range(vegitable_row+2,fruit_row):
    vegitable_lst.append(l[i][:7])
for i in range(vegitable_row+2,fruit_row):
    vegitable_lst.append(l[i][:8])
fruit_lst=[]
for i in range(fruit_row+2,rows):
    if max(l[i][:7]):
        fruit_lst.append(l[i][:7])

# ヘッダーも含め再構成
for i,v in enumerate(vegitable_lst):
    vegitable_lst[i]=[v[0],v[1],v[2]+v[3],v[4],v[5],v[6],'野菜',wareki,weather,date,'\r\n']
for i,v in enumerate(fruit_lst):
    fruit_lst[i]=[v[0],v[1],v[2]+v[3],v[4],v[5],v[6],'果実',wareki,weather,date,'\r\n']
header=[['product_name'],['area'],['unit'],['high_price'],['middle_price'],['low_price'],['category'],['wareki'],['weather'],['date'],['\r\n']]
csvfile_lst=header+vegitable_lst+fruit_lst
# できたリストの行数を確認
csv_rows=sum(1 for _ in csvfile_lst)
#　リストを展開したのち１行のテキストファイルに変換
csvtmp=[]
for i in range(csv_rows):
    csvtmp.append(','.join(csvfile_lst[i]))
csvfile=','.join(i for i in csvtmp)
# 余計な「,」等を削除
csvfile=csvfile.replace(',\r\n,','\r\n').replace('－     ','－').replace(',\r\n','')

#書き込み
filename='seika_'+date+'.csv'

with open(filename, 'w', encoding='utf-8') as w:
    w.write(csvfile)