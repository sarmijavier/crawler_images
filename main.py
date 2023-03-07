from bs4 import BeautifulSoup
import urllib3
import sys
import json 

http = urllib3.PoolManager()


def get_page(url: str, depth: int) -> None:
	"""
	Get the page(s) and get the images and links.

	Parameters:
	url (string): the main url
	depth (int): How mane pages the crawler are going to visit

	Return:
	it doesn't return anything but creates a json file with result
	"""

	response = http.request('GET', url)
	soup = BeautifulSoup(response.data, 'html.parser')
	links = get_links_to_pages(soup)
	images = get_url_images(soup)
	count_depth = 0

	dict_result = {
		'results':[
			{
				'imageUrl': f'url{images[0]}',
				'sourceUrl': url,
				'depth': count_depth
			}
		] 
	}

	list_results_aux = [] 

	for i in range(depth - 1):
		response = http.request('GET', f'{url}{links[i]}')
		soup = BeautifulSoup(response.data, 'html.parser')
		links_page = get_links_to_pages(soup)
		images_page = get_url_images(soup)
		count_depth = count_depth + 1
		dict_page = {
			'imageUrl': f'{url}{images_page[0]}',
			'sourceUrl': f'{url}{links_page[i]}',
			'depth': count_depth
		}
		list_results_aux.append(dict_page)

	dict_result['results'].append(list_results_aux)	

	with open('result.json', 'w') as fp:
		json.dump(dict_result, fp)	
        

def get_links_to_pages(soup: object) -> None:
	links = [link.get('href') for link in soup.findAll('a')]
	return links


def get_url_images(soup: object) -> None:
	images = [img.get('src') for img in soup.findAll('img')]
	return images


if __name__ == '__main__':
	print('''
	Welcome to the crawler!
	Please make sure to add the next arguments as the example:
	python main.py https://urltocrawl how_many_pages_to_crawl
	https://www.davivienda.com/wps/portal/personas/nuevo', 3
	'''
	)

	arguments = sys.argv
	if len(arguments) == 3:	
		url = arguments[1]
		depth = abs(int(arguments[2]))
		import pdb ; pdb.set_trace()
		get_page(url, depth)
	else:
		print('please make sure to follow the instructions above')
    
