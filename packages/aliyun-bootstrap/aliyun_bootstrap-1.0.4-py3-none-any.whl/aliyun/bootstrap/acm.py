try:
    import nacos
except ImportError:
    # If nacos is not available, make this module a no-op
    import sys
    sys.modules[__name__] = type('DummyACM', (), {
        'get_agent_url_from_acm': lambda *args, **kwargs: None
    })()
    # Skip the rest of the file
    __all__ = ['get_agent_url_from_acm']
    # Return early without executing the rest of the module
    print("Not found Naocos")

import json
import threading

import requests
import shutil


default_endpoint_internal_suffix_addr = "internal.edas.aliyun.com"
default_arms_namespace_id = "c845a7b4-23a1-4f28-a380-5ab30d8a280f"
finance_arms_namespace_id = "7602b2de-7eb8-4728-a13e-3f25954aee40"
gov_arms_namespace_id = "d8b73b92-9427-46e9-945c-6df6dca2af60"

acm_endpoint_name = {
    "cn-qingdao": "addr-qd-internal.edas.aliyun.com",
    "cn-beijing": "addr-bj-internal.edas.aliyun.com",
    "cn-hangzhou": "addr-hz-internal.edas.aliyun.com",
    "cn-shanghai": "addr-sh-internal.edas.aliyun.com",
    "cn-shenzhen": "addr-sz-internal.edas.aliyun.com",
    "cn-zhangjiakou": "addr-cn-zhangjiakou-internal.edas.aliyun.com",
    "cn-hongkong": "addr-hk-internal.edas.aliyuncs.com",
    "ap-southeast-1": "addr-singapore-internal.edas.aliyun.com",
    "cn-shanghai-finance-1": "addr-cn-shanghai-finance-1-internal.edas.aliyun.com",
    "cn-north-2-gov-1": "addr-cn-north-2-gov-1-internal.edas.aliyun.com",
    "cn-public": "acm.aliyun.com",
    "eu-central-1": "addr-eu-central-1-internal.edas.aliyun.com",
    "ap-southeast-2": "addr-ap-southeast-2-internal.edas.aliyun.com",
    "us-west-1": "addr-us-west-1-internal.edas.aliyun.com",
    "us-east-1": "addr-us-east-1-internal.edas.aliyun.com",
}

client = None
region_id = "cn-hangzhou"
app_id = ""

callback_funcs = []

config_json = None


def get_internal_endpoint_and_namespace_id(region_id):
    if region_id == "cn-hangzhou":
        return "addr-hz-" + default_endpoint_internal_suffix_addr, default_arms_namespace_id
    elif region_id == "cn-beijing":
        return "addr-bj-" + default_endpoint_internal_suffix_addr, default_arms_namespace_id
    elif region_id == "cn-shanghai":
        return "addr-sh-" + default_endpoint_internal_suffix_addr, default_arms_namespace_id
    elif region_id == "cn-shenzhen":
        return "addr-sz-" + default_endpoint_internal_suffix_addr, default_arms_namespace_id
    elif region_id == "cn-qingdao":
        return "addr-qd-" + default_endpoint_internal_suffix_addr, default_arms_namespace_id
    elif region_id == "cn-hongkong":
        return "addr-hk-" + default_endpoint_internal_suffix_addr, default_arms_namespace_id
    elif region_id == "ap-southeast-1":
        return "addr-singapore-" + default_endpoint_internal_suffix_addr, default_arms_namespace_id
    elif region_id == "cn-hangzhou-finance":
        return "addr-hz-internal.jbp.console.aliyun.com", finance_arms_namespace_id
    elif region_id == "cn-shanghai-finance-1":
        return "addr-cn-shanghai-finance-1-" + default_endpoint_internal_suffix_addr, finance_arms_namespace_id
    elif region_id == "cn-shenzhen-finance-1":
        return "addr-sz-internal.jbp.console.aliyun.com", finance_arms_namespace_id
    elif region_id == "cn-north-2-gov-1":
        return "addr-cn-north-2-gov-1-" + default_endpoint_internal_suffix_addr, gov_arms_namespace_id
    if region_id in acm_endpoint_name:
        return acm_endpoint_name[region_id], default_arms_namespace_id
    return "", ""


def get_public_endpoint_and_namespace_id():
    return "acm.aliyun.com", default_arms_namespace_id


def get_server_list(addr):
    url = addr + "/diamond-server/diamond"
    response = requests.request("GET", url)
    response = response.text.replace('\n', ',')
    if response[len(response) - 1] == ',':
        response = response[:len(response) - 1]
    return response


def is_connectable_with_url(url):
    try:
        response = requests.request("GET", url, timeout=1)
        if response.status_code == 200:
            return True
    except Exception:
        return False


def init_acm_client(_region_id, user_id):
    region_id = _region_id
    addr, ns = get_internal_endpoint_and_namespace_id(region_id)
    private = is_connectable_with_url("http://" + addr + ":8080/diamond-server/diamond")
    if addr == "" or not private:
        addr, ns = get_public_endpoint_and_namespace_id()

    server_list = get_server_list("http://" + addr + ":8080")
    client = nacos.NacosClient(server_addresses=server_list, namespace=ns)
    url = get_agent_init_config(client, user_id)
    return client

def get_config_data_id(user_id)->str:
    data_id = get_gray_config_data_id(user_id)
    if data_id is None:
        data_id =  "pyagent.global"
    return data_id
def get_gray_config_data_id(user_id):
    if user_id is None:
        return None
    data_id = f"onepilot.{user_id}"
    return data_id



def get_agent_init_config(client, user_id=None,region_id="cn-hangzhou"):
    if client is None:
        return
    data_id = get_config_data_id(user_id)
    content = client.get_config(data_id, region_id, 1)
    if content is None:
        print("get config from acm failed", content)
    print(content)
    config_json = json.loads(content)
    return config_json

def get_agent_url_from_acm(region_id="cn-hangzhou",user_id=None):
    client = init_acm_client(region_id, user_id)
    config = get_agent_init_config(client,user_id=user_id,region_id=region_id)
    latest_url = get_agent_url_from_config(config)
    _clear_tmp_file()
    return latest_url

def _clear_tmp_file():
    shutil.rmtree("nacos-data")

def get_agent_url_from_config(config):
    latest_url = None
    if "pythonAgent" in config:
        pyagent = config["pythonAgent"]
        if "latestUrl" in pyagent:
            latest_url = pyagent["latestUrl"]
        return latest_url
