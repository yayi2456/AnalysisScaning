import matplotlib.pyplot as plt
dp95= [0.1951, 0.2174, 0.2955, 0.268, 0.4516, 0.2, 0.62, 0.3765, 0.2, 0.4386]
dp100= [0.3284, 0.1957, 0.3415, 0.1633, 0.4286, 0.4416, 0.936, 0.7983, 0.513, 0.973]
dp150=[0.6905, 0.0, 0.7868, 0.6667, 0.3605, 0.8177, 0.8622, 0.3231, 0.7803, 0.9966]
dp160= [0.4677, 0.9635, 0.7744, 0.984, 0.386, 0.8963, 0.9965, 0.1351, 0.9885, 0.9896]
dp200=[0.6552, 0.9959, 0.9873, 0.9939, 0.6838, 0.9793, 0.9962, 0.629, 0.9734, 0.9976]

dp150=[0.375, 0.5625, 0.4724, 0.2578, 0.1818, 0.2254, 0.9139, 0.8051, 0.9962, 0.5212]
dp160=[0.7838, 0.3654, 0.3333, 0.4712, 0.9448, 0.9856, 0.9946, 0.7784, 0.7361, 0.994]

def subplot_me():
    xaxis=range(10)
    plt.figure()
    plt.title('delay percentile of each node')
    plt.subplot(231)
    plt.bar(xaxis,dp95)
    plt.ylim(0,1.0)
    plt.title('95 requests per node per epoch')
    plt.subplot(232)
    plt.bar(xaxis,dp100)
    plt.title('100 requests per node per epoch')
    plt.subplot(233)
    plt.bar(xaxis,dp150)
    plt.title('150 requests per node per epoch')
    plt.subplot(234)
    plt.bar(xaxis,dp160)
    plt.title('160 requests per node per epoch')
    plt.subplot(235)
    plt.bar(xaxis,dp200)
    plt.title('200 requests per node per epoch')
    
    plt.show()

if __name__=='__main__':
    subplot_me()