import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
from datetime import datetime
from SecretColors import Palette

def addperiod(start, end, level, height, name, color, textcolor='black'):
    period = datetime.strptime(end, "%Y-%m-%d")-datetime.strptime(start, "%Y-%m-%d")
    ax.barh(level, period.days, left=datetime.strptime(start, "%Y-%m-%d"), align='edge', label=name, height=height, color=color)
    ax.text((datetime.strptime(start, "%Y-%m-%d")+period/2), level + height/2, name, ha='center', va='center', color=textcolor)

def addarrow(start, end, level):
    period = datetime.strptime(end, "%Y-%m-%d") - datetime.strptime(start, "%Y-%m-%d")
    ax.arrow(datetime.strptime(start, "%Y-%m-%d"), level+0.5, period.days-0.8, 0, head_width=0.1, head_length=0.8, head_starts_at_zero = False)
    ax.arrow(datetime.strptime(start, "%Y-%m-%d")+period, level+0.5, -period.days+0.8, 0, head_width=0.1, head_length=0.8, head_starts_at_zero = False)
    ax.plot([datetime.strptime(start, "%Y-%m-%d")+period, datetime.strptime(start, "%Y-%m-%d")+period], [level+0.5, 0], ls='dotted', color='black')

def addtimeline(names, dates, levels):
    dates = [datetime.strptime(d, "%Y-%m-%d") for d in dates]



    markerline, stemline, baseline = ax.stem(dates, levels,
                                             linefmt="C3-", basefmt="k-",
                                             use_line_collection=True)

    plt.setp(markerline, mec="k", mfc="w", zorder=3)

    # Shift the markers to the baseline by replacing the y-data by zeros.
    markerline.set_ydata(np.zeros(len(dates)))

    # annotate lines
    vert = np.array(['top', 'bottom'])[(levels > 0).astype(int)]
    rot = np.array([0, 0])[(levels > 0).astype(int)]
    for d, l, r, va, rot in zip(dates, levels, names, vert, rot):
        ax.annotate(r, xy=(d, l), xytext=(-3, np.sign(l)*3),
                    textcoords="offset points", va=va, ha="right", backgroundcolor='white', rotation=rot)


if __name__ == "__main__":
    # Create figure and plot a stem plot with the date
    fig, ax = plt.subplots(figsize=(8.8, 4), constrained_layout=True)
    ax.set(title="Planning (lower) and outcome (upper) timelines")

    palette = Palette()

    planning = {'Finish model for dependency builder': '2020-04-25',
                'Midterm presentation ARP': '2020-04-29',
                'Finish scraper':'2020-05-15',
                'Finish data collection': '2020-05-30',
                'Finish annotator tool': '2020-06-15',
                'Final presentation ARP': '2020-06-30',
                'Finish depen-\ndency builder':'2020-08-01',
                'Have interviews planned': '2020-08-08',
                'Hand in draft research topics': '2020-09-01',
                'Start annotation datacollection':'2020-09-09',
                'Finish research topics': '2020-09-10',
                'Start data preparation code': '2020-09-20',
                'Preliminary test on\nannotated data so far': '2020-10-02',
                'Decide BERT vs\nembedding + LSTM': '2020-10-09',
                'Hand in draft report': '2020-10-20',
                'Stop datacollection if not done': '2020-11-01',
                'Start optimizing empathy\ndetection model': '2020-11-06',
                'Start work on call for empathy model': '2020-11-20',
                'Finish work on model': '2020-12-08',
                'Finish final draft\n(green light version)':'2020-12-24',
                'Finish final version': '2021-01-15',
                '':'2021-02-01'
                }


    levels = np.tile([-1, -2, -3, -4, -5, -6],
                     int(np.ceil(len(list(planning.values())) / 6)))[:len(list(planning.values()))]
    addtimeline(list(planning.keys()), list(planning.values()), levels)

    reality = {'First meeting': '2020-03-17',
               'Start working on scraper': '2020-04-05',
               'Midterm presentation ARP': '2020-04-29',
               'Finish model for dependency builder': '2020-05-05',
               'Start annotator CLI program': '2020-05-06',
               'Finish scraper':'2020-06-24',
               'Change annotation CLI to website': '2020-06-25',
               'Final presentation ARP': '2020-06-30',
               'Finish data collection': '2020-07-04',
               'Have interviews planned': '2020-08-28',
               'Finish annotation website': '2020-08-30'}

    levels = np.tile([1, 2, 3, 4, 5],
                     int(np.ceil(len(list(reality.values())) / 5)))[:len(list(reality.values()))]
    addtimeline(list(reality.keys()), list(reality.values()), levels)

    addperiod('2021-01-25', '2021-02-01',-0.8, 0.8, 'Grad-\nuation\nweek', palette.blue(no_of_colors=4)[0])
    addperiod('2020-08-08','2020-08-25', 0, 0.8, 'Holiday', palette.blue(no_of_colors=4)[1])
    addperiod('2020-08-08', '2020-08-25', -0.8, 0.8, 'Holiday', palette.blue(no_of_colors=4)[1])
    addperiod('2020-12-25', '2021-01-04', -0.8, 0.8, 'Christ-\nmas\nholiday', palette.blue(no_of_colors=4)[2], textcolor='white')
    addperiod('2020-09-01','2020-09-09', -0.8, 0.8,'Inter\nviews', palette.blue(no_of_colors=4)[3], textcolor='white')
    addperiod('2020-09-01', '2020-09-14', 0, 0.8, 'Inter\nviews', palette.blue(no_of_colors=4)[3], textcolor='white')
    # addperiod('2020-04-25', '2020-05-05', -0.4, 0.4, '')
    # addperiod('2020-05-15', '2020-06-24', -0.4, 0.4, '')
    # addperiod('2020-05-30', '2020-07-04', -0.8, 0.4, '')
    addarrow('2020-04-25', '2020-05-05', -1) #dependecy builder
    addarrow('2020-05-15', '2020-06-24', -1) #scraper
    addarrow('2020-05-30', '2020-07-04', -2) #data collection
    addarrow('2020-06-15', '2020-08-30', -3) #annotation tool
    addarrow('2020-08-08', '2020-08-28', -2) #interviews


    # format xaxis with 4 month intervals
    ax.get_xaxis().set_major_locator(mdates.MonthLocator(interval=1))
    ax.get_xaxis().set_major_formatter(mdates.DateFormatter("%b %Y"))
    plt.setp(ax.get_xticklabels(), rotation=30, ha="right")

    # remove y axis and spines
    ax.get_yaxis().set_visible(False)
    for spine in ["left", "top", "right"]:
        ax.spines[spine].set_visible(False)
    # ax.get_yaxis().label.set_visible(True)
    ax.text(datetime.strptime('2020-02-17', "%Y-%m-%d"), 3, 'Execution', ha='center',va='center',
            rotation='vertical', fontsize=15)
    ax.text(datetime.strptime('2020-02-17', "%Y-%m-%d"), -3, 'Planning', ha='center', va='center',
            rotation='vertical', fontsize=15)
    ax.margins(y=0.1, x=0.1)
    # plt.legend((ax.arrow(0,0, 1, 0 )), ('arrow'))
    plt.show()