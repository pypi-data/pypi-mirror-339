import requests
import pandas as pd
from bs4 import BeautifulSoup
import pysbd
from datetime import datetime, timedelta
import wide_analysis.data.collect_data_new as collect_data_new

####To Collect from the new dates ###


def extract_div_contents_from_page(url, date):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error: Received status code {response.status_code} for URL: {url}")
        return pd.DataFrame(columns=['date','title','text_url','deletion_discussion','label','confirmation','discussion','verdict'])

    soup = BeautifulSoup(response.content, 'html.parser')
    heading_divs = soup.find_all('div', class_='mw-heading mw-heading3')

    data_rows = []
    for i, heading_div in enumerate(heading_divs):
        h3_tag = heading_div.find('h3')
        if not h3_tag:
            continue
        title_anchor = h3_tag.find('a')
        if not title_anchor:
            continue

        title = title_anchor.get_text(strip=True)
        text_url = 'https://en.wikipedia.org' + title_anchor.get('href', '')
        discussion_html = ""
        next_heading_div = heading_divs[i+1] if i + 1 < len(heading_divs) else None

        sibling = heading_div.next_sibling
        while sibling and sibling != next_heading_div:
            discussion_html += str(sibling)
            sibling = sibling.next_sibling
        label = ""
        confirmation = ""
        parts = discussion_html.split('<div class="mw-heading mw-heading3">')
        discussion_part = parts[0] if len(parts) > 0 else ''
        verdict_part = '<div class="mw-heading mw-heading3">' + parts[1] if len(parts) > 1 else ''
        data_rows.append([
            date,
            title,
            text_url,
            discussion_html,  
            label,
            confirmation,
            discussion_part,
            verdict_part
        ])
    df = pd.DataFrame(data_rows, columns=[
        'date', 'title', 'text_url', 'deletion_discussion',
        'label', 'confirmation', 'discussion', 'verdict'
    ])
    return df

########################################


def extract_div_contents_with_additional_columns(url, log_date):
    response = requests.get(url)
    if response.status_code != 200:
        return pd.DataFrame(columns=['log_date', 'title', 'text_url', 'deletion_discussion', 'label', 'confirmation', 'verdict', 'discussion'])

    soup = BeautifulSoup(response.content, 'html.parser')
    div_classes = ['boilerplate afd vfd xfd-closed', 'boilerplate afd vfd xfd-closed archived mw-archivedtalk']
    divs = []
    for div_class in div_classes:
        divs.extend(soup.find_all('div', class_=div_class))
    url_fragment = url.split('#')[-1].replace('_', ' ')
    data = []
    for div in divs:
        title_tag = div.find('a')
        if title_tag:
            title_span = div.find('span', {'data-mw-comment-start': True})
            if title_span:
                title_anchor = title_span.find_next_sibling('a')
                if title_anchor:
                    title = title_anchor.text
                    text_url = 'https://en.wikipedia.org' + title_anchor['href']
            else:
                title = title_tag.text
                text_url = 'https://en.wikipedia.org' + title_tag['href']
                
            deletion_discussion = div.prettify()

            # Extract label
            label = ''
            verdict_tag = div.find('p')
            if verdict_tag:
                label_b_tag = verdict_tag.find('b')
                if label_b_tag:
                    label = verdict_tag.prettify()

            # Extract confirmation
            confirmation = ''
            discussion_tag = div.find('dd').find('i')
            if discussion_tag:
                confirmation_b_tag = discussion_tag.find('b')
                if confirmation_b_tag:
                    confirmation = discussion_tag.prettify()

        
            parts = deletion_discussion.split('<div class="mw-heading mw-heading3">')
            discussion = parts[0] if len(parts) > 0 else ''
            verdict = '<div class="mw-heading mw-heading3">' + parts[1] if len(parts) > 1 else ''
            data.append([log_date, title, text_url, deletion_discussion, label, confirmation, discussion, verdict])
    df = pd.DataFrame(data, columns=['log_date', 'title', 'text_url', 'deletion_discussion', 'label', 'confirmation', 'verdict', 'discussion'])
    return df


