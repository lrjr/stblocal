#!/usr/bin/python

# Copyright 2017 Stb-tester.com Ltd.

"""
Google sheets integration for performance reporting.

Use:

    GoogleSheet().record_measurement(
        time.time(), "measurement", {"duration": 5})

Initial Setup:

1. Create a google API project called "stb-tester-test-pack-example"
2. Create a google service account called "stb-tester-test-pack-example"
3. Save the private key json file to
   config/credentials/google-service-account.json
4. Create a google spreadsheet with a sheet called Measurements
5. Share the sheet with the service account using the service account email
   address ("client_email" in google-service-account.json)
6. Get the sheet id from the URL and set it in stbt.conf as
   test_pack.google_sheets_id
7. Run `tests/google.py` to make sure everything's working.
"""

import argparse
import os
import sys


SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CREDENTIALS_FILE = 'config/credentials/google-service-account.json'


class GoogleSheet(object):
    def __init__(self, spreadsheet_id=None, credentials_file=None):
        import httplib2
        from apiclient import discovery

        if spreadsheet_id is None:
            from stbt import get_config
            spreadsheet_id = get_config("test_pack", "google_sheets_id")
        print "Using spreadsheet %r" % spreadsheet_id

        credentials = self._get_credentials(credentials_file)
        http = credentials.authorize(httplib2.Http())
        discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                        'version=v4')
        self.service = discovery.build('sheets', 'v4', http=http,
                                       discoveryServiceUrl=discoveryUrl)
        self.sheets = self.service.spreadsheets()  # pylint: disable=no-member
        self.spreadsheet_id = spreadsheet_id

    @staticmethod
    def _get_credentials(credentials_file=None):
        if credentials_file is None:
            credentials_file = _find_file('../%s' % CREDENTIALS_FILE)

        try:
            from oauth2client.service_account import ServiceAccountCredentials
            return ServiceAccountCredentials.from_json_keyfile_name(
                credentials_file, scopes=SCOPES)
        except ImportError:
            pass

        # Support older versions of oauth2client:
        import json
        from oauth2client.client import SignedJwtAssertionCredentials

        with open(credentials_file) as f:
            cred_json = json.load(f)
        return SignedJwtAssertionCredentials(
            service_account_name=cred_json["client_email"],
            private_key=cred_json['private_key'],
            scope=SCOPES,
            token_uri=cred_json['token_uri'])

    def record_measurement(self, time, name, data):
        import datetime
        import pytz

        data = data.copy()
        data['time'] = datetime.datetime.fromtimestamp(time).replace(
            tzinfo=pytz.utc).isoformat()
        data['measurement'] = name

        headings = self.sheets.values().get(
            spreadsheetId=self.spreadsheet_id,
            range='Measurements!A1:Z1').execute()['values'][0]

        required_headings = set(data.keys())
        missing_headings = required_headings - set(headings)

        if missing_headings:
            headings.extend(missing_headings)
            self.sheets.values().update(
                spreadsheetId=self.spreadsheet_id,
                range='Measurements',
                body={'values': [headings]},
                valueInputOption="RAW").execute()

        out_data = [data.get(x) for x in headings]
        self.sheets.values().append(
            spreadsheetId=self.spreadsheet_id, range='Measurements',
            body={'values': [out_data]}, valueInputOption="RAW",
            insertDataOption="INSERT_ROWS").execute()

    def get(self):
        response = self.sheets.values().get(
            spreadsheetId=self.spreadsheet_id, range="Measurements").execute()
        return response.get('values')


def test_spreadsheet_integration():
    GoogleSheet().record_measurement(1234, "hello", {})


def main(argv):
    import time

    parser = argparse.ArgumentParser()
    parser.parse_args(argv[1:])

    GoogleSheet().record_measurement(time.time(), "testing", {})


def _find_file(path, root=os.path.dirname(os.path.abspath(__file__))):
    return os.path.join(root, path)


if __name__ == '__main__':
    sys.exit(main(sys.argv))
