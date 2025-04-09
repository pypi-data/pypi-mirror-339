
from dataclasses import dataclass
from typing import List

import requests
from requests.models import Response

@dataclass
class Todo:
    Id: int
    Status: str
    Comment: str
    Deadline: str
    UserId: int
    Type: int
    Url: str


@dataclass
class Adatlap:
    Id: int
    Name: str
    Url: str
    ContactId: int
    StatusId: int
    UserId: int
    Deleted: int


@dataclass
class Address:
    Id: int
    ContactId: int
    Type: str
    Name: str
    CountryId: str
    PostalCode: str
    City: str
    County: str
    Address: str
    Default: int
    CreatedBy: str
    CreatedAt: str
    UpdatedBy: str
    UpdatedAt: str


@dataclass
class TodoDetails:
    Id: int
    UserId: str
    ContactId: int
    ProjectId: int
    Type: str
    Duration: int
    Reminder: int
    Status: str
    Mode: str
    Deadline: str
    Comment: str
    CreatedBy: str
    CreatedAt: str
    UpdatedBy: str
    UpdatedAt: str
    ClosedBy: str
    ClosedAt: str
    AddressId: int
    SenderUserId: int
    Attachments: List[str]
    Members: List[str]
    Notes: List[str]


@dataclass
class MiniCrmResponse:
    Count: int
    Results: List[dict]


