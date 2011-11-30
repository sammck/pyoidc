
__author__ = 'rohe0002'

import hmac
import hashlib
import time
import random
import base64
from oic import oauth2
from oic.oauth2 import MissingRequiredAttribute
from oic.oauth2 import Base
from oic.oauth2 import TooManyValues

from pytest import raises

class CLASS(Base):
    c_attributes = Base.c_attributes.copy()
    c_attributes["req_str"] = oauth2.SINGLE_REQUIRED_STRING
    c_attributes["opt_str"] = oauth2.SINGLE_OPTIONAL_STRING
    c_attributes["opt_int"] = oauth2.SINGLE_OPTIONAL_INT
    c_attributes["opt_str_list"] = oauth2.OPTIONAL_LIST_OF_STRINGS
    c_attributes["req_str_list"] = oauth2.REQUIRED_LIST_OF_STRINGS
    c_attributes["opt_json"] = oauth2.SINGLE_OPTIONAL_JSON

    def __init__(self,
                 req_str=None,
                 opt_str=None,
                 opt_int=None,
                 opt_str_list=None,
                 req_str_list=None,
                 opt_json=None,
                 **kwargs):
        Base.__init__(self, **kwargs)
        self.req_str = req_str
        self.opt_str = opt_str
        self.opt_int = opt_int
        self.opt_str_list = opt_str_list or []
        self.req_str_list = req_str_list or []
        self.opt_json = opt_json

        
def _eq(l1, l2):
    return set(l1) == set(l2)

def test_authz_req_urlencoded_1():
    ar = oauth2.AuthorizationRequest(["code"], "foobar")
    ue = ar.get_urlencoded()
    print ue
    assert ue == "response_type=code&client_id=foobar"

def test_authz_req_urlencoded_2():
    ar = oauth2.AuthorizationRequest(["code"], "foobar",
                                     "http://foobar.example.com/oaclient",
                                     state="cold")
    ue = ar.get_urlencoded()
    print ue
    assert ue == "state=cold&redirect_uri=http%3A%2F%2Ffoobar.example.com%2Foaclient&response_type=code&client_id=foobar"

def test_authz_req_urlencoded_3():
    ar = oauth2.AuthorizationRequest(["token"],
                                    "s6BhdRkqt3",
                                    "https://client.example.com/cb",
                                    state="xyz")
    ue = ar.get_urlencoded()
    print ue
    assert ue == "state=xyz&redirect_uri=https%3A%2F%2Fclient.example.com%2Fcb&response_type=token&client_id=s6BhdRkqt3"

def test_authz_req_urlencoded_4():
    ar = oauth2.AuthorizationRequest(["code"], "foobar")
    urlencoded = ar.get_urlencoded()
    ar2 = oauth2.AuthorizationRequest.set_urlencoded(urlencoded)

    print ar
    print ar2
    
    for attr in ar.c_attributes.keys():
        assert getattr(ar, attr) == getattr(ar2, attr)
    
def test_authz_req_urlencoded_5():
    ar = oauth2.AuthorizationRequest(["code"], "foobar",
                                     "http://foobar.example.com/oaclient",
                                     ["foo", "bar"],
                                     state="cold")

    ue = ar.get_urlencoded()
    print ue
    assert ue == "scope=foo+bar&state=cold&redirect_uri=http%3A%2F%2Ffoobar.example.com%2Foaclient&response_type=code&client_id=foobar"

def test_authz_req_urlencoded_6():
    ar = oauth2.AuthorizationRequest(["code"], "foobar",
                                     "http://foobar.example.com/oaclient",
                                     ["foo", "bar"],
                                     state="cold")

    urlencoded = ar.get_urlencoded()
    ar2 = oauth2.AuthorizationRequest.set_urlencoded(urlencoded)

    for attr in ar.c_attributes.keys():
        assert getattr(ar, attr) == getattr(ar2, attr)

def test_authz_req_urlencoded_7():
    ar = oauth2.AuthorizationRequest(["code"])
    raises(MissingRequiredAttribute, ar.verify)

def test_authz_req_urlencoded_8():
    ar = oauth2.AuthorizationRequest([10], "foobar",
                                     "http://foobar.example.com/oaclient",
                                     ["foo", "bar"],
                                     state="cold")

    raises(ValueError, ar.verify)

