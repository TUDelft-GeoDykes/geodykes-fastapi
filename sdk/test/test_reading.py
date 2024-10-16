# coding: utf-8

"""
    Geodykes Web Service

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)

    The version of the OpenAPI document: 0.1.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from openapi_client.models.reading import Reading

class TestReading(unittest.TestCase):
    """Reading unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> Reading:
        """Test Reading
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `Reading`
        """
        model = Reading()
        if include_optional:
            return Reading(
                id = 56,
                crossection = '',
                sensor_id = 56,
                sensor_name = '',
                sensor_type = '',
                sensor_location = [
                    1.337
                    ],
                sensor_is_active = True,
                location_in_topology = [
                    1.337
                    ],
                unit = '',
                value = 1.337,
                time = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f')
            )
        else:
            return Reading(
                id = 56,
                crossection = '',
                sensor_id = 56,
                sensor_name = '',
                sensor_type = '',
                sensor_location = [
                    1.337
                    ],
                sensor_is_active = True,
                location_in_topology = [
                    1.337
                    ],
                unit = '',
                value = 1.337,
                time = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'),
        )
        """

    def testReading(self):
        """Test Reading"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
