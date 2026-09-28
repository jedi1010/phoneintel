# PhoneIntel

PhoneIntel is a Python command-line tool for analyzing publicly available phone-number metadata using the `phonenumbers` library.

It can display:

* International phone-number format
* E.164 format
* National format
* Country calling code
* National number
* Geographic/region description when available
* Carrier information when available
* Number type
* Possible/valid status
* Associated timezone information
* Current time for associated timezones
* Difference between the phone-number timezone and the computer timezone
* JSON report output

## Important limitation

PhoneIntel does **not** provide:

* GPS/live location tracking
* Exact physical location of a phone
* SIM card numbers
* IMSI/IMEI
* Private subscriber information
* Call or SMS records
* WhatsApp/Telegram information
* Websites visited by a subscriber
* Applications used by a subscriber
* Access to telecom-provider databases

The information returned depends on the public numbering metadata available to the underlying library.

## Requirements

* Python 3.9 or newer
* `pip`
* Internet access for installing dependencies

Kali Linux, Debian, Ubuntu and other Linux distributions are supported.

## Installation

Clone the repository:

```bash
git clone https://github.com/jedi1010/phoneintel.git
cd phoneintel
```

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate it on Linux/macOS:

```bash
source .venv/bin/activate
```

On Windows:

```powershell
.venv\Scripts\activate
```

Install the dependency:

```bash
pip install -r requirements.txt
```

## Kali Linux

On recent Kali Linux versions, system-wide `pip` installation may be blocked by PEP 668.

Use a virtual environment:

```bash
sudo apt update
sudo apt install -y python3-venv python3-full
```

Then:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
ls -l phoneintel.py
sudo chown username:username phoneintel.py
chmod +x phoneintel.py
```

## Usage

Run:

```bash
python phoneintel.py +97152*******
or
./phoneintel.py +97152*******
```

Replace the example number with a number you are authorized to analyze.

Example:

```text
============================================================
PHONE NUMBER INTELLIGENCE CREATED BY JEDI1010
============================================================
Phone number:       +97152*******
International:      +971 52 *** ****
E.164:              +97152*******
National:           052 *** ****
Country code:       +971
National number:    52*******
Region:             ...
Carrier:            ...
Number type:        Mobile
Possible:           True
Valid:              True
...
============================================================
```

The program also creates:

```text
phoneintel.json
```

The JSON file contains the same analysis in machine-readable format.

## Syntax check

Before running the program, you can check the Python syntax:

```bash
python -m py_compile phoneintel.py
```

No output normally means the syntax check succeeded.

## Making the script executable

On Linux:

```bash
chmod +x phoneintel.py
```

Then:

```bash
./phoneintel.py +97152*******
```

## JSON output

PhoneIntel automatically creates:

```text
phoneintel.json
```

Example structure:

```json
{
    "input": "+97152*******",
    "international": "+971 52 *** ****",
    "e164": "+97152*******",
    "national": "052 *** ****",
    "country_code": 971,
    "national_number": "52*******",
    "region": "",
    "carrier": "",
    "number_type": "Mobile",
    "possible": true,
    "valid": true,
    "time_zones": [
        "Asia/Dubai"
    ]
}
```

Use fictional or test numbers when publishing example output.

## Privacy

Do not publish real people's phone numbers, generated reports containing personal information, or other private data in the repository.

## Responsible use

Only analyze phone numbers when you have a legitimate reason and appropriate authorization.

Do not use this project to harass, stalk, impersonate, or obtain private information about another person.

# Disclaimer

PhoneIntel is provided for **educational purposes only**.

The tool uses publicly available numbering metadata to provide information such as country/region, carrier information, number type, validity status, formatting, and associated time zones. It does **not** provide GPS location, real-time physical location, SIM/IMSI information, IMEI information, private subscriber information, call records, SMS records, or access to private accounts or devices.

## Responsible Use

You are responsible for ensuring that your use of PhoneIntel complies with all applicable laws, regulations, privacy requirements, and terms of service in your jurisdiction.

Do not use this software to:

* Track or locate individuals without authorization.
* Harass, threaten, stalk, or intimidate anyone.
* Obtain private or confidential information without permission.
* Attempt unauthorized access to phones, networks, accounts, or services.
* Conduct fraud, impersonation, or other illegal activities.
* Circumvent privacy or security protections.

Only analyze phone numbers that you are authorized to investigate or that you have a legitimate reason to process.

## Accuracy

PhoneIntel relies on third-party numbering metadata and public databases. Results may be incomplete, outdated, inaccurate, or unavailable for certain numbers.

A phone number's reported country, carrier, region, time zone, validity, or type should not be treated as proof of a person's identity, physical location, nationality, residence, or current carrier.

## No Warranty

This software is provided **"as is"**, without warranties of any kind. The developers and contributors are not responsible for any damage, loss, privacy violation, legal issue, or other consequence resulting from the use or misuse of this software.

By using PhoneIntel, you acknowledge that you are responsible for your own actions and for complying with applicable laws and regulations.

**Use responsibly.**

## License

This project is released under the MIT License. See `LICENSE` for details.

## Author

Created by JEDI1010.

Contributions, bug reports and improvements are welcome.
