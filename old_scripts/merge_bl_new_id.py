import sys
import pandas as pd
import numpy as np


'''
1. assume all bl available and all parseclan created
2. open file containing all old bl
3. open file containing all new csv
4. zip both (check right order//same length etc)
5. merge:
    a. on id if possible
    b. on word-onset-offset-spkr if possible
    c. print error otherwise and manual check...
6. output in WHERE
'''


if __name__=="__main__":

    # open file with old bl paths
    list_old_bl_paths = sys.argv[1]
    list_old_bl = open(list_old_bl_paths).readlines()
    list_old_bl = [l.strip() for l in list_old_bl]

    # open file with new csv paths
    list_new_csv_paths = sys.argv[2]
    list_new_csv = open(list_new_csv_paths).readlines()
    list_new_csv = [l.strip() for l in list_new_csv]

    error_file = sys.argv[3]
    errors = []

    for audio in zip(list_old_bl, list_new_csv):
        print(audio)
        old_bl_path = audio[0]
        new_csv_path = audio[1]

        old_bl = pd.read_csv(old_bl_path, keep_default_na=False)
        new_csv = pd.read_csv(new_csv_path, keep_default_na=False)

        # for those with unchanged annotid
        merged = new_csv.merge(old_bl[['annotid', 'basic_level']], on='annotid', how='inner')
        merged = merged.rename(columns={'basic_level_y':'basic_level'})
        merged = merged.drop("basic_level_x", 1)
        merged = merged.replace(r'\s+', "NA", regex=True)
        # merged.to_csv(old_bl_path.replace(".csv", "_temp.csv"))
        s = list(merged['annotid'])
        #print(s)
        # for those without an annotid match
        for i,r in new_csv.iterrows():
            # if already processed, pass
            if r['annotid'] in s:
                pass
            else:
                # print(r)
                tmp = old_bl[old_bl['word']==r['word']]
                # if only one bl for that word, write that bl

                if len(tmp.basic_level.unique())==1:
                    # print("done")
                    new_row = r
                    new_row['basic_level'] = tmp['basic_level'].iloc[0]
                    merged = merged.append(new_row)
                else:
                    tmp = tmp[tmp['timestamp']==r['timestamp']]
                    # print(tmp)
                    if len(tmp.basic_level.unique())==1:
                        # print(tmp.basic_level.unique())
                        # print("done2")
                        new_row = r
                        new_row['basic_level'] = tmp['basic_level'].iloc[0]
                        merged = merged.append(new_row)
                    else:
                        print("Could not find match") # for")
                        print(r["annotid"])
                        errors.append([new_csv, str(new_row['annotid'])])
                        # print(r)
        # if len(merged) != len(old_bl):
        #     print("Length error")
        #     errors.append([new_csv, "length"])
        # write output
        merged.to_csv(old_bl_path.replace(".csv", "_new.csv"))

    with open(error_file, 'w') as fo:
        for l in errors:
            fo.write(l)
