import requests, bs4

BASE_URL = 'https://finance.yahoo.com/quote/'


def safe_get(request, model_name):
    try:
        current_info = model_name.objects.get(owner=request.user)
    except model_name.DoesNotExist:
        current_info = None
    return current_info


def safe_get_nasdaq(request, model_name, nasdaq):
    try:
        current_info = model_name.objects.get(owner=request.user, nasdaq_symbol=nasdaq)
    except model_name.DoesNotExist:
        current_info = None
    return current_info


def compare_price(URL, set_price, user_agent, body):
    """ Compares set price for company stock to the price scraped off of Yahoo Finance
        using BeautifulSoup and returns an updated report.
    Args:
        URL: Yahoo Finance URL where price is scrapped.
        set_price: Desired price for that stock.
        user_agent: The User-Agent associated with computer.
        body: total report on which prices have dipped below desired prices.
    Returns:
        Updated total report on which prices have dipped below desired prices.
        body += '\nPrice right: ' + URL for success,
        body for otherwise.
    """
    headers = {
        "User-Agent": user_agent}

    res = requests.get(URL, headers=headers)

    if res:
        print('Successfully retrieved information')
        soup = bs4.BeautifulSoup(res.content, features="html.parser")
        data_extracted = soup.findAll('span', class_='Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)')
        price = data_extracted[0].getText()
        float_price = float(price.replace(',', ''))

        if set_price >= float_price:
            body += '\nPrice right: ' + URL
            print('good')
            return body, True, float_price
        else:
            print('bad')
            return body, False, float_price

    else:
        print('Not Found')
        return body, False, None