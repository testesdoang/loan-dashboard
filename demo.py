import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title='Demo Dashboard',
                   page_icon='🐧',
                   layout='wide')

st.title("Financial Insight Dashboard: Loan Performance & Trends")
st.divider()
st.markdown('---')

st.sidebar.header("Dashboard Filters and Features")

st.sidebar.markdown(
    '''
- **Overview**: Provides a summary of key loan metrics.
- **Time-Based Analysis**: Shows trends over time and loan amounts.
- **Loan Performance**: Analyzes loan conditions and distributions.
- **Financial Analysis**: Examines loan amounts and distributions based on conditions.
'''
)

loan = pd.read_pickle('data_input/loan_clean')
loan['purpose'] = loan['purpose'].str.replace('_'," ")

with st.container(border=True):
    col1,col2 = st.columns(2)

    with col1:
        st.metric('Total Loans',f"{loan['id'].count():,.0f}",help="Total Number of Loans")
        st.metric('Total Loan Amount',f"${loan['loan_amount'].sum():,.0f}",help='Sum of All Loans Amount')
    with col2:
        st.metric('Average Interest Rate',f"{loan['interest_rate'].mean():,.0f}%",help='Percentage of the Loan Amount That the Borrower Has to Pay')
        st.metric('Average Loan Amount',f"${loan['loan_amount'].mean():,.0f}",help='Average Interest Rate Across All Loans')

with st.container(border=True):
    tab1,tab2,tab3 = st.tabs(['Loans Issued Over Time','Loan Amount Over Time','Issue Date Analysis'])
    with tab1:
        loan_date_count = loan.groupby('issue_date')['loan_amount'].count()
        issuedate = loan['issue_date'].value_counts().sort_index()
        line_count = px.line(issuedate,
            markers = True,
            title = 'Number of Loans Issued Over Time',
            labels={
            'value':'Number of Loans',
            'issue_date':'Issue Date'
        },
        template='seaborn'
        ).update_layout(showlegend=False)
        st.plotly_chart(line_count)

    with tab2:
        loan_date_sum = loan.groupby('issue_date')['loan_amount'].sum()
        line_sum = px.line(loan_date_sum,
            markers = True,
            title = 'Loan Amount Over Time',
            labels={
            'value':'Number of Loans',
            'issue_date':'Issue Date'
        },
        template='seaborn').update_layout(showlegend=False)
        st.plotly_chart(line_sum)

    with tab3:
        loan_day_count = loan.groupby('issue_weekday')['loan_amount'].count()
        bar_day_count = px.bar(loan_day_count,
        category_orders = {
            'issue_weekday' : ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
        },
        title='Distribution of Loans by Day of the Week',
        labels={
            'value':'Number of Loans',
            'issue_weekday':'Day of the Week'
        },
        template='seaborn'
        ).update_layout(showlegend=False)
        st.plotly_chart(bar_day_count)

st.subheader("Loan Performance")

with st.expander('Click Here to Expand Visualization'):
    col3,col4=st.columns(2)
    with col3:
        pie_loans = px.pie(loan,
        names = 'loan_condition',
        hole = 0.5,
        title = 'Distribution of Loans by Condition',
        template='seaborn' 
        )
        st.plotly_chart(pie_loans)

    with col4:
        grade = loan['grade'].value_counts().sort_index()
        bar_loans_grade = px.bar(grade,
        title='Distribution of Loans by Grade',
        labels={
            'grade':'Grade',
            'value':'Number of Loans'
        },
        template='seaborn'   ).update_layout(showlegend=False)
        st.plotly_chart(bar_loans_grade)
st.divider()

st.subheader("Financial Analysis")

condition = st.selectbox('Select Loan Condition',['Good Loan','Bad Loan'])
loan_condition = loan[loan['loan_condition'] == condition]

with st.container(border=True):
    tab4,tab5 = st.tabs(['Loan Amount Distribution','Loan Amount Distribution by Purpose'])
    with tab4:
        hist_loan = px.histogram(
        loan_condition,
        x = 'loan_amount',
        title = 'Loan Amount Distribution by Condition',
        color = 'term',
        nbins = 20,
        template='seaborn',
        labels={
            'loan_amount':'Loan Amount',
            'term':'Loan Term'
        }
    )
        st.plotly_chart(hist_loan)

    with tab5:
        box_loan = px.box(loan_condition,
        x = 'purpose',
        y = 'loan_amount',
        color = 'term',
        title = 'Loan Amount Distribution by Purpose',
        labels = {
            'purpose' : 'Loan Purpose',
            'loan_amount' : 'Loan Amount',
            'term' : 'Loan Term'
        },
        template = 'seaborn'
        )
        st.plotly_chart(box_loan)