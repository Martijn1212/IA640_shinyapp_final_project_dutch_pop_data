import pandas as pd
from plotnine import ggplot, aes, theme_minimal, geom_point, geom_line, geom_col, ggtitle, ylim

def load_data(x):                                                           #loading the CSV files in to python for all the years
    data = f"DATA/CBS_{x}.csv"
    df = pd.read_csv(data)
    df.replace(-99997, 0, inplace=True)                               #replacing the wrong value in the data with 0 to minimize error
    return df

def compare_data(option, x, code):                                          #the main comparison function that looks at the choise and starts the right function for it
    list_of_data = {}

    for data in x:
        df = load_data(data)

        code = int(code)
        if code >= 1000 and code < 10000:                                   #Checling for postal code, and checking if its a valid value
            df["Postcode-4"] = df["Postcode-4"].astype(str)
            code = str(code)
            df = df[df["Postcode-4"] == code]
            list_of_data[data] = df

        else:
            list_of_data[data] = df

    if option == "Man and Woman":                                           #chosing the grapfhs for the choises
        man_woman(list_of_data, x)
        return man_woman(list_of_data, x)

    if option == "Urban vs Rural":
        City_or_not(list_of_data, x)
        return City_or_not(list_of_data, x)


    if option == "Age":
        Age_disply(list_of_data, x)
        return Age_disply(list_of_data, x)

    if option == "Migration background":
        migration(list_of_data, x)
        return migration(list_of_data, x)

    if option == "Building Age":
        building_age(list_of_data, x)
        return building_age(list_of_data, x)

    if option == "Rent vs Owned":
        rent_or_not(list_of_data, x)
        return rent_or_not(list_of_data, x)
    return f""

                                                                            #Data manipulation
def man_woman(list_of_data, data):
    rows = []

    for year in data:
        df = list_of_data[year]


        Man_count = df["Man"].sum()                                         #counting the data
        Woman_count = df["Vrouw"].sum()

                                                                            #adding it to a data frame
        rows.append({"Year": int(year), "Group": "Man", "Count": int(Man_count)})
        rows.append({"Year": int(year), "Group": "Woman", "Count": int(Woman_count)})

                                                                            #starting the plot
    plot_df = pd.DataFrame(rows)
                                                                            #changeing the data to percentiges
    plot_df["Percent"] = plot_df.groupby("Year")["Count"].transform(lambda x: x / x.sum() * 100)

                                                                            # Line plot
    m_v = (
            ggplot(plot_df, aes(x="Year", y="Percent", color="Group"))
            + geom_line(size=1.5)
            + geom_point(size=3)
            + theme_minimal()
            + ggtitle("Amount of men compared to women in the region")
            + ylim(45, max(plot_df["Percent"]) * 1.1)                #adding space above and below the data
    )
    return m_v

def City_or_not(list_of_data, data):
    rows = []

    for year in data:
        df = list_of_data[year]

        df["Urban"] = df["city"] >= 3

        urban_count = df["Urban"].sum()
        rural_count = len(df) - urban_count

        rows.append({"Year": int(year), "Group": "Urban", "Count": int(urban_count)})
        rows.append({"Year": int(year), "Group": "Rural", "Count": int(rural_count)})

    plot_df = pd.DataFrame(rows)
    plot_df["Percent"] = plot_df.groupby("Year")["Count"].transform(lambda x: x / x.sum() * 100)

    p = (
            ggplot(plot_df, aes(x="Year", y="Percent", color="Group"))
            + geom_line(size=1.5)
            + geom_point(size=3)
            + theme_minimal()
            + ggtitle("Amount of people living in the city and rural area")
            + ylim(min(plot_df["Percent"]) * 0.9, max(plot_df["Percent"]) * 1.1)
    )
    return p

def Age_disply(list_of_data, data):
    rows = []

    for year in data:
        df = list_of_data[year]
                                                                            # asablishing an order
        age_group_order = ["Under 15", "15 to 25", "25 to 45", "45 to 65", "65 years and over"]

        u15_count = df["tot 15 jaar"].sum()
        a15_25_count = df["15 tot 25 jaar"].sum()
        a25_45_count = df["25 tot 45 jaar"].sum()
        a45_65_count = df["45 tot 65 jaar"].sum()
        o65_count = df["65 jaar en ouder"].sum()

        rows.append({"Year": int(year), "Group": "Under 15", "Count": int(u15_count)})
        rows.append({"Year": int(year), "Group": "15 to 25", "Count": int(a15_25_count)})
        rows.append({"Year": int(year), "Group": "25 to 45", "Count": int(a25_45_count)})
        rows.append({"Year": int(year), "Group": "45 to 65", "Count": int(a45_65_count)})
        rows.append({"Year": int(year), "Group": "65 years and over", "Count": int(o65_count)})

    plot_df = pd.DataFrame(rows)
                                                                            #Making an order to the data so the legent isn't bad
    plot_df["Group"] = pd.Categorical(plot_df["Group"], categories=age_group_order, ordered=True)
    plot_df["Percent"] = plot_df.groupby("Year")["Count"].transform(lambda x: x / x.sum() * 100)


    m_v = (
            ggplot(plot_df, aes(x="Year", y="Percent", color="Group"))
            + geom_line(size=1.5)
            + geom_point(size=3)
            + theme_minimal()
            + ggtitle("Distribution over age groups in the region")
            + ylim(min(plot_df["Percent"]) * 0.9, max(plot_df["Percent"]) * 1.1)
    )
    return m_v

