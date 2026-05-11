#!/usr/bin/env python3
"""Rebuild cannery.ics from a hard-coded events list.

Self-contained: no external repo dependency. Edit the EVENTS list
to add or update deadlines, then run this script.
"""
import datetime
import pathlib

HERE = pathlib.Path(__file__).resolve().parent

# (uid_slug, summary, iso_date, description, url, categories, priority, alarms)
EVENTS = [
    (
        "llc-name-reservation-expires",
        "LA Name Reservation #092819327 EXPIRES",
        "2026-05-22",
        "Hard deadline. LA Secretary of State name reservation for Might Could Cannery LLC expires today. File Articles of Organization via geauxBIZ before this date or the name may be claimed.\nhttps://geauxbiz.sos.la.gov/",
        "https://geauxbiz.sos.la.gov/",
        "LLC,QSBS,HARD",
        1,
        [
            ("-P14D", "14 days to LA name reservation expiry"),
            ("-P7D", "1 week to LA name reservation expiry"),
            ("-P3D", "3 days to LA name reservation expiry"),
            ("-P1D", "1 day to LA name reservation expiry"),
        ],
    ),
    (
        "articles-of-org-target",
        "File LA Articles of Organization (target)",
        "2026-05-15",
        "Target file date with a 1-week buffer to the 2026-05-22 reservation expiry. Per Research_Gaps_Filled.md the QSBS-correct structure is a C-corp (DE or LA) issuing Series Seed preferred, not LLC member units.\nhttps://geauxbiz.sos.la.gov/",
        "https://geauxbiz.sos.la.gov/",
        "LLC,QSBS",
        1,
        [("-P3D", "3 days to Articles of Organization target")],
    ),
    (
        "sam-gov-registration-begin",
        "Begin SAM.gov registration (4-6 week processing)",
        "2026-05-15",
        "Begin SAM.gov the same day EIN is received. 4-6 week processing means USDA LFPP 2026-06-05 is likely unreachable without an existing registration. Required for all federal grant applications.\nhttps://sam.gov/",
        "https://sam.gov/",
        "LLC,GRANTS",
        2,
        (),
    ),
    (
        "call-senate-offices",
        "Call Sen. Cassidy + Kennedy re: FY2028 CPF pipeline",
        "2026-05-13",
        "This week task per grants calendar. FY2027 House Community Project Funding window closed. Contact Senate offices now to register for FY2028 earmark pipeline.\nCassidy: (225) 929-7711\nKennedy: (225) 926-8033",
        "",
        "GRANTS,EARMARKS",
        3,
        (),
    ),
    (
        "email-ldaf-rfsi",
        "Email LDAF re: next RFSI Louisiana cycle",
        "2026-05-13",
        "This week task. Highest-fit grant in the pipeline (5 stars). Aquaculture explicitly eligible. Last LA cycle closed April 2024; no announcement yet for next cycle.\nRFSI@ldaf.state.la.us",
        "https://www.ldaf.la.gov/business/grants-funding/resilient-food-systems-infrastructure",
        "GRANTS,LDAF",
        2,
        (),
    ),
    (
        "usda-lfpp-fy2026",
        "USDA LFPP FY2026 deadline ($500K ceiling)",
        "2026-06-05",
        "USDA AMS Local Food Promotion Program FY2026.\nCeiling: $500K impl / $100K plan. Match: 25% cash. Fit: 4 stars - aquaculture eligible.\nContact: FMLFPPgrants@usda.gov\nhttps://www.ams.usda.gov/services/grants/lfpp\n\nNOTE: SAM.gov + Grants.gov registration must be active.",
        "https://www.ams.usda.gov/services/grants/lfpp",
        "GRANTS,USDA",
        2,
        [
            ("-P14D", "2 weeks to USDA LFPP deadline"),
            ("-P3D", "3 days to USDA LFPP deadline"),
        ],
    ),
    (
        "nfwf-ncrf-2026-full",
        "NFWF NCRF 2026 Full Proposals (invitation only)",
        "2026-06-24",
        "NFWF National Coastal Resilience Fund 2026 - full proposals.\nCeiling: $7M. INVITATION ONLY. Pre-proposals closed March 31. Might Could not invited this cycle.\nhttps://www.nfwf.org/programs/national-coastal-resilience-fund/national-coastal-resilience-fund-2026-request-proposals",
        "https://www.nfwf.org/programs/national-coastal-resilience-fund/national-coastal-resilience-fund-2026-request-proposals",
        "GRANTS,REFERENCE",
        5,
        (),
    ),
    (
        "restore-act-direct",
        "RESTORE Act Direct Component (Jefferson Parish)",
        "2026-10-31",
        "U.S. Treasury / Jefferson Parish RESTORE Act Direct Component.\nFit: 3 stars. Parish must lead; for-profits ineligible as direct applicants.\nJefferson Parish: Michelle Gonzales - JPCoastalZone@JeffParish.net / (504) 736-6719",
        "https://home.treasury.gov/policy-issues/financial-markets-financial-institutions-and-fiscal-service/restore-act/direct-component",
        "GRANTS,RESTORE",
        3,
        [("-P30D", "30 days to RESTORE Direct deadline")],
    ),
]


def render():
    today = datetime.date.today()
    parts = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//Might Could Cannery//Deadlines Feed//EN",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        "X-WR-CALNAME:Might Could Cannery - Deadlines",
        "X-WR-CALDESC:LLC formation, grant deadlines, and QSBS milestones for Might Could Cannery",
        "X-WR-TIMEZONE:America/Chicago",
        "REFRESH-INTERVAL;VALUE=DURATION:PT1H",
        "X-PUBLISHED-TTL:PT1H",
    ]
    kept = 0
    for slug, summary, iso, desc, url, cats, priority, alarms in EVENTS:
        d = datetime.date.fromisoformat(iso)
        if d < today - datetime.timedelta(days=1):
            continue
        kept += 1
        nd = d + datetime.timedelta(days=1)
        uid = f"mcc-{slug}@calendar-feeds.philipinosis.github"
        block = [
            "BEGIN:VEVENT",
            f"UID:{uid}",
            f"SUMMARY:{summary}",
            f"DTSTART;VALUE=DATE:{d.strftime('%Y%m%d')}",
            f"DTEND;VALUE=DATE:{nd.strftime('%Y%m%d')}",
            f"DESCRIPTION:{desc.replace(chr(10), '\\n')}",
        ]
        if url:
            block.append(f"URL:{url}")
        if cats:
            block.append(f"CATEGORIES:{cats}")
        block.append(f"PRIORITY:{priority}")
        for trig, alarm_desc in alarms:
            block += [
                "BEGIN:VALARM",
                "ACTION:DISPLAY",
                f"TRIGGER:{trig}",
                f"DESCRIPTION:{alarm_desc}",
                "END:VALARM",
            ]
        block.append("END:VEVENT")
        parts.append("\n".join(block))
    parts.append("END:VCALENDAR")
    return "\n".join(parts) + "\n", kept


if __name__ == "__main__":
    ics, kept = render()
    (HERE / "cannery.ics").write_text(ics, encoding="utf-8")
    print(f"WROTE cannery.ics events={kept}")
