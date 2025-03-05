from django.shortcuts import render

import json
import requests

def home(request):
    if request.method == "POST":
        zipcode = request.POST.get('zipcode', '')  # Use request.POST.get to safely get form data

        api_request = requests.get(
            "https://www.airnowapi.org/aq/observation/zipCode/current/?format=application/json&zipCode="
            + zipcode + "&distance=25&API_KEY=EFA7E1A7-D6BB-4060-B72F-70C276D435F1"
        )

        try:
            api = json.loads(api_request.content)
        except Exception as e:
            api = "Error.."
        if api != "Error..":
            if api[0]['Category']['Name'] == "Good":
                category_description = "(0 - 50) Air Quality is satisfactory, air pollution poses little"
            elif api[0]['Category']['Name'] == "Moderate":
                category_description = "(51 - 100) Air Quality is acceptable "
            elif api[0]['Category']['Name'] == "Unhealthy for Sensitive Groups":
                category_description = "(101 - 150) Air Quality is a, air pollution poses little"
            elif api[0]['Category']['Name'] == "Unhealthy":
                category_description = "(151 - 200 ) General public is not likely affected"
            elif api[0]['Category']['Name'] == "Very Unhealthy":
                category_description = "(201 - 300) Every one will experience health conditions"
            elif api[0]['Category']['Name'] == "Hazardous":
                category_description = "(301 - 500) Health warning, Emergency condition"

        return render(request, "home.html", {'api': api, 'category_description': category_description})
    else:
        return render(request, "home.html", {})

def about(request):
    return render(request, 'about.html')