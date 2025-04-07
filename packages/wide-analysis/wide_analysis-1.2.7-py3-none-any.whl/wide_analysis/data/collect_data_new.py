# import requests
# import pandas as pd
# from bs4 import BeautifulSoup
# import pysbd
# from datetime import datetime, timedelta

# def extract_div_contents_from_page(url, date):
#     response = requests.get(url)
#     if response.status_code != 200:
#         print(f"Error: Received status code {response.status_code} for URL: {url}")
#         return pd.DataFrame(columns=['date','title','text_url','deletion_discussion','label','confirmation','discussion','verdict'])

#     soup = BeautifulSoup(response.content, 'html.parser')
#     heading_divs = soup.find_all('div', class_='mw-heading mw-heading3')

#     data_rows = []
#     for i, heading_div in enumerate(heading_divs):
#         h3_tag = heading_div.find('h3')
#         if not h3_tag:
#             continue
#         title_anchor = h3_tag.find('a')
#         if not title_anchor:
#             continue

#         title = title_anchor.get_text(strip=True)
#         text_url = 'https://en.wikipedia.org' + title_anchor.get('href', '')
#         discussion_html = ""
#         next_heading_div = heading_divs[i+1] if i + 1 < len(heading_divs) else None

#         sibling = heading_div.next_sibling
#         while sibling and sibling != next_heading_div:
#             discussion_html += str(sibling)
#             sibling = sibling.next_sibling
#         label = ""
#         confirmation = ""
#         parts = discussion_html.split('<div class="mw-heading mw-heading3">')
#         discussion_part = parts[0] if len(parts) > 0 else ''
#         verdict_part = '<div class="mw-heading mw-heading3">' + parts[1] if len(parts) > 1 else ''
#         data_rows.append([
#             date,
#             title,
#             text_url,
#             discussion_html,  
#             label,
#             confirmation,
#             discussion_part,
#             verdict_part
#         ])
#     df = pd.DataFrame(data_rows, columns=[
#         'date', 'title', 'text_url', 'deletion_discussion',
#         'label', 'confirmation', 'discussion', 'verdict'
#     ])
#     return df

# # def extract_label(label_html):
# #     soup = BeautifulSoup(label_html, 'html.parser')
# #     b_tag = soup.find('b')
# #     return b_tag.text.strip() if b_tag else ''

# def extract_label(label_html):
#     soup = BeautifulSoup(label_html, 'html.parser')
#     p_tag = soup.find('p')
#     if p_tag:
#         b_tag = p_tag.find('b')
#         if b_tag:
#             return b_tag.get_text(strip=True).lower()
#         return p_tag.get_text(strip=True).lower()
#     return soup.get_text(" ", strip=True).lower()


# def process_labels(df):
#     df['proper_label'] = df['label'].apply(extract_label)
#     return df

# def extract_confirmation(confirmation_html):
#     soup = BeautifulSoup(confirmation_html, 'html.parser')
#     red_span = soup.find('span', {'style': 'color:red'})
#     if not red_span:
#         return ''
#     b_tag = red_span.find('b')
#     return b_tag.text.strip() if b_tag else ''

# def process_confirmations(df):
#     df['confirmation'] = df['confirmation'].apply(extract_confirmation)
#     return df

# def extract_post_links_text(discussion_html):
#     split_point = '<span class="plainlinks">'
#     if split_point in discussion_html:
#         parts = discussion_html.split(split_point)
#         if len(parts) > 1:
#             return parts[1]
#     return discussion_html

# def process_discussion(df):
#     df['discussion_cleaned'] = df['discussion'].apply(extract_post_links_text)
#     return df

# def html_to_plaintext(html_content):
#     soup = BeautifulSoup(html_content, 'html.parser')
#     for tag in soup.find_all(['p', 'li', 'dd', 'dl']):
#         tag.insert_before('\n')
#         tag.insert_after('\n')

#     for br in soup.find_all('br'):
#         br.replace_with('\n')
#     text = soup.get_text(separator=' ', strip=True)
#     text = '\n'.join([line.strip() for line in text.splitlines() if line.strip() != ''])
#     return text