def test_authz_req_urlencoded_9():
    txt = "scope=foo+bar&state=-11&redirect_uri=http%3A%2F%2Ffoobar.example.com%2Foaclient&response_type=code&client_id=foobar"

    ar = oauth2.AuthorizationRequest.set_urlencoded(txt)
    print ar
    assert ar.state == "-11"

def test_authz_req_urlencoded_10():
    txt = "scope=openid&state=id-6a3fc96caa7fd5cb1c7d00ed66937134&redirect_uri=http%3A%2F%2Flocalhost%3A8087authz&response_type=code&client_id=a1b2c3"

    ar = oauth2.AuthorizationRequest.set_urlencoded(txt)
    print ar
    assert ar.scope == ["openid"]
    assert ar.response_type == ["code"]


def test_authz_req_json_1():
    ar = oauth2.AuthorizationRequest(["code"], "foobar")
    js = ar.get_json()
    print js
    assert js == '{"response_type": ["code"], "client_id": "foobar"}'

def test_authz_req_json_2():
    ar = oauth2.AuthorizationRequest(["code"], "foobar",
                                     "http://foobar.example.com/oaclient",
                                     state="cold")
    ue = ar.get_json()
    print ue
    assert ue == '{"state": "cold", "redirect_uri": "http://foobar.example.com/oaclient", "response_type": ["code"], "client_id": "foobar"}'

def test_authz_req_urlencoded_3():
    ar = oauth2.AuthorizationRequest(["token"],
                                    "s6BhdRkqt3",
                                    "https://client.example.com/cb",
                                    state="xyz")
    ue = ar.get_json()
    print ue
    assert ue == '{"state": "xyz", "redirect_uri": "https://client.example.com/cb", "response_type": ["token"], "client_id": "s6BhdRkqt3"}'

def test_authz_req_urlencoded_4():
    ar = oauth2.AuthorizationRequest(["code"], "foobar")
    jtxt = ar.get_json()
    ar2 = oauth2.AuthorizationRequest.set_json(jtxt)

    print ar
    print ar2

    for attr in ar.c_attributes.keys():
        assert getattr(ar, attr) == getattr(ar2, attr)

def test_authz_req_x1():
    query = 'redirect_uri=http%3A%2F%2Flocalhost%3A8080%2Fauthz&response_type=code&client_id=0123456789'

    ar = oauth2.AuthorizationRequest.set_urlencoded(query)

    print ar

    assert ar.verify()

# AuthorizationErrorResponse

def test_authz_err_resp_1():
    aer = oauth2.AuthorizationErrorResponse(error="access_denied", state="xyz")

    assert aer
    print aer.__dict__.items()
    assert aer.error == "access_denied"
    assert aer.state == "xyz"
    assert aer.c_extension == {}

def test_authz_err_resp_2():
    aer = oauth2.AuthorizationErrorResponse(error="access_denied",
                            error_description="brewers has a four game series",
                            foo="bar")

    assert aer
    print aer.__dict__.items()
    assert aer.error == "access_denied"
    assert aer.error_description == "brewers has a four game series"
    assert aer.c_extension == {'foo': 'bar'}

# TokenErrorResponse

def test_authz_err_resp_1():
    ter = oauth2.TokenErrorResponse(error="access_denied", state="xyz")

    assert ter
    print ter.__dict__.items()
    assert ter.error == "access_denied"
    assert ter.c_extension == {'state': 'xyz'}

def test_authz_err_resp_2():
    ter = oauth2.TokenErrorResponse(error="access_denied",
                            error_description="brewers has a four game series",
                            foo="bar")

    assert ter
    print ter.__dict__.items()
    assert ter.error == "access_denied"
    assert ter.error_description == "brewers has a four game series"
    assert ter.c_extension == {'foo': 'bar'}

# AccessTokenResponse

def test_accesstokenreponse_1():
    at = oauth2.AccessTokenResponse("SlAV32hkKG", "8xLOxBtZp8", 3600)

    assert at
    atj = at.get_json()
    print atj
    assert atj == '{"access_token": "SlAV32hkKG", "token_type": "8xLOxBtZp8", "expires_in": 3600}'

# AccessTokenRequest

