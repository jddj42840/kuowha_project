from flask_restplus import Namespace, Resource, fields, model

api = Namespace("account", description=u"帳號及權限管理")

# base model
base_output_payload = api.model(u'基礎輸入參數定義', {
    'result': fields.Integer(required=True, default=0),
    'message': fields.String(required=True, default="")
})

# get_account_list
get_account_output = api.model(u'帳號清單',{
    'result': fields.Integer(required=True, default=0),
    'message': fields.String(required=True, default=""),
    'data':fields.String(Required=True, example="{'new_user_id':'', 'new_role':[], 'new_email':''}")
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

# update_account_list
update_account_payload = api.model(u'更新帳號資訊',{
    'old_user_id':fields.String(Required=True, example="account01"),
    'data':fields.String(Required=True, example="{'new_user_id':'', 'new_role':[], 'new_email':''}")
    # 'data':fields
    
})


# forget
account_forget_payload = api.model(u'忘記密碼t',{
    'user_id': fields.String(required=True, example="itri@kuohwa.com"),
    
})
       
# autosave_detect_table_payload
autosave_detect_table = api.model(u'表格偵測自動儲存',{
    'uuid': fields.String(required=True, example='sa5e122hy215cb3degrt'),
    'data': fields.String(required=True, example="{ 'page_number':{ 'table_id':{ 'upper_left':'99,82', 'upper_right':'99,857', 'lower_right':'2356,857', 'lower_left':'2356,82', 'cells':[{'name':'cell_id1', 'upper_left':'99,82', 'upper_right':'99,857', 'lower_right':'2356,857', 'lower_left':'2356,82', 'start_row':0, 'end_row':2, 'start_col':0, 'end_col':3, 'content':'example'}] } } }" )
    
}) 
   
# get_detdect_table
table_payload = api.model(u'表格偵測輸入',{
    'uuid': fields.String(required=True, example='sa5e122hy215cb3degrt')
})

get_detdect_table_output = get_detdect_table = api.model(u'表格偵測輸出',{
    'result': fields.Integer(required=True, default=0),
    'message': fields.String(required=True, default=""),
    'data': fields.String(required=True, example="{ 'page_number':{ 'table_id':{ 'upper_left':'99,82', 'upper_right':'99,857', 'lower_right':'2356,857', 'lower_left':'2356,82', 'cells':[{'name':'cell_id1', 'upper_left':'99,82', 'upper_right':'99,857', 'lower_right':'2356,857', 'lower_left':'2356,82', 'start_row':0, 'end_row':2, 'start_col':0, 'end_col':3, 'content':'example'}] } } }" )
})

# autosave_key_value_mapping
key_value_mapping = api.model(u'單元格偵測自動儲存',{
    # "datas":fields.String(Required=True,example="data['field':'epr_key', 'fieldvalue':['Bo', 'Beoad'], 'vendor':'', 'file_type':'' ]")
    "data":fields.List(fields.String(required=True, example="{ 'field':'epr_key1', 'fieldvalue':['Bo','Borad'], 'vendor':'', 'file_type':'' }"))
    
})

# get_key_value_mapping
get_key_value_mapping = api.model(u'ERP Key-Value 對照表 API',{
    "vendor":fields.String(example=' '),
    "file_type":fields.String(example=' '),
    # "filse_type":fields.String(example='')

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
