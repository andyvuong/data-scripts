"""
    Data Source: https://www.quandl.com/
    
    @author Andy Vuong
            08/2016
"""
import sys, json
import requests

def getAuth():
    """
      Reads a config file for the auth key for the data source's API
    """
    with open('./configs') as f:
        for line in f:
            params = line.split('=');    
            if params[0] == 'stock_auth':
                return params[1]

def buildQuery(ticker, start_date, end_date, key):
    """
      Builds a new query to make to the the data source API endpoint
    """
    return 'https://www.quandl.com/api/v3/datasets/WIKI/{}.json?&start_date={}&end_date={}&column_index=4&api_key={}' \
    .format(ticker, start_date, end_date, key)

def queryPriceSource(query):
    """
      Sends a new query to the data source API endpoint and processes the response
    """
    print 'Query: {}'.format(query)
    data = requests.get(query).json()
    return computeAverage(data['dataset']['data'])
    

def computeAverage(dataset):
    """
      Computes the average closing price for the given dataset
    """
    return sum([item[1] for item in dataset]) / len(dataset)

def main():
    if len(sys.argv) < 4:
        print 'Gets the average closing price of the given company from the specified start-date to end-date.'
        print 'Please note that information is pulled from a community database. \n'
        print 'USAGE: "python get-stock.py <ticker> <start ~ 2014-01-01> <end ~ 2014-01-31>"'
        return
    key = getAuth()
    start = sys.argv[2]
    end = sys.argv[3]
    query = buildQuery(sys.argv[1], start, end, key)
    print 'Average from {} to {}: {}'.format(start, end, queryPriceSource(query))

if __name__ == "__main__":
    main()