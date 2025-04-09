r'''
# CDKTF prebuilt bindings for terraform-provider-openstack/openstack provider version ~> 3.0.0

This repo builds and publishes the [Terraform openstack provider](https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0.0/docs) bindings for [CDK for Terraform](https://cdk.tf).

## Available Packages

### NPM

The npm package is available at [https://www.npmjs.com/package/@cdktf/provider-openstack](https://www.npmjs.com/package/@cdktf/provider-openstack).

`npm install @cdktf/provider-openstack`

### PyPI

The PyPI package is available at [https://pypi.org/project/cdktf-cdktf-provider-openstack](https://pypi.org/project/cdktf-cdktf-provider-openstack).

`pipenv install cdktf-cdktf-provider-openstack`

### Nuget

The Nuget package is available at [https://www.nuget.org/packages/HashiCorp.Cdktf.Providers.Openstack](https://www.nuget.org/packages/HashiCorp.Cdktf.Providers.Openstack).

`dotnet add package HashiCorp.Cdktf.Providers.Openstack`

### Maven

The Maven package is available at [https://mvnrepository.com/artifact/com.hashicorp/cdktf-provider-openstack](https://mvnrepository.com/artifact/com.hashicorp/cdktf-provider-openstack).

```
<dependency>
    <groupId>com.hashicorp</groupId>
    <artifactId>cdktf-provider-openstack</artifactId>
    <version>[REPLACE WITH DESIRED VERSION]</version>
</dependency>
```

### Go

The go package is generated into the [`github.com/cdktf/cdktf-provider-openstack-go`](https://github.com/cdktf/cdktf-provider-openstack-go) package.

`go get github.com/cdktf/cdktf-provider-openstack-go/openstack/<version>`

Where `<version>` is the version of the prebuilt provider you would like to use e.g. `v11`. The full module name can be found
within the [go.mod](https://github.com/cdktf/cdktf-provider-openstack-go/blob/main/openstack/go.mod#L1) file.

## Docs

Find auto-generated docs for this provider here:

* [Typescript](./docs/API.typescript.md)
* [Python](./docs/API.python.md)
* [Java](./docs/API.java.md)
* [C#](./docs/API.csharp.md)
* [Go](./docs/API.go.md)

You can also visit a hosted version of the documentation on [constructs.dev](https://constructs.dev/packages/@cdktf/provider-openstack).

## Versioning

This project is explicitly not tracking the Terraform openstack provider version 1:1. In fact, it always tracks `latest` of `~> 3.0.0` with every release. If there are scenarios where you explicitly have to pin your provider version, you can do so by [generating the provider constructs manually](https://cdk.tf/imports).

These are the upstream dependencies:

* [CDK for Terraform](https://cdk.tf)
* [Terraform openstack provider](https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0.0)
* [Terraform Engine](https://terraform.io)

If there are breaking changes (backward incompatible) in any of the above, the major version of this project will be bumped.

## Features / Issues / Bugs

Please report bugs and issues to the [CDK for Terraform](https://cdk.tf) project:

* [Create bug report](https://cdk.tf/bug)
* [Create feature request](https://cdk.tf/feature)

## Contributing

### Projen

This is mostly based on [Projen](https://github.com/projen/projen), which takes care of generating the entire repository.

### cdktf-provider-project based on Projen

There's a custom [project builder](https://github.com/cdktf/cdktf-provider-project) which encapsulate the common settings for all `cdktf` prebuilt providers.

### Provider Version

The provider version can be adjusted in [./.projenrc.js](./.projenrc.js).

### Repository Management

The repository is managed by [CDKTF Repository Manager](https://github.com/cdktf/cdktf-repository-manager/).
'''
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

import typeguard
from importlib.metadata import version as _metadata_package_version
TYPEGUARD_MAJOR_VERSION = int(_metadata_package_version('typeguard').split('.')[0])

def check_type(argname: str, value: object, expected_type: typing.Any) -> typing.Any:
    if TYPEGUARD_MAJOR_VERSION <= 2:
        return typeguard.check_type(argname=argname, value=value, expected_type=expected_type) # type:ignore
    else:
        if isinstance(value, jsii._reference_map.InterfaceDynamicProxy): # pyright: ignore [reportAttributeAccessIssue]
           pass
        else:
            if TYPEGUARD_MAJOR_VERSION == 3:
                typeguard.config.collection_check_strategy = typeguard.CollectionCheckStrategy.ALL_ITEMS # type:ignore
                typeguard.check_type(value=value, expected_type=expected_type) # type:ignore
            else:
                typeguard.check_type(value=value, expected_type=expected_type, collection_check_strategy=typeguard.CollectionCheckStrategy.ALL_ITEMS) # type:ignore

