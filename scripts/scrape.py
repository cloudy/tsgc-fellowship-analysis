import pandas as pd
import numpy as np

# scrape rules
start_year = 2008
end_year = 2019
url_pre = 'http://www.tsgc.utexas.edu/grants/'
award_type = 'fellows'
all_data = pd.DataFrame()
f_dir = ''

for year in range(start_year, end_year + 1):
    try:
        print(year)
        url = url_pre + str(year) + '/' + award_type + '.html'
        df = pd.read_html(url, header=0)
        df = df[np.argmax([len(d) for d in df])]
        df['YEAR'] = year
        all_data = all_data.append(df, sort=False, ignore_index=True)
    except:
        print('Year not found:',year)

all_data.to_csv(f_dir+'tsgc-'+award_type+'-'+str(start_year)+'-'+str(end_year)+'.csv', index_label=False, index=False)