def test_extra():
    atr = oauth2.AccessTokenRequest("authorization_code",
                                    "SplxlOBeZQQYbYS6WxSbIA",
                                    "https://client.example.com/cb",
                                    "client_id",
                                    extra="foo")

    assert atr
    query = atr.get_urlencoded(True)
    print query
    assert query == "code=SplxlOBeZQQYbYS6WxSbIA&grant_type=authorization_code&client_id=client_id&redirect_uri=https%3A%2F%2Fclient.example.com%2Fcb&extra=foo"

    atr2 = oauth2.AccessTokenRequest.set_urlencoded(query, True)
    print atr2.c_extension
    assert atr2.c_extension == {"extra": "foo"}

# AuthorizationResponse

def test_authz_resp_1():
    atr = oauth2.AuthorizationResponse("SplxlOBeZQQYbYS6WxSbIA",
                                        "Fun_state",
                                        extra="foo")

    assert atr.code == "SplxlOBeZQQYbYS6WxSbIA"
    assert atr.state == "Fun_state"
    print atr.c_extension
    assert atr.c_extension == {"extra": "foo"}

# ROPCAccessTokenRequest

#noinspection PyArgumentEqualDefault
def test_ropc_acc_token_req():
    ropc = oauth2.ROPCAccessTokenRequest("password", "johndoe", "A3ddj3w")

    assert ropc.grant_type == "password"
    assert ropc.username == "johndoe"
    assert ropc.password == "A3ddj3w"

# CCAccessTokenRequest

def test_cc_acc_token_req():
    cc = oauth2.CCAccessTokenRequest(scope="/foo")

    assert cc.grant_type == "client_credentials"
    assert cc.scope == "/foo"

# RefreshAccessTokenRequest

def test_ratr():
    ratr = oauth2.RefreshAccessTokenRequest(refresh_token="ababababab",
                                            client_id="Client_id")

    assert ratr.grant_type == "refresh_token"
    assert ratr.refresh_token == "ababababab"
    assert ratr.client_id == "Client_id"

    assert ratr.verify()

def test_crypt():
    crypt = oauth2.Crypt("4-amino-1H-pyrimidine-2-one")
    ctext = crypt.encrypt("Cytosine")
    plain = crypt.decrypt(ctext)
    print plain
    assert plain == 'Cytosine        '

    ctext = crypt.encrypt("cytidinetriphosp")
    plain = crypt.decrypt(ctext)

    assert plain == 'cytidinetriphosp'

def test_crypt2():
    db = {}
    csum = hmac.new("secret", digestmod=hashlib.sha224)
    csum.update("%s" % time.time())
    csum.update("%f" % random.random())
    txt = csum.digest() # 28 bytes long, 224 bits
    print len(txt)
    db[txt] = "foobar"
    txt = "%saces" % txt # another 4 bytes
    #print len(txt), txt
    crypt = oauth2.Crypt("4-amino-1H-pyrimidine-2-one")
    ctext = crypt.encrypt(txt)
    onthewire = base64.b64encode(ctext)
    #print onthewire
    plain = crypt.decrypt(base64.b64decode(onthewire))
    #print len(plain), plain
    #assert plain == txt
    assert plain.endswith("aces")
    assert db[plain[:-4]] == "foobar"

def test_authz_load_dict():
    bib = {"scope": ["openid"],
           "state": "id-6da9ca0cc23959f5f33e8becd9b08cae",
           "redirect_uri": "http://localhost:8087authz",
           "response_type": ["code"],
           "client_id": "a1b2c3"}

    arq = oauth2.AuthorizationRequest(**bib)

    assert arq.scope == bib["scope"]
    assert arq.response_type == bib["response_type"]
    assert arq.redirect_uri == bib["redirect_uri"]
    assert arq.state == bib["state"]
    assert arq.client_id == bib["client_id"]

def test_authz_req_set_json():
    argv = {"scope": ["openid"],
            "state": "id-b0be8bb64118c3ec5f70093a1174b039",
            "redirect_uri": "http://localhost:8087authz",
            "response_type": ["code"],
            "client_id": "a1b2c3"}

    arq = oauth2.AuthorizationRequest(**argv)


    jstr = arq.get_json()

    jarq = oauth2.AuthorizationRequest.set_json(jstr)

    assert jarq.scope == ["openid"]
    assert jarq.response_type == ["code"]
    assert jarq.redirect_uri == "http://localhost:8087authz"
    assert jarq.state == "id-b0be8bb64118c3ec5f70093a1174b039"
    assert jarq.client_id == "a1b2c3"

