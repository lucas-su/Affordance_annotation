import pandas, numpy, csv, pickle
from language_model.datafunctions import allnames
from statistics import  mean, stdev



if __name__ == "__main__":
    annotationDataset = pandas.read_pickle("..\\language_model\\data\\combined_final.pickle")
    threadstodo = pandas.read_pickle("..\\language_model\\data\\threadstodo_2020-12-01_09-15-02.759611.pickle")

    with open('data\\allnameslist.pickle', 'rb') as file:
        allnameslist = pickle.load(file)
    # annotatornames = [allnameslist[i] for i in [5,8,105,163]]
    removedAnnotators = [allnameslist[i] for i in []]
    annotatornames = ['52618', 'Tony']

    agreemode = 0
    for annotatorname in annotatornames:
        total_agreement = 0
        total_messages = 0
        skipped = 0
        try:
            annot1threads = annotationDataset.groupby("annotator1Name").get_group(annotatorname).thread.unique()
        except:
            annot1threads = []
        try:
            annot2threads = annotationDataset.groupby("annotator2Name").get_group(annotatorname).thread.unique()
        except:
            annot2threads = []
        try:
            annot3threads = annotationDataset.groupby("annotator3Name").get_group(annotatorname).thread.unique()
        except:
            annot3threads =[]

        for thread in annot1threads:
            if annotationDataset.groupby('thread').get_group(thread).annotator2Name.unique().__len__()>0 and \
                    annotationDataset.groupby('thread').get_group(thread).annotator3Name.unique().__len__()>0:
                if not annotationDataset.groupby('thread').get_group(thread).annotator2Name.unique()[0] in removedAnnotators and \
                    not annotationDataset.groupby('thread').get_group(thread).annotator3Name.unique()[0] in removedAnnotators:
                    otherscompEmph = annotationDataset.groupby('thread').get_group(thread).annotator2IsEmpathy == \
                                     annotationDataset.groupby('thread').get_group(thread).annotator3IsEmpathy
                    annotcompEmph = annotationDataset.groupby('thread').get_group(thread).annotator1IsEmpathy == \
                                    [x if list(otherscompEmph)[i] else list(annotationDataset.groupby('thread').get_group(thread).annotator1IsEmpathy)[i] for i, x in enumerate(annotationDataset.groupby('thread').get_group(thread).annotator2IsEmpathy)]
                    for i, text in enumerate(annotationDataset.groupby('thread').get_group(thread).text):
                        if not type(list(annotationDataset.groupby('thread').get_group(thread).annotator1IsEmpathy)[i]) == float:
                            if agreemode:
                                if not list(annotcompEmph)[i]:
                                    print(text, annotatorname,
                                          list(annotationDataset.groupby('thread').get_group(thread).annotator1IsEmpathy)[i])
                                    if list(annotationDataset.groupby('thread').get_group(thread).annotator1IsEmpathy)[i] == True:
                                        print(list(annotationDataset.groupby('thread').get_group(thread).annotator1EmpathyType)[
                                                  i],
                                              list(annotationDataset.groupby('thread').get_group(
                                                  thread).annotator1EmpathyValence)[i])
                                    # else:
                                    #     continue
                                    inp = input('1 to agree, 0 to disagree, 2 to switch agreemode')
                                    if int(inp) == 2:
                                        agreemode = not agreemode
                                        continue
                                    total_messages += 1
                                    total_agreement += int(inp)
                                else:
                                    skipped+=1
                            # if not list(annotcompEmph)[i]:
                            else:
                                print(text, annotatorname, list(annotationDataset.groupby('thread').get_group(thread).annotator1IsEmpathy)[i])
                                if list(annotationDataset.groupby('thread').get_group(thread).annotator1IsEmpathy)[i] == True:
                                    print(list(annotationDataset.groupby('thread').get_group(thread).annotator1EmpathyType)[i],
                                          list(annotationDataset.groupby('thread').get_group(thread).annotator1EmpathyValence)[i])
                                else:
                                    continue
                                inp = input('1 to agree, 0 to disagree, 2 to switch agreemode')
                                if int(inp) == 2:
                                    agreemode = not agreemode
                                    continue
                                total_messages += 1
                                total_agreement += int(inp)
                                # else:
                                #     skipped+=1
        print("intermediary result: {} agreed out of {} for annotator {}".format(total_agreement, total_messages,
                                                                                 annotatorname))
        for thread in annot2threads:
            if annotationDataset.groupby('thread').get_group(thread).annotator1Name.unique().__len__()>0 and \
                    annotationDataset.groupby('thread').get_group(thread).annotator3Name.unique().__len__()>0:
                if not annotationDataset.groupby('thread').get_group(thread).annotator1Name.unique()[0] in removedAnnotators and \
                    not annotationDataset.groupby('thread').get_group(thread).annotator3Name.unique()[0] in removedAnnotators:
                    otherscompEmph = annotationDataset.groupby('thread').get_group(thread).annotator1IsEmpathy == annotationDataset.groupby('thread').get_group(thread).annotator3IsEmpathy
                    annotcompEmph = annotationDataset.groupby('thread').get_group(thread).annotator2IsEmpathy == \
                                    [x if list(otherscompEmph)[i] else list(annotationDataset.groupby('thread').get_group(thread).annotator2IsEmpathy)[i] for i, x in enumerate(annotationDataset.groupby('thread').get_group(thread).annotator1IsEmpathy)]
                    for i, text in enumerate(annotationDataset.groupby('thread').get_group(thread).text):
                        if not type(list(annotationDataset.groupby('thread').get_group(thread).annotator2IsEmpathy)[i]) == float:
                            if agreemode:
                                if not list(annotcompEmph)[i]:
                                    print(text, annotatorname, list(annotationDataset.groupby('thread').get_group(thread).annotator2IsEmpathy)[i])
                                    if list(annotationDataset.groupby('thread').get_group(thread).annotator2IsEmpathy)[i] == True:
                                        print(list(annotationDataset.groupby('thread').get_group(thread).annotator2EmpathyType)[i],
                                              list(annotationDataset.groupby('thread').get_group(thread).annotator2EmpathyValence)[i])
                                    # else:
                                    #     continue
                                    inp = input('1 to agree, 0 to disagree, 2 to switch agreemode')
                                    if int(inp) == 2:
                                        agreemode = not agreemode
                                        continue
                                    total_messages += 1
                                    total_agreement += int(inp)
                                else:
                                    skipped+=1
                            else:
                                print(text, annotatorname,
                                      list(annotationDataset.groupby('thread').get_group(thread).annotator2IsEmpathy)[i])
                                if list(annotationDataset.groupby('thread').get_group(thread).annotator2IsEmpathy)[i] == True:
                                    print(list(annotationDataset.groupby('thread').get_group(thread).annotator2EmpathyType)[
                                              i],
                                          list(annotationDataset.groupby('thread').get_group(
                                              thread).annotator2EmpathyValence)[i])
                                else:
                                    continue
                                inp = input('1 to agree, 0 to disagree, 2 to switch agreemode')
                                if int(inp) == 2:
                                    agreemode = not agreemode
                                    continue
                                total_messages += 1
                                total_agreement += int(inp)
        print("intermediary result: {} agreed out of {} for annotator {}".format(total_agreement, total_messages, annotatorname))
        for thread in annot3threads:
            if annotationDataset.groupby('thread').get_group(thread).annotator1Name.unique().__len__()>0 and \
                    annotationDataset.groupby('thread').get_group(thread).annotator2Name.unique().__len__()>0:
                if not annotationDataset.groupby('thread').get_group(thread).annotator1Name.unique()[0] in removedAnnotators and \
                    not annotationDataset.groupby('thread').get_group(thread).annotator2Name.unique()[0] in removedAnnotators:
                    otherscompEmph = annotationDataset.groupby('thread').get_group(thread).annotator1IsEmpathy == annotationDataset.groupby('thread').get_group(thread).annotator2IsEmpathy
                    annotcompEmph = annotationDataset.groupby('thread').get_group(thread).annotator3IsEmpathy == \
                                    [x if list(otherscompEmph)[i] else list(annotationDataset.groupby('thread').get_group(thread).annotator3IsEmpathy)[i] for i, x in enumerate(annotationDataset.groupby('thread').get_group(thread).annotator1IsEmpathy)]
                    for i, text in enumerate(annotationDataset.groupby('thread').get_group(thread).text):
                        if not type(list(annotationDataset.groupby('thread').get_group(thread).annotator3IsEmpathy)[i]) == float:
                            if agreemode:
                                if not list(annotcompEmph)[i]:
                                    print(text, annotatorname,  list(annotationDataset.groupby('thread').get_group(thread).annotator3IsEmpathy)[i])
                                    if list(annotationDataset.groupby('thread').get_group(thread).annotator3IsEmpathy)[i] == True:
                                        print(list(annotationDataset.groupby('thread').get_group(thread).annotator3EmpathyType)[i],
                                              list(annotationDataset.groupby('thread').get_group(thread).annotator3EmpathyValence)[i])
                                    # else:
                                    #     continue
                                    inp = input('1 to agree, 0 to disagree, 2 to switch agreemode')
                                    if int(inp) == 2:
                                        agreemode = not agreemode
                                        continue
                                    total_messages += 1
                                    total_agreement += int(inp)
                                else:
                                    skipped += 1
                            else:
                                print(text, annotatorname,
                                      list(annotationDataset.groupby('thread').get_group(thread).annotator3IsEmpathy)[i])
                                if list(annotationDataset.groupby('thread').get_group(thread).annotator3IsEmpathy)[i] == True:
                                    print(list(annotationDataset.groupby('thread').get_group(thread).annotator3EmpathyType)[
                                              i],
                                          list(annotationDataset.groupby('thread').get_group(
                                              thread).annotator3EmpathyValence)[i])
                                else:
                                    continue
                                inp = input('1 to agree, 0 to disagree, 2 to switch agreemode')
                                if int(inp) == 2:
                                    agreemode = not agreemode
                                    continue
                                total_messages += 1
                                total_agreement += int(inp)


        print("{} agreed out of {} for annotator {}".format(total_agreement,total_messages, annotatorname))
        print("{} skipped".format(skipped))
        with open('manual_annotator_compare.csv', 'a') as file:
            writer = csv.writer(file)
            writer.writerow([annotatorname,total_agreement,total_messages])