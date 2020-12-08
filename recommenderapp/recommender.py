from random import randrange


movies = [
    {
        'title':"Toy Story",
        'year':"1995",
        'filename':"images/movies/1.jpg"
    },
    {
        'title':"Jumanji",
        'year':"1995",
        'filename': "images/movies/2.jpg"
    },
    {
        'title':"Gumpy Old Men",
        'year':"1995",
        'filename': "images/movies/3.jpg"
    },
    {
        'title':"Waiting to Exhale",
        'year':"1995",
        'filename': "images/movies/4.jpg"
    },
    {
        'title':"Father of the Bride Part II",
        'year':"1995",
        'filename': "images/movies/5.jpg"
    },
    {
        'title':"Heat",
        'year':"1995",
        'filename': "images/movies/6.jpg"
    },
    {
        'title':"Sabrina",
        'year':"1995",
        'filename': "images/movies/7.jpg"
    },
    {
        'title':"Tom and Huck",
        'year':"1995",
        'filename': "images/movies/8.jpg"
    },
    {
        'title':"Sudden Death",
        'year':"1995",
        'filename': "images/movies/9.jpg"
    },
    {
        'title':"GoldenEye",
        'year':"1995",
        'filename': "images/movies/10.jpg"
    },
    {
        'title':"American President, The",
        'year':"1995",
        'filename': "images/movies/11.jpg"
    }

]

def getBestByCategory(category):
    rm=randrange(len(movies)+1)
    print(rm)
    return movies[:rm]