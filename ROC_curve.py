import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

low = [np.arange(1, 9), "low"]  # Defines the column indexes for the low-level data.
high = [np.arange(9, 19), "high"]  # Defines the column indexes for the high-level data.
combined = [np.arange(1, 19), "comb"]  # Defines the column indexes for the combined data.

data_levels = [low, high, combined]
depth = ["shallow", "deep"]
PC_LIST = [6, 5, 9]


def roc_file_read(is_deep, data_level, pc):
    if pc == 0:
        file_name = "ROC/" + depth[is_deep] + "_" + data_level[1] + "_ROC.csv"

    else:
        file_name = "ROC/" + depth[is_deep] + "_" + data_level[1] + "_" + str(pc) + "_ROC.csv"

    data = pd.read_csv(file_name)

    return data["tpr"], data["fpr"], data.loc[0].at["auc"]


def roc_curve_plotter(is_deep, pca):
    fig = plt.figure()
    ax = fig.add_subplot(111)

    colours = ["r", "b", "k"]

    for m, data_level in enumerate(data_levels):
        if pca != 0:
            pc = PC_LIST[m]

        else:
            pc = 0

        tpr, fpr, auc = roc_file_read(is_deep, data_level, pc)

        if pca == 0:
            ax.plot(tpr, 1 - fpr, label=data_level[1] + " " + depth[is_deep] + " AUC = {0:.3f}".format(auc),
                    color=colours[m])

        else:
            ax.plot(tpr, 1 - fpr, label=data_level[1] + " " + depth[is_deep] + " AUC = {0:.3f}".format(auc),
                    color=colours[m])

    ax.set_xlabel('Signal efficiency', fontsize=12)
    ax.set_ylabel('Background rejection', fontsize=12)
    ax.set_xlim(-0.01, 1.01)
    ax.set_ylim(-0.01, 1.01)
    ax.grid(True, which="both")
    ax.legend(loc='lower left', fontsize=12)

    if pca == 0:
        ax.set_title("ROC curve SUSY dataset using a " + depth[is_deep] + " network", fontsize=12)
        plt.savefig("ROC/ROC_curve_" + depth[is_deep] + ".pdf", dpi=300)

    else:
        ax.set_title("ROC curve SUSY dataset using a " + depth[is_deep] + " network and PCA", fontsize=12)
        plt.savefig("ROC/ROC_curve_" + depth[is_deep] + "_PCA.pdf", dpi=300)


def learning_file_read(is_deep, data_level, pc):
    if pc == 0:
        file_name = "History/" + depth[is_deep] + "_" + data_level[1] + ".csv"

    else:
        file_name = "History/" + depth[is_deep] + "_" + data_level[1] + "_" + str(pc) + ".csv"

    data = pd.read_csv(file_name)

    return data["epoch"], data["accuracy"]*100, data["loss"]*100, data["val_accuracy"]*100, data["val_loss"]*100


def learning_curve_plotter(is_deep, pca):
    fig, axes = plt.subplots(1, 2, figsize=(15, 7))

    colours, fmts = ["r", "b", "k"], ["--r", "--b", "k--k"]

    for m, data_level in enumerate(data_levels):
        if pca != 0:
            pc = PC_LIST[m]

        else:
            pc = 0

        epoch, accuracy, loss, val_accuracy, val_loss = learning_file_read(is_deep, data_level, pc)

        axes[0].plot(epoch, accuracy, label=data_level[1] + " " + depth[is_deep], color=colours[m])
        #axes[0].plot(epoch, val_accuracy, label="validation " + data_level[1] + " " + depth[is_deep], color=colours[m],
                     #linestyle='dashed')

        axes[1].plot(epoch, loss, label=data_level[1] + " " + depth[is_deep], color=colours[m])
        #axes[1].plot(epoch, loss, label="Validation" + data_level[1] + " " + depth[is_deep], color=colours[m],
                     #linestyle='dashed')

    for i in range(2):
        axes[i].set_xlabel('Epoch', fontsize=12)
        axes[i].set_xlim(0, 150)
        axes[i].grid(True, which="both")
        axes[i].legend(loc='lower right', fontsize=12)

    axes[0].set_ylabel('Accuracy (%)', fontsize=12)
    axes[0].set_ylim(50, 80)

    axes[1].set_ylabel('Loss (%)', fontsize=12)
    axes[1].set_ylim(40, 70)

    if pca == 0:
        plt.savefig("History/Learning_curve_" + depth[is_deep] + ".pdf", dpi=300)
        axes[0].set_title("Learning curve SUSY dataset using a " + depth[is_deep] + " network", fontsize=12)
        axes[1].set_title("Loss curve SUSY dataset using a " + depth[is_deep] + " network", fontsize=12)


    else:
        plt.savefig("History/Learning_curve_" + depth[is_deep] + "_PCA.pdf", dpi=300)
        axes[0].set_title("Learning curve SUSY dataset using a " + depth[is_deep] + " network and PCA", fontsize=12)
        axes[1].set_title("Loss curve SUSY dataset using a " + depth[is_deep] + " network and PCA", fontsize=12)


def main():
    for n in range(2):
        roc_curve_plotter(n, 0)
        learning_curve_plotter(n, 0)


def pca_main():
    for n in range(2):
        roc_curve_plotter(n, 1)
        learning_curve_plotter(n, 1)


main()
pca_main()