from ._jsii import *

__all__ = [
    "bgpvpn_network_associate_v2",
    "bgpvpn_port_associate_v2",
    "bgpvpn_router_associate_v2",
    "bgpvpn_v2",
    "blockstorage_qos_association_v3",
    "blockstorage_qos_v3",
    "blockstorage_quotaset_v3",
    "blockstorage_volume_attach_v3",
    "blockstorage_volume_type_access_v3",
    "blockstorage_volume_type_v3",
    "blockstorage_volume_v3",
    "compute_aggregate_v2",
    "compute_flavor_access_v2",
    "compute_flavor_v2",
    "compute_instance_v2",
    "compute_interface_attach_v2",
    "compute_keypair_v2",
    "compute_quotaset_v2",
    "compute_servergroup_v2",
    "compute_volume_attach_v2",
    "containerinfra_cluster_v1",
    "containerinfra_clustertemplate_v1",
    "containerinfra_nodegroup_v1",
    "data_openstack_blockstorage_availability_zones_v3",
    "data_openstack_blockstorage_quotaset_v3",
    "data_openstack_blockstorage_snapshot_v3",
    "data_openstack_blockstorage_volume_v3",
    "data_openstack_compute_aggregate_v2",
    "data_openstack_compute_availability_zones_v2",
    "data_openstack_compute_flavor_v2",
    "data_openstack_compute_hypervisor_v2",
    "data_openstack_compute_instance_v2",
    "data_openstack_compute_keypair_v2",
    "data_openstack_compute_limits_v2",
    "data_openstack_compute_quotaset_v2",
    "data_openstack_containerinfra_cluster_v1",
    "data_openstack_containerinfra_clustertemplate_v1",
    "data_openstack_containerinfra_nodegroup_v1",
    "data_openstack_dns_zone_v2",
    "data_openstack_fw_group_v2",
    "data_openstack_fw_policy_v2",
    "data_openstack_fw_rule_v2",
    "data_openstack_identity_auth_scope_v3",
    "data_openstack_identity_endpoint_v3",
    "data_openstack_identity_group_v3",
    "data_openstack_identity_project_ids_v3",
    "data_openstack_identity_project_v3",
    "data_openstack_identity_role_v3",
    "data_openstack_identity_service_v3",
    "data_openstack_identity_user_v3",
    "data_openstack_images_image_ids_v2",
    "data_openstack_images_image_v2",
    "data_openstack_keymanager_container_v1",
    "data_openstack_keymanager_secret_v1",
    "data_openstack_loadbalancer_flavor_v2",
    "data_openstack_networking_addressscope_v2",
    "data_openstack_networking_floatingip_v2",
    "data_openstack_networking_network_v2",
    "data_openstack_networking_port_ids_v2",
    "data_openstack_networking_port_v2",
    "data_openstack_networking_qos_bandwidth_limit_rule_v2",
    "data_openstack_networking_qos_dscp_marking_rule_v2",
    "data_openstack_networking_qos_minimum_bandwidth_rule_v2",
    "data_openstack_networking_qos_policy_v2",
    "data_openstack_networking_quota_v2",
    "data_openstack_networking_router_v2",
    "data_openstack_networking_secgroup_v2",
    "data_openstack_networking_subnet_ids_v2",
    "data_openstack_networking_subnet_v2",
    "data_openstack_networking_subnetpool_v2",
    "data_openstack_networking_trunk_v2",
    "data_openstack_sharedfilesystem_availability_zones_v2",
    "data_openstack_sharedfilesystem_share_v2",
    "data_openstack_sharedfilesystem_sharenetwork_v2",
    "data_openstack_sharedfilesystem_snapshot_v2",
    "db_configuration_v1",
    "db_database_v1",
    "db_instance_v1",
    "db_user_v1",
    "dns_recordset_v2",
    "dns_transfer_accept_v2",
    "dns_transfer_request_v2",
    "dns_zone_v2",
    "fw_group_v2",
    "fw_policy_v2",
    "fw_rule_v2",
    "identity_application_credential_v3",
    "identity_ec2_credential_v3",
    "identity_endpoint_v3",
    "identity_group_v3",
    "identity_inherit_role_assignment_v3",
    "identity_project_v3",
    "identity_role_assignment_v3",
    "identity_role_v3",
    "identity_service_v3",
    "identity_user_membership_v3",
    "identity_user_v3",
    "images_image_access_accept_v2",
    "images_image_access_v2",
    "images_image_v2",
    "keymanager_container_v1",
    "keymanager_order_v1",
    "keymanager_secret_v1",
    "lb_flavorprofile_v2",
    "lb_l7_policy_v2",
    "lb_l7_rule_v2",
    "lb_listener_v2",
    "lb_loadbalancer_v2",
    "lb_member_v2",
    "lb_members_v2",
    "lb_monitor_v2",
    "lb_pool_v2",
    "lb_quota_v2",
    "networking_addressscope_v2",
    "networking_floatingip_associate_v2",
    "networking_floatingip_v2",
    "networking_network_v2",
    "networking_port_secgroup_associate_v2",
    "networking_port_v2",
    "networking_portforwarding_v2",
    "networking_qos_bandwidth_limit_rule_v2",
    "networking_qos_dscp_marking_rule_v2",
    "networking_qos_minimum_bandwidth_rule_v2",
    "networking_qos_policy_v2",
    "networking_quota_v2",
    "networking_rbac_policy_v2",
    "networking_router_interface_v2",
    "networking_router_route_v2",
    "networking_router_v2",
    "networking_secgroup_rule_v2",
    "networking_secgroup_v2",
    "networking_subnet_route_v2",
    "networking_subnet_v2",
    "networking_subnetpool_v2",
    "networking_trunk_v2",
    "objectstorage_account_v1",
    "objectstorage_container_v1",
    "objectstorage_object_v1",
    "objectstorage_tempurl_v1",
    "orchestration_stack_v1",
    "provider",
    "sharedfilesystem_securityservice_v2",
    "sharedfilesystem_share_access_v2",
    "sharedfilesystem_share_v2",
    "sharedfilesystem_sharenetwork_v2",
    "vpnaas_endpoint_group_v2",
    "vpnaas_ike_policy_v2",
    "vpnaas_ipsec_policy_v2",
    "vpnaas_service_v2",
    "vpnaas_site_connection_v2",
]