# def process_html_to_plaintext(df):
#     df['discussion_cleaned'] = df['discussion_cleaned'].apply(html_to_plaintext)
#     return df
# def split_text_into_sentences(text):
#     seg = pysbd.Segmenter(language="en", clean=False)
#     sentences = seg.segment(text)
#     return ' '.join(sentences[1:])

# def process_split_text_into_sentences(df):
#     df['discussion_cleaned'] = df['discussion_cleaned'].apply(split_text_into_sentences)
#     return df
# def process_data(url, date):
#     df = extract_div_contents_from_page(url, date)
#     if df.empty:
#         return 'Empty DataFrame'
#     df = process_labels(df)
#     df = process_confirmations(df)
#     df = process_discussion(df)
#     df = process_html_to_plaintext(df)
#     df = process_split_text_into_sentences(df)
#     #print(df)
#     return df

# def collect_deletion_discussions_new(start_date, end_date):
#     base_url = 'https://en.wikipedia.org/wiki/Wikipedia:Articles_for_deletion/Log/'
#     all_data = pd.DataFrame()

#     current_date = start_date
#     while current_date <= end_date:
#         try:
#             print(f"Processing {current_date.strftime('%Y-%B-%d')}")
#             # date_str = current_date.strftime('%Y_%B_%d')
#             date_str = f"{current_date.year}_{current_date.strftime('%B')}_{current_date.day}"
#             url = base_url + date_str

#             log_date_str = current_date.strftime('%Y-%m-%d')
#             df_daily = extract_div_contents_from_page(url, log_date_str)
#             if not df_daily.empty:
#                 df_daily = process_labels(df_daily)
#                 df_daily = process_confirmations(df_daily)
#                 df_daily = process_discussion(df_daily)
#                 df_daily = process_html_to_plaintext(df_daily)
#                 df_daily = process_split_text_into_sentences(df_daily)

#                 all_data = pd.concat([all_data, df_daily], ignore_index=True)

#         except Exception as e:
#             print(f"Error processing {current_date.strftime('%Y-%B-%d')}: {e}")
            
#         current_date += timedelta(days=1)
#         if 'log_date' not in all_data.columns:
#             all_data['log_date'] = log_date_str

#     return all_data


# # if __name__ == '__main__':
# #     url ='https://en.wikipedia.org/wiki/Wikipedia:Articles_for_deletion/Log/2025_January_11#Westballz'
# #     #df_example = process_data(url, date='2025_January_11')
# #     #print(df_example[df_example['title'] == 'Westballz']['discussion_cleaned'].iloc[0])

# #     # OR do a date range
# #     start_dt = datetime(2024, 7, 15)
# #     end_dt   = datetime(2024, 7, 18)
# #     big_df   = collect_deletion_discussions_new(start_dt, end_dt)


# #     print(big_df)


import requests
import pandas as pd
from bs4 import BeautifulSoup
import pysbd
from datetime import datetime, timedelta
import re

def extract_label(label_html):
    if not label_html:
        return ''
    
    soup = BeautifulSoup(label_html, 'html.parser')
    
    # Look for the <p> tag containing "The result was" and a <b> tag
    for p in soup.find_all('p'):
        p_text = p.get_text(strip=True).lower()
        if "the result was" in p_text:
            b_tag = p.find('b')
            if b_tag:
                return b_tag.get_text(strip=True)
    
    # Fallback: look for any <b> tag within paragraphs that might contain the verdict
    for p in soup.find_all('p'):
        b_tag = p.find('b')
        if b_tag and b_tag.get_text(strip=True):
            return b_tag.get_text(strip=True)
    
    return ''

def process_labels(df):
    df['label'] = df['label'].apply(extract_label)
    return df

