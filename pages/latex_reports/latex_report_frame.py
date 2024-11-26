from pylatex import (
    Document,
    PageStyle,
    Head,
    Section,
    Tabular,
    Center,
    Subsection,
    Subsubsection,
    Foot,
    simple_page_number,
    Command,
    Itemize,
    MiniPage,
    Figure,
    SubFigure,
    StandAloneGraphic,
    LargeText,
    MediumText,
    VerticalSpace,
    Tabu,
    FlushLeft,
    Math,
    Enumerate,
    Table,
    Tabularx,
    LongTabu,
    LongTabularx,
    Label,
    MultiColumn,
    Alignat,

)

from pylatex.basic import NewLine, NewPage, LineBreak
from pylatex.utils import rm_temp_dir, bold, italic, fix_filename, NoEscape
from pylatex.utils import bold
from pylatex.package import Package
import os
from datetime import date
import pandas as pd
from PIL import Image

from latex_standard_functions import *
import sympy as sp


# ===================================================================================================#
# Document Settings
def document_setting():
    doc = Document(document_options=['10pt', 'a4paper'])
    # Import of packages
    # Add the sets-pace package
    doc.preamble.append(Package('setspace'))
    doc.preamble.append(Package('placeins'))
    # Set double-spacing
    doc.preamble.append(Command('doublespacing'))
    doc.preamble.append(
        Command('usepackage', options=['left=2cm', 'right=2cm', 'top=3cm', 'bottom=3.0cm'], arguments=['geometry']))
    doc.preamble.append(Command('usepackage', arguments=['amsmath']))
    doc.preamble.append(Command('usepackage', arguments=['amssymb']))
    doc.preamble.append(Command('usepackage', arguments=['graphicx']))
    doc.preamble.append(Command('usepackage', arguments=['fancyhdr']))
    doc.preamble.append(Command('usepackage', arguments=['siunitx']))
    doc.preamble.append(Command('pagestyle', 'fancy'))
    doc.packages.append(Package('rotating'))
    doc.packages.append(Package('longtable'))
    doc.packages.append(Package('booktabs'))
    doc.packages.append(Package('pdflscape'))

    return doc


