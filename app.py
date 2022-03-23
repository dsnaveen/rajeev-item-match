import streamlit as st
import pandas as pd
import numpy as np
import os
import warnings
warnings.filterwarnings('ignore')
import re
from fuzzywuzzy import process
import streamlit as st
import xlsxwriter
from io import BytesIO
from utils import *

st.header('Item Matching')

target_file = st.file_uploader("Please upload the target input file")
if target_file is not None:
	df_target = pd.read_excel(target_file)

	target = [x.lower().strip() for x in set(df_target['target'])]

input_file = st.file_uploader("Please upload the daily input file")

if input_file is not None:
	df_excel = pd.ExcelFile(input_file)
	sheets = df_excel.sheet_names

	sheetname = st.selectbox('Choose your sheet',sheets)

	st.write('You selected:', sheetname)

	df_input  = pd.read_excel(input_file, sheet_name=sheetname)

	df_input.columns = [col.lower().strip() for col in df_input.columns]

if input_file is not None and target_file is not None:
	st.write('Both files are successfully uploaded')

	if st.button('Run'):
		df_input['match1'] = df_input['description of goods.'].apply(lambda x : get_regex_match(x, target))

		outname = sheetname.strip().replace(' ','')

		csv = convert_df(df_input)

		st.download_button(
		     label="Download data as CSV",
		     data=csv,
		     file_name=f'{outname}.csv',
		     mime='text/csv',
		 )

