import sys
sys.path.append('..')
from scrape import digi
from scrape import europa
from scrape import mediafax
from bs4 import BeautifulSoup


def test_trim_text():
    text_long = 'a' * 300

    text_short = 'a' * 20

    assert len(digi.trim_text(text_long)) == 258
    assert len(digi.trim_text(text_short)) == len(text_short)
    assert digi.trim_text(234) == TypeError

    assert len(europa.trim_text(text_long)) == 258
    assert len(europa.trim_text(text_short)) == len(text_short)
    assert europa.trim_text(234) == TypeError

    assert len(mediafax.trim_text(text_long)) == 258
    assert len(mediafax.trim_text(text_short)) == len(text_short)
    assert mediafax.trim_text(234) == TypeError


def test_get_from_sites():
    bad_address = 'http://www.abc_xyz.demo'
    expected = 'Error while connecting to ' + bad_address

    assert digi.get_from_digi(website_address=bad_address) == expected
    assert europa.get_from_europa(website_address=bad_address) == expected
    assert mediafax.get_from_mediafax(website_address=bad_address) == expected


def test_get_article():
    article_digi = BeautifulSoup('''
        <p>Abcd efgh</p>
        <p>Abcd efgh</p>
        <p>Abcd efgh</p>
        <p>Abcd efgh</p>
        ''', 'html.parser')
    assert len(digi.get_text(article_digi)) == 40

    article_europa = BeautifulSoup('''
        <p>Abcd efgh</p>
        <p>Abcd efgh</p>
        <p>Abcd efgh</p>
        <p>Abcd efgh</p>
        ''', 'html.parser')
    assert len(europa.get_text(article_europa)) == 40

    article_mediafax = BeautifulSoup('''
        <div id='article_text_content'>
            <div class='just-article-content'>
                <p>Abcd efgh</p>
                <p>Abcd efgh</p>
                <p>Abcd efgh</p>
                <p>Abcd efgh</p>
            </div>
        </div>
        ''', 'html.parser')
    assert len(mediafax.get_text(article_mediafax)) == 40


def test_get_thumbnail():
    pic_digi = BeautifulSoup('''
        <figure class="article-thumb">
            <img src='source_of_photo'></img>
        </figure>
    ''', 'html.parser')
    assert digi.get_thumbnail(pic_digi) == 'source_of_photo'

    pic_europa = BeautifulSoup('''
        <img src='source_of_photo'></img>
    ''', 'html.parser')
    assert europa.get_thumbnail(pic_europa) == 'source_of_photo'

    pic_mediafax = BeautifulSoup('''
        <div class="ArticleImageContainer">
            <img data-src='source_of_photo'></img>
        </div>
    ''', 'html.parser')
    assert mediafax.get_thumbnail(pic_mediafax)
