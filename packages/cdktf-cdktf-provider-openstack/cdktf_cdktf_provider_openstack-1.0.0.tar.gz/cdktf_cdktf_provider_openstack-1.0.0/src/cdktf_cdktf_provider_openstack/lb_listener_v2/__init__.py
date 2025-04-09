r'''
# `openstack_lb_listener_v2`

Refer to the Terraform Registry for docs: [`openstack_lb_listener_v2`](https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/lb_listener_v2).
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

from .._jsii import *

import cdktf as _cdktf_9a9027ec
import constructs as _constructs_77d1e7e8


class LbListenerV2(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-openstack.lbListenerV2.LbListenerV2",
):
    '''Represents a {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/lb_listener_v2 openstack_lb_listener_v2}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        loadbalancer_id: builtins.str,
        protocol: builtins.str,
        protocol_port: jsii.Number,
        admin_state_up: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        allowed_cidrs: typing.Optional[typing.Sequence[builtins.str]] = None,
        alpn_protocols: typing.Optional[typing.Sequence[builtins.str]] = None,
        client_authentication: typing.Optional[builtins.str] = None,
        client_ca_tls_container_ref: typing.Optional[builtins.str] = None,
        client_crl_container_ref: typing.Optional[builtins.str] = None,
        connection_limit: typing.Optional[jsii.Number] = None,
        default_pool_id: typing.Optional[builtins.str] = None,
        default_tls_container_ref: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        hsts_include_subdomains: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        hsts_max_age: typing.Optional[jsii.Number] = None,
        hsts_preload: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        insert_headers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        sni_container_refs: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        tenant_id: typing.Optional[builtins.str] = None,
        timeout_client_data: typing.Optional[jsii.Number] = None,
        timeout_member_connect: typing.Optional[jsii.Number] = None,
        timeout_member_data: typing.Optional[jsii.Number] = None,
        timeouts: typing.Optional[typing.Union["LbListenerV2Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        timeout_tcp_inspect: typing.Optional[jsii.Number] = None,
        tls_ciphers: typing.Optional[builtins.str] = None,
        tls_versions: typing.Optional[typing.Sequence[builtins.str]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/lb_listener_v2 openstack_lb_listener_v2} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param loadbalancer_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/lb_listener_v2#loadbalancer_id LbListenerV2#loadbalancer_id}.
        :param protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/lb_listener_v2#protocol LbListenerV2#protocol}.
        :param protocol_port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/lb_listener_v2#protocol_port LbListenerV2#protocol_port}.
        :param admin_state_up: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/lb_listener_v2#admin_state_up LbListenerV2#admin_state_up}.
        :param allowed_cidrs: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/lb_listener_v2#allowed_cidrs LbListenerV2#allowed_cidrs}.
        :param alpn_protocols: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/lb_listener_v2#alpn_protocols LbListenerV2#alpn_protocols}.
        :param client_authentication: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/lb_listener_v2#client_authentication LbListenerV2#client_authentication}.
        :param client_ca_tls_container_ref: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/lb_listener_v2#client_ca_tls_container_ref LbListenerV2#client_ca_tls_container_ref}.
        :param client_crl_container_ref: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/lb_listener_v2#client_crl_container_ref LbListenerV2#client_crl_container_ref}.
        :param connection_limit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/lb_listener_v2#connection_limit LbListenerV2#connection_limit}.
        :param default_pool_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/lb_listener_v2#default_pool_id LbListenerV2#default_pool_id}.
        :param default_tls_container_ref: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/lb_listener_v2#default_tls_container_ref LbListenerV2#default_tls_container_ref}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/lb_listener_v2#description LbListenerV2#description}.
        :param hsts_include_subdomains: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/lb_listener_v2#hsts_include_subdomains LbListenerV2#hsts_include_subdomains}.
        :param hsts_max_age: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/lb_listener_v2#hsts_max_age LbListenerV2#hsts_max_age}.
        :param hsts_preload: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/lb_listener_v2#hsts_preload LbListenerV2#hsts_preload}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/lb_listener_v2#id LbListenerV2#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param insert_headers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/lb_listener_v2#insert_headers LbListenerV2#insert_headers}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/lb_listener_v2#name LbListenerV2#name}.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/lb_listener_v2#region LbListenerV2#region}.
        :param sni_container_refs: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/lb_listener_v2#sni_container_refs LbListenerV2#sni_container_refs}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/lb_listener_v2#tags LbListenerV2#tags}.
        :param tenant_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/lb_listener_v2#tenant_id LbListenerV2#tenant_id}.
        :param timeout_client_data: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/lb_listener_v2#timeout_client_data LbListenerV2#timeout_client_data}.
        :param timeout_member_connect: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/lb_listener_v2#timeout_member_connect LbListenerV2#timeout_member_connect}.
        :param timeout_member_data: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/lb_listener_v2#timeout_member_data LbListenerV2#timeout_member_data}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/lb_listener_v2#timeouts LbListenerV2#timeouts}
        :param timeout_tcp_inspect: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/lb_listener_v2#timeout_tcp_inspect LbListenerV2#timeout_tcp_inspect}.
        :param tls_ciphers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/lb_listener_v2#tls_ciphers LbListenerV2#tls_ciphers}.
        :param tls_versions: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/lb_listener_v2#tls_versions LbListenerV2#tls_versions}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2015d9c39d18d00647db96bc34c7f744b9d7a401e81f2a96b98bd60c3fd5e08)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = LbListenerV2Config(
            loadbalancer_id=loadbalancer_id,
            protocol=protocol,
            protocol_port=protocol_port,
            admin_state_up=admin_state_up,
            allowed_cidrs=allowed_cidrs,
            alpn_protocols=alpn_protocols,
            client_authentication=client_authentication,
            client_ca_tls_container_ref=client_ca_tls_container_ref,
            client_crl_container_ref=client_crl_container_ref,
            connection_limit=connection_limit,
            default_pool_id=default_pool_id,
            default_tls_container_ref=default_tls_container_ref,
            description=description,
            hsts_include_subdomains=hsts_include_subdomains,
            hsts_max_age=hsts_max_age,
            hsts_preload=hsts_preload,
            id=id,
            insert_headers=insert_headers,
            name=name,
            region=region,
            sni_container_refs=sni_container_refs,
            tags=tags,
            tenant_id=tenant_id,
            timeout_client_data=timeout_client_data,
            timeout_member_connect=timeout_member_connect,
            timeout_member_data=timeout_member_data,
            timeouts=timeouts,
            timeout_tcp_inspect=timeout_tcp_inspect,
            tls_ciphers=tls_ciphers,
            tls_versions=tls_versions,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a LbListenerV2 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the LbListenerV2 to import.
        :param import_from_id: The id of the existing LbListenerV2 that should be imported. Refer to the {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/lb_listener_v2#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the LbListenerV2 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbaeaa22e868988f652d9927ca9141e980eaebaa15e7076112fb7723bcc9a9f4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/lb_listener_v2#create LbListenerV2#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/lb_listener_v2#delete LbListenerV2#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/lb_listener_v2#update LbListenerV2#update}.
        '''
        value = LbListenerV2Timeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAdminStateUp")
    def reset_admin_state_up(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdminStateUp", []))

    @jsii.member(jsii_name="resetAllowedCidrs")
    def reset_allowed_cidrs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedCidrs", []))

    @jsii.member(jsii_name="resetAlpnProtocols")
    def reset_alpn_protocols(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAlpnProtocols", []))

    @jsii.member(jsii_name="resetClientAuthentication")
    def reset_client_authentication(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientAuthentication", []))

    @jsii.member(jsii_name="resetClientCaTlsContainerRef")
    def reset_client_ca_tls_container_ref(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientCaTlsContainerRef", []))

    @jsii.member(jsii_name="resetClientCrlContainerRef")
    def reset_client_crl_container_ref(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientCrlContainerRef", []))

    @jsii.member(jsii_name="resetConnectionLimit")
    def reset_connection_limit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConnectionLimit", []))

    @jsii.member(jsii_name="resetDefaultPoolId")
    def reset_default_pool_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultPoolId", []))

    @jsii.member(jsii_name="resetDefaultTlsContainerRef")
    def reset_default_tls_container_ref(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultTlsContainerRef", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetHstsIncludeSubdomains")
    def reset_hsts_include_subdomains(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHstsIncludeSubdomains", []))

    @jsii.member(jsii_name="resetHstsMaxAge")
    def reset_hsts_max_age(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHstsMaxAge", []))

    @jsii.member(jsii_name="resetHstsPreload")
    def reset_hsts_preload(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHstsPreload", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetInsertHeaders")
    def reset_insert_headers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInsertHeaders", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetSniContainerRefs")
    def reset_sni_container_refs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSniContainerRefs", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTenantId")
    def reset_tenant_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTenantId", []))

    @jsii.member(jsii_name="resetTimeoutClientData")
    def reset_timeout_client_data(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeoutClientData", []))

    @jsii.member(jsii_name="resetTimeoutMemberConnect")
    def reset_timeout_member_connect(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeoutMemberConnect", []))

    @jsii.member(jsii_name="resetTimeoutMemberData")
    def reset_timeout_member_data(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeoutMemberData", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetTimeoutTcpInspect")
    def reset_timeout_tcp_inspect(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeoutTcpInspect", []))

    @jsii.member(jsii_name="resetTlsCiphers")
    def reset_tls_ciphers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTlsCiphers", []))

    @jsii.member(jsii_name="resetTlsVersions")
    def reset_tls_versions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTlsVersions", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.member(jsii_name="synthesizeHclAttributes")
    def _synthesize_hcl_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeHclAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "LbListenerV2TimeoutsOutputReference":
        return typing.cast("LbListenerV2TimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="adminStateUpInput")
    def admin_state_up_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "adminStateUpInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedCidrsInput")
    def allowed_cidrs_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedCidrsInput"))

    @builtins.property
    @jsii.member(jsii_name="alpnProtocolsInput")
    def alpn_protocols_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "alpnProtocolsInput"))

    @builtins.property
    @jsii.member(jsii_name="clientAuthenticationInput")
    def client_authentication_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientAuthenticationInput"))

    @builtins.property
    @jsii.member(jsii_name="clientCaTlsContainerRefInput")
    def client_ca_tls_container_ref_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientCaTlsContainerRefInput"))

    @builtins.property
    @jsii.member(jsii_name="clientCrlContainerRefInput")
    def client_crl_container_ref_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientCrlContainerRefInput"))

    @builtins.property
    @jsii.member(jsii_name="connectionLimitInput")
    def connection_limit_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "connectionLimitInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultPoolIdInput")
    def default_pool_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultPoolIdInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultTlsContainerRefInput")
    def default_tls_container_ref_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultTlsContainerRefInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="hstsIncludeSubdomainsInput")
    def hsts_include_subdomains_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "hstsIncludeSubdomainsInput"))

    @builtins.property
    @jsii.member(jsii_name="hstsMaxAgeInput")
    def hsts_max_age_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "hstsMaxAgeInput"))

    @builtins.property
    @jsii.member(jsii_name="hstsPreloadInput")
    def hsts_preload_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "hstsPreloadInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="insertHeadersInput")
    def insert_headers_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "insertHeadersInput"))

    @builtins.property
    @jsii.member(jsii_name="loadbalancerIdInput")
    def loadbalancer_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "loadbalancerIdInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="protocolInput")
    def protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "protocolInput"))

    @builtins.property
    @jsii.member(jsii_name="protocolPortInput")
    def protocol_port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "protocolPortInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="sniContainerRefsInput")
    def sni_container_refs_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "sniContainerRefsInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="tenantIdInput")
    def tenant_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tenantIdInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutClientDataInput")
    def timeout_client_data_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "timeoutClientDataInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutMemberConnectInput")
    def timeout_member_connect_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "timeoutMemberConnectInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutMemberDataInput")
    def timeout_member_data_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "timeoutMemberDataInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "LbListenerV2Timeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "LbListenerV2Timeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutTcpInspectInput")
    def timeout_tcp_inspect_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "timeoutTcpInspectInput"))

    @builtins.property
    @jsii.member(jsii_name="tlsCiphersInput")
    def tls_ciphers_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tlsCiphersInput"))

    @builtins.property
    @jsii.member(jsii_name="tlsVersionsInput")
    def tls_versions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tlsVersionsInput"))

    @builtins.property
    @jsii.member(jsii_name="adminStateUp")
    def admin_state_up(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "adminStateUp"))

    @admin_state_up.setter
    def admin_state_up(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3357c36807e39f76e194a6bd102ac50fa33d3215603f5c3c06b82a5e744f37a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "adminStateUp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowedCidrs")
    def allowed_cidrs(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedCidrs"))

    @allowed_cidrs.setter
    def allowed_cidrs(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7076ecad77629271fc75e5691d8859a2e0a32af0a92e9ba818b1ed6a624880d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedCidrs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="alpnProtocols")
    def alpn_protocols(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "alpnProtocols"))

    @alpn_protocols.setter
    def alpn_protocols(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d249bcebc2f813c4bbe1bd055517d1291485c0f458eb4bdc3bc0f7086cfbf8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alpnProtocols", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientAuthentication")
    def client_authentication(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientAuthentication"))

    @client_authentication.setter
    def client_authentication(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7a0f1febe7de5465d55fb820796dd30e59253210e2186017fae5e8e94ad6d82)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientAuthentication", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientCaTlsContainerRef")
    def client_ca_tls_container_ref(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientCaTlsContainerRef"))

    @client_ca_tls_container_ref.setter
    def client_ca_tls_container_ref(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6918c6f4d03139517aea27d03b4d282157fee31d5230836191462b7b8bc6240)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientCaTlsContainerRef", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientCrlContainerRef")
    def client_crl_container_ref(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientCrlContainerRef"))

    @client_crl_container_ref.setter
    def client_crl_container_ref(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49b14acdc2757250fb5cfcaec01e9c58cf32f0b02e2275c308c1742a1c8cd124)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientCrlContainerRef", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="connectionLimit")
    def connection_limit(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "connectionLimit"))

    @connection_limit.setter
    def connection_limit(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40c56c974f77477ed622737ec4165aa48eb1b89186c042070695a58457460e18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectionLimit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultPoolId")
    def default_pool_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultPoolId"))

    @default_pool_id.setter
    def default_pool_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a9b014acf6b962fbf9227376c13c6efb8fe582b7783608737ed569e0e58f5cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultPoolId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultTlsContainerRef")
    def default_tls_container_ref(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultTlsContainerRef"))

    @default_tls_container_ref.setter
    def default_tls_container_ref(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2627a7956a4025d61f559eb9572e1876c74f396f8750f0e1e17a9de187b964be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultTlsContainerRef", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32ce64411d54d7d348478c249e73130ce60640040dddf858437f45f1486c4b7e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hstsIncludeSubdomains")
    def hsts_include_subdomains(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "hstsIncludeSubdomains"))

    @hsts_include_subdomains.setter
    def hsts_include_subdomains(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f95c7441567b72addd6adb389c443ee49143817b3eb7931adb3405c50ed3b98c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hstsIncludeSubdomains", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hstsMaxAge")
    def hsts_max_age(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "hstsMaxAge"))

    @hsts_max_age.setter
    def hsts_max_age(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b150f580f0bd36b7ad0ef7fb45f52e556ba11579628a24b07b35e2b3c6a8c56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hstsMaxAge", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hstsPreload")
    def hsts_preload(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "hstsPreload"))

    @hsts_preload.setter
    def hsts_preload(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac329043fde1405e84bfcf09766679c3c4217c55b9a5d049f44b575c9cd7c03b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hstsPreload", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fd620612f76c9613bd671ca2555d73ce94fb23f84a5ea25a56acd1ad84e6802)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="insertHeaders")
    def insert_headers(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "insertHeaders"))

    @insert_headers.setter
    def insert_headers(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a95e09a6c77f2114c869da89b25a203b2e43f27c6a06b4099e44f79e8a5ce430)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "insertHeaders", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="loadbalancerId")
    def loadbalancer_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "loadbalancerId"))

    @loadbalancer_id.setter
    def loadbalancer_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__037db11edfebf2579a066c56dce6242d7b95f1fa7d634eabef9528aa44482aea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loadbalancerId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15b06d7dcf2815825c540608b5631a9520c2cd4e8ee510fa6736eaa7ef828bb3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protocol"))

    @protocol.setter
    def protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d85ab1726aba67906ef34965381353d8448d3577c3e7a86cd03a684fce3bac23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="protocolPort")
    def protocol_port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "protocolPort"))

    @protocol_port.setter
    def protocol_port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b7db4e1b586e9d1b186e2cc42854aa275efd4b494347823c06f8bf966351399)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocolPort", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f4e7981c00e5481183cdbce7a2460e3186313d2fa6b0123390945435b057eb3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sniContainerRefs")
    def sni_container_refs(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "sniContainerRefs"))

    @sni_container_refs.setter
    def sni_container_refs(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0d1aecc3e30fef1564b00a33b703f9890441fac20662effbbc87a94b0312cbb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sniContainerRefs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfbab1504e6c74c4ff6e41c1b187b771a82587979b2f594d750a482d6f5c8ac7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tenantId")
    def tenant_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tenantId"))

    @tenant_id.setter
    def tenant_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e98c3ec518957e1b2a10e7588aed7580d17e81c1c4390cff921bcb607cd5c450)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tenantId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeoutClientData")
    def timeout_client_data(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "timeoutClientData"))

    @timeout_client_data.setter
    def timeout_client_data(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac03de4ed6ee775cb7f89c0cb73cbd857816d86af5aa114fc83596161cad528c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeoutClientData", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeoutMemberConnect")
    def timeout_member_connect(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "timeoutMemberConnect"))

    @timeout_member_connect.setter
    def timeout_member_connect(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d64662e86f38a6f7a7910cb51903c341c56141b24169d55616a6f4959559dc14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeoutMemberConnect", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeoutMemberData")
    def timeout_member_data(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "timeoutMemberData"))

    @timeout_member_data.setter
    def timeout_member_data(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4fc0ceb9a9f3e00c84b5519155e19c9f7b59f750d7aef40db11bc3e3963abfb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeoutMemberData", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeoutTcpInspect")
    def timeout_tcp_inspect(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "timeoutTcpInspect"))

    @timeout_tcp_inspect.setter
    def timeout_tcp_inspect(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b068e08db5dbbde6492c609000d3600a9c67a325255198040725b6f8471e85b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeoutTcpInspect", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tlsCiphers")
    def tls_ciphers(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tlsCiphers"))

    @tls_ciphers.setter
    def tls_ciphers(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5cfd7789d1a7d02bd307c03cf265152bf0a8876ce76fe621da6ecc3ecb746d01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tlsCiphers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tlsVersions")
    def tls_versions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tlsVersions"))

    @tls_versions.setter
    def tls_versions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d04877696586298d2f94a032f2087adc38c68f2dacfdc86fee93b07cb81c908)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tlsVersions", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-openstack.lbListenerV2.LbListenerV2Config",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "loadbalancer_id": "loadbalancerId",
        "protocol": "protocol",
        "protocol_port": "protocolPort",
        "admin_state_up": "adminStateUp",
        "allowed_cidrs": "allowedCidrs",
        "alpn_protocols": "alpnProtocols",
        "client_authentication": "clientAuthentication",
        "client_ca_tls_container_ref": "clientCaTlsContainerRef",
        "client_crl_container_ref": "clientCrlContainerRef",
        "connection_limit": "connectionLimit",
        "default_pool_id": "defaultPoolId",
        "default_tls_container_ref": "defaultTlsContainerRef",
        "description": "description",
        "hsts_include_subdomains": "hstsIncludeSubdomains",
        "hsts_max_age": "hstsMaxAge",
        "hsts_preload": "hstsPreload",
        "id": "id",
        "insert_headers": "insertHeaders",
        "name": "name",
        "region": "region",
        "sni_container_refs": "sniContainerRefs",
        "tags": "tags",
        "tenant_id": "tenantId",
        "timeout_client_data": "timeoutClientData",
        "timeout_member_connect": "timeoutMemberConnect",
        "timeout_member_data": "timeoutMemberData",
        "timeouts": "timeouts",
        "timeout_tcp_inspect": "timeoutTcpInspect",
        "tls_ciphers": "tlsCiphers",
        "tls_versions": "tlsVersions",
    },
)
class LbListenerV2Config(_cdktf_9a9027ec.TerraformMetaArguments):
    def __init__(
        self,
        *,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
        loadbalancer_id: builtins.str,
        protocol: builtins.str,
        protocol_port: jsii.Number,
        admin_state_up: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        allowed_cidrs: typing.Optional[typing.Sequence[builtins.str]] = None,
        alpn_protocols: typing.Optional[typing.Sequence[builtins.str]] = None,
        client_authentication: typing.Optional[builtins.str] = None,
        client_ca_tls_container_ref: typing.Optional[builtins.str] = None,
        client_crl_container_ref: typing.Optional[builtins.str] = None,
        connection_limit: typing.Optional[jsii.Number] = None,
        default_pool_id: typing.Optional[builtins.str] = None,
        default_tls_container_ref: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        hsts_include_subdomains: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        hsts_max_age: typing.Optional[jsii.Number] = None,
        hsts_preload: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        insert_headers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        sni_container_refs: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        tenant_id: typing.Optional[builtins.str] = None,
        timeout_client_data: typing.Optional[jsii.Number] = None,
        timeout_member_connect: typing.Optional[jsii.Number] = None,
        timeout_member_data: typing.Optional[jsii.Number] = None,
        timeouts: typing.Optional[typing.Union["LbListenerV2Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        timeout_tcp_inspect: typing.Optional[jsii.Number] = None,
        tls_ciphers: typing.Optional[builtins.str] = None,
        tls_versions: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param loadbalancer_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/lb_listener_v2#loadbalancer_id LbListenerV2#loadbalancer_id}.
        :param protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/lb_listener_v2#protocol LbListenerV2#protocol}.
        :param protocol_port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/lb_listener_v2#protocol_port LbListenerV2#protocol_port}.
        :param admin_state_up: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/lb_listener_v2#admin_state_up LbListenerV2#admin_state_up}.
        :param allowed_cidrs: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/lb_listener_v2#allowed_cidrs LbListenerV2#allowed_cidrs}.
        :param alpn_protocols: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/lb_listener_v2#alpn_protocols LbListenerV2#alpn_protocols}.
        :param client_authentication: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/lb_listener_v2#client_authentication LbListenerV2#client_authentication}.
        :param client_ca_tls_container_ref: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/lb_listener_v2#client_ca_tls_container_ref LbListenerV2#client_ca_tls_container_ref}.
        :param client_crl_container_ref: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/lb_listener_v2#client_crl_container_ref LbListenerV2#client_crl_container_ref}.
        :param connection_limit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/lb_listener_v2#connection_limit LbListenerV2#connection_limit}.
        :param default_pool_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/lb_listener_v2#default_pool_id LbListenerV2#default_pool_id}.
        :param default_tls_container_ref: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/lb_listener_v2#default_tls_container_ref LbListenerV2#default_tls_container_ref}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/lb_listener_v2#description LbListenerV2#description}.
        :param hsts_include_subdomains: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/lb_listener_v2#hsts_include_subdomains LbListenerV2#hsts_include_subdomains}.
        :param hsts_max_age: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/lb_listener_v2#hsts_max_age LbListenerV2#hsts_max_age}.
        :param hsts_preload: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/lb_listener_v2#hsts_preload LbListenerV2#hsts_preload}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/lb_listener_v2#id LbListenerV2#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param insert_headers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/lb_listener_v2#insert_headers LbListenerV2#insert_headers}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/lb_listener_v2#name LbListenerV2#name}.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/lb_listener_v2#region LbListenerV2#region}.
        :param sni_container_refs: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/lb_listener_v2#sni_container_refs LbListenerV2#sni_container_refs}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/lb_listener_v2#tags LbListenerV2#tags}.
        :param tenant_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/lb_listener_v2#tenant_id LbListenerV2#tenant_id}.
        :param timeout_client_data: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/lb_listener_v2#timeout_client_data LbListenerV2#timeout_client_data}.
        :param timeout_member_connect: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/lb_listener_v2#timeout_member_connect LbListenerV2#timeout_member_connect}.
        :param timeout_member_data: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/lb_listener_v2#timeout_member_data LbListenerV2#timeout_member_data}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/lb_listener_v2#timeouts LbListenerV2#timeouts}
        :param timeout_tcp_inspect: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/lb_listener_v2#timeout_tcp_inspect LbListenerV2#timeout_tcp_inspect}.
        :param tls_ciphers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/lb_listener_v2#tls_ciphers LbListenerV2#tls_ciphers}.
        :param tls_versions: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/lb_listener_v2#tls_versions LbListenerV2#tls_versions}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = LbListenerV2Timeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa56d4c6daf87357033ca83d82378255c44e0a4b367bc09f2c96a568a8dead90)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument loadbalancer_id", value=loadbalancer_id, expected_type=type_hints["loadbalancer_id"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            check_type(argname="argument protocol_port", value=protocol_port, expected_type=type_hints["protocol_port"])
            check_type(argname="argument admin_state_up", value=admin_state_up, expected_type=type_hints["admin_state_up"])
            check_type(argname="argument allowed_cidrs", value=allowed_cidrs, expected_type=type_hints["allowed_cidrs"])
            check_type(argname="argument alpn_protocols", value=alpn_protocols, expected_type=type_hints["alpn_protocols"])
            check_type(argname="argument client_authentication", value=client_authentication, expected_type=type_hints["client_authentication"])
            check_type(argname="argument client_ca_tls_container_ref", value=client_ca_tls_container_ref, expected_type=type_hints["client_ca_tls_container_ref"])
            check_type(argname="argument client_crl_container_ref", value=client_crl_container_ref, expected_type=type_hints["client_crl_container_ref"])
            check_type(argname="argument connection_limit", value=connection_limit, expected_type=type_hints["connection_limit"])
            check_type(argname="argument default_pool_id", value=default_pool_id, expected_type=type_hints["default_pool_id"])
            check_type(argname="argument default_tls_container_ref", value=default_tls_container_ref, expected_type=type_hints["default_tls_container_ref"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument hsts_include_subdomains", value=hsts_include_subdomains, expected_type=type_hints["hsts_include_subdomains"])
            check_type(argname="argument hsts_max_age", value=hsts_max_age, expected_type=type_hints["hsts_max_age"])
            check_type(argname="argument hsts_preload", value=hsts_preload, expected_type=type_hints["hsts_preload"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument insert_headers", value=insert_headers, expected_type=type_hints["insert_headers"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument sni_container_refs", value=sni_container_refs, expected_type=type_hints["sni_container_refs"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tenant_id", value=tenant_id, expected_type=type_hints["tenant_id"])
            check_type(argname="argument timeout_client_data", value=timeout_client_data, expected_type=type_hints["timeout_client_data"])
            check_type(argname="argument timeout_member_connect", value=timeout_member_connect, expected_type=type_hints["timeout_member_connect"])
            check_type(argname="argument timeout_member_data", value=timeout_member_data, expected_type=type_hints["timeout_member_data"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument timeout_tcp_inspect", value=timeout_tcp_inspect, expected_type=type_hints["timeout_tcp_inspect"])
            check_type(argname="argument tls_ciphers", value=tls_ciphers, expected_type=type_hints["tls_ciphers"])
            check_type(argname="argument tls_versions", value=tls_versions, expected_type=type_hints["tls_versions"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "loadbalancer_id": loadbalancer_id,
            "protocol": protocol,
            "protocol_port": protocol_port,
        }
        if connection is not None:
            self._values["connection"] = connection
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if for_each is not None:
            self._values["for_each"] = for_each
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if provisioners is not None:
            self._values["provisioners"] = provisioners
        if admin_state_up is not None:
            self._values["admin_state_up"] = admin_state_up
        if allowed_cidrs is not None:
            self._values["allowed_cidrs"] = allowed_cidrs
        if alpn_protocols is not None:
            self._values["alpn_protocols"] = alpn_protocols
        if client_authentication is not None:
            self._values["client_authentication"] = client_authentication
        if client_ca_tls_container_ref is not None:
            self._values["client_ca_tls_container_ref"] = client_ca_tls_container_ref
        if client_crl_container_ref is not None:
            self._values["client_crl_container_ref"] = client_crl_container_ref
        if connection_limit is not None:
            self._values["connection_limit"] = connection_limit
        if default_pool_id is not None:
            self._values["default_pool_id"] = default_pool_id
        if default_tls_container_ref is not None:
            self._values["default_tls_container_ref"] = default_tls_container_ref
        if description is not None:
            self._values["description"] = description
        if hsts_include_subdomains is not None:
            self._values["hsts_include_subdomains"] = hsts_include_subdomains
        if hsts_max_age is not None:
            self._values["hsts_max_age"] = hsts_max_age
        if hsts_preload is not None:
            self._values["hsts_preload"] = hsts_preload
        if id is not None:
            self._values["id"] = id
        if insert_headers is not None:
            self._values["insert_headers"] = insert_headers
        if name is not None:
            self._values["name"] = name
        if region is not None:
            self._values["region"] = region
        if sni_container_refs is not None:
            self._values["sni_container_refs"] = sni_container_refs
        if tags is not None:
            self._values["tags"] = tags
        if tenant_id is not None:
            self._values["tenant_id"] = tenant_id
        if timeout_client_data is not None:
            self._values["timeout_client_data"] = timeout_client_data
        if timeout_member_connect is not None:
            self._values["timeout_member_connect"] = timeout_member_connect
        if timeout_member_data is not None:
            self._values["timeout_member_data"] = timeout_member_data
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if timeout_tcp_inspect is not None:
            self._values["timeout_tcp_inspect"] = timeout_tcp_inspect
        if tls_ciphers is not None:
            self._values["tls_ciphers"] = tls_ciphers
        if tls_versions is not None:
            self._values["tls_versions"] = tls_versions

    @builtins.property
    def connection(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("connection")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]], result)

    @builtins.property
    def count(
        self,
    ) -> typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]], result)

    @builtins.property
    def depends_on(
        self,
    ) -> typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]], result)

    @builtins.property
    def for_each(self) -> typing.Optional[_cdktf_9a9027ec.ITerraformIterator]:
        '''
        :stability: experimental
        '''
        result = self._values.get("for_each")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.ITerraformIterator], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[_cdktf_9a9027ec.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformProvider], result)

    @builtins.property
    def provisioners(
        self,
    ) -> typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provisioners")
        return typing.cast(typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]], result)

    @builtins.property
    def loadbalancer_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/lb_listener_v2#loadbalancer_id LbListenerV2#loadbalancer_id}.'''
        result = self._values.get("loadbalancer_id")
        assert result is not None, "Required property 'loadbalancer_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def protocol(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/lb_listener_v2#protocol LbListenerV2#protocol}.'''
        result = self._values.get("protocol")
        assert result is not None, "Required property 'protocol' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def protocol_port(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/lb_listener_v2#protocol_port LbListenerV2#protocol_port}.'''
        result = self._values.get("protocol_port")
        assert result is not None, "Required property 'protocol_port' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def admin_state_up(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/lb_listener_v2#admin_state_up LbListenerV2#admin_state_up}.'''
        result = self._values.get("admin_state_up")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def allowed_cidrs(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/lb_listener_v2#allowed_cidrs LbListenerV2#allowed_cidrs}.'''
        result = self._values.get("allowed_cidrs")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def alpn_protocols(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/lb_listener_v2#alpn_protocols LbListenerV2#alpn_protocols}.'''
        result = self._values.get("alpn_protocols")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def client_authentication(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/lb_listener_v2#client_authentication LbListenerV2#client_authentication}.'''
        result = self._values.get("client_authentication")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_ca_tls_container_ref(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/lb_listener_v2#client_ca_tls_container_ref LbListenerV2#client_ca_tls_container_ref}.'''
        result = self._values.get("client_ca_tls_container_ref")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_crl_container_ref(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/lb_listener_v2#client_crl_container_ref LbListenerV2#client_crl_container_ref}.'''
        result = self._values.get("client_crl_container_ref")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def connection_limit(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/lb_listener_v2#connection_limit LbListenerV2#connection_limit}.'''
        result = self._values.get("connection_limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def default_pool_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/lb_listener_v2#default_pool_id LbListenerV2#default_pool_id}.'''
        result = self._values.get("default_pool_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_tls_container_ref(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/lb_listener_v2#default_tls_container_ref LbListenerV2#default_tls_container_ref}.'''
        result = self._values.get("default_tls_container_ref")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/lb_listener_v2#description LbListenerV2#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def hsts_include_subdomains(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/lb_listener_v2#hsts_include_subdomains LbListenerV2#hsts_include_subdomains}.'''
        result = self._values.get("hsts_include_subdomains")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def hsts_max_age(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/lb_listener_v2#hsts_max_age LbListenerV2#hsts_max_age}.'''
        result = self._values.get("hsts_max_age")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def hsts_preload(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/lb_listener_v2#hsts_preload LbListenerV2#hsts_preload}.'''
        result = self._values.get("hsts_preload")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/lb_listener_v2#id LbListenerV2#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def insert_headers(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/lb_listener_v2#insert_headers LbListenerV2#insert_headers}.'''
        result = self._values.get("insert_headers")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/lb_listener_v2#name LbListenerV2#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/lb_listener_v2#region LbListenerV2#region}.'''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sni_container_refs(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/lb_listener_v2#sni_container_refs LbListenerV2#sni_container_refs}.'''
        result = self._values.get("sni_container_refs")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/lb_listener_v2#tags LbListenerV2#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tenant_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/lb_listener_v2#tenant_id LbListenerV2#tenant_id}.'''
        result = self._values.get("tenant_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeout_client_data(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/lb_listener_v2#timeout_client_data LbListenerV2#timeout_client_data}.'''
        result = self._values.get("timeout_client_data")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def timeout_member_connect(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/lb_listener_v2#timeout_member_connect LbListenerV2#timeout_member_connect}.'''
        result = self._values.get("timeout_member_connect")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def timeout_member_data(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/lb_listener_v2#timeout_member_data LbListenerV2#timeout_member_data}.'''
        result = self._values.get("timeout_member_data")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["LbListenerV2Timeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/lb_listener_v2#timeouts LbListenerV2#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["LbListenerV2Timeouts"], result)

    @builtins.property
    def timeout_tcp_inspect(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/lb_listener_v2#timeout_tcp_inspect LbListenerV2#timeout_tcp_inspect}.'''
        result = self._values.get("timeout_tcp_inspect")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tls_ciphers(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/lb_listener_v2#tls_ciphers LbListenerV2#tls_ciphers}.'''
        result = self._values.get("tls_ciphers")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tls_versions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/lb_listener_v2#tls_versions LbListenerV2#tls_versions}.'''
        result = self._values.get("tls_versions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LbListenerV2Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-openstack.lbListenerV2.LbListenerV2Timeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class LbListenerV2Timeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/lb_listener_v2#create LbListenerV2#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/lb_listener_v2#delete LbListenerV2#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/lb_listener_v2#update LbListenerV2#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3155079b198102d4e94865f79b471611ad34537c780801afa2b22c4811544812)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/lb_listener_v2#create LbListenerV2#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/lb_listener_v2#delete LbListenerV2#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/lb_listener_v2#update LbListenerV2#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LbListenerV2Timeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LbListenerV2TimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-openstack.lbListenerV2.LbListenerV2TimeoutsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2165452a5a36ad843998c8dcbac4df17cdabbaa8548a000cbe1d7216ae931a7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @jsii.member(jsii_name="resetUpdate")
    def reset_update(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpdate", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteInput")
    def delete_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteInput"))

    @builtins.property
    @jsii.member(jsii_name="updateInput")
    def update_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "updateInput"))

    @builtins.property
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc07223283800623558633c2cb45a67074ba12c7a69a7eb4e8101ab045f889e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a73735e566fef92e4d8e722405d1c88764f44641dc0b9470b4bf54c1a662134b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c30063c6ed95d12751ae0cfe368c0bd5c0a649ceeba7533b1096305bb1e1999e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LbListenerV2Timeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LbListenerV2Timeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LbListenerV2Timeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0026cb84348d0a4b5cca1a6baa192d115783475f51d53f3bb4fc2d35a0879894)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "LbListenerV2",
    "LbListenerV2Config",
    "LbListenerV2Timeouts",
    "LbListenerV2TimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__c2015d9c39d18d00647db96bc34c7f744b9d7a401e81f2a96b98bd60c3fd5e08(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    loadbalancer_id: builtins.str,
    protocol: builtins.str,
    protocol_port: jsii.Number,
    admin_state_up: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    allowed_cidrs: typing.Optional[typing.Sequence[builtins.str]] = None,
    alpn_protocols: typing.Optional[typing.Sequence[builtins.str]] = None,
    client_authentication: typing.Optional[builtins.str] = None,
    client_ca_tls_container_ref: typing.Optional[builtins.str] = None,
    client_crl_container_ref: typing.Optional[builtins.str] = None,
    connection_limit: typing.Optional[jsii.Number] = None,
    default_pool_id: typing.Optional[builtins.str] = None,
    default_tls_container_ref: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    hsts_include_subdomains: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    hsts_max_age: typing.Optional[jsii.Number] = None,
    hsts_preload: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    insert_headers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    sni_container_refs: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    tenant_id: typing.Optional[builtins.str] = None,
    timeout_client_data: typing.Optional[jsii.Number] = None,
    timeout_member_connect: typing.Optional[jsii.Number] = None,
    timeout_member_data: typing.Optional[jsii.Number] = None,
    timeouts: typing.Optional[typing.Union[LbListenerV2Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    timeout_tcp_inspect: typing.Optional[jsii.Number] = None,
    tls_ciphers: typing.Optional[builtins.str] = None,
    tls_versions: typing.Optional[typing.Sequence[builtins.str]] = None,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbaeaa22e868988f652d9927ca9141e980eaebaa15e7076112fb7723bcc9a9f4(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3357c36807e39f76e194a6bd102ac50fa33d3215603f5c3c06b82a5e744f37a9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7076ecad77629271fc75e5691d8859a2e0a32af0a92e9ba818b1ed6a624880d9(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d249bcebc2f813c4bbe1bd055517d1291485c0f458eb4bdc3bc0f7086cfbf8c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7a0f1febe7de5465d55fb820796dd30e59253210e2186017fae5e8e94ad6d82(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6918c6f4d03139517aea27d03b4d282157fee31d5230836191462b7b8bc6240(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49b14acdc2757250fb5cfcaec01e9c58cf32f0b02e2275c308c1742a1c8cd124(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40c56c974f77477ed622737ec4165aa48eb1b89186c042070695a58457460e18(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a9b014acf6b962fbf9227376c13c6efb8fe582b7783608737ed569e0e58f5cf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2627a7956a4025d61f559eb9572e1876c74f396f8750f0e1e17a9de187b964be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32ce64411d54d7d348478c249e73130ce60640040dddf858437f45f1486c4b7e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f95c7441567b72addd6adb389c443ee49143817b3eb7931adb3405c50ed3b98c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b150f580f0bd36b7ad0ef7fb45f52e556ba11579628a24b07b35e2b3c6a8c56(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac329043fde1405e84bfcf09766679c3c4217c55b9a5d049f44b575c9cd7c03b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fd620612f76c9613bd671ca2555d73ce94fb23f84a5ea25a56acd1ad84e6802(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a95e09a6c77f2114c869da89b25a203b2e43f27c6a06b4099e44f79e8a5ce430(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__037db11edfebf2579a066c56dce6242d7b95f1fa7d634eabef9528aa44482aea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15b06d7dcf2815825c540608b5631a9520c2cd4e8ee510fa6736eaa7ef828bb3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d85ab1726aba67906ef34965381353d8448d3577c3e7a86cd03a684fce3bac23(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b7db4e1b586e9d1b186e2cc42854aa275efd4b494347823c06f8bf966351399(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f4e7981c00e5481183cdbce7a2460e3186313d2fa6b0123390945435b057eb3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0d1aecc3e30fef1564b00a33b703f9890441fac20662effbbc87a94b0312cbb(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfbab1504e6c74c4ff6e41c1b187b771a82587979b2f594d750a482d6f5c8ac7(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e98c3ec518957e1b2a10e7588aed7580d17e81c1c4390cff921bcb607cd5c450(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac03de4ed6ee775cb7f89c0cb73cbd857816d86af5aa114fc83596161cad528c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d64662e86f38a6f7a7910cb51903c341c56141b24169d55616a6f4959559dc14(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4fc0ceb9a9f3e00c84b5519155e19c9f7b59f750d7aef40db11bc3e3963abfb(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b068e08db5dbbde6492c609000d3600a9c67a325255198040725b6f8471e85b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cfd7789d1a7d02bd307c03cf265152bf0a8876ce76fe621da6ecc3ecb746d01(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d04877696586298d2f94a032f2087adc38c68f2dacfdc86fee93b07cb81c908(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa56d4c6daf87357033ca83d82378255c44e0a4b367bc09f2c96a568a8dead90(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    loadbalancer_id: builtins.str,
    protocol: builtins.str,
    protocol_port: jsii.Number,
    admin_state_up: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    allowed_cidrs: typing.Optional[typing.Sequence[builtins.str]] = None,
    alpn_protocols: typing.Optional[typing.Sequence[builtins.str]] = None,
    client_authentication: typing.Optional[builtins.str] = None,
    client_ca_tls_container_ref: typing.Optional[builtins.str] = None,
    client_crl_container_ref: typing.Optional[builtins.str] = None,
    connection_limit: typing.Optional[jsii.Number] = None,
    default_pool_id: typing.Optional[builtins.str] = None,
    default_tls_container_ref: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    hsts_include_subdomains: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    hsts_max_age: typing.Optional[jsii.Number] = None,
    hsts_preload: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    insert_headers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    sni_container_refs: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    tenant_id: typing.Optional[builtins.str] = None,
    timeout_client_data: typing.Optional[jsii.Number] = None,
    timeout_member_connect: typing.Optional[jsii.Number] = None,
    timeout_member_data: typing.Optional[jsii.Number] = None,
    timeouts: typing.Optional[typing.Union[LbListenerV2Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    timeout_tcp_inspect: typing.Optional[jsii.Number] = None,
    tls_ciphers: typing.Optional[builtins.str] = None,
    tls_versions: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3155079b198102d4e94865f79b471611ad34537c780801afa2b22c4811544812(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2165452a5a36ad843998c8dcbac4df17cdabbaa8548a000cbe1d7216ae931a7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc07223283800623558633c2cb45a67074ba12c7a69a7eb4e8101ab045f889e0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a73735e566fef92e4d8e722405d1c88764f44641dc0b9470b4bf54c1a662134b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c30063c6ed95d12751ae0cfe368c0bd5c0a649ceeba7533b1096305bb1e1999e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0026cb84348d0a4b5cca1a6baa192d115783475f51d53f3bb4fc2d35a0879894(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LbListenerV2Timeouts]],
) -> None:
    """Type checking stubs"""
    pass
