import pandas, numpy, pickle
from language_model.datafunctions import allnames
from statistics import  mean, stdev
import matplotlib.pyplot as plt

def calculate_differences(features, allnameslist):
    differences = numpy.zeros(allnameslist.__len__())

    for featurename in features:
        counts = [checkAnnotator(x, featurename, allnameslist) for x in allnameslist]
        # title='Call to Action'
        # groupedbarplot(counts, allnames, title)
        differences = [differences[i] + count for i, count in enumerate([x[0] - x[1] for x in counts])]
    return [difference/features.__len__() for difference in differences ]


def val_counts(name, feature):
    totalTrue = []
    totalFalse = []
    try:
        if feature == 'IsEmpathy':
            count1 = annotationDataset.groupby('annotator1Name').get_group(name).annotator1IsEmpathy.value_counts()
        elif feature == 'IsAnswer':
            count1 = annotationDataset.groupby('annotator1Name').get_group(name).annotator1IsAnswer.value_counts()
        elif feature == 'CallToAction':
            count1 = annotationDataset.groupby('annotator1Name').get_group(name).annotator1CallToAction.value_counts()
        elif feature == 'AskEmpathy':
            count1 = annotationDataset.groupby('annotator1Name').get_group(name).annotator1AskEmpathy.value_counts()
        elif feature == 'IsQuestion':
            count1 = annotationDataset.groupby('annotator1Name').get_group(name).annotator1IsQuestion.value_counts()
    except:
        count1 = [0,0]
    try:
        if feature == 'IsEmpathy':
            count2 = annotationDataset.groupby('annotator2Name').get_group(name).annotator2IsEmpathy.value_counts()
        elif feature == 'IsAnswer':
            count2 = annotationDataset.groupby('annotator2Name').get_group(name).annotator2IsAnswer.value_counts()
        elif feature == 'CallToAction':
            count2 = annotationDataset.groupby('annotator2Name').get_group(name).annotator2CallToAction.value_counts()
        elif feature == 'AskEmpathy':
            count2 = annotationDataset.groupby('annotator2Name').get_group(name).annotator2AskEmpathy.value_counts()
        elif feature == 'IsQuestion':
            count2 = annotationDataset.groupby('annotator2Name').get_group(name).annotator2IsQuestion.value_counts()
    except:
        count2 = [0,0]
    try:
        if feature == 'IsEmpathy':
            count3 = annotationDataset.groupby('annotator3Name').get_group(name).annotator3IsEmpathy.value_counts()
        elif feature == 'IsAnswer':
            count3 = annotationDataset.groupby('annotator3Name').get_group(name).annotator3IsAnswer.value_counts()
        elif feature == 'CallToAction':
            count3 = annotationDataset.groupby('annotator3Name').get_group(name).annotator3CallToAction.value_counts()
        elif feature == 'AskEmpathy':
            count3 = annotationDataset.groupby('annotator3Name').get_group(name).annotator3AskEmpathy.value_counts()
        elif feature == 'IsQuestion':
            count3 = annotationDataset.groupby('annotator3Name').get_group(name).annotator3IsQuestion.value_counts()
    except:
        count3 = [0,0]
    try:
        if count1.keys()[0] == 0:
            totalFalse.append(count1[0])
    except:
        pass
    try:
        if count2.keys()[0] == 0:
            totalFalse.append(count2[0])
    except:
        pass
    try:
        if count3.keys()[0] == 0:
            totalFalse.append(count3[0])
    except:
        pass
    try:
        if count1.keys()[1] == 1:
            totalTrue.append(count1[1])
    except:
        pass
    try:
        if count2.keys()[1] == 1:
            totalTrue.append(count2[1])
    except:
        pass
    try:
        if count3.keys()[1] == 1:
            totalTrue.append(count3[1])
    except:
        pass
    try:
        if count1.keys()[1] == 0:
            totalFalse.append(count1[1])
    except:
        pass
    try:
        if count2.keys()[1] == 0:
            totalFalse.append(count2[1])
    except:
        pass
    try:
        if count3.keys()[1] == 0:
            totalFalse.append(count3[1])
    except:
        pass
    try:
        if count1.keys()[0] == 1:
            totalTrue.append(count1[0])
    except:
        pass
    try:
        if count2.keys()[0] == 1:
            totalTrue.append(count2[0])
    except:
        pass
    try:
        if count3.keys()[0] == 1:
            totalTrue.append(count3[0])
    except:
        pass
    return totalTrue, totalFalse


