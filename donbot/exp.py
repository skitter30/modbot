from donbot import Donbot
from lxml import html, cssselect
from getvotes import GetVotes
import numpy as np
import pandas as pd
import texthero as hero

obj = GetVotes(username="skitter30", password="*")

target_user = "Auro"

#City that never sleeps, BoTC, White flag, Newbie 1900, Mini 2040
threads = {
                # town
        'name': ['city', 'botc', 'white flag', 'newbie 1900', 'mini 2040', \
                 # scum
                 'covid', 'downtown train', 'nomination mafia', 'jungle republic', 'newbie 1893', 'newbie 1898', 'crown of misery', 
                 # 'unknown'
                 'game of thrones'],
                 
                 # town 
        'thread': ["https://forum.mafiascum.net/viewtopic.php?f=54&t=82824", \
                   "https://forum.mafiascum.net/viewtopic.php?f=84&t=83094", \
                   "https://forum.mafiascum.net/viewtopic.php?f=150&t=81775", \
                   "https://forum.mafiascum.net/viewtopic.php?f=50&t=77781", \
                   "https://forum.mafiascum.net/viewtopic.php?f=53&t=77634",
                   # scum
                   "https://forum.mafiascum.net/viewtopic.php?f=3&t=82957", \
                   "https://forum.mafiascum.net/viewtopic.php?f=54&t=78257", \
                   "https://forum.mafiascum.net/viewtopic.php?f=52&t=78999", \
                   "https://forum.mafiascum.net/viewtopic.php?f=52&t=78634", \
                   "https://forum.mafiascum.net/viewtopic.php?f=50&t=77453", \
                   "https://forum.mafiascum.net/viewtopic.php?f=50&t=77673", \
                   "https://forum.mafiascum.net/viewtopic.php?f=52&t=78009",
                   # 'unknown'
                   "https://forum.mafiascum.net/viewtopic.php?f=3&t=83318"],
                   
        'alignment': ['town', 'town', 'town', 'town', 'town',
                      'scum', 'scum', 'scum', 'scum', 'scum', 'scum', 'scum', 
                      'unknown']
            }

threads = pd.DataFrame(threads, columns = ['name', 'thread', 'alignment'])

temp_posts = []
df = pd.DataFrame()

for ind in threads.index:
    temp_posts = []
    temp_posts.append(obj.getISOs(usernames = [target_user], thread=threads['thread'][ind]))
    for posts in temp_posts:
        temp_df = pd.DataFrame([[post, threads['alignment'][ind], threads['name'][ind]] for post in posts])
    df = df.append(temp_df, ignore_index = True)

df.columns = ['text', 'alignment', 'game']
df.to_csv (r'file.path', index = False, header=True)

#Clean, tf-idf score, and TSNE
df['tsne'] = (
            df['text']
            .pipe(hero.clean)
            .pipe(hero.tfidf)
            .pipe(hero.tsne)
   )

#Plot!
hero.scatterplot(df, col='tsne', color='alignment', title="What am I doing?")
