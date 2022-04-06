import pandas, numpy, csv, pickle
from language_model.datafunctions import allnames
from statistics import  mean, stdev



if __name__ == "__main__":
    annotationDataset = pandas.read_pickle("..\\language_model\\data\\annotationDataset_2020-12-01_09-15-00.163841.pickle")
    threadstodo = pandas.read_pickle("..\\language_model\\data\\threadstodo_2020-12-01_09-15-02.759611.pickle")

    with open('data\\allnameslist.pickle', 'rb') as file:
        allnameslist = pickle.load(file)

    # annotatornames = [allnameslist[i] for i in [5,8,105,163]]

    # annotatornames = [allnameslist[i] for i in [39,44,50,88,89,92,124,129,134,145,146,154,156]]
    scoredict = {}
    nextiterationscoredict = {}
    iteration0dict = {}
    iteration1dict = {}
    iteration2dict = {}
    iteration3dict = {}
    with open('data\\agreementscore_with_nan_correction_4.csv', 'r') as file:
        reader = csv.reader(file)
        linenum = 0
        for line in reader:
            if line:
                if line[0] == '0':
                    iteration0dict[line[1]] = line[2]
                if line[0] == '1':
                    iteration1dict[line[1]] = line[2]
                # if line[0] == '2':
                #     iteration2dict[line[1]] = 2* float(line[2])
                # if line[0] == '3':
                #     iteration3dict[line[1]] = float(line[2])
    #
    #         linenum += 1
    # iteration0mean = mean([float(x) for x in iteration0dict.values()])
    # iteration0stdev = stdev([float(x) for x in iteration0dict.values()])
    # removedAnnotators = [key for key in iteration0dict.keys() if float(iteration0dict[key])<(iteration0mean-iteration0stdev)]
    # removedAnnotators.extend(['A3E9FY9IWAR90X', 'A1CDPZMO705DEQ', 'A23ATSM5CU43EI', 'Maru', 'ADTJF28QF3VKE', 'johny',
    #                           'JEYANTHI', 'A30TM32AO7OB3W', 'A2RBB56IYWJ2YZ', 'Jennifer Billiris', 'A27K5BAW3U9W6P',
    #                           'A70GUOHM5F8DC', 'A2D214FXNIM28I', 'A19LFT0F3JO9BP', 'AY1GRLXDMXELF', 'noyjhing', 'ARUN'])
    #

    # removedAnnotators.append(numpy.nan)
    removedAnnotators = [numpy.nan, 'gebruikersnaam', 'A28LMUIZO84GAX', 'AMEQUH2AXDPR2', 'A1W8PU7Z3JLV5B', 'Ik begrijp dat je je boos voelt', 'A23KAJRDVCVGOE', 'APGBKNB9G69GT', 'A2ECERIL4RF6FO', 'A1BOQAPANXDC0K', 'A1H6DME332958N', 'A3PIJWV36NY7U4', 'Efun/A1Y9D4RKC3BZQ3', 'michel ', 'A3MAM5PA42A7CW', 'A4QDCBGN79832', 'A3G479CZZJOSJ2', 'A161R7U61GXNFC', 'Aaa', 'ACI8PUCF5OPDC', 'A26BNL983RC4YZ', 'A2GZ468WSRF7WJ', 'A382SL9ROIY1P6', 'A2R5TVQYSZE74K', 'A1M987KDHQYKY7', 'A1YO75Q6M618HU', 'als gebruikersnaam.', 'A121QS3395N67M', 'A3NI8HMVCT7SOF', 'A25STPOLAHMLIA', 'Cock', 'A1R65GQL81PGIK', 'A1SBFOZG5J97Z1', 'A1XLJP8MM2H5DX', 'mtk', 'PHILIP']

    remcount = 0
    for annotatorname in allnameslist:
        scoredict[annotatorname] = mean([2*float(iteration0dict[annotatorname]),1])
        try:
            nextiterationscoredict[annotatorname] = 2*float(iteration1dict[annotatorname])
        except:
            remcount +=1
            if remcount > 30:
                print('username not in nextiterationscoredict: {}'.format(remcount))
    # for annotator in iteration1dict.keys():
    #     scoredict[annotator] = mean([float(iteration0dict[annotator])*2, float(iteration1dict[annotator])*2])
    for removedannotator in removedAnnotators:
        try:
            del scoredict[removedannotator]
        except:
            print("{} already removed.".format(removedannotator))
    for iteration in [2,3]:
        # if iteration == 1:
        #     for annotatorname in nextiterationscoredict.keys():
        #         with open('data\\agreementscore_with_nan_correction_6.csv', 'a') as file:
        #             writer = csv.writer(file)
        #             writer.writerow([0, annotatorname, nextiterationscoredict[annotatorname]])
        #         nextiterationscoredict[annotatorname] = 2* nextiterationscoredict[annotatorname]
        if iteration > 0:
            for annotator in scoredict.keys():
                scoredict[annotator] = mean([nextiterationscoredict[annotator], scoredict[annotator]])
            meanval = mean(scoredict.values())
            stdevval = stdev(scoredict.values())
            for annotatorname in allnameslist:
                if annotatorname not in removedAnnotators:
                    if float(scoredict[annotatorname]) < (meanval-stdevval):
                        if annotatorname not in ['52618', 'Tony']:
                            removedAnnotators.append(annotatorname)
                            del scoredict[annotatorname]
        else:
            meanval = 1
            stdevval = 0
        print('mean: {} stdev{}'.format(meanval, stdevval))
        with open('data\\agreementscore_stats_5.csv', 'a') as file:
            writer = csv.writer(file)
            writer.writerow(removedAnnotators)
            writer.writerow([mean(scoredict.values()),stdev(scoredict.values())])
        if removedAnnotators.__len__()>1:
            print("amount of annotators removed: {}".format(removedAnnotators.__len__()))
            print(removedAnnotators)
        else:
            print(removedAnnotators.__len__())
        # for annotator in nextiterationscoredict.keys():
        #     scoredict[annotator] = mean([nextiterationscoredict[annotator], scoredict[annotator]])
        for annotatorname in allnameslist:
            if annotatorname in removedAnnotators:
                print("skipping: {}".format(annotatorname))
                continue
            print("Working on annotator {}, {} out of {}".format(annotatorname, allnameslist.index(annotatorname)+1, allnameslist.__len__()))
            print("{} is larger than {}".format(scoredict[annotatorname], (meanval-stdevval)))
            # if annotatorname in iteration3dict.keys():
            #     print('found {} in csv file, skipping')
            #     nextiterationscoredict[annotatorname] = 2 * float(iteration3dict[annotatorname])
            #     print(nextiterationscoredict[annotatorname])
            #     continue
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
                if not annotationDataset.groupby('thread').get_group(thread).annotator2Name.unique()[0] in removedAnnotators \
                        and type(annotationDataset.groupby('thread').get_group(thread).annotator2Name.unique()[0]) == str:
                    comp12emp = annotationDataset.groupby('thread').get_group(thread).annotator1IsEmpathy == \
                                annotationDataset.groupby('thread').get_group(thread).annotator2IsEmpathy
                    comp12askemp = annotationDataset.groupby('thread').get_group(thread).annotator1AskEmpathy == \
                                   annotationDataset.groupby('thread').get_group(thread).annotator2AskEmpathy
                    comp12cta = annotationDataset.groupby('thread').get_group(thread).annotator1CallToAction == \
                                annotationDataset.groupby('thread').get_group(thread).annotator2CallToAction
                    comp12isans = annotationDataset.groupby('thread').get_group(thread).annotator1IsAnswer == \
                                  annotationDataset.groupby('thread').get_group(thread).annotator2IsAnswer
                    comp12isq = annotationDataset.groupby('thread').get_group(thread).annotator1IsQuestion == \
                                annotationDataset.groupby('thread').get_group(thread).annotator2IsQuestion
                    multiplier12 = scoredict[annotationDataset.groupby('thread').get_group(thread).annotator2Name.unique()[0]]
                    for i, _ in enumerate(comp12emp):
                        if type(list(annotationDataset.groupby('thread').get_group(thread).annotator1AskEmpathy)[i]) == float:
                            comp12askemp[i] = False # don't count nan as agreeing
                            total_messages -= 1
                        if type(list(annotationDataset.groupby('thread').get_group(thread).annotator1CallToAction)[i]) == float:
                            comp12cta[i] = False
                            total_messages -= 1
                        if type(list(annotationDataset.groupby('thread').get_group(thread).annotator1IsAnswer)[i]) == float:
                            comp12isans[i] = False
                            total_messages -= 1
                        if type(list(annotationDataset.groupby('thread').get_group(thread).annotator1IsQuestion)[i]) == float:
                            comp12isq[i] = False
                            total_messages -= 1
                        if type(list(annotationDataset.groupby('thread').get_group(thread).annotator1IsEmpathy)[i]) == float:
                            comp12emp[i] = False
                            total_messages -= 1
                    total_agreement += sum([sum(x) * multiplier12 for x in [comp12askemp, comp12cta, comp12isans, comp12isq, comp12emp]])
                    total_messages += sum([x.__len__() for x in [comp12askemp, comp12cta, comp12isans, comp12isq, comp12emp]])

                if not annotationDataset.groupby('thread').get_group(thread).annotator3Name.unique()[0] in removedAnnotators \
                        and type(annotationDataset.groupby('thread').get_group(thread).annotator3Name.unique()[0]) == str:
                    comp13emp = annotationDataset.groupby('thread').get_group(thread).annotator1IsEmpathy == \
                                annotationDataset.groupby('thread').get_group(thread).annotator3IsEmpathy
                    comp13askemp = annotationDataset.groupby('thread').get_group(thread).annotator1AskEmpathy == \
                                   annotationDataset.groupby('thread').get_group(thread).annotator3AskEmpathy
                    comp13cta = annotationDataset.groupby('thread').get_group(thread).annotator1CallToAction == \
                                annotationDataset.groupby('thread').get_group(thread).annotator3CallToAction
                    comp13isans = annotationDataset.groupby('thread').get_group(thread).annotator1IsAnswer == \
                                  annotationDataset.groupby('thread').get_group(thread).annotator3IsAnswer
                    comp13isq = annotationDataset.groupby('thread').get_group(thread).annotator1IsQuestion == \
                                annotationDataset.groupby('thread').get_group(thread).annotator3IsQuestion
                    # comp13 = annotationDataset.groupby('thread').get_group(thread).annotator1IsEmpathy == \
                    # annotationDataset.groupby('thread').get_group(thread).annotator3IsEmpathy
                    multiplier13 = scoredict[annotationDataset.groupby('thread').get_group(thread).annotator3Name.unique()[0]]
                    for i, _ in enumerate(comp13emp):
                        if type(list(annotationDataset.groupby('thread').get_group(thread).annotator1AskEmpathy)[i]) == float:
                            comp13askemp[i] = False  # don't count nan as agreeing
                            total_messages -= 1
                        if type(list(annotationDataset.groupby('thread').get_group(thread).annotator1CallToAction)[i]) == float:
                            comp13cta[i] = False
                            total_messages -= 1
                        if type(list(annotationDataset.groupby('thread').get_group(thread).annotator1IsAnswer)[i]) == float:
                            comp13isans[i] = False
                            total_messages -= 1
                        if type(list(annotationDataset.groupby('thread').get_group(thread).annotator1IsQuestion)[i]) == float:
                            comp13isq[i] = False
                            total_messages -= 1
                        if type(list(annotationDataset.groupby('thread').get_group(thread).annotator1IsEmpathy)[i]) == float:
                            comp13emp[i] = False
                            total_messages -= 1
                    total_agreement += sum([sum(x) * multiplier13 for x in [comp13askemp, comp13cta, comp13isans, comp13isq, comp13emp]])
                    total_messages += sum([x.__len__() for x in [comp13askemp, comp13cta, comp13isans, comp13isq, comp13emp]])

            for thread in annot2threads:
                if not annotationDataset.groupby('thread').get_group(thread).annotator1Name.unique()[0] in removedAnnotators \
                        and type(annotationDataset.groupby('thread').get_group(thread).annotator1Name.unique()[0]) == str:
                    comp21emp = annotationDataset.groupby('thread').get_group(thread).annotator2IsEmpathy == \
                                annotationDataset.groupby('thread').get_group(thread).annotator1IsEmpathy
                    comp21askemp = annotationDataset.groupby('thread').get_group(thread).annotator2AskEmpathy == \
                                   annotationDataset.groupby('thread').get_group(thread).annotator1AskEmpathy
                    comp21cta = annotationDataset.groupby('thread').get_group(thread).annotator2CallToAction == \
                                annotationDataset.groupby('thread').get_group(thread).annotator1CallToAction
                    comp21isans = annotationDataset.groupby('thread').get_group(thread).annotator2IsAnswer == \
                                  annotationDataset.groupby('thread').get_group(thread).annotator1IsAnswer
                    comp21isq = annotationDataset.groupby('thread').get_group(thread).annotator2IsQuestion == \
                                annotationDataset.groupby('thread').get_group(thread).annotator1IsQuestion

                    # comp21 = annotationDataset.groupby('thread').get_group(thread).annotator2IsEmpathy == annotationDataset.groupby('thread').get_group(thread).annotator1IsEmpathy
                    multiplier21 = scoredict[annotationDataset.groupby('thread').get_group(thread).annotator1Name.unique()[0]]
                    for i, _ in enumerate(comp21emp):
                        if type(list(annotationDataset.groupby('thread').get_group(thread).annotator2AskEmpathy)[i]) == float:
                            comp21askemp[i] = False  # don't count nan as agreeing
                            total_messages -= 1
                        if type(list(annotationDataset.groupby('thread').get_group(thread).annotator2CallToAction)[i]) == float:
                            comp21cta[i] = False
                            total_messages -= 1
                        if type(list(annotationDataset.groupby('thread').get_group(thread).annotator2IsAnswer)[i]) == float:
                            comp21isans[i] = False
                            total_messages -= 1
                        if type(list(annotationDataset.groupby('thread').get_group(thread).annotator2IsQuestion)[i]) == float:
                            comp21isq[i] = False
                            total_messages -= 1
                        if type(list(annotationDataset.groupby('thread').get_group(thread).annotator2IsEmpathy)[i]) == float:
                            comp21emp[i] = False
                            total_messages -= 1
                            # comp21[i] = False
                    total_agreement += sum([sum(x) * multiplier21 for x in [comp21askemp, comp21cta, comp21isans, comp21isq, comp21emp]])
                    total_messages += sum([x.__len__() for x in [comp21askemp, comp21cta, comp21isans, comp21isq, comp21emp]])

                if not annotationDataset.groupby('thread').get_group(thread).annotator3Name.unique()[0] in removedAnnotators \
                        and type(annotationDataset.groupby('thread').get_group(thread).annotator3Name.unique()[0]) == str:
                    comp23emp = annotationDataset.groupby('thread').get_group(thread).annotator2IsEmpathy == \
                                annotationDataset.groupby('thread').get_group(thread).annotator3IsEmpathy
                    comp23askemp = annotationDataset.groupby('thread').get_group(thread).annotator2AskEmpathy == \
                                   annotationDataset.groupby('thread').get_group(thread).annotator3AskEmpathy
                    comp23cta = annotationDataset.groupby('thread').get_group(thread).annotator2CallToAction == \
                                annotationDataset.groupby('thread').get_group(thread).annotator3CallToAction
                    comp23isans = annotationDataset.groupby('thread').get_group(thread).annotator2IsAnswer == \
                                  annotationDataset.groupby('thread').get_group(thread).annotator3IsAnswer
                    comp23isq = annotationDataset.groupby('thread').get_group(thread).annotator2IsQuestion == \
                                annotationDataset.groupby('thread').get_group(thread).annotator3IsQuestion

                    # comp23 = annotationDataset.groupby('thread').get_group(thread).annotator2IsEmpathy == annotationDataset.groupby('thread').get_group(thread).annotator3IsEmpathy
                    multiplier23 = scoredict[annotationDataset.groupby('thread').get_group(thread).annotator3Name.unique()[0]]
                    for i, _ in enumerate(comp23emp):
                        if type(list(annotationDataset.groupby('thread').get_group(thread).annotator2AskEmpathy)[i]) == float:
                            comp23askemp[i] = False  # don't count nan as agreeing
                            total_messages -= 1
                        if type(list(annotationDataset.groupby('thread').get_group(thread).annotator2CallToAction)[i]) == float:
                            comp23cta[i] = False
                            total_messages -= 1
                        if type(list(annotationDataset.groupby('thread').get_group(thread).annotator2IsAnswer)[i]) == float:
                            comp23isans[i] = False
                            total_messages -= 1
                        if type(list(annotationDataset.groupby('thread').get_group(thread).annotator2IsQuestion)[i]) == float:
                            comp23isq[i] = False
                            total_messages -= 1
                        if type(list(annotationDataset.groupby('thread').get_group(thread).annotator2IsEmpathy)[i]) == float:
                            comp23emp[i] = False
                            total_messages -= 1
                    total_agreement += sum([sum(x) * multiplier23 for x in [comp23askemp, comp23cta, comp23isans, comp23isq, comp23emp]])
                    total_messages += sum([x.__len__() for x in [comp23askemp, comp23cta, comp23isans, comp23isq, comp23emp]])


            for thread in annot3threads:
                if not annotationDataset.groupby('thread').get_group(thread).annotator1Name.unique()[0] in removedAnnotators \
                        and type(annotationDataset.groupby('thread').get_group(thread).annotator1Name.unique()[0]) == str:
                    comp31emp = annotationDataset.groupby('thread').get_group(thread).annotator3IsEmpathy == \
                                annotationDataset.groupby('thread').get_group(thread).annotator1IsEmpathy
                    comp31askemp = annotationDataset.groupby('thread').get_group(thread).annotator3AskEmpathy == \
                                   annotationDataset.groupby('thread').get_group(thread).annotator1AskEmpathy
                    comp31cta = annotationDataset.groupby('thread').get_group(thread).annotator3CallToAction == \
                                annotationDataset.groupby('thread').get_group(thread).annotator1CallToAction
                    comp31isans = annotationDataset.groupby('thread').get_group(thread).annotator3IsAnswer == \
                                  annotationDataset.groupby('thread').get_group(thread).annotator1IsAnswer
                    comp31isq = annotationDataset.groupby('thread').get_group(thread).annotator3IsQuestion == \
                                annotationDataset.groupby('thread').get_group(thread).annotator1IsQuestion

                    # comp31 = annotationDataset.groupby('thread').get_group(thread).annotator3IsEmpathy == annotationDataset.groupby('thread').get_group(thread).annotator1IsEmpathy
                    multiplier31 = scoredict[annotationDataset.groupby('thread').get_group(thread).annotator1Name.unique()[0]]
                    for i, _ in enumerate(comp31emp):
                        if type(list(annotationDataset.groupby('thread').get_group(thread).annotator3AskEmpathy)[i]) == float:
                            comp31askemp[i] = False  # don't count nan as agreeing
                            total_messages -= 1
                        if type(list(annotationDataset.groupby('thread').get_group(thread).annotator3CallToAction)[i]) == float:
                            comp31cta[i] = False
                            total_messages -= 1
                        if type(list(annotationDataset.groupby('thread').get_group(thread).annotator3IsAnswer)[i]) == float:
                            comp31isans[i] = False
                            total_messages -= 1
                        if type(list(annotationDataset.groupby('thread').get_group(thread).annotator3IsQuestion)[i]) == float:
                            comp31isq[i] = False
                            total_messages -= 1
                        if type(list(annotationDataset.groupby('thread').get_group(thread).annotator3IsEmpathy)[i]) == float:
                            comp31emp[i] = False
                            total_messages -= 1

                            # comp31[i] = False
                    total_agreement += sum([sum(x) * multiplier31 for x in [comp31askemp, comp31cta, comp31isans, comp31isq, comp31emp]])
                    total_messages += sum([x.__len__() for x in [comp31askemp, comp31cta, comp31isans, comp31isq, comp31emp]])



                if not annotationDataset.groupby('thread').get_group(thread).annotator2Name.unique()[0] in removedAnnotators \
                        and type(annotationDataset.groupby('thread').get_group(thread).annotator2Name.unique()[0]) == str:
                    comp32emp = annotationDataset.groupby('thread').get_group(thread).annotator3IsEmpathy == \
                                annotationDataset.groupby('thread').get_group(thread).annotator2IsEmpathy
                    comp32askemp = annotationDataset.groupby('thread').get_group(thread).annotator3AskEmpathy == \
                                   annotationDataset.groupby('thread').get_group(thread).annotator2AskEmpathy
                    comp32cta = annotationDataset.groupby('thread').get_group(thread).annotator3CallToAction == \
                                annotationDataset.groupby('thread').get_group(thread).annotator2CallToAction
                    comp32isans = annotationDataset.groupby('thread').get_group(thread).annotator3IsAnswer == \
                                  annotationDataset.groupby('thread').get_group(thread).annotator2IsAnswer
                    comp32isq = annotationDataset.groupby('thread').get_group(thread).annotator3IsQuestion == \
                                annotationDataset.groupby('thread').get_group(thread).annotator2IsQuestion

                    # comp32 = annotationDataset.groupby('thread').get_group(thread).annotator3IsEmpathy == annotationDataset.groupby('thread').get_group(thread).annotator2IsEmpathy
                    multiplier32 = scoredict[annotationDataset.groupby('thread').get_group(thread).annotator2Name.unique()[0]]
                    for i, _ in enumerate(comp32emp):
                        if type(list(annotationDataset.groupby('thread').get_group(thread).annotator3AskEmpathy)[i]) == float:
                            comp32askemp[i] = False  # don't count nan as agreeing
                            total_messages -= 1
                        if type(list(annotationDataset.groupby('thread').get_group(thread).annotator3CallToAction)[i]) == float:
                            comp32cta[i] = False
                            total_messages -= 1
                        if type(list(annotationDataset.groupby('thread').get_group(thread).annotator3IsAnswer)[i]) == float:
                            comp32isans[i] = False
                            total_messages -= 1
                        if type(list(annotationDataset.groupby('thread').get_group(thread).annotator3IsQuestion)[i]) == float:
                            comp32isq[i] = False
                            total_messages -= 1
                        if type(list(annotationDataset.groupby('thread').get_group(thread).annotator3IsEmpathy)[i]) == float:
                            comp32emp[i] = False
                            total_messages -= 1
                    total_agreement += sum([sum(x) * multiplier32 for x in [comp32askemp, comp32cta, comp32isans, comp32isq, comp32emp]])
                    total_messages += sum([x.__len__() for x in [comp32askemp, comp32cta, comp32isans, comp32isq, comp32emp]])

            if total_messages == 0:
                agreement_factor = scoredict[annotatorname]
                print('annotator {} has no co annotators left!'.format(annotatorname))
            else:
                agreement_factor =(total_agreement/total_messages)
            with open('data\\agreementscore_with_nan_correction_6.csv', 'a') as file:
                writer = csv.writer(file)
                writer.writerow([iteration, annotatorname, agreement_factor])
            nextiterationscoredict[annotatorname] = 2* agreement_factor
            print(nextiterationscoredict[annotatorname])
