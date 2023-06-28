import requests
from bs4 import BeautifulSoup
import regex as re
import random


def create_wiki_links(number, starting_link, seed):
    """
    Return a list of random links to Wikipedia articles.
    Also creates a file of these links for reference.
    """

    random.seed(seed)

    link_list = [starting_link]
    article_string = ''
    link = starting_link

    # If any of these are part of a Wiki link,
    # it does not lead to an Italian article.
    not_wanted_list = [
        'https',
        'File',
        'Categoria',
        'Aiuto',
        'Portale',
        'Template',
        'Wikipedia:',
        'Discussione']

    # Looks through the article and finds a link to another
    for n in range(number + 1):
        page = requests.get(link)

        soup = BeautifulSoup(page.content, 'html.parser')

        title = soup.find("title")
        print(title.text)
        article_string += (
            '\n'
            + title.text
            + ": "
            + link)

        # print(soup)

        allLinks = soup.find(id="bodyContent").find_all("a")
        random.shuffle(allLinks)

        if n == number:
            break

        for ran_link in allLinks:
            # We are only interested in other Wiki articles
            link_status = 0     # Stays 0 if ran_link is a Wiki link
            try:
                if ran_link['href'].find("/wiki/") == -1:
                    link_status = 1
            except KeyError:
                continue
            for not_wanted in not_wanted_list:
                if ran_link['href'].find(not_wanted) != -1:
                    link_status = 1
            if link_status == 1:
                continue

            # Add this link to our scraping list
            ran_link = str(ran_link['href'])
            ran_link = 'https://it.wikipedia.org/' + ran_link
            print(ran_link)
            link_list.append(ran_link)
            link = ran_link
            break

    with open('article_list.txt', 'a', encoding='utf-8') as file:
        file.write(article_string)

    return link_list


def scrape_wiki_discussions(link_list):
    """
    Takes a list of Wiki links (to the articles)
    and returns the discussion texts as a string.
    """

    topics_dict = {}

    for link in link_list:

        link = re.sub(
            'https://it.wikipedia.org//wiki/',
            'https://it.wikipedia.org//wiki/Discussione:',
            link)
        print(link)

        page = requests.get(link)
        soup = BeautifulSoup(page.content, 'html.parser')

        title_list = soup.body.find_all(
            'h2',
            attrs={'class': 'ext-discussiontools-init-section'})
        title_strings = []
        for title in title_list:
            if title.text is not None:
                text = title.text
                title_strings.append(text)

        # paragraph_list = soup.body.find_all('p')
        # comment_strings = []
        # for paragraph_list in paragraph_list:
        #    if title.text is not None:
        #        text = title.text
        #        comment_strings.append(text)

        #print(title_strings)
        # print(comment_strings)

        # HTML text to string, removing what is not part of the discussion
        body_str = (soup.body.text)
        body_str = body_str.replace(
            """Da Wikipedia, l'enciclopedia libera.
            \n\n\n\nJump to navigation
            \nJump to search""",
            "")
        body_str = re.sub(
            'Estratto da "https://it.wikipedia.org/.*"$.*sui cookie',
            '', body_str,
            flags=re.DOTALL | re.M)

        # Use title_list to split the string at the discussion topic title
        # and cleaning up the titles.
        new_title_list = []
        for title in title_strings:
            new_title = (
                'Titolo: '
                + title.replace('[modifica wikitesto]', '')
                + '\n')
            body_str = body_str.replace(title, '\n###' + new_title)
            new_title_list.append(new_title)

        topic_list = body_str.split('###')
        topic_list = topic_list[1:]

        # print(topic_list)

        try:
            topic_dict = {}
            for i, topic in enumerate(topic_list):
                topic = topic.replace(new_title_list[i], '')
                topic_dict[new_title_list[i].replace('\n', '')] = topic

            # Eliminating Wiki discussion topics without the option to respond,
            # just because it is difficult to split into individual comments.
            for topic in list(topic_dict):
                if 'Rispondi[rispondi]' not in topic_dict[topic]:
                    topic_dict.pop(topic, None)

            # Now we can split topics into individual comments
            # unsing the respond button, creating a list for every topic.
            for topic in topic_dict:
                comment_list = topic_dict[topic].split('Rispondi[rispondi]')
                topic_dict[topic] = comment_list

            new_key_dict = {}
            article_title = ''
            for key in topic_dict:
                new_key = re.search('Discussione:.*$', body_str, flags=re.M)
                if new_key:
                    article_title = new_key.group(0)
                    new_key = article_title + ', ' + key
                    #print(new_key)
                new_key_dict[new_key] = key

            for new_key in new_key_dict:
                if new_key_dict[new_key] in topic_dict:
                    key = new_key_dict[new_key]
                    topic_dict[new_key] = topic_dict[key]
                    topic_dict.pop(key, None)

            #print(topic_dict)
            topics_dict = topics_dict | topic_dict

        except IndexError:
            print('Error')

    return topics_dict


seed = 1998     # Use 1998 for consistent results

# Wipes the file from previous runs of the code
with open('article_list.txt', 'w', encoding='utf-8') as file:
    file.write('')


# Allows for a variable number of starting points (max 12).
n_starting_points = 0
link_list = [
    'https://it.wikipedia.org//wiki/Polizia',
    'https://it.wikipedia.org//wiki/Transgender',
    'https://it.wikipedia.org//wiki/Cambiamento_climatico',
    'https://it.wikipedia.org//wiki/Nazionalsocialismo',
    'https://it.wikipedia.org//wiki/Roma',
    'https://it.wikipedia.org//wiki/I_promessi_sposi',
    'https://it.wikipedia.org//wiki/Bibbia',
    'https://it.wikipedia.org//wiki/Guerra',
    'https://it.wikipedia.org//wiki/Sigmund_Freud',
    'https://it.wikipedia.org//wiki/Taylor_Swift',
    'https://it.wikipedia.org//wiki/Napoleone_Bonaparte',
    'https://it.wikipedia.org//wiki/Vegetarianismo',
    'https://it.wikipedia.org//wiki/Russia',
    'https://it.wikipedia.org//wiki/Black_Lives_Matter',
    'https://it.wikipedia.org//wiki/Colonialismo_italiano'
    'https://it.wikipedia.org//wiki/Terrorismo',
    'https://it.wikipedia.org//wiki/Intelligenza',
    'https://it.wikipedia.org//wiki/Energia_nucleare']

link_list = link_list[n_starting_points:]

comment_dict = {}
for link in link_list:
    #single_dict = scrape_wiki_discussions(
    #    create_wiki_links(100, link, seed))
    #comment_dict = comment_dict | single_dict
    create_wiki_links(100, link, seed)

# scrape_wiki_discussions(create_wiki_links(50, link_list[2], seed))

with open('dict_output2.txt', 'w', encoding='utf-8') as convert_file:
    convert_file.write(str(comment_dict))
