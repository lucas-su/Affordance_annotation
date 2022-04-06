from statistics import mean, stdev
import numpy, csv, pandas, pickle
import matplotlib.pyplot as plt

def histplot(values,values2, bins1, bins2):
    width = 0.4

    x = numpy.arange(len(values))
    fig, (ax, ax2) = plt.subplots(1,2,sharey=True,gridspec_kw={'width_ratios': [bins1.__len__(), bins2.__len__()]},figsize=(20,10), dpi=100)

    hist1 = ax.hist(values, bins1, color="#1e88e5")
    hist2 = ax2.hist(values2, bins2, color="#1e88e5")

    d=0.0075  # how big to make the diagonal lines in axes coordinates
    # arguments to pass to plot, just so we don't keep repeating them
    kwargs = dict(transform=ax.transAxes, color='k', clip_on=False)

    ax.plot((1 - d+0.0017, 1 + d-0.0017), (-d, +d), **kwargs)
    kwargs.update(transform=ax2.transAxes)
    d2 = 0.05
    ax2.plot((-d2, +d2), ( -d,  +d), **kwargs)

    ax.set_ylabel('Number of annotators', fontsize=18)
    ax.set_title('Annotation count distribution for iteration {}'.format(int(iteration)+1), fontsize=19)

    ax.spines['right'].set_visible(False)
    ax2.spines['left'].set_visible(False)
    ax2.set_yticks([])
    ax.set_yticks(numpy.arange(0,70,5))
    ax2.set_ylim(0,70)
    ax.set_yticklabels(numpy.arange(0, 70, 5))

    ax.set_xlim(min(bins1)-5, max(bins1)+5)
    ax.set_xticks(bins1)
    ax.set_xticklabels(bins1, rotation=45)
    ax2.set_xticks(bins2)
    ax2.set_xticklabels(bins2, rotation=45)

    fig.tight_layout()
    plt.savefig('C:\\Users\\lucas\\Documents\\Graduation\\figures\\plt\\frequency_count_{}'.format(iteration+1), dpi=300)

    # plt.show()

def groupedbarplot(valuesBefore,values2Before, values,values2, bins1, bins2):
    width = 0.4

    x = numpy.arange(len(values))
    fig, (ax, ax2) = plt.subplots(1,2,sharey=True,gridspec_kw={'width_ratios': [bins1.__len__(), bins2.__len__()]},figsize=(20,10), dpi=100)

    hist1 = ax.hist((valuesBefore, values), bins1, color=["#1e88e5", '#fbc02d'], label=['Before removal', 'After removal'])
    hist2 = ax2.hist((values2Before, values2), bins2, color=["#1e88e5", '#fbc02d'])

    d=0.0075  # how big to make the diagonal lines in axes coordinates
    # arguments to pass to plot, just so we don't keep repeating them
    kwargs = dict(transform=ax.transAxes, color='k', clip_on=False)

    ax.plot((1 - d+0.0017, 1 + d-0.0017), (-d, +d), **kwargs)
    kwargs.update(transform=ax2.transAxes)
    d2 = 0.05
    ax2.plot((-d2, +d2), ( -d,  +d), **kwargs)

    ax.set_ylabel('Number of annotators', fontsize=18)
    ax.set_title('Annotation count distribution before and after annotator removal', fontsize=19)

    ax.spines['right'].set_visible(False)
    ax2.spines['left'].set_visible(False)
    ax2.set_yticks([])
    ax.set_yticks(numpy.arange(0,55,5))
    ax2.set_ylim(0,55)
    ax.set_yticklabels(numpy.arange(0, 55, 5))

    ax.set_xlim(min(bins1)-5, max(bins1)+5)
    ax.set_xticks(bins1)
    ax.set_xticklabels(bins1, rotation=45)
    ax2.set_xticks(bins2)
    ax2.set_xticklabels(bins2, rotation=45)
    ax.legend()
    fig.tight_layout()
    plt.savefig('C:\\Users\\lucas\\Documents\\Graduation\\figures\\plt\\frequency_count_grouped_hist', dpi=300)

    # plt.show()