def checkAnnotator(annotator, feature, allowedannotators):
    try:
        threads1 =  annotationDataset.groupby('annotator1Name').get_group(annotator).thread.unique()
    except:
        threads1 = []
    try:
        threads2 =  annotationDataset.groupby('annotator2Name').get_group(annotator).thread.unique()
    except:
        threads2 = []
    try:
        threads3 =  annotationDataset.groupby('annotator3Name').get_group(annotator).thread.unique()
    except:
        threads3 = []

    allthreads = numpy.concatenate((threads1,threads2, threads3), axis=None)
    # allthreads = allthreads.append(list(threads1))
    # allthreads = allthreads.append(list(threads2))
    # allthreads = allthreads.append(list(threads3))
    valCounts = val_counts(annotator, feature)
    combined_val_counts = [sum(valCounts[0]), sum(valCounts[1])]
    if sum(combined_val_counts) != 0:
        normalized_val_counts = combined_val_counts[0]/sum(combined_val_counts)
    else:
        normalized_val_counts = 0
    #
    totalTrue1 = []
    totalTrue2 = []
    totalTrue = []
    totalFalse1 = []
    totalFalse2 = []
    totalFalse= []
    for thread in allthreads:
        if threadstodo.loc[threadstodo['name']==thread].annotator1.values[0] == annotator:
            if feature == 'IsEmpathy':
                if list(annotationDataset.groupby('thread').get_group(thread).annotator2Name)[0] in allowedannotators:
                    count1 = annotationDataset.groupby('thread').get_group(thread).annotator2IsEmpathy.value_counts()
                else:
                    print('skipping {}'.format(list(annotationDataset.groupby('thread').get_group(thread).annotator2Name)[0]))
                    count1 = pandas.Series({-1:-1})
                if list(annotationDataset.groupby('thread').get_group(thread).annotator3Name)[0] in allowedannotators:
                    count2 = annotationDataset.groupby('thread').get_group(thread).annotator3IsEmpathy.value_counts()
                else:
                    print('skipping {}'.format(list(annotationDataset.groupby('thread').get_group(thread).annotator3Name)[0]))
                    count2 = pandas.Series({-1:-1})
            elif feature == 'IsAnswer':
                if list(annotationDataset.groupby('thread').get_group(thread).annotator2Name)[0] in allowedannotators:
                    count1 = annotationDataset.groupby('thread').get_group(thread).annotator2IsAnswer.value_counts()
                else:
                    print('skipping {}'.format(list(annotationDataset.groupby('thread').get_group(thread).annotator2Name)[0]))
                    count1 = pandas.Series({-1:-1})
                if list(annotationDataset.groupby('thread').get_group(thread).annotator3Name)[0] in allowedannotators:
                    count2 = annotationDataset.groupby('thread').get_group(thread).annotator3IsAnswer.value_counts()
                else:
                    print('skipping {}'.format(list(annotationDataset.groupby('thread').get_group(thread).annotator3Name)[0]))
                    count2 = pandas.Series({-1:-1})
            elif feature == 'CallToAction':
                if list(annotationDataset.groupby('thread').get_group(thread).annotator2Name)[0] in allowedannotators:
                    count1 = annotationDataset.groupby('thread').get_group(thread).annotator2CallToAction.value_counts()
                else:
                    print('skipping {}'.format(list(annotationDataset.groupby('thread').get_group(thread).annotator2Name)[0]))
                    count1 = pandas.Series({-1:-1})
                if list(annotationDataset.groupby('thread').get_group(thread).annotator3Name)[0] in allowedannotators:
                    count2 = annotationDataset.groupby('thread').get_group(thread).annotator3CallToAction.value_counts()
                else:
                    print('skipping {}'.format(list(annotationDataset.groupby('thread').get_group(thread).annotator3Name)[0]))
                    count2 = pandas.Series({-1:-1})
            elif feature == 'AskEmpathy':
                if list(annotationDataset.groupby('thread').get_group(thread).annotator2Name)[0] in allowedannotators:
                    count1 = annotationDataset.groupby('thread').get_group(thread).annotator2AskEmpathy.value_counts()
                else:
                    print('skipping {}'.format(list(annotationDataset.groupby('thread').get_group(thread).annotator2Name)[0]))
                    count1 = pandas.Series({-1:-1})
                if list(annotationDataset.groupby('thread').get_group(thread).annotator3Name)[0] in allowedannotators:
                    count2 = annotationDataset.groupby('thread').get_group(thread).annotator3AskEmpathy.value_counts()
                else:
                    print('skipping {}'.format(list(annotationDataset.groupby('thread').get_group(thread).annotator3Name)[0]))
                    count2 = pandas.Series({-1:-1})
            elif feature == 'IsQuestion':
                if list(annotationDataset.groupby('thread').get_group(thread).annotator2Name)[0] in allowedannotators:
                    count1 = annotationDataset.groupby('thread').get_group(thread).annotator2IsQuestion.value_counts()
                else:
                    print('skipping {}'.format(list(annotationDataset.groupby('thread').get_group(thread).annotator2Name)[0]))
                    count1 = pandas.Series({-1:-1})
                if list(annotationDataset.groupby('thread').get_group(thread).annotator3Name)[0] in allowedannotators:
                    count2 = annotationDataset.groupby('thread').get_group(thread).annotator3IsQuestion.value_counts()
                else:
                    print('skipping {}'.format(list(annotationDataset.groupby('thread').get_group(thread).annotator3Name)[0]))
                    count2 = pandas.Series({-1:-1})
        elif threadstodo.loc[threadstodo['name']==thread].annotator2.values[0] == annotator:
            if feature == 'IsEmpathy':
                if list(annotationDataset.groupby('thread').get_group(thread).annotator1Name)[0] in allowedannotators:
                    count1 = annotationDataset.groupby('thread').get_group(thread).annotator1IsEmpathy.value_counts()
                else:
                    print('skipping {}'.format(list(annotationDataset.groupby('thread').get_group(thread).annotator1Name)[0]))
                    count1 = pandas.Series({-1:-1})
                if list(annotationDataset.groupby('thread').get_group(thread).annotator3Name)[0] in allowedannotators:
                    count2 = annotationDataset.groupby('thread').get_group(thread).annotator3IsEmpathy.value_counts()
                else:
                    print('skipping {}'.format(list(annotationDataset.groupby('thread').get_group(thread).annotator3Name)[0]))
                    count2 = pandas.Series({-1:-1})
            elif feature == 'IsAnswer':
                if list(annotationDataset.groupby('thread').get_group(thread).annotator1Name)[0] in allowedannotators:
                    count1 = annotationDataset.groupby('thread').get_group(thread).annotator1IsAnswer.value_counts()
                else:
                    print('skipping {}'.format(list(annotationDataset.groupby('thread').get_group(thread).annotator1Name)[0]))
                    count1 = pandas.Series({-1:-1})
                if list(annotationDataset.groupby('thread').get_group(thread).annotator3Name)[0] in allowedannotators:
                    count2 = annotationDataset.groupby('thread').get_group(thread).annotator3IsAnswer.value_counts()
                else:
                    print('skipping {}'.format(list(annotationDataset.groupby('thread').get_group(thread).annotator3Name)[0]))
                    count2 = pandas.Series({-1:-1})
            elif feature == 'CallToAction':
                if list(annotationDataset.groupby('thread').get_group(thread).annotator1Name)[0] in allowedannotators:
                    count1 = annotationDataset.groupby('thread').get_group(thread).annotator1CallToAction.value_counts()
                else:
                    print('skipping {}'.format(list(annotationDataset.groupby('thread').get_group(thread).annotator1Name)[0]))
                    count1 = pandas.Series({-1:-1})
                if list(annotationDataset.groupby('thread').get_group(thread).annotator3Name)[0] in allowedannotators:
                    count2 = annotationDataset.groupby('thread').get_group(thread).annotator3CallToAction.value_counts()
                else:
                    print('skipping {}'.format(list(annotationDataset.groupby('thread').get_group(thread).annotator3Name)[0]))
                    count2 = pandas.Series({-1:-1})
            elif feature == 'AskEmpathy':
                if list(annotationDataset.groupby('thread').get_group(thread).annotator1Name)[0] in allowedannotators:
                    count1 = annotationDataset.groupby('thread').get_group(thread).annotator1AskEmpathy.value_counts()
                else:
                    print('skipping {}'.format(list(annotationDataset.groupby('thread').get_group(thread).annotator1Name)[0]))
                    count1 = pandas.Series({-1:-1})
                if list(annotationDataset.groupby('thread').get_group(thread).annotator3Name)[0] in allowedannotators:
                    count2 = annotationDataset.groupby('thread').get_group(thread).annotator3AskEmpathy.value_counts()
                else:
                    print('skipping {}'.format(list(annotationDataset.groupby('thread').get_group(thread).annotator3Name)[0]))
                    count2 = pandas.Series({-1:-1})
            elif feature == 'IsQuestion':
                if list(annotationDataset.groupby('thread').get_group(thread).annotator1Name)[0] in allowedannotators:
                    count1 = annotationDataset.groupby('thread').get_group(thread).annotator1IsQuestion.value_counts()
                else:
                    print('skipping {}'.format(list(annotationDataset.groupby('thread').get_group(thread).annotator1Name)[0]))
                    count1 = pandas.Series({-1: -1})
                if list(annotationDataset.groupby('thread').get_group(thread).annotator3Name)[0] in allowedannotators:
                    count2 = annotationDataset.groupby('thread').get_group(thread).annotator3IsQuestion.value_counts()
                else:
                    print('skipping {}'.format(list(annotationDataset.groupby('thread').get_group(thread).annotator3Name)[0]))
                    count2 = pandas.Series({-1: -1})
        elif threadstodo.loc[threadstodo['name'] == thread].annotator3.values[0] == annotator:
            if feature == 'IsEmpathy':
                if list(annotationDataset.groupby('thread').get_group(thread).annotator1Name)[0] in allowedannotators:
                    count1 = annotationDataset.groupby('thread').get_group(thread).annotator1IsEmpathy.value_counts()
                else:
                    print('skipping {}'.format(
                        list(annotationDataset.groupby('thread').get_group(thread).annotator1Name)[0]))
                    count1 = pandas.Series({-1: -1})
                if list(annotationDataset.groupby('thread').get_group(thread).annotator2Name)[0] in allowedannotators:
                    count2 = annotationDataset.groupby('thread').get_group(thread).annotator2IsEmpathy.value_counts()
                else:
                    print('skipping {}'.format(list(annotationDataset.groupby('thread').get_group(thread).annotator2Name)[0]))
                    count2 = pandas.Series({-1: -1})
            elif feature == 'IsAnswer':
                if list(annotationDataset.groupby('thread').get_group(thread).annotator1Name)[0] in allowedannotators:
                    count1 = annotationDataset.groupby('thread').get_group(thread).annotator1IsAnswer.value_counts()
                else:
                    print('skipping {}'.format(list(annotationDataset.groupby('thread').get_group(thread).annotator1Name)[0]))
                    count1 = pandas.Series({-1: -1})
                if list(annotationDataset.groupby('thread').get_group(thread).annotator2Name)[0] in allowedannotators:
                    count2 = annotationDataset.groupby('thread').get_group(thread).annotator2IsAnswer.value_counts()
                else:
                    print('skipping {}'.format(list(annotationDataset.groupby('thread').get_group(thread).annotator2Name)[0]))
                    count2 = pandas.Series({-1:-1})
            elif feature == 'CallToAction':
                if list(annotationDataset.groupby('thread').get_group(thread).annotator1Name)[0] in allowedannotators:
                    count1 = annotationDataset.groupby('thread').get_group(thread).annotator1CallToAction.value_counts()
                else:
                    print('skipping {}'.format(list(annotationDataset.groupby('thread').get_group(thread).annotator1Name)[0]))
                    count1 = pandas.Series({-1:-1})
                if list(annotationDataset.groupby('thread').get_group(thread).annotator2Name)[0] in allowedannotators:
                    count2 = annotationDataset.groupby('thread').get_group(thread).annotator2CallToAction.value_counts()
                else:
                    print('skipping {}'.format(list(annotationDataset.groupby('thread').get_group(thread).annotator2Name)[0]))
                    count2 = pandas.Series({-1:-1})
            elif feature == 'AskEmpathy':
                if list(annotationDataset.groupby('thread').get_group(thread).annotator1Name)[0] in allowedannotators:
                    count1 = annotationDataset.groupby('thread').get_group(thread).annotator1AskEmpathy.value_counts()
                else:
                    print('skipping {}'.format(list(annotationDataset.groupby('thread').get_group(thread).annotator1Name)[0]))
                    count1 = pandas.Series({-1:-1})
                if list(annotationDataset.groupby('thread').get_group(thread).annotator2Name)[0] in allowedannotators:
                    count2 = annotationDataset.groupby('thread').get_group(thread).annotator2AskEmpathy.value_counts()
                else:
                    print('skipping {}'.format(list(annotationDataset.groupby('thread').get_group(thread).annotator2Name)[0]))
                    count2 = pandas.Series({-1:-1})
            elif feature == 'IsQuestion':
                if list(annotationDataset.groupby('thread').get_group(thread).annotator1Name)[0] in allowedannotators:
                    count1 = annotationDataset.groupby('thread').get_group(thread).annotator1IsQuestion.value_counts()
                else:
                    print('skipping {}'.format(list(annotationDataset.groupby('thread').get_group(thread).annotator1Name)[0]))
                    count1 = pandas.Series({-1:-1})
                if list(annotationDataset.groupby('thread').get_group(thread).annotator2Name)[0] in allowedannotators:
                    count2 = annotationDataset.groupby('thread').get_group(thread).annotator2IsQuestion.value_counts()
                else:
                    print('skipping {}'.format(list(annotationDataset.groupby('thread').get_group(thread).annotator2Name)[0]))
                    count2 = pandas.Series({-1:-1})
        try:
            if count1.keys()[0] == 0:
                totalFalse1.append(count1[0])
        except:
            pass
        try:
            if count2.keys()[0] == 0:
                totalFalse2.append(count2[0])
        except:
            pass
        try:
            if count1.keys()[0] == 1:
                totalTrue1.append(count1[0])
        except:
            pass
        try:
            if count2.keys()[0] == 1:
                totalTrue2.append(count2[0])
        except:
            pass
    combined_val_counts1 = [sum(totalTrue1), sum(totalFalse1)]
    combined_val_counts2 = [sum(totalTrue2), sum(totalFalse2)]
    if sum(combined_val_counts1) != 0:
        normalized_val_counts1 = combined_val_counts1[0] / sum(combined_val_counts1)
    else:
        normalized_val_counts1 = 0
    if sum(combined_val_counts2) != 0:
        normalized_val_counts2 = combined_val_counts2[0] / sum(combined_val_counts2)
    else:
        normalized_val_counts2 = 0
    return normalized_val_counts, (normalized_val_counts1 + normalized_val_counts2)/2


