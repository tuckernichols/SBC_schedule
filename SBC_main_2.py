import SBC_Functions


def searchDay(day, lunch : bool, filename):
    data = SBC_Functions.pdf_to_pandas(f"saveFolder/{filename}")
    col = SBC_Functions.data_col(day, lunch)

    collected_data = SBC_Functions.collect_data(data, col)
    sorted_data = SBC_Functions.sort_data(collected_data)
    print(collected_data)
    print(sorted_data)
    return sorted_data


# searchDay("wednesday", lunch=True)


def search_name(name, filename):
    shifts = []
    data = SBC_Functions.pdf_to_pandas(f"saveFolder/{filename}")
    for col in range(1, 15):
        collected_data = SBC_Functions.collect_data(data, col)
        # print(collected_data)
        for namedata in collected_data:
            if namedata[0] == name:
                shifts.append([SBC_Functions.reverse_mappings(col), namedata[1]])
    print(shifts)
    return shifts


def upload_Newest():
    SBC_Functions.save_schedule_PDF()


search_name("Jonny", "7.22.24-8.4.24 Schedule.pdf")


# PLANING
# how do i make this accessible to everyone working there
#
#
# front end?

#   website though flask
# pros:
# full control
# demonstrates knowage of flack and JS
# cons:
# need responsive design
# brush up on many skills
#
#

