#
# Generator functions for various matplotlib plots
#
# See __main__ for usage explanation
#

import matplotlib.pyplot as plt


def generate_plot(z,y,x,nodes,layers,filename):
    """
    Generate plot: epochs vs generated text modified bleu score
    :param y: list of modified bleu score
    :param x: list of number of epochs
    """

    assert len(x) == len(y)
    assert len(x) == len(z)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.plot(x, y, 'ro', linestyle='--', color='r', label='Quality score')
    #for i, j in zip(x, y):
    #    ax.annotate("(%d, %.2f)" % (i, j), xy=(i + 10, j))

    plt.plot(x, z, 'ro', linestyle='--', color='b', label='Overfitting score')
    #for i, j in zip(x, z):
    #    ax.annotate("(%d, %.2f)" % (i, j), xy=(i + 10, j))

    plt.title('LSTM-RNN Training: ' + nodes + ' nodes, ' + layers + ' layer')
    plt.ylim(0.0, 1.0)
    plt.xlabel('Epochs')
    plt.ylabel('Modified BLEU Score')
    plt.legend(loc='upper left')
    #plt.show()
    plt.savefig('plots/' + filename + '.png')

if __name__ == '__main__':
    
    # Find below all the data that the plots in our final paper were generated from. 
    # x is the list of epochs, y is the list of quality metrics, and z is the list of overfit metrics
    # for text generated from weight files from different epochs for a particular LSTM-RNN configuration.

    # 128 nodes, 1 layer
    # from eval/eval-sherlock-4-1l-128n.txt
    #x=(10, 25, 50, 100, 150, 201, 250, 296, 351, 420, 450, 501, 554, 603, 655, 707)
    #y=(0.26846786961505226, 0.10227870170279553, 0.18461572302099583, 0.14951534018076051, 0.16820821319262422, 0.14798459399121525, 0.0602636655170068, 0.17017441768539213, 0.2487923167003286, 0.21858147897045235, 0.06151652316808356, 0.0539513350331463, 0.22439295184491517, 0.09057327729420017, 0.20366392177912393, 0.057373441086334534)
    #z=(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.26427831840118443, 0, 0)

    # 256 nodes, 1 layer
    # from eval/eval-sherlock-4-1l-256n.txt
    #x=(10, 25, 50, 100, 154, 194, 252, 302, 350, 401, 451, 505, 541)
    #y=(0.06767846488734539, 0.05025708839022766, 0.16504619191667017, 0.17698082440315904, 0.15864402585731205, 0.14730882087664054, 0.17567280876189875, 0.03746313988853144, 0.13457605387336366, 0.17993579598802284, 0.052760876078963063, 0.1213105827294185, 0.15891144491306872)
    #z=(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.2693466632631657, 0, 0)
    
    # 1024 nodes, 1 layer
    # from eval/eval-sherlock-4-1l-1024n.txt
    #x=(10, 25, 50, 78, 112, 154, 202, 254, 301, 355, 400, 436, 519, 547, 608, 638, 685, 747, 812, 891, 909)
    #y=(0.29752478554134326, 0.0997759089559363, 0.34681803844701536, 0.03201490743997056, 0.7181111650766473, 0.43316078187691287, 0.12252997172528347, 0.4654732677681353, 0.5927141651200241, 0.8719422616141561, 0.8819249784373815, 0.12899920637396287, 0.9588042224393037, 0.9650496102916104, 0.9342871756211043, 0.6216481229097076, 0.6776695152358914, 0.9594882281462972, 0.9205586490906075, 0.9547986778222574, 0.8814708558076952)
    #z=(0, 0, 0.26196281937593935, 0, 0.5615273241719938, 0.3206758623378994, 0.047051521384919526, 0.367210332974902, 0.5220715237237974, 0.810108987046919, 0.8423266931445371, 0, 0.9299058501221101, 0.9291107343307017, 0.9112336558044049, 0.5717941054880816, 0.6105277112929566, 0.9365758559800322, 0.8661104876905621, 0.9267670363805183, 0.8435730126396955)

    # 512/256 nodes, 2 layers
    # from eval/eval-sherlock-4-2l-512.256n.txt
    #x=(10, 25, 50, 75, 100, 150, 201, 251, 303, 350, 400, 452, 507, 551, 608, 653, 700, 755, 803, 835, 899, 968)
    #y=(0.049559105153475176, 0.055603544867114656, 0.19632210875519532, 0.23039213783026713, 0.20200330297343125, 0.25199168734129734, 0.28985078709917245, 0.39013041880077537, 0.4204169224574269, 0.988237246272058, 0.5733290637763985, 0.9387417063293018, 0.9760724046619889, 0.9093048835398857, 0.9488373858095701, 0.927535644644205, 0.9568327169549677, 0.8719219097163797, 0.6285902554479845, 0.798273646113933, 0.6429839550194523, 0.8788303434638343)
    #z=(0, 0, 0.12621774979764105, 0.13905680578997015, 0.041830459050886906, 0.05158140381429151, 0.07175743503749396, 0.1781707959160332, 0.24608995526429567, 0.9654613461547911, 0.4123068798642042, 0.8591670854528494, 0.9524886338459646, 0.8165288575644204, 0.8933773265583395, 0.8635827978126673, 0.9177113561122987, 0.8120958924357704, 0.5248771428544192, 0.7180754559392909, 0.5423375204804449, 0.8145211132997765)

    # The uncommented selection below is an example for a configuration with 512 nodes and 1 layer.

    # 512 nodes, 1 layer
    # from eval/eval-sherlock-4-1l-512n.txt
    x=(10, 25, 50, 100, 153, 203, 251, 304, 356, 406, 458, 503, 551, 602, 653, 704, 755, 800, 870, 905, 950, 991)
    y=(0.08042825006705723, 0.1538783216259101, 0.11612527604455962, 0.3789348647505896, 0.2631536953415491, 0.13312718700691428, 0.5044047267987788, 0.3832290318661171, 0.4259141882144608, 0.34542396824092453, 0.22149532852210305, 0.5536791524853111, 0.15281203083089248, 0.4528333703818216, 0.6121231131881659, 0.6959895584449027, 0.3090461578718035, 0.3788688504864227, 0.3762870333299695, 0.6403367884498243, 0.5882853264101581, 0.5103826887884199)
    z=(0, 0, 0.022806503103401907, 0, 0.1632848002476029, 0.058845992280553344, 0.41806613804455844, 0.2840747498754383, 0.36038927287518263, 0.2516409834433342, 0.14346852716643577, 0.47170595851494773, 0, 0.3124727076514561, 0.5555327043398457, 0.6259281914401206, 0.22485471676248842, 0.2910888570913254, 0.2476755445416368, 0.5628850975934933, 0.5012235647523915, 0.4475411113182632)
    
    # nodes and layers for the plot title, and name of the file to save the plot (saved to plots/filename.png)
    nodes = "512"
    layers = "1"
    filename = "512n-1l"

    generate_plot(z,y,x,nodes,layers,filename)
