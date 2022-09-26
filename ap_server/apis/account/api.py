from base_api import CustomResource  # 加 __init__ 問題會變成 api
# from base_api import *
from apis.account.model import *    # import model 全部的物件
from apis.account.module import *   # 使用 OracelAcess 類別
import time
from configs import biz_consts # 設定值
from flask_mail import Message
from base_api.__init__ import mail
login_time = time.localtime()
# 專案API------------------------------
# module 寫邏輯(要改) autopep8
@api.route("/forget")
class Forget(CustomResource):
    @api.expect(account_forget_payload)
    @api.marshal_with(base_output_payload)
    def post(self):
        data = api.payload
        sql = "select * from account where account=:0"   # sql 語法在 sql developer 抓得到，用 account_list 也抓得到
        data_list = OracleAccess.query(sql, [data['user_id']])[0]
        Forget_message = Message("title",
                                 sender=('forgetbot42840@gmail.com'),
                                 recipients=[data_list[0]])
        Forget_message.body = data_list[1]
        mail.send(Forget_message)
        return {'return':0, 'message':''}


@api.route("/get_account_list")
class Get_account_list(CustomResource):
    @api.marshal_with(get_account_output)
    def post(self):
        sql = 'select * from account_list'
        data = []
        for account_list in OracleAccess.query(sql):
            data.append({'user_id': account_list[0], 
                         'role': account_list[1], 'email': account_list[2], 
                         'update_time': account_list[3]})
        return {'return':0, 'message':'', 'data':data}
    
    
@api.route("/add_account_list")
class Add_account_list(CustomResource):
    @api.expect(account_input_payload)
    @api.marshal_with(base_output_payload)
    def post(self):
        data = api.payload
        rows=[(data['user_id'], str(data['role']).upper(), data['email'], 
               time.strftime("%Y-%m-%d", login_time))]
        sql="insert into Account_list(user_id, userrole, useremail, logintime) values (:1, :2, :3, :4)"
        OracleAccess.insert(sql, rows)
        return {'return':0, 'message':''}
    
 
@api.route("/delete_account_list")
class Delete_account_list(CustomResource):
    @api.expect(delete_account_payload)
    @api.marshal_with(base_output_payload)
    def post(self):
        data = api.payload
        sql = 'delete from Account_list where user_id=:user_id'
        OracleAccess.execute(sql,[data['user_id']])
        return {'return':0, 'message':''}
    
# 使用 Nested、model有誤(修正)
@api.route("/update_account_list")
class Upload_account_list(CustomResource):
    @api.expect(update_account_payload)
    @api.marshal_with(base_output_payload)
    def post(self):
        payload = api.payload
        new_info = payload.get('data')
        sql = "update Account_list set user_id='{}', userrole='{}', useremail='{}', loginTime='{}' where user_id='{}'".format(
            new_info.get('new_user_id'), 
            str(new_info.get('new_role')).replace("'",''), new_info.get('new_email'), 
            time.strftime("%Y-%m-%d", login_time), payload['old_user_id']
        )
        OracleAccess.update(sql)    # execute
        return {'return':0, 'message':''}
    
# Nested (簡化)
@api.route("/autosave_detect_table")
class Auto_save_detect_table(CustomResource):
    @api.expect(autosave_detect_table)
    @api.marshal_with(base_output_payload)
    def post(self):
        data = api.payload
        table_id_data = list(data['data']['page_number']['table_id'].values())
        cells_data = list(data['data']['page_number']['table_id']['cells'][0].values())
        rows = [data['uuid']]
        rows.extend(table_id_data[0:4])
        rows.extend(cells_data[0:10])
        sql="""insert into detect_table
            (uuid, upper_left, upper_right,
             lower_left, lower_right, cell_name,
             cell_upper_left, cell_upper_right, cell_lower_left,
             cell_lower_right, start_row, end_row,
             start_col, end_col, content)
             values (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11, :12, :13, :14, :15)"""
        OracleAccess.insert(sql, [rows])
        return {"result": 0, "message": " "}
    