publication.publish()

# Loading modules to ensure their types are registered with the jsii runtime library
from . import bgpvpn_network_associate_v2
from . import bgpvpn_port_associate_v2
from . import bgpvpn_router_associate_v2
from . import bgpvpn_v2
from . import blockstorage_qos_association_v3
from . import blockstorage_qos_v3
from . import blockstorage_quotaset_v3
from . import blockstorage_volume_attach_v3
from . import blockstorage_volume_type_access_v3
from . import blockstorage_volume_type_v3
from . import blockstorage_volume_v3
from . import compute_aggregate_v2
from . import compute_flavor_access_v2
from . import compute_flavor_v2
from . import compute_instance_v2
from . import compute_interface_attach_v2
from . import compute_keypair_v2
from . import compute_quotaset_v2
from . import compute_servergroup_v2
from . import compute_volume_attach_v2
from . import containerinfra_cluster_v1
from . import containerinfra_clustertemplate_v1
from . import containerinfra_nodegroup_v1
from . import data_openstack_blockstorage_availability_zones_v3
from . import data_openstack_blockstorage_quotaset_v3
from . import data_openstack_blockstorage_snapshot_v3
from . import data_openstack_blockstorage_volume_v3
from . import data_openstack_compute_aggregate_v2
from . import data_openstack_compute_availability_zones_v2
from . import data_openstack_compute_flavor_v2
from . import data_openstack_compute_hypervisor_v2
from . import data_openstack_compute_instance_v2
from . import data_openstack_compute_keypair_v2
from . import data_openstack_compute_limits_v2
from . import data_openstack_compute_quotaset_v2
from . import data_openstack_containerinfra_cluster_v1
from . import data_openstack_containerinfra_clustertemplate_v1
from . import data_openstack_containerinfra_nodegroup_v1
from . import data_openstack_dns_zone_v2
from . import data_openstack_fw_group_v2
from . import data_openstack_fw_policy_v2
from . import data_openstack_fw_rule_v2
from . import data_openstack_identity_auth_scope_v3
from . import data_openstack_identity_endpoint_v3
from . import data_openstack_identity_group_v3
from . import data_openstack_identity_project_ids_v3
from . import data_openstack_identity_project_v3
from . import data_openstack_identity_role_v3
from . import data_openstack_identity_service_v3
from . import data_openstack_identity_user_v3
from . import data_openstack_images_image_ids_v2
from . import data_openstack_images_image_v2
from . import data_openstack_keymanager_container_v1
from . import data_openstack_keymanager_secret_v1
from . import data_openstack_loadbalancer_flavor_v2
from . import data_openstack_networking_addressscope_v2
from . import data_openstack_networking_floatingip_v2
from . import data_openstack_networking_network_v2
from . import data_openstack_networking_port_ids_v2
from . import data_openstack_networking_port_v2
from . import data_openstack_networking_qos_bandwidth_limit_rule_v2
from . import data_openstack_networking_qos_dscp_marking_rule_v2
from . import data_openstack_networking_qos_minimum_bandwidth_rule_v2
from . import data_openstack_networking_qos_policy_v2
from . import data_openstack_networking_quota_v2
from . import data_openstack_networking_router_v2
from . import data_openstack_networking_secgroup_v2
from . import data_openstack_networking_subnet_ids_v2
from . import data_openstack_networking_subnet_v2
from . import data_openstack_networking_subnetpool_v2
from . import data_openstack_networking_trunk_v2
from . import data_openstack_sharedfilesystem_availability_zones_v2
from . import data_openstack_sharedfilesystem_share_v2
from . import data_openstack_sharedfilesystem_sharenetwork_v2
from . import data_openstack_sharedfilesystem_snapshot_v2
from . import db_configuration_v1
from . import db_database_v1
from . import db_instance_v1
from . import db_user_v1
from . import dns_recordset_v2
from . import dns_transfer_accept_v2
from . import dns_transfer_request_v2
from . import dns_zone_v2
from . import fw_group_v2
from . import fw_policy_v2
from . import fw_rule_v2
from . import identity_application_credential_v3
from . import identity_ec2_credential_v3
from . import identity_endpoint_v3
from . import identity_group_v3
from . import identity_inherit_role_assignment_v3
from . import identity_project_v3
from . import identity_role_assignment_v3
from . import identity_role_v3
from . import identity_service_v3
from . import identity_user_membership_v3
from . import identity_user_v3
from . import images_image_access_accept_v2
from . import images_image_access_v2
from . import images_image_v2
from . import keymanager_container_v1
from . import keymanager_order_v1
from . import keymanager_secret_v1
from . import lb_flavorprofile_v2
from . import lb_l7_policy_v2
from . import lb_l7_rule_v2
from . import lb_listener_v2
from . import lb_loadbalancer_v2
from . import lb_member_v2
from . import lb_members_v2
from . import lb_monitor_v2
from . import lb_pool_v2
from . import lb_quota_v2
from . import networking_addressscope_v2
from . import networking_floatingip_associate_v2
from . import networking_floatingip_v2
from . import networking_network_v2
from . import networking_port_secgroup_associate_v2
from . import networking_port_v2
from . import networking_portforwarding_v2
from . import networking_qos_bandwidth_limit_rule_v2
from . import networking_qos_dscp_marking_rule_v2
from . import networking_qos_minimum_bandwidth_rule_v2
from . import networking_qos_policy_v2
from . import networking_quota_v2
from . import networking_rbac_policy_v2
from . import networking_router_interface_v2
from . import networking_router_route_v2
from . import networking_router_v2
from . import networking_secgroup_rule_v2
from . import networking_secgroup_v2
from . import networking_subnet_route_v2
from . import networking_subnet_v2
from . import networking_subnetpool_v2
from . import networking_trunk_v2
from . import objectstorage_account_v1
from . import objectstorage_container_v1
from . import objectstorage_object_v1
from . import objectstorage_tempurl_v1
from . import orchestration_stack_v1
from . import provider
from . import sharedfilesystem_securityservice_v2
from . import sharedfilesystem_share_access_v2
from . import sharedfilesystem_share_v2
from . import sharedfilesystem_sharenetwork_v2
from . import vpnaas_endpoint_group_v2
from . import vpnaas_ike_policy_v2
from . import vpnaas_ipsec_policy_v2
from . import vpnaas_service_v2
from . import vpnaas_site_connection_v2
