from oci.exceptions import ServiceError
from base.oracle import OracleClientUtil
import oci

def verify_account(ocu: OracleClientUtil):
    '''
    验证账号是否被封
    如果被封将无法获取到甲骨文上的用户ID, 并直接报错, 通过错误来返回无效配置
    '''
    idc = ocu.create_client("identity")
    tenancy = ocu.tenancy()
    region = ocu.region()
    try:
        users = idc.list_users(compartment_id=tenancy)
        for user in users.data:
            if user.id == ocu.user():
                pass
    except Exception as e:
        if 'NotAuthenticated' == e.code:
            return False