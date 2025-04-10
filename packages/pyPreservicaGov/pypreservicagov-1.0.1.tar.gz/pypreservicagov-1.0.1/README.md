# pyPreservica.Gov

Python Module For Harvesting public Modern.Gov Committee and Meeting Records into Preservica for Long Term Preservation.

pyPreservica.Gov is a Python Module which allows Preservica users to automatically harvest public records from the 
Civica Modern.Gov Content Management system directly into a Preservica Long Term Digital Preservation platform


## Usage

Once installed you can run pyPreservica.Gov directly from the command line

        $ python -m  pyPreservicaGov

The first time the module is run, it will create a credentials.properties file in the local directory and then exit

Edit the credentials.properties, the first section should contain your Preservica username, password and hostname of
the Preservica system you would like to connect to.

The second section contains the security tag which should be assigned to the records as they are ingested. For example 
records which can be published immediately on the Preservica access portal should be set to "public".

The site_name parameter should point to the URL of the Modern.Gov system you would like to harvest.

parent.folder should be the UUID of the Preservica collection the Committee folders will be ingested into. 

The committee.FromDate and committee.ToDate parameters specify the date range of meetings which will be harvested.
    
    [credentials]
    username=test@test.com
    password=1234567
    server=uk.preservica.com
    
    [Modern.Gov]
    security.tag=open
    site_name=https://democracy.local_authority.gov.uk/
    parent.folder=372d2881-7cce-4c2e-99f7-386c3cf4a922
    committee.FromDate=01/01/1980
    committee.ToDate=01/01/2024


Once the credentials.properties has been updated you can run pyPreservica.Gov again directly from the command line
to start the harvest process.

        $ python -m  pyPreservicaGov


## License

The package is available as open source under the terms of the Apache License 2.0

## Support 

pyPreservica.Gov is 3rd party open source client and is not affiliated or supported by Preservica Ltd.
There is no support for use of the library by Preservica Ltd.
Bug reports can be raised directly on GitHub.

Users of pyPreservica.Gov should make sure they are licensed to use the Preservica REST APIs. 

## Installation

pyPreservica.Gov is available from the Python Package Index (PyPI)

https://pypi.org/project/pyPreservicaGov/

To install pyPreservica.Gov, simply run this simple command in your terminal of choice:


    $ pip install pyPreservicaGov



