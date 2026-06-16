import pandas as pd

df = pd.read_csv("netflix_titles.csv", encoding="latin1")

print(df.head())

#unwanted coloums remove
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
print(df.head())
print(df.shape)

#understand the data
print(df.shape)      # rows & columns
print(df.columns)    # column names
print(df.info())     # data types

#data cleaning 
# Missing values fill
df.fillna("Unknown", inplace=True)

# date_added ko datetime me convert
df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')

# Year column create
df['year_added'] = df['date_added'].dt.year

# 1) movies vs tv shows
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style("whitegrid")

type_counts = df['type'].value_counts()

plt.figure()
plt.pie(type_counts, labels=type_counts.index, autopct='%1.1f%%', startangle=90)

# donut hole
centre_circle = plt.Circle((0,0),0.70,fc='white')
fig = plt.gcf()
fig.gca().add_artist(centre_circle)

plt.title("Distribution of Movies vs TV Shows", fontsize=14)
plt.show()

#hypotheses 1:
#movies are more than TV shows
movies = df[df['type'] == 'Movie'].shape[0]
tv = df[df['type'] == 'TV Show'].shape[0]

print("Movies:", movies)
print("TV Shows:", tv)

#conclusion
if movies > tv:
    print("Hypothesis True: Movies are more than TV Shows")
else:
    print("Hypothesis False")

# 2) content added per year
year_data = df['year_added'].value_counts().sort_index()

plt.figure()
plt.plot(year_data.index, year_data.values, marker='o', linestyle='-')

plt.title("Trend of Content Added Over Years", fontsize=14)
plt.xlabel("Year")
plt.ylabel("Number of Shows")
plt.grid(True)

plt.show()

#hypotheses 2:
#content increase in recent year
df['year_added'] = pd.to_datetime(df['date_added']).dt.year

year_counts = df['year_added'].value_counts().sort_index()

print(year_counts)

# 3) top countries
import plotly.express as px

# country data clean karo (multiple countries split karne ke liye)
country_df = df['country'].str.split(',', expand=True).stack().reset_index(level=1, drop=True)
country_df = country_df.str.strip()

# count
country_counts = country_df.value_counts().reset_index()
country_counts.columns = ['country', 'count']

# map plot
fig = px.choropleth(
    country_counts,
    locations="country",
    locationmode="country names",
    color="count",
    title="Netflix Content by Country",
)

fig.show()

# 4) Rating distribution
plt.figure()

sns.countplot(
    y='rating',
    data=df,
    order=df['rating'].value_counts().index,
    palette='coolwarm'   #color add
)

plt.title("Content Rating Distribution", fontsize=14)
plt.xlabel("Count")
plt.ylabel("Rating")

plt.show()

#hypotheses 3:
#TV-MA is a common rating
top_rating = df['rating'].value_counts().idxmax()
print("Most common rating:", top_rating)

# 5) top geners
genre_data = df['listed_in'].str.split(',', expand=True).stack()

top_genres = genre_data.value_counts().head(10)
plt.figure()
top_genres.plot(
    kind='bar',
    color=plt.cm.viridis(range(len(top_genres)))  #gradient colors
)

plt.title("Top 10 Genres on Netflix", fontsize=14)
plt.xlabel("Genre")
plt.ylabel("Count")
plt.xticks(rotation=45)

plt.show()

# 6) movie duration
movies = df[df['type'] == 'Movie'].copy()

movies['duration'] = movies['duration'].str.replace(' min', '')
movies['duration'] = pd.to_numeric(movies['duration'], errors='coerce')

plt.figure()

sns.histplot(
    movies['duration'],
    bins=20,
    kde=True,
    color='purple'   #color change
)

plt.title("Distribution of Movie Durations", fontsize=14)
plt.xlabel("Duration (minutes)")
plt.ylabel("Frequency")

plt.show()

#hypotheses 4:
#Duration of Movies is more than Tv shows
avg_duration = movies['duration'].mean()

print("Average movie duration:", avg_duration)