def test_sp_sep_list_deserializer():
    vals = oauth2.sp_sep_list_deserializer("foo bar zen")
    assert len(vals) == 3
    assert _eq(vals, ["foo", "bar", "zen"])

    vals = oauth2.sp_sep_list_deserializer(["foo bar zen"])
    assert len(vals) == 3
    assert _eq(vals, ["foo", "bar", "zen"])

def test_json_serializer():
    val = oauth2.json_serializer({"foo": ["bar", "stool"]})
    print val
    assert val == '{"foo": ["bar", "stool"]}'

def test_json_deserializer():
    _dict = {"foo": ["bar", "stool"]}
    val = oauth2.json_serializer(_dict)

    sdict = oauth2.json_deserializer(val)
    assert _dict == sdict

def test_omit():
    err = oauth2.ErrorResponse("invalid_request",
                                "Something was missing",
                                "http://example.com/error_message.html")

    ue_str = err.to_urlencoded()
    ueo_str = err.to_urlencoded(omit=["error_uri"])

    assert ue_str != ueo_str
    assert "error_message" not in ueo_str
    assert "error_message" in ue_str

def test_missing_required():
    err = oauth2.ErrorResponse()
    assert err.error is None

    raises(MissingRequiredAttribute, "err.to_urlencoded()")

def test_get_urlencoded():
    atr = oauth2.AccessTokenResponse(
                            access_token="2YotnFZFEjr1zCsicMWpAA",
                            token_type="example",
                            expires_in=3600,
                            refresh_token="tGzv3JOkF0XG5Qx2TlKWIA",
                            example_parameter="example_value",
                            scope=["inner", "outer"])

    assert _eq(atr.scope, ["inner", "outer"])

    uec = atr.get_urlencoded()
    print uec
    assert "inner+outer" in uec

def test_get_urlencoded_extended_omit():
    atr = oauth2.AccessTokenResponse(
                            access_token="2YotnFZFEjr1zCsicMWpAA",
                            token_type="example",
                            expires_in=3600,
                            refresh_token="tGzv3JOkF0XG5Qx2TlKWIA",
                            example_parameter="example_value",
                            scope=["inner", "outer"],
                            extra=["local", "external"],
                            level=3)

    assert _eq(atr.c_extension.keys(), ["example_parameter", "extra", "level"])

    uec = atr.get_urlencoded(extended=True)
    print uec
    assert "level=3" in uec
    assert "example_parameter=example_value" in uec
    assert "extra=local+external" in uec
    ouec = atr.get_urlencoded(extended=True, omit=["extra"])
    print ouec
    assert "level=3" in ouec
    assert "example_parameter=example_value" in ouec
    assert "extra=local+external" not in ouec
    assert uec != ouec
    assert len(uec) == (len(ouec) + len("extra=local+external") + 1)

    atr2 = oauth2.AccessTokenResponse.set_urlencoded(uec, True)
    print atr2.keys()
    assert _eq(atr2.keys(),['access_token', 'expires_in', 'token_type',
                            'scope', 'refresh_token', 'level',
                            'example_parameter', 'extra'])

    atr3 = oauth2.AccessTokenResponse.set_urlencoded(ouec, True)
    print atr3.keys()
    assert _eq(atr3.keys(),['access_token', 'expires_in', 'token_type',
                            'scope', 'refresh_token', 'level',
                            'example_parameter'])

##noinspection PyUnusedLocal
#def test_get_urlencoded_to_many_values():
#    uec = "access_token=2YotnFZFEjr1zCsicMWpAA+AAA111BBB222CCC333"
#    raises(ValueError, "oauth2.AccessTokenResponse.set_urlencoded(uec)")