# ===================================================================================================#
# Title Page Settings
def title_page(doc, kwargs):
    docNumber = kwargs["docNumber"]
    LOGO_PATH = kwargs["LOGO_PATH"]
    designCompany = kwargs["designCompany"]
    projectName = kwargs["projectName"]

    print(projectName)

    projectNumber = kwargs["projectNumber"]
    docTitle = kwargs["docTitle"]
    revision = kwargs["revision"]
    customerCompanyName = kwargs["customerCompanyName"]
    customerContactPerson = kwargs["customerContactPerson"]
    customerContactEmail = kwargs["customerContactEmail"]
    customerContactNumber = kwargs["customerContactNumber"]
    engineer = kwargs["engineer"]
    registration = kwargs["registration"]
    email = kwargs["email"]
    designCompanyPhone = kwargs["designCompanyPhone"]
    designCompanyAddressA = kwargs["designCompanyAddressA"]
    designCompanyAddressB = kwargs["designCompanyAddressB"]
    designCompanyAddressC = kwargs["designCompanyAddressC"]
    designCompanyCountry = kwargs["designCompanyCountry"]
    designCompanyWebsite = kwargs["designCompanyWebsite"]

    doc.append(Command('titlepage'))

    # Add the logo to the title page
    with doc.create(Center()) as centered:
        with doc.create(Figure(position='h')) as logo:
            logo.add_image(LOGO_PATH, width='220px')

        with doc.create(Center()):
            doc.append(Command('Large', projectName))
        doc.append(VerticalSpace('0.4cm'))

        with doc.create(Center()):
            doc.append(Command('large', projectNumber))
        doc.append(VerticalSpace('0.4cm'))

        with doc.create(Center()):
            doc.append(Command('Large', docNumber))
        doc.append(VerticalSpace('0.3cm'))

        line = Command('hrulefill')
        with doc.create(Center()):
            doc.append(line)
        doc.append(VerticalSpace('0.05cm'))

        with doc.create(Center()):
            doc.append(Command('LARGE', docTitle))

        doc.append(VerticalSpace('0.05cm'))

        line = Command('hrulefill')
        with doc.create(Center()):
            doc.append(line)

        with doc.create(Center()):
            doc.append(Command('Large', customerCompanyName))

        doc.append(VerticalSpace('1cm'))

        with doc.create(Tabu('X[r] X[l] X[r] X[l]')) as table:
            # table.add_row(Command('textbf', 'Company Name:'), customerCompanyName, Command('textbf', 'Engineer:'), engineer)
            table.add_row(Command('textbf', 'Contact Person:'), customerContactPerson,
                          Command('textbf', 'Engineer:'), engineer)
            table.add_row(Command('textbf', 'Contact Email:'), customerContactEmail,
                          Command('textbf', 'Reg.:'), registration)
            table.add_row(Command('textbf', 'Contact Number:'), customerContactNumber,
                          Command('textbf', 'Phone:'), designCompanyPhone)
            table.add_row(Command('textbf', 'Date:'), date.today().strftime("%B %d, %Y"),
                          Command('textbf', 'Address:'), designCompanyAddressA)
            table.add_row(Command('textbf', 'Revision:'), revision,
                          NoEscape(r"\makebox[1cm]{}"), designCompanyAddressB)
            table.add_row(NoEscape(r"\makebox[1cm]{}"), NoEscape(r"\makebox[1cm]{}"), NoEscape(r"\makebox[1cm]{}"),
                          designCompanyAddressC)
            table.add_row(NoEscape(r"\makebox[1cm]{}"), NoEscape(r"\makebox[1cm]{}"), Command('textbf', 'Country:'),
                          designCompanyCountry)
            table.add_row(NoEscape(r"\makebox[1cm]{}"), NoEscape(r"\makebox[1cm]{}"), Command('textbf', 'Website:'),
                          designCompanyWebsite)
            table.add_row(NoEscape(r"\makebox[1cm]{}"), NoEscape(r"\makebox[1cm]{}"), Command('textbf', 'Email:'),
                          email)

    return doc


# ===================================================================================================#
# Revision Table
def revision_table(doc, rev_table):
    # rev, description, originator, reviewed, engineer, date_rev

    print("dddddddddddddddddddddddddddddddd")
    print(rev_table)
    with doc.create(Center()) as centered:
        with doc.create(Tabu('| c | c | c | c | c | c |')) as table:
            table.add_hline()
            table.add_row('Rev.', 'Description', 'Originator', 'Reviewed', 'Engineer', 'Date', mapper=[bold])
            table.add_hline()
            for items in rev_table:
                print(items)
                table.add_row(items[0], items[1], items[2], items[3], items[4], items[5])
            table.add_hline()

    return doc


# ===================================================================================================#
# Foot and Header Settings
def foot_header(doc, kwargs):
    docNumber = kwargs["docNumber"]
    LOGO_PATH = kwargs["LOGO_PATH"]
    designCompany = kwargs["designCompany"]
    projectName = kwargs["projectName"]
    projectNumber = kwargs["projectNumber"]
    docTitle = kwargs["docTitle"]
    revision = kwargs["revision"]
    customerCompanyName = kwargs["customerCompanyName"]
    customerContactPerson = kwargs["customerContactPerson"]
    customerContactEmail = kwargs["customerContactEmail"]
    customerContactNumber = kwargs["customerContactNumber"]
    engineer = kwargs["engineer"]
    registration = kwargs["registration"]
    email = kwargs["email"]
    designCompanyPhone = kwargs["designCompanyPhone"]
    designCompanyAddressA = kwargs["designCompanyAddressA"]
    designCompanyAddressB = kwargs["designCompanyAddressB"]
    designCompanyAddressC = kwargs["designCompanyAddressC"]
    designCompanyCountry = kwargs["designCompanyCountry"]
    designCompanyWebsite = kwargs["designCompanyWebsite"]

    # Add document header
    header = PageStyle("header")
    # Create left header
    with header.create(Head("L")):
        header.append(docTitle)
        header.append(LineBreak())
        header.append(NoEscape(r'\rule{\linewidth}{0.4pt}'))
    # # Create center header
    # with header.create(Head("C")):
    #     header.append("Company")
    # Create right header
    with header.create(Head("R")):
        header.append(docNumber)
        header.append(LineBreak())

    # Create left footer
    with header.create(Foot("L")):
        header.append(NoEscape(r'\rule{\linewidth}{0.4pt}'))
        header.append(LineBreak())
        header.append("Revision: " + revision)
    # Create center footer
    # with header.create(Foot("C")):
    #     header.append("Center Footer")
    # Create right footer
    with header.create(Foot("R")):
        header.append(LineBreak())
        header.append(simple_page_number())

    doc.preamble.append(header)
    doc.change_document_style("header")

    return doc


