#!/usr/bin/env python3

import sys
import json
from datetime import datetime
from zoneinfo import ZoneInfo

import phonenumbers

from phonenumbers import (
    geocoder,
    carrier,
    timezone,
    PhoneNumberType,
    PhoneNumberFormat
)


def type_name(number_type):
    names = {
        PhoneNumberType.FIXED_LINE: "Fixed line",
        PhoneNumberType.MOBILE: "Mobile",
        PhoneNumberType.FIXED_LINE_OR_MOBILE: "Fixed line or mobile",
        PhoneNumberType.TOLL_FREE: "Toll free",
        PhoneNumberType.PREMIUM_RATE: "Premium rate",
        PhoneNumberType.SHARED_COST: "Shared cost",
        PhoneNumberType.VOIP: "VoIP",
        PhoneNumberType.PERSONAL_NUMBER: "Personal number",
        PhoneNumberType.PAGER: "Pager",
        PhoneNumberType.UAN: "UAN",
        PhoneNumberType.VOICEMAIL: "Voicemail",
        PhoneNumberType.UNKNOWN: "Unknown",
    }

    return names.get(number_type, "Unknown")


def get_current_timezone():
    tz = datetime.now().astimezone().tzinfo

    if hasattr(tz, "key"):
        return tz.key

    return str(tz)


def get_current_utc_offset():
    return datetime.now().astimezone().utcoffset()


def calculate_timezone_difference(phone_timezone):
    try:
        now = datetime.now()

        phone_tz = ZoneInfo(phone_timezone)

        phone_offset = (
            now.replace(tzinfo=phone_tz).utcoffset()
        )

        current_offset = get_current_utc_offset()

        if phone_offset is None or current_offset is None:
            return None

        difference = phone_offset - current_offset

        return difference.total_seconds() / 3600

    except Exception:
        return None


def get_phone_current_times(phone_time_zones):
    current_times = {}

    for tz_name in phone_time_zones:
        try:
            current_time = datetime.now(
                ZoneInfo(tz_name)
            )

            current_times[tz_name] = {
                "date": current_time.strftime("%Y-%m-%d"),
                "time": current_time.strftime("%H:%M:%S"),
                "timezone": current_time.tzname(),
                "utc_offset": current_time.strftime("%z"),
                "datetime": current_time.strftime(
                    "%Y-%m-%d %H:%M:%S %z"
                )
            }

        except Exception:
            current_times[tz_name] = {
                "date": "Unknown",
                "time": "Unknown",
                "timezone": "Unknown",
                "utc_offset": "Unknown",
                "datetime": "Unknown"
            }

    return current_times


def analyze(number):

    try:
        parsed = phonenumbers.parse(number, None)

    except phonenumbers.NumberParseException as e:
        return {
            "error": f"Invalid phone-number format: {e}"
        }

    possible = phonenumbers.is_possible_number(parsed)
    valid = phonenumbers.is_valid_number(parsed)

    phone_time_zones = list(
        timezone.time_zones_for_number(parsed)
    )

    current_timezone = get_current_timezone()

    timezone_difference = None

    if phone_time_zones:
        timezone_difference = (
            calculate_timezone_difference(
                phone_time_zones[0]
            )
        )

    phone_current_times = (
        get_phone_current_times(
            phone_time_zones
        )
    )

    result = {
        "input": number,

        "international":
            phonenumbers.format_number(
                parsed,
                PhoneNumberFormat.INTERNATIONAL
            ),

        "e164":
            phonenumbers.format_number(
                parsed,
                PhoneNumberFormat.E164
            ),

        "national":
            phonenumbers.format_number(
                parsed,
                PhoneNumberFormat.NATIONAL
            ),

        "country_code":
            parsed.country_code,

        "national_number":
            str(parsed.national_number),

        "region":
            geocoder.description_for_number(
                parsed,
                "en"
            ),

        "carrier":
            carrier.name_for_number(
                parsed,
                "en"
            ),

        "number_type":
            type_name(
                phonenumbers.number_type(parsed)
            ),

        "possible":
            possible,

        "valid":
            valid,

        "time_zones":
            phone_time_zones,

        "current_timezone":
            current_timezone,

        "timezone_difference_hours":
            timezone_difference,

        "phone_current_times":
            phone_current_times
    }

    return result


def format_difference(difference):

    if difference is None:
        return "Unknown"

    if difference == 0:
        return "Same time zone"

    if difference > 0:
        return (
            f"+{difference:g} hours "
            "(phone timezone ahead)"
        )

    return (
        f"{difference:g} hours "
        "(phone timezone behind)"
    )


def print_report(data):

    if "error" in data:
        print(f"[!] {data['error']}")
        return

    print("\n" + "=" * 60)

    print(
        "PHONE NUMBER INTELLIGENCE CREATED BY JEDI1010"
    )

    print("=" * 60)

    print(
        f"Phone number:       {data['input']}"
    )

    print(
        f"International:      {data['international']}"
    )

    print(
        f"E.164:              {data['e164']}"
    )

    print(
        f"National:           {data['national']}"
    )

    print(
        f"Country code:       +{data['country_code']}"
    )

    print(
        f"National number:    {data['national_number']}"
    )

    print(
        f"Region:             "
        f"{data['region'] or 'Unknown'}"
    )

    print(
        f"Carrier:            "
        f"{data['carrier'] or 'Unknown'}"
    )

    print(
        f"Number type:        {data['number_type']}"
    )

    print(
        f"Possible:           {data['possible']}"
    )

    print(
        f"Valid:              {data['valid']}"
    )

    print()

    if data["time_zones"]:
        print(
            "Phone time zones:   "
            + ", ".join(data["time_zones"])
        )
    else:
        print(
            "Phone time zones:   Unknown"
        )

    print()

    print(
        f"Current system TZ:  "
        f"{data['current_timezone']}"
    )

    print(
        f"Time difference:    "
        f"{format_difference(data['timezone_difference_hours'])}"
    )

    print()

    print(
        "PHONE CURRENT DATE/TIME:"
    )

    if data["phone_current_times"]:

        for tz_name, info in (
            data["phone_current_times"].items()
        ):

            print(f"  {tz_name}")

            print(
                f"    Date:            "
                f"{info['date']}"
            )

            print(
                f"    Time:            "
                f"{info['time']}"
            )

            print(
                f"    Time zone:       "
                f"{info['timezone']}"
            )

            print(
                f"    UTC offset:      "
                f"{info['utc_offset']}"
            )

            print(
                f"    Current:         "
                f"{info['datetime']}"
            )

    else:
        print("  Unknown")

    print("=" * 60)


def main():

    if len(sys.argv) != 2:

        print(
            f"Usage: {sys.argv[0]} "
            "+971501234567"
        )

        sys.exit(1)

    number = sys.argv[1]

    result = analyze(number)

    print_report(result)

    try:

        with open(
            "phoneintel.json",
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                result,
                f,
                indent=4,
                ensure_ascii=False
            )

        print(
            "\n[+] JSON report saved to "
            "phoneintel.json"
        )

    except OSError as e:

        print(
            f"\n[!] Could not save JSON report: "
            f"{e}"
        )


if __name__ == "__main__":
    main()
