from bs4 import BeautifulSoup
import requests
import json
import codecs

#Function that gets data from IMDB
def getJSON(html):
	data = {}
        #Finds the title of the movie
	data['title'] =  html.find(itemprop='name').text.strip()
	#Finds the Rating of the Movie out of 10
	data['rating'] = html.find(itemprop='ratingValue').text
        #Gives the Rating of the Movie (PG-13, R Rated, Etc.)
	data['rated'] = html.find(itemprop='contentRating')['content']
	#Finds the Genres of the Movie
	tags = html.findAll("span",{"itemprop":"genre"})
	genres = []
	for genre in tags:
		genres.append(genre.text.strip())
	data['genre'] = genres	
        #Finds the Actors/Cast of the Movie
	tags = html.findAll(itemprop="actors")
	actors = []
	for actor in tags:
		actors.append(actor.text.strip().replace(',',''))
	data['cast'] = actors
	#Finds the Writers of Movie
	tags = html.findAll(itemprop="creator")
	creators = []
	for creator in tags:
		creators.append(creator.text.strip().replace(',',''))
	data['writers'] = creators	
	#Finds the Director of the Movie	
	directors = []
	tags = html.findAll(itemprop="director")
	for director in tags:
		directors.append(director.text.strip().replace(',',''))
	data['directors'] = directors
	#Returns the data from the function
	json_data = json.dumps(data)
	json_parsed=json.loads(json_data)
	return json_parsed

#Function that puts the URL through Beautiful Soup	
def getHTML(url):
	response = requests.get(url)
	return BeautifulSoup(response.content,'html.parser', from_encoding="utf-8")	
	
#Function that gets the URL
def getURL(input):
	try:
		if input[0] == 't' and input[1] == 't':
			html = getHTML('http://www.imdb.com/title/'+input+'/')
			
		else:
			html = getHTML('https://www.google.co.in/search?q='+input)
			for cite in html.findAll('cite'):
				if 'imdb.com/title/tt' in cite.text:
					html = getHTML('http://'+cite.text)
					break
		return getJSON(html)	
	except Exception as e:
		return 'Invalid input or Network Error!'

def printMoviesToFile(movie, moviecsv):
        #Gets Movie title
        input = movie
        #Prints prompt to wait
        print('Getting information, Please Wait....')
        #Gets Data of the Movie
        parsed=getURL(input)
        #Prints Details of the Movie onto the CSV File
        print('Title', input, file=moviecsv, sep=',')
        try: 
                print('Rating',parsed['rating'], '/10', file=moviecsv, sep=',')
                print('Certification', parsed['rated'], file=moviecsv, sep=',')
                print('Genre', file=moviecsv, end=',')
                for i in parsed['genre']:
                        print(i, file=moviecsv, end=',')
                print('\n', file=moviecsv, end='')
                print('Cast', file=moviecsv, end=',')
                for j in parsed['cast']:
                        j = j.encode('ascii', 'ignore').decode('ascii')
                print(j, file=moviecsv, end=',')
                print('\n', file=moviecsv, end='')
                print('Directors', file=moviecsv, end=',')
                for k in parsed['directors']:
                        print(k, file=moviecsv, end=',')
                print('\n', file=moviecsv, end='')
                print('Writers', file=moviecsv, end=',')
                for l in parsed['writers']:
                        l = l.encode('ascii', 'ignore').decode('ascii')
                        print(l, file=moviecsv, end=',')
                print('\n', file=moviecsv, end='')
                print('', file=moviecsv)
        except (UnicodeEncodeError, TypeError, UnboundLocalError):
                pass

def main():

        f = codecs.open('imdb_movie_titles.csv', mode='r', encoding='latin-1')
        moviecsv=codecs.open('moviecsv.csv', mode='w', encoding='latin-1')
        counter=0
        for line in f:
                counter+=1
                line=line.strip()
                print(line)
                printMoviesToFile(line, moviecsv)
                print(counter, 'Movies Completed')
        moviecsv.close()
        
                
main()
