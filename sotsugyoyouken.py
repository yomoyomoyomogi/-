import streamlit as st

st.title("🎓筑波大学心理学類卒業要件チェッカー")
st.write("このサイトは、卒業要件を満たしているかどうかを確認するためのものです。以下の手順に従って、CSVファイルをアップロードしてください。")
st.write("1.TWINSの成績照会を開く。")
st.write("2.下にスクロールし、ダウンロードボタンを押す。")
st.write("3.ファイル形式はcsv、文字コードはUTF-8、BOMありでダウンロードする。")


import csv
# CSVファイルを読み
csv_file = st.file_uploader("卒業要件を確認したいCSVファイルをアップロードしてください。", type="csv")

csv_text = None
if csv_file:
    try:
        csv_text = csv_file.read().decode('utf-8')
    except UnicodeDecodeError:
        csv_file.seek(0)
        csv_text = csv_file.read().decode('cp932')
    st.write(f"CSV読み込み完了: {len(csv_text.splitlines())} 行")


def clean_row(row):
    return {k.strip(): (v.strip() if isinstance(v, str) else v) for k, v in row.items()}


def csv_rows():
    if not csv_text:
        return []
    reader = csv.DictReader(csv_text.splitlines())
    if reader.fieldnames:
        reader.fieldnames = [fn.strip('\ufeff').strip() for fn in reader.fieldnames]
    for row in reader:
        yield clean_row(row)

# 方法1: csv.DictReader（推奨）
st.dataframe(list(csv_rows()))

count_kannrennkamoku = 0

if csv_file:
    reader = csv.DictReader(csv_text.splitlines())

    for row in reader:
        if row['科目区分'].strip()=='C0' and row['総合評価'].strip() in ['A+','A', 'B', 'C','P','履修中']:
            tannisuu = float(row['単位数'])
            count_kannrennkamoku += tannisuu
st.markdown('<p style="font-weight:bold;">基礎科目の関連科目</p>', unsafe_allow_html=True)
st.write(f"基礎科目中の関連科目の単位数: {count_kannrennkamoku}")

if count_kannrennkamoku >33:
    count_kannrennkamoku1 = 33
    st.markdown(f'<p style="color:red;">関連科目の単位数が\'{count_kannrennkamoku-count_kannrennkamoku1}\'単位超えています。</p>', unsafe_allow_html=True)
else :
        count_kannrennkamoku1 = count_kannrennkamoku

if count_kannrennkamoku < 6:
    st.markdown(f'<p style="color:red;">基礎科目の関連科目数が\'{6 - count_kannrennkamoku1}\'足りません。</p>', unsafe_allow_html=True)
else:
    st.write('基礎科目の関連科目数は足りています。')



#共通科目左

kyoutu_hissyu = ["ファーストイヤーセミナー","学問への誘い","基礎体育(秋)","基礎体育(春)","応用体育(秋)","応用体育(春)","基礎語AI","基礎語BI","基礎語AII"
,"データサイエンス","情報リテラシー(演習)","情報リテラシー(講義)","English Reading Skills I","English Presentation Skills I","English Reading Skills II","English Presentation Skills II"]

def normalize(name):
    name = name.strip()

    if "基礎体育" in name and "(秋)" in name:
        return "基礎体育(秋)"
    if "基礎体育" in name and "(春)" in name:
        return "基礎体育(春)"
    if "応用体育" in name and "(秋)" in name:
        return "応用体育(秋)"
    if "応用体育" in name and "(春)" in name:
        return "応用体育(春)"
    if "基礎" in name and "語BII" in name:
        return "基礎語BII"
    if "基礎" in name and "語BI" in name:
        return "基礎語BI"
    if "基礎" in name and "語AII" in name:
        return "基礎語AII"
    if "基礎" in name and "語AI" in name:
        return "基礎語AI"
   
    return name  # 条件に合致しない場合はそのまま返す
    

count_kyotuleft = 0.0