# NEST 勿使用formate(修正)
@api.route("/get_detect_table")
class Get_detect_table(CustomResource):
    @api.expect(table_payload)
    @api.marshal_with(get_detdect_table_output)
    def post(self):
        data_input = api.payload
        sql = "SELECT * from DETECT_TABLE where uuid =:0 "
        text = OracleAccess.query(sql, [data_input['uuid']])[0]
        return_data = {"page_number":{"table_id":{
            "upper_left":text[1],
            "upper_right":text[2],
            "lower_right":text[3],
            "lower_left":text[4],
            "cells":[
                {
                    "name":text[5],
                    "upper_left":text[6],
                    "upper_right":text[7],
                    "lower_right":text[8],
                    "lower_left":text[9],
                    "start_row":text[10],
                    "end_row":text[11],
                    "start_col":text[12],
                    "end_col":text[13],
                    "content":text[14]
                }
            ]
        }}}
        return {"result":0,
                "message":" ",
                "data":return_data}

# Nested(簡化)
@api.route("/autosave_Key_value_mapping")
class Autosave_Key_value_mapping(CustomResource):
    @api.expect(key_value_mapping)
    @api.marshal_with(base_output_payload)
    def post(self):
        data = api.payload
        dict_info = list(data['data'][0].values())
        rows =(dict_info[0], str(dict_info[1]), dict_info[2], dict_info[3])
        print(rows)
        sql = """insert into key_value_mapping(field, field_value, vendor, file_type)
                values(:1, :2, :3, :4)"""
        OracleAccess.insert(sql,[rows])
        return {"result": 0, "message": "string"}
   
# Nested
@api.route("/get_key_value_mapping")
class Get_ket_value_mapping(CustomResource):
    @api.expect(get_key_value_mapping)
    def post(self):
        data = api.payload
        vendor = data['vendor']
        file_type = data['file_type']
        # 均為空值
        data = {}
        if vendor == ' ' and file_type == ' ':
            sql = 'SELECT * from key_value_mapping '
        # 其中一個不為空值
        elif vendor != ' ' and file_type == ' ':  # vendor有值
            sql = "select * from key_value_mapping where vendor = '{}'".format(vendor)
        elif vendor == ' ' and file_type != ' ':
            sql = "select * from key_value_mapping where file_type = '{}'".format(file_type)
        # 兩個均不為空值
        else:
            sql = "select * from key_value_mapping where vendor = '{}' and file_type = '{}'".format(vendor,file_type)
        DataBase_data = OracleAccess.query(sql)     # 得到的值為 list 型態, 裡面的元素為 tupal
        for element in DataBase_data:
            index = element[0]
            inside_element = element[1].replace('"','')
            data[index] = inside_element    # 變得跟dict一樣       
        return {"result": 0, "message": "string", "data":data}
    
    
@api.route("/autosave_image_path")
class Autosave_image_path(CustomResource):
    @api.expect(autosave_image_path)
    # @api.marshal_with(base_output_payload)
    def post(self):
        data = api.payload
        uuid = data['uuid']
        # 資料庫沒東西刪除原來不會錯
        sql = 'delete from image_path where uuid=:user_id'
        OracleAccess.execute(sql,[uuid])
        sql="insert into image_path(uuid, front_path, back_path) values (:1, :2, :3)"
        OracleAccess.insert(sql, [(uuid, data['front_path'], data['back_path'])]) 
        return {"result": 0, "message": "string"}
    
# 不可使用字串方式 NO format(修正)
@api.route("/get_image_path")
class Get_image_path(CustomResource):
    @api.expect(get_image_path)
    def post(self):
        data = api.payload
        if data['uuid'] == " ":
            return {"result": 1, "message": "error"}
        sql = "select * from image_path where uuid = :1"
        get_data = OracleAccess.query(sql, [data['uuid']])[0]  # 目前的到的值型態為 list
        data = {"uuid": get_data[0], "front_path":get_data[1], "back_path":get_data[2]}
        return {"result": 0, "message": "string", "data":data}

    
