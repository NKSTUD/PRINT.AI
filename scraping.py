from bs4 import BeautifulSoup
import requests


# Function to extract Product Title
def get_title(soup):
    try:
        # Outer Tag Object
        title = soup.find("span", attrs={"id": 'productTitle'})

        # Inner NavigatableString Object
        title_value = title.string

        # Title as a string value
        title_string = title_value.strip()

    # # Printing types of values for efficient understanding
    # print(type(title))
    # print(type(title_value))
    # print(type(title_string))
    # print()

    except AttributeError:
        title_string = ""

    return title_string


# Function to extract Product Price
def get_description(soup):
    try:
        description = soup.find("span", attrs={'id': 'productDescription_feature_div'}).string.strip()

    except AttributeError:

        try:
            # If there is some deal description
            description = soup.find("span", attrs={'id': 'descriptionblock_dealdescription'}).string.strip()

        except Exception:
            description = ""

    return description


# Function to extract Product Rating
def get_rating(soup):
    try:
        rating = soup.find("i", attrs={'class': 'a-icon a-icon-star a-star-4-5'}).string.strip()

    except AttributeError:

        try:
            rating = soup.find("span", attrs={'class': 'a-icon-alt'}).string.strip()
        except:
            rating = ""

    return rating


# Function to extract Number of User Reviews
def get_review_count(soup):
    try:
        review_count = soup.find("span", attrs={'id': 'acrCustomerReviewText'}).string.strip()

    except AttributeError:
        review_count = ""

    return review_count


# Function to extract Availability Status
def get_availability(soup):
    try:
        available = soup.find("div", attrs={'id': 'availability'})
        available = available.find("span").string.strip()

    except AttributeError:
        available = "Not Available"

    return available


if __name__ == '__main__':

    # Headers for request
    HEADERS = {
        'accept': '*/*',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36 Edg/101.0.1210.53',
        'Accept-Language': 'en-US,en;q=0.9,it;q=0.8,es;q=0.7',
        'referer': 'https://www.google.com/',
        'cookie': 'DSID=AAO-7r4OSkS76zbHUkiOpnI0kk-X19BLDFF53G8gbnd21VZV2iehu-w_2v14cxvRvrkd_NjIdBWX7wUiQ66f-D8kOkTKD1BhLVlqrFAaqDP3LodRK2I0NfrObmhV9HsedGE7-mQeJpwJifSxdchqf524IMh9piBflGqP0Lg0_xjGmLKEQ0F4Na6THgC06VhtUG5infEdqMQ9otlJENe3PmOQTC_UeTH5DnENYwWC8KXs-M4fWmDADmG414V0_X0TfjrYu01nDH2Dcf3TIOFbRDb993g8nOCswLMi92LwjoqhYnFdf1jzgK0'
    }

    # The webpage URL
    URL = "https://www.amazon.com/s?k=playstation+4&ref=nb_sb_noss_2"

    # HTTP Request
    webpage = requests.get(URL, headers=HEADERS)

    # Soup Object containing all data
    soup = BeautifulSoup(webpage.content, "lxml")

    # Fetch links as List of Tag Objects
    links = soup.find_all("a", attrs={'class': 'a-link-normal s-no-outline'})

    links_list = [link.get('href') for link in links]
    main_link = "https://www.amazon.com"
    for link in links_list:
        new_webpage = requests.get(main_link + link, headers=HEADERS)
        new_soup = BeautifulSoup(new_webpage.content, "lxml")
        # Function calls to display all necessary product information
        prompt = ''
        if main_link.endswith('fr'):
            prompt = f"Write an ad copy for product named {get_title(new_soup)} with features  in French fr ."
        else:
            prompt = "Write an ad copy for product named {product_name} with features  in French fr ."

        print("Product Title =", get_title(new_soup))
        print("Product Price =", get_description(new_soup))
        print("Product Rating =", get_rating(new_soup))
        print("Number of Product Reviews =", get_review_count(new_soup))
        print("Availability =", get_availability(new_soup))
