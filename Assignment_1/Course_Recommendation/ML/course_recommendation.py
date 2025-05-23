# -*- coding: utf-8 -*-
"""course_recommendation.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/132gEyR-Valaf2e8Gup5dMgcKLV58xVuk
"""

import pandas as pd
import numpy as np
import pickle

courses=pd.read_csv(r"venv_name\udemy_courses.csv")

courses.head()

#title
#is_paid
#num_subscribers
#level
#duration
#subject

courses["subject"].value_counts()

courses.info()

courses=courses[['course_title','url','is_paid','price','num_subscribers','level','content_duration','subject']]
courses['title']=courses['course_title'].copy()
courses['domain']=courses['subject'].copy()
courses['level']=courses['level'].copy()
courses['url']=courses['url'].copy()
courses['is_paid']=courses['is_paid'].copy()
courses['price']=courses['price'].copy()
courses.head()

courses.isnull().sum()

courses.duplicated().sum()

courses=courses.drop_duplicates()

courses['subject']=courses['subject'].str.replace(' ','')

courses.iloc[0]

courses['subject']=courses['subject'].apply(lambda x:x.split())
courses['subject'].apply(lambda x:[i.replace(" ","")for i in x])
courses.head()

courses['title']=courses['title'].apply(lambda x:x.split())
courses['title'].apply(lambda x:[i.replace(" ","")for i in x])



courses['course_level']=courses['level'].copy()

courses['level']=courses['level'].str.replace(' ','')

courses.head()

courses.head()

courses['durations']=courses['content_duration'].copy()

print(courses)

courses['is_paid'] = courses['is_paid'].astype(str)
courses['price'] = courses['price'].astype(str)
courses['num_subscribers'] = courses['num_subscribers'].astype(str)

courses['content_duration'] = courses['content_duration'].astype(str)

courses['num_subscribers']=courses['num_subscribers'].apply(lambda x:x.split())



courses['content_duration']=courses['content_duration'].apply(lambda x:x.split())

courses['is_paid']=courses['is_paid'].apply(lambda x:x.split())



courses['level']=courses['level'].apply(lambda x:x.split())
courses['level'].apply(lambda x:[i.replace(" ","")for i in x])
courses.head()

courses['course_level']=courses['course_level'].apply(lambda x:x.split())
courses['course_level'].apply(lambda x:[i.replace(" ","")for i in x])
courses.head()

courses.head()

courses['tags']=courses['is_paid']+courses['content_duration']+courses['subject']+courses['course_level']

newc = courses[['course_title','durations','domain','tags','level','url','is_paid','price']]
newc

newc['tags'] = newc['tags'].apply(lambda x:" ".join(x))

newc.head()

from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features = 3679,stop_words = 'english')

vectors = cv.fit_transform(newc['tags']).toarray()
vectors

cv.get_feature_names_out()

"""from sklearn.metrics.pairwise import cosine_similarity
similarity = cosine_similarity(vectors)
"""

from sklearn.metrics.pairwise import cosine_similarity
similarity=cosine_similarity(vectors)

print(similarity)

def recommend(domain, min_duration=None, max_duration=None,level = 'AllLevels'):
    index = newc[newc['domain'] == domain].index

    if len(index) == 0:
        print("Course not found.")
        return []

    index = index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

    recommended_courses = []

    for i in distances[1:]:  
        course_index = i[0]
        course_duration = newc.iloc[course_index]['durations']
        course_level = newc.iloc[course_index]['level'][0]

        if (min_duration is None or course_duration >= min_duration) and \
           (max_duration is None or course_duration <= max_duration) and \
           (level in course_level):
            recommended_courses.append({
                'course_title': newc.iloc[course_index]['course_title'],
                'duration': course_duration,
                'level': course_level,
                'url': courses.iloc[course_index]['url'] , # Get URL from original courses dataframe
                'is_paid': courses.iloc[course_index]['is_paid'],  # Get is_paid status from original courses dataframe
                'price': courses.iloc[course_index]['price']
            })

        if len(recommended_courses) >= 30:
            break

    # if recommended_courses:
    #     print("Recommended courses:")
    #     for count, course in enumerate(recommended_courses, start=1):
    #         print(f"{count}. Course Name: {course['course_title']}")
    #         print(f"   Duration: {course['duration']}")
    #         print(f"   Course Level: {course['level']}")
    #         print(f"   URL: {course['url']}")
    # else:
    #     print("No courses found within the specified duration range.")

    

# Call the function with a course title and optional duration range
# recommend("Web Development", min_duration=1, max_duration=2,level = "BeginnerLevel")
pickle.dump(newc,open('model.pkl','wb'))
model=pickle.load(open('model.pkl','rb'))
pickle.dump(similarity,open('similarity.pkl','wb'))