# -*- coding: UTF-8 -*-
from base_api.custom_cls import CustomMethodView, CustomRequestParser, CustomResource   # 在當前資料夾(base_api)導入類別
from flask import Blueprint, Flask, request, session
from utils.orcl_utils import OracleAccess   # 目前了解是跟 Oracle 有關

from base_api.custom_cls import Api     # 當前目錄底下的custom_cls 導入 Api 類
from apis.account.api import api as account_ns  # 從 account 目錄底下的 api.py 裡面導入 api 物件 <<api = Namespace(...)>> 的那句 並設為 account_ns
# from flask_mail import Mail, Message    # flask mail 
from configs import mail_consts 
api_blueprint = Blueprint('api', __name__, url_prefix='/api')   #blueprint :　藍圖　
api = Api(api_blueprint, version="0.0.1", description='', title='Kuohwa API Service', doc="/doc")   # swagger API 設定 ，我可以新增很多不同區塊的api

# init db
OracleAccess.initialise()

# init app
app = Flask(__name__, template_folder="../templates", static_folder="../static", static_url_path="")
app.config.SWAGGER_UI_DOC_EXPANSION = 'list'
app.config.SWAGGER_UI_REQUEST_DURATION = True
app.secret_key = "test123456789"    #session key
app.config['JSON_AS_ASCII'] = False

# mail
app.config.from_object(mail_consts)
# app.config['MAIL_SERVER']='smtp.gmail.com'
# app.config['MAIL_PORT'] = 465
# app.config['MAIL_USERNAME'] = 'forgetbot42840@gmail.com'
# app.config['MAIL_PASSWORD'] = 'pkbwxifbdyoshlim'
# app.config['MAIL_USE_TLS'] = False
# app.config['MAIL_USE_SSL'] = True
# app.config['SESSION_CRYPTO_KEY'] = load_aes_key()
# app.config["SESSION_COOKIE_HTTPONLY"] = True
# app.session_interface = EncryptedSessionInterface()


# register blueprint
app.register_blueprint(api_blueprint)   # 註冊 api_blueprint 可以在其他py檔案使用，使用前還需要再用第 10 行的方式叫出來

# register swagger api
api.add_namespace(account_ns)
# # namespace
# account_api = api.namespace("account", description=u"帳號及權限管理")
# table_api = api.namespace("table", description=u"表格偵測結構")
# cell_api = api.namespace("cell", description=u"單元格類型標記")
# orc_api = api.namespace("orc", description=u"ORC文字辨識")
# history_api = api.namespace("history", description=u"歷史編輯紀錄")