#noinspection PyUnusedLocal
def test_get_set_json():
    """

    """
    item = CLASS(req_str="Fair", opt_str="game", opt_int=9,
                opt_str_list=["one", "two"], req_str_list=["spike", "lee"],
                opt_json='{"ford": "green"}')

    jso = item.get_json()
    print jso
    item2 = CLASS.set_json(jso)
    print item2
    assert _eq(item2.keys(),['opt_str', 'req_str', 'opt_json', 'req_str_list',
                             'opt_str_list', 'opt_int'])

    jso_1 = '{"req_str": "Fair", "req_str_list": ["spike", "lee"], "opt_int": [9]}'

    item3 = CLASS.set_json(jso_1)
    assert _eq(item3.keys(),['req_str', 'req_str_list', 'opt_int'])
    assert item3.opt_int == 9

    jso_2 = '{"req_str": "Fair", "req_str_list": ["spike", "lee"], "opt_int": [9, 10]}'
    raises(TooManyValues, "CLASS.set_json(jso_2)")

    jso_3 = '{"req_str": "Fair", "req_str_list": ["spike", "lee"], "extra": "out"}'
    item4 = CLASS.set_json(jso_3, extended=True)

    print item4
    assert _eq(item4.keys(),['req_str', 'req_str_list', 'extra'])
    assert item4.extra == "out"
    
    item4 = CLASS.from_json(jso_3, extended=True)

    print item4
    assert _eq(item4.keys(),['req_str', 'req_str_list', 'extra'])
    assert item4.extra == "out"

def test_to_from_jwt():
    item = CLASS(req_str="Fair", opt_str="game", opt_int=9,
                opt_str_list=["one", "two"], req_str_list=["spike", "lee"],
                opt_json='{"ford": "green"}')

    jws = item.to_jwt(True, "A1B2C3D4", "HS256")

    print jws

    jitem = CLASS.from_jwt(jws, "A1B2C3D4")

    print jitem.keys()

    assert _eq(jitem.keys(), ['opt_str', 'req_str', 'opt_json',
                              'req_str_list', 'opt_str_list', 'opt_int'])

#noinspection PyUnusedLocal
def test_TokenErrorResponse():
    terr = oauth2.TokenErrorResponse("invalid_request", "Missing argument")
    assert terr.verify()

    terr = oauth2.TokenErrorResponse("whatever", "Missing argument")
    raises(ValueError, "terr.verify()")

#noinspection PyUnusedLocal,PyArgumentEqualDefault
def test_ROPCAccessTokenRequest():
    ratr = oauth2.ROPCAccessTokenRequest("password", "user", "secret")
    assert ratr.verify()

    ratr = oauth2.ROPCAccessTokenRequest("certificate", "user", "secret")
    raises(AssertionError, "ratr.verify()")


#noinspection PyUnusedLocal,PyArgumentEqualDefault
def test_CCAccessTokenRequest():
    catr = oauth2.CCAccessTokenRequest("client_credentials", "home")
    assert catr.verify()

    catr = oauth2.CCAccessTokenRequest("password", "home")
    raises(AssertionError, "catr.verify()")

def test_TokenRevocationRequest():
    trr = oauth2.TokenRevocationRequest("token")
    assert trr.verify()

def test_factory():
    _dict = {"req_str":"Fair", "opt_str":"game", "opt_int":9,
                "opt_str_list":["one", "two"], "req_str_list":["spike", "lee"],
                "opt_json":'{"ford": "green"}'}

    cls = oauth2.factory(CLASS, **_dict)
    cls.verify()
    assert _eq(cls.keys(), ['opt_str', 'req_str', 'opt_json',
                              'req_str_list', 'opt_str_list', 'opt_int'])

    _dict = {"req_str":"Fair", "opt_str":"game", "opt_int":9,
                "opt_str_list":["one", "two"], "req_str_list":["spike", "lee"],
                "opt_json":'{"ford": "green"}', "extra":"internal"}

    cls = oauth2.factory(CLASS, **_dict)
    cls.verify()
    assert _eq(cls.keys(), ['opt_str', 'req_str', 'opt_json',
                              'req_str_list', 'opt_str_list', 'opt_int'])

    _dict = {"req_str":"Fair", "opt_str":"game", "opt_int":9,
                "opt_str_list":["one", "two"], "req_str_list":["spike", "lee"]}

    cls = oauth2.factory(CLASS, **_dict)
    cls.verify()
    assert _eq(cls.keys(), ['opt_str', 'req_str', 'req_str_list',
                            'opt_str_list', 'opt_int'])

