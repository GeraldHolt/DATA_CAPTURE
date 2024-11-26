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

import sympy as sp

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
# Dataframe to Latex
# def table_df(doc, df):
#     # Convert the dataframe to a LaTeX table and add it to the section
#     cols = df.columns
#     no_cols = len(cols)
#     tab_col = 'X'  # Set the desired column format, e.g., 'X' for equal-width columns

#     for x in range(1, no_cols):
#         tab_col += " c"

#     header = []
#     with doc.create(Tabularx(tab_col)) as table:
#         # Add column headers
#         for col_name in df.columns:
#             header.append(col_name)
#         table.add_hline()
#         table.add_row(header)
#         table.add_hline()

#         for _, row in df.iterrows():
#             row_cont = []
#             for _, value in row.items():
#                 row_cont.append(value)
#             table.add_row(row_cont)
#         table.add_hline()

def table_df(doc, df):
    # Convert the dataframe to a LaTeX table and add it to the section
    cols = df.columns
    no_cols = len(cols)
    tab_col = 'X'  # Set the desired column format, e.g., 'X' for equal-width columns

    for x in range(1, no_cols):
        tab_col += " c"

    header = []
    with doc.create(Tabularx(tab_col)) as table:
        # Add column headers
        for col_name in df.columns:
            header.append(col_name)
        table.add_hline()
        table.add_row(header)
        table.add_hline()

        for _, row in df.iterrows():
            row_cont = []
            for col_name, value in row.items():
                if col_name == "Symbol":
                    # Use math mode for "Symbol" column content
                    value_math = value
                    row_cont.append(value_math)
                else:
                    row_cont.append(value)
            table.add_row(row_cont)
        table.add_hline()
    doc.append(NewLine())





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


# Standard Section Function
def section_heading(doc, heading, content):
    doc.append(NoEscape(r'\newpage'))
    with doc.create(Section(heading)):
        doc.append(content)


# Standard Sub-Section Function
def sub_section_heading(doc, sub_heading, content):
    with doc.create(Subsection(sub_heading)):
        doc.append(content)


# Alphanumeric Itemise Function
def alphanum_bullet_points(doc, content):
    with doc.create(Enumerate(enumeration_symbol=r'(\alph*)')) as enum:
        for item in content:
            enum.add_item(item)


# Standard Itemise Function
def bullet_points(doc, content):
    with doc.create(Itemize()) as itemize:
        for item in content:
            itemize.add_item(item)


# Standard Itemise Function
def plain_list(doc, content_list):
    for item in content_list:
        doc.append(item)
        doc.append(NewLine())


# List to Latex
def list_to_Latex(doc, content_list):
    with doc.create(Tabularx('X l l l')) as table:
        table.add_hline()
        table.add_row('Description', 'Symbol', 'Value', 'Units', mapper=[bold])
        table.add_hline()
        for row in content_list:
            table.add_row(row)





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
