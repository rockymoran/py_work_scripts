import numpy as np
import pandas as pd
from scipy.stats import norm
import matplotlib.pyplot as plt


def all_instructor_scores():
    score_param = '2. Instructor'
    
    df = pd.read_csv(r'c:\Work\2-12-19_evals.csv')
    df = df.dropna()
    df.sort_values(by=score_param, ascending=True, inplace=True)

    scores = df[score_param]
    sigma = scores.std()
    mu = scores.mean()
    mean_label = 'Instructor mean (' + str(np.around(mu, 2)) + ')'
    std_label = 'Standard deviation (' + str(np.around(sigma, 2)) + ')'

    fit = norm.pdf(scores, mu, sigma)
    fig, ax1 = plt.subplots()

    # plot the histogram for the TIES scores. Save y (bins) for use in labels
    y, x, _ = ax1.hist(scores, color='r', zorder=0, label='Score Frequency')

    # plot twinned axis with normal distribution, a fill for standard deviation, and a vertical line at the mean
    ax2 = ax1.twinx()
    ax2.plot(scores, fit, '-0', label='Distribution')
    ax2.fill_between(scores, fit, 0, where=(scores < mu+sigma) & (scores > mu-sigma),
                     alpha=.6, label=std_label)
    ax2.axvline(mu, linestyle='--', color='b', label=mean_label)

    # set display of labels/legends and ticks
    ax1.set_xlabel('TIES Instructor Score')
    ax1.set_ylabel('Frequency')
    ax1.set_yticks(np.arange(0, y.max()+10, 10))
    ax2.set_ylim(0, max(fit)+.1)
    ax2.set_xlim(min(scores), 7)
    ax2.set_ylabel('')

    plt.title('Fall 2018 TIES Distribution \n All Haas Courses')
    ax1.legend(loc='upper center')
    ax2.legend(loc='center left')

    plt.show()


if __name__ == "__main__":
    all_instructor_scores()
