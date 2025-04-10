from PySCHARE.pyschare.helpers.styles import get_label_styles, meta_layout, meta_style, box_layout, vbox_layout

from PySCHARE.pyschare.helpers.create_widgets import create_helper, get_text_fields, get_label_buttons, \
    get_uploader, get_date_picker, get_variable_text_area

from PySCHARE.pyschare.helpers.constants import datafacts_helper, metatable_helper, provenance_helper, \
    dictionary_helper, stats_helper, bar_plot_helper, plot_helper, correlation_helper, metadata, output_names, \
    button_labels, field_names

# chunk 1
import ipywidgets as wd
from IPython.display import display, HTML, clear_output
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
from scipy.stats import pearsonr, chi2_contingency


def generate_stats_table(df, columns, title, styles):
    html_content = f""" <html><table style="{styles['table']}">"""
    html_content += f""" <tr><th colspan="10" style="{styles['title']}">{title}</th></tr>"""
    html_content += f""" <tr><th style="{styles['first_header']}">name</th>"""
    html_content += f""" <th style="{styles['stats_header']}">type</th>"""
    html_content += f""" <th style="{styles['stats_header']}">count</th>"""
    html_content += f""" <th style="{styles['stats_header']}">missing</th>"""

    if title == "Ordinal" or title == "Nominal":
        html_content += f"""<th style="{styles['stats_header']}">unique</th>"""
        html_content += f"""<th style="{styles['stats_header']}">mostFreq</th>"""
        html_content += f"""<th style="{styles['stats_header']}">leastFreq</th></tr>"""
    else:
        html_content += f"""<th style="{styles['stats_header']}">min</th>"""
        html_content += f"""<th style="{styles['stats_header']}">median</th>"""
        html_content += f"""<th style="{styles['stats_header']}">max</th>"""
        html_content += f"""<th style="{styles['stats_header']}">mean</th>"""
        html_content += f"""<th style="{styles['stats_header']}">stdDeviation</th>"""
        html_content += f"""<th style="{styles['stats_header']}">zeros</th></tr>"""

    for col in columns:
        if col in df.columns:
            html_content += f"""<tr><td style="{styles['cell']}">{col}</td>"""
            html_content += f"""<td style="{styles['stats_cell']}">{df[col].dtype}</td>"""
            html_content += f"""<td style="{styles['stats_cell']}">{df[col].count()}</td>"""
            html_content += f"""<td style="{styles['stats_cell']}">{df[col].isnull().mean() * 100:.2f}%</td>"""

            if title == "Ordinal" or title == "Nominal":
                html_content += f"""<td style="{styles['stats_cell']}">{df[col].nunique()}</td>"""
                html_content += f"""<td style="{styles['stats_cell']}">{df[col].mode()[0] if not df[col].mode().empty else 'N/A'}</td>"""
                html_content += f"""<td style="{styles['stats_cell']}">{df[col].value_counts().idxmin() if not df[col].value_counts().empty else 'N/A'}</td></tr>"""
            else:
                html_content += f"""<td style="{styles['stats_cell']}">{df[col].min():.2f}</td>"""
                html_content += f"""<td style="{styles['stats_cell']}">{df[col].median():.2f}</td>"""
                html_content += f"""<td style="{styles['stats_cell']}">{df[col].max():.2f}</td>"""
                html_content += f"""<td style="{styles['stats_cell']}">{df[col].mean():.2f}</td>"""
                html_content += f"""<td style="{styles['stats_cell']}">{df[col].std():.2f}</td>"""
                html_content += f"""<td style="{styles['stats_cell']}">{(df[col] == 0).mean() * 100:.2f}%</td></tr>"""
    html_content += "</table></html>"

    with open(f'{title.lower()}_data.html', 'w') as f:
        f.write(html_content)

    display(HTML(html_content))
    return html_content



def get_columns(text):
    return [col.strip() for col in text.split(',')]


