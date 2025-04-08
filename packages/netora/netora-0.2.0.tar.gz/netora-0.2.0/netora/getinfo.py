import os
import sys
import datetime
import zoneinfo

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from netora.resources.currencies import currencies

def sort_data(name, data):
    if name not in data or data[name] is None:
        return "Not Found"
    else:
        return data[name]

def get_ip_info(ip_info, ip_info2, location_link=""):
    ip = sort_data("ip", ip_info)
    ipv = sort_data("version", ip_info)

    isp = sort_data("org", ip_info)
    continent_code = sort_data("continentCode", ip_info2)

    continent_name = sort_data("continentName", ip_info2)    
    country = sort_data("country_name", ip_info)

    phone_code = sort_data("country_calling_code", ip_info)
    city = sort_data("city", ip_info)

    country_code = sort_data("country", ip_info)  
    latitude = sort_data("latitude", ip_info)

    longitude = sort_data("longitude", ip_info)
    timezone = sort_data("timezone", ip_info)

    country_capital = sort_data("country_capital", ip_info)
    currency_name = sort_data("currency_name", ip_info)
    
    if currency_name == "Not Found":
        currency_symbol = "Not Found"
    else:
        currency_symbol = currencies.get(currency_name, "Currency symbol not found")

    if timezone == "Not Found":
        local_time = "Not Found"
    else: 
        local_time = datetime.datetime.now(zoneinfo.ZoneInfo(timezone)).strftime('%H:%M:%S')
    
    return {
        "ip": ip,
        "ipv": ipv,
        "isp": isp,
        "continent_code": continent_code,
        "continent_name": continent_name,
        "country": country,
        "phone_code": phone_code,
        "city": city,
        "country_code": country_code,
        "latitude": latitude,
        "longitude": longitude,
        "location_link": location_link,
        "currency_name": currency_name,
        "currency_symbol": currency_symbol,
        "local_time": local_time,
        "country_capital": country_capital,
    }