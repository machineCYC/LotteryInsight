from datetime import date


def get_today():
    today = date.today().strftime("%Y-%m-%d")
    return today


def transfer_commonera2rocera(year: str):
    return str(int(year) - 1911)


def transfer_date2ym(date: str):
    ym = "-".join(date.split('-')[:2])
    return ym


def create_year_month_list(start_ym: str, end_ym: str):
    start_year, start_month = start_ym.split("-")
    end_year, end_month = end_ym.split("-")

    years = [y for y in range(int(start_year), int(end_year) + 1, 1)]
    months = [m for m in range(1, 13)]

    ym_list = [
        dict(year=y, month=m)
        for y in years
        for m in months
        if (
            (y < int(end_year))
            or ((y == int(end_year) and (m <= int(end_month))))
        )
        and (
            (y > int(start_year))
            or (y == int(start_year) and (m >= int(start_month)))
        )
    ]
    return ym_list