def extract_div_contents_from_url(url,date):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error: Received status code {response.status_code} for URL: {url}")
        return pd.DataFrame(columns=['date','title', 'text_url', 'deletion_discussion', 'label', 'confirmation', 'discussion', 'verdict'])

    soup = BeautifulSoup(response.content, 'html.parser')
    div_classes = ['boilerplate afd vfd xfd-closed', 'boilerplate afd vfd xfd-closed archived mw-archivedtalk']
    divs = []
    for div_class in div_classes:
        divs.extend(soup.find_all('div', class_=div_class))
    url_fragment = url.split('#')[-1].replace('_', ' ')
    log_date = url.split('/')[-1]


    data = []
    for div in divs:
        try:
            title = None
            text_url = None
            title_tag = div.find('a')
            if title_tag:
                title_span = div.find('span', {'data-mw-comment-start': True})
                if title_span:
                    title_anchor = title_span.find_next_sibling('a')
                    if title_anchor:
                        title = title_anchor.text
                        text_url = 'https://en.wikipedia.org' + title_anchor['href']
                else:
                    title = title_tag.text
                    text_url = 'https://en.wikipedia.org' + title_tag['href']

            if title == 'talk page' or title is None:
                heading_tag = div.find('div', class_='mw-heading mw-heading3')
                if heading_tag:
                    title_tag = heading_tag.find('a')
                    if title_tag:
                        title = title_tag.text
                        text_url = 'https://en.wikipedia.org' + title_tag['href']

            if not title:
                continue
            if title.lower() != url_fragment.lower():
                continue  
            deletion_discussion = div.prettify()
            label = ''
            verdict_tag = div.find('p')
            if verdict_tag:
                label_b_tag = verdict_tag.find('b')
                if label_b_tag:
                    label = label_b_tag.text.strip()
            confirmation = ''
            discussion_tag = div.find('dd')
            if discussion_tag:
                discussion_tag_i = discussion_tag.find('i')
                if discussion_tag_i:
                    confirmation_b_tag = discussion_tag_i.find('b')
                    if confirmation_b_tag:
                        confirmation = confirmation_b_tag.text.strip()
            parts = deletion_discussion.split('<div class="mw-heading mw-heading3">')
            discussion = parts[0] if len(parts) > 0 else ''
            verdict = '<div class="mw-heading mw-heading3">' + parts[1] if len(parts) > 1 else ''

            data.append([date,title, text_url, deletion_discussion, label, confirmation, verdict, discussion])
        except Exception as e:
            print(f"Error processing div: {e}")
            continue

    df = pd.DataFrame(data, columns=['date', 'title', 'text_url', 'deletion_discussion', 'label', 'confirmation', 'discussion', 'verdict'])
    return df




def extract_div_contents_from_url_new(url,date):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error: Received status code {response.status_code} for URL: {url}")
        return pd.DataFrame(columns=['date', 'title', 'text_url', 'deletion_discussion', 'label', 'confirmation', 'discussion', 'verdict'])

    soup = BeautifulSoup(response.content, 'html.parser')
    div_classes = ['boilerplate afd vfd xfd-closed', 'boilerplate afd vfd xfd-closed archived mw-archivedtalk',"mw-heading mw-heading3"]
    divs = []

    for div_class in div_classes:
        divs.extend(soup.find_all('div', class_=div_class))

    url_fragment = url.split('#')[-1].replace('_', ' ')
    log_date = url.split('/')[-1]

    data = []
    for i, div in enumerate(divs):
        try:
            title = None
            text_url = None
            title_tag = div.find('a')
            if title_tag:
                title_span = div.find('span', {'data-mw-comment-start': True})
                if title_span:
                    title_anchor = title_span.find_next_sibling('a')
                    if title_anchor:
                        title = title_anchor.text
                        text_url = 'https://en.wikipedia.org' + title_anchor['href']
                else:
                    title = title_tag.text
                    text_url = 'https://en.wikipedia.org' + title_tag['href']

            if title == 'talk page' or title is None:
                heading_tag = div.find('div', class_='mw-heading mw-heading3')
                if heading_tag:
                    title_tag = heading_tag.find('a')
                    if title_tag:
                        title = title_tag.text
                        text_url = 'https://en.wikipedia.org' + title_tag['href']

            if not title:
                continue
            if title.lower() != url_fragment.lower():
                continue

            next_div = div.find_next('div', class_='mw-heading mw-heading3')
            deletion_discussion = ''
            sibling = div.find_next_sibling()
            while sibling and sibling != next_div:
                deletion_discussion += str(sibling)
                sibling = sibling.find_next_sibling()

            label = ''
            verdict_tag = div.find('p')
            if verdict_tag:
                label_b_tag = verdict_tag.find('b')
                if label_b_tag:
                    label = label_b_tag.text.strip()
            confirmation = ''
            discussion_tag = div.find('dd')
            if discussion_tag:
                discussion_tag_i = discussion_tag.find('i')
                if discussion_tag_i:
                    confirmation_b_tag = discussion_tag_i.find('b')
                    if confirmation_b_tag:
                        confirmation = confirmation_b_tag.text.strip()
            parts = deletion_discussion.split('<div class="mw-heading mw-heading3">')
            discussion = parts[0] if len(parts) > 0 else ''
            verdict = '<div class="mw-heading mw-heading3">' + parts[1] if len(parts) > 1 else ''

            data.append([date, title, text_url, deletion_discussion, label, confirmation, verdict, discussion])
        except Exception as e:
            print(f"Error processing div: {e}")
            continue

    df = pd.DataFrame(data, columns=['date', 'title', 'text_url', 'deletion_discussion', 'label', 'confirmation', 'discussion', 'verdict'])
    return df

