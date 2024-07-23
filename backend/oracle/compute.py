from oci.exceptions import ServiceError
from base.oracle import OracleClientUtil
import oci

def list_all_instance(ocu: OracleClientUtil, return_list: bool = False):
    network_client = ocu.create_client('network')
    compute_client = ocu.create_client('compute')
    tenancy = ocu.tenancy()
    region = ocu.region()
    instance_name_vnic_list = {}
    try:
        availability_domains = ocu.get_AD()
        for ad in availability_domains:
            instances = compute_client.list_instances(compartment_id=tenancy, availability_domain=ad.name).data
            if instances:
                instance_result = (
                    f'当前可用性域(`{ad.name}`)下的实例有:\n'
                )
                for instance in instances:
                    id = instance.id

                    display_name = instance.display_name
                    shape = instance.shape

                    config = instance.shape_config
                    processor = config.processor_description
                    instance_data= [display_name, shape]  #
                    vnic_attachments = oci.pagination.list_call_get_all_results(
                        compute_client.list_vnic_attachments,
                        compartment_id=instance.compartment_id,
                        instance_id=instance.id
                    ).data
                    for va in vnic_attachments:
                        print(va.vnic_id)
                        vnic_ocid = network_client.get_vnic(va.vnic_id).data.id
                        instance_name_vnic_list[vnic_ocid] = {'name': display_name, 'availability_domain': ad.name}
        if return_list:
            if instance_name_vnic_list:
                print(instance_name_vnic_list)
                return instance_name_vnic_list
            else:
                return {}
    except ServiceError as e:
        return 'Error'
