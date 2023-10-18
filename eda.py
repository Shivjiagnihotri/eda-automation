import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme(color_codes=True)
import warnings

st.title("Simplified EDA: Uncover Data Insights Effortlessly")

# Upload the CSV file
uploaded_file = st.file_uploader("Upload CSV file:")

# Check if the file is uploaded
if uploaded_file is not None:
    # Read the CSV file into a Pandas DataFrame
    df = pd.read_csv(uploaded_file)

    # Show the DataFrame
    st.dataframe(df)

    # Select EDA Method
    select_method = st.selectbox('Select your Single Value Exploratory Data Analysis Method', ("Countplot Barchart", "Pie Chart", "Boxplot", "Histplot"))

    if select_method == "Countplot Barchart":
        # Get the names of all columns with data type 'object' (categorical columns) excluding 'Country'
        cat_vars = df.select_dtypes(include='object').columns.tolist()

        # Create a figure with subplots
        num_cols = len(cat_vars)
        num_rows = (num_cols + 2) // 3
        fig, axs = plt.subplots(nrows=num_rows, ncols=3, figsize=(15, 5*num_rows))
        axs = axs.flatten()

        # Create a countplot for the top 10 values of each categorical variable using Seaborn
        for i, var in enumerate(cat_vars):
            top_values = df[var].value_counts().head(10).index
            filtered_df = df.copy()
            filtered_df[var] = df[var].apply(lambda x: x if x in top_values else 'Other')
            sns.countplot(x=var, data=filtered_df, ax=axs[i])
            axs[i].set_title(var)
            axs[i].tick_params(axis='x', rotation=90)

        # Remove any extra empty subplots if needed
        if num_cols < len(axs):
            for i in range(num_cols, len(axs)):
                fig.delaxes(axs[i])

        # Adjust spacing between subplots
        fig.tight_layout()

        # Show plots using Streamlit
        st.pyplot(fig)
    
    elif select_method == "Pie Chart":
        # Specify the maximum number of categories to show individually
        max_categories = 5

        # Filter categorical columns with 'object' data type
        cat_cols = [col for col in df.columns if col != 'y' and df[col].dtype == 'object']

        # Create a figure with subplots
        num_cols = len(cat_cols)
        num_rows = (num_cols + 2) // 3
        fig, axs = plt.subplots(nrows=num_rows, ncols=3, figsize=(20, 5*num_rows))
        axs = axs.flatten()

        # Create a pie chart for each categorical column
        for i, col in enumerate(cat_cols):
            if i < len(axs):  # Ensure we don't exceed the number of subplots
                # Count the number of occurrences for each category
                cat_counts = df[col].value_counts()

                # Group categories beyond the top max_categories as 'Other'
                if len(cat_counts) > max_categories:
                    top_categories = cat_counts.head(max_categories)
                    other_category = pd.Series(cat_counts[max_categories:].sum(), index=['Other'])
                    cat_counts = pd.concat([top_categories, other_category])

                # Create a pie chart
                axs[i].pie(cat_counts, labels=cat_counts.index, autopct='%1.1f%%', startangle=90)
                axs[i].set_title(f'{col} Distribution')

        # Remove any extra empty subplots if needed
        if num_cols < len(axs):
            for i in range(num_cols, len(axs)):
                fig.delaxes(axs[i])

        # Adjust spacing between subplots
        fig.tight_layout()

        # Display plots using Streamlit
        st.pyplot(fig)

   
    elif select_method == "Boxplot":
        # Get the names of all columns with data type 'int' or 'float', excluding 'churn_risk_score'
        num_vars = df.select_dtypes(include=['int', 'float']).columns.tolist()

        # Create a figure with subplots
        num_cols = len(num_vars)
        num_rows = (num_cols + 2) // 3
        fig, axs = plt.subplots(nrows=num_rows, ncols=3, figsize=(15, 5*num_rows))
        axs = axs.flatten()

        # Create a box plot for each numerical variable using Seaborn
        for i, var in enumerate(num_vars):
            sns.boxplot(x=df[var], ax=axs[i])
            axs[i].set_title(var)

        # Remove any extra empty subplots if needed
        if num_cols < len(axs):
            for i in range(num_cols, len(axs)):
                fig.delaxes(axs[i])

        # Adjust spacing between subplots
        fig.tight_layout()

        # Display the boxplot using Streamlit
        st.pyplot(fig)

    elif select_method == "Histplot":
        # Get the names of all columns with data type 'int'
        int_vars = df.select_dtypes(include=['int', 'float']).columns.tolist()

        # Create a figure with subplots
        num_cols = len(int_vars)
        num_rows = (num_cols + 2) // 3  # To make sure there are enough rows for the subplots
        fig, axs = plt.subplots(nrows=num_rows, ncols=3, figsize=(15, 5*num_rows))
        axs = axs.flatten()

        # Create a histogram for each integer variable
        for i, var in enumerate(int_vars):
            df[var].plot.hist(ax=axs[i])
            axs[i].set_title(var)

        # Remove any extra empty subplots if needed
        if num_cols < len(axs):
            for i in range(num_cols, len(axs)):
                fig.delaxes(axs[i])

        # Adjust spacing between subplots
        fig.tight_layout()

        # Show plot
        st.pyplot(fig)


    # Select EDA Method
    select_method2 = st.selectbox('Select your Categorial Exploratory Data Analysis Method', ("Multi Class Boxplot", "Multiclass Barplot", "Multi Class Density Plot", "Multi Class Histplot"))

    if select_method2 == "Multi Class Boxplot":
        # Get the names of all columns with data type 'object' (categorical columns)
        cat_cols = df.select_dtypes(include='object').columns.tolist()
        selected_column = st.selectbox('Select a categorical column:', cat_cols)

        num_vars = df.select_dtypes(include=['int', 'float']).columns.tolist()
        # Select a categorical column
        int_vars = df.select_dtypes(include=['int', 'float']).columns.tolist()
        int_vars = [col for col in num_vars if col != selected_column]

        # Create a figure with subplots
        num_cols = len(int_vars)
        num_rows = (num_cols + 2) // 3  # To make sure there are enough rows for the subplots
        fig, axs = plt.subplots(nrows=num_rows, ncols=3, figsize=(15, 5*num_rows))
        axs = axs.flatten()
        # Create a box plot for each integer variable using Seaborn with hue='attrition'
        for i, var in enumerate(int_vars):
            sns.boxplot(y=var, x=selected_column, data=df, ax=axs[i])
            axs[i].set_title(var)

        # Remove any extra empty subplots if needed
        if num_cols < len(axs):
            for i in range(num_cols, len(axs)):
                fig.delaxes(axs[i])

        # Adjust spacing between subplots
        fig.tight_layout()

        # Show plot
        st.pyplot(fig)

    elif select_method2 == "Multiclass Barplot":
        # Get the names of all columns with data type 'object' (categorical columns)
        cat_cols = df.select_dtypes(include='object').columns.tolist()
        selected_column = st.selectbox('Select a categorical column:', cat_cols)

        # Get the names of all columns with data type 'object' (categorical variables)
        cat_vars = df.select_dtypes(include=['object']).columns.tolist()

        # Exclude 'Country' from the list if it exists in cat_vars
        if selected_column in cat_vars:
            cat_vars.remove(selected_column)

        # Create a figure with subplots, but only include the required number of subplots
        num_cols = len(cat_vars)
        num_rows = (num_cols + 2) // 3  # To make sure there are enough rows for the subplots
        fig, axs = plt.subplots(nrows=num_rows, ncols=3, figsize=(15, 5*num_rows))
        axs = axs.flatten()

        # Create a count plot for each categorical variable
        for i, var in enumerate(cat_vars):
            filtered_df = df[df[var].notnull()]  # Exclude rows with NaN values in the variable
            sns.countplot(x=var, hue=selected_column, data=filtered_df, ax=axs[i])
            axs[i].set_xticklabels(axs[i].get_xticklabels(), rotation=90)

        # Remove any remaining blank subplots
        for i in range(num_cols, len(axs)):
            fig.delaxes(axs[i])

        # Adjust spacing between subplots
        fig.tight_layout()

        # Show plot
        st.pyplot(fig)
    
    elif select_method2 == "Multi Class Density Plot":
        # Get the names of all columns with data type 'object' (categorical columns)
        cat_cols = df.select_dtypes(include='object').columns.tolist()
        selected_column = st.selectbox('Select a categorical column:', cat_cols)

        # Get the names of all columns with data type 'object' (categorical variables)
        cat_vars = df.select_dtypes(include=['object']).columns.tolist()

        # Exclude 'Attrition' from the list if it exists in cat_vars
        if  selected_column in cat_vars:
            cat_vars.remove( selected_column)

        # Create a figure with subplots, but only include the required number of subplots
        num_cols = len(cat_vars)
        num_rows = (num_cols + 2) // 3  # To make sure there are enough rows for the subplots
        fig, axs = plt.subplots(nrows=num_rows, ncols=3, figsize=(15, 5*num_rows))
        axs = axs.flatten()

        # Create a count plot for the top 6 values of each categorical variable as a density plot
        for i, var in enumerate(cat_vars):
            top_values = df[var].value_counts().nlargest(6).index
            filtered_df = df[df[var].isin(top_values)]
    
            # Set x-tick positions explicitly
            tick_positions = range(len(top_values))
            axs[i].set_xticks(tick_positions)
            axs[i].set_xticklabels(top_values, rotation=90)  # Set x-tick labels
    
            sns.histplot(x=var, hue= selected_column, data=filtered_df, ax=axs[i], multiple="fill", kde=False, element="bars", fill=True, stat='density')
            axs[i].set_xlabel(var)

        # Remove any remaining blank subplots
        for i in range(num_cols, len(axs)):
            fig.delaxes(axs[i])

        # Adjust spacing between subplots
        fig.tight_layout()

        # Show plot
        st.pyplot(fig)

    elif select_method2 == "Multi Class Histplot":
        # Get the names of all columns with data type 'object' (categorical columns)
        cat_cols = df.select_dtypes(include='object').columns.tolist()
        selected_column = st.selectbox('Select a categorical column:', cat_cols)

        # Get the names of all columns with data type 'int'
        int_vars = df.select_dtypes(include=['int', 'float']).columns.tolist()
        int_vars = [col for col in num_vars if col != selected_column]

        # Create a figure with subplots
        num_cols = len(int_vars)
        num_rows = (num_cols + 2) // 3  # To make sure there are enough rows for the subplots
        fig, axs = plt.subplots(nrows=num_rows, ncols=3, figsize=(15, 5*num_rows))
        axs = axs.flatten()

        # Create a histogram for each integer variable with hue='Attrition'
        for i, var in enumerate(int_vars):
            sns.histplot(data=df, x=var, hue=selected_column, kde=True, ax=axs[i])
            axs[i].set_title(var)

        # Remove any extra empty subplots if needed
        if num_cols < len(axs):
            for i in range(num_cols, len(axs)):
                fig.delaxes(axs[i])

        # Adjust spacing between subplots
        fig.tight_layout()

        # Show plot
        st.pyplot(fig)