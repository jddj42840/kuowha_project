from apis import account
from base_api import CustomResource  # 加 __init__ 問題會變成 api
from apis.account.model import *    # import model 全部的物件
from apis.account.module import *   # 使用 OracelAcess 類別
from flask import session
import time
from configs import biz_consts # 設定值
from flask_mail import Mail, Message
# import smtplib  #use flask mail
import ast
import json
login_time = time.localtime()
# 專案API------------------------------
  
@api.route("/forget")
class Forget(CustomResource):
    @api.expect(account_forget_payload)
    # @api.marshal_with(base_output_payload)
    def post(self):
        from base_api import app    # 使用延遲導入，不怎麼 ok
        from flask import current_app
        forget_method = OracleAccess()
        data_list={}
        mail = Mail(app) 
        data = api.payload
        email_id = str(data['user_id'])
        # sql = "select * from account_login WHERE account LIKE '{}' ".format(email_id)
        sql = "select * from account where account='{}'".format(email_id)   # sql 語法在 sql developer 抓得到，用 account_list 也抓得到
        print(sql)
        data_list = forget_method.get(sql)
        data_list = data_list[0]
        print(data_list)
        # print(get_account_email)
        # print(gettext)
        Forget_message = Message("title", sender=('forgetbot42840@gmail.com'), recipients=[data_list[0]])
        # forget_article = "你的密碼為 : " + str(data_list[1])
        # print(type(forget_article))
        Forget_message.body = str(data_list[1])
        mail.send(Forget_message)
        print(app)
        return {'return':0, 'message':''}


# @api.route("/forget")
# class Forget(CustomResource):
#     @api.expect(account_forget_payload)
#     def post(self):
#         data = api.payload
#         email = data['user_id']
#         get_method = OracleAccess()
#         sql = "select * from account where account = '{}'".format(email)
#         account_lists = get_method.get(sql)
#         account_lists = account_lists[0]
        
#         # print(list)
#         return 'success'


@api.route("/get_account_list")
class Get_account_list(CustomResource):
    @api.marshal_with(get_account_output)
    def post(self):
        get_method = OracleAccess()
        sql = 'select * from account_list'
        getlist = get_method.get(sql)
        data = []
        for account_list in getlist:
            # print(account_list[0])
            user_id = account_list[0]
            user_role = account_list[1]
            user_mail = account_list[2]
            update_time = account_list[3]
            data.append({'user_id': user_id, 'role': user_role, 'email': user_mail, 'update_time': update_time})
        # print(data)
        # return 'success'
        return {'return':0, 'message':'', 'data':data}
    
    
@api.route("/add_account_list")
class Add_account_list(CustomResource):
    @api.expect(account_input_payload)
    @api.marshal_with(base_output_payload)
    def post(self):
        data = api.payload
        sql_method = OracleAccess()
        data = api.payload
        User_id = str(data['user_id'])
        User_role = str(data['role'])  # 如何輸入值為 list
        User_role.upper()
        Role_data = data['role']
        print (biz_consts.ROLE_DICT)
        User_email = str(data['email'])
        LoginTime = time.strftime("%Y-%m-%d", login_time)
        rows=[(User_id, User_role, User_email, LoginTime)]
        sql="insert into Account_list(user_id, userrole, useremail, logintime) values (:1, :2, :3, :4)"
        sql_method.insert(sql, rows)
        
        return {'return':0, 'message':''}
    
 
@api.route("/delete_account_list")
class Delete_account_list(CustomResource):
    @api.expect(delete_account_payload)
    @api.marshal_with(base_output_payload)
    def post(self):
        data = api.payload
        user_id = data['user_id']
        # print(User_id)
        sql_delet_method = OracleAccess()
        sql = 'delete from Account_list where user_id=:user_id'
        sql_delet_method.execute(sql,[user_id])
        return {'return':0, 'message':''}
    
    
