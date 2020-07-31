from donbot import Donbot
from lxml import html, cssselect
from getvotes import GetVotes
import numpy as np
import pandas as pd
import texthero as hero

obj = GetVotes(username="Auro", password="*")

target_user = "Auro"

#City that never sleeps, BoTC, White flag, Newbie 1900, Mini 2040
town_threads = ["https://forum.mafiascum.net/viewtopic.php?p=11778017", "https://forum.mafiascum.net/viewtopic.php?p=11838042", "https://forum.mafiascum.net/viewtopic.php?f=150&t=81775", "https://forum.mafiascum.net/viewtopic.php?f=50&t=77781", "https://forum.mafiascum.net/viewtopic.php?f=53&t=77634"]

#Covid game, Downtown train, Nomination Mafia, Jungle Republic, Newbie 1893, Newbie 1898, Crown of Misery
scum_threads = ["https://forum.mafiascum.net/viewtopic.php?f=3&t=82957", "https://forum.mafiascum.net/viewtopic.php?f=54&t=78257", "https://forum.mafiascum.net/viewtopic.php?f=52&t=78999", "https://forum.mafiascum.net/viewtopic.php?f=52&t=78634", "https://forum.mafiascum.net/viewtopic.php?f=50&t=77453", "https://forum.mafiascum.net/viewtopic.php?f=50&t=77673", "https://forum.mafiascum.net/viewtopic.php?f=52&t=78009"]

#Game of Thrones
unknown_threads = ["https://forum.mafiascum.net/viewtopic.php?f=3&t=83318"]

posts_town = []
posts_scum = []
posts_unknown = []

for thread in town_threads:
    posts_town.append(obj.getISOs(usernames = [target_user], thread=thread))

for thread in scum_threads:
    posts_scum.append(obj.getISOs(usernames = [target_user], thread=thread))

for thread in unknown_threads:
    posts_unknown.append(obj.getISOs(usernames = [target_user], thread=thread))

df = pd.DataFrame()

#Try to make a pd dataframe with the second column as "town" for the town game
for posts in posts_town:
    df_temp = pd.DataFrame([[post, "town"] for post in posts])
    df = df.append(df_temp, ignore_index=True)

for posts in posts_scum:
    df_temp = pd.DataFrame([[post, "scum"] for post in posts])
    df = df.append(df_temp, ignore_index=True)

for posts in posts_unknown:
    df_temp = pd.DataFrame([[post, "unknown"] for post in posts])
    df = df.append(df_temp, ignore_index=True)

df.columns = ['text', 'alignment']
print(df)

#Clean, tf-idf score, and TSNE
df['tsne'] = (
            df['text']
            .pipe(hero.clean)
            .pipe(hero.tfidf)
            .pipe(hero.tsne)
   )

#Plot!
hero.scatterplot(df, col='tsne', color='alignment', title="What am I doing?")