kyoutu_rissyu = []

if csv_file:
    reader = csv.DictReader(csv_text.splitlines())

    for row in reader:
        if row['科目区分'].strip()=='C' and row['総合評価'].strip() in ['A+','A', 'B', 'C','P','履修中']:
            name = row.get('科目名 ', '').strip()
            normalised = normalize(name)
            if normalised in kyoutu_hissyu:
                count_kyotuleft += float(row['単位数'])  #共通科目左の単位数
                if normalised not in kyoutu_rissyu:
                   kyoutu_rissyu.append(normalised)


st.markdown('<p style="font-weight:bold;">基礎科目の共通科目</p>', unsafe_allow_html=True)
for sub in kyoutu_hissyu:
    if sub not in kyoutu_rissyu:
        st.markdown(f'<p style="color:red;">未履修: {sub}</p>', unsafe_allow_html=True)






if csv_file:
    reader = csv.DictReader(csv_text.splitlines())

    for row in reader:
        if row['科目区分'].strip()=='C' and row['総合評価'].strip() in ['A+','A', 'B', 'C','P','履修中']:
            name = row.get('科目名 ', '').strip()
            normalised = normalize(name)

          

#共通科目全体の単位数


count_kyotukamoku = 0

for row in csv_rows():
        if row['科目区分'].strip()=='C' and row['総合評価'].strip() in ['A+','A', 'B', 'C','P','履修中']:
            tannisu_2 = float(row['単位数'])
            count_kyotukamoku += tannisu_2



if count_kyotukamoku-count_kyotuleft >= 29:
    count_kyotukamoku1 = 28
else :
        count_kyotukamoku1 = count_kyotukamoku

st.write(f"共通科目中の選択科目単位数: {count_kyotukamoku-count_kyotuleft}")
st.write(f"共通科目中の必修科目単位数: {count_kyotuleft}")


#学士基盤はとれてるか

if csv_file:
    reader = csv.DictReader(csv_text.splitlines())

    total_12 = 0
    
    for row in reader:
        if row['科目区分'].strip()=='C' and row['総合評価'].strip() in ['A+','A', 'B', 'C','P','履修中']:
            code = row.get('科目番号', '').strip()
            if code.startswith('12'):
                try:
                    credits_1 = float(row['単位数'].replace(',','.'))
                    total_12 += credits_1
                except:
                    continue

if count_kyotukamoku1 <1 or total_12 <2:
    st.markdown('<p style="color:red;">学士基盤科目が足りません。</p>', unsafe_allow_html=True)
else:
    st.write("学士基盤科目は足りています。")

#専門基礎科目

sennmonkiso_hissyu = ["人間学I","心理学概論","キャリアデザイン入門","心理学研究法","心理学統計法II","心理学統計法実習","心理学統計法I","心理学英語セミナー","心理学実験","心理学研究実習I"]


sennmonkiso_rissyu = []

  #とりあえず教育基礎論とかは含まない

    
sennmonkisotani_left = 0.0  

    
if csv_file:
    reader = csv.DictReader(csv_text.splitlines())

    for row in reader:
        if row['科目区分'].strip()=='B' and row['総合評価'].strip() in ['A+','A', 'B', 'C','P','履修中']:
            name_1 = row.get('科目名 ', '').strip()
            if name_1 in sennmonkiso_hissyu:
                sennmonkisotani_left += float(row['単位数'])
                if name_1 not in sennmonkiso_rissyu:
                   sennmonkiso_rissyu.append(name_1)

st.markdown('<p style="font-weight:bold;">専門基礎科目</p>', unsafe_allow_html=True)
for sub_1 in sennmonkiso_hissyu:
    if sub_1 not in sennmonkiso_rissyu:
        st.markdown(f'<p style="color:red;">未履修: {sub_1}</p>', unsafe_allow_html=True)


found = False