# ===================================================================================================#
# Table of Contents
def table_contents(doc):
    doc.append(NoEscape(r'\newpage'))
    doc.append(NoEscape(r'\tableofcontents'))
    doc.append(NewPage())

    return doc


# ===================================================================================================#
# Sub Section
def subsection(doc, subheading, contents):
    with doc.create(Subsection(subheading)):
        for content in contents:
            if content[0] == "bullet":
                bullet_points(doc, content[1])

            elif content[0] == "table_std":
                table_std(doc, content[1])

            elif content[0] == "df":
                table_df(doc, content[1])

            elif content[0] == "df_list":
                table_df_list(doc, content[1])

            elif content[0] == "calc":
                doc.append(NoEscape(content[1]))

            elif content[0] == "img":
                image = content[1]
                caption = content[2]
                size = content[3]
                images(doc, caption, image, size)

            else:
                doc.append(content[1])

    return doc


# def subsection_landscape(doc, subheading, contents):
#     with doc.create(Subsection(subheading)):
#         for content in contents:
#             table_df_landscape(doc, content[1])



# ===================================================================================================#
# Latex Symbols
def lat_sym(symbol):
    sym = sp.latex(sp.Symbol(symbol))
    return sym


# ===================================================================================================#
# Latex Equation
def eqn(doc, comment, eqns):
    with doc.create(FlushLeft()):
        doc.append(comment)
        doc.append(NoEscape(eqns))


# ===================================================================================================#
# Latex Equation
def eqn2(doc, eqns):
    doc.append(NoEscape(eqns))


# ===================================================================================================#
# Images
def images(doc, caption, image, size):
    with doc.create(Figure(position='h')) as img:
        img.add_image(image, width=size)
        img.add_caption(caption)


# ===================================================================================================#
# Standard Append Table to Document
def table_X_l_l_l(doc, content):
    with doc.create(Tabularx('X l l l')) as table:
        table.add_hline()
        table.add_row('Description', 'Symbol', 'Value', 'Units', mapper=[bold])
        table.add_hline()
        for idx, rw in content.iterrows():
            table.add_row(idx, rw[0], rw[1], rw[2])
    doc.append(NewLine())


# ===================================================================================================#
# Standard Append Table to Document
def table_std(doc, table):
    '''
    First row is the column headers
    Count the number items in the first row to determine bumber of columns
    Rest is the table
    '''
    columns = table[0]
    num_col = len(columns)

    col_setting = 'X'
    for x in range(num_col):
        if x == 0:
            pass
        else:
            col_setting += " l"

    with doc.create(Tabularx(col_setting)) as tab:
        tab.add_hline()
        tab.add_row(columns, mapper=[bold])
        tab.add_hline()
        for row in table[1:]:
            tab.add_row(row)
        tab.add_hline()
    doc.append(NewLine())


# ===================================================================================================#
# Table to dataframe
def table_df(doc, df):
    # Convert the dataframe to a LaTeX table and add it to the section
    cols = df.columns
    no_cols = len(cols)
    tab_col = 'c X'  # Set the desired column format, e.g., 'X' for equal-width columns
    print(tab_col)
    for x in range(1, no_cols):
        tab_col += " l"

    header = ["Item"]
    with doc.create(Tabularx(tab_col)) as table:
        # Add column headers
        for col_name in df.columns:
            header.append(col_name)
        table.add_hline()
        table.add_row(header)
        table.add_hline()

        row_counter = 1
        for _, row in df.iterrows():
            row_cont = [str(row_counter)+"."]
            for col_name, value in row.items():
                if col_name == "Symbol":
                    # Use math mode for "Symbol" column content
                    value_math = value
                    row_cont.append(value_math)
                else:
                    row_cont.append(value)
            row_counter += 1
            table.add_row(row_cont)
        table.add_hline()
    doc.append(NewLine())


