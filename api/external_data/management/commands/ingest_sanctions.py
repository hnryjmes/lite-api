import itertools
import logging

from django.conf import settings
from django.core.management.base import BaseCommand

from elasticsearch_dsl import connections
import pyexcel

import requests
import xmltodict

from api.external_data import documents
from api.flags.enums import SystemFlags
import hashlib

log = logging.getLogger(__name__)


def get_un_sanctions():
    response = requests.get(settings.SANCTION_LIST_SOURCES["un_sanctions_file"])
    response.raise_for_status()
    return xmltodict.parse(
        response.content,
        postprocessor=(lambda path, key, value: (key.lower(), value)),
        xml_attribs=False,
        cdata_key="p",
        force_list=["entity_address", "individual_address"],
    )


def get_office_financial_sanctions_implementation():
    response = requests.get(settings.SANCTION_LIST_SOURCES["office_financial_sanctions_file"])
    response.raise_for_status()
    return xmltodict.parse(
        response.content,
        postprocessor=(lambda path, key, value: (key.lower(), value)),
        xml_attribs=False,
        cdata_key="p",
    )


def get_uk_sanctions_list():
    book = pyexcel.get_book(url=settings.SANCTION_LIST_SOURCES["uk_sanctions_file"])
    return parse_ods(book)


def parse_ods(book):
    for sheet_name in book.sheet_names():
        records = iter(book[sheet_name])
        # Top 2 lines is just meta
        next(records)
        next(records)
        headers = next(records)
        for row in records:
            data = dict(zip(headers, row))
            yield {**data, "sheet": sheet_name}


def join_fields(data, fields):
    return " ".join(str(data[field]) for field in fields if data.get(field))


def hash_values(data_values):
    data = "".join([val for val in data_values if val is not None])
    return hashlib.md5(data.encode()).hexdigest()  # nosec


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--rebuild", default=False, action="store_true")

    def rebuild_index(self):
        connection = connections.get_connection()
        connection.indices.delete(index=settings.ELASTICSEARCH_SANCTION_INDEX_ALIAS, ignore=[404])
        documents.SanctionDocumentType.init()

    def handle(self, *args, **options):
        if options["rebuild"]:
            self.rebuild_index()
        self.populate_united_nations_sanctions()
        self.populate_office_financial_sanctions_implementation()
        self.populate_uk_sanctions_list()

    def populate_united_nations_sanctions(self):
        try:
            parsed = get_un_sanctions()
            successful = 0
            failed = 0
            individuals = parsed["consolidated_list"]["individuals"]["individual"]
            entities = parsed["consolidated_list"]["entities"]["entity"]
            for item in itertools.chain(individuals, entities):
                try:
                    item.pop("nationality", None)
                    item.pop("title", None)

                    address_dicts = item.pop("entity_address", {}) or item.pop("individual_address", {})

                    addresses = []
                    for address_dict in address_dicts:
                        if address_dict:
                            addresses.append(" ".join([item for item in address_dict.values() if item]))

                    document = documents.SanctionDocumentType(
                        meta={"id": item["dataid"]},
                        name=join_fields(item, fields=["first_name", "second_name", "third_name"]),
                        address=addresses,
                        flag_uuid=SystemFlags.SANCTION_UN_SC_MATCH,
                        reference=item["dataid"],
                        data=item,
                    )
                    document.save()
                    successful += 1
                except:
                    failed += 1
                    log.exception(
                        "Error loading un sanction record -> %s",
                        exc_info=True,
                    )
            log.info(
                f"uk sanctions (successful:{successful} failed:{failed})",
            )
        except:
            log.exception(
                "Error loading un sanctions -> %s",
                exc_info=True,
            )

    def populate_office_financial_sanctions_implementation(self):
        successful = 0
        failed = 0
        try:
            parsed = get_office_financial_sanctions_implementation()
            for item in parsed["arrayoffinancialsanctionstarget"]["financialsanctionstarget"]:
                try:
                    item.pop("nationality", None)
                    address = join_fields(
                        item, fields=["address1", "address2", "address3", "address4", "address5", "address6"]
                    )
                    name = join_fields(item, fields=["name1", "name2", "name3", "name4", "name5", "name6"])
                    postcode = normalize_address(item["postcode"])
                    if postcode not in normalize_address(address):
                        address += " " + postcode

                    # We need to hash the data that uniquely identifies records atm we only care about names
                    unique_id = hash_values([item["groupid"], name])
                    document = documents.SanctionDocumentType(
                        meta={"id": f"ofs:{unique_id}"},
                        name=name,
                        address=address,
                        postcode=postcode,
                        flag_uuid=SystemFlags.SANCTION_OFSI_MATCH,
                        reference=item["groupid"],
                        data=item,
                    )
                    document.save()
                    successful += 1
                except:
                    failed += 1
                    log.exception(
                        "Error loading office financial sanction record -> %s",
                        exc_info=True,
                    )
            log.info(
                f"office financial sanctions (successful:{successful} failed:{failed})",
            )
        except:
            log.exception(
                "Error office financial sanctions -> %s",
                exc_info=True,
            )

    def populate_uk_sanctions_list(self):
        successful = 0
        failed = 0
        try:
            parsed = get_uk_sanctions_list()
            for item in parsed:
                try:
                    item.pop("nationality", None)
                    address = join_fields(
                        item, fields=["Address Line 1", "Address Line 2", "Address Line 3", "Address Line 4"]
                    )
                    postcode = normalize_address(item["Address Postal Code"])
                    if postcode not in normalize_address(address):
                        address += " " + postcode
                    name = join_fields(item, fields=["Name 1", "Name 2", "Name 3", "Name 4", "Name 5", "Name 6"])
                    unique_id = hash_values([item["Unique ID"], name, address, postcode, item["Regime Name"]])
                    document = documents.SanctionDocumentType(
                        meta={"id": f"uk:{unique_id}"},
                        name=name,
                        address=address,
                        postcode=postcode,
                        flag_uuid=SystemFlags.SANCTION_UK_MATCH,
                        reference=item["Unique ID"],
                        data=item,
                    )
                    document.save()
                    successful += 1
                except:
                    failed += 1
                    log.exception(
                        "Error loading uk sanction record -> %s",
                        exc_info=True,
                    )
            log.info(
                f"uk sanctions (successful:{successful} failed:{failed})",
            )
        except:
            log.exception(
                "Error loading uk sanctions -> %s",
                exc_info=True,
            )


def normalize_address(value):
    if isinstance(value, int):
        value = str(value)
    if not value or value.lower() in ["unknown", None, ""]:
        return ""

    return value.replace(" ", "")
