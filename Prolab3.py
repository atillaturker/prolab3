import json
import networkx as nx
import matplotlib.pyplot as plt
from collections import Counter
from colorama import Fore, Style, init
from collections import defaultdict

class User:
    def __init__(self, username, name, followers_count, following_count, language, region, tweets, following, followers):
        self.username = username
        self.name = name
        self.followers_count = followers_count
        self.following_count = following_count
        self.language = language
        self.region = region
        self.tweets = tweets
        self.following = following
        self.followers = followers

class UserHashTable:
    def __init__(self):
        self.users = {}

    def add_user(self, user):
        self.users[user.username] = user

    def get_user(self, username):
        return self.users.get(username, None)
    

class InterestAnalyzer:
    def __init__(self):
        self.interests_hash = defaultdict(list)

    def analyze_tweets(self, user_table):
        for user in user_table.users.values():
            user_interests = set()
            for tweet in user.tweets:
                words = tweet.split()
                for word in words:
                    user_interests.add(word)

            for interest in user_interests:
                self.interests_hash[interest].append(user.username)

    def search_interest(self, interest):
        return self.interests_hash.get(interest, [])   


with open('data.json', 'r', encoding='utf-8') as file:
    user_data = json.load(file)


user_table = UserHashTable()


for user_info in user_data:
    user_object = User(**user_info)
    user_table.add_user(user_object)


# Örneğin, kullanıcı adı 'verna91' olan kullanıcının bilgileri
user_target= user_table.get_user('verna91')
#print(f"{Fore.GREEN}user name:{Style.RESET_ALL} {Fore.WHITE}{user_target.username}")
#print(f"{Fore.GREEN}name: {Style.RESET_ALL}{Fore.WHITE}{user_target.name}")
#print(f"{Fore.GREEN}language: {Style.RESET_ALL}{Fore.WHITE}{user_target.language}")
#print(f"{Fore.GREEN}user followers: {Style.RESET_ALL}{Fore.WHITE}{user_target.followers}")
#print(f"{Fore.GREEN}user following: {Style.RESET_ALL}{Fore.WHITE}{user_target.following}")

# Tüm kullanıcılar arasındaki takipçi-takip edilen ilişkileri içeren bir graf oluşturun
full_graph_edges = []

for user in user_table.users.values():
    for follower in user.followers:
        full_graph_edges.append((user.username, follower))
    for followed in user.following:
        full_graph_edges.append((user.username, followed))

# Graf
full_graph = nx.DiGraph()  # Yönlü graf kullanıyoruz (DiGraph)
full_graph.add_edges_from(full_graph_edges)

# Belirli bir kullanıcı
target_username = 'lillie.hegmann'

# Belirli kullanıcının çevresindeki ilişkileri içeren bir alt graf 
subgraph_edges = []

for user in user_table.users.values():
    if user.username == target_username or user.username in user.followers or user.username in user.following:
        for follower in user.followers:
            subgraph_edges.append((user.username, follower))
        for followed in user.following:
            subgraph_edges.append((user.username, followed))

# Alt graf
subgraph = nx.DiGraph()  # Yönlü graf
subgraph.add_edges_from(subgraph_edges)

# Alt grafı görselleştirme
pos = nx.spring_layout(subgraph)
nx.draw(subgraph, pos, with_labels=True, font_size=6, node_size=50, arrowsize=5)
plt.show()

interest_analyzer = InterestAnalyzer()


interest_analyzer.analyze_tweets(user_table)

for interest, users in interest_analyzer.interests_hash.items():
    print(f"Interest: {interest}") #Users: {users}


interest_analyzer = InterestAnalyzer()


interest_analyzer.analyze_tweets(user_table)


searched_interest = 'ahlat'
users_with_interest = interest_analyzer.search_interest(searched_interest)

print(f"Users interested in '{searched_interest}': {users_with_interest}")    