# ===================================================================================================#
# Table List to dataframe
def table_df_list(doc, df):
    # Convert the dataframe to a LaTeX table and add it to the section
    cols = df.columns
    no_cols = len(cols)
    if no_cols == 1:
        tab_col = 'X'  # Set the desired column format, e.g., 'X' for equal-width columns
        tab_col = 'c' + ' ' + tab_col

        header = ["Item"]
        with doc.create(Tabularx(tab_col)) as table:
            # Add column headers
            for col_name in df.columns:
                header.append(col_name)
            table.add_hline()
            table.add_row(header)
            table.add_hline()
            row_counter = 1
            for _, row in df.iterrows():
                row_cont = [str(row_counter)+"."]
                for col_name, value in row.items():
                    if col_name == "Symbol":
                        # Use math mode for "Symbol" column content
                        value_math = value
                        row_cont.append(value_math)
                    else:
                        row_cont.append(value)
                row_counter += 1
                table.add_row(row_cont)
            table.add_hline()
        doc.append(NewLine())


# ===================================================================================================#
# Append rows to table
def table_dataframe_append(doc, dataFrame):
    table_rows = []
    for index, row in dataFrame.iterrows():
        description = index
        symbol = row['Variable']
        value = row['Value']
        units = row['Unit']

        # create a row for the table
        table_row = [description, symbol, value, units]

        # add the row to the list of table rows
        table_rows.append(table_row)


# ===================================================================================================#
# Standard Section Function
def section_heading(doc, heading, content):
    doc.append(NoEscape(r'\newpage'))
    with doc.create(Section(heading)):
        doc.append(content)


# ===================================================================================================#
# Standard Sub-Section Function
def sub_section_heading(doc, sub_heading, content):
    with doc.create(Subsection(sub_heading)):
        doc.append(content)


# ===================================================================================================#
# Alphanumeric Itemise Function
def alphanum_bullet_points(doc, content):
    with doc.create(Enumerate(enumeration_symbol=r'(\alph*)')) as enum:
        for item in content:
            enum.add_item(item)


# ===================================================================================================#
# Standard Itemise Function
def bullet_points(doc, content):
    with doc.create(Itemize()) as itemize:
        for item in content:
            itemize.add_item(item)


# ===================================================================================================#
# Standard Itemise Function
def plain_list(doc, content_list):
    for item in content_list:
        doc.append(item)
        doc.append(NewLine())


# ===================================================================================================#
# List to Latex
def list_to_Latex(doc, content_list):
    with doc.create(Tabularx('X l l l')) as table:
        table.add_hline()
        table.add_row('Description', 'Symbol', 'Value', 'Units', mapper=[bold])
        table.add_hline()
        for row in content_list:
            table.add_row(row)


# ===================================================================================================#
# Display Images in Latex
def display_images(doc, image_list):
    for image in image_list:
        file_path = image[2]
        with doc.create(Figure(position='h!')) as img:
            img.add_image(file_path, width="450px")
            img.add_caption(image[1])


def display_images_2(doc, image_list):
    for image in image_list:
        file_path = image[2]
        with doc.create(Figure(position='h!')) as img:
            img.add_image(file_path, width="350px")
            img.add_caption(image[1])


def display_images_3(doc, image_list):
    for image in image_list:
        file_path = image[2]
        with doc.create(Figure(position='h!')) as img:
            img.add_image(file_path, width="450px")
            img.add_caption(image[1])


