from flask import Flask,render_template,request,jsonify
import requests

app=Flask(__name__)
API_KEY="aaaa2d144354174a9382e38e80e6030b"

def get_coordinates(city):
    url=f"https://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={API_KEY}"
    r=requests.get(url)
    if r.status_code==200:
        data=r.json()
        if len(data)>0:
            return data[0]["lat"],data[0]["lon"]
    return None,None

def get_aqi(lat,lon):
    url=f"https://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
    r=requests.get(url)
    if r.status_code==200:
        data=r.json()
        aqi=data["list"][0]["main"]["aqi"]
        comp=data["list"][0]["components"]
        return {"aqi":aqi,"components":comp}
    return {"error":"Unable to fetch AQI"}

@app.route("/",methods=["GET","POST"])
def index():
    result=None
    if request.method=="POST":
        city=request.form["city"]
        lat,lon=get_coordinates(city)
        if lat is not None and lon is not None:
            result=get_aqi(lat,lon)
            result["city"]=city.title()
        else:
            result={"error":"City not found"}
    return render_template("index.html",result=result)

@app.route("/get_aqi", methods=["POST"])
def get_aqi_endpoint():
    city = request.args.get("city")
    if not city:
        return jsonify({"error": "City not provided"})
    lat, lon = get_coordinates(city)
    if lat is not None and lon is not None:
        result = get_aqi(lat, lon)
        result["city"] = city.title()
        return jsonify(result)
    else:
        return jsonify({"error": "City not found"})

if __name__=="__main__":
    app.run(debug=True)