def test_grant_init():
    grant = oauth2.Grant()
    assert grant.state == ""
    assert grant.grant_expiration_time == 0
    assert grant.token_expiration_time == 0

    grant = oauth2.Grant("openid")
    assert grant.state == "openid"
    assert grant.grant_expiration_time == 0
    assert grant.token_expiration_time == 0

def test_grant_resp():
    resp = oauth2.AuthorizationResponse("code", "state")
    grant = oauth2.Grant("openid")
    grant.add_code(resp)

    assert grant.code == "code"
    assert grant.grant_expiration_time != 0
    assert grant.state == "openid"
    assert grant.token_expiration_time == 0

    grant = oauth2.Grant("openid", 1)
    grant.add_code(resp)
    time.sleep(2)

    assert grant.valid_code() == False

    grant = oauth2.Grant.from_code(resp)
    assert grant.code == "code"
    assert grant.grant_expiration_time != 0
    assert grant.state == ""
    assert grant.token_expiration_time == 0


def test_grant_access_token_1():
    resp = oauth2.AuthorizationResponse("code", "state")
    grant = oauth2.Grant("openid")
    grant.add_code(resp)

    atr = oauth2.AccessTokenResponse(
                            access_token="2YotnFZFEjr1zCsicMWpAA",
                            token_type="example",
                            expires_in=1,
                            refresh_token="tGzv3JOkF0XG5Qx2TlKWIA",
                            example_parameter="example_value",
                            xscope=["inner", "outer"])

    grant.add_token(atr)

    print grant.keys()
    assert _eq(grant.keys(), ['code', 'token_expiration_time', 'access_token',
                              'expires_in', 'token_type', 'xscope',
                              'grant_expiration_time', 'state',
                              'gexp_in', 'refresh_token',
                              'example_parameter'])

    assert grant.access_token == "2YotnFZFEjr1zCsicMWpAA"
    assert grant.token_type == "example"
    assert grant.refresh_token == "tGzv3JOkF0XG5Qx2TlKWIA"
    assert grant.example_parameter == "example_value"
    assert grant.xscope == ["inner", "outer"]
    assert grant.token_expiration_time != 0

    time.sleep(2)
    assert grant.valid_token() == False

def test_grant_access_token_2():
    resp = oauth2.AuthorizationResponse("code", "state")
    grant = oauth2.Grant("openid")
    grant.add_code(resp)

    atr = oauth2.AccessTokenResponse(
                            access_token="2YotnFZFEjr1zCsicMWpAA",
                            token_type="example",
                            refresh_token="tGzv3JOkF0XG5Qx2TlKWIA",
                            example_parameter="example_value",
                            scope=["inner", "outer"])

    grant.add_token(atr)

    assert grant.valid_token() == True
    time.sleep(2)
    assert grant.valid_token() == True

    assert "%s" % grant != ""

def test_client_get_grant():
    cli = oauth2.Client()

    resp = oauth2.AuthorizationResponse("code", "state")
    grant = oauth2.Grant("state")
    grant.add_code(resp)

    cli.grant["openid"] = grant

    gr1 = cli.grant_from_state("state")

    assert gr1.state == "state"
    assert gr1.code == "code"

    gr2 = cli.grant_from_state_or_scope("","openid")
    assert gr2.state == "state"
    assert gr2.code == "code"

    scope = cli.scope_from_state("state")
    assert scope == "openid"

    scope = cli.scope_from_state("foo")
    assert scope is None

    gr2 = cli.grant_from_state_or_scope("foo","")
    assert gr2 is None

def test_client_parse_args():
    cli = oauth2.Client()

    args = {
        "response_type":"",
        "client_id":"client_id",
        "redirect_uri":"http://example.com/authz",
        "scope":"scope",
        "state":"state",
    }
    ar_args = cli._parse_args(oauth2.AuthorizationRequest, **args)

    assert _eq(ar_args.keys(), ['scope', 'state', 'redirect_uri',
                                'response_type', 'client_id'])

def test_client_parse_extra_args():
    cli = oauth2.Client()

    args = {
        "response_type":"",
        "client_id":"client_id",
        "redirect_uri":"http://example.com/authz",
        "scope":"scope",
        "state":"state",
        "extra_session": "home"
    }
    ar_args = cli._parse_args(oauth2.AuthorizationRequest, **args)

    assert _eq(ar_args.keys(), ['scope', 'state', 'redirect_uri',
                                'response_type', 'client_id', 'session'])