# ============================================================================== #
# Main Program
def latex_report(doc_number, inputs_kwargs, rev_table, file_path, sections):
    # ----------------------------------------------------------------------------------------------------#
    # Document Settings
    doc = document_setting()

    # ----------------------------------------------------------------------------------------------------#
    # Building the Document
    # Cover Page
    # Title page content
    doc = title_page(doc, inputs_kwargs)
    doc.append(NewPage())

    # ----------------------------------------------------------------------------------------------------#
    # Revision Table
    # ----------------------------------------------------------------------------------------------------#
    doc = revision_table(doc, rev_table)
    doc.append(NewPage())

    # ----------------------------------------------------------------------------------------------------#
    # Table of Contents
    # ----------------------------------------------------------------------------------------------------#
    doc = table_contents(doc)

    # ----------------------------------------------------------------------------------------------------#
    # Define the header and footer
    doc = foot_header(doc, inputs_kwargs)

    # ----------------------------------------------------------------------------------------------------#
    # Section1: General
    section = sections['section_1']
    # section_1 = [heading, heading_sub, content]
    heading_1 = section[0]
    heading_1_1 = section[1]
    content_1_1 = section[2]

    section = sections['section_2']
    # section_1 = [heading, heading_sub, content]

    heading_1_2 = section[1]
    content_1_2 = section[2]

    section = sections['section_3']
    # section_1 = [heading, heading_sub, content]

    heading_1_3 = section[1]
    content_1_3 = section[2]

    with doc.create(Section(heading_1)):
        doc = subsection(doc, heading_1_1, content_1_1)

        doc = subsection(doc, heading_1_2, content_1_2)

        doc = subsection(doc, heading_1_3, content_1_3)

        # doc = subsection(doc, heading_1_4, content_1_4)
        #
        # doc = subsection(doc, heading_1_5, content_1_5)

    doc.append(NewPage())
    # # ----------------------------------------------------------------------------------------------------#
    # Section2: Dimensional Data
    section = sections['section_4']
    heading_2 = section[0]
    heading_2_1 = section[1]
    content_2_1 = section[2]

    section = sections['section_5']
    heading_2_2 = section[1]
    content_2_2 = section[2]

    with doc.create(Section(heading_2)):
        doc = subsection(doc, heading_2_1, content_2_1)

        doc = subsection(doc, heading_2_2, content_2_2)

    doc.append(NewPage())

    # ----------------------------------------------------------------------------------------------------#
    # Section3: Resources
    section = sections['section_6']
    heading_2 = section[0]
    heading_2_1 = section[1]
    content_2_1 = section[2]

    section = sections['section_7']
    heading_2_2 = section[1]
    content_2_2 = section[2]

    with doc.create(Section(heading_2)):
        doc = subsection(doc, heading_2_1, content_2_1)

        doc = subsection(doc, heading_2_2, content_2_2)

    doc.append(NewPage())

    # ----------------------------------------------------------------------------------------------------#
    # Section4: Activities and Deliverables
    section = sections['section_8']
    heading_2 = section[0]
    heading_2_1 = section[1]
    content_2_1 = section[2]

    section = sections['section_9']
    heading_2_2 = section[1]
    content_2_2 = section[2]

    with doc.create(Section(heading_2)):
        doc = subsection(doc, heading_2_1, content_2_1)

        doc = subsection(doc, heading_2_2, content_2_2)

    doc.append(NewPage())

    # ----------------------------------------------------------------------------------------------------#
    # Section5: Decisions and Actions
    # Landscape Table Required

    section = sections['section_10']
    heading_2 = section[0]
    heading_2_1 = section[1]
    content_2_1 = section[2]

    section = sections['section_11']
    heading_2_2 = section[1]
    content_2_2 = section[2]


    # Decision Table
    table_landscape_1 = fr'''
        \begin{{landscape}}%
        \section{{{heading_2}}}%
        \subsection{{{heading_2_1}}} %
    '''
    doc.append(NoEscape(table_landscape_1))

    df = content_2_1[0][1]


    header = ['Item']
    for col_name in df.columns:
        header.append(col_name)
    no_col = len(header)

    table_landscape_2 = fr'''
        \begin{{longtable}}{{ | c | p{{9cm}} | p{{10cm}} | p{{2cm}} |}}
        \hline
        {{{header[0]}}} & {{{header[1]}}} & {{{header[2]}}} & {{{header[3]}}}\\
        \hline
        \endfirsthead
    '''
    doc.append(NoEscape(table_landscape_2))

    table_landscape_3 = fr'''
        \hline
        {{{header[0]}}} & {{{header[1]}}} & {{{header[2]}}} & {{{header[3]}}}\\
        \hline
        \endhead
    '''
    doc.append(NoEscape(table_landscape_3))

    # table_landscape_4 = fr'''
    #     \hline
    #     \multicolumn{{4}}{{| r |}}{{Continued on the next page}}\\
    #     \hline
    #     \endfoot
    #     '''
    # doc.append(NoEscape(table_landscape_4))

    row_counter = 1
    for _, row in df.iterrows():
        row_cont = [str(row_counter) + "."]
        for col_name, value in row.items():
            value.replace('%', r'\%')
            row_cont.append(value)
        row_counter += 1
        table_landscape_5 = fr'''
            {{{row_cont[0]}}} & {{{row_cont[1]}}} & {{{row_cont[2]}}} & {{{row_cont[3]}}} \\
            '''
        doc.append(NoEscape(table_landscape_5))
        doc.append(NoEscape(r'''\hline'''))

    table_landscape_6 = r'''
            \end{longtable}
            \end{landscape}
            '''

    doc.append(NoEscape(table_landscape_6))

    doc.append(NewPage())

    # Action Table
    table_landscape_1 = fr'''
            \begin{{landscape}}%
            \subsection{{{heading_2_2}}} %
        '''
    doc.append(NoEscape(table_landscape_1))



    df = content_2_2[0][1]
    header = ['Item']
    for col_name in df.columns:
        header.append(col_name)
    no_col = len(header)

    table_landscape_2 = fr'''
            \begin{{longtable}}{{ | c | p{{8cm}} | p{{8cm}} | p{{3cm}} | p{{2cm}} |}}
            \hline
            {{{header[0]}}} & {{{header[1]}}} & {{{header[2]}}} & {{{header[3]}}} & {{{header[4]}}}\\
            \hline
            \endfirsthead
        '''
    doc.append(NoEscape(table_landscape_2))

    table_landscape_3 = fr'''
            \hline
            {{{header[0]}}} & {{{header[1]}}} & {{{header[2]}}} & {{{header[3]}}} & {{{header[4]}}}\\
            \hline
            \endhead
        '''
    doc.append(NoEscape(table_landscape_3))

    # table_landscape_4 = fr'''
    #         \hline
    #         \multicolumn{{5}}{{| r |}}{{Continued on the next page}}\\
    #         \hline
    #         \endfoot
    #         '''
    # doc.append(NoEscape(table_landscape_4))

    row_counter = 1
    for _, row in df.iterrows():
        row_cont = [str(row_counter) + "."]
        for col_name, value in row.items():
            value.replace('%', r'\%')
            row_cont.append(value)
        row_counter += 1
        table_landscape_5 = fr'''
                {{{row_cont[0]}}} & {{{row_cont[1]}}} & {{{row_cont[2]}}} & {{{row_cont[3]}}} & {{{row_cont[4]}}}\\
                '''
        doc.append(NoEscape(table_landscape_5))
        doc.append(NoEscape(r'''\hline'''))

    table_landscape_6 = r'''
                \end{longtable}
                \end{landscape}
                '''

    doc.append(NoEscape(table_landscape_6))


    # # ----------------------------------------------------------------------------------------------------#
    # # Section3: Calculations for Bracket Type 1
    # with doc.create(Section(heading_3)):
    #     doc = subsection(doc, heading_3_1, content_3_1)
    #
    #     doc = subsection(doc, heading_3_2, content_3_2)
    #
    #     eqn(doc, comment_3_3_1, L_1_eqn)
    #     eqn(doc, comment_3_3_2, e_eqn)
    #
    #     eqn(doc, comment_3_4_1, f_egn)
    #     eqn(doc, comment_3_4_2, a_egn)
    #     eqn(doc, comment_3_4_3, p_egn)
    #
    #     doc = subsection(doc, heading_3_3, content_3_3)
    #
    #     eqn(doc, comment_3_5_1, sigma_eqn)
    #     eqn(doc, comment_3_5_2, delta_eqn)
    #     eqn(doc, comment_3_5_3, sigma_allow_eqn)
    #     eqn2(doc, sf_eqn)
    #
    #     doc = subsection(doc, heading_3_4, content_3_4)
    #
    #     eqn(doc, comment_3_6_1, sigmac_allow_eqn)
    #     eqn(doc, comment_3_6_2, sigmac_actual_eqn)
    #     eqn2(doc, sfg_eqn)
    #
    #     doc = subsection(doc, heading_3_7, content_3_7)
    #
    #     eqn(doc, comment_3_8_1, bolt_area_eqn)
    #     eqn(doc, comment_3_8_2, tr_eqn)
    #     eqn(doc, comment_3_8_3, vr_eqn)
    #     eqn(doc, comment_3_8_4, m_eqn)
    #     eqn(doc, comment_3_8_5, t1_eqn)
    #     eqn(doc, comment_3_8_6, t2_eqn)
    #     eqn(doc, comment_3_8_7, v_eqn)
    #     eqn(doc, comment_3_8_8, ic_eqn)
    #     eqn2(doc, sfic_eqn)
    #
    #     doc = subsection(doc, heading_3_9, content_3_9)
    #
    # doc.append(NewPage())
    #
    # # ----------------------------------------------------------------------------------------------------#
    # # Section4: Calculations for Bracket Type 2
    # with doc.create(Section(heading_4)):
    #     doc = subsection(doc, heading_4_1, content_4_1)
    #
    #     doc = subsection(doc, heading_4_2, content_4_2)
    #
    #     eqn(doc, comment_4_3_1, L_1_eqn_2)
    #     eqn(doc, comment_4_3_2, e_eqn_2)
    #
    #     eqn(doc, comment_4_4_1, f_egn_2)
    #     eqn(doc, comment_4_4_2, a_egn_2)
    #     eqn(doc, comment_4_4_3, p_egn_2)
    #
    #     doc = subsection(doc, heading_4_3, content_4_3)
    #
    #     eqn(doc, comment_4_5_1, sigma_eqn_2)
    #     eqn(doc, comment_4_5_2, delta_eqn_2)
    #     eqn(doc, comment_4_5_3, sigma_allow_eqn_2)
    #     eqn2(doc, sf_eqn_2)
    #
    #     doc = subsection(doc, heading_4_4, content_4_4)
    #
    #     eqn(doc, comment_4_6_1, sigmac_allow_eqn_2)
    #     eqn(doc, comment_4_6_2, sigmac_actual_eqn_2)
    #     eqn2(doc, sfg_eqn_2)
    #
    #     doc = subsection(doc, heading_4_7, content_4_7)
    #
    #     eqn(doc, comment_4_8_1, bolt_area_eqn_2)
    #     eqn(doc, comment_4_8_2, tr_eqn_2)
    #     eqn(doc, comment_4_8_3, vr_eqn_2)
    #     eqn(doc, comment_4_8_4, m_eqn_2)
    #     eqn(doc, comment_4_8_5, t1_eqn_2)
    #     eqn(doc, comment_4_8_6, t2_eqn_2)
    #     eqn(doc, comment_4_8_7, v_eqn_2)
    #     eqn(doc, comment_4_8_8, ic_eqn_2)
    #     eqn2(doc, sfic_eqn_2)
    #
    #     doc = subsection(doc, heading_4_9, content_4_9)
    #
    #     doc.append(special_note)
    #
    # doc.append(NewPage())
    #
    # # ----------------------------------------------------------------------------------------------------#
    # # Section5: Calculations for Bracket Type 3
    # with doc.create(Section(heading_5)):
    #     doc = subsection(doc, heading_5_1, content_5_1)
    #
    #     doc = subsection(doc, heading_5_2, content_5_2)
    #
    #     eqn(doc, comment_5_3_1, L_1_eqn_3)
    #     eqn(doc, comment_5_3_2, e_eqn_3)
    #
    #     eqn(doc, comment_5_4_1, f_egn_3)
    #     eqn(doc, comment_5_4_2, a_egn_3)
    #     eqn(doc, comment_5_4_3, p_egn_3)
    #
    #     doc = subsection(doc, heading_5_3, content_5_3)
    #
    #     eqn(doc, comment_5_5_1, sigma_eqn_3)
    #     eqn(doc, comment_5_5_2, delta_eqn_3)
    #     eqn(doc, comment_5_5_3, sigma_allow_eqn_3)
    #     eqn2(doc, sf_eqn_3)
    #
    #     doc = subsection(doc, heading_5_4, content_5_4)
    #
    #     eqn(doc, comment_5_6_1, sigmac_allow_eqn_3)
    #     eqn(doc, comment_5_6_2, sigmac_actual_eqn_3)
    #     eqn2(doc, sfg_eqn_3)
    #
    #     doc = subsection(doc, heading_5_7, content_5_7)
    #
    #     eqn(doc, comment_5_8_1, bolt_area_eqn_3)
    #     eqn(doc, comment_5_8_2, tr_eqn_3)
    #     eqn(doc, comment_5_8_3, vr_eqn_3)
    #     eqn(doc, comment_5_8_4, m_eqn_3)
    #     eqn(doc, comment_5_8_5, t1_eqn_3)
    #     eqn(doc, comment_5_8_6, t2_eqn_3)
    #     eqn(doc, comment_5_8_7, v_eqn_3)
    #     eqn(doc, comment_5_8_8, ic_eqn_3)
    #     eqn2(doc, sfic_eqn_3)
    #
    #     doc = subsection(doc, heading_5_9, content_5_9)
    #
    #     doc.append(special_note)
    #
    # doc.append(NewPage())
    # # ----------------------------------------------------------------------------------------------------#
    # # Section6: Splitter Chute
    # with doc.create(Section(heading_6)):
    #     doc = subsection(doc, heading_6_1, content_6_1)
    #
    #     doc = subsection(doc, heading_6_2, content_6_2)
    #
    #     doc.append(special_note_2)
    #     doc.append(NewLine())
    #
    # doc.append(NewPage())
    # # ----------------------------------------------------------------------------------------------------#
    # # Section7: Impact Loading back of Splitter
    # with doc.create(Section(heading_7)):
    #     doc = subsection(doc, heading_7_1, content_7_1)
    #
    #     doc = subsection(doc, heading_7_2, content_7_2)
    #
    #     eqn(doc, comment_7_1_1, P_beam_eqn)
    #
    #     eqn(doc, comment_8_1_1, sigma_bend_eqn)
    #
    #     eqn(doc, comment_7_1_2, P_plate_eqn)
    #
    #     eqn(doc, comment_8_1_2, sigma_plate_eqn)
    #
    #     doc.append(special_note_3)
    #
    # doc.append(NewPage())
    #
    # # ----------------------------------------------------------------------------------------------------#
    # # Section8: Measuring Flas
    # with doc.create(Section(heading_8)):
    #     doc = subsection(doc, heading_8_1, content_8_1)
    #
    #     doc = subsection(doc, heading_8_2, content_8_2)
    #
    #
    # # ----------------------------------------------------------------------------------------------------#
    # # Section9: Measuring Flas
    # with doc.create(Section(heading_9)):
    #     doc = subsection(doc, heading_9_1, content_9_1)
    #
    #     doc = subsection(doc, heading_9_2, content_9_2)
    #
    #     eqn(doc, comment_9_1_1, P_stiff_eqn)
    #
    #     eqn(doc, comment_10_1_1, sigma_bend_stiffener_eqn)
    #
    #     eqn(doc, comment_9_1_2, P_plate2_eqn)
    #
    #     eqn(doc, comment_10_1_2, sigma2_plate_eqn)
    #
    #     doc.append(special_note_3)
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    # doc.append(NewPage())
    # # ----------------------------------------------------------------------------------------------------#
    # # Appendix: Appendix
    # with doc.create(Section(heading_A)):
    #     doc = subsection(doc, heading_3_10, content_5_10)
    #
    #
    #
    #

    # Generate the calculation document

    calc_path = os.path.join(file_path, doc_number)
    try:
        doc.generate_pdf(calc_path, clean_tex=False)

    except:
        print("---")
        print(calc_path)
        print("Latex generation problem")
        print("Download the file and open Manual in MikTex")

# if __name__ == '__main__':
#     print("jjjjjjjjjjjjjjjjjjjj")
#     main()