if __name__ == "__main__":
    # iteration = 3
    annotationDataset = pandas.read_pickle("..\\language_model\\data\\combined_final.pickle")
    dataBefore = []
    for iteration in [0,1,2,3]:
        # with open('..\\Utils\\data\\allnameslist.pickle', 'rb') as file:
        #     allnameslist = pickle.load(file)
        # data = []
        # removedannotators = ['AUFPXC0XZDM6I', 'A1R5U7VMS0NVXJ', 'A3GKQF2LCPC7P2', 'A3FGEB6UO5O6ZI', 'A3TZHINICFQZ55',
        #                      'A17MXJGHY1K4Q2', 'A2HDCSPSMKB2WG', 'A1Y9DCHJTW89LM', 'A1UZQDT3KFC77A','A3E9FY9IWAR90X',
        #                      'A1CDPZMO705DEQ', 'A23ATSM5CU43EI', 'Maru', 'ADTJF28QF3VKE', 'johny', 'JEYANTHI',
        #                      'A30TM32AO7OB3W', 'A2RBB56IYWJ2YZ', 'Jennifer Billiris', 'A27K5BAW3U9W6P', 'A70GUOHM5F8DC',
        #                      'A2D214FXNIM28I', 'A19LFT0F3JO9BP', 'AY1GRLXDMXELF', 'noyjhing', 'ARUN', 'gebruikersnaam',
        #                      'A28LMUIZO84GAX', 'AMEQUH2AXDPR2', 'A1W8PU7Z3JLV5B', 'Ik begrijp dat je je boos voelt',
        #                      'A23KAJRDVCVGOE', 'APGBKNB9G69GT', 'A2ECERIL4RF6FO', 'A1BOQAPANXDC0K', 'A1H6DME332958N',
        #                      'A3PIJWV36NY7U4', 'Efun/A1Y9D4RKC3BZQ3', 'michel ', 'A3MAM5PA42A7CW', 'A4QDCBGN79832',
        #                      'A3G479CZZJOSJ2', 'A161R7U61GXNFC', 'Aaa', 'ACI8PUCF5OPDC', 'A26BNL983RC4YZ', 'A2GZ468WSRF7WJ',
        #                      'A382SL9ROIY1P6', 'A2R5TVQYSZE74K', 'A1M987KDHQYKY7', 'A1YO75Q6M618HU', 'als gebruikersnaam.',
        #                      'A121QS3395N67M', 'A3NI8HMVCT7SOF', 'A25STPOLAHMLIA', 'Cock', 'A1R65GQL81PGIK',
        #                      'A1SBFOZG5J97Z1', 'A1XLJP8MM2H5DX', 'mtk', 'PHILIP']
        iterationdict ={}
        data =[]

        with open('..\\Utils\\data\\agreementscore_with_nan_correction_6.csv', 'r') as file:
            reader = csv.reader(file)
            linenum = 0
            for line in reader:
                # if not linenum == 0:
                if line:
                    if int(line[0]) == iteration:
                        iterationdict[line[1]] = line[2]


        for name in iterationdict.keys():
            data.append(annotationDataset.loc[annotationDataset['annotator1Name'] == name]['thread'].count() + \
                        annotationDataset.loc[annotationDataset['annotator2Name'] == name]['thread'].count() + \
                        annotationDataset.loc[annotationDataset['annotator3Name'] == name]['thread'].count())
        if iteration == 0:
            for name in iterationdict.keys():
                dataBefore.append(annotationDataset.loc[annotationDataset['annotator1Name'] == name]['thread'].count() + \
                            annotationDataset.loc[annotationDataset['annotator2Name'] == name]['thread'].count() + \
                            annotationDataset.loc[annotationDataset['annotator3Name'] == name]['thread'].count())
            data2Before = []
            for x in data:
                if x > 400:
                    data2Before.append(x)


        bins1 = list(numpy.arange(0, 400, 10))
        bins2 = list(numpy.arange(700, 750, 10))
        data2 = []
        for x in data:
            if x > 400:
                data2.append(x)
                data.pop(data.index(x))
        # histplot(data, data2, bins1, bins2)
    groupedbarplot(dataBefore, data2Before, data, data2, bins1, bins2)