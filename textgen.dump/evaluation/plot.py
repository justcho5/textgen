#
# Generator functions for various matplotlib plots
#

import matplotlib.pyplot as plt


def generate_plot(y=(0.0836508963522, 0.166864061986, 0.242782762145, 0.740473459369, 0.961789417496),
                  x=(25, 50, 100, 250, 500)):
    """
    Generate plot: epochs vs generated text modified bleu score
    :param y: list of modified bleu score
    :param x: list of number of epochs
    """

    assert len(x) == len(y)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.plot(x, y, 'ro', linestyle='--', color='r', label='LSTM: 512 nodes X 2 layes')
    for i, j in zip(x, y):
        ax.annotate("(%d, %.2f)" % (i, j), xy=(i + 10, j))

    plt.xlabel('Epochs')
    plt.ylabel('Modified BLEU Score')
    plt.legend(loc='upper left')
    plt.show()

if __name__ == '__main__':
    generate_plot()
