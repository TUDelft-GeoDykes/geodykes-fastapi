# coding: utf-8

"""
    Geodykes Web Service

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)

    The version of the OpenAPI document: 0.1.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from openapi_client.models.cards import Cards

class TestCards(unittest.TestCase):
    """Cards unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> Cards:
        """Test Cards
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `Cards`
        """
        model = Cards()
        if include_optional:
            return Cards(
                items = [
                    openapi_client.models.card.Card(
                        front = '', 
                        back = '', 
                        hint = '', 
                        id = 56, 
                        deck_id = 56, )
                    ]
            )
        else:
            return Cards(
                items = [
                    openapi_client.models.card.Card(
                        front = '', 
                        back = '', 
                        hint = '', 
                        id = 56, 
                        deck_id = 56, )
                    ],
        )
        """

    def testCards(self):
        """Test Cards"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
