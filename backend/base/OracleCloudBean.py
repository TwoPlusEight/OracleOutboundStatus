class OracleCloudBean:
    def __init__(self):
        self.oracleCloud = {}
        self._name = ""
        self._region = ""
        self._totalOutbound = 0.0
        self._subscriptionStartTime = ""
        self._oracleCloudMap = {
            0: self._setName,
            1: self._setRegion,
            2: self._setAvailableDomain,
            3: self._setTotalOutbound,
            4: self._setSubscriptionStartTime
        }

        self.instance = []
        self._instanceName = ""
        self._instanceShape = ""
        self._instanceCPU = ""
        self._instanceOCID = ""
        self._instanceMap = {
            0: self._setInstanceName,
            1: self._setInstanceShape,
            2: self._setInstanceCPU
        }

        self.VNIC = []
        self._VNICName = ""
        self._VNICOutbound = 0.0
        self._VNICMap = {
            0: self._setVNICName,
            1: self._setVNICOutbound,
        }

        self._bucket = {}
        self._bucketRequests = 0.0
        self._bucketOutbound = 0.0
        self._bucketMap = {
            0: self._setBucketRequests,
            1: self._setBucketOutbound
        }

    #####
    # 存储桶数据
    #####
    def _setBucketRequests(self, bucketRequests):
        self._bucketRequests = bucketRequests

    def _setBucketOutbound(self, bucketOutbound):
        self._bucketOutbound = bucketOutbound

    def _setBucket(self):
        self._bucket = {
            "requests": self._bucketRequests,
            "outbound": self._bucketOutbound
        }

    def overwriteBucket(self, row: list):
        """
        写入存储桶数据
        :param row: [请求次数, 出站流量]
        :return:
        """
        for data in row:
            index = row.index(data)
            self._bucketMap[index](data)
        self._setBucket()

    #####
    # 虚拟网卡数据
    #####
    def _setVNICName(self, VNICName):
        self._VNICName = VNICName

    def _setVNICOutbound(self, VNICOutbound):
        self._VNICOutbound = VNICOutbound

    # def _setVNICOCID(self, VNICOCID):
    #     self._VNICOCID = VNICOCID

    def _addVNIC(self):
        vnic = {
            "name": self._VNICName,
            "outbound": self._VNICOutbound
        }
        self.VNIC.append(vnic)

    def resetVNIC(self):
        self.VNIC = []

    def overwriteVNIC(self, row: list):
        """
        写入网卡数据
        :param row: [网卡名称, 出站流量]
        :return:
        """
        for data in row:
            index = row.index(data)
            self._VNICMap[index](data)
        self._addVNIC()

    #####
    # 实例数据
    #####
    def _setInstanceName(self, instanceName):
        self._instanceName = instanceName

    def _setInstanceShape(self, instanceShape):
        self._instanceShape = instanceShape

    def _setInstanceCPU(self, instanceCPU):
        self._instanceCPU = instanceCPU

    # def _setInstanceOCID(self, instanceOCID):
    #     self._instanceOCID = instanceOCID

    def _addInstance(self):
        instance = {
            "name": self._instanceName,
            "shape": self._instanceShape,
            "cpu": self._instanceCPU,
            "vnic": self.VNIC
        }
        self.instance.append(instance)

    def overwriteInstance(self, row: list):
        for data in row:
            index = row.index(data)
            self._instanceMap[index](data)
        self._addInstance()

    #####
    # 账号数据
    #####
    def _setName(self, name):
        self._name = name

    def _setRegion(self, region):
        self._region = region

    def _setAvailableDomain(self, availableDomain):
        self._availableDomain = availableDomain

    def _setTotalOutbound(self, totalOutbound):
        self._totalOutbound = totalOutbound
    
    def _setSubscriptionStartTime(self, subscriptionStartTime):
        self._subscriptionStartTime = subscriptionStartTime

    #####
    # 所有账号数据
    #####
    def addOracleCloud(self):
        oci = {
            "name": self._name,
            "region": self._region,
            "subsStartTime": self._subscriptionStartTime,
            "data": {
                # "availableDomain": self._availableDomain,
                "outbound": self._totalOutbound,
                "instance": self.instance,
                "bucket": self._bucket
            }
        }
        self.oracleCloud = oci

    def overwriteOracleCloud(self, row: list):
        for data in row:
            index = row.index(data)
            self._oracleCloudMap[index](data)
        self.addOracleCloud()
