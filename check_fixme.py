import os
import sys
import pandas as pd

if __name__ == "__main__":

    home_visit_paths = sys.argv[1]

    error_code = "***FIXME***"
    no_bl = "***FIX ME***"
    annotid_fixme = []
    word_fixme = []
    basic_level_fixme = []
    other_fixme = []

    with open(home_visit_paths, 'r') as f:
        lines = f.readlines()

    for line in lines:
        print(line)
        line = line.strip()
        # if mode == 'audio':
        old_path = line+"/Analysis/Audio_Analysis/"
        cols = ["tier", "word", "utterance_type", "object_present", \
            "speaker", "annotid", "timestamp", "basic_level"]

        # TODO video later maybe -- less important
        # elif mode == 'video':
        #     old_path = line+"/Analysis/Video_Analysis/"
        #     cols = ["tier", "word", "utterance_type", "object_presence", \
        #         "speaker", "annotid", "timestamp", "basic_level"]

        for csv_file in os.listdir(old_path):
            if csv_file.endswith("sparse_code.csv"):
                # try:
                    # read csv file
                csv_df = pd.read_csv(os.path.join(old_path, csv_file), usecols = cols)
                    # remove column in which fixme are supposed to be
                    # csv_df = csv_df[cols[:-1]]
                # except ValueError:
                #     print(csv_file)
                for column in csv_df:
                    # print(column)
                    if error_code in csv_df[column].values or no_bl in csv_df[column].values:
                        #print(column)
                        if column == "annotid":
                            annotid_fixme.append(line)
                        elif column == "word":
                            word_fixme.append(line)
                        elif column == "basic_level":
                            basic_level_fixme.append(line)
                        else:
                            other_fixme.append(line)

    with open("fixme_errors.txt", "w+") as f:
        f.write("basic_level\n")
        for l in basic_level_fixme:
            f.write(l+"\n")
        f.write("annotid\n")
        for l in annotid_fixme:
            f.write(l+"\n")
        f.write("word\n")
        for l in word_fixme:
            f.write(l+"\n")
        f.write("other\n")
        for l in other_fixme:
            f.write(l+"\n")
