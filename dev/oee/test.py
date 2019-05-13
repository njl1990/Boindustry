from common import ResponseMsg
# Create your tests here.

data = {'data': 'data'}
msg = "error"
RMsg=ResponseMsg()

print(RMsg.success(data=data))
print(RMsg.failed(msg=msg))