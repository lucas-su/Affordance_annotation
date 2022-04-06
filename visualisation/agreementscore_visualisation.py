from statistics import mean, stdev
import numpy, csv
import matplotlib.pyplot as plt

def singlebarplot(values, mean, stdev):
    width = 0.4

    x = numpy.arange(len(values))
    fig, ax = plt.subplots(figsize=(20,10), dpi=100)

    rects1 = ax.bar(x - width / 2, values, width, label='Normal to high agreement', color="#1e88e5")
    rects2 = ax.bar(x - width / 2, [x if x < mean-stdev else 0 for x in values], width, label='Low agreement', color="#fbc02d")
    rects3 = ax.bar(x - width / 2, [x if x < mean-2*stdev else 0 for x in values], width, label='Very low agreement', color="#e64a19")
    plt.axhline(-1*mean)
    plt.axhline(mean)
    # plt.axhline(0)
    plt.axhline(mean - 1*stdev, ls='--')
    plt.axhline(mean + stdev, ls='--')
    plt.axhline(mean - 2*stdev, ls='-.')
    plt.axhline(mean + 2*stdev, ls='-.')
    plt.text(-7, mean + 2*stdev, '2 stdevs', ha='left', va='bottom')
    plt.text(-7, mean + stdev, '1 stdev', ha='left', va='bottom')
    plt.text(-7, mean, 'mean', ha='left', va='bottom')
    plt.text(-7, mean, 'mean', ha='left', va='bottom')
    plt.text(-7, mean - 1*stdev, '1 stdev', ha='left', va='bottom')
    plt.text(-7, mean - 2*stdev, '2 stdevs', ha='left', va='bottom')

    plt.text(-7, mean + 2*stdev-0.01, round(mean +2*stdev,2), ha='left', va='top')
    plt.text(-7, mean + stdev-0.01, round(mean + stdev,2), ha='left', va='top')
    plt.text(-7, mean-0.01, round(mean ,2), ha='left', va='top')
    plt.text(-7, mean-0.01, round(mean,2), ha='left', va='top')
    plt.text(-7, mean - 1*stdev-0.01, round(mean - stdev,2), ha='left', va='top')
    plt.text(-7, mean - 2*stdev-0.01, round(mean - 2*stdev, 2), ha='left', va='top')

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
            # if height > (mean + stdev):
            #     ax.annotate('{}:{}'.format(i + 1, round(height, 2)),
            #                 xy=(rect.get_x() + rect.get_width() / 2, height),
            #                 xytext=(0, 3),  # 3 points vertical offset
            #                 textcoords="offset points",
            #                 ha='center', va='bottom', rotation=90)
            if height < (mean - stdev):
                ax.annotate('{}: {}'.format(i + 1, round(height, 2)),
                            xy=(rect.get_x() + rect.get_width() / 2, 0),
                            xytext=(0, -5),  # 3 points vertical offset
                            textcoords="offset points",
                            ha='center', va='top', rotation=90)

    autolabel(rects1)
    ax.set_ylabel('Agreement scores', fontsize=18)
    # ax.set_title('Agreement between annotators and co-annotators for iteration {}'.format(int(iteration)+1), fontsize=19)
    ax.set_ylim(0, max(values)+.1) #min(values)-.2
    # ax.set_ylim(0,2.5)
    # ax.set_xticks(x)
    # ax.set_xticklabels([i+1 for i in x])
    ax.set_xlim(-8, values.__len__())
    plt.tick_params(
        axis='x',  # changes apply to the x-axis
        which='both',  # both major and minor ticks are affected
        bottom=False,  # ticks along the bottom edge are off
        top=False,  # ticks along the top edge are off
        labelbottom=False)  # labels along the bottom edge are off
    ax.legend(loc='upper right')
    fig.tight_layout()
    plt.savefig('C:\\Users\\lucas\\Documents\\Graduation\\figures\\plt\\agreementscore_no_doubling_{}'.format(int(iteration)+1), dpi=300)

    # plt.show()

if __name__ == "__main__":
    for iteration in ['0','1','2','3']:
        iteration0 ={}
        iteration1 = {}
        iteration2 = {}
        iteration3 = {}
        with open('..\\Utils\\data\\agreementscore_with_nan_correction_6.csv', 'r') as file:
            reader = csv.reader(file)
            linenum = 0
            for line in reader:
                # if not linenum == 0:
                if line:
                    if line[0] == '0':
                        iteration0[line[1]] = line[2]
                    if line[0] == '1':
                        iteration1[line[1]] = line[2]
                    if line[0] == '2':
                        iteration2[line[1]] = line[2]
                    if line[0] == '3':
                        iteration3[line[1]] = line[2]
                # linenum += 1
        # iteration1_old_removed = {}
        # for name in iteration0.keys():
        #     if float(iteration0[name]) >= 0.32:
        #         iteration1_old_removed[name] = iteration1[name]
        if iteration == '0':
            vals = [float(x) for x in iteration0.values()]
            # vals = [mean([1, 2* float(iteration0[annotator])]) for annotator in iteration0.keys()]
            # meanval0 = mean(vals0)
            # stdevval0 = stdev(vals0)
        elif iteration == '1':
            vals = [float(x) for x in iteration1.values()]
            # vals = [mean([mean([2* float(iteration0[annotator])]), 2*float(iteration1[annotator])]) for annotator in iteration1.keys()]
            # meanval = 1.1747900083884173
            # stdevval = 0.411394730240442
        elif iteration == '2':
            vals = [float(x) for x in iteration2.values()]
            # vals = [mean([2*float(iteration1[annotator]), 2*float(iteration2[annotator])]) for annotator in iteration2.keys()]
        elif iteration == '3':
            vals = [float(x) for x in iteration3.values()]
            # vals = [mean([2*float(iteration2[annotator]), 2*float(iteration3[annotator])]) for annotator in iteration3.keys()]
        # vals = [2*val for val in vals]
        meanval = mean(vals)
        stdevval = stdev(vals)
        singlebarplot(vals, meanval, stdevval)