import oci
from datetime import datetime, timedelta


def get_date_time():
    current_time = datetime.now()
    month_start = current_time.replace(day=1)
    if current_time.month == 12:
        next_month = current_time.replace(year=current_time.year + 1, month=1)
    else:
        next_month = current_time.replace(month=current_time.month)
    month_end = next_month - timedelta(days=1)

    formatted_month_start = month_start.strftime("%Y-%m-%dT00:00:00Z")
    formatted_month_end = month_end.strftime("%Y-%m-%dT00:00:00Z")
    return formatted_month_start, formatted_month_end


def get_all_instance_ip_and_usage(config):
    tenant = config["tenancy"]

    compute_client = oci.core.ComputeClient(config)
    virtual_network_client = oci.core.VirtualNetworkClient(config)
    usage_client = oci.usage_api.UsageapiClient(config)

    time_usage_started, time_usage_ended = get_date_time()
    vnic_lists = {}
    try:
        requestSummarizedUsagesDetails = oci.usage_api.models.RequestSummarizedUsagesDetails(
            tenant_id=tenant,
            # granularity='DAILY',
            granularity='MONTHLY',
            query_type='USAGE',
            group_by=['resourceId', 'skuName'],
            time_usage_started=time_usage_started,
            time_usage_ended=time_usage_ended,
            compartment_depth=2
        )

        # usageClient.request_summarized_usages
        request_summarized_usages = usage_client.request_summarized_usages(
            requestSummarizedUsagesDetails,
            retry_strategy=oci.retry.DEFAULT_RETRY_STRATEGY
        )

        data_usage = 0
        each_usage = ''
        for item in request_summarized_usages.data.items:
            if 'ocid1.vnic.' in item.resource_id:
                # 创建OCI SDK的客户端
                virtual_network_client = oci.core.VirtualNetworkClient(config)

                # 指定VNIC OCID
                vnic_ocid = str(item.resource_id)
                try:
                    # 获取VNIC的名称
                    response = virtual_network_client.get_vnic(vnic_ocid)
                    vnic_name = response.data.display_name
                except oci.exceptions.ServiceError as e:
                    vnic_name = '已删除的网卡'
                vnic_lists[vnic_ocid] = {'name': vnic_name, 'usage': f'{item.computed_quantity:.3f}GB'}
    except oci.exceptions.ServiceError as e:
        print("Service Error")
    except Exception as e:
        print("Exception Error")

    try:
        instance_list = compute_client.list_instances(compartment_id=tenant).data
        result = (
            f'获取实例列表\n'
            f'`-----------------------------------`\n'
            f'`名称 | OCPU | 内存(GB) | 配置 | 网卡名称 | 内网IP | 公网IP | 出站流量`\n'
        )
        for instance in instance_list:
            instance_id = instance.id  # ID
            instance_compartment_id = instance.compartment_id  # tenancy id
            display_name = instance.display_name  # 名称
            config = instance.shape_config
            cpu = config.ocpus  # OCPU
            mem = config.memory_in_gbs  # 内存
            shape = instance.shape  # 配置

            vnic_attachments = oci.pagination.list_call_get_all_results(
                compute_client.list_vnic_attachments,
                compartment_id=instance.compartment_id,
                instance_id=instance.id
            ).data
            vnics = [virtual_network_client.get_vnic(va.vnic_id).data for va in vnic_attachments]
            # print(vnics)
            for vnic in vnics:
                vnic_name = vnic_lists[vnic.id]['name']
                vnic_usage = vnic_lists[vnic.id]['usage']
                private_ip = vnic.private_ip
                if vnic.public_ip:
                    public_ip = vnic.public_ip
                else:
                    public_ip = "None"
                result += (
                    f"{display_name} | {cpu:.0f} | {mem:.0f} | {shape} | {vnic_name} | {private_ip} | {public_ip} | {vnic_usage}\n")
        print(result)
    except oci.exceptions.ServiceError as e:
        print(e)


config = oci.config.from_file(r'./configs/seoul.conf', 'Seoul')
get_all_instance_ip_and_usage(config)
