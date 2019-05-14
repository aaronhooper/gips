from unittest import main, mock, TestCase
import geo

class TestGeo(TestCase):

    def setUp(self):
        self.mock_html = """
        <tr><td>IP</td><td>8.8.8.8</td></tr>
        <tr><td>Continent Code</td><td>NA</td></tr>
        <tr><td>Continent</td><td>North America</td></tr>
        <tr><td>Country Codes</td><td>US, USA</td></tr>
        <tr><td>Country</td><td>United States</td></tr>
        """


    def test_extract_ips(self):
        mock_text = """
        2.110.20.189 - - [07/May/2019:19:39:08 +0000]
        192.168.1.5 - - [07/May/2019:19:40:00 +0000]
        176.249.131.208 - - [07/May/2019:19:40:20 +0000]

        """
        mock_read = mock.Mock(return_value=mock_text)
        mock_file = mock.Mock(read=mock_read)

        result = geo.extract_ips(mock_file)
        self.assertEqual(["2.110.20.189","192.168.1.5", "176.249.131.208"], result)


    def test_geolocate_ip(self):
        mock_response = mock.Mock(text=self.mock_html)

        with mock.patch("geo.requests.get") as mock_get:
            mock_get.return_value = mock_response

            result = geo.geolocate_ip("8.8.8.8")
            self.assertEqual("United States", result)
            mock_get.assert_called_with('https://ipgeolocation.io/ip-location/8.8.8.8')


    def test_extract_country(self):
        expected = "United States"
        self.assertEqual(geo.extract_country(self.mock_html), expected)


    def test_is_reserved(self):
        self.assertEqual(geo.is_reserved("127.0.0.1"), True)
        self.assertEqual(geo.is_reserved("127.34.45.200"), True)
        self.assertEqual(geo.is_reserved("127.99.99.99"), True)

        self.assertEqual(geo.is_reserved("192.168.3.7"), True)
        self.assertEqual(geo.is_reserved("192.168.1.2"), True)
        self.assertEqual(geo.is_reserved("192.168.254.23"), True)

        self.assertEqual(geo.is_reserved("42.155.6.92"), False)
        self.assertEqual(geo.is_reserved("96.94.123.77"), False)
        self.assertEqual(geo.is_reserved("199.217.44.1"), False)

        self.assertEqual(geo.is_reserved("172.16.1.94"), True)
        self.assertEqual(geo.is_reserved("172.24.211.94"), True)
        self.assertEqual(geo.is_reserved("172.29.41.12"), True)

        self.assertEqual(geo.is_reserved("10.11.12.1"), True)
        self.assertEqual(geo.is_reserved("10.65.1.254"), True)
        self.assertEqual(geo.is_reserved("10.2.10.2"), True)


    def test_remove_emptys(self):
        input_list = ['abc', '123', '', 'aeiou', '', 'xyz']
        result = geo.remove_emptys(input_list)

        self.assertEqual(result, ['abc', '123', 'aeiou', 'xyz'])


if __name__ == "__main__":
    main()