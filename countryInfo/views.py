from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CountryInfoSerializer

class CountryInfoView(APIView):
    def get(self, request, country_name):
        url = f"https://en.wikipedia.org/wiki/{country_name}"
        html_content = requests.get(url).content
        soup = BeautifulSoup(html_content, 'html.parser')
        info_box = soup.find("table", {"class": "infobox ib-country vcard"})
        if not info_box:
            return Response({'error': 'Country information not found'}, status=404)
        data = {}
        rows = info_box.find_all("tr")
        for row in rows:
            key = row.find("th")
            value = row.find("td")
            if key and value:
                key_text = key.text.strip()
                if key_text == "Capital":
                    data["capital"] = value.text.strip()
                elif key_text == "Largest city":
                    data["largest_city"] = value.text.strip().split(";")
                elif key_text == "Official languages":
                    languages = []
                    for element in value.find_all("a"):
                        languages.append(element.text)
                    data["official_languages"] = languages
                elif key_text == "Area":
                    value_text = value.text.strip()
                    if "Total" in value_text:
                        area_parts = value_text.split("\n")
                        for area_part in area_parts:
                            if "Total" in area_part:
                                total_area = area_part.replace("Total", "").strip()
                                if "km²" in total_area:
                                    data["area_total"] = int(total_area.split()[0].replace(",",""))
                elif key_text == "Population":
                    population_string = value.text.strip()
                    population_parts = population_string.split(" ")
                    data["population"] = int(float(population_parts[0].replace(",", "")) * int(population_parts[1]))
                elif key_text == "GDP (nominal)":
                     if key_text == "GDP (nominal)":
                        GDP_parts = value.text.strip().split("\n")
                        for GDP_part in GDP_parts:
                            if "Total" in GDP_part:
                                GDP_part_parts = GDP_part.split(" ")
                                data["GDP_nominal"] = float(GDP_part_parts[1].replace(",", ""))
        # Extracting flag link
        img_src = info_box.find("img")["src"]
        img_src = "https:" + img_src
        data["flag_link"] = img_src
        # Using serializer
        serializer = CountryInfoSerializer(data=data)
        serializer.is_valid()
        return Response(serializer.data)
