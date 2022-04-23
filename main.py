import boto3
import tkintershow
import sys
#*************************言語コードと言語名を取得*******************************************#
def langsearch(text): 
        lang = {"de":"ドイツ語","en":"英語","es":"スペイン語","fr":"フランス語","it":"イタリア語","pt":"ポルトガル語","ja":"日本語","ko":"韓国語","hi":"ヒンディー語"}
        comprehend = boto3.client('comprehend')
        result = comprehend.detect_dominant_language(Text=text)

        for language in result["Languages"]:
            langresult = (language["LanguageCode"])
        return langresult,lang[langresult]
#============================================================================================#
#コマンドライン
if len(sys.argv) < 2:
    print('画像のファイル名を引数として入力してください。')
    exit()
elif len(sys.argv) > 2:
    print('指定できるファイルは1つだけです。')
try:
    picture = sys.argv[1]
    textract = boto3.client('textract')
    with open(picture, 'rb') as file:
        result = textract.detect_document_text(
            Document={'Bytes': file.read()})
except OSError:
    print("ファイル名が違います。")
else:
    Text = ""

    for block in result['Blocks']:
        if block['BlockType'] == 'LINE':
            Text += block['Text']

    languagecode,language= langsearch(Text) #抽出されたTextをもってlangsearchを呼び出す
    couka_sokutei = tkintershow.Tkintershow
    couka_sokutei.tkintershow(Text,language,languagecode) #引数をみっつもって表示プログラムに飛ぶ


  