for row in csv_rows():
        if row['科目区分'].strip()=='B' and row['総合評価'].strip() in ['A+','A', 'B', 'C','P','履修中']:
            name_2 = row.get('科目名 ', '').strip()
            
            if "教育基礎論" in name_2 or "学校の経営・制度・社会" in name_2:
                found = True

if not found:
    print("未履修:教育基礎論または学校の経営・制度・社会のどちらか")


found = False

for row in csv_rows():
        if row['科目区分'].strip()=='B' and row['総合評価'].strip() in ['A+','A', 'B', 'C','P','履修中']:
            name_2 = row.get('科目名', '').strip()

            if "障害科学I" in name_2 or "障害科学II" in name_2:
                found = True

if not found:
    st.write("未履修:障害科学Iまたは障害科学IIのどちらか")

#専門基礎科目単位数

count_sennmonkiso = 0.0

for row in csv_rows():
        if row['科目区分'].strip()=='B' and row['総合評価'].strip() in ['A+','A', 'B', 'C','P','履修中']:
            credits_2 = float(row['単位数'])
            count_sennmonkiso += credits_2 #専門基礎科目全体の単位数

shougai_added = False
kyouiku_added = False
for row in csv_rows():
        if row['科目区分'].strip()=='B' and row['総合評価'].strip() in ['A+','A', 'B', 'C','P','履修中']:
            name_3 = row.get('科目名', '').strip()

            if ("障害科学I" in name_3 or "障害科学II" in name_3) and not shougai_added:
                sennmonkisotani_left += 2.0
                shougai_added = True
            if ("教育基礎論" in name_3 or "学校の経営・制度・社会" in name_3) and not kyouiku_added:
                sennmonkisotani_left += 2.0
                kyouiku_added = True

st.write(f"専門基礎科目中の必修科目単位数: {sennmonkisotani_left}")
sennmonkisotani_right = count_sennmonkiso - sennmonkisotani_left
st.write(f"専門基礎科目中の選択科目単位数: {sennmonkisotani_right}")


ningencore= sennmonkisotani_right
for row in csv_rows():
        if row['科目区分'].strip()=='B' and row['総合評価'].strip() in ['A+','A', 'B', 'C','P','履修中']:
            name_4 = row.get('科目名 ', '').strip()
            if "心理学研究実習II" in name_4:
                ningencore -= 3.0
            
if ningencore >10:
    st.markdown(f'<p style="color:red;">人間学群コア・カリキュラムの科目が\'{ningencore-10}\'単位超えています。</p>', unsafe_allow_html=True)
else:
    st.write("人間学群コア・カリキュラムの科目は範囲内です。")

#専門科目必修

sennmon_hissyu =["知覚・認知心理学","感情・人格心理学","神経・生理心理学","社会・集団・家族心理学","発達心理学","臨床心理学概論","卒業研究セミナー","卒業研究", "学習・言語心理学"]

sennmon_rissyu = []
sennmon_left =0.0

if csv_file:
    reader = csv.DictReader(csv_text.splitlines())

    for row in reader:
        if row['科目区分'].strip()=='A' and row['総合評価'].strip() in ['A+','A', 'B', 'C','P','履修中']:
            name_5 = row.get('科目名 ', '').strip()
            if name_5 in sennmon_hissyu:
                if name_5 not in sennmon_rissyu:
                    sennmon_left += float(row['単位数'])
                    sennmon_rissyu.append(name_5)

st.markdown('<p style="font-weight:bold;">専門科目の必修科目</p>', unsafe_allow_html=True)
for sub_5 in sennmon_hissyu:
    if sub_5 not in sennmon_rissyu:
        st.markdown(f'<p style="color:red;">未履修: {sub_5}</p>', unsafe_allow_html=True)

st.write(f"専門科目の必修科目単位数: {sennmon_left}")

