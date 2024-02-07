import oci


class RaiseException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message


def identity_client(config):
    """
    身份客户端(确实想不到什么更合适的名称)

    参数:
    config: 用户配置的字典

    返回值:
    IdentityClient: 身份客户端的服务
    """
    return oci.identity.IdentityClient(config)


def compute_client(config):
    """
    计算客户端(确实想不到什么更合适的名称)

    参数:
    config: 用户配置的字典

    返回值:
    ComputeClient: 计算客户端的服务
    """
    return oci.core.ComputeClient(config)


def virtual_network_client(config):
    """
    虚拟云网客户端

    参数:
    config: 用户配置的字典

    返回值:
    VirtualNetworkClient: 虚拟云网客户端的服务
    """
    return oci.core.VirtualNetworkClient(config)


def usage_client(config):
    """
    使用量客户端

    参数:
    config: 用户配置的字典

    返回值:
    UsageapiClient: 使用量客户端的服务
    """
    return oci.usage_api.UsageapiClient(config)


def subscription_client(config):
    """
    订阅客户端

    参数:
    config: 用户配置的字典

    返回值:
    OrganizationSubscriptionClient: 使用量客户端的服务
    """
    return oci.onesubscription.OrganizationSubscriptionClient(config)


def limits_client(config):
    """
    配额客户端

    参数:
    config: 用户配置的字典

    返回值:
    LimitsClient: 使用量客户端的服务
    """
    return oci.limits.LimitsClient(config)


def default_case():
    raise RaiseException("Current client have not included.")


class OracleClientUtil:
    def __init__(self, user_configuration_dir, user_configuration_name):
        self.config = oci.config.from_file(user_configuration_dir, user_configuration_name)

    def create_client(self, client_name):
        """
        根据需要的客户端名称返回对应服务

        参数:
        user_configuration_dir: 用户配置文件路径
        user_configuration_name: 用户配置文件标题
        client_name: 客户端名称
        - identity
        - compute
        - network
        - usage
        - subscription
        - limits

        对应client_name的返回值:
        IdentityClient
        ComputeClient
        VirtualNetworkClient
        UsageapiClient
        OrganizationSubscriptionClient
        LimitsClient
        """
        """
        用于选择客户端
        """
        clients = {
            'identity': identity_client,
            'compute': compute_client,
            'network': virtual_network_client,
            'usage': usage_client,
            'subscription': subscription_client,
            'limits': limits_client,
        }
        return clients.get(client_name, default_case)(self.config)

    def tenancy(self):
        """
        获取当前租户名称
        """
        return self.config['tenancy']

    def region(self):
        """
        获取当前区域名称
        """
        return self.config['region']

    def fingerprint(self):
        """
        获取当前租户密钥指纹
        """
        return self.config['fingerprint']

    def get_AD(self):
        """
        获取当前租户下的所有可用性域
        """
        identityClient = self.create_client('identity')
        availability_domains = identityClient.list_availability_domains(self.tenancy()).data
        return availability_domains

    def usage_model(self):
        return oci.usage_api.models


class OracleModels:
    def __init__(self, ocu: OracleClientUtil):
        self.ocu = ocu

    def monthly_usage_model(self, tenant_id, start, end):
        model = self.ocu.usage_model().RequestSummarizedUsagesDetails(
            tenant_id=tenant_id,
            granularity='MONTHLY',
            query_type='USAGE',
            group_by=['resourceId', 'skuName'],
            time_usage_started=start,
            time_usage_ended=end,
            compartment_depth=2
        )
        return model
