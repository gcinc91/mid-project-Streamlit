


def get_date(date):

    year = [i for i in str(date.year)]
    new_date = f'{date.day}/{date.month}/{"".join(year[2:])}'
    return new_date