def test_client_endpoint():
    cli = oauth2.Client()
    cli.authorization_endpoint = "https://example.org/oauth2/as"
    cli.token_endpoint = "https://example.org/oauth2/token"
    cli.token_revocation_endpoint = "https://example.org/oauth2/token_rev"

    ae = cli._endpoint("authorization_endpoint")
    assert ae == "https://example.org/oauth2/as"
    te = cli._endpoint("token_endpoint")
    assert te == "https://example.org/oauth2/token"
    tre = cli._endpoint("token_revocation_endpoint")
    assert tre == "https://example.org/oauth2/token_rev"

    ae = cli._endpoint("authorization_endpoint", **{
                            "authorization_endpoint": "https://example.com/as"})
    assert ae == "https://example.com/as"

    cli.token_endpoint = ""
    raises(Exception, 'cli._endpoint("token_endpoint")')
    raises(Exception, 'cli._endpoint("foo_endpoint")')


def test_server_parse_parse_authorization_request():
    srv = oauth2.Server()
    ar = oauth2.AuthorizationRequest(["code"], "foobar",
                                     "http://foobar.example.com/oaclient",
                                     state="cold")
    uencq = ar.get_urlencoded()

    areq = srv.parse_authorization_request(query=uencq)

    assert isinstance(areq, oauth2.AuthorizationRequest)
    assert areq.response_type == ["code"]
    assert areq.client_id == "foobar"
    assert areq.redirect_uri == "http://foobar.example.com/oaclient"
    assert areq.state == "cold"
    
    urluenc = "%s?%s" % ("https://example.com/authz", uencq)

    areq = srv.parse_authorization_request(url=urluenc)

    assert isinstance(areq, oauth2.AuthorizationRequest)
    assert areq.response_type == ["code"]
    assert areq.client_id == "foobar"
    assert areq.redirect_uri == "http://foobar.example.com/oaclient"
    assert areq.state == "cold"

def test_server_parse_jwt_request():
    srv = oauth2.Server()
    ar = oauth2.AuthorizationRequest(["code"], "foobar",
                                     "http://foobar.example.com/oaclient",
                                     state="cold")

    jwt = ar.get_jwt(key="A1B2C3D4", algorithm="HS256")

    req = srv.parse_jwt_request(txt=jwt, key="A1B2C3D4")

    assert isinstance(req, oauth2.AuthorizationRequest)
    assert req.response_type == ["code"]
    assert req.client_id == "foobar"
    assert req.redirect_uri == "http://foobar.example.com/oaclient"
    assert req.state == "cold"

def test_server_parse_token_request():
    atr = oauth2.AccessTokenRequest("authorization_code",
                                    "SplxlOBeZQQYbYS6WxSbIA",
                                    "https://client.example.com/cb",
                                    "client_id",
                                    extra="foo")

    uenc = atr.get_urlencoded(extended=True)

    srv = oauth2.Server()
    tr = srv.parse_token_request(body=uenc)
    print tr.keys()
    
    assert isinstance(tr, oauth2.AccessTokenRequest)
    assert _eq(tr.keys(), ['code', 'grant_type', 'client_id', 'redirect_uri'])

    assert tr.grant_type == "authorization_code"
    assert tr.code == "SplxlOBeZQQYbYS6WxSbIA"

    tr = srv.parse_token_request(body=uenc, extend=True)
    print tr.keys()

    assert isinstance(tr, oauth2.AccessTokenRequest)
    assert _eq(tr.keys(), ['code', 'grant_type', 'client_id', 'redirect_uri',
                           'extra'])

    assert tr.extra == "foo"

def test_server_parse_refresh_token_request():
    ratr = oauth2.RefreshAccessTokenRequest(refresh_token="ababababab",
                                            client_id="Client_id")

    uenc = ratr.get_urlencoded()

    srv = oauth2.Server()
    tr = srv.parse_refresh_token_request(body=uenc)
    print tr.keys()

    assert isinstance(tr, oauth2.RefreshAccessTokenRequest)
    assert tr.refresh_token == "ababababab"
    assert tr.client_id == "Client_id"