def groupedbarplot_annotatorgroups(groups, labels, threshold, title):
    width = 0.4

    x = numpy.arange(len(groups[0]))
    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width / 2, groups[0], width, label='Annotator',color="#1e88e5")
    rects2 = ax.bar(x + width / 2, groups[1], width, label='Others', color="#fbc02d")
    plt.axhline(threshold[0])
    plt.axhline(threshold[1])
    ax.set_ylabel('Proportion {}'.format(title))
    ax.set_title('{} label proportions for each annotator'.format(title))
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=45, ha="right")
    ax.legend()
    fig.tight_layout()

    plt.show()


def singlebarplot(values, mean, stdev):
    width = 0.4

    x = numpy.arange(len(values))
    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width / 2, values, width, label='Annotator', color="#1e88e5")

    plt.axhline(-1*mean)
    plt.axhline(mean)
    plt.axhline(0)
    plt.axhline(-1*mean - 1*stdev, ls='--')
    plt.axhline(mean + stdev, ls='--')
    plt.axhline(-1*mean - 2*stdev, ls='-.')
    plt.axhline(mean + 2*stdev, ls='-.')
    plt.text(-5, mean + 2*stdev, '2 stdevs', ha='left', va='bottom')
    plt.text(-5, mean + stdev, '1 stdev', ha='left', va='bottom')
    plt.text(-5, mean, 'mean', ha='left', va='bottom')
    plt.text(-5, -1*mean, 'mean', ha='left', va='bottom')
    plt.text(-5, -1*mean - 1*stdev, '1 stdev', ha='left', va='bottom')
    plt.text(-5, -1*mean - 2*stdev, '2 stdevs', ha='left', va='bottom')

    plt.text(-5, mean + 2*stdev, round(mean +2*stdev,2), ha='left', va='top')
    plt.text(-5, mean + stdev, round(mean + stdev,2), ha='left', va='top')
    plt.text(-5, mean, round(mean ,2), ha='left', va='top')
    plt.text(-5, -1*mean, round(mean,2), ha='left', va='top')
    plt.text(-5, -1*mean - 1*stdev, round(mean + stdev,2), ha='left', va='top')
    plt.text(-5, -1*mean - 2*stdev, round(mean + 2*stdev, 2), ha='left', va='top')

    def autolabel(rects):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for i, rect in enumerate(rects):
            height = rect.get_height()
            # if height >= 0:
            #     ax.annotate(i + 1,
            #                 xy=(rect.get_x() + rect.get_width() / 2, 0),
            #                 xytext=(0, -20),
            #                 textcoords="offset points",
            #                 ha='center', va='bottom', rotation=90
            #                 )
            # elif height >= -1*mean-stdev:
            #     ax.annotate(i + 1,
            #                 xy=(rect.get_x() + rect.get_width() / 2, height),
            #                 xytext=(0, -15),
            #                 textcoords="offset points",
            #                 ha='center', va='bottom', rotation=90
            #
            #                 )
            if height > (mean + stdev):
                ax.annotate('{}:{}'.format(i + 1, round(height, 2)),
                            xy=(rect.get_x() + rect.get_width() / 2, height),
                            xytext=(0, 3),  # 3 points vertical offset
                            textcoords="offset points",
                            ha='center', va='bottom', rotation=90)
            if height < (-1*mean - stdev):
                ax.annotate('{}: {}'.format(i + 1, round(height, 2)),
                            xy=(rect.get_x() + rect.get_width() / 2, height),
                            xytext=(0, -5),  # 3 points vertical offset
                            textcoords="offset points",
                            ha='center', va='top', rotation=90)

    autolabel(rects1)
    ax.set_ylabel('Mean differences')
    ax.set_title('Mean differences between annotators and co-annotators')
    ax.set_ylim(min(values)-.1, max(values)+.1)
    # ax.set_xticks(x)
    # ax.set_xticklabels([i+1 for i in x])
    ax.legend()
    fig.tight_layout()

    plt.show()