def migration(list_of_data, data):
    rows = []

    for year in data:
        df = list_of_data[year]
        year = int(year)

        if year >= 2022:
            dutch = df["Geboren in Nederland met een Nederlandse herkomst"].sum()
            eurodutch = df["Geboren in Nederland met een Europese herkomst (excl. Nederland)"].sum()
            noneurodutch = df["Geboren in Nederland met herkomst buiten Europa"].sum()
            total_dutch = dutch + eurodutch + noneurodutch
            euronew = df["Geboren buiten Nederland met een Europese herkomst (excl. Nederland)"].sum()
            noneuronew = df["Geboren buiten Nederland met een herkomst buiten Europa"].sum()
            total_new = euronew + noneuronew

            rows.append({"Year": int(year), "Group": "in The Netherlands", "Count": int(total_dutch)})
            rows.append({"Year": int(year), "Group": "outside The Netherlands (Europe)", "Count": int(euronew)})
            rows.append({"Year": int(year), "Group": "outside The Netherlands (non-Europe)", "Count": int(noneuronew)})
            rows.append({"Year": int(year), "Group": "outside The Netherlands", "Count": int(total_new)})
        else:
            total_dutch = df["Nederlandse achtergond"].sum()
            euronew = df["Westerse migratie achtergrond"].sum()
            noneuronew = df["Niet-westerse migratie achtergrond"].sum()
            total_new = euronew + noneuronew



            rows.append({"Year": int(year), "Group": "in The Netherlands", "Count": int(total_dutch)})
            rows.append({"Year": int(year), "Group": "outside The Netherlands (Europe)", "Count": int(euronew)})
            rows.append({"Year": int(year), "Group": "outside The Netherlands (non-Europe)", "Count": int(noneuronew)})
            rows.append({"Year": int(year), "Group": "outside The Netherlands", "Count": int(total_new)})

    plot_df = pd.DataFrame(rows)
    plot_df["Percent"] = plot_df.groupby("Year")["Count"].transform(lambda x: x / x.sum() * 100)

    m_v = (
            ggplot(plot_df, aes(x="Year", y="Percent", color="Group"))
            + geom_line(size=1.5)
            + geom_point(size=3)
            + theme_minimal()
            + ggtitle("Immigration numbers in the region (\"People born\")")
            + ylim(min(plot_df["Percent"]) * 0.9, max(plot_df["Percent"]) * 1.1)
    )
    return m_v

def building_age(list_of_data, data):
    year = data[-1]                                                          # Use first selected year only (data is not nesesery over many years

    df = list_of_data[year]

    age_columns = [                                                         #asablishing an order
        ("voor 1945", "Before 1945"),
        ("1945 tot 1965", "1945–1965"),
        ("1965 tot 1975", "1965–1975"),
        ("1975 tot 1985", "1975–1985"),
        ("1985 tot 1995", "1985–1995"),
        ("1995 tot 2005", "1995–2005"),
        ("2005 tot 2015", "2005–2015"),
        ("2015 en later", "2015 and later")
    ]

    rows = []

    for col_name, label in age_columns:
        count = df[col_name].sum()
        rows.append({"Group": label, "Count": int(count)})

    plot_df = pd.DataFrame(rows)

    total = plot_df["Count"].sum()
    plot_df["Percent"] = plot_df["Count"] / total * 100
                                                                            # Making an order to the data so the order isn't random isn't bad
    plot_df["Group"] = pd.Categorical(plot_df["Group"],
                                      categories=[label for _, label in age_columns],
                                      ordered=True)

    ba = (
        ggplot(plot_df, aes(x="Group", y="Percent"))
        + geom_col()                                                        #maiing bar chart
        + theme_minimal()
        + ggtitle(f"The age of the building in the region (in: {year})")
    )

    return ba

def rent_or_not(list_of_data, data):
    rows = []

    for year in data:
        df = list_of_data[year]

        Homeowner = df["Koopwoning"].sum()
        renter = df["Huurwoning"].sum()
        Renterscoorperation = df["Huurcoporatie"].sum()

        rows.append({"Year": int(year), "Group": "Home owner", "Count": int(Homeowner)})
        rows.append({"Year": int(year), "Group": "Rented", "Count": int(renter)})
        rows.append({"Year": int(year), "Group": "Renters coorperation", "Count": int(Renterscoorperation)})

    plot_df = pd.DataFrame(rows)

    plot_df["Percent"] = plot_df.groupby("Year")["Count"].transform(lambda x: x / x.sum() * 100)

    m_v = (
            ggplot(plot_df, aes(x="Year", y="Percent", color="Group"))
            + geom_line(size=1.5)
            + geom_point(size=3)
            + theme_minimal()
            + ggtitle("Houses that are rented, bought or from a \"renting corporation\"")
            + ylim(min(plot_df["Percent"]) * 0.9, max(plot_df["Percent"]) * 1.1)
    )
    return m_v