def extract_div_contents_from_page(url, date):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error: Received status code {response.status_code} for URL: {url}")
        return pd.DataFrame(columns=[
            'date', 'title', 'text_url', 'deletion_discussion',
            'label', 'confirmation', 'discussion', 'verdict'
        ])
    
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
        
        # Important fix: Find the boilerplate div that contains the verdict
        # Look for the boilerplate div that appears BEFORE the current heading
        boilerplate_div = None
        current_element = heading_div
        
        # Search backward for the closest boilerplate div
        while current_element:
            previous_element = current_element.previous_sibling
            if previous_element is None:
                if getattr(current_element, 'parent', None):
                    current_element = current_element.parent
                    continue
                else:
                    break
                
            if (getattr(previous_element, 'name', None) == 'div' and 
                previous_element.get('class') and 
                'boilerplate' in previous_element.get('class')):
                boilerplate_div = previous_element
                break
                
            current_element = previous_element
        
        label_html = str(boilerplate_div) if boilerplate_div else ""
        
        # Extract confirmation from <dd><i><b>
        confirmation = ''
        verdict_soup = BeautifulSoup(discussion_html, 'html.parser')
        dd_tag = verdict_soup.find('dd')
        if dd_tag:
            i_tag = dd_tag.find('i')
            if i_tag:
                b_tag = i_tag.find('b')
                if b_tag:
                    confirmation = str(i_tag)
        
        # Split raw HTML to extract discussion and verdict parts.
        parts = discussion_html.split('<div class="mw-heading mw-heading3">')
        discussion_part = parts[0] if len(parts) > 0 else ''
        verdict_part = '<div class="mw-heading mw-heading3">' + parts[1] if len(parts) > 1 else ''
        
        data_rows.append([
            date,
            title,
            text_url,
            discussion_html,
            label_html,
            confirmation,
            discussion_part,
            verdict_part
        ])
    
    df = pd.DataFrame(data_rows, columns=[
        'date', 'title', 'text_url', 'deletion_discussion',
        'label', 'confirmation', 'discussion', 'verdict'
    ])
    return df


def extract_confirmation(confirmation_html):
    soup = BeautifulSoup(confirmation_html, 'html.parser')
    red_span = soup.find('span', {'style': 'color:red'})
    if not red_span:
        return ''
    b_tag = red_span.find('b')
    return b_tag.get_text(strip=True) if b_tag else ''

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

def process_data(url, date):
    df = extract_div_contents_from_page(url, date)
    if df.empty:
        return 'Empty DataFrame'
    df = process_labels(df)
    df = process_confirmations(df)
    df = process_discussion(df)
    df = process_html_to_plaintext(df)
    df = process_split_text_into_sentences(df)
    return df

def collect_deletion_discussions_new(start_date, end_date):
    base_url = 'https://en.wikipedia.org/wiki/Wikipedia:Articles_for_deletion/Log/'
    all_data = pd.DataFrame()
    
    current_date = start_date
    while current_date <= end_date:
        try:
            print(f"Processing {current_date.strftime('%Y-%B-%d')}")
            date_str = f"{current_date.year}_{current_date.strftime('%B')}_{current_date.day}"
            url = base_url + date_str
            log_date_str = current_date.strftime('%Y-%m-%d')
            
            df_daily = extract_div_contents_from_page(url, log_date_str)
            if not df_daily.empty:
                df_daily = process_labels(df_daily)
                df_daily = process_confirmations(df_daily)
                df_daily = process_discussion(df_daily)
                df_daily = process_html_to_plaintext(df_daily)
                df_daily = process_split_text_into_sentences(df_daily)
                
                all_data = pd.concat([all_data, df_daily], ignore_index=True)
        except Exception as e:
            print(f"Error processing {current_date.strftime('%Y-%B-%d')}: {e}")
        current_date += timedelta(days=1)
    
    if 'log_date' not in all_data.columns and not all_data.empty:
        all_data['log_date'] = log_date_str
    
    return all_data



# if __name__ == '__main__':
#     url ='https://en.wikipedia.org/wiki/Wikipedia:Articles_for_deletion/Log/2025_January_11#Westballz'
#     #df_example = process_data(url, date='2025_January_11')
#     #print(df_example[df_example['title'] == 'Westballz']['discussion_cleaned'].iloc[0])

#     # OR do a date range
#     start_dt = datetime(2024, 1, 1)
#     end_dt   = datetime(2024, 1, 2)
#     big_df   = collect_deletion_discussions_new(start_dt, end_dt)


#     print(big_df.label.unique().tolist())


