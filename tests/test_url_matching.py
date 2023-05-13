"""Tests for Sopel's ``reddit`` plugin"""
from __future__ import annotations

import pytest

from sopel.trigger import PreTrigger


TMP_CONFIG = """
[core]
owner = Admin
nick = Sopel
enable =
    reddit
host = irc.libera.chat
"""


@pytest.fixture
def bot(botfactory, configfactory):
    settings = configfactory('default.ini', TMP_CONFIG)
    return botfactory.preloaded(settings, ['reddit'])


@pytest.mark.parametrize('proto', ('http://', 'https://'))
@pytest.mark.parametrize('trailing_slash', (True, False))
@pytest.mark.parametrize('base', (
    'reddit.com',
    'www.reddit.com',
    'old.reddit.com',
    'new.reddit.com',
    'beta.reddit.com',
    'np.reddit.com',
    'pay.reddit.com',
    'ssl.reddit.com',
    'it.reddit.com',
    'es.reddit.com',
    'fr.reddit.com',
    'pl.reddit.com',
    # sometimes, enough is enough
))
@pytest.mark.parametrize('path, rule_name', (
    ('/r/subname', 'auto_subreddit_info'),
    ('/comments/123456', 'post_or_comment_info'),
    ('/r/subname/comments/123456', 'post_or_comment_info'),
    ('/r/subname/comments/123456/post_title_slug', 'post_or_comment_info'),
    ('/r/subname/comments/123456/post_title_slug/234567', 'post_or_comment_info'),
))
@pytest.mark.parametrize('query', (
    '',
    '?context=1337',
    'param=value',
))
def test_long_url_matching(proto, base, path, query, trailing_slash, rule_name, bot):
    link = proto + base + path

    if trailing_slash:
        link += '/'

    link += query

    # we don't allow for query parameters on subreddit links (yet?)
    should_match = rule_name and not (rule_name == 'auto_subreddit_info' and query)

    line = PreTrigger(bot.nick, ':User!user@irc.libera.chat PRIVMSG #channel {}'.format(link))
    matched_rules = [
        # we can ignore matches that don't come from this plugin
        match[0] for match in bot.rules.get_triggered_rules(bot, line)
        if match[0].get_plugin_name() == 'reddit'
    ]

    if should_match:
        assert len(matched_rules) == 1
        assert matched_rules[0].get_rule_label() == rule_name
    else:
        assert len(matched_rules) == 0


@pytest.mark.parametrize('proto', ('http://', 'https://'))
@pytest.mark.parametrize('base', ('redd.it', 'reddit.com'))
@pytest.mark.parametrize('trailing_slash', (True, False))
def test_short_url_matching(proto, base, trailing_slash, bot):
    link = proto + base + '/sh0r7'

    if trailing_slash:
        link += '/'

    line = PreTrigger(bot.nick, ':User!user@irc.libera.chat PRIVMSG #channel {}'.format(link))
    matched_rules = [
        # we can ignore matches that don't come from this plugin
        match[0] for match in bot.rules.get_triggered_rules(bot, line)
        if match[0].get_plugin_name() == 'reddit'
    ]

    assert len(matched_rules) == 1
    assert matched_rules[0].get_rule_label() == 'post_or_comment_info'


@pytest.mark.parametrize('proto', ('http://', 'https://'))
@pytest.mark.parametrize('subdomain', ('i', 'preview'))
@pytest.mark.parametrize('slug', ('', 'didnt-expect-to-find-this-near-school-v0-'))
@pytest.mark.parametrize('ext', ('jpg', 'jpeg', 'png', 'gif', 'mp4'))
@pytest.mark.parametrize('sig', (True, False))
def test_hosted_image_url_matching(proto, subdomain, slug, ext, sig, bot):
    link = proto + subdomain + '.redd.it/' + slug + 'yib0zwk1mmza1.' + ext

    if sig:
        link += '?s=965439a2d38896d978f5c2ecc0237964e7674813'

    line = PreTrigger(bot.nick, ':User!user@irc.libera.chat PRIVMSG #channel {}'.format(link))
    matched_rules = [
        # we can ignore matches that don't come from this plugin
        match[0] for match in bot.rules.get_triggered_rules(bot, line)
        if match[0].get_plugin_name() == 'reddit'
    ]

    assert len(matched_rules) == 1
    assert matched_rules[0].get_rule_label() == 'image_info'

    matches = [match for match in matched_rules[0].match(bot, line)]
    assert len(matches) == 1
    assert matches[0].group('image') == 'yib0zwk1mmza1.' + ext
