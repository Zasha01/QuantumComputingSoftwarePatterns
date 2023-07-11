
import matplotlib.pyplot as plt

import pandas as pd
import numpy as np


# Sample data
def plotCircuitDistribution(transpilation, optimization, backend):
    np.random.seed(0)
    data = pd.DataFrame({
        'approach': np.repeat(['seed', 'opt', 'back'], 3),
        'view': np.tile(['average', 'aggregated', 'fixed'], 3),
        'TopT1': transpilation[0] + optimization[0] + backend[0],  # adjust these values according to your data
        'TopT10': transpilation[1] + optimization[1] + backend[1],
        'Rest': transpilation[2] + optimization[2] + backend[2] , # The rest is the total shots - TopT1 - TopT10
    })

    # Combine 'approach' and 'view' into a single category
    data['category'] = data['approach'] + '-' + data['view']

    # Plot each rank in a separate barplot layer
    width = 0.35  # the width of the bars
    ind = np.arange(len(data))  # the x locations for the groups
    fig, ax = plt.subplots()

    ax.bar(ind - width/2, data['Rest'], width, label='Rest', color='lightcoral')
    ax.bar(ind - width/2, data['TopT10'], width, label='TopT10', color='indianred', bottom=data['Rest'])
    ax.bar(ind - width/2, data['TopT1'], width, label='TopT1', color='brown', bottom=data['Rest'] + data['TopT10'])

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Number of Circuits')
    ax.set_title('Circuit Distribution by Approach and View')
    ax.set_xticks(ind)
    ax.set_xticklabels(data['category'])
    ax.legend()

    fig.tight_layout()
    plt.show()

if __name__ == "__main__":
    transpilation = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    optimization = [[10, 11, 12], [13, 14, 15], [16, 17, 18]]
    backend = [[19, 20, 21], [22, 23, 24], [25, 26, 27]]
    plotCircuitDistribution(transpilation, optimization, backend)



