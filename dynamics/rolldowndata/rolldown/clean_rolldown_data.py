# files to be cleaned should be put into
# /dynamics/rolldowndata/rolldown/unprocessed
import pandas as pd
from os import listdir, rename
from os.path import isfile, join

# set folder paths
unprocessed_path = 'unprocessed'
processed_path = 'processed'
raw_path = 'raw'
clean_path = 'clean'

# make list of unprocessed files
only_files = [f for f in listdir(unprocessed_path) if isfile(join(unprocessed_path, f))]

# create file paths
file_paths = []
for f in only_files:
    f = join('.', unprocessed_path, f)
    file_paths.append(f)

# clean and transform each file in file_paths list
for i, f in enumerate(file_paths):
    rolldown = pd.read_csv(f)

    # make a new boolean column, needed to clean data later
    rolldown['throttle and brake == 0 or na'] = ((rolldown['throttle'] == 0) & \
                                            (rolldown['mechanical_brake_state'] == 0)) | \
                                            ((rolldown['throttle'].isna()) & \
                                             (rolldown['mechanical_brake_state'].isna()))

    # resort index to ensure data is in correct order
    # then reset the index, finally, make the index a column
    # making the index a column makes it easier to find the subset we need
    rolldown.reset_index(drop = True, inplace = True)
    rolldown.reset_index(inplace = True)
    rolldown.rename(columns={'index' : 'row_no'}, inplace = True)

    # remove unnecessary columns
    # include throttle and brake state for now
    col_snip = ['row_no', 'throttle', 'mechanical_brake_state', 'Time Offset [ms]', 'vehicle_velocity_left', \
                    'vehicle_velocity_right', 'throttle and brake == 0 or na']
    rolldown = rolldown[col_snip]

    # make new dataframe to find subset of rows
    # that contain the required data
    find_subset = pd.concat([rolldown['throttle and brake == 0 or na'], rolldown['row_no']], axis = 1)

    # cumsum on boolean column to find multiple
    # subsets of rows fitting our requirements
    find_subset_bool = find_subset['throttle and brake == 0 or na'] != find_subset['throttle and brake == 0 or na'].shift()
    find_subset_cumsum = find_subset_bool.cumsum()
    subset_groups = find_subset.groupby(find_subset_cumsum)
    group_counts = subset_groups.agg({'row_no':['count', 'min', 'max']})

    # drop unnecessary column levels
    group_counts.columns = group_counts.columns.droplevel()
    group_counts = group_counts.merge(find_subset, how='left', left_on = ['min'], right_on = ['row_no'])
    group_counts = group_counts[group_counts['throttle and brake == 0 or na'] == True]

    # take the largest single subset
    max_count = group_counts[group_counts['count'] == group_counts['count'].max()]
    minimum = max_count['min'].iloc[0]
    maximum = max_count['max'].iloc[0]

    # slice original dataframe with found subset indices
    rolldown = rolldown.loc[minimum:maximum + 1]

    # remove throttle, row_no, and brake state
    col_snip = ['Time Offset [ms]', 'vehicle_velocity_left', \
                    'vehicle_velocity_right']
    rolldown = rolldown[col_snip]

    # drop rows where velocity columns are na
    rolldown = rolldown.loc[(rolldown['vehicle_velocity_left'].notna()) \
                            & (rolldown['vehicle_velocity_right'].notna())]

    # calculate avg velocity
    rolldown['average_velocity'] = (rolldown['vehicle_velocity_left'] \
                                    + rolldown['vehicle_velocity_right']) / 2

    # finally, write df to clean folder
    cleaned_file = str('clean_' + only_files[i])
    cleaned_file = join('.', processed_path, clean_path, cleaned_file)
    rolldown.to_csv(cleaned_file, index = False)

    # rename and move unprocessed file to processed/raw folder
    raw_file = str('raw_' + only_files[i])
    raw_file = join('.', processed_path, raw_path, raw_file)
    rename(f, raw_file)