if __name__ == "__main__":
    annotationDataset = pandas.read_pickle("..\\language_model\\data\\combined_final.pickle")
    threadstodo = pandas.read_pickle("..\\language_model\\data\\threadstodo_2020-12-01_09-15-02.759611.pickle")
    with open('data\\allnameslist.pickle', 'rb') as file:
        allnameslist = pickle.load(file)
    # features = ['CallToAction', 'IsEmpathy', 'IsAnswer', 'AskEmpathy', 'IsQuestion']
    features = ['IsQuestion']
    print('checking feature {}'.format(features[0]))
    # differences = calculate_differences(features, allnameslist)
    removedAnnotators = ['Mar258', 'A1M987KDHQYKY7', 'AMEQUH2AXDPR2', 'A28LMUIZO84GAX']
    differences = calculate_differences(features, [x for x in allnameslist if x not in removedAnnotators])
    with open('data\\differences_2_{}.pickle'.format(features[0]), 'wb') as file:
        pickle.dump(differences, file)
    # differences1 = differences.copy()
    #
    # diffstdev = stdev(differences)
    # diffmean = mean(differences)
    # removedAnnotators = []
    # removedAnnotatorsIndex = []
    # for i, diff in enumerate(differences):
    #     if diff > (diffmean + diffstdev) or diff < (diffmean - diffstdev):
    #         removedAnnotatorsIndex.append(i)
    #         removedAnnotators.append(allnameslist[i])
    # for i in removedAnnotatorsIndex[::-1]:
    #     del differences[i]
    # print("annotators {} removed".format(removedAnnotators))
    # differences2 = calculate_differences(features, [x for x in allnameslist if x not in removedAnnotators])
    #
    # for annotatorindex in [allnameslist.index(removedAnnotator) for removedAnnotator in removedAnnotators]:
    #     differences2.insert(annotatorindex, 0)
    # groupedbarplot_annotatorgroups([differences1, differences2],allnameslist, [diffmean-diffstdev, diffmean+diffstdev], 'title')
    # singlebarplot(differences)