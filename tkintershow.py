from tkinter import *
import pymysql
import boto3
import datetime
date = datetime.date.today()
translate = boto3.client('translate') #クライアントの作成

#***********************************tkinterに表示する****************************************#
class Tkintershow:
    def tkintershow(Text,language,languagecode):
        import tkinter as tk #tkinterモジュールを読み込む
        root = tk.Tk()
        root.title("抽出翻訳読み上げ君 ver1.0") #タイトル
        root.geometry('640x700') #ウィンドウサイズ
        textresult = tk.Message( #抽出したテキストを表示
        root,
        aspect=550, 
        relief="raised", 
        text=Text) 
        textresult.grid(row=2,padx=35, pady=5)

        bresult = tk.Message( #検出された言語を表示
        root,
        aspect=500, 
        text="検出された言語 = " + language,bg="Yellow")
        bresult.grid(row=1)

    #***************************サブウィンドウ_翻訳先言語選択画面****************************#
        sub_win_trans = tk.Toplevel()
        sub_win_trans.geometry('+665+26') #ウィンドウサイズ
        rdo_txt = [['de',"ドイツ語"], #言語コードと日本語の２次元配列
        ['en',"英語"],
        ['es',"スペイン語"],
        ['fr',"フランス語"],
        ['it',"イタリア語"],
        ['pt',"ポルトガル語"],
        ['ja',"日本語"],
        ['ko',"韓国語"],
        ['hi',"ヒンディー語"]]
        
        rdo_var = tk.IntVar() #ラジオボタンの状態
        text_trans = tk.Message(
        sub_win_trans,
        aspect=500,
        text="「翻訳先言語」",bg="green") 
        text_trans.grid()

        # ラジオボタンを動的に作成して配置
        for i in range(len(rdo_txt)):
            rdo = tk.Radiobutton(sub_win_trans, value=i, variable=rdo_var, text=rdo_txt[i][1]) 
            rdo.grid(padx=33.3)
    #========================================================================================#

    #*************************サブウィンドウ_読み上げ言語選択画面****************************#
        sub_win_polly = tk.Toplevel()
        sub_win_polly.geometry('+665+305')

        polly_txt = [['Hans',"ドイツ語"],
        ['Emma',"英語"],
        ['Lucia',"スペイン語"],
        ['Celine',"フランス語"],
        ['Giorgio',"イタリア語"],
        ['Cristiano',"ポルトガル語"],
        ['Mizuki',"日本語"],
        ['Seoyeon',"韓国語"],
        ['Aditi',"ヒンディー語"]]

        text_polly = tk.Message(
        sub_win_polly,
        aspect=500, 
        text="「読み上げ言語」",bg="red") 
        text_polly.grid()

        polly_var = tk.IntVar()
        # ラジオボタンを動的に作成して配置
        for i in range(len(rdo_txt)):
            polly = tk.Radiobutton(sub_win_polly, value=i, variable=polly_var, text=polly_txt[i][1]) 
            polly.grid(padx=33.3)
    #========================================================================================#

    #*******************************言語コードとボイスIDを取得*******************************#
        def btn_click_trans(): 
            num_trans = rdo_var.get()
            return rdo_txt[num_trans][0],rdo_txt[num_trans][1]

        def btn_click_polly():
            num_polly = polly_var.get()
            return polly_txt[num_polly][0],polly_txt[num_polly][1]
    #========================================================================================#
       

    #*************************************翻訳して表示***************************************#
        def transletion(): 
            try:
                global Targetname
                Target,Targetname = btn_click_trans() #ラジオボタンから言語コードを取得           

                result = translate.translate_text( #翻訳した言語をresultに代入
                    Text= Text,
                    SourceLanguageCode = languagecode,
                    TargetLanguageCode = Target)
                global transretedtext
                transretedtext = result['TranslatedText'] #翻訳結果を保持

                transreted = tk.Message( #翻訳後の文字を表示
                root,
                aspect=500, 
                relief="raised",
                text=result['TranslatedText'])
                transreted.grid(pady=5)
            
                button_reading = tk.Button(text="「読み上げ」 (元言語"+Targetname+")", command=polly) #翻訳完了後に読み上げボタンを表示
                button_reading.grid()
            except:
                print("エラー発生")
            finally:
                pass
            #以下で削除
            def funcA():
                transreted.destroy()
            def funcB():
                button_reading.destroy()
            def funcC():
                buttonForget.destroy()

            buttonForget = tk.Button(root,
                          text = '削除',
                          command=lambda: [funcA(), funcB(), funcC()])
            buttonForget.grid()
    #*************************************データベース***************************************#
            dph = pymysql.connect(
            host = "localhost",
            user = "fujishima",
            password = "3a6a9a12a15a",
            db = "fujishima",
            charset = "utf8",
            cursorclass=pymysql.cursors.DictCursor
            )  
            stmt = dph.cursor()
            stmt.execute("INSERT INTO mydb VALUES (%s, %s, %s, %s, %s)", (date,Text, transretedtext, language,Targetname))
            dph.commit()
    #========================================================================================#
    #========================================================================================#
        
    #******************************翻訳したテキストを読み上げ********************************#
        def polly():
            voiceid,voiceidname= btn_click_polly() #ラジオボタンからIDを取得
            Path = Targetname+"→"+voiceidname+".mp3" #ファイル名
            import contextlib
            # 音声ファイルの自動再生のためにosの機能を使用するためにimportする
            import os
            # AWSの pollyサービスを呼び出す
            polly = boto3.client('polly')

            # polly.synthesize_speech は音声合成の詳細を設定している
            # VoiceId = 'Mizuki' 以外の声はP94を確認
            result = polly.synthesize_speech(
                Text=transretedtext, OutputFormat='mp3', VoiceId=voiceid)
            # ファイル名
            path = Path
            try:
            # 音声ストリームの再生
                with contextlib.closing(result['AudioStream']) as stream:
                    # 作成した音声出力ファイルを開く
                    with open(path, 'wb') as file:
                        file.write(stream.read())
            except:
                print("読み込みエラー")
            finally:
                pass
            # os.name == 'nt'　は Windows
            if os.name == 'nt':
                os.startfile(path)
   
        button = tk.Button(text="翻訳", command=transletion,activebackground="blue") #翻訳ボタンを表示
        button.grid(row=3)

        root.mainloop()    
    #========================================================================================#
    #========================================================================================#
