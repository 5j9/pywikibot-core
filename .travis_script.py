#!/usr/bin/python
# -*- coding: utf-8 -*-
"""The script to be run by travis."""
from os import getenv, mkdir
from os.path import expanduser
from subprocess import check_call


HOME = expanduser('~')
FAMILY = getenv('FAMILY')
LANGUAGE = getenv('LANGUAGE')
USER_PASSWORD = getenv('USER_PASSWORD')
PYWIKIBOT_USERNAME = getenv('PYWIKIBOT_USERNAME')
OAUTH_DOMAIN = getenv('OAUTH_DOMAIN')
OAUTH_PYWIKIBOT_USERNAME = getenv('OAUTH_PYWIKIBOT_USERNAME')


if getenv('PYSETUP_TEST_EXTRAS') == '1':
    check_call(['pip', 'install',  '-e', '.[mwoauth,security]'])

mkdir(HOME + '/.pywikibot')


generate_family_args = [
    'python', 'pwb.py', 'generate_family_file',
    'https://wiki.musicbrainz.org/', 'musicbrainz', 'n']
check_call(generate_family_args)
if FAMILY == 'wpbeta':
    check_call([
        'python', '-m', 'generate_family_file',
        'http://' + LANGUAGE + '.wikipedia.beta.wmflabs.org/', 'wpbeta', 'y'])
elif FAMILY == 'wpbeta':
    check_call([
        'python', '-m', 'generate_family_file',
        'http://' + LANGUAGE + '.wikisource.beta.wmflabs.org/', 'wpbeta', 'y'])

check_call([
    'python', '-W', 'error::UserWarning', '-m', 'generate_user_files',
    '-dir:' + HOME + '/.pywikibot/', '-family:' + FAMILY, '-lang:' + LANGUAGE,
    '-v', '-user:' + PYWIKIBOT_USERNAME])

if PYWIKIBOT_USERNAME and USER_PASSWORD:
    user_config = (
        "usernames['wikipedia']['en'] = '{user}'\n"
        "usernames['wikipedia']['test'] = '{user}'\n"
        "usernames['wikidata']['test'] = '{user}'\n"
        "usernames['commons']['commons'] = '{user}'\n"
        "password_file = '{home}/.pywikibot/passwordfile')\n"
        "max_retries = 2\n"
        "maximum_GET_length = 5000\n"
        "console_encoding = 'utf8'\n"
        "authenticate['wiki.musicbrainz.org'] = ('NOTSPAM', 'NOTSPAM')\n"
        .format(user=PYWIKIBOT_USERNAME, home=HOME))
    if OAUTH_DOMAIN:
        if OAUTH_PYWIKIBOT_USERNAME:
            user_config += (
                "usernames['{fam}']['{lang}'] = '{user}'\n".format(
                    lang=LANGUAGE, fam=FAMILY, user=OAUTH_PYWIKIBOT_USERNAME))
        oauth_token = getenv(
            'OAUTH_TOKENS_' + FAMILY.upper() + '_' + LANGUAGE.uppper())
        if oauth_token:
            user_config += (
                "authenticate['{domain}'] = ('{tokens}')\n".format(
                    domain=OAUTH_DOMAIN,
                    tokens=oauth_token.replace(':', "', '")))
    with open(HOME + '/.pywikibot/user-config.py') as user_config_file:
        user_config_file.write(user_config)
    with open(HOME + '/.pywikibot/passwordfile') as passwordfile:
        passwordfile.write(
            "('{user}', '{password}')\n"
            .format(user=PYWIKIBOT_USERNAME, password=USER_PASSWORD))

if getenv('USE_NOSE') == '1':
