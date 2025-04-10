import pandas as pd
import numpy as np
from IPython.display import display_html

class WoeIvCalculator:
    def __init__(self, df, target):
        self.df = df
        self.target = target

    def calculate_woe_iv(self, feature):
        lst = []
        for i in range(self.df[feature].nunique()):
            val = list(self.df[feature].unique())[i]
            lst.append({
                'Value': val,
                'All': self.df[self.df[feature] == val].count()[feature],
                'Good': self.df[(self.df[feature] == val) & (self.df[self.target] == 0)].count()[feature],
                'Bad': self.df[(self.df[feature] == val) & (self.df[self.target] == 1)].count()[feature]
            })

        dset = pd.DataFrame(lst)
        dset['Share'] = dset['All'] / dset['All'].sum()
        dset['Bad Rate'] = dset['Bad'] / dset['All']
        dset['Good Rate'] = dset['Good'] / dset['All']
        dset['Distribution Bad'] = dset['Bad'] / dset['Bad'].sum()
        dset['Distribution Good'] = dset['Good'] / dset['Good'].sum()
        dset['WoE'] = np.log(dset['Distribution Good'] / dset['Distribution Bad'])
        dset['IV'] = (dset['Distribution Good'] - dset['Distribution Bad']) * dset['WoE']
        dset = dset.replace([np.inf, -np.inf], 0)
        dset['IV'] = dset['IV'].sum()

        dset['Bad Rate'] = dset['Bad Rate'].apply(lambda x: f'{x:.2f}%')
        dset['Good Rate'] = dset['Good Rate'].apply(lambda x: f'{x:.2f}%')
        dset['Distribution Bad'] = dset['Distribution Bad'].apply(lambda x: f'{x:.2f}%')
        dset['Distribution Good'] = dset['Distribution Good'].apply(lambda x: f'{x:.2f}%')

        return dset[['Category', 'All', 'Good', 'Bad', 'Good Rate', 'Bad Rate', 'Distribution Good', 'Distribution Bad', 'WoE', 'IV']]

    def calculate_woe_iv_for_all_features(self):
        result_html = ""
        for feature in self.features:
            woe_iv_df = self.calculate_woe_iv(self.df, feature, self.target)
            woe_iv_df['Feature'] = feature
            woe_iv_df = woe_iv_df[['Feature', 'Category', 'All', 'Good', 'Bad', 'Good Rate', 'Bad Rate', 'Distribution Good', 'Distribution Bad', 'WoE', 'IV']]
            woe_iv_df = woe_iv_df.sort_values(by='WoE', ascending=False)
            
            def color_woe(val):
                color = 'background: linear-gradient(90deg, transparent {0}%, lightgreen {0}%, lightgreen {1}%, transparent {1}%)'.format(50, 50 + int(val * 50)) if val > 0 else 'background: linear-gradient(90deg, transparent {0}%, lightcoral {0}%, lightcoral {1}%, transparent {1}%)'.format(50 + int(val * 50), 50)
                return color

            woe_iv_df['WoE'] = woe_iv_df['WoE'].apply(lambda x: f'<div style="width: 150px; {color_woe(x)}">{x:.4f}</div>')
            result_html += woe_iv_df.to_html(escape=False, index=False, justify='center', border=0, classes='dataframe table text-center', table_id='woe_iv_table') + "<br>"

        display_html(f'<div style="width: 100%;">{result_html}</div>', raw=True)