@api.route("/update_account_list")
class Upload_account_list(CustomResource):
    @api.expect(update_account_payload)
    @api.marshal_with(base_output_payload)
    def post(self):
        payload = api.payload
        old_user_id = payload['old_user_id']
        update_data = payload['data']
        update_data = ast.literal_eval(update_data)
        new_user_id = update_data['new_user_id']
        new_role = str(update_data['new_role'])
        new_email = update_data['new_email']
        new_role = new_role.replace("'",'')
        print(new_role) # List
        
        UpdateTime = time.strftime("%Y-%m-%d", login_time)
        sql_update_metmod = OracleAccess()
        sql = "update Account_list set user_id='{}', userrole='{}', useremail='{}', loginTime='{}' where user_id='{}'".format(
            new_user_id, new_role, new_email, UpdateTime, old_user_id
        )
        print(sql)
        sql_update_metmod.update(sql)
        return {'return':0, 'message':''}
    
    
@api.route("/autosave_detect_table")
class Auto_save_detect_table(CustomResource):
    @api.expect(autosave_detect_table)
    @api.marshal_with(base_output_payload)
    def post(self):
        data = api.payload
        uuid = data['uuid']
        payload_data = data['data']
        res = ast.literal_eval(payload_data)
        text_dict = res.items()
        # payload_list = list(res)  # 轉為 list 格式
        keys = list(text_dict)
        page_number = keys[0][0]  # page_number
        inner_dict = keys[0][1] # inner dict
        get_table_id = inner_dict.get('table_id') # 取到 table_id 的 value
        upper_left = get_table_id.get('upper_left')
        upper_right = get_table_id.get('upper_right')
        lower_right = get_table_id.get('lower_right')
        lower_left = get_table_id.get('lower_left')
        get_cell = get_table_id.get('cells')    # cells(list) 底下的index[0] value 為 dict
        cells_values = get_cell[0]  # 取到 cells 底下的 dict
        cells_name = cells_values.get('name')
        cells_upper_left = cells_values.get('upper_left')
        cells_upper_right = cells_values.get('upper_right')
        cells_lower_rihght = cells_values.get('lower_right')
        cells_lower_left = cells_values.get('lower_left')
        cells_start_row = cells_values.get('start_row')
        cells_end_row = cells_values.get('end_row')
        cells_start_col = cells_values.get('start_col')
        cells_end_col = cells_values.get('end_col')
        cells_content = cells_values.get('content')
        # 另一種寫法，將所有dict 的 value 寫成一個 list
        cells_value_list = cells_values.values()
        # 將收取到的值存入DB
        rows = [(uuid, upper_left, upper_right, lower_right, lower_left, cells_name, cells_upper_left, 
               cells_upper_right, cells_lower_rihght, cells_lower_left, cells_start_row, cells_end_row,
               cells_start_col, cells_end_col, cells_content)]
        sql="insert into detect_table"\
            "(uuid, upper_left, upper_right, lower_left, lower_right, cell_name, cell_upper_left, cell_upper_right, cell_lower_left, cell_lower_right, start_row, end_row, start_col, end_col, content)"\
            " values (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11, :12, :13, :14, :15)"
        add_detect_table = OracleAccess()
        add_detect_table.insert(sql, rows)
        return {"result": 0, "message": "string"}
    


