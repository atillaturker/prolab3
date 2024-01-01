import json
import networkx as nx
import matplotlib.pyplot as plt
from collections import Counter

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
    
class InterestMatcher:
    def __init__(self):
        self.users = {}
        self.interests_hash = {}

    def add_user(self, user):
        self.users[user.username] = user
        self.update_interests_hash(user)

    def update_interests_hash(self, user):
        for tweet in user.tweets:
            words = tweet.split()
            word_freq = Counter(words)

            for word, freq in word_freq.items():
                if freq > 1:
                    if word not in self.interests_hash:
                        self.interests_hash[word] = []

                    self.interests_hash[word].append(user.username)

    def find_common_interests(self, user1, user2):
        common_interests = set(user1.tweets) & set(user2.tweets)
        return common_interests

    def match_users(self):
        matches = []

        for username1, user1 in self.users.items():
            for username2, user2 in self.users.items():
                if username1 != username2:
                    common_interests = self.find_common_interests(user1, user2)

                    if common_interests:
                        matches.append((username1, username2, common_interests))

        return matches
    

# Önce data.json dosyasını okuyalım
with open('data.json', 'r', encoding='utf-8') as file:
    user_data = json.load(file)

# Şimdi her bir kullanıcı için bir nesne oluşturalım ve hash tablosunda tutalım
user_table = UserHashTable()
# Şimdi her bir kullanıcı için bir nesne oluşturalım ve eşleştirme algoritması için kullanıcıları ekleyelim
interest_matcher = InterestMatcher()

for user_info in user_data:
    user_object = User(**user_info)
    user_table.add_user(user_object)
    interest_matcher.add_user(user_object)
# Şimdi users hash tablosunda her bir kullanıcının bilgilerini bulabilirsiniz
# Örneğin, kullanıcı adı 'burcu06' olan kullanıcının bilgilerine şu şekilde erişebilirsiniz:
user_ymohr = user_table.get_user('ymohr')
print(user_ymohr.username)
print(user_ymohr.name)


# Tüm kullanıcılar arasındaki takipçi-takip edilen ilişkileri içeren bir graf oluşturun
full_graph_edges = []

for user in user_table.users.values():
    for follower in user.followers:
        full_graph_edges.append((user.username, follower))
    for followed in user.following:
        full_graph_edges.append((user.username, followed))

# Grafı oluştur
full_graph = nx.DiGraph()  # Yönlü graf kullanıyoruz (DiGraph)
full_graph.add_edges_from(full_graph_edges)

# Belirli bir kullanıcı adını tanımlayın
target_username = 'georgiana.auer'

# Belirli kullanıcının çevresindeki ilişkileri içeren bir alt graf oluşturun
subgraph_edges = []

for user in user_table.users.values():
    if user.username == target_username or user.username in user.followers or user.username in user.following:
        for follower in user.followers:
            subgraph_edges.append((user.username, follower))
        for followed in user.following:
            subgraph_edges.append((user.username, followed))

# Alt grafı oluştur
subgraph = nx.DiGraph()  # Yönlü graf kullanıyoruz (DiGraph)
subgraph.add_edges_from(subgraph_edges)

# Alt grafı görselleştir
pos = nx.spring_layout(subgraph)
nx.draw(subgraph, pos, with_labels=True, font_size=6, node_size=50, arrowsize=5)
#plt.show()

# İlgi alanlarını ve paylaşan kullanıcıları göster
#for interest, users in interest_matcher.interests_hash.items():
#   print(f"Interest: {interest}, Users: {users}")
# İlgili kısımları InterestMatcher sınıfına ekleyin
matches = interest_matcher.match_users()

# Ortak ilgi alanlarına sahip kullanıcıları göster
for match in matches:
    user1_username, user2_username, common_interests = match
    print(f"Users {user1_username} and {user2_username} have common interests:")
    for interest in common_interests:
        print(f"  - {interest}")
