from linebot import LineBotApi
from linebot.models import TextSendMessage, QuickReply, QuickReplyButton, MessageAction
import os

CHANNEL_ACCESS_TOKEN = os.environ['LINE_CHANNEL_ACCESS_TOKEN']
LINE_BOT_API = LineBotApi(CHANNEL_ACCESS_TOKEN)

class LineHandler:
    def __init__(self, dynamodb_handler, openai_handler):
        self.line_bot_api = LINE_BOT_API
        self.dynamodb_handler = dynamodb_handler
        self.openai_handler = openai_handler
        
        # モードごとのメッセージを辞書で定義
        self.mode_messages = {
            0: "ストーリーを終了しました。",
        }


    def reply_message(self, reply_token, ai_response, mode_code):
        quick_reply_items = self.generate_quick_reply_items(mode_code)
        try:
            self.line_bot_api.reply_message(
                reply_token,
                TextSendMessage(
                    text=ai_response,
                    quick_reply=QuickReply(items=quick_reply_items)
                ))
        except Exception as e:
            print(f"Error while replying to message: {e}")

    

        
    def process_user_message(self,user_message, reply_token, user_id):
        mode_code = self.dynamodb_handler.get_mode_code(user_id)
        if user_message == "【完了】":
            mode_code = 0
            self.dynamodb_handler.update_user_usage(user_id, 0, mode_code)
            ai_response = self.mode_messages[0]
            self.reply_message(reply_token, ai_response, mode_code)
            return None, mode_code, ai_response  # これ以降の処理をスキップします
            
        elif user_message.startswith("【モード:"):
            if "ファンタジー" in user_message:
                mode_code = 1
                self.dynamodb_handler.update_user_usage(user_id, 0, mode_code)
                prompt = '''
                            あなたはファンタジーストーリーをランダムで生成するストーリー作成者です。以下の要件を守ってください。
                            
                            ###あなたのルール
                            ・ストーリーは3回に分けて、ユーザーが行動を選択後に次のストーリーを送信してください。
                            ・主人公は私にしてください。
                            ・ストーリーは3回で終了してください。
                            ・ストーリーは1回毎にユーザーに対して、行動の選択肢を与えてください。
                            ・ストーリーは意外性のある展開にしてください。
                            ・ストーリーを進めてる間はたくさん絵文字を使用してください。
                        '''
                        
            elif "サスペンス" in user_message:
                mode_code = 2
                self.dynamodb_handler.update_user_usage(user_id, 0, mode_code)
                prompt = '''
                            あなたはサスペンスストーリーをランダムで生成するストーリー作成者です。以下の要件を守ってください。
                            
                            ###あなたのルール
                            ・ストーリーは3回に分けて、ユーザーが行動を選択後に次のストーリーを送信してください。
                            ・主人公は私にしてください。
                            ・ストーリーは3回で終了してください。
                            ・ストーリーは1回毎にユーザーに対して、行動の選択肢を与えてください。
                            ・ストーリーは意外性のある展開にしてください。
                            ・ストーリーを進めてる間はたくさん絵文字を使用してください。
                      '''
                      
            elif "コメディ" in user_message:
                mode_code = 3
                self.dynamodb_handler.update_user_usage(user_id, 0, mode_code)
                prompt = '''
                            あなたはコメディストーリーをランダムで生成するストーリー作成者です。以下の要件を守ってください。
                            
                            ###あなたのルール
                            ・ストーリーは3回に分けて、ユーザーが行動を選択後に次のストーリーを送信してください。
                            ・主人公は私にしてください。
                            ・ストーリーは3回で終了してください。
                            ・ストーリーは1回毎にユーザーに対して、行動の選択肢を与えてください。
                            ・ストーリーは意外性のある展開にしてください。
                            ・ストーリーを進めてる間はたくさん絵文字を使用してください。
                      '''
            elif "恋愛" in user_message:
                mode_code = 4
                self.dynamodb_handler.update_user_usage(user_id, 0, mode_code)
                prompt = '''
                            あなたは恋愛ストーリーをランダムで生成するストーリー作成者です。以下の要件を守ってください。
                            
                            ###あなたのルール
                            ・ストーリーは3回に分けて、ユーザーが行動を選択後に次のストーリーを送信してください。
                            ・主人公は私にしてください。
                            ・ストーリーは3回で終了してください。
                            ・ストーリーは1回毎にユーザーに対して、行動の選択肢を与えてください。
                            ・ストーリーは意外性のある展開にしてください。
                            ・ストーリーを進めてる間はたくさん絵文字を使用してください。
                      '''
            elif "ホラー" in user_message:
                mode_code = 5
                self.dynamodb_handler.update_user_usage(user_id, 0, mode_code)
                prompt = '''
                            あなたはホラーストーリーをランダムで生成するストーリー作成者です。以下の要件を守ってください。
                            
                            ###あなたのルール
                            ・ストーリーは3回に分けて、ユーザーが行動を選択後に次のストーリーを送信してください。
                            ・主人公は私にしてください。
                            ・ストーリーは3回で終了してください。
                            ・ストーリーは1回毎にユーザーに対して、行動の選択肢を与えてください。
                            ・ストーリーは意外性のある展開にしてください。
                            ・ストーリーを進めてる間はたくさん絵文字を使用してください。
                      '''
            elif "アドベンチャー" in user_message:
                mode_code = 6
                self.dynamodb_handler.update_user_usage(user_id, 0, mode_code)
                prompt = '''
                            あなたはアドベンチャーストーリーをランダムで生成するストーリー作成者です。以下の要件を守ってください。
                            
                            ###あなたのルール
                            ・ストーリーは3回に分けて、ユーザーが行動を選択後に次のストーリーを送信してください。
                            ・主人公は私にしてください。
                            ・ストーリーは3回で終了してください。
                            ・ストーリーは1回毎にユーザーに対して、行動の選択肢を与えてください。
                            ・ストーリーは意外性のある展開にしてください。
                            ・ストーリーを進めてる間はたくさん絵文字を使用してください。
                      '''
            elif "SF" in user_message:
                mode_code = 7
                self.dynamodb_handler.update_user_usage(user_id, 0, mode_code)
                prompt = '''
                            あなたはSFストーリーをランダムで生成するストーリー作成者です。以下の要件を守ってください。
                            
                            ###あなたのルール
                            ・ストーリーは3回に分けて、ユーザーが行動を選択後に次のストーリーを送信してください。
                            ・主人公は私にしてください。
                            ・ストーリーは3回で終了してください。
                            ・ストーリーは1回毎にユーザーに対して、行動の選択肢を与えてください。
                            ・ストーリーは意外性のある展開にしてください。
                            ・ストーリーを進めてる間はたくさん絵文字を使用してください。
                      '''
            elif "ミステリー" in user_message:
                mode_code = 8
                self.dynamodb_handler.update_user_usage(user_id, 0, mode_code)
                prompt = '''
                            あなたはミステリーストーリーをランダムで生成するストーリー作成者です。以下の要件を守ってください。
                            
                            ###あなたのルール
                            ・ストーリーは3回に分けて、ユーザーが行動を選択後に次のストーリーを送信してください。
                            ・主人公は私にしてください。
                            ・ストーリーは3回で終了してください。
                            ・ストーリーは1回毎にユーザーに対して、行動の選択肢を与えてください。
                            ・ストーリーは意外性のある展開にしてください。
                            ・ストーリーを進めてる間はたくさん絵文字を使用してください。
                      '''
        else:
            prompt = f'ユーザー：{user_message}\nAI：'
            self.dynamodb_handler.update_user_usage(user_id, 0, mode_code)
        
        conversation_history = self.dynamodb_handler.get_conversation_history(user_id)
        ai_response = self.openai_handler.get_ai_response(prompt, user_id, conversation_history,mode_code)
        self.reply_message(reply_token, ai_response, mode_code)
        return prompt, mode_code, ai_response

        

    def generate_quick_reply_items(self, mode_code):
        if mode_code == 0:
            quick_reply_items = [
                QuickReplyButton(action=MessageAction(label="ファンタジー", text="【モード:ファンタジー】")),
                QuickReplyButton(action=MessageAction(label="サスペンス", text="【モード:サスペンス】")),
                QuickReplyButton(action=MessageAction(label="コメディ", text="【モード:コメディ】")),
                QuickReplyButton(action=MessageAction(label="恋愛", text="【モード:恋愛】")),
                QuickReplyButton(action=MessageAction(label="ホラー", text="【モード:ホラー】")),
                QuickReplyButton(action=MessageAction(label="アドベンチャー", text="【モード:アドベンチャー】")),
                QuickReplyButton(action=MessageAction(label="SF", text="【モード:SF】")),
                QuickReplyButton(action=MessageAction(label="ミステリー", text="【モード:ミステリー】"))
            ]
        else:
            quick_reply_items = [
                QuickReplyButton(action=MessageAction(label="完了", text="【完了】"))
            ]
        return quick_reply_items