@api.route("/get_detect_table")
class Get_detect_table(CustomResource):
    @api.expect(table_payload)
    # @api.marshal_with(get_detdect_table_output)
    def post(self):
        data_input = api.payload
        uuid = data_input['uuid']
        sql = "SELECT * from detect_table where uuid = '{}'".format(uuid)
        get_detect_data = OracleAccess()
        text = get_detect_data.get(sql)
        text = text[0]
        # print(text)
        return_data = {"page_number":{"table_id":{
            "upper_left": text[1],
            "upper_right": text[2],
            "lower_right": text[3],
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
                "message":"",
                "data":return_data}


@api.route("/autosave_Key_value_mapping")
class Autosave_Key_value_mapping(CustomResource):
    @api.expect(key_value_mapping)
    @api.marshal_with(base_output_payload)
    def post(self):
        data = api.payload
        get_data = data.get('data')
        get_data = get_data[0]  # 去掉最外圍的list
        get_data = ast.literal_eval(get_data)
        dict_field = get_data.get('field')
        dict_filedvalue = str(get_data.get('fieldvalue'))
        dict_vendor = get_data.get('vendor')
        dict_type = get_data.get('file_type')
        rows=[(dict_field, dict_filedvalue, dict_vendor, dict_type)]
        sql = "insert into key_value_mapping(field, field_value, vendor, file_type) values(:1, :2, :3, :4)"
        sql_method = OracleAccess()
        sql_method.insert(sql,rows)
        print(dict_field, dict_filedvalue, dict_vendor, dict_type)
        
        # print(type(get_data))
        # print(dict_field)
        # print(type(data))     # type = dict
        return {"result": 0, "message": "string"}
   

@api.route("/get_key_value_mapping")
class Get_ket_value_mapping(CustomResource):
    @api.expect(get_key_value_mapping)
    # @api.marshal_with(base_output_payload)
    def post(self):
        data = api.payload
        vendor = data['vendor']
        file_type = data['file_type']
        # 均為空值
        data = {}
        if vendor == " " and file_type == " ":
            sql = 'SELECT * from key_value_mapping '
        # 其中一個不為空值
        elif vendor != ' ' and file_type == ' ':  # vendor有值
            sql = "select * from key_value_mapping where vendor = '{}'".format(vendor)
        elif vendor == ' ' and file_type != ' ':
            sql = "select * from key_value_mapping where file_type = '{}'".format(file_type)
        # 兩個均不為空值
        else:
            sql = "select * from key_value_mapping where vendor = '{}' and file_type = '{}'".format(vendor,file_type)
        print(sql)
        get_oracle = OracleAccess()
        DataBase_data = get_oracle.get(sql)     # 得到的值為 list 型態, 裡面的元素為 tupal
        for element in DataBase_data:
            # print(outside)
            index = element[0]
            inside_element = element[1]
            inside_element = inside_element.replace('"','')
            data[index] = inside_element
            
            # print(inside_element)
            # data.update( index = inside_element)
            
        # print{}
        
        return {"result": 0, "message": "string", "data":data}
    
    
@api.route("/autosave_image_path")
class Autosave_image_path(CustomResource):
    @api.expect(autosave_image_path)
    # @api.marshal_with(base_output_payload)
    def post(self):
        data = api.payload
        uuid = data['uuid']
        front_path = data['front_path']
        back_path = data['back_path']
        sql_method = OracleAccess()
        # 資料庫沒東西刪除原來不會錯
        
        sql = 'delete from image_path where uuid=:user_id'
        sql_method.execute(sql,[uuid])
        sql="insert into image_path(uuid, front_path, back_path) values (:1, :2, :3)"
        rows = [(uuid, front_path, back_path)]
        sql_method.insert(sql, rows) 

     
        # print(sql)
        return {"result": 0, "message": "string"}
    
    
@api.route("/get_image_path")
class Get_image_path(CustomResource):
    @api.expect(get_image_path)
    # @api.marshal_with(base_output_payload)
    def post(self):
        data = api.payload
        uuid = data['uuid']
        sql_method = OracleAccess()
        if uuid != " ":
            sql = "select * from image_path where uuid = '{}'".format(uuid)
            # print(sql)
            get_data = sql_method.get(sql)  # 目前的到的值型態為 list
            get_data = get_data[0]
            data = {"uuid": get_data[0], "front_path":get_data[1], "back_path":get_data[2]}
            return {"result": 0, "message": "string", "data":data}
        else:
            print("is null !")
            return " null "
    
