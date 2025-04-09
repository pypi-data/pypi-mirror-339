# coding: utf-8
# Copyright 2024 Network Dynamics Lab, McGill University
# Distributed under the MIT License

import argparse
import json
from pathlib import Path
from typing import Dict, List

import bs4
from bs4 import BeautifulSoup
from tqdm import tqdm

SUBSTITUTE_TAGS = {
    'persName',
    'orgName',
    'publicationStmt',
    'titleStmt',
    'biblScope'
}

def get_affiliation_from_grobid_xml(raw_xml: BeautifulSoup) -> Dict:
    """
    Get affiliation from grobid xml
    :param raw_xml:
    :return:
    """
    location_dict = dict()
    laboratory_name = ""
    institution_name = ""

    if raw_xml and raw_xml.affiliation:
        for child in raw_xml.affiliation:
            if child.name == "orgname":
                if child.has_attr("type"):
                    if child["type"] == "laboratory":
                        laboratory_name = child.text
                    elif child["type"] == "institution":
                        institution_name = child.text
            elif child.name == "address":
                for grandchild in child:
                    if grandchild.name and grandchild.text:
                        location_dict[grandchild.name] = grandchild.text

        if laboratory_name or institution_name:
            return {
                "laboratory": laboratory_name,
                "institution": institution_name,
                "location": location_dict
            }

    return {}

def get_author_data_from_grobid_xml(raw_xml: BeautifulSoup) -> List[Dict]:
    """
    Returns a list of dictionaries, one for each author,
    containing the first and last names.

    e.g.
        {
            "first": first,
            "middle": middle,
            "last": last,
            "suffix": suffix,
            "affiliation": {
                "laboratory": "",
                "institution": "",
                "location": "",
            },
            "email": ""
        }
    """
    authors = []

    for author in raw_xml.find_all("author"):

        first = ""
        middle = []
        last = ""
        suffix = ""

        if author.persname:
            # forenames include first and middle names
            forenames = author.persname.find_all("forename")

            # surnames include last names
            surnames = author.persname.find_all("surname")

            # name suffixes
            suffixes = author.persname.find_all("suffix")

            for forename in forenames:
                if forename.has_attr("type"):
                    if forename["type"] == "first":
                        if not first:
                            first = forename.text
                        else:
                            middle.append(forename.text)
                    elif forename["type"] == "middle":
                        middle.append(forename.text)

            if len(surnames) > 1:
                for surname in surnames[:-1]:
                    middle.append(surname.text)
                last = surnames[-1].text
            elif len(surnames) == 1:
                last = surnames[0].text

            if len(suffix) >= 1:
                suffix = " ".join([suffix.text for suffix in suffixes])

        affiliation = get_affiliation_from_grobid_xml(author)

        email = ""
        if author.email:
            email = author.email.text

        author_dict = {
            "first": first,
            "middle": middle,
            "last": last,
            "suffix": suffix,
            "affiliation": affiliation,
            "email": email
        }

        authors.append(author_dict)

    return authors

def get_publication_datetime_from_grobid_xml(raw_xml: BeautifulSoup) -> str:
    """
    Finds and returns the publication datetime if it exists
    :param raw_xml:
    :return:
    """
    if raw_xml.publicationStmt:
        for child in raw_xml.publicationstmt:
            if child.name == "date" \
                    and child.has_attr("type") \
                    and child["type"] == "published" \
                    and child.has_attr("when"):
                return child["when"]
    return ""

def clean_tags(el: bs4.element.Tag):
    """
    Replace all tags with lowercase version
    :param el:
    :return:
    """
    for sub_tag in SUBSTITUTE_TAGS:
        for sub_el in el.find_all(sub_tag):
            sub_el.name = sub_tag.lower()

def extract_paper_metadata_from_grobid_xml(tag: bs4.element.Tag) -> Dict:
    """
    Extract paper metadata (title, authors, affiliation, year) from grobid xml
    :param tag:
    :return:
    """
    clean_tags(tag)
    paper_metadata = {
        "title": tag.titlestmt.title.text,
        "authors": get_author_data_from_grobid_xml(tag),
        "year": get_publication_datetime_from_grobid_xml(tag)
    }
    return paper_metadata