class MiniCrmClient:
    base_url = "https://r3.minicrm.hu/Api/"

    def __init__(
        self,
        system_id,
        api_key,
        description=None,
        script_name=None,
    ):

        self.script_name = script_name
        self.description = description
        self.system_id = system_id
        self.system = system_id
        self.api_key = api_key

    def list_todos(self, adatlap_id, criteria=lambda _: True) -> List[Todo]:
        todos = self.get_request(endpoint="ToDoList", id=adatlap_id)
        return [Todo(**todo) for todo in todos.json() if criteria(todo)]

    def get_request(
        self,
        endpoint,
        id=None,
        query_params=None,
        isR3=True,
    ) -> Response:

        endpoint = f"{'R3/' if isR3 else ''}{endpoint}{'/'+str(id) if id else ''}"
        return requests.get(
            f"{self.base_url}{endpoint}",
            auth=(self.system_id, self.api_key),
            params=query_params,
        )

    def get_adatlap(
        self, category_id, status_id=None, criteria=lambda _: True, deleted=False
    ):
        query_params = {"CategoryId": category_id}
        if status_id:
            query_params["StatusId"] = status_id

        adatlapok = self.get_request(endpoint="Project", query_params=query_params)

        return [
            Adatlap(**adatlap)
            for adatlap in adatlapok.json()
            if criteria(adatlap) and (adatlap["Deleted"] == 0 or deleted)
        ]

    def get_adatlap_details(
        self,
        id,
    ):
        return self.get_request(
                endpoint="Project",
                id=id,
            ).json()

    def contact_details(self, contact_id=None, adatlap_id=None):
        if adatlap_id and not contact_id:
            contact_id = self.get_adatlap_details(adatlap_id).ContactId
        resp = self.get_request(
            "Contact",
            id=contact_id,
        )

        return resp.json()

    def address_ids(
        self,
        contact_id,
    ) -> List[int]:
        resp = self.get_request(
            "AddressList",
            id=contact_id,
        )
        return resp.json()["Results"]

    def address_details(self, address_id: int):
        return Address(
            **self.get_request(
                "Address",
                id=address_id,
            ).json()
        )

    def address_list(self, contact_id):
        return [self.address_details(i) for i in self.address_ids(contact_id)]

    def get_address(self, contact_id, typeof=None):
        addresses = self.address_list(contact_id=contact_id)
        for address in addresses:
            if typeof is None or address.Type == typeof:
                return address
        return None

    def todo_details(self, todo_id):
        return TodoDetails(
            **self.get_request(
                endpoint="ToDo",
                id=todo_id,
            ).json()
        )

    def get_order(self, order_id):
        return self.get_request(endpoint="Order", id=order_id, isR3=False)

    def create_order(
        self,
        adatlap,
        offer_id,
        adatlap_status=None,
        project_data=None,
    ):
        contactData = self.contact_details(contact_id=adatlap.ContactId)
        offerData = self.get_offer(offer_id).json()
        randomId = random.randint(100000, 999999)
        products = "\n".join(
            [
                f"""<Product Id="{item['Id']}">
            <!-- Name of product [required int] -->
            <Name>{item['Name']}</Name>
            <!-- SKU code of product [optional string]-->
            <SKU>{item['SKU']}</SKU>
            <!-- Nett price of product [required int] -->
            <PriceNet>{item['PriceNet']}</PriceNet>
            <!-- Quantity of product [required int] -->
            <Quantity>{item["Quantity"]}</Quantity>
            <!-- Unit of product [required string] -->
            <Unit>darab</Unit>
            <!-- VAT of product [required int] -->
            <VAT>27%</VAT>
            <!-- Folder of product in MiniCRM. If it does not exist, then it is created automaticly [required string] -->
            <FolderName>Default products</FolderName>
        </Product>"""
                for item in offerData["Items"]
            ]
        )
        xml_string = (
            f"""<?xml version="1.0" encoding="UTF-8"?>
    <Projects>
        <Project Id="{randomId}">
            <StatusId>3099</StatusId>
            <Name>{adatlap.Name}</Name>
            <ContactId>{adatlap.ContactId}</ContactId>
            <UserId>{adatlap.UserId}</UserId>
            <CategoryId>32</CategoryId>
            <Contacts>
                <Contact Id="{randomId}">
                    <FirstName>{contactData["FirstName"]}</FirstName>
                    <LastName>{contactData["LastName"]}</LastName>
                    <Type>{contactData["Type"]}</Type>
                    <Email>{contactData["Email"]}</Email>
                    <Phone>{contactData["Phone"]}</Phone>
                </Contact>
            </Contacts>
            <Orders>
                <Order Id="{randomId}">
                    <Number>{adatlap.Name}</Number>
                    <CurrencyCode>HUF</CurrencyCode>
                    <!-- Performace date of order [required date] -->
                    <Performance>2015-09-22 12:15:13</Performance>
                    <Status>Draft</Status>
                    <!-- Data of Customer -->
                    <Customer>
                        <!-- Name of Customer [required string] -->
                        <Name>{contactData.LastName} {contactData.FirstName}</Name>
                        <!-- Country of customer [required string] -->
                        <CountryId>Magyarország</CountryId>
                        <!-- Postalcode of customer [required string] -->
                        <PostalCode>{offerData["Customer"]["PostalCode"]}</PostalCode>
                        <!-- City of customer [required string] -->
                        <City>{offerData["Customer"]["City"]}</City>
                        <!-- Address of customer [required string] -->
                        <Address>{offerData["Customer"]["Address"]}</Address>
                    </Customer>
                    <!-- Data of product -->
                    <Products>
                        <!-- Id = External id of product [required int] -->
                        {products}
                    </Products>
                    <Project>
                        <Enum1951>{adatlap_status if adatlap_status else ''}</Enum1951>
                        """
            + "\n".join(
                [
                    f"<{k}><![CDATA[{v}]]></{k}>"
                    for k, v in project_data.items()
                    if v
                ] if project_data is not None else []
            )
            + """
                    </Project>
                </Order>
            </Orders>
        </Project>
    </Projects>"""
        )

        return requests.post(
            f"https://r3.minicrm.hu/Api/SyncFeed/119/Upload",
            auth=(self.system_id, self.api_key),
            data=xml_string.encode("utf-8"),
            headers={"Content-Type": "application/xml"},
        )

    def get_offer(self, offer_id):
        return self.get_request(endpoint="Offer", id=offer_id, isR3=False)

    def update_request(
        self, id, fields={}, endpoint="Project", isR3=True, method="PUT"
    ):

        endpoint = f'{"/R3" if isR3 else ""}/{endpoint}/{id}'
        if method == "PUT":
            return requests.put(
                f"https://r3.minicrm.hu/Api{endpoint}",
                auth=(self.system_id, self.api_key),
                json=fields,
            )
        elif method == "POST":
            return requests.post(
                f"https://r3.minicrm.hu/Api{endpoint}",
                auth=(self.system_id, self.api_key),
                json=fields,
            )

    def update_adatlap_fields(self, id, fields: dict):
        return self.update_request(
            id=id, fields=fields, endpoint="Project"
        )

    def create_to_do(self, adatlap_id, user, type, comment, deadline):

        data = {
            "ProjectId": adatlap_id,
            "UserId": user,
            "Type": type,
            "Comment": comment,
            "Deadline": deadline,
        }

        return requests.put(
            f"https://r3.minicrm.hu/Api/R3/ToDo/",
            auth=(self.system_id, self.api_key),
            params=data,
        )

    def update_todo(self, id, fields):
        return self.update_request(id=id, fields=fields, endpoint="ToDo")

    def update_offer_order(self, offer_id, fields, project=True, type="Offer"):
        return self.update_request(
            id=str(offer_id) + ("/Project" if project else ""),
            fields=fields,
            endpoint=type,
            isR3=False,
            method="POST",
        )

    def update_order_status(self, order_id, status="Complete"):
        return self.update_request(
            id=str(order_id) + "/" + status, method="POST", isR3=False, endpoint="Order"
        )
