r'''
# `provider`

Refer to the Terraform Registry for docs: [`openstack`](https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs).
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


class OpenstackProvider(
    _cdktf_9a9027ec.TerraformProvider,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-openstack.provider.OpenstackProvider",
):
    '''Represents a {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs openstack}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        alias: typing.Optional[builtins.str] = None,
        allow_reauth: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        application_credential_id: typing.Optional[builtins.str] = None,
        application_credential_name: typing.Optional[builtins.str] = None,
        application_credential_secret: typing.Optional[builtins.str] = None,
        auth_url: typing.Optional[builtins.str] = None,
        cacert_file: typing.Optional[builtins.str] = None,
        cert: typing.Optional[builtins.str] = None,
        cloud: typing.Optional[builtins.str] = None,
        default_domain: typing.Optional[builtins.str] = None,
        delayed_auth: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        disable_no_cache_header: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        domain_id: typing.Optional[builtins.str] = None,
        domain_name: typing.Optional[builtins.str] = None,
        enable_logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        endpoint_overrides: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        endpoint_type: typing.Optional[builtins.str] = None,
        insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        key: typing.Optional[builtins.str] = None,
        max_retries: typing.Optional[jsii.Number] = None,
        password: typing.Optional[builtins.str] = None,
        project_domain_id: typing.Optional[builtins.str] = None,
        project_domain_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        swauth: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        system_scope: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tenant_id: typing.Optional[builtins.str] = None,
        tenant_name: typing.Optional[builtins.str] = None,
        token: typing.Optional[builtins.str] = None,
        user_domain_id: typing.Optional[builtins.str] = None,
        user_domain_name: typing.Optional[builtins.str] = None,
        user_id: typing.Optional[builtins.str] = None,
        user_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs openstack} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param alias: Alias name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs#alias OpenstackProvider#alias}
        :param allow_reauth: If set to ``false``, OpenStack authorization won't be perfomed automatically, if the initial auth token get expired. Defaults to ``true``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs#allow_reauth OpenstackProvider#allow_reauth}
        :param application_credential_id: Application Credential ID to login with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs#application_credential_id OpenstackProvider#application_credential_id}
        :param application_credential_name: Application Credential name to login with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs#application_credential_name OpenstackProvider#application_credential_name}
        :param application_credential_secret: Application Credential secret to login with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs#application_credential_secret OpenstackProvider#application_credential_secret}
        :param auth_url: The Identity authentication URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs#auth_url OpenstackProvider#auth_url}
        :param cacert_file: A Custom CA certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs#cacert_file OpenstackProvider#cacert_file}
        :param cert: A client certificate to authenticate with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs#cert OpenstackProvider#cert}
        :param cloud: An entry in a ``clouds.yaml`` file to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs#cloud OpenstackProvider#cloud}
        :param default_domain: The name of the Domain ID to scope to if no other domain is specified. Defaults to ``default`` (Identity v3). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs#default_domain OpenstackProvider#default_domain}
        :param delayed_auth: If set to ``false``, OpenStack authorization will be perfomed, every time the service provider client is called. Defaults to ``true``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs#delayed_auth OpenstackProvider#delayed_auth}
        :param disable_no_cache_header: If set to ``true``, the HTTP ``Cache-Control: no-cache`` header will not be added by default to all API requests. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs#disable_no_cache_header OpenstackProvider#disable_no_cache_header}
        :param domain_id: The ID of the Domain to scope to (Identity v3). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs#domain_id OpenstackProvider#domain_id}
        :param domain_name: The name of the Domain to scope to (Identity v3). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs#domain_name OpenstackProvider#domain_name}
        :param enable_logging: Outputs very verbose logs with all calls made to and responses from OpenStack. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs#enable_logging OpenstackProvider#enable_logging}
        :param endpoint_overrides: A map of services with an endpoint to override what was from the Keystone catalog. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs#endpoint_overrides OpenstackProvider#endpoint_overrides}
        :param endpoint_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs#endpoint_type OpenstackProvider#endpoint_type}.
        :param insecure: Trust self-signed certificates. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs#insecure OpenstackProvider#insecure}
        :param key: A client private key to authenticate with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs#key OpenstackProvider#key}
        :param max_retries: How many times HTTP connection should be retried until giving up. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs#max_retries OpenstackProvider#max_retries}
        :param password: Password to login with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs#password OpenstackProvider#password}
        :param project_domain_id: The ID of the domain where the proejct resides (Identity v3). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs#project_domain_id OpenstackProvider#project_domain_id}
        :param project_domain_name: The name of the domain where the project resides (Identity v3). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs#project_domain_name OpenstackProvider#project_domain_name}
        :param region: The OpenStack region to connect to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs#region OpenstackProvider#region}
        :param swauth: Use Swift's authentication system instead of Keystone. Only used for interaction with Swift. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs#swauth OpenstackProvider#swauth}
        :param system_scope: If set to ``true``, system scoped authorization will be enabled. Defaults to ``false`` (Identity v3). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs#system_scope OpenstackProvider#system_scope}
        :param tenant_id: The ID of the Tenant (Identity v2) or Project (Identity v3) to login with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs#tenant_id OpenstackProvider#tenant_id}
        :param tenant_name: The name of the Tenant (Identity v2) or Project (Identity v3) to login with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs#tenant_name OpenstackProvider#tenant_name}
        :param token: Authentication token to use as an alternative to username/password. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs#token OpenstackProvider#token}
        :param user_domain_id: The ID of the domain where the user resides (Identity v3). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs#user_domain_id OpenstackProvider#user_domain_id}
        :param user_domain_name: The name of the domain where the user resides (Identity v3). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs#user_domain_name OpenstackProvider#user_domain_name}
        :param user_id: User ID to login with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs#user_id OpenstackProvider#user_id}
        :param user_name: Username to login with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs#user_name OpenstackProvider#user_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c296a0a70f54038ecc9d9471b2283c854a31f9368ad483babb40f8e1902b6b0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = OpenstackProviderConfig(
            alias=alias,
            allow_reauth=allow_reauth,
            application_credential_id=application_credential_id,
            application_credential_name=application_credential_name,
            application_credential_secret=application_credential_secret,
            auth_url=auth_url,
            cacert_file=cacert_file,
            cert=cert,
            cloud=cloud,
            default_domain=default_domain,
            delayed_auth=delayed_auth,
            disable_no_cache_header=disable_no_cache_header,
            domain_id=domain_id,
            domain_name=domain_name,
            enable_logging=enable_logging,
            endpoint_overrides=endpoint_overrides,
            endpoint_type=endpoint_type,
            insecure=insecure,
            key=key,
            max_retries=max_retries,
            password=password,
            project_domain_id=project_domain_id,
            project_domain_name=project_domain_name,
            region=region,
            swauth=swauth,
            system_scope=system_scope,
            tenant_id=tenant_id,
            tenant_name=tenant_name,
            token=token,
            user_domain_id=user_domain_id,
            user_domain_name=user_domain_name,
            user_id=user_id,
            user_name=user_name,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a OpenstackProvider resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the OpenstackProvider to import.
        :param import_from_id: The id of the existing OpenstackProvider that should be imported. Refer to the {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the OpenstackProvider to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf3eba471d77d385753a3c9cd685356e187d818489c92d41b3a185affc7c4cd4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetAlias")
    def reset_alias(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAlias", []))

    @jsii.member(jsii_name="resetAllowReauth")
    def reset_allow_reauth(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowReauth", []))

    @jsii.member(jsii_name="resetApplicationCredentialId")
    def reset_application_credential_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApplicationCredentialId", []))

    @jsii.member(jsii_name="resetApplicationCredentialName")
    def reset_application_credential_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApplicationCredentialName", []))

    @jsii.member(jsii_name="resetApplicationCredentialSecret")
    def reset_application_credential_secret(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApplicationCredentialSecret", []))

    @jsii.member(jsii_name="resetAuthUrl")
    def reset_auth_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthUrl", []))

    @jsii.member(jsii_name="resetCacertFile")
    def reset_cacert_file(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCacertFile", []))

    @jsii.member(jsii_name="resetCert")
    def reset_cert(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCert", []))

    @jsii.member(jsii_name="resetCloud")
    def reset_cloud(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloud", []))

    @jsii.member(jsii_name="resetDefaultDomain")
    def reset_default_domain(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultDomain", []))

    @jsii.member(jsii_name="resetDelayedAuth")
    def reset_delayed_auth(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelayedAuth", []))

    @jsii.member(jsii_name="resetDisableNoCacheHeader")
    def reset_disable_no_cache_header(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisableNoCacheHeader", []))

    @jsii.member(jsii_name="resetDomainId")
    def reset_domain_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDomainId", []))

    @jsii.member(jsii_name="resetDomainName")
    def reset_domain_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDomainName", []))

    @jsii.member(jsii_name="resetEnableLogging")
    def reset_enable_logging(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableLogging", []))

    @jsii.member(jsii_name="resetEndpointOverrides")
    def reset_endpoint_overrides(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEndpointOverrides", []))

    @jsii.member(jsii_name="resetEndpointType")
    def reset_endpoint_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEndpointType", []))

    @jsii.member(jsii_name="resetInsecure")
    def reset_insecure(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInsecure", []))

    @jsii.member(jsii_name="resetKey")
    def reset_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKey", []))

    @jsii.member(jsii_name="resetMaxRetries")
    def reset_max_retries(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxRetries", []))

    @jsii.member(jsii_name="resetPassword")
    def reset_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPassword", []))

    @jsii.member(jsii_name="resetProjectDomainId")
    def reset_project_domain_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProjectDomainId", []))

    @jsii.member(jsii_name="resetProjectDomainName")
    def reset_project_domain_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProjectDomainName", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetSwauth")
    def reset_swauth(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSwauth", []))

    @jsii.member(jsii_name="resetSystemScope")
    def reset_system_scope(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSystemScope", []))

    @jsii.member(jsii_name="resetTenantId")
    def reset_tenant_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTenantId", []))

    @jsii.member(jsii_name="resetTenantName")
    def reset_tenant_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTenantName", []))

    @jsii.member(jsii_name="resetToken")
    def reset_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetToken", []))

    @jsii.member(jsii_name="resetUserDomainId")
    def reset_user_domain_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserDomainId", []))

    @jsii.member(jsii_name="resetUserDomainName")
    def reset_user_domain_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserDomainName", []))

    @jsii.member(jsii_name="resetUserId")
    def reset_user_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserId", []))

    @jsii.member(jsii_name="resetUserName")
    def reset_user_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserName", []))

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
    @jsii.member(jsii_name="aliasInput")
    def alias_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "aliasInput"))

    @builtins.property
    @jsii.member(jsii_name="allowReauthInput")
    def allow_reauth_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowReauthInput"))

    @builtins.property
    @jsii.member(jsii_name="applicationCredentialIdInput")
    def application_credential_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "applicationCredentialIdInput"))

    @builtins.property
    @jsii.member(jsii_name="applicationCredentialNameInput")
    def application_credential_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "applicationCredentialNameInput"))

    @builtins.property
    @jsii.member(jsii_name="applicationCredentialSecretInput")
    def application_credential_secret_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "applicationCredentialSecretInput"))

    @builtins.property
    @jsii.member(jsii_name="authUrlInput")
    def auth_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="cacertFileInput")
    def cacert_file_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cacertFileInput"))

    @builtins.property
    @jsii.member(jsii_name="certInput")
    def cert_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "certInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudInput")
    def cloud_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cloudInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultDomainInput")
    def default_domain_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultDomainInput"))

    @builtins.property
    @jsii.member(jsii_name="delayedAuthInput")
    def delayed_auth_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "delayedAuthInput"))

    @builtins.property
    @jsii.member(jsii_name="disableNoCacheHeaderInput")
    def disable_no_cache_header_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disableNoCacheHeaderInput"))

    @builtins.property
    @jsii.member(jsii_name="domainIdInput")
    def domain_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "domainIdInput"))

    @builtins.property
    @jsii.member(jsii_name="domainNameInput")
    def domain_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "domainNameInput"))

    @builtins.property
    @jsii.member(jsii_name="enableLoggingInput")
    def enable_logging_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableLoggingInput"))

    @builtins.property
    @jsii.member(jsii_name="endpointOverridesInput")
    def endpoint_overrides_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "endpointOverridesInput"))

    @builtins.property
    @jsii.member(jsii_name="endpointTypeInput")
    def endpoint_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endpointTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="insecureInput")
    def insecure_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "insecureInput"))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="maxRetriesInput")
    def max_retries_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxRetriesInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="projectDomainIdInput")
    def project_domain_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectDomainIdInput"))

    @builtins.property
    @jsii.member(jsii_name="projectDomainNameInput")
    def project_domain_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectDomainNameInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="swauthInput")
    def swauth_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "swauthInput"))

    @builtins.property
    @jsii.member(jsii_name="systemScopeInput")
    def system_scope_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "systemScopeInput"))

    @builtins.property
    @jsii.member(jsii_name="tenantIdInput")
    def tenant_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tenantIdInput"))

    @builtins.property
    @jsii.member(jsii_name="tenantNameInput")
    def tenant_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tenantNameInput"))

    @builtins.property
    @jsii.member(jsii_name="tokenInput")
    def token_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tokenInput"))

    @builtins.property
    @jsii.member(jsii_name="userDomainIdInput")
    def user_domain_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userDomainIdInput"))

    @builtins.property
    @jsii.member(jsii_name="userDomainNameInput")
    def user_domain_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userDomainNameInput"))

    @builtins.property
    @jsii.member(jsii_name="userIdInput")
    def user_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userIdInput"))

    @builtins.property
    @jsii.member(jsii_name="userNameInput")
    def user_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userNameInput"))

    @builtins.property
    @jsii.member(jsii_name="alias")
    def alias(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "alias"))

    @alias.setter
    def alias(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81f167c3f7b6a7a3e06df8f9e9d52792df61cd45b31699ffe25bc31c85342055)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alias", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowReauth")
    def allow_reauth(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowReauth"))

    @allow_reauth.setter
    def allow_reauth(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aaf4a5a25b56540cb11529427ff3cb3aae2151fffa46763b6c30fc5794006819)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowReauth", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="applicationCredentialId")
    def application_credential_id(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "applicationCredentialId"))

    @application_credential_id.setter
    def application_credential_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67533ac4a6a0bf3ab7a6c421cf61cdb9a782f168966b767397d6a4f2fb55e065)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationCredentialId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="applicationCredentialName")
    def application_credential_name(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "applicationCredentialName"))

    @application_credential_name.setter
    def application_credential_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1399c5c4359dbff59dd02cc58ff5eb10c792d5832bcf9399c91db80b25d148d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationCredentialName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="applicationCredentialSecret")
    def application_credential_secret(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "applicationCredentialSecret"))

    @application_credential_secret.setter
    def application_credential_secret(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86cd637bb3544e937edcfdd2f78419d25f3a1ee3afb5657449bd1943e6a8707d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationCredentialSecret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="authUrl")
    def auth_url(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authUrl"))

    @auth_url.setter
    def auth_url(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb241cbdfeee2db64706a4e36c65539836bc220fd75e25646616f37e193f366c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cacertFile")
    def cacert_file(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cacertFile"))

    @cacert_file.setter
    def cacert_file(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b716d129fcc71ec99dd1c2fe0159caa70b444bfb017b7e17fa21a124d662c45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cacertFile", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cert")
    def cert(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cert"))

    @cert.setter
    def cert(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f332f356ca745ad473aab8c30c86f0acaf749db44f9eb0f66894afdefb106572)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cert", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cloud")
    def cloud(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cloud"))

    @cloud.setter
    def cloud(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abd6efef3bfe324fada007b66b174d4f2331b78addd5b6c11cd94bf1de795d41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cloud", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultDomain")
    def default_domain(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultDomain"))

    @default_domain.setter
    def default_domain(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2137b1e9157eac01fda8fd27889e0c5deaa042399c8c06886175518fc721c105)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultDomain", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delayedAuth")
    def delayed_auth(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "delayedAuth"))

    @delayed_auth.setter
    def delayed_auth(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3682e9a437f41c789bf4cd719d8161a7bff99d11c38658d2b69a252c080e0a2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delayedAuth", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="disableNoCacheHeader")
    def disable_no_cache_header(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disableNoCacheHeader"))

    @disable_no_cache_header.setter
    def disable_no_cache_header(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fb14ab2fe4301adafff18491ad4be699d78b2d2ca1682c9268bf9a52695e331)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableNoCacheHeader", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="domainId")
    def domain_id(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "domainId"))

    @domain_id.setter
    def domain_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebffa6882e278c7d96477aa2275f4b8e65ce01e5fd7f8e5e913059d45ca80d7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domainId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "domainName"))

    @domain_name.setter
    def domain_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c66247e71f036504989b02b07c97db6b6ca4470807ccc48be0ea31f84de8c858)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domainName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableLogging")
    def enable_logging(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableLogging"))

    @enable_logging.setter
    def enable_logging(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__586b741cc2ffef11628c50d61ed100c142407cec269bad04e4986332dd5e4c45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableLogging", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="endpointOverrides")
    def endpoint_overrides(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "endpointOverrides"))

    @endpoint_overrides.setter
    def endpoint_overrides(
        self,
        value: typing.Optional[typing.Mapping[builtins.str, builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fff878231af86607dfbb28f70aa2bddf16523eec74d2c0b45c71ec514e85d6ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endpointOverrides", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="endpointType")
    def endpoint_type(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endpointType"))

    @endpoint_type.setter
    def endpoint_type(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81bb064f1aab1abd11e6df6979d1603dde6b909171a0c0da4c11f292c2b8041c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endpointType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="insecure")
    def insecure(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "insecure"))

    @insecure.setter
    def insecure(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7100987b1ae58c096ff0a281ce0f4eb5acb3a6f3e35f187f1bdb0be1b3e59fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "insecure", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "key"))

    @key.setter
    def key(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90613dea0c1f841c210aea88d84e08fec4fca80dee068750100e7a25253c91ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxRetries")
    def max_retries(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxRetries"))

    @max_retries.setter
    def max_retries(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3a49f7c5351edee7a12a50511f79ba06b7c4e698a9cac24555f8b1216a7b35b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxRetries", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "password"))

    @password.setter
    def password(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b87382ce86ca5cedb98b06e875cb4f923e9a31eefa202276554b48de4aae5d3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectDomainId")
    def project_domain_id(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectDomainId"))

    @project_domain_id.setter
    def project_domain_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e578df0231eaa42bcc47f1d289c6fa49035a15ca5e9cb1a9e33b27948b191673)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectDomainId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectDomainName")
    def project_domain_name(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectDomainName"))

    @project_domain_name.setter
    def project_domain_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fba188b1957b59ed5ed1c31fc602b7b852c3e7169c76d61b6600879ac812b31e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectDomainName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "region"))

    @region.setter
    def region(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__605f8386e921405ade159a693ec1b52355ce0350fb2eee16d7c904dddfec99e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="swauth")
    def swauth(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "swauth"))

    @swauth.setter
    def swauth(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40f23bc84b5f48785d73885f58c84a0ab652ccfd970b157bd2ae3ef74bcee8a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "swauth", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="systemScope")
    def system_scope(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "systemScope"))

    @system_scope.setter
    def system_scope(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a6dcea594d49b381e056c43d5b06e21a48dc7de39b4f4bd958c0cb19ab22f08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "systemScope", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tenantId")
    def tenant_id(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tenantId"))

    @tenant_id.setter
    def tenant_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__837d69712f80255db358b4272b66356a2dd8a499fc5607eb48dcff468398befd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tenantId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tenantName")
    def tenant_name(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tenantName"))

    @tenant_name.setter
    def tenant_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86ddb36b9f43f6de3cbefbcdb7aa5f47e89d5f9ce2d49ea5af4caf34fec3ee45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tenantName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="token")
    def token(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "token"))

    @token.setter
    def token(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1351ebede74fa18d64d3111d0bf829984d819c4b4a301b2bc36392c62fc9cad1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "token", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userDomainId")
    def user_domain_id(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userDomainId"))

    @user_domain_id.setter
    def user_domain_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1410c78e3da362391935214ea7d67f2020247a477beec0243728d73334b00761)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userDomainId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userDomainName")
    def user_domain_name(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userDomainName"))

    @user_domain_name.setter
    def user_domain_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bd8f0b4e925a7005c0a276d7f0e708e6d72c3dc871f9bd671639b82fa776cf0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userDomainName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userId")
    def user_id(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userId"))

    @user_id.setter
    def user_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa684974b2e8eb1a0fc4d599fa384789e5e8cc79b704434cd79d0c37d08007a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userName")
    def user_name(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userName"))

    @user_name.setter
    def user_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad81da91d17f0513a46ec8242c6ffdf86c277eeb6705c1903ce2e2251c563024)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userName", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-openstack.provider.OpenstackProviderConfig",
    jsii_struct_bases=[],
    name_mapping={
        "alias": "alias",
        "allow_reauth": "allowReauth",
        "application_credential_id": "applicationCredentialId",
        "application_credential_name": "applicationCredentialName",
        "application_credential_secret": "applicationCredentialSecret",
        "auth_url": "authUrl",
        "cacert_file": "cacertFile",
        "cert": "cert",
        "cloud": "cloud",
        "default_domain": "defaultDomain",
        "delayed_auth": "delayedAuth",
        "disable_no_cache_header": "disableNoCacheHeader",
        "domain_id": "domainId",
        "domain_name": "domainName",
        "enable_logging": "enableLogging",
        "endpoint_overrides": "endpointOverrides",
        "endpoint_type": "endpointType",
        "insecure": "insecure",
        "key": "key",
        "max_retries": "maxRetries",
        "password": "password",
        "project_domain_id": "projectDomainId",
        "project_domain_name": "projectDomainName",
        "region": "region",
        "swauth": "swauth",
        "system_scope": "systemScope",
        "tenant_id": "tenantId",
        "tenant_name": "tenantName",
        "token": "token",
        "user_domain_id": "userDomainId",
        "user_domain_name": "userDomainName",
        "user_id": "userId",
        "user_name": "userName",
    },
)
class OpenstackProviderConfig:
    def __init__(
        self,
        *,
        alias: typing.Optional[builtins.str] = None,
        allow_reauth: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        application_credential_id: typing.Optional[builtins.str] = None,
        application_credential_name: typing.Optional[builtins.str] = None,
        application_credential_secret: typing.Optional[builtins.str] = None,
        auth_url: typing.Optional[builtins.str] = None,
        cacert_file: typing.Optional[builtins.str] = None,
        cert: typing.Optional[builtins.str] = None,
        cloud: typing.Optional[builtins.str] = None,
        default_domain: typing.Optional[builtins.str] = None,
        delayed_auth: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        disable_no_cache_header: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        domain_id: typing.Optional[builtins.str] = None,
        domain_name: typing.Optional[builtins.str] = None,
        enable_logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        endpoint_overrides: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        endpoint_type: typing.Optional[builtins.str] = None,
        insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        key: typing.Optional[builtins.str] = None,
        max_retries: typing.Optional[jsii.Number] = None,
        password: typing.Optional[builtins.str] = None,
        project_domain_id: typing.Optional[builtins.str] = None,
        project_domain_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        swauth: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        system_scope: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tenant_id: typing.Optional[builtins.str] = None,
        tenant_name: typing.Optional[builtins.str] = None,
        token: typing.Optional[builtins.str] = None,
        user_domain_id: typing.Optional[builtins.str] = None,
        user_domain_name: typing.Optional[builtins.str] = None,
        user_id: typing.Optional[builtins.str] = None,
        user_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param alias: Alias name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs#alias OpenstackProvider#alias}
        :param allow_reauth: If set to ``false``, OpenStack authorization won't be perfomed automatically, if the initial auth token get expired. Defaults to ``true``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs#allow_reauth OpenstackProvider#allow_reauth}
        :param application_credential_id: Application Credential ID to login with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs#application_credential_id OpenstackProvider#application_credential_id}
        :param application_credential_name: Application Credential name to login with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs#application_credential_name OpenstackProvider#application_credential_name}
        :param application_credential_secret: Application Credential secret to login with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs#application_credential_secret OpenstackProvider#application_credential_secret}
        :param auth_url: The Identity authentication URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs#auth_url OpenstackProvider#auth_url}
        :param cacert_file: A Custom CA certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs#cacert_file OpenstackProvider#cacert_file}
        :param cert: A client certificate to authenticate with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs#cert OpenstackProvider#cert}
        :param cloud: An entry in a ``clouds.yaml`` file to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs#cloud OpenstackProvider#cloud}
        :param default_domain: The name of the Domain ID to scope to if no other domain is specified. Defaults to ``default`` (Identity v3). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs#default_domain OpenstackProvider#default_domain}
        :param delayed_auth: If set to ``false``, OpenStack authorization will be perfomed, every time the service provider client is called. Defaults to ``true``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs#delayed_auth OpenstackProvider#delayed_auth}
        :param disable_no_cache_header: If set to ``true``, the HTTP ``Cache-Control: no-cache`` header will not be added by default to all API requests. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs#disable_no_cache_header OpenstackProvider#disable_no_cache_header}
        :param domain_id: The ID of the Domain to scope to (Identity v3). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs#domain_id OpenstackProvider#domain_id}
        :param domain_name: The name of the Domain to scope to (Identity v3). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs#domain_name OpenstackProvider#domain_name}
        :param enable_logging: Outputs very verbose logs with all calls made to and responses from OpenStack. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs#enable_logging OpenstackProvider#enable_logging}
        :param endpoint_overrides: A map of services with an endpoint to override what was from the Keystone catalog. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs#endpoint_overrides OpenstackProvider#endpoint_overrides}
        :param endpoint_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs#endpoint_type OpenstackProvider#endpoint_type}.
        :param insecure: Trust self-signed certificates. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs#insecure OpenstackProvider#insecure}
        :param key: A client private key to authenticate with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs#key OpenstackProvider#key}
        :param max_retries: How many times HTTP connection should be retried until giving up. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs#max_retries OpenstackProvider#max_retries}
        :param password: Password to login with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs#password OpenstackProvider#password}
        :param project_domain_id: The ID of the domain where the proejct resides (Identity v3). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs#project_domain_id OpenstackProvider#project_domain_id}
        :param project_domain_name: The name of the domain where the project resides (Identity v3). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs#project_domain_name OpenstackProvider#project_domain_name}
        :param region: The OpenStack region to connect to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs#region OpenstackProvider#region}
        :param swauth: Use Swift's authentication system instead of Keystone. Only used for interaction with Swift. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs#swauth OpenstackProvider#swauth}
        :param system_scope: If set to ``true``, system scoped authorization will be enabled. Defaults to ``false`` (Identity v3). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs#system_scope OpenstackProvider#system_scope}
        :param tenant_id: The ID of the Tenant (Identity v2) or Project (Identity v3) to login with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs#tenant_id OpenstackProvider#tenant_id}
        :param tenant_name: The name of the Tenant (Identity v2) or Project (Identity v3) to login with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs#tenant_name OpenstackProvider#tenant_name}
        :param token: Authentication token to use as an alternative to username/password. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs#token OpenstackProvider#token}
        :param user_domain_id: The ID of the domain where the user resides (Identity v3). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs#user_domain_id OpenstackProvider#user_domain_id}
        :param user_domain_name: The name of the domain where the user resides (Identity v3). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs#user_domain_name OpenstackProvider#user_domain_name}
        :param user_id: User ID to login with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs#user_id OpenstackProvider#user_id}
        :param user_name: Username to login with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs#user_name OpenstackProvider#user_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3947881f483202175409dc8d630f0a9aafa132f4b0ad294b9797a557232b7755)
            check_type(argname="argument alias", value=alias, expected_type=type_hints["alias"])
            check_type(argname="argument allow_reauth", value=allow_reauth, expected_type=type_hints["allow_reauth"])
            check_type(argname="argument application_credential_id", value=application_credential_id, expected_type=type_hints["application_credential_id"])
            check_type(argname="argument application_credential_name", value=application_credential_name, expected_type=type_hints["application_credential_name"])
            check_type(argname="argument application_credential_secret", value=application_credential_secret, expected_type=type_hints["application_credential_secret"])
            check_type(argname="argument auth_url", value=auth_url, expected_type=type_hints["auth_url"])
            check_type(argname="argument cacert_file", value=cacert_file, expected_type=type_hints["cacert_file"])
            check_type(argname="argument cert", value=cert, expected_type=type_hints["cert"])
            check_type(argname="argument cloud", value=cloud, expected_type=type_hints["cloud"])
            check_type(argname="argument default_domain", value=default_domain, expected_type=type_hints["default_domain"])
            check_type(argname="argument delayed_auth", value=delayed_auth, expected_type=type_hints["delayed_auth"])
            check_type(argname="argument disable_no_cache_header", value=disable_no_cache_header, expected_type=type_hints["disable_no_cache_header"])
            check_type(argname="argument domain_id", value=domain_id, expected_type=type_hints["domain_id"])
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            check_type(argname="argument enable_logging", value=enable_logging, expected_type=type_hints["enable_logging"])
            check_type(argname="argument endpoint_overrides", value=endpoint_overrides, expected_type=type_hints["endpoint_overrides"])
            check_type(argname="argument endpoint_type", value=endpoint_type, expected_type=type_hints["endpoint_type"])
            check_type(argname="argument insecure", value=insecure, expected_type=type_hints["insecure"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument max_retries", value=max_retries, expected_type=type_hints["max_retries"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument project_domain_id", value=project_domain_id, expected_type=type_hints["project_domain_id"])
            check_type(argname="argument project_domain_name", value=project_domain_name, expected_type=type_hints["project_domain_name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument swauth", value=swauth, expected_type=type_hints["swauth"])
            check_type(argname="argument system_scope", value=system_scope, expected_type=type_hints["system_scope"])
            check_type(argname="argument tenant_id", value=tenant_id, expected_type=type_hints["tenant_id"])
            check_type(argname="argument tenant_name", value=tenant_name, expected_type=type_hints["tenant_name"])
            check_type(argname="argument token", value=token, expected_type=type_hints["token"])
            check_type(argname="argument user_domain_id", value=user_domain_id, expected_type=type_hints["user_domain_id"])
            check_type(argname="argument user_domain_name", value=user_domain_name, expected_type=type_hints["user_domain_name"])
            check_type(argname="argument user_id", value=user_id, expected_type=type_hints["user_id"])
            check_type(argname="argument user_name", value=user_name, expected_type=type_hints["user_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if alias is not None:
            self._values["alias"] = alias
        if allow_reauth is not None:
            self._values["allow_reauth"] = allow_reauth
        if application_credential_id is not None:
            self._values["application_credential_id"] = application_credential_id
        if application_credential_name is not None:
            self._values["application_credential_name"] = application_credential_name
        if application_credential_secret is not None:
            self._values["application_credential_secret"] = application_credential_secret
        if auth_url is not None:
            self._values["auth_url"] = auth_url
        if cacert_file is not None:
            self._values["cacert_file"] = cacert_file
        if cert is not None:
            self._values["cert"] = cert
        if cloud is not None:
            self._values["cloud"] = cloud
        if default_domain is not None:
            self._values["default_domain"] = default_domain
        if delayed_auth is not None:
            self._values["delayed_auth"] = delayed_auth
        if disable_no_cache_header is not None:
            self._values["disable_no_cache_header"] = disable_no_cache_header
        if domain_id is not None:
            self._values["domain_id"] = domain_id
        if domain_name is not None:
            self._values["domain_name"] = domain_name
        if enable_logging is not None:
            self._values["enable_logging"] = enable_logging
        if endpoint_overrides is not None:
            self._values["endpoint_overrides"] = endpoint_overrides
        if endpoint_type is not None:
            self._values["endpoint_type"] = endpoint_type
        if insecure is not None:
            self._values["insecure"] = insecure
        if key is not None:
            self._values["key"] = key
        if max_retries is not None:
            self._values["max_retries"] = max_retries
        if password is not None:
            self._values["password"] = password
        if project_domain_id is not None:
            self._values["project_domain_id"] = project_domain_id
        if project_domain_name is not None:
            self._values["project_domain_name"] = project_domain_name
        if region is not None:
            self._values["region"] = region
        if swauth is not None:
            self._values["swauth"] = swauth
        if system_scope is not None:
            self._values["system_scope"] = system_scope
        if tenant_id is not None:
            self._values["tenant_id"] = tenant_id
        if tenant_name is not None:
            self._values["tenant_name"] = tenant_name
        if token is not None:
            self._values["token"] = token
        if user_domain_id is not None:
            self._values["user_domain_id"] = user_domain_id
        if user_domain_name is not None:
            self._values["user_domain_name"] = user_domain_name
        if user_id is not None:
            self._values["user_id"] = user_id
        if user_name is not None:
            self._values["user_name"] = user_name

    @builtins.property
    def alias(self) -> typing.Optional[builtins.str]:
        '''Alias name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs#alias OpenstackProvider#alias}
        '''
        result = self._values.get("alias")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def allow_reauth(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set to ``false``, OpenStack authorization won't be perfomed automatically, if the initial auth token get expired. Defaults to ``true``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs#allow_reauth OpenstackProvider#allow_reauth}
        '''
        result = self._values.get("allow_reauth")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def application_credential_id(self) -> typing.Optional[builtins.str]:
        '''Application Credential ID to login with.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs#application_credential_id OpenstackProvider#application_credential_id}
        '''
        result = self._values.get("application_credential_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def application_credential_name(self) -> typing.Optional[builtins.str]:
        '''Application Credential name to login with.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs#application_credential_name OpenstackProvider#application_credential_name}
        '''
        result = self._values.get("application_credential_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def application_credential_secret(self) -> typing.Optional[builtins.str]:
        '''Application Credential secret to login with.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs#application_credential_secret OpenstackProvider#application_credential_secret}
        '''
        result = self._values.get("application_credential_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def auth_url(self) -> typing.Optional[builtins.str]:
        '''The Identity authentication URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs#auth_url OpenstackProvider#auth_url}
        '''
        result = self._values.get("auth_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cacert_file(self) -> typing.Optional[builtins.str]:
        '''A Custom CA certificate.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs#cacert_file OpenstackProvider#cacert_file}
        '''
        result = self._values.get("cacert_file")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cert(self) -> typing.Optional[builtins.str]:
        '''A client certificate to authenticate with.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs#cert OpenstackProvider#cert}
        '''
        result = self._values.get("cert")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cloud(self) -> typing.Optional[builtins.str]:
        '''An entry in a ``clouds.yaml`` file to use.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs#cloud OpenstackProvider#cloud}
        '''
        result = self._values.get("cloud")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_domain(self) -> typing.Optional[builtins.str]:
        '''The name of the Domain ID to scope to if no other domain is specified.

        Defaults to ``default`` (Identity v3).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs#default_domain OpenstackProvider#default_domain}
        '''
        result = self._values.get("default_domain")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delayed_auth(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set to ``false``, OpenStack authorization will be perfomed, every time the service provider client is called. Defaults to ``true``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs#delayed_auth OpenstackProvider#delayed_auth}
        '''
        result = self._values.get("delayed_auth")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def disable_no_cache_header(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set to ``true``, the HTTP ``Cache-Control: no-cache`` header will not be added by default to all API requests.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs#disable_no_cache_header OpenstackProvider#disable_no_cache_header}
        '''
        result = self._values.get("disable_no_cache_header")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def domain_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the Domain to scope to (Identity v3).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs#domain_id OpenstackProvider#domain_id}
        '''
        result = self._values.get("domain_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def domain_name(self) -> typing.Optional[builtins.str]:
        '''The name of the Domain to scope to (Identity v3).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs#domain_name OpenstackProvider#domain_name}
        '''
        result = self._values.get("domain_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_logging(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Outputs very verbose logs with all calls made to and responses from OpenStack.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs#enable_logging OpenstackProvider#enable_logging}
        '''
        result = self._values.get("enable_logging")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def endpoint_overrides(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A map of services with an endpoint to override what was from the Keystone catalog.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs#endpoint_overrides OpenstackProvider#endpoint_overrides}
        '''
        result = self._values.get("endpoint_overrides")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def endpoint_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs#endpoint_type OpenstackProvider#endpoint_type}.'''
        result = self._values.get("endpoint_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def insecure(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Trust self-signed certificates.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs#insecure OpenstackProvider#insecure}
        '''
        result = self._values.get("insecure")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''A client private key to authenticate with.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs#key OpenstackProvider#key}
        '''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_retries(self) -> typing.Optional[jsii.Number]:
        '''How many times HTTP connection should be retried until giving up.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs#max_retries OpenstackProvider#max_retries}
        '''
        result = self._values.get("max_retries")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''Password to login with.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs#password OpenstackProvider#password}
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project_domain_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the domain where the proejct resides (Identity v3).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs#project_domain_id OpenstackProvider#project_domain_id}
        '''
        result = self._values.get("project_domain_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project_domain_name(self) -> typing.Optional[builtins.str]:
        '''The name of the domain where the project resides (Identity v3).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs#project_domain_name OpenstackProvider#project_domain_name}
        '''
        result = self._values.get("project_domain_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The OpenStack region to connect to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs#region OpenstackProvider#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def swauth(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Use Swift's authentication system instead of Keystone. Only used for interaction with Swift.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs#swauth OpenstackProvider#swauth}
        '''
        result = self._values.get("swauth")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def system_scope(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set to ``true``, system scoped authorization will be enabled. Defaults to ``false`` (Identity v3).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs#system_scope OpenstackProvider#system_scope}
        '''
        result = self._values.get("system_scope")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tenant_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the Tenant (Identity v2) or Project (Identity v3) to login with.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs#tenant_id OpenstackProvider#tenant_id}
        '''
        result = self._values.get("tenant_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tenant_name(self) -> typing.Optional[builtins.str]:
        '''The name of the Tenant (Identity v2) or Project (Identity v3) to login with.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs#tenant_name OpenstackProvider#tenant_name}
        '''
        result = self._values.get("tenant_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def token(self) -> typing.Optional[builtins.str]:
        '''Authentication token to use as an alternative to username/password.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs#token OpenstackProvider#token}
        '''
        result = self._values.get("token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_domain_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the domain where the user resides (Identity v3).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs#user_domain_id OpenstackProvider#user_domain_id}
        '''
        result = self._values.get("user_domain_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_domain_name(self) -> typing.Optional[builtins.str]:
        '''The name of the domain where the user resides (Identity v3).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs#user_domain_name OpenstackProvider#user_domain_name}
        '''
        result = self._values.get("user_domain_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_id(self) -> typing.Optional[builtins.str]:
        '''User ID to login with.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs#user_id OpenstackProvider#user_id}
        '''
        result = self._values.get("user_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_name(self) -> typing.Optional[builtins.str]:
        '''Username to login with.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs#user_name OpenstackProvider#user_name}
        '''
        result = self._values.get("user_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OpenstackProviderConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "OpenstackProvider",
    "OpenstackProviderConfig",
]

publication.publish()

def _typecheckingstub__4c296a0a70f54038ecc9d9471b2283c854a31f9368ad483babb40f8e1902b6b0(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    alias: typing.Optional[builtins.str] = None,
    allow_reauth: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    application_credential_id: typing.Optional[builtins.str] = None,
    application_credential_name: typing.Optional[builtins.str] = None,
    application_credential_secret: typing.Optional[builtins.str] = None,
    auth_url: typing.Optional[builtins.str] = None,
    cacert_file: typing.Optional[builtins.str] = None,
    cert: typing.Optional[builtins.str] = None,
    cloud: typing.Optional[builtins.str] = None,
    default_domain: typing.Optional[builtins.str] = None,
    delayed_auth: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    disable_no_cache_header: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    domain_id: typing.Optional[builtins.str] = None,
    domain_name: typing.Optional[builtins.str] = None,
    enable_logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    endpoint_overrides: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    endpoint_type: typing.Optional[builtins.str] = None,
    insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    key: typing.Optional[builtins.str] = None,
    max_retries: typing.Optional[jsii.Number] = None,
    password: typing.Optional[builtins.str] = None,
    project_domain_id: typing.Optional[builtins.str] = None,
    project_domain_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    swauth: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    system_scope: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tenant_id: typing.Optional[builtins.str] = None,
    tenant_name: typing.Optional[builtins.str] = None,
    token: typing.Optional[builtins.str] = None,
    user_domain_id: typing.Optional[builtins.str] = None,
    user_domain_name: typing.Optional[builtins.str] = None,
    user_id: typing.Optional[builtins.str] = None,
    user_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf3eba471d77d385753a3c9cd685356e187d818489c92d41b3a185affc7c4cd4(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81f167c3f7b6a7a3e06df8f9e9d52792df61cd45b31699ffe25bc31c85342055(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aaf4a5a25b56540cb11529427ff3cb3aae2151fffa46763b6c30fc5794006819(
    value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67533ac4a6a0bf3ab7a6c421cf61cdb9a782f168966b767397d6a4f2fb55e065(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1399c5c4359dbff59dd02cc58ff5eb10c792d5832bcf9399c91db80b25d148d2(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86cd637bb3544e937edcfdd2f78419d25f3a1ee3afb5657449bd1943e6a8707d(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb241cbdfeee2db64706a4e36c65539836bc220fd75e25646616f37e193f366c(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b716d129fcc71ec99dd1c2fe0159caa70b444bfb017b7e17fa21a124d662c45(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f332f356ca745ad473aab8c30c86f0acaf749db44f9eb0f66894afdefb106572(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abd6efef3bfe324fada007b66b174d4f2331b78addd5b6c11cd94bf1de795d41(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2137b1e9157eac01fda8fd27889e0c5deaa042399c8c06886175518fc721c105(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3682e9a437f41c789bf4cd719d8161a7bff99d11c38658d2b69a252c080e0a2f(
    value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fb14ab2fe4301adafff18491ad4be699d78b2d2ca1682c9268bf9a52695e331(
    value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebffa6882e278c7d96477aa2275f4b8e65ce01e5fd7f8e5e913059d45ca80d7f(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c66247e71f036504989b02b07c97db6b6ca4470807ccc48be0ea31f84de8c858(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__586b741cc2ffef11628c50d61ed100c142407cec269bad04e4986332dd5e4c45(
    value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fff878231af86607dfbb28f70aa2bddf16523eec74d2c0b45c71ec514e85d6ce(
    value: typing.Optional[typing.Mapping[builtins.str, builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81bb064f1aab1abd11e6df6979d1603dde6b909171a0c0da4c11f292c2b8041c(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7100987b1ae58c096ff0a281ce0f4eb5acb3a6f3e35f187f1bdb0be1b3e59fc(
    value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90613dea0c1f841c210aea88d84e08fec4fca80dee068750100e7a25253c91ed(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3a49f7c5351edee7a12a50511f79ba06b7c4e698a9cac24555f8b1216a7b35b(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b87382ce86ca5cedb98b06e875cb4f923e9a31eefa202276554b48de4aae5d3b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e578df0231eaa42bcc47f1d289c6fa49035a15ca5e9cb1a9e33b27948b191673(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fba188b1957b59ed5ed1c31fc602b7b852c3e7169c76d61b6600879ac812b31e(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__605f8386e921405ade159a693ec1b52355ce0350fb2eee16d7c904dddfec99e2(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40f23bc84b5f48785d73885f58c84a0ab652ccfd970b157bd2ae3ef74bcee8a5(
    value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a6dcea594d49b381e056c43d5b06e21a48dc7de39b4f4bd958c0cb19ab22f08(
    value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__837d69712f80255db358b4272b66356a2dd8a499fc5607eb48dcff468398befd(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86ddb36b9f43f6de3cbefbcdb7aa5f47e89d5f9ce2d49ea5af4caf34fec3ee45(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1351ebede74fa18d64d3111d0bf829984d819c4b4a301b2bc36392c62fc9cad1(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1410c78e3da362391935214ea7d67f2020247a477beec0243728d73334b00761(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bd8f0b4e925a7005c0a276d7f0e708e6d72c3dc871f9bd671639b82fa776cf0(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa684974b2e8eb1a0fc4d599fa384789e5e8cc79b704434cd79d0c37d08007a4(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad81da91d17f0513a46ec8242c6ffdf86c277eeb6705c1903ce2e2251c563024(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3947881f483202175409dc8d630f0a9aafa132f4b0ad294b9797a557232b7755(
    *,
    alias: typing.Optional[builtins.str] = None,
    allow_reauth: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    application_credential_id: typing.Optional[builtins.str] = None,
    application_credential_name: typing.Optional[builtins.str] = None,
    application_credential_secret: typing.Optional[builtins.str] = None,
    auth_url: typing.Optional[builtins.str] = None,
    cacert_file: typing.Optional[builtins.str] = None,
    cert: typing.Optional[builtins.str] = None,
    cloud: typing.Optional[builtins.str] = None,
    default_domain: typing.Optional[builtins.str] = None,
    delayed_auth: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    disable_no_cache_header: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    domain_id: typing.Optional[builtins.str] = None,
    domain_name: typing.Optional[builtins.str] = None,
    enable_logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    endpoint_overrides: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    endpoint_type: typing.Optional[builtins.str] = None,
    insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    key: typing.Optional[builtins.str] = None,
    max_retries: typing.Optional[jsii.Number] = None,
    password: typing.Optional[builtins.str] = None,
    project_domain_id: typing.Optional[builtins.str] = None,
    project_domain_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    swauth: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    system_scope: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tenant_id: typing.Optional[builtins.str] = None,
    tenant_name: typing.Optional[builtins.str] = None,
    token: typing.Optional[builtins.str] = None,
    user_domain_id: typing.Optional[builtins.str] = None,
    user_domain_name: typing.Optional[builtins.str] = None,
    user_id: typing.Optional[builtins.str] = None,
    user_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
