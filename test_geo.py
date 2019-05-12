from unittest import main, mock, TestCase
import geo

class TestGeo(TestCase):

    def setUp(self):
        self.input_html = """
        <tr><td>IP</td><td>8.8.8.8</td></tr>
        <tr><td>Continent Code</td><td>NA</td></tr>
        <tr><td>Continent</td><td>North America</td></tr>
        <tr><td>Country Codes</td><td>US, USA</td></tr>
        <tr><td>Country</td><td>United States</td></tr>
        """


    def test_geolocate_ip(self):
        mock_response = mock.Mock(text=self.input_html)

        with mock.patch("geo.requests.get") as mock_get:
            mock_get.return_value = mock_response

            result = geo.geolocate_ip("8.8.8.8")
            self.assertEqual("United States", result)
            mock_get.assert_called_with('https://ipgeolocation.io/ip-location/8.8.8.8')


    def test_extract_country(self):
        expected = "United States"
        self.assertEqual(geo.extract_country(self.input_html), expected)


    def test_is_reserved(self):
        self.assertEqual(geo.is_reserved("127.0.0.1"), True)
        self.assertEqual(geo.is_reserved("192.168.3.7"), True)
        self.assertEqual(geo.is_reserved("192.168.1.2"), True)

        self.assertEqual(geo.is_reserved("42.155.6.92"), False)
        self.assertEqual(geo.is_reserved("96.94.123.77"), False)
        self.assertEqual(geo.is_reserved("234.217.44.1"), False)


    def test_remove_emptys(self):
        input_list = ['abc', '123', '', 'aeiou', '', 'xyz']
        result = geo.remove_emptys(input_list)

        self.assertEqual(result, ['abc', '123', 'aeiou', 'xyz'])


if __name__ == "__main__":
    main()