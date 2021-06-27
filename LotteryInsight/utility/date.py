from datetime import date


def get_today():
    today = date.today().strftime("%Y-%m-%d")
    return today


def get_ym():
    ym = date.today().strftime("%Y-%m")
    return ym


def split_date2yearmonthdate(date):
    year, month, date = date.split("-")
    return year, month, date


def transfer_commonera2rocera(year):
    return str(int(year) - 1911)


def create_year_month_list(start_ym, end_ym):
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
