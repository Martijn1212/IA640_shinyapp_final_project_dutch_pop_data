from shiny import App, ui, render
import main

app_ui = ui.page_fluid(
                                                                        #Years checkbox
    ui.input_checkbox_group(
        "data_years",
        "Compare data from years:",
        choices=["2018", "2019", "2020", "2021", "2022", "2023"],       #options in the checkboxes
        selected=[],
        inline=True                                                     #Transpose it to horizontal 
        
    ),
                                                                        #options chack boxes
    ui.input_checkbox_group(
        "data_choice",
        "Select data to compare:",
        choices=[
            "Man and Woman", "Urban vs Rural", "Age", "Migration background",
            "Building Age", "Rent vs Owned"
        ],
        selected=[],
        inline=True
    ),
                                                                        #numeric input for the postal code
    ui.input_numeric(
        "code",
        "Enter first digits of your postal code (1000–9999):",
        value=0000,                                                     #initial value that is out of range on purpus to make egnoring it eazyer
        min=1000,                                                       #min value that exists
        max=9999,                                                       #max value posible
        step=1                                                          #only whole numbers
    ),
    ui.output_ui("general_info"),                                       #output for the table with the total population data
    ui.output_ui("plots_container"),                                    #iutput for the plots

                                                                        #making a grid for the outputs of the graphs
    ui.tags.style("""
    .plot-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr); /* 2 columns */
        gap: 20px;
        margin-top: 20px;
    }
    """)
)


def server(input, output, session):
    @output
    @render.text
    def general_info():                                                 #generating table output
        years = input.data_years()                                      #making the input data avaleble
        code = input.code()

        if not years:                                                   #checking if a year has been selected
            return ui.p("Select at least one year.")

        year_cells = []                                                 #opening the lists nesesery for the table
        pop_cells = []

        for year in years:                                              #iterating trough the years to get the full range
            df = main.load_data(year)

                                                                        # Filter by postal code if valid
            code_int = int(code)
            if 1000 <= code_int <= 9999:                                #checking if a postal code has been added
                df["Postcode-4"] = df["Postcode-4"].astype(str)
                df = df[df["Postcode-4"] == str(code_int)]              #taking only the data from the specific line


            population = df["Totaal"].sum()                             # Compute total population
            population= f"{population:,}"                               #adding the "," to the number for eazy reading


            year_cells.append(ui.tags.td(str(year)))                    #adding the year to the table list
            pop_cells.append(ui.tags.td(str(population)))

        return  ui.tags.table(                                          #rendering and adding the data to the table
        ui.tags.tbody(
            ui.tags.tr(
                ui.tags.th("Year"),
                *year_cells
            ),
            ui.tags.tr(
                ui.tags.th("Population"),
                *pop_cells
            )
        ),
        class_="table table-striped table-bordered"
    )

    @output
    @render.ui
    def plots_container():                                              #making a plot for every option chosen
        choices = input.data_choice()
        return ui.div(
            *[
                ui.output_plot(f"plot_{choice.replace(' ', '_')}")
                for choice in choices
            ],
            class_ = "plot-grid"
        )

    def make_plot_renderer(choice):                                     #rendering the plot for every plot chosen
        @output(id=f"plot_{choice.replace(' ', '_')}")
        @render.plot
        def _():
            years = input.data_years()
            code = input.code()
            return main.compare_data(choice, years, code)

    for choice in ["Man and Woman", "Urban vs Rural", "Age",
                   "Migration background", "Building Age", "Rent vs Owned"]:
        make_plot_renderer(choice)                                      #iterating trough the plots of the data


app = App(app_ui, server)                                               # initiating the full app