#CCで始まる心理学類の科目
if csv_file:
    reader = csv.DictReader(csv_text.splitlines())
    CC = 0
    for row in reader:
        if row['科目区分'].strip()=='A' and row['総合評価'].strip() in ['A+','A', 'B', 'C','P','履修中']:
            code_5 = row.get('科目番号', '').strip()
            if code_5.startswith('CC'):
                try:
                    credits_3 = float(row['単位数'].replace(',','.'))
                    CC += credits_3
                except:
                    continue

    st.write(f"心理学類の科目の単位数: {CC-sennmon_left}")
    if CC - sennmon_left >= 59:
       st.markdown(f'<p style="color:red;">心理学類の科目の単位数が\'{CC - sennmon_left - 58}\'単位超えています。</p>', unsafe_allow_html=True)
    elif CC - sennmon_left <= 20:
       st.markdown(f'<p style="color:red;">心理学類の科目の単位数が\'{21 - (CC - sennmon_left)}\'単位足りません。</p>', unsafe_allow_html=True)
    else:
       st.write("心理学類の科目の単位数は足りています。")

#CC２７から始まる科目の単位
if csv_file:
    reader = csv.DictReader(csv_text.splitlines())
    CC27 = 0
    
    for row in reader:
        if row['科目区分'].strip()=='A' and row['総合評価'].strip() in ['A+','A', 'B', 'C','P','履修中']:
            code_6 = row.get('科目番号', '').strip()
            if code_6.startswith('CC27'):
                try:
                    credits_4 = float(row['単位数'].replace(',','.'))
                    CC27 += credits_4
                except:
                    continue

    st.write(f"CC27から始まる科目の単位数: {CC27}")
    if CC27 <6:
        st.markdown(f'<p style="color:red;">CC27から始まる科目の単位数が\'{6 - CC27}\'単位足りません。</p>', unsafe_allow_html=True)
    else:
        st.write("CC27から始まる科目の単位数は足りています。")



#CB,CEで始まる科目の単位数
if csv_file:
    reader = csv.DictReader(csv_text.splitlines())
    CBCE = 0
   
    for row in reader:
        if row['科目区分'].strip()=='A' and row['総合評価'].strip() in ['A+','A', 'B', 'C','P','履修中']:
            code_7 = row.get('科目番号', '').strip()
            if code_7.startswith('CB') or code_7.startswith('CE'):
                try:
                    credits_5 = float(row['単位数'].replace(',','.'))
                    CBCE += credits_5
                except:
                    continue

    st.write(f"CB,CEで始まる科目の単位数: {CBCE}")
    if CBCE >37:
      st.markdown(f'<p style="color:red;">CB,CEで始まる科目の単位数が\'{CBCE - 37}\'単位超えています。</p>', unsafe_allow_html=True)
    else:
        st.write("CB,CEで始まる科目の単位数は範囲内です。") 

    st.write(f"専門科目中の選択科目の単位数: {CBCE + CC - sennmon_left}")
    if CBCE + CC - sennmon_left > 58:
      st.markdown(f'<p style="color:red;">専門科目中の選択科目の単位数が\'{CBCE + CC - sennmon_left - 58}\'単位超えています。</p>', unsafe_allow_html=True)
    else:
        st.write("専門科目中の選択科目の単位数は範囲内です。")



sogotani = 0.0
for row in csv_rows():
        if row['総合評価'].strip() in ['A+','A', 'B', 'C','P','履修中']:
            tannisu_3 = float(row['単位数'])
            sogotani += tannisu_3

st.markdown('<p style="font-weight:bold;">総単位数</p>', unsafe_allow_html=True)
st.write(f"取得単位数は{sogotani}単位です。卒業まであと{124 - sogotani}単位必要です。単位取得に制限がある科目は、範囲を超えたものもカウントしています。ご注意を！")
st.write("赤字で、範囲を超えていますと表示がなければ大丈夫です！")


st.markdown(
    """
    <style>
    .stApp{background-color: #ffffcc;}
    </style>
    """,
    unsafe_allow_html=True
)