def get_text(div: bs4.element.Tag):
    """
    Extract text from div
    :param div:
    :return:
    """


    if div.head:
        head_texts = []
        for p in div.head.next_siblings:
            head_texts.append(p.text)
        return f'{div.head.text}: {" ".join(head_texts)}'
    else:
        texts = []
        if div.children:
            for child in div.children:
                texts.append(child.text)
        elif div.text:
            texts.append(div.text)
        return " ".join(texts)

def extract_disclosure_from_tei_xml(
    sp: BeautifulSoup
):
    """
    Parse back matter from soup
    """
    keywords = ['funding', 'competing', 'conflict', 'disclosure', 'statement', 'information']
    back_text = []
    found = False
    if sp.back:
        for div in sp.back.find_all('div'):
            for child_div in div.find_all('div'):
                back_text.append(get_text(child_div))
        sp.back.decompose()
    for div in sp.body.find_all('div'):
        if div.find_all('div'):
                for child_div in div.find_all('div'):
                    for keyword in keywords:
                        if child_div.head and keyword in child_div.head.text.lower():
                            back_text.append(get_text(child_div))
                            found = True
                            break
        else:
            for keyword in keywords:
                if div.head and keyword in div.head.text.lower():
                    back_text.append(get_text(div))
                    found = True
                    break
    return back_text, found

def _clean_empty_and_duplicate_authors_from_grobid_parse(authors: List[Dict]) -> List[Dict]:
    """
    Within affiliation, `location` is a dict with fields <settlement>, <region>, <country>, <postCode>, etc.
    Too much hassle, so just take the first one that's not empty.
    """
    # stripping empties
    clean_authors_list = []
    for author in authors:
        clean_first = author['first'].strip()
        clean_last = author['last'].strip()
        clean_middle = [m.strip() for m in author['middle']]
        clean_suffix = author['suffix'].strip()
        if clean_first or clean_last or clean_middle:
            author['first'] = clean_first
            author['last'] = clean_last
            author['middle'] = clean_middle
            author['suffix'] = clean_suffix
            clean_authors_list.append(author)
    # combining duplicates (preserve first occurrence of author name as position)
    key_to_author_blobs = {}
    ordered_keys_by_author_pos = []
    for author in clean_authors_list:
        key = (author['first'], author['last'], ' '.join(author['middle']), author['suffix'])
        if key not in key_to_author_blobs:
            key_to_author_blobs[key] = author
            ordered_keys_by_author_pos.append(key)
        else:
            if author['email']:
                key_to_author_blobs[key]['email'] = author['email']
            if author['affiliation'] and (author['affiliation']['institution'] or author['affiliation']['laboratory'] or author['affiliation']['location']):
                key_to_author_blobs[key]['affiliation'] = author['affiliation']
    dedup_authors_list = [key_to_author_blobs[key] for key in ordered_keys_by_author_pos]
    return dedup_authors_list

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process GROBID XML files.')
    parser.add_argument('folder_xml', type=str, help='Path to the folder containing XML files')
    args = parser.parse_args()

    folder_xml = Path(args.folder_xml)
    xml_list = []
    disclosures = []
    back_matters = []
    metadatas = []
    for x in folder_xml.iterdir():
        if x.name.endswith('xml'):
            xml_list.append(x)
    count_extra = 0
    for xml_path in tqdm(xml_list):
        soup = BeautifulSoup(open(xml_path, 'rb').read(), "xml")
        metadata = extract_paper_metadata_from_grobid_xml(soup.fileDesc)
        # clean metadata authors (remove dupes etc)
        metadata['authors'] = _clean_empty_and_duplicate_authors_from_grobid_parse(metadata['authors'])
        back_matter, found = extract_disclosure_from_tei_xml(soup)
        count_extra += 1 if found else 0
        disclosure = ' '.join(back_matter)
        metadata['disclosure'] = disclosure
        open(str(xml_path).replace('grobid.tei.xml', 'jsonl2'), 'w').write(json.dumps(metadata))
