from flask_restplus import Namespace, Resource, fields, model

api = Namespace("account", description=u"帳號及權限管理")

# base model
base_output_payload = api.model(u'基礎輸入參數定義', {
    'result': fields.Integer(required=True, default=0),
    'message': fields.String(required=True, default=" ")
})

# get_account_list
get_account_output = api.model(u'帳號清單',{
    'result': fields.Integer(required=True, default=0),
    'message': fields.String(required=True, default=" "),
    'data':fields.String(Required=True, example={'new_user_id':'', 'new_role':[], 'new_email':''})
})

#add_account_list
account_input_payload = api.model(u'輸入帳號', {
    'user_id': fields.String(required=True, example="account01"),
    'role': fields.List(fields.String(required=True, example="GENERAL_USER")),
    'email': fields.String(required=True, example="tami@tami.com")
})

# delete_account_list
delete_account_payload = api.model(u'帳號刪除input', {
    'user_id': fields.String(required=True, example="account01")
})
# Nested API

# update_account_list pep8
update_info = api.model(u'update_info', {
    'new_user_id': fields.String(required=True, example=" "),
    'new_role': fields.List(fields.String(required=True, example=" ")),
    'new_email': fields.String(required=True, example=" ")
})
update_account_payload = api.model(u'更新帳號資訊',{
    'old_user_id':fields.String(Required=True, example=" "),
    'data': fields.Nested(update_info)
})



# forget
account_forget_payload = api.model(u'忘記密碼',{
    'user_id': fields.String(required=True, example="itri@kuohwa.com")
})
       
# autosave_detect_table_payload
cells_info = api.model(u'cells',{
    'name': fields.String(reqired=True, example='cell_id'),
    'upper_left': fields.String(reqired=True, example='99,82'),
    'upper_right': fields.String(reqired=True, example='99,857'),
    'lower_right': fields.String(reqired=True, example='2356,857'),
    'lower_left': fields.String(reqired=True, example='2356,82'),
    'start_row': fields.Integer(reqired=True, example=0),
    'end_row': fields.Integer(reqired=True, example=2),
    'start_col': fields.Integer(reqired=True, example=0),
    'end_col': fields.Integer(reqired=True, example=3),
    'content': fields.String(reqired=True, example='example'),  
})

table_id_info = api.model(u'table_id_info',{
     'upper_left': fields.String(required=True, example='99,82'),
     'upper_right': fields.String(required=True, example='99,857'),
     'lower_right': fields.String(required=True, example='2356,857'),
     'lower_left': fields.String(required=True, example='2356,82'),
     'cells': fields.List(fields.Nested(cells_info))
     
})

page_number_info = api.model(u'page_number',{
    'table_id': fields.Nested(table_id_info)
})

data_info = api.model(u'data_info',{
    'page_number': fields.Nested(page_number_info)
})

                        
autosave_detect_table =api.model(u'表格偵測自動儲存',{
    'uuid': fields.String(required=True, example='sa5e122hy215cb3degrt'),
     'data': fields.Nested(data_info)
})
   
# get_detdect_table
table_payload = api.model(u'表格偵測輸入',{
    'uuid': fields.String(required=True, example='sa5e122hy215cb3degrt')
})

get_detdect_table_output = api.model(u'表格偵測輸出',{
    'result': fields.Integer(required=True, default=0),
    'message': fields.String(required=True, default=""),
    'data' : fields.Nested(data_info)
})

# autosave_key_value_mapping 
key_value_info = api.model(u'key_value_info',{
    'field': fields.String(required=True, example="epr_key"),
    'fieldvalue': fields.String(example=["Bor","Borad"]),
    'vendor': fields.String(required=False, example= " "),
    "file_type":fields.String(reqired=False, example=" ")
})

key_value_mapping = api.model(u'單元格偵測自動儲存',{
    "data": fields.List(fields.Nested(key_value_info))
    })
    

# get_key_value_mapping
get_key_value_mapping = api.model(u'ERP Key-Value 對照表 API',{
    "vendor":fields.String(example=' '),
    "file_type":fields.String(example=' '),
})

# autosave_image_path
autosave_image_path = api.model(u'自動儲存圖片路徑', {
    "uuid":fields.String(example=' '),
    "front_path":fields.String(example=' '),
    "back_path":fields.String(example=' ')
})

get_image_path = api.model(u'圖片路徑',{
    "uuid":fields.String(example=' ')
})                       