def extract_label(label_html):
    soup = BeautifulSoup(label_html, 'html.parser')
    b_tag = soup.find('b')
    return b_tag.text.strip() if b_tag else ''

def process_labels(df):
    df['proper_label'] = df['label'].apply(extract_label)
    return df

def extract_confirmation(confirmation_html):
    soup = BeautifulSoup(confirmation_html, 'html.parser')
    b_tag = soup.find('span', {'style': 'color:red'}).find('b')
    return b_tag.text.strip() if b_tag else ''

def process_confirmations(df):
    df['confirmation'] = df['confirmation'].apply(extract_confirmation)
    return df

def extract_post_links_text(discussion_html):
    split_point = '<span class="plainlinks">'
    if split_point in discussion_html:
        parts = discussion_html.split(split_point)
        if len(parts) > 1:
            return parts[1]
    return discussion_html

def process_discussion(df):

    df['discussion_cleaned'] = df['discussion'].apply(extract_post_links_text)
    return df

def html_to_plaintext(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    for tag in soup.find_all(['p', 'li', 'dd', 'dl']):
        tag.insert_before('\n')
        tag.insert_after('\n')
    for br in soup.find_all('br'):
        br.replace_with('\n')

    text = soup.get_text(separator=' ', strip=True)
    text = '\n'.join([line.strip() for line in text.splitlines() if line.strip() != ''])

    return text

def process_html_to_plaintext(df):
    df['discussion_cleaned'] = df['discussion_cleaned'].apply(html_to_plaintext)
    return df

def split_text_into_sentences(text):
    seg = pysbd.Segmenter(language="en", clean=False)
    sentences = seg.segment(text)
    return ' '.join(sentences[1:])

def process_split_text_into_sentences(df):
    df['discussion_cleaned'] = df['discussion_cleaned'].apply(split_text_into_sentences)
    return df

def process_data(url,date):
    df = extract_div_contents_from_url(url,date)
    if df.discussion.tolist() == []:
      df = extract_div_contents_from_url_new(url,date)
    df = process_discussion(df)
    df = process_html_to_plaintext(df)
    df = process_split_text_into_sentences(df)
    if not df.empty:
        return df
    else:
        return 'Empty DataFrame'

def collect_deletion_discussions(start_date, end_date):
    base_url = 'https://en.wikipedia.org/wiki/Wikipedia:Articles_for_deletion/Log/'
    all_data = pd.DataFrame()

    current_date = start_date
    while current_date <= end_date:
        try:
            print(f"Processing {current_date.strftime('%Y-%B-%d')}")
            date_str = current_date.strftime('%Y_%B_%d')
            url = base_url + date_str
            log_date = current_date.strftime('%Y-%m-%d')

            df = extract_div_contents_with_additional_columns(url, log_date)
            if not df.empty:
                df = process_labels(df)
                df = process_confirmations(df)
                df = process_discussion(df)
                df = process_html_to_plaintext(df)
                df = process_split_text_into_sentences(df)
                all_data = pd.concat([all_data, df], ignore_index=True)
            current_date += timedelta(days=1)
        except Exception as e:
            print(f"Error processing {current_date.strftime('%Y-%B-%d')}: {e}")
            try:
                df = extract_div_contents_from_url_new(url, log_date)
                if not df.empty:
                    df = process_labels(df)
                    df = process_confirmations(df)
                    df = process_discussion(df)
                    df = process_html_to_plaintext(df)
                    df = process_split_text_into_sentences(df)
                    all_data = pd.concat([all_data, df], ignore_index=True)
            except Exception as inner_e:
                print(f"Error in alternative extraction for {current_date.strftime('%Y-%B-%d')}: {inner_e}")
            finally:
                current_date += timedelta(days=1)
    if all_data.empty:
        all_data = collect_data_new.collect_deletion_discussions_new(start_date, end_date)
    return all_data



if __name__ == '__main__':
    start_dt = datetime(2025, 1, 10)
    end_dt   = datetime(2025, 1, 12)
    big_df   = collect_deletion_discussions(start_dt, end_dt)

    # if big_df.empty:
    #     big_df = collect_data.collect_deletion_discussions_new(start_dt, end_dt)
    print(big_df)
