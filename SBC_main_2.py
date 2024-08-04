import SBC_Functions


def search_day(day, lunch: bool, filename):
    data = SBC_Functions.pdf_to_pandas(f"saveFolder/{filename}")
    col = SBC_Functions.data_col(day, lunch)

    collected_data = SBC_Functions.collect_data(data, col)
    sorted_data = SBC_Functions.sort_data(collected_data)
    return sorted_data


def search_name(name, filename):
    shifts = []
    data = SBC_Functions.pdf_to_pandas(f"saveFolder/{filename}")
    for col in range(1, 15):
        collected_data = SBC_Functions.collect_data(data, col)
        for namedata in collected_data:
            if namedata[0] == name:
                shifts.append([SBC_Functions.reverse_mappings(col), namedata[1]])
    print(shifts)
    return shifts


def upload_newest_schedule():
    SBC_Functions.save_schedule_PDF()

