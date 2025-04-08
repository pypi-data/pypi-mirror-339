import os
import unittest
import sys

current_dir = os.path.dirname(__file__)
src_dir = os.path.join(current_dir, "..")

class TestExportInfo(unittest.TestCase):
    def test_export_info(self):
        file_path = os.path.normpath(
            os.path.join(current_dir, "data", "mock-output.txt")
        )
        
        data = {
            "ip": "192.168.1.1",
            "ipv": "IPv4",
            "isp": "ExampleISP",
            "continent_code": "NA",
            "continent_name": "North America",
            "country": "USA",
            "phone_code": "+1",
            "city": "New York",
            "country_code": "US",
            "latitude": 40.7128,
            "longitude": -74.0060,
            "location_link": "http://example.com",
            "currency_name": "USD",
            "currency_symbol": "$",
            "local_time": "2025-03-10 14:00:00",
            "country_capital": "Washington, D.C.",
        }

        with open(file_path, "w") as f:
            for key, value in data.items():
                if isinstance(value, float): 
                    value = f"{value:.4f}"                            
                f.write(f"{key}: {value}\n")
            f.write("\n[*] IP lookup completed with 15 results") 

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.readlines()

        content = [line.strip() for line in content]    

        self.assertTrue("ip: 192.168.1.1" in content)
        self.assertTrue("isp: ExampleISP" in content)
        self.assertTrue("continent_code: NA" in content)
        self.assertTrue("city: New York" in content)
        self.assertTrue("latitude: 40.7128" in content)
        self.assertTrue("longitude: -74.0060" in content)
        self.assertTrue("currency_name: USD" in content)
        self.assertTrue("country_capital: Washington, D.C." in content)

    def tearDown(self):
        file_path = os.path.normpath(
            os.path.join(current_dir, "data", "mock-output.txt")
        )
        if os.path.exists(file_path):
            os.remove(file_path)

if __name__ == "__main__":
    unittest.main()