from dotenv import load_dotenv
from gftools import (GuruFinancials, GuruStockAnnualTenK, GuruDividendHistory, GuruPriceHistory, GuruAnnualMarketValue)
import os

load_dotenv()
gt = os.getenv('guru_token')
ticker = 'txn'


div_data = GuruDividendHistory(ticker=ticker, token=gt)
price_data = GuruPriceHistory(ticker=ticker, token=gt)
fin_data = GuruFinancials(ticker=ticker, token=gt)
annual_data = GuruStockAnnualTenK(ticker=ticker, token=gt)
value_data = GuruAnnualMarketValue(ticker=ticker, token=gt)

print(value_data.api_data_df_nrm)