def get_options(ordinal_text, nominal_text):
    return ["None"] + get_columns(ordinal_text) + get_columns(nominal_text)


def upload_data(data_uploader):
    stats_df = pd.read_csv(BytesIO(data_uploader.value[0]['content']))
    display(stats_df.head())
    return stats_df


def get_variables(df, var1, var2):
    return df[[var1, var2]].drop_duplicates()

class _DataLabels:
    def __init__(self):
        self.dictionary_df = None
        self.stats_df = None
        self.outputs = {}
        self.metatext = metadata

        for name in output_names:
            self.outputs[name] = wd.Output()

        self.edit_button = {}
        self.save_button = {}

        for label in button_labels:
            self.edit_button[label] = get_label_buttons('Edit', 'firebrick')
            self.save_button[label] = get_label_buttons('Save', 'darkgray')

        self.stats_button = get_label_buttons('Show Statistics Table', 'darkgray')
        self.show_data_button = get_label_buttons('Show Data', 'darkgray')
        self.dictionary_uploader = get_uploader('Upload Data Dictionary')
        self.data_uploader = get_uploader('Upload Data')

        self.datafacts_help = create_helper(datafacts_helper, 'datafacts')
        self.metatable_help = create_helper(metatable_helper, 'metatable')
        self.provenance_help = create_helper(provenance_helper, 'provenance')
        self.dictionary_help = create_helper(dictionary_helper, 'dictionary')
        self.stats_help = create_helper(stats_helper, 'stats')
        self.barplot_help = create_helper(bar_plot_helper, 'barplot')
        self.plot_help = create_helper(plot_helper, 'plot')
        self.correlation_help = create_helper(correlation_helper, 'correlation')

        self.fields = {}

        for name in field_names:
            new_name = name.replace(' ', '_').lower()
            self.fields[new_name] = get_text_fields(name)

        self.ordinal_text = get_variable_text_area('Ordinal Variables')
        self.nominal_text = get_variable_text_area('Nominal Variables')
        self.continuous_text = get_variable_text_area('Continuous Variables')
        self.discrete_text = get_variable_text_area('Discrete Variables')

        self.time_from_field = get_date_picker('Data Collection (From)')
        self.time_to_field = get_date_picker('Data Collection (To)')

        self.text_container = wd.VBox([self.ordinal_text, self.nominal_text, self.continuous_text, self.discrete_text])

        self.var1_dropdown = wd.Dropdown(description='Variable Names:', disabled=False, style=meta_style,
                                         layout=meta_layout)
        self.var2_dropdown = wd.Dropdown(description='Variable Descriptions:', disabled=False, style=meta_style,
                                         layout=meta_layout)
        self.dropdown_container1 = wd.HBox([self.var1_dropdown, self.var2_dropdown])

        self.varA_dropdown = wd.Dropdown(description="Variable A:", options=["None", ""], value="None")
        self.varB_dropdown = wd.Dropdown(description="Variable B:", options=["None", ""], value="None")
        self.categorical_dropdown = wd.SelectMultiple(description="Categorical:", options=[],
                                                      style={'description_width': 'initial'})
        self.continuous_dropdown = wd.SelectMultiple(description="Continuous:", options=[],
                                                     style={'description_width': 'initial'})

        self.dropdown_container2 = wd.HBox([self.varA_dropdown, self.varB_dropdown])
        self.dropdown_container3 = wd.HBox([self.categorical_dropdown, self.continuous_dropdown])

        self.first_dropdown = wd.Dropdown(description='Variable 1:', options=["None", ""], value="None")
        self.second_dropdown = wd.Dropdown(description='Variable 2:', options=["None", ""], value="None")
        self.third_dropdown = wd.Dropdown(description='Variable 3:', options=["None", ""], value="None")
        self.dropdown_container4 = wd.HBox([self.first_dropdown, self.second_dropdown, self.third_dropdown])

        # chunk 8

        self.facts_input_area = wd.VBox(
            [self.fields['project_title'], self.fields['project_description'], self.save_button['facts']])

        self.meta_input_area = wd.VBox(
            [self.fields['filename'], self.fields['format'], self.fields['url'], self.fields['domain'],
             self.fields['keywords'], self.fields['type'],
             self.fields['geography'], self.fields['data_collection_method'], self.fields['time_method'],
             self.fields['rows'],
             self.fields['columns'], self.fields['cdes'],
             self.fields['missing'], self.fields['license'], self.fields['released'], self.time_from_field,
             self.time_to_field,
             self.fields['funding_agency'],
             self.fields['description'], self.save_button['meta']])

        self.pro_input_area = wd.VBox(
            [self.fields['source_name'], self.fields['source_url'], self.fields['source_email'],
             self.fields['author_name'],
             self.fields['author_url'], self.fields['author_email'], self.save_button['pro']])

        self.label_styles = get_label_styles()

        self.data_uploader.observe(self.update_data, names='value')

        self.varA_dropdown.observe(self.create_pair_plot, names='value')
        self.varB_dropdown.observe(self.create_pair_plot, names='value')
        self.categorical_dropdown.observe(self.calculate_correlations_new, names='value')
        self.continuous_dropdown.observe(self.calculate_correlations_new, names='value')
        self.first_dropdown.observe(self.show_catplots, names='value')
        self.second_dropdown.observe(self.show_catplots, names='value')
        self.third_dropdown.observe(self.show_catplots, names='value')

        self.save_button['facts'].on_click(self.save_facts_button_clicked)
        self.edit_button['facts'].on_click(self.edit_facts_button_clicked)

        self.save_button['meta'].on_click(self.save_meta_button_clicked)
        self.edit_button['meta'].on_click(self.edit_meta_button_clicked)

        self.save_button['pro'].on_click(self.save_pro_button_clicked)
        self.edit_button['pro'].on_click(self.edit_pro_button_clicked)

        self.dropdown_container = wd.HBox([self.var1_dropdown, self.var2_dropdown])
        self.dictionary_uploader.observe(self.dictionary_uploaded, names='value')

        self.var1_dropdown.observe(self.dropdown_changed, names='value')
        self.var2_dropdown.observe(self.dropdown_changed, names='value')

        self.ordinal_text.observe(self.update_dropdown_options, names='value')
        self.nominal_text.observe(self.update_dropdown_options, names='value')

        self.show_data_button.on_click(self.show_data_button_clicked)

        self.stats_button.on_click(self.stats_button_clicked)

    def generate_facts(self):
        facts = {
            "Project Title": self.fields['project_title'].value,
            "Project Description": self.fields['project_description'].value
        }

        facts_content = f"""
            <html>
            <table style="{self.label_styles['table']}">
                <tr><th style="{self.label_styles['first_title']}">Data Facts</th>
                   <th style="{self.label_styles['title']}"></th>
               </tr>
           """

        for key, value in facts.items():
            facts_content += f"""
                   <tr>
                       <td style="{self.label_styles['key_cell']}">{key}</td>
                       <td style="{self.label_styles['cell']}">{value}</td>
                   </tr>
                   """
        facts_content += "</table></html>"

        with open('facts.html', 'w') as f:
            f.write(facts_content)
        return facts_content

    def save_facts_button_clicked(self, b):
        self.facts_input_area.layout.display = 'none'
        facts_html = self.generate_facts()

        with self.outputs['facts']:
            clear_output(wait=True)
            display(HTML(facts_html))
            display(self.edit_button['facts'])

    def edit_facts_button_clicked(self, b):
        self.outputs['facts'].clear_output()
        self.facts_input_area.layout.display = 'block'

    def generate_metatable(self, text):
        new_fields = {
            "Filename": self.fields['filename'],
            "Format": self.fields['format'],
            "Study/Project URL": self.fields['url'],
            "Domain": self.fields['domain'],
            "Keywords": self.fields['keywords'],
            "Type": self.fields['type'],
            "Geography": self.fields['geography'],
            "Data Collection Method": self.fields['data_collection_method'],
            "Time Method": self.fields['time_method'],
            "Rows": self.fields['rows'],
            "Columns": self.fields['columns'],
            "CDEs": self.fields['cdes'],
            "Missing": self.fields['missing'],
            "License": self.fields['license'],
            "Released": self.fields['released'],
            "Data Collection Timeline": (self.time_from_field, self.time_to_field),
            "Funding Agency": self.fields['funding_agency'],
            "Description": self.fields['description']
        }

        for key, field in new_fields.items():
            if isinstance(field, tuple):
                text[key] = (field[0].value.strftime("%Y-%m-%d") if field[0].value else None,
                             field[1].value.strftime("%Y-%m-%d") if field[1].value else None)
            else:
                text[key] = field.value if key != "Released" else field.value.strftime(
                    "%Y-%m-%d") if field.value else None

        meta_content = f"""
            <html>
            <table style="{self.label_styles['table']}">
                <tr><th style="{self.label_styles['first_title']}">Metadata Table</th>
                   <th style="{self.label_styles['title']}"></th>
               </tr>
           """

        for key, value in text.items():
            if isinstance(value, tuple):
                meta_content += f"""
                   <tr>
                       <td colspan="2" style="{self.label_styles['key_cell']}">{key}</td>
                   </tr>
                   <tr>
                       <td style="{self.label_styles['sub_cell']}">From</td>
                       <td style="{self.label_styles['cell']}">{value[0]}</td>
                   </tr>
                   <tr>
                       <td style="{self.label_styles['sub_cell']}">To</td>
                       <td style="{self.label_styles['cell']}">{value[1]}</td>
                   </tr>
                   """
            else:
                meta_content += f"""
                   <tr>
                       <td style="{self.label_styles['key_cell']}">{key}</td>
                       <td style="{self.label_styles['cell']}">{value}</td>
                   </tr>
                   """
        meta_content += "</table></html>"

        with open('metatable.html', 'w') as f:
            f.write(meta_content)
        return meta_content

    def save_meta_button_clicked(self, b):
        self.meta_input_area.layout.display = 'none'
        meta_html = self.generate_metatable(self.metatext)

        with self.outputs['meta']:
            clear_output(wait=True)
            display(HTML(meta_html))
            display(self.edit_button['meta'])

    def edit_meta_button_clicked(self, b):
        self.outputs['meta'].clear_output()
        self.meta_input_area.layout.display = 'block'

    # chunk 13
    @property
    def generate_pro_table(self):
        provenance_data = {
            "Source": (
                self.fields['source_name'].value, self.fields['source_url'].value, self.fields['source_email'].value),
            "Author": (
                self.fields['author_name'].value, self.fields['author_url'].value, self.fields['author_email'].value)
        }

        pro_content = f"""
        <html>
        <table style="{self.label_styles['table']}">
            <tr><th style="{self.label_styles['first_title']}">Provenance</th>
               <th style="{self.label_styles['title']}"></th>
           </tr>
       """

        for key, value in provenance_data.items():
            pro_content += f"""
               <tr>
                   <td colspan="2" style="{self.label_styles['key_cell']}">{key}</td>
               </tr>
               <tr>
                   <td style="{self.label_styles['sub_cell']}">Name</td>
                   <td style="{self.label_styles['cell']}">{value[0]}</td>
               </tr>
               <tr>
                   <td style="{self.label_styles['sub_cell']}">URL</td>
                   <td style="{self.label_styles['cell']}">{value[1]}</td>
               </tr>
               <tr>
                   <td style="{self.label_styles['sub_cell']}">Email</td>
                   <td style="{self.label_styles['cell']}">{value[2]}</td>
               </tr>
            """

        pro_content += "</table></html>"

        with open('provenance_data.html', 'w') as f:
            f.write(pro_content)

        return pro_content

    def save_pro_button_clicked(self, b):
        self.pro_input_area.layout.display = 'none'
        prov_html = self.generate_pro_table

        with self.outputs['pro']:
            clear_output(wait=True)
            display(HTML(prov_html))
            display(self.edit_button['pro'])

    def edit_pro_button_clicked(self, b):
        self.outputs['pro'].clear_output()
        self.pro_input_area.layout.display = 'block'

    # chunk 14

    def dictionary_uploaded(self, change):
        # global dictionary_df
        dictionary_df = pd.read_csv(BytesIO(self.dictionary_uploader.value[0]['content']))
        options = dictionary_df.columns.tolist()
        self.var1_dropdown.options = options
        self.var2_dropdown.options = options

        display(self.dropdown_container)

    # chunk 15
    def generate_variable_table(self, variables_df):

        html_content = f"""
        <html>
        <table style="{self.label_styles['table']}">
            <tr>
                <th style="{self.label_styles['first_title']}">Variables</th>
                <th style="{self.label_styles['title']}"></th>
            </tr>
        """

        for index, row in variables_df.iterrows():
            html_content += f"""
            <tr>
                <td style="{self.label_styles['key_cell_variable']}">{row[0]}</td>
                <td style="{self.label_styles['cell']}">{row[1]}</td>
            </tr>
            """

        html_content += "</table></html>"

        with open("variables.html", 'w') as file:
            file.write(html_content)

        # display(HTML(html_content))
        return html_content

    def dropdown_changed(self, change):
        if self.var1_dropdown.value and self.var2_dropdown.value:
            variables_df = get_variables(self.dictionary_df, self.var1_dropdown.value, self.var2_dropdown.value)
            var_html = self.generate_variable_table(variables_df)

        with self.outputs['var']:
            clear_output(wait=True)
            display(HTML(var_html))

    # chunk 16

    def update_dropdown_options(self, change=None):
        value_options = get_options(self.ordinal_text.value, self.nominal_text.value)
        self.first_dropdown.options = value_options
        self.second_dropdown.options = value_options
        self.third_dropdown.options = value_options

    def show_data_button_clicked(self, b):
        self.upload_data(self.data_uploader())
        with self.outputs['show_data']:
            clear_output(wait=True)
            display(self.stats_df.head())
            display(self.text_container)

    # chunk 18
    def stats_button_clicked(self, b):
        display(wd.VBox([self.stats_button], layout=box_layout))
        with self.outputs['stats']:
            clear_output(wait=True)

            # df = pd.read_csv(BytesIO(data_uploader.value[0]['content']))
            ordinal_var = get_columns(self.ordinal_text.value)
            nominal_var = get_columns(self.nominal_text.value)
            continuous_var = get_columns(self.continuous_text.value)
            discrete_var = get_columns(self.discrete_text.value)

            if ordinal_var:
                generate_stats_table(self.stats_df, ordinal_var, "Ordinal", self.label_styles)
            if nominal_var:
                generate_stats_table(self.stats_df, nominal_var, "Nominal", self.label_styles)
            if continuous_var:
                generate_stats_table(self.stats_df, continuous_var, "Continuous", self.label_styles)
            if discrete_var:
                generate_stats_table(self.stats_df, discrete_var, "Discrete", self.label_styles)

    def update_data(self, change):
        self.upload_data(self.data_uploader())
        options = ["None"] + self.stats_df.columns.tolist()
        self.varA_dropdown.options = options
        self.varB_dropdown.options = options
        self.categorical_dropdown.options = options
        self.continuous_dropdown.options = options
        # update_dropdown_options(None)
        self.create_pair_plot(None)
        # show_barplots(None)
        self.show_catplots(None)
        self.calculate_correlations_new(None)

    def show_catplots(self, change):
        stats_df = self.upload_data(self.data_uploader())

        cat1 = self.first_dropdown.value
        cat2 = self.second_dropdown.value
        cat3 = self.third_dropdown.value

        with self.outputs['hist']:
            clear_output(wait=True)
        # plt.figure(figsize=(10, 6))

        if cat1 == "None" and cat2 == "None" and cat3 == "None":
            return

        if cat1 != "None" and cat2 == "None" and cat3 == "None":
            sns.catplot(data=stats_df, x=cat1, kind="count")
            plt.show()
            plt.close()

        elif cat1 != "None" and cat2 != "None" and cat3 == "None":
            sns.catplot(data=stats_df, x=cat1, kind="count")
            sns.catplot(data=stats_df, x=cat2, kind="count")
            sns.catplot(data=stats_df, x=cat1, hue=cat2, kind="count")
            plt.show()
            plt.close()

        elif cat1 != "None" and cat2 != "None" and cat3 != "None":
            sns.catplot(data=stats_df, x=cat1, kind="count")
            sns.catplot(data=stats_df, x=cat2, kind="count")
            sns.catplot(data=stats_df, x=cat3, kind="count")
            sns.catplot(data=stats_df, x=cat1, hue=cat2, kind="count")
            sns.catplot(data=stats_df, x=cat1, hue=cat3, kind="count")
            sns.catplot(data=stats_df, x=cat2, hue=cat3, kind="count")
            sns.catplot(data=stats_df, x=cat1, hue=cat2, col=cat3, kind="count")
            plt.show()
            plt.close()

    def create_pair_plot(self, change):

        clear_output(wait=True)
        fig, axes = plt.subplots(2, 2, figsize=(14, 12))
        if self.varA_dropdown.value != "None" and self.varB_dropdown.value != "None":
            ct_counts = self.stats_df.groupby([self.varA_dropdown.value, self.varB_dropdown.value]).size()
            ct_counts = ct_counts.reset_index(name='count')
            ct_countsA = ct_counts.pivot(index=self.varA_dropdown.value, columns=self.varB_dropdown.value,
                                         values='count')
            ct_countsB = ct_counts.pivot(index=self.varB_dropdown.value, columns=self.varA_dropdown.value,
                                         values='count')

            sns.histplot(self.stats_df[self.varA_dropdown.value], kde=False, color=".3", ax=axes[0, 0])
            sns.histplot(self.stats_df[self.varB_dropdown.value], kde=False, color=".3", ax=axes[1, 1])

            sns.heatmap(ct_countsA, ax=axes[0, 1])
            sns.heatmap(ct_countsB, ax=axes[1, 0])
        elif self.varA_dropdown.value != "None":
            sns.histplot(self.stats_df[self.varA_dropdown.value], kde=False, color=".3", ax=axes[0, 0])
            axes[1, 1].set_visible(False)
            axes[0, 1].set_visible(False)
            axes[1, 0].set_visible(False)
        elif self.varB_dropdown.value != "None":
            sns.histplot(self.stats_df[self.varB_dropdown.value], kde=False, color=".3", ax=axes[1, 1])
            axes[0, 0].set_visible(False)
            axes[0, 1].set_visible(False)
            axes[1, 0].set_visible(False)
        else:
            print("Please select at least one variable for analysis.")
            axes[0, 0].set_visible(False)
            axes[1, 1].set_visible(False)
            axes[0, 1].set_visible(False)
            axes[1, 0].set_visible(False)

        with self.outputs['pair_plot']:
            clear_output(wait=True)
            plt.show()

    # chunk 22
    def calculate_correlations_new(self, change):
        self.stats_df = self.upload_data(self.data_uploader())
        clear_output(wait=True)
        display(wd.VBox([self.categorical_dropdown, self.continuous_dropdown]))

        categorical_vars = [var for var in self.categorical_dropdown.value if var != "None"]
        continuous_vars = [var for var in self.continuous_dropdown.value if var != "None"]

        if categorical_vars:
            df_categorical = pd.get_dummies(self.stats_df[categorical_vars])
        else:
            df_categorical = pd.DataFrame()

        df_continuous = self.stats_df[continuous_vars] if continuous_vars else pd.DataFrame()

        df_combined = pd.concat([df_categorical, df_continuous], axis=1)

        corr_matrix = pd.DataFrame(np.zeros((df_combined.shape[1], df_combined.shape[1])),
                                   columns=df_combined.columns,
                                   index=df_combined.columns)

        for var1 in df_combined.columns:
            for var2 in df_combined.columns:
                if var1 in df_categorical.columns and var2 in df_categorical.columns:
                    confusion_matrix = pd.crosstab(df_combined[var1], df_combined[var2])
                    chi2, _, _, _ = chi2_contingency(confusion_matrix)
                    n = confusion_matrix.sum().sum()
                    r, k = confusion_matrix.shape
                    cramers_v = np.sqrt(chi2 / (n * (min(k - 1, r - 1))))
                    corr_matrix.at[var1, var2] = cramers_v
                elif var1 in df_continuous.columns and var2 in df_continuous.columns:
                    corr_matrix.at[var1, var2], _ = pearsonr(df_combined[var1], df_combined[var2])
                else:
                    corr_matrix.at[var1, var2], _ = pearsonr(df_combined[var1], df_combined[var2])

        plt.figure(figsize=(14, 12))
        sns.heatmap(corr_matrix, annot=True, cmap='Spectral', fmt='.2f', square=False)
        plt.title('Correlation Matrix')

        with self.outputs['corr_plot']:
            clear_output(wait=True)
            plt.show()


def get_facts():
    facts_instance = _DataLabels()
    return display(wd.VBox([facts_instance.datafacts_help], layout=vbox_layout),
                   wd.VBox([facts_instance.facts_input_area], layout=vbox_layout),
                   facts_instance.outputs['facts'])


def get_meta():
    meta_instance = _DataLabels()
    return display(wd.VBox([meta_instance.metatable_help], layout=vbox_layout),
                   wd.VBox([meta_instance.meta_input_area], layout=vbox_layout),
                   meta_instance.outputs['meta'])


def get_provenance():
    pro_instance = _DataLabels()
    return display(wd.VBox([pro_instance.provenance_help], layout=vbox_layout),
                   wd.VBox([pro_instance.pro_input_area], layout=vbox_layout),
                   pro_instance.outputs['pro'])


def get_dictionary():
    dict_instance = _DataLabels()
    return display(wd.VBox([dict_instance.dictionary_help]), wd.VBox([dict_instance.dictionary_uploader]),
                   dict_instance.dropdown_container1, dict_instance.outputs['var'])


def get_data_summary():
    sum_instance = _DataLabels()
    return display(wd.VBox([sum_instance.stats_help]), wd.VBox([sum_instance.data_uploader], layout=vbox_layout),
                   wd.VBox([sum_instance.show_data_button], layout=vbox_layout),
                   wd.VBox([sum_instance.outputs['show_data']]))


def get_summary_stats():
    stat_instance = _DataLabels()
    return display(stat_instance.stats_button, stat_instance.outputs['stats'])


def get_show_barplots():
    bar_instance = _DataLabels()
    return display(wd.VBox([bar_instance.barplot_help]), bar_instance.dropdown_container4, bar_instance.outputs['bars'])


def get_show_pairplots():
    show_instance = _DataLabels()
    return display(wd.VBox([show_instance.plot_help]), show_instance.dropdown_container2,
                   show_instance.outputs['pair_plot'])

def get_show_correlations():
    cor_instance = _DataLabels()
    return display(wd.VBox([cor_instance.correlation_help]), cor_instance.dropdown_container3,
                   cor_instance.outputs['corr_plot'])

def get_labels():
    get_facts()
    get_meta()
    get_provenance()
    get_dictionary()
    get_data_summary()
    get_summary_stats()
    get_show_barplots()
    get_show_pairplots()
    get_show_correlations()
