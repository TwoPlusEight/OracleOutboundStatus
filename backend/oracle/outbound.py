import oci
from oci.exceptions import ServiceError
from base.oracle import OracleClientUtil, OracleModels
from base.OracleCloudBean import OracleCloudBean
from oracle.subscription import get_subscriptions
from datetime import datetime, timedelta


def get_data(ocu: OracleClientUtil, profile_name):
    """
    13-60 获取VNIC OCID/存储桶对应的出站流量/请求次数
    68-95 获取实例对应的网卡出站流量
    """
    ocb = OracleCloudBean()
    tenant_id = ocu.tenancy()
    region = ocu.region()
    usage_client = ocu.create_client("usage")
    network_client = ocu.create_client("network")
    compute_client = ocu.create_client('compute')
    current_time = datetime.now()
    month_start = current_time.replace(day=1)
    if current_time.month == 12:
        next_month = month_start.replace(year=current_time.year + 1, month=1)
    else:
        next_month = month_start.replace(month=current_time.month + 1)
    month_end = next_month - timedelta(days=1)

    time_usage_started = month_start.strftime("%Y-%m-%dT00:00:00Z")
    time_usage_ended = month_end.strftime("%Y-%m-%dT00:00:00Z")
    try:
        om = OracleModels(ocu)
        monthly_usage = usage_client.request_summarized_usages(
            om.monthly_usage_model(tenant_id, time_usage_started, time_usage_ended)
        )
    except ServiceError as e:
        return "Service Error"
    except Exception as e:
        return "Exception Error"

    json = {}
    instance_outbound = bucket_outbound = bucket_requests = 0.0
    for item in monthly_usage.data.items:
        if 'ocid1.vnic.' in item.resource_id:
            vnic_ocid = str(item.resource_id)
            try:
                # 获取VNIC的名称
                response = network_client.get_vnic(vnic_ocid)
                vnic_name = response.data.display_name
            except ServiceError as e:
                vnic_name = '已删除的网卡'
            json[vnic_ocid] = {
                "name": vnic_name,
                "outbound": round(item.computed_quantity, 4),
            }
            instance_outbound += round(item.computed_quantity, 4)

        if 'Object Storage - Outbound Data Transfer' in item.sku_name:
            bucket_outbound += round(item.computed_quantity, 4)

        if 'Object Storage - Requests' in item.sku_name:
            bucket_requests += round(item.computed_quantity, 4)

    total = round(instance_outbound + bucket_outbound, 4)
    json["bucket_requests"] = bucket_requests
    json["bucket_outbound"] = bucket_outbound
    json["total"] = total

    availability_domains = ocu.get_AD()
    for ad in availability_domains:
        try:
            instances = compute_client.list_instances(compartment_id=tenant_id, availability_domain=ad.name).data
        except ServiceError as e:
            return 'Error'

        if not instances:
            continue
        for instance in instances:
            id = instance.id

            display_name = instance.display_name
            shape = instance.shape

            config = instance.shape_config
            processor = config.processor_description
            try:
                vnic_attachments = oci.pagination.list_call_get_all_results(
                    compute_client.list_vnic_attachments,
                    compartment_id=instance.compartment_id,
                    instance_id=instance.id
                ).data
            except ServiceError as e:
                return 'Error'
            for va in vnic_attachments:
                data = json[va.vnic_id] if va.vnic_id in json else {"name": "None", "outbound":0.0}
                ocb.overwriteVNIC([data["name"], data["outbound"]])
            ocb.overwriteInstance([display_name, shape, processor])
            ocb.resetVNIC()
    ocb.overwriteBucket([bucket_requests, bucket_outbound])

    start_time = get_subscriptions(ocu=ocu)

    ocb.overwriteOracleCloud([profile_name, region, "", json["total"], start_time])
    return ocb.oracleCloud
