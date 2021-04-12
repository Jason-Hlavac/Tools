import json
import requests

class account(object):
    def __init__(self, n):
        self.name = n
        self.client = "" #Enter Client ID
        self.secret = "" #Enter Client Secret
        self.token = self.getToken()
        self.data = self.getAPI(self.name, self.token)
    def initialize(self):
        task = input(""" 
Please select a function for channel, {}, by typing a number:         
[1] Display Broadcaster Data
[2] Display Game Data
[3] Display Tag Data
[4] Exit
        """.format(self.name))
        
        if(task == "1"):
            self.Broadcaster_data()
        elif(task == "2"):
            self.Game_data()
        elif(task == "3"):
            self.Tag_data()
        elif(task == "4"):
            pass
        else:
            print("Error: Command not found")
            self.initialize()
            
    def Broadcaster_data(self):
        data = self.getAPI(self.name, self.token)
        inner_data = data["data"][0]
        print("Username : " + inner_data["display_name"])
        print("Language : " + inner_data["broadcaster_language"])
        if(inner_data["is_live"] == True):
            print("Status : Live")
            print("Current Title : " + inner_data["title"])
            print("Stream Started : " + inner_data["started_at"])
        elif(inner_data["is_live"] == False):
            print("Status : Offline")
            print("Previous Title : " + inner_data["title"])
        self.initialize()
            
            
    def Game_data(self):
        
        result = self.Game_numbers()
        inner_data = self.data["data"][0]
        if(inner_data["is_live"] == True):
            print("Current Game : " + result["game_name"])
            print(result["game_name"] + " currently has " + str(result["viewer_count"]) + " viewers")
            print(result["game_name"] + " currently has " + str(result["streamer_count"]) + " streamers")
            print(self.name + " currently has " + str(result["viewers"]) + " viewers")
            print(self.name + " currently has " + str((shortenFloat(float(result["viewers"])/ float(result["viewer_count"]), 5))*100)+ "% of the viewers for " + result["game_name"])
            if(float(result["viewers"])/ float(result["viewer_count"]) > 1.0 / result["streamer_count"]):
                print(self.name + " is currently at above average viewers for " + result["game_name"])
            elif(float(result["viewers"])/ float(result["viewer_count"]) < 1.0 / result["streamer_count"]):
                print(self.name + " is currently at below average viewers for " + result["game_name"])
            elif(float(result["viewers"])/ float(result["viewer_count"]) == 1.0 / result["streamer_count"]):
                print(self.name + " is currently at average viewers for " + result["game_name"])
            else:
                print("Error in viewer average calculation")
        elif(inner_data["is_live"] == False):
            print(self.name + " is not live right now")
            print("Previous Game : " + result["game_name"])
        else:
            print("Error in updating activity status")
        self.initialize()
    
    def Tag_data(self):
        link = "https://api.twitch.tv/helix/streams/tags"
        request_head = {
        "client-id" : self.client,
        "Authorization" : self.token
        }
        parameters = {
        "broadcaster_id" : str(self.data["data"][0]["id"]),
        "first" : 100
        }
        response = requests.get(link, parameters, headers = request_head).json()
        inner_data = response["data"]
        result = []
        for i in range(len(inner_data)):
            if(inner_data[i]["is_auto"] == False):
                auto = "User Created"
            elif(inner_data[i]["is_auto"] == True):
                auto = "Auto Generated"
            else:
                auto = "No Result"
            result.append(auto + " : " + inner_data[i]["localization_names"]["en-us"])
        print(result)
        print(self.name + " has " + str(len(inner_data)) + " tags")
        self.initialize()
        
    def Game_numbers(self):
        data = self.getAPI(self.name, self.token)
        inner_data = data["data"][0]
        game_id = inner_data["game_id"]
        link = "https://api.twitch.tv/helix/streams"
        request_head = {
        "client-id" : self.client,
        "Authorization" : self.token
        }
        parameters = {
            "game_id" : game_id,
            "after" : "",
            "first" : 100
        }
        minimum = 9999999
        stop = True
        views_list = []
        viewers = 0
        while(stop):
            try:
                response = requests.get(link, parameters, headers = request_head).json()
                parameters["after"] = response["pagination"]["cursor"]
            except:
                stop = False
            data = response["data"]
            for i in range(len(data)):
                views_list.append(data[i]["viewer_count"])
                if(data[i]["user_name"] == self.name):
                    viewers = data[i]["viewer_count"]
                if(data[i]["viewer_count"] < minimum):
                    minimum = data[i]["viewer_count"]
                elif(data[i]["viewer_count"] > minimum):
                    stop = False
                
            if  parameters["after"] == None:
                stop = False
        
        parameters.pop("after", None)
        response = requests.get(link, parameters, headers = request_head).json()
        data = response["data"]
        result = {
            "streamer_count" : len(views_list),
            "viewer_count" : sum(views_list),
            "game_name" : data[0]["game_name"],
            "viewers" : viewers
        }
        return result
    
    def getToken(self):
        token_head = {
        "client_id" : self.client,
        "client_secret" : self.secret,
        "grant_type" : "client_credentials"
        }
        token_url = "https://id.twitch.tv/oauth2/token?client_id="+ token_head["client_id"]+"&client_secret="+ token_head["client_secret"]+"&grant_type="+ token_head["grant_type"]
        token_response = requests.post(token_url)
        return "Bearer " +token_response.json()["access_token"]


    
    def getAPI(self, name, token):
        name = name.lower()
        endpoint = "https://api.twitch.tv/helix/search/channels?query=" + name
        request_head = {
        "client-id" : self.client,
        "Authorization" : self.token
        }
        return requests.get(endpoint, headers = request_head).json()

def shortenFloat(value, end):
    value = str(value)
    start = value.find(".")
    if(len(value[start : len(value)]) > end):
        return float(str(value[0 : start]) + str(value[start: start + end+1]))
    else:
        return float(value)

    
def main():
    spookeh = account("SpuukehScary")
    spookeh.initialize()
    
if __name__ == "__main__":
    main()
