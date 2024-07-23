from oci.exceptions import ServiceError
from base.oracle import OracleClientUtil
import oci

def get_subscriptions(ocu: OracleClientUtil):
    subscription_client = ocu.create_client("subscription")
    tenancy_id = ocu.tenancy()
    try:
        subscriptions = subscription_client.list_organization_subscriptions(compartment_id=tenancy_id).data
        start = str(subscriptions[0].time_start).split(" ")[0]
        print(start)
        return start
        # for subscription in subscriptions:
        #     subscription_id = subscription.id
        #     subscription_name = subscription.service_name
        #     subscription_start = str(subscription.time_start).split(" ")[0]
        #     subscription_end = str(subscription.time_end).split(" ")[0]
        #     result += (f"订阅ID: {subscription_id}\n"
        #                f"订阅名称: {subscription_name}\n"
        #                f"订阅起始日期: {subscription_start}\n"
        #                f"订阅结束日期: {subscription_end}\n")
    except ServiceError as e:
        return 'Error'