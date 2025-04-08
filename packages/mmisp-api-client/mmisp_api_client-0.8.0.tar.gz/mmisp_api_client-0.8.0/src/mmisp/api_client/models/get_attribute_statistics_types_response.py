from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetAttributeStatisticsTypesResponse")


@_attrs_define
class GetAttributeStatisticsTypesResponse:
    """
    Attributes:
        md5 (Union[Unset, str]):
        sha1 (Union[Unset, str]):
        sha256 (Union[Unset, str]):
        filename (Union[Unset, str]):
        pdb (Union[Unset, str]):
        filenamesha1 (Union[Unset, str]):
        filenamesha256 (Union[Unset, str]):
        ip_src (Union[Unset, str]):
        ip_dst (Union[Unset, str]):
        hostname (Union[Unset, str]):
        domain (Union[Unset, str]):
        domainip (Union[Unset, str]):
        email (Union[Unset, str]):
        email_src (Union[Unset, str]):
        email_dst (Union[Unset, str]):
        email_subject (Union[Unset, str]):
        email_attachment (Union[Unset, str]):
        email_body (Union[Unset, str]):
        eppn (Union[Unset, str]):
        float_ (Union[Unset, str]):
        git_commit_id (Union[Unset, str]):
        url (Union[Unset, str]):
        http_method (Union[Unset, str]):
        user_agent (Union[Unset, str]):
        ja3_fingerprint_md5 (Union[Unset, str]):
        jarm_fingerprint (Union[Unset, str]):
        favicon_mmh3 (Union[Unset, str]):
        hassh_md5 (Union[Unset, str]):
        hasshserver_md5 (Union[Unset, str]):
        regkey (Union[Unset, str]):
        regkeyvalue (Union[Unset, str]):
        as_ (Union[Unset, str]):
        bro (Union[Unset, str]):
        zeek (Union[Unset, str]):
        community_id (Union[Unset, str]):
        pattern_in_file (Union[Unset, str]):
        aba_rtn (Union[Unset, str]):
        anonymised (Union[Unset, str]):
        attachment (Union[Unset, str]):
        authentihash (Union[Unset, str]):
        azure_application_id (Union[Unset, str]):
        bank_account_nr (Union[Unset, str]):
        bic (Union[Unset, str]):
        bin_ (Union[Unset, str]):
        boolean (Union[Unset, str]):
        btc (Union[Unset, str]):
        campaign_id (Union[Unset, str]):
        campaign_name (Union[Unset, str]):
        cc_number (Union[Unset, str]):
        cdhash (Union[Unset, str]):
        chrome_extension_id (Union[Unset, str]):
        comment (Union[Unset, str]):
        cookie (Union[Unset, str]):
        cortex (Union[Unset, str]):
        counter (Union[Unset, str]):
        country_of_residence (Union[Unset, str]):
        cpe (Union[Unset, str]):
        dash (Union[Unset, str]):
        datetime_ (Union[Unset, str]):
        date_of_birth (Union[Unset, str]):
        dkim (Union[Unset, str]):
        dkim_signature (Union[Unset, str]):
        dns_soa_email (Union[Unset, str]):
        email_dst_display_name (Union[Unset, str]):
        email_header (Union[Unset, str]):
        email_message_id (Union[Unset, str]):
        email_mime_boundary (Union[Unset, str]):
        email_reply_to (Union[Unset, str]):
        email_src_display_name (Union[Unset, str]):
        email_thread_index (Union[Unset, str]):
        email_x_mailer (Union[Unset, str]):
        filenameauthentihash (Union[Unset, str]):
        filenameimpfuzzy (Union[Unset, str]):
        filenameimphash (Union[Unset, str]):
        filenamemd5 (Union[Unset, str]):
        filename_pattern (Union[Unset, str]):
        filenamepehash (Union[Unset, str]):
        filenamesha224 (Union[Unset, str]):
        filenamesha384 (Union[Unset, str]):
        filenamesha3_224 (Union[Unset, str]):
        filenamesha3_256 (Union[Unset, str]):
        filenamesha3_384 (Union[Unset, str]):
        filenamesha3_512 (Union[Unset, str]):
        filenamesha512 (Union[Unset, str]):
        filenamesha512224 (Union[Unset, str]):
        filenamesha512256 (Union[Unset, str]):
        filenamessdeep (Union[Unset, str]):
        filenametlsh (Union[Unset, str]):
        filenamevhash (Union[Unset, str]):
        first_name (Union[Unset, str]):
        frequent_flyer_number (Union[Unset, str]):
        full_name (Union[Unset, str]):
        gender (Union[Unset, str]):
        gene (Union[Unset, str]):
        github_organisation (Union[Unset, str]):
        github_repository (Union[Unset, str]):
        github_username (Union[Unset, str]):
        hex_ (Union[Unset, str]):
        hostnameport (Union[Unset, str]):
        iban (Union[Unset, str]):
        identity_card_number (Union[Unset, str]):
        impfuzzy (Union[Unset, str]):
        imphash (Union[Unset, str]):
        integer (Union[Unset, str]):
        ip_dstport (Union[Unset, str]):
        ip_srcport (Union[Unset, str]):
        issue_date_of_the_visa (Union[Unset, str]):
        jabber_id (Union[Unset, str]):
        kusto_query (Union[Unset, str]):
        last_name (Union[Unset, str]):
        link (Union[Unset, str]):
        mac_address (Union[Unset, str]):
        mac_eui_64 (Union[Unset, str]):
        malware_sample (Union[Unset, str]):
        malware_type (Union[Unset, str]):
        middle_name (Union[Unset, str]):
        mime_type (Union[Unset, str]):
        mobile_application_id (Union[Unset, str]):
        mutex (Union[Unset, str]):
        named_pipe (Union[Unset, str]):
        nationality (Union[Unset, str]):
        other (Union[Unset, str]):
        passenger_name_record_locator_number (Union[Unset, str]):
        passport_country (Union[Unset, str]):
        passport_expiration (Union[Unset, str]):
        passport_number (Union[Unset, str]):
        pattern_in_memory (Union[Unset, str]):
        pattern_in_traffic (Union[Unset, str]):
        payment_details (Union[Unset, str]):
        pehash (Union[Unset, str]):
        pgp_private_key (Union[Unset, str]):
        pgp_public_key (Union[Unset, str]):
        phone_number (Union[Unset, str]):
        place_of_birth (Union[Unset, str]):
        place_port_of_clearance (Union[Unset, str]):
        place_port_of_onward_foreign_destination (Union[Unset, str]):
        place_port_of_original_embarkation (Union[Unset, str]):
        port (Union[Unset, str]):
        primary_residence (Union[Unset, str]):
        process_state (Union[Unset, str]):
        prtn (Union[Unset, str]):
        redress_number (Union[Unset, str]):
        sha224 (Union[Unset, str]):
        sha384 (Union[Unset, str]):
        sha3_224 (Union[Unset, str]):
        sha3_256 (Union[Unset, str]):
        sha3_384 (Union[Unset, str]):
        sha3_512 (Union[Unset, str]):
        sha512 (Union[Unset, str]):
        sha512224 (Union[Unset, str]):
        sha512256 (Union[Unset, str]):
        sigma (Union[Unset, str]):
        size_in_bytes (Union[Unset, str]):
        snort (Union[Unset, str]):
        special_service_request (Union[Unset, str]):
        ssdeep (Union[Unset, str]):
        ssh_fingerprint (Union[Unset, str]):
        stix2_pattern (Union[Unset, str]):
        target_email (Union[Unset, str]):
        target_external (Union[Unset, str]):
        target_location (Union[Unset, str]):
        target_machine (Union[Unset, str]):
        target_org (Union[Unset, str]):
        target_user (Union[Unset, str]):
        telfhash (Union[Unset, str]):
        text (Union[Unset, str]):
        threat_actor (Union[Unset, str]):
        tlsh (Union[Unset, str]):
        travel_details (Union[Unset, str]):
        twitter_id (Union[Unset, str]):
        uri (Union[Unset, str]):
        vhash (Union[Unset, str]):
        visa_number (Union[Unset, str]):
        vulnerability (Union[Unset, str]):
        weakness (Union[Unset, str]):
        whois_creation_date (Union[Unset, str]):
        whois_registrant_email (Union[Unset, str]):
        whois_registrant_name (Union[Unset, str]):
        whois_registrant_org (Union[Unset, str]):
        whois_registrant_phone (Union[Unset, str]):
        whois_registrar (Union[Unset, str]):
        windows_scheduled_task (Union[Unset, str]):
        windows_service_displayname (Union[Unset, str]):
        windows_service_name (Union[Unset, str]):
        x509_fingerprint_md5 (Union[Unset, str]):
        x509_fingerprint_sha1 (Union[Unset, str]):
        x509_fingerprint_sha256 (Union[Unset, str]):
        xmr (Union[Unset, str]):
        yara (Union[Unset, str]):
        dom_hash (Union[Unset, str]):
        onion_address (Union[Unset, str]):
    """

    md5: Union[Unset, str] = UNSET
    sha1: Union[Unset, str] = UNSET
    sha256: Union[Unset, str] = UNSET
    filename: Union[Unset, str] = UNSET
    pdb: Union[Unset, str] = UNSET
    filenamesha1: Union[Unset, str] = UNSET
    filenamesha256: Union[Unset, str] = UNSET
    ip_src: Union[Unset, str] = UNSET
    ip_dst: Union[Unset, str] = UNSET
    hostname: Union[Unset, str] = UNSET
    domain: Union[Unset, str] = UNSET
    domainip: Union[Unset, str] = UNSET
    email: Union[Unset, str] = UNSET
    email_src: Union[Unset, str] = UNSET
    email_dst: Union[Unset, str] = UNSET
    email_subject: Union[Unset, str] = UNSET
    email_attachment: Union[Unset, str] = UNSET
    email_body: Union[Unset, str] = UNSET
    eppn: Union[Unset, str] = UNSET
    float_: Union[Unset, str] = UNSET
    git_commit_id: Union[Unset, str] = UNSET
    url: Union[Unset, str] = UNSET
    http_method: Union[Unset, str] = UNSET
    user_agent: Union[Unset, str] = UNSET
    ja3_fingerprint_md5: Union[Unset, str] = UNSET
    jarm_fingerprint: Union[Unset, str] = UNSET
    favicon_mmh3: Union[Unset, str] = UNSET
    hassh_md5: Union[Unset, str] = UNSET
    hasshserver_md5: Union[Unset, str] = UNSET
    regkey: Union[Unset, str] = UNSET
    regkeyvalue: Union[Unset, str] = UNSET
    as_: Union[Unset, str] = UNSET
    bro: Union[Unset, str] = UNSET
    zeek: Union[Unset, str] = UNSET
    community_id: Union[Unset, str] = UNSET
    pattern_in_file: Union[Unset, str] = UNSET
    aba_rtn: Union[Unset, str] = UNSET
    anonymised: Union[Unset, str] = UNSET
    attachment: Union[Unset, str] = UNSET
    authentihash: Union[Unset, str] = UNSET
    azure_application_id: Union[Unset, str] = UNSET
    bank_account_nr: Union[Unset, str] = UNSET
    bic: Union[Unset, str] = UNSET
    bin_: Union[Unset, str] = UNSET
    boolean: Union[Unset, str] = UNSET
    btc: Union[Unset, str] = UNSET
    campaign_id: Union[Unset, str] = UNSET
    campaign_name: Union[Unset, str] = UNSET
    cc_number: Union[Unset, str] = UNSET
    cdhash: Union[Unset, str] = UNSET
    chrome_extension_id: Union[Unset, str] = UNSET
    comment: Union[Unset, str] = UNSET
    cookie: Union[Unset, str] = UNSET
    cortex: Union[Unset, str] = UNSET
    counter: Union[Unset, str] = UNSET
    country_of_residence: Union[Unset, str] = UNSET
    cpe: Union[Unset, str] = UNSET
    dash: Union[Unset, str] = UNSET
    datetime_: Union[Unset, str] = UNSET
    date_of_birth: Union[Unset, str] = UNSET
    dkim: Union[Unset, str] = UNSET
    dkim_signature: Union[Unset, str] = UNSET
    dns_soa_email: Union[Unset, str] = UNSET
    email_dst_display_name: Union[Unset, str] = UNSET
    email_header: Union[Unset, str] = UNSET
    email_message_id: Union[Unset, str] = UNSET
    email_mime_boundary: Union[Unset, str] = UNSET
    email_reply_to: Union[Unset, str] = UNSET
    email_src_display_name: Union[Unset, str] = UNSET
    email_thread_index: Union[Unset, str] = UNSET
    email_x_mailer: Union[Unset, str] = UNSET
    filenameauthentihash: Union[Unset, str] = UNSET
    filenameimpfuzzy: Union[Unset, str] = UNSET
    filenameimphash: Union[Unset, str] = UNSET
    filenamemd5: Union[Unset, str] = UNSET
    filename_pattern: Union[Unset, str] = UNSET
    filenamepehash: Union[Unset, str] = UNSET
    filenamesha224: Union[Unset, str] = UNSET
    filenamesha384: Union[Unset, str] = UNSET
    filenamesha3_224: Union[Unset, str] = UNSET
    filenamesha3_256: Union[Unset, str] = UNSET
    filenamesha3_384: Union[Unset, str] = UNSET
    filenamesha3_512: Union[Unset, str] = UNSET
    filenamesha512: Union[Unset, str] = UNSET
    filenamesha512224: Union[Unset, str] = UNSET
    filenamesha512256: Union[Unset, str] = UNSET
    filenamessdeep: Union[Unset, str] = UNSET
    filenametlsh: Union[Unset, str] = UNSET
    filenamevhash: Union[Unset, str] = UNSET
    first_name: Union[Unset, str] = UNSET
    frequent_flyer_number: Union[Unset, str] = UNSET
    full_name: Union[Unset, str] = UNSET
    gender: Union[Unset, str] = UNSET
    gene: Union[Unset, str] = UNSET
    github_organisation: Union[Unset, str] = UNSET
    github_repository: Union[Unset, str] = UNSET
    github_username: Union[Unset, str] = UNSET
    hex_: Union[Unset, str] = UNSET
    hostnameport: Union[Unset, str] = UNSET
    iban: Union[Unset, str] = UNSET
    identity_card_number: Union[Unset, str] = UNSET
    impfuzzy: Union[Unset, str] = UNSET
    imphash: Union[Unset, str] = UNSET
    integer: Union[Unset, str] = UNSET
    ip_dstport: Union[Unset, str] = UNSET
    ip_srcport: Union[Unset, str] = UNSET
    issue_date_of_the_visa: Union[Unset, str] = UNSET
    jabber_id: Union[Unset, str] = UNSET
    kusto_query: Union[Unset, str] = UNSET
    last_name: Union[Unset, str] = UNSET
    link: Union[Unset, str] = UNSET
    mac_address: Union[Unset, str] = UNSET
    mac_eui_64: Union[Unset, str] = UNSET
    malware_sample: Union[Unset, str] = UNSET
    malware_type: Union[Unset, str] = UNSET
    middle_name: Union[Unset, str] = UNSET
    mime_type: Union[Unset, str] = UNSET
    mobile_application_id: Union[Unset, str] = UNSET
    mutex: Union[Unset, str] = UNSET
    named_pipe: Union[Unset, str] = UNSET
    nationality: Union[Unset, str] = UNSET
    other: Union[Unset, str] = UNSET
    passenger_name_record_locator_number: Union[Unset, str] = UNSET
    passport_country: Union[Unset, str] = UNSET
    passport_expiration: Union[Unset, str] = UNSET
    passport_number: Union[Unset, str] = UNSET
    pattern_in_memory: Union[Unset, str] = UNSET
    pattern_in_traffic: Union[Unset, str] = UNSET
    payment_details: Union[Unset, str] = UNSET
    pehash: Union[Unset, str] = UNSET
    pgp_private_key: Union[Unset, str] = UNSET
    pgp_public_key: Union[Unset, str] = UNSET
    phone_number: Union[Unset, str] = UNSET
    place_of_birth: Union[Unset, str] = UNSET
    place_port_of_clearance: Union[Unset, str] = UNSET
    place_port_of_onward_foreign_destination: Union[Unset, str] = UNSET
    place_port_of_original_embarkation: Union[Unset, str] = UNSET
    port: Union[Unset, str] = UNSET
    primary_residence: Union[Unset, str] = UNSET
    process_state: Union[Unset, str] = UNSET
    prtn: Union[Unset, str] = UNSET
    redress_number: Union[Unset, str] = UNSET
    sha224: Union[Unset, str] = UNSET
    sha384: Union[Unset, str] = UNSET
    sha3_224: Union[Unset, str] = UNSET
    sha3_256: Union[Unset, str] = UNSET
    sha3_384: Union[Unset, str] = UNSET
    sha3_512: Union[Unset, str] = UNSET
    sha512: Union[Unset, str] = UNSET
    sha512224: Union[Unset, str] = UNSET
    sha512256: Union[Unset, str] = UNSET
    sigma: Union[Unset, str] = UNSET
    size_in_bytes: Union[Unset, str] = UNSET
    snort: Union[Unset, str] = UNSET
    special_service_request: Union[Unset, str] = UNSET
    ssdeep: Union[Unset, str] = UNSET
    ssh_fingerprint: Union[Unset, str] = UNSET
    stix2_pattern: Union[Unset, str] = UNSET
    target_email: Union[Unset, str] = UNSET
    target_external: Union[Unset, str] = UNSET
    target_location: Union[Unset, str] = UNSET
    target_machine: Union[Unset, str] = UNSET
    target_org: Union[Unset, str] = UNSET
    target_user: Union[Unset, str] = UNSET
    telfhash: Union[Unset, str] = UNSET
    text: Union[Unset, str] = UNSET
    threat_actor: Union[Unset, str] = UNSET
    tlsh: Union[Unset, str] = UNSET
    travel_details: Union[Unset, str] = UNSET
    twitter_id: Union[Unset, str] = UNSET
    uri: Union[Unset, str] = UNSET
    vhash: Union[Unset, str] = UNSET
    visa_number: Union[Unset, str] = UNSET
    vulnerability: Union[Unset, str] = UNSET
    weakness: Union[Unset, str] = UNSET
    whois_creation_date: Union[Unset, str] = UNSET
    whois_registrant_email: Union[Unset, str] = UNSET
    whois_registrant_name: Union[Unset, str] = UNSET
    whois_registrant_org: Union[Unset, str] = UNSET
    whois_registrant_phone: Union[Unset, str] = UNSET
    whois_registrar: Union[Unset, str] = UNSET
    windows_scheduled_task: Union[Unset, str] = UNSET
    windows_service_displayname: Union[Unset, str] = UNSET
    windows_service_name: Union[Unset, str] = UNSET
    x509_fingerprint_md5: Union[Unset, str] = UNSET
    x509_fingerprint_sha1: Union[Unset, str] = UNSET
    x509_fingerprint_sha256: Union[Unset, str] = UNSET
    xmr: Union[Unset, str] = UNSET
    yara: Union[Unset, str] = UNSET
    dom_hash: Union[Unset, str] = UNSET
    onion_address: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        md5 = self.md5

        sha1 = self.sha1

        sha256 = self.sha256

        filename = self.filename

        pdb = self.pdb

        filenamesha1 = self.filenamesha1

        filenamesha256 = self.filenamesha256

        ip_src = self.ip_src

        ip_dst = self.ip_dst

        hostname = self.hostname

        domain = self.domain

        domainip = self.domainip

        email = self.email

        email_src = self.email_src

        email_dst = self.email_dst

        email_subject = self.email_subject

        email_attachment = self.email_attachment

        email_body = self.email_body

        eppn = self.eppn

        float_ = self.float_

        git_commit_id = self.git_commit_id

        url = self.url

        http_method = self.http_method

        user_agent = self.user_agent

        ja3_fingerprint_md5 = self.ja3_fingerprint_md5

        jarm_fingerprint = self.jarm_fingerprint

        favicon_mmh3 = self.favicon_mmh3

        hassh_md5 = self.hassh_md5

        hasshserver_md5 = self.hasshserver_md5

        regkey = self.regkey

        regkeyvalue = self.regkeyvalue

        as_ = self.as_

        bro = self.bro

        zeek = self.zeek

        community_id = self.community_id

        pattern_in_file = self.pattern_in_file

        aba_rtn = self.aba_rtn

        anonymised = self.anonymised

        attachment = self.attachment

        authentihash = self.authentihash

        azure_application_id = self.azure_application_id

        bank_account_nr = self.bank_account_nr

        bic = self.bic

        bin_ = self.bin_

        boolean = self.boolean

        btc = self.btc

        campaign_id = self.campaign_id

        campaign_name = self.campaign_name

        cc_number = self.cc_number

        cdhash = self.cdhash

        chrome_extension_id = self.chrome_extension_id

        comment = self.comment

        cookie = self.cookie

        cortex = self.cortex

        counter = self.counter

        country_of_residence = self.country_of_residence

        cpe = self.cpe

        dash = self.dash

        datetime_ = self.datetime_

        date_of_birth = self.date_of_birth

        dkim = self.dkim

        dkim_signature = self.dkim_signature

        dns_soa_email = self.dns_soa_email

        email_dst_display_name = self.email_dst_display_name

        email_header = self.email_header

        email_message_id = self.email_message_id

        email_mime_boundary = self.email_mime_boundary

        email_reply_to = self.email_reply_to

        email_src_display_name = self.email_src_display_name

        email_thread_index = self.email_thread_index

        email_x_mailer = self.email_x_mailer

        filenameauthentihash = self.filenameauthentihash

        filenameimpfuzzy = self.filenameimpfuzzy

        filenameimphash = self.filenameimphash

        filenamemd5 = self.filenamemd5

        filename_pattern = self.filename_pattern

        filenamepehash = self.filenamepehash

        filenamesha224 = self.filenamesha224

        filenamesha384 = self.filenamesha384

        filenamesha3_224 = self.filenamesha3_224

        filenamesha3_256 = self.filenamesha3_256

        filenamesha3_384 = self.filenamesha3_384

        filenamesha3_512 = self.filenamesha3_512

        filenamesha512 = self.filenamesha512

        filenamesha512224 = self.filenamesha512224

        filenamesha512256 = self.filenamesha512256

        filenamessdeep = self.filenamessdeep

        filenametlsh = self.filenametlsh

        filenamevhash = self.filenamevhash

        first_name = self.first_name

        frequent_flyer_number = self.frequent_flyer_number

        full_name = self.full_name

        gender = self.gender

        gene = self.gene

        github_organisation = self.github_organisation

        github_repository = self.github_repository

        github_username = self.github_username

        hex_ = self.hex_

        hostnameport = self.hostnameport

        iban = self.iban

        identity_card_number = self.identity_card_number

        impfuzzy = self.impfuzzy

        imphash = self.imphash

        integer = self.integer

        ip_dstport = self.ip_dstport

        ip_srcport = self.ip_srcport

        issue_date_of_the_visa = self.issue_date_of_the_visa

        jabber_id = self.jabber_id

        kusto_query = self.kusto_query

        last_name = self.last_name

        link = self.link

        mac_address = self.mac_address

        mac_eui_64 = self.mac_eui_64

        malware_sample = self.malware_sample

        malware_type = self.malware_type

        middle_name = self.middle_name

        mime_type = self.mime_type

        mobile_application_id = self.mobile_application_id

        mutex = self.mutex

        named_pipe = self.named_pipe

        nationality = self.nationality

        other = self.other

        passenger_name_record_locator_number = self.passenger_name_record_locator_number

        passport_country = self.passport_country

        passport_expiration = self.passport_expiration

        passport_number = self.passport_number

        pattern_in_memory = self.pattern_in_memory

        pattern_in_traffic = self.pattern_in_traffic

        payment_details = self.payment_details

        pehash = self.pehash

        pgp_private_key = self.pgp_private_key

        pgp_public_key = self.pgp_public_key

        phone_number = self.phone_number

        place_of_birth = self.place_of_birth

        place_port_of_clearance = self.place_port_of_clearance

        place_port_of_onward_foreign_destination = self.place_port_of_onward_foreign_destination

        place_port_of_original_embarkation = self.place_port_of_original_embarkation

        port = self.port

        primary_residence = self.primary_residence

        process_state = self.process_state

        prtn = self.prtn

        redress_number = self.redress_number

        sha224 = self.sha224

        sha384 = self.sha384

        sha3_224 = self.sha3_224

        sha3_256 = self.sha3_256

        sha3_384 = self.sha3_384

        sha3_512 = self.sha3_512

        sha512 = self.sha512

        sha512224 = self.sha512224

        sha512256 = self.sha512256

        sigma = self.sigma

        size_in_bytes = self.size_in_bytes

        snort = self.snort

        special_service_request = self.special_service_request

        ssdeep = self.ssdeep

        ssh_fingerprint = self.ssh_fingerprint

        stix2_pattern = self.stix2_pattern

        target_email = self.target_email

        target_external = self.target_external

        target_location = self.target_location

        target_machine = self.target_machine

        target_org = self.target_org

        target_user = self.target_user

        telfhash = self.telfhash

        text = self.text

        threat_actor = self.threat_actor

        tlsh = self.tlsh

        travel_details = self.travel_details

        twitter_id = self.twitter_id

        uri = self.uri

        vhash = self.vhash

        visa_number = self.visa_number

        vulnerability = self.vulnerability

        weakness = self.weakness

        whois_creation_date = self.whois_creation_date

        whois_registrant_email = self.whois_registrant_email

        whois_registrant_name = self.whois_registrant_name

        whois_registrant_org = self.whois_registrant_org

        whois_registrant_phone = self.whois_registrant_phone

        whois_registrar = self.whois_registrar

        windows_scheduled_task = self.windows_scheduled_task

        windows_service_displayname = self.windows_service_displayname

        windows_service_name = self.windows_service_name

        x509_fingerprint_md5 = self.x509_fingerprint_md5

        x509_fingerprint_sha1 = self.x509_fingerprint_sha1

        x509_fingerprint_sha256 = self.x509_fingerprint_sha256

        xmr = self.xmr

        yara = self.yara

        dom_hash = self.dom_hash

        onion_address = self.onion_address

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if md5 is not UNSET:
            field_dict["md5"] = md5
        if sha1 is not UNSET:
            field_dict["sha1"] = sha1
        if sha256 is not UNSET:
            field_dict["sha256"] = sha256
        if filename is not UNSET:
            field_dict["filename"] = filename
        if pdb is not UNSET:
            field_dict["pdb"] = pdb
        if filenamesha1 is not UNSET:
            field_dict["filename|sha1"] = filenamesha1
        if filenamesha256 is not UNSET:
            field_dict["filename|sha256"] = filenamesha256
        if ip_src is not UNSET:
            field_dict["ip-src"] = ip_src
        if ip_dst is not UNSET:
            field_dict["ip-dst"] = ip_dst
        if hostname is not UNSET:
            field_dict["hostname"] = hostname
        if domain is not UNSET:
            field_dict["domain"] = domain
        if domainip is not UNSET:
            field_dict["domain|ip"] = domainip
        if email is not UNSET:
            field_dict["email"] = email
        if email_src is not UNSET:
            field_dict["email-src"] = email_src
        if email_dst is not UNSET:
            field_dict["email-dst"] = email_dst
        if email_subject is not UNSET:
            field_dict["email-subject"] = email_subject
        if email_attachment is not UNSET:
            field_dict["email-attachment"] = email_attachment
        if email_body is not UNSET:
            field_dict["email-body"] = email_body
        if eppn is not UNSET:
            field_dict["eppn"] = eppn
        if float_ is not UNSET:
            field_dict["float"] = float_
        if git_commit_id is not UNSET:
            field_dict["git-commit-id"] = git_commit_id
        if url is not UNSET:
            field_dict["url"] = url
        if http_method is not UNSET:
            field_dict["http-method"] = http_method
        if user_agent is not UNSET:
            field_dict["user-agent"] = user_agent
        if ja3_fingerprint_md5 is not UNSET:
            field_dict["ja3-fingerprint-md5"] = ja3_fingerprint_md5
        if jarm_fingerprint is not UNSET:
            field_dict["jarm-fingerprint"] = jarm_fingerprint
        if favicon_mmh3 is not UNSET:
            field_dict["favicon-mmh3"] = favicon_mmh3
        if hassh_md5 is not UNSET:
            field_dict["hassh-md5"] = hassh_md5
        if hasshserver_md5 is not UNSET:
            field_dict["hasshserver-md5"] = hasshserver_md5
        if regkey is not UNSET:
            field_dict["regkey"] = regkey
        if regkeyvalue is not UNSET:
            field_dict["regkey|value"] = regkeyvalue
        if as_ is not UNSET:
            field_dict["AS"] = as_
        if bro is not UNSET:
            field_dict["bro"] = bro
        if zeek is not UNSET:
            field_dict["zeek"] = zeek
        if community_id is not UNSET:
            field_dict["community-id"] = community_id
        if pattern_in_file is not UNSET:
            field_dict["pattern-in-file"] = pattern_in_file
        if aba_rtn is not UNSET:
            field_dict["aba-rtn"] = aba_rtn
        if anonymised is not UNSET:
            field_dict["anonymised"] = anonymised
        if attachment is not UNSET:
            field_dict["attachment"] = attachment
        if authentihash is not UNSET:
            field_dict["authentihash"] = authentihash
        if azure_application_id is not UNSET:
            field_dict["azure-application-id"] = azure_application_id
        if bank_account_nr is not UNSET:
            field_dict["bank-account-nr"] = bank_account_nr
        if bic is not UNSET:
            field_dict["bic"] = bic
        if bin_ is not UNSET:
            field_dict["bin"] = bin_
        if boolean is not UNSET:
            field_dict["boolean"] = boolean
        if btc is not UNSET:
            field_dict["btc"] = btc
        if campaign_id is not UNSET:
            field_dict["campaign-id"] = campaign_id
        if campaign_name is not UNSET:
            field_dict["campaign-name"] = campaign_name
        if cc_number is not UNSET:
            field_dict["cc-number"] = cc_number
        if cdhash is not UNSET:
            field_dict["cdhash"] = cdhash
        if chrome_extension_id is not UNSET:
            field_dict["chrome-extension-id"] = chrome_extension_id
        if comment is not UNSET:
            field_dict["comment"] = comment
        if cookie is not UNSET:
            field_dict["cookie"] = cookie
        if cortex is not UNSET:
            field_dict["cortex"] = cortex
        if counter is not UNSET:
            field_dict["counter"] = counter
        if country_of_residence is not UNSET:
            field_dict["country-of-residence"] = country_of_residence
        if cpe is not UNSET:
            field_dict["cpe"] = cpe
        if dash is not UNSET:
            field_dict["dash"] = dash
        if datetime_ is not UNSET:
            field_dict["datetime"] = datetime_
        if date_of_birth is not UNSET:
            field_dict["date-of-birth"] = date_of_birth
        if dkim is not UNSET:
            field_dict["dkim"] = dkim
        if dkim_signature is not UNSET:
            field_dict["dkim-signature"] = dkim_signature
        if dns_soa_email is not UNSET:
            field_dict["dns-soa-email"] = dns_soa_email
        if email_dst_display_name is not UNSET:
            field_dict["email-dst-display-name"] = email_dst_display_name
        if email_header is not UNSET:
            field_dict["email-header"] = email_header
        if email_message_id is not UNSET:
            field_dict["email-message-id"] = email_message_id
        if email_mime_boundary is not UNSET:
            field_dict["email-mime-boundary"] = email_mime_boundary
        if email_reply_to is not UNSET:
            field_dict["email-reply-to"] = email_reply_to
        if email_src_display_name is not UNSET:
            field_dict["email-src-display-name"] = email_src_display_name
        if email_thread_index is not UNSET:
            field_dict["email-thread-index"] = email_thread_index
        if email_x_mailer is not UNSET:
            field_dict["email-x-mailer"] = email_x_mailer
        if filenameauthentihash is not UNSET:
            field_dict["filename|authentihash"] = filenameauthentihash
        if filenameimpfuzzy is not UNSET:
            field_dict["filename|impfuzzy"] = filenameimpfuzzy
        if filenameimphash is not UNSET:
            field_dict["filename|imphash"] = filenameimphash
        if filenamemd5 is not UNSET:
            field_dict["filename|md5"] = filenamemd5
        if filename_pattern is not UNSET:
            field_dict["filename-pattern"] = filename_pattern
        if filenamepehash is not UNSET:
            field_dict["filename|pehash"] = filenamepehash
        if filenamesha224 is not UNSET:
            field_dict["filename|sha224"] = filenamesha224
        if filenamesha384 is not UNSET:
            field_dict["filename|sha384"] = filenamesha384
        if filenamesha3_224 is not UNSET:
            field_dict["filename|sha3-224"] = filenamesha3_224
        if filenamesha3_256 is not UNSET:
            field_dict["filename|sha3-256"] = filenamesha3_256
        if filenamesha3_384 is not UNSET:
            field_dict["filename|sha3-384"] = filenamesha3_384
        if filenamesha3_512 is not UNSET:
            field_dict["filename|sha3-512"] = filenamesha3_512
        if filenamesha512 is not UNSET:
            field_dict["filename|sha512"] = filenamesha512
        if filenamesha512224 is not UNSET:
            field_dict["filename|sha512/224"] = filenamesha512224
        if filenamesha512256 is not UNSET:
            field_dict["filename|sha512/256"] = filenamesha512256
        if filenamessdeep is not UNSET:
            field_dict["filename|ssdeep"] = filenamessdeep
        if filenametlsh is not UNSET:
            field_dict["filename|tlsh"] = filenametlsh
        if filenamevhash is not UNSET:
            field_dict["filename|vhash"] = filenamevhash
        if first_name is not UNSET:
            field_dict["first-name"] = first_name
        if frequent_flyer_number is not UNSET:
            field_dict["frequent-flyer-number"] = frequent_flyer_number
        if full_name is not UNSET:
            field_dict["full-name"] = full_name
        if gender is not UNSET:
            field_dict["gender"] = gender
        if gene is not UNSET:
            field_dict["gene"] = gene
        if github_organisation is not UNSET:
            field_dict["github-organisation"] = github_organisation
        if github_repository is not UNSET:
            field_dict["github-repository"] = github_repository
        if github_username is not UNSET:
            field_dict["github-username"] = github_username
        if hex_ is not UNSET:
            field_dict["hex"] = hex_
        if hostnameport is not UNSET:
            field_dict["hostname|port"] = hostnameport
        if iban is not UNSET:
            field_dict["iban"] = iban
        if identity_card_number is not UNSET:
            field_dict["identity-card-number"] = identity_card_number
        if impfuzzy is not UNSET:
            field_dict["impfuzzy"] = impfuzzy
        if imphash is not UNSET:
            field_dict["imphash"] = imphash
        if integer is not UNSET:
            field_dict["integer"] = integer
        if ip_dstport is not UNSET:
            field_dict["ip-dst|port"] = ip_dstport
        if ip_srcport is not UNSET:
            field_dict["ip-src|port"] = ip_srcport
        if issue_date_of_the_visa is not UNSET:
            field_dict["issue-date-of-the-visa"] = issue_date_of_the_visa
        if jabber_id is not UNSET:
            field_dict["jabber-id"] = jabber_id
        if kusto_query is not UNSET:
            field_dict["kusto-query"] = kusto_query
        if last_name is not UNSET:
            field_dict["last-name"] = last_name
        if link is not UNSET:
            field_dict["link"] = link
        if mac_address is not UNSET:
            field_dict["mac-address"] = mac_address
        if mac_eui_64 is not UNSET:
            field_dict["mac-eui-64"] = mac_eui_64
        if malware_sample is not UNSET:
            field_dict["malware-sample"] = malware_sample
        if malware_type is not UNSET:
            field_dict["malware-type"] = malware_type
        if middle_name is not UNSET:
            field_dict["middle-name"] = middle_name
        if mime_type is not UNSET:
            field_dict["mime-type"] = mime_type
        if mobile_application_id is not UNSET:
            field_dict["mobile-application-id"] = mobile_application_id
        if mutex is not UNSET:
            field_dict["mutex"] = mutex
        if named_pipe is not UNSET:
            field_dict["named pipe"] = named_pipe
        if nationality is not UNSET:
            field_dict["nationality"] = nationality
        if other is not UNSET:
            field_dict["other"] = other
        if passenger_name_record_locator_number is not UNSET:
            field_dict["passenger-name-record-locator-number"] = passenger_name_record_locator_number
        if passport_country is not UNSET:
            field_dict["passport-country"] = passport_country
        if passport_expiration is not UNSET:
            field_dict["passport-expiration"] = passport_expiration
        if passport_number is not UNSET:
            field_dict["passport-number"] = passport_number
        if pattern_in_memory is not UNSET:
            field_dict["pattern-in-memory"] = pattern_in_memory
        if pattern_in_traffic is not UNSET:
            field_dict["pattern-in-traffic"] = pattern_in_traffic
        if payment_details is not UNSET:
            field_dict["payment-details"] = payment_details
        if pehash is not UNSET:
            field_dict["pehash"] = pehash
        if pgp_private_key is not UNSET:
            field_dict["pgp-private-key"] = pgp_private_key
        if pgp_public_key is not UNSET:
            field_dict["pgp-public-key"] = pgp_public_key
        if phone_number is not UNSET:
            field_dict["phone-number"] = phone_number
        if place_of_birth is not UNSET:
            field_dict["place-of-birth"] = place_of_birth
        if place_port_of_clearance is not UNSET:
            field_dict["place-port-of-clearance"] = place_port_of_clearance
        if place_port_of_onward_foreign_destination is not UNSET:
            field_dict["place-port-of-onward-foreign-destination"] = place_port_of_onward_foreign_destination
        if place_port_of_original_embarkation is not UNSET:
            field_dict["place-port-of-original-embarkation"] = place_port_of_original_embarkation
        if port is not UNSET:
            field_dict["port"] = port
        if primary_residence is not UNSET:
            field_dict["primary-residence"] = primary_residence
        if process_state is not UNSET:
            field_dict["process-state"] = process_state
        if prtn is not UNSET:
            field_dict["prtn"] = prtn
        if redress_number is not UNSET:
            field_dict["redress-number"] = redress_number
        if sha224 is not UNSET:
            field_dict["sha224"] = sha224
        if sha384 is not UNSET:
            field_dict["sha384"] = sha384
        if sha3_224 is not UNSET:
            field_dict["sha3-224"] = sha3_224
        if sha3_256 is not UNSET:
            field_dict["sha3-256"] = sha3_256
        if sha3_384 is not UNSET:
            field_dict["sha3-384"] = sha3_384
        if sha3_512 is not UNSET:
            field_dict["sha3-512"] = sha3_512
        if sha512 is not UNSET:
            field_dict["sha512"] = sha512
        if sha512224 is not UNSET:
            field_dict["sha512/224"] = sha512224
        if sha512256 is not UNSET:
            field_dict["sha512/256"] = sha512256
        if sigma is not UNSET:
            field_dict["sigma"] = sigma
        if size_in_bytes is not UNSET:
            field_dict["size-in-bytes"] = size_in_bytes
        if snort is not UNSET:
            field_dict["snort"] = snort
        if special_service_request is not UNSET:
            field_dict["special-service-request"] = special_service_request
        if ssdeep is not UNSET:
            field_dict["ssdeep"] = ssdeep
        if ssh_fingerprint is not UNSET:
            field_dict["ssh-fingerprint"] = ssh_fingerprint
        if stix2_pattern is not UNSET:
            field_dict["stix2-pattern"] = stix2_pattern
        if target_email is not UNSET:
            field_dict["target-email"] = target_email
        if target_external is not UNSET:
            field_dict["target-external"] = target_external
        if target_location is not UNSET:
            field_dict["target-location"] = target_location
        if target_machine is not UNSET:
            field_dict["target-machine"] = target_machine
        if target_org is not UNSET:
            field_dict["target-org"] = target_org
        if target_user is not UNSET:
            field_dict["target-user"] = target_user
        if telfhash is not UNSET:
            field_dict["telfhash"] = telfhash
        if text is not UNSET:
            field_dict["text"] = text
        if threat_actor is not UNSET:
            field_dict["threat-actor"] = threat_actor
        if tlsh is not UNSET:
            field_dict["tlsh"] = tlsh
        if travel_details is not UNSET:
            field_dict["travel-details"] = travel_details
        if twitter_id is not UNSET:
            field_dict["twitter-id"] = twitter_id
        if uri is not UNSET:
            field_dict["uri"] = uri
        if vhash is not UNSET:
            field_dict["vhash"] = vhash
        if visa_number is not UNSET:
            field_dict["visa-number"] = visa_number
        if vulnerability is not UNSET:
            field_dict["vulnerability"] = vulnerability
        if weakness is not UNSET:
            field_dict["weakness"] = weakness
        if whois_creation_date is not UNSET:
            field_dict["whois-creation-date"] = whois_creation_date
        if whois_registrant_email is not UNSET:
            field_dict["whois-registrant-email"] = whois_registrant_email
        if whois_registrant_name is not UNSET:
            field_dict["whois-registrant-name"] = whois_registrant_name
        if whois_registrant_org is not UNSET:
            field_dict["whois-registrant-org"] = whois_registrant_org
        if whois_registrant_phone is not UNSET:
            field_dict["whois-registrant-phone"] = whois_registrant_phone
        if whois_registrar is not UNSET:
            field_dict["whois-registrar"] = whois_registrar
        if windows_scheduled_task is not UNSET:
            field_dict["windows-scheduled-task"] = windows_scheduled_task
        if windows_service_displayname is not UNSET:
            field_dict["windows-service-displayname"] = windows_service_displayname
        if windows_service_name is not UNSET:
            field_dict["windows-service-name"] = windows_service_name
        if x509_fingerprint_md5 is not UNSET:
            field_dict["x509-fingerprint-md5"] = x509_fingerprint_md5
        if x509_fingerprint_sha1 is not UNSET:
            field_dict["x509-fingerprint-sha1"] = x509_fingerprint_sha1
        if x509_fingerprint_sha256 is not UNSET:
            field_dict["x509-fingerprint-sha256"] = x509_fingerprint_sha256
        if xmr is not UNSET:
            field_dict["xmr"] = xmr
        if yara is not UNSET:
            field_dict["yara"] = yara
        if dom_hash is not UNSET:
            field_dict["dom-hash"] = dom_hash
        if onion_address is not UNSET:
            field_dict["onion-address"] = onion_address

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        md5 = d.pop("md5", UNSET)

        sha1 = d.pop("sha1", UNSET)

        sha256 = d.pop("sha256", UNSET)

        filename = d.pop("filename", UNSET)

        pdb = d.pop("pdb", UNSET)

        filenamesha1 = d.pop("filename|sha1", UNSET)

        filenamesha256 = d.pop("filename|sha256", UNSET)

        ip_src = d.pop("ip-src", UNSET)

        ip_dst = d.pop("ip-dst", UNSET)

        hostname = d.pop("hostname", UNSET)

        domain = d.pop("domain", UNSET)

        domainip = d.pop("domain|ip", UNSET)

        email = d.pop("email", UNSET)

        email_src = d.pop("email-src", UNSET)

        email_dst = d.pop("email-dst", UNSET)

        email_subject = d.pop("email-subject", UNSET)

        email_attachment = d.pop("email-attachment", UNSET)

        email_body = d.pop("email-body", UNSET)

        eppn = d.pop("eppn", UNSET)

        float_ = d.pop("float", UNSET)

        git_commit_id = d.pop("git-commit-id", UNSET)

        url = d.pop("url", UNSET)

        http_method = d.pop("http-method", UNSET)

        user_agent = d.pop("user-agent", UNSET)

        ja3_fingerprint_md5 = d.pop("ja3-fingerprint-md5", UNSET)

        jarm_fingerprint = d.pop("jarm-fingerprint", UNSET)

        favicon_mmh3 = d.pop("favicon-mmh3", UNSET)

        hassh_md5 = d.pop("hassh-md5", UNSET)

        hasshserver_md5 = d.pop("hasshserver-md5", UNSET)

        regkey = d.pop("regkey", UNSET)

        regkeyvalue = d.pop("regkey|value", UNSET)

        as_ = d.pop("AS", UNSET)

        bro = d.pop("bro", UNSET)

        zeek = d.pop("zeek", UNSET)

        community_id = d.pop("community-id", UNSET)

        pattern_in_file = d.pop("pattern-in-file", UNSET)

        aba_rtn = d.pop("aba-rtn", UNSET)

        anonymised = d.pop("anonymised", UNSET)

        attachment = d.pop("attachment", UNSET)

        authentihash = d.pop("authentihash", UNSET)

        azure_application_id = d.pop("azure-application-id", UNSET)

        bank_account_nr = d.pop("bank-account-nr", UNSET)

        bic = d.pop("bic", UNSET)

        bin_ = d.pop("bin", UNSET)

        boolean = d.pop("boolean", UNSET)

        btc = d.pop("btc", UNSET)

        campaign_id = d.pop("campaign-id", UNSET)

        campaign_name = d.pop("campaign-name", UNSET)

        cc_number = d.pop("cc-number", UNSET)

        cdhash = d.pop("cdhash", UNSET)

        chrome_extension_id = d.pop("chrome-extension-id", UNSET)

        comment = d.pop("comment", UNSET)

        cookie = d.pop("cookie", UNSET)

        cortex = d.pop("cortex", UNSET)

        counter = d.pop("counter", UNSET)

        country_of_residence = d.pop("country-of-residence", UNSET)

        cpe = d.pop("cpe", UNSET)

        dash = d.pop("dash", UNSET)

        datetime_ = d.pop("datetime", UNSET)

        date_of_birth = d.pop("date-of-birth", UNSET)

        dkim = d.pop("dkim", UNSET)

        dkim_signature = d.pop("dkim-signature", UNSET)

        dns_soa_email = d.pop("dns-soa-email", UNSET)

        email_dst_display_name = d.pop("email-dst-display-name", UNSET)

        email_header = d.pop("email-header", UNSET)

        email_message_id = d.pop("email-message-id", UNSET)

        email_mime_boundary = d.pop("email-mime-boundary", UNSET)

        email_reply_to = d.pop("email-reply-to", UNSET)

        email_src_display_name = d.pop("email-src-display-name", UNSET)

        email_thread_index = d.pop("email-thread-index", UNSET)

        email_x_mailer = d.pop("email-x-mailer", UNSET)

        filenameauthentihash = d.pop("filename|authentihash", UNSET)

        filenameimpfuzzy = d.pop("filename|impfuzzy", UNSET)

        filenameimphash = d.pop("filename|imphash", UNSET)

        filenamemd5 = d.pop("filename|md5", UNSET)

        filename_pattern = d.pop("filename-pattern", UNSET)

        filenamepehash = d.pop("filename|pehash", UNSET)

        filenamesha224 = d.pop("filename|sha224", UNSET)

        filenamesha384 = d.pop("filename|sha384", UNSET)

        filenamesha3_224 = d.pop("filename|sha3-224", UNSET)

        filenamesha3_256 = d.pop("filename|sha3-256", UNSET)

        filenamesha3_384 = d.pop("filename|sha3-384", UNSET)

        filenamesha3_512 = d.pop("filename|sha3-512", UNSET)

        filenamesha512 = d.pop("filename|sha512", UNSET)

        filenamesha512224 = d.pop("filename|sha512/224", UNSET)

        filenamesha512256 = d.pop("filename|sha512/256", UNSET)

        filenamessdeep = d.pop("filename|ssdeep", UNSET)

        filenametlsh = d.pop("filename|tlsh", UNSET)

        filenamevhash = d.pop("filename|vhash", UNSET)

        first_name = d.pop("first-name", UNSET)

        frequent_flyer_number = d.pop("frequent-flyer-number", UNSET)

        full_name = d.pop("full-name", UNSET)

        gender = d.pop("gender", UNSET)

        gene = d.pop("gene", UNSET)

        github_organisation = d.pop("github-organisation", UNSET)

        github_repository = d.pop("github-repository", UNSET)

        github_username = d.pop("github-username", UNSET)

        hex_ = d.pop("hex", UNSET)

        hostnameport = d.pop("hostname|port", UNSET)

        iban = d.pop("iban", UNSET)

        identity_card_number = d.pop("identity-card-number", UNSET)

        impfuzzy = d.pop("impfuzzy", UNSET)

        imphash = d.pop("imphash", UNSET)

        integer = d.pop("integer", UNSET)

        ip_dstport = d.pop("ip-dst|port", UNSET)

        ip_srcport = d.pop("ip-src|port", UNSET)

        issue_date_of_the_visa = d.pop("issue-date-of-the-visa", UNSET)

        jabber_id = d.pop("jabber-id", UNSET)

        kusto_query = d.pop("kusto-query", UNSET)

        last_name = d.pop("last-name", UNSET)

        link = d.pop("link", UNSET)

        mac_address = d.pop("mac-address", UNSET)

        mac_eui_64 = d.pop("mac-eui-64", UNSET)

        malware_sample = d.pop("malware-sample", UNSET)

        malware_type = d.pop("malware-type", UNSET)

        middle_name = d.pop("middle-name", UNSET)

        mime_type = d.pop("mime-type", UNSET)

        mobile_application_id = d.pop("mobile-application-id", UNSET)

        mutex = d.pop("mutex", UNSET)

        named_pipe = d.pop("named pipe", UNSET)

        nationality = d.pop("nationality", UNSET)

        other = d.pop("other", UNSET)

        passenger_name_record_locator_number = d.pop("passenger-name-record-locator-number", UNSET)

        passport_country = d.pop("passport-country", UNSET)

        passport_expiration = d.pop("passport-expiration", UNSET)

        passport_number = d.pop("passport-number", UNSET)

        pattern_in_memory = d.pop("pattern-in-memory", UNSET)

        pattern_in_traffic = d.pop("pattern-in-traffic", UNSET)

        payment_details = d.pop("payment-details", UNSET)

        pehash = d.pop("pehash", UNSET)

        pgp_private_key = d.pop("pgp-private-key", UNSET)

        pgp_public_key = d.pop("pgp-public-key", UNSET)

        phone_number = d.pop("phone-number", UNSET)

        place_of_birth = d.pop("place-of-birth", UNSET)

        place_port_of_clearance = d.pop("place-port-of-clearance", UNSET)

        place_port_of_onward_foreign_destination = d.pop("place-port-of-onward-foreign-destination", UNSET)

        place_port_of_original_embarkation = d.pop("place-port-of-original-embarkation", UNSET)

        port = d.pop("port", UNSET)

        primary_residence = d.pop("primary-residence", UNSET)

        process_state = d.pop("process-state", UNSET)

        prtn = d.pop("prtn", UNSET)

        redress_number = d.pop("redress-number", UNSET)

        sha224 = d.pop("sha224", UNSET)

        sha384 = d.pop("sha384", UNSET)

        sha3_224 = d.pop("sha3-224", UNSET)

        sha3_256 = d.pop("sha3-256", UNSET)

        sha3_384 = d.pop("sha3-384", UNSET)

        sha3_512 = d.pop("sha3-512", UNSET)

        sha512 = d.pop("sha512", UNSET)

        sha512224 = d.pop("sha512/224", UNSET)

        sha512256 = d.pop("sha512/256", UNSET)

        sigma = d.pop("sigma", UNSET)

        size_in_bytes = d.pop("size-in-bytes", UNSET)

        snort = d.pop("snort", UNSET)

        special_service_request = d.pop("special-service-request", UNSET)

        ssdeep = d.pop("ssdeep", UNSET)

        ssh_fingerprint = d.pop("ssh-fingerprint", UNSET)

        stix2_pattern = d.pop("stix2-pattern", UNSET)

        target_email = d.pop("target-email", UNSET)

        target_external = d.pop("target-external", UNSET)

        target_location = d.pop("target-location", UNSET)

        target_machine = d.pop("target-machine", UNSET)

        target_org = d.pop("target-org", UNSET)

        target_user = d.pop("target-user", UNSET)

        telfhash = d.pop("telfhash", UNSET)

        text = d.pop("text", UNSET)

        threat_actor = d.pop("threat-actor", UNSET)

        tlsh = d.pop("tlsh", UNSET)

        travel_details = d.pop("travel-details", UNSET)

        twitter_id = d.pop("twitter-id", UNSET)

        uri = d.pop("uri", UNSET)

        vhash = d.pop("vhash", UNSET)

        visa_number = d.pop("visa-number", UNSET)

        vulnerability = d.pop("vulnerability", UNSET)

        weakness = d.pop("weakness", UNSET)

        whois_creation_date = d.pop("whois-creation-date", UNSET)

        whois_registrant_email = d.pop("whois-registrant-email", UNSET)

        whois_registrant_name = d.pop("whois-registrant-name", UNSET)

        whois_registrant_org = d.pop("whois-registrant-org", UNSET)

        whois_registrant_phone = d.pop("whois-registrant-phone", UNSET)

        whois_registrar = d.pop("whois-registrar", UNSET)

        windows_scheduled_task = d.pop("windows-scheduled-task", UNSET)

        windows_service_displayname = d.pop("windows-service-displayname", UNSET)

        windows_service_name = d.pop("windows-service-name", UNSET)

        x509_fingerprint_md5 = d.pop("x509-fingerprint-md5", UNSET)

        x509_fingerprint_sha1 = d.pop("x509-fingerprint-sha1", UNSET)

        x509_fingerprint_sha256 = d.pop("x509-fingerprint-sha256", UNSET)

        xmr = d.pop("xmr", UNSET)

        yara = d.pop("yara", UNSET)

        dom_hash = d.pop("dom-hash", UNSET)

        onion_address = d.pop("onion-address", UNSET)

        get_attribute_statistics_types_response = cls(
            md5=md5,
            sha1=sha1,
            sha256=sha256,
            filename=filename,
            pdb=pdb,
            filenamesha1=filenamesha1,
            filenamesha256=filenamesha256,
            ip_src=ip_src,
            ip_dst=ip_dst,
            hostname=hostname,
            domain=domain,
            domainip=domainip,
            email=email,
            email_src=email_src,
            email_dst=email_dst,
            email_subject=email_subject,
            email_attachment=email_attachment,
            email_body=email_body,
            eppn=eppn,
            float_=float_,
            git_commit_id=git_commit_id,
            url=url,
            http_method=http_method,
            user_agent=user_agent,
            ja3_fingerprint_md5=ja3_fingerprint_md5,
            jarm_fingerprint=jarm_fingerprint,
            favicon_mmh3=favicon_mmh3,
            hassh_md5=hassh_md5,
            hasshserver_md5=hasshserver_md5,
            regkey=regkey,
            regkeyvalue=regkeyvalue,
            as_=as_,
            bro=bro,
            zeek=zeek,
            community_id=community_id,
            pattern_in_file=pattern_in_file,
            aba_rtn=aba_rtn,
            anonymised=anonymised,
            attachment=attachment,
            authentihash=authentihash,
            azure_application_id=azure_application_id,
            bank_account_nr=bank_account_nr,
            bic=bic,
            bin_=bin_,
            boolean=boolean,
            btc=btc,
            campaign_id=campaign_id,
            campaign_name=campaign_name,
            cc_number=cc_number,
            cdhash=cdhash,
            chrome_extension_id=chrome_extension_id,
            comment=comment,
            cookie=cookie,
            cortex=cortex,
            counter=counter,
            country_of_residence=country_of_residence,
            cpe=cpe,
            dash=dash,
            datetime_=datetime_,
            date_of_birth=date_of_birth,
            dkim=dkim,
            dkim_signature=dkim_signature,
            dns_soa_email=dns_soa_email,
            email_dst_display_name=email_dst_display_name,
            email_header=email_header,
            email_message_id=email_message_id,
            email_mime_boundary=email_mime_boundary,
            email_reply_to=email_reply_to,
            email_src_display_name=email_src_display_name,
            email_thread_index=email_thread_index,
            email_x_mailer=email_x_mailer,
            filenameauthentihash=filenameauthentihash,
            filenameimpfuzzy=filenameimpfuzzy,
            filenameimphash=filenameimphash,
            filenamemd5=filenamemd5,
            filename_pattern=filename_pattern,
            filenamepehash=filenamepehash,
            filenamesha224=filenamesha224,
            filenamesha384=filenamesha384,
            filenamesha3_224=filenamesha3_224,
            filenamesha3_256=filenamesha3_256,
            filenamesha3_384=filenamesha3_384,
            filenamesha3_512=filenamesha3_512,
            filenamesha512=filenamesha512,
            filenamesha512224=filenamesha512224,
            filenamesha512256=filenamesha512256,
            filenamessdeep=filenamessdeep,
            filenametlsh=filenametlsh,
            filenamevhash=filenamevhash,
            first_name=first_name,
            frequent_flyer_number=frequent_flyer_number,
            full_name=full_name,
            gender=gender,
            gene=gene,
            github_organisation=github_organisation,
            github_repository=github_repository,
            github_username=github_username,
            hex_=hex_,
            hostnameport=hostnameport,
            iban=iban,
            identity_card_number=identity_card_number,
            impfuzzy=impfuzzy,
            imphash=imphash,
            integer=integer,
            ip_dstport=ip_dstport,
            ip_srcport=ip_srcport,
            issue_date_of_the_visa=issue_date_of_the_visa,
            jabber_id=jabber_id,
            kusto_query=kusto_query,
            last_name=last_name,
            link=link,
            mac_address=mac_address,
            mac_eui_64=mac_eui_64,
            malware_sample=malware_sample,
            malware_type=malware_type,
            middle_name=middle_name,
            mime_type=mime_type,
            mobile_application_id=mobile_application_id,
            mutex=mutex,
            named_pipe=named_pipe,
            nationality=nationality,
            other=other,
            passenger_name_record_locator_number=passenger_name_record_locator_number,
            passport_country=passport_country,
            passport_expiration=passport_expiration,
            passport_number=passport_number,
            pattern_in_memory=pattern_in_memory,
            pattern_in_traffic=pattern_in_traffic,
            payment_details=payment_details,
            pehash=pehash,
            pgp_private_key=pgp_private_key,
            pgp_public_key=pgp_public_key,
            phone_number=phone_number,
            place_of_birth=place_of_birth,
            place_port_of_clearance=place_port_of_clearance,
            place_port_of_onward_foreign_destination=place_port_of_onward_foreign_destination,
            place_port_of_original_embarkation=place_port_of_original_embarkation,
            port=port,
            primary_residence=primary_residence,
            process_state=process_state,
            prtn=prtn,
            redress_number=redress_number,
            sha224=sha224,
            sha384=sha384,
            sha3_224=sha3_224,
            sha3_256=sha3_256,
            sha3_384=sha3_384,
            sha3_512=sha3_512,
            sha512=sha512,
            sha512224=sha512224,
            sha512256=sha512256,
            sigma=sigma,
            size_in_bytes=size_in_bytes,
            snort=snort,
            special_service_request=special_service_request,
            ssdeep=ssdeep,
            ssh_fingerprint=ssh_fingerprint,
            stix2_pattern=stix2_pattern,
            target_email=target_email,
            target_external=target_external,
            target_location=target_location,
            target_machine=target_machine,
            target_org=target_org,
            target_user=target_user,
            telfhash=telfhash,
            text=text,
            threat_actor=threat_actor,
            tlsh=tlsh,
            travel_details=travel_details,
            twitter_id=twitter_id,
            uri=uri,
            vhash=vhash,
            visa_number=visa_number,
            vulnerability=vulnerability,
            weakness=weakness,
            whois_creation_date=whois_creation_date,
            whois_registrant_email=whois_registrant_email,
            whois_registrant_name=whois_registrant_name,
            whois_registrant_org=whois_registrant_org,
            whois_registrant_phone=whois_registrant_phone,
            whois_registrar=whois_registrar,
            windows_scheduled_task=windows_scheduled_task,
            windows_service_displayname=windows_service_displayname,
            windows_service_name=windows_service_name,
            x509_fingerprint_md5=x509_fingerprint_md5,
            x509_fingerprint_sha1=x509_fingerprint_sha1,
            x509_fingerprint_sha256=x509_fingerprint_sha256,
            xmr=xmr,
            yara=yara,
            dom_hash=dom_hash,
            onion_address=onion_address,
        )

        get_attribute_statistics_types_response.additional_properties = d
        return get_attribute_statistics_types